# -*- coding: utf-8 -*-
#!/usr/bin/python3
#
# This script knocking on the port of your Pitboss games to
# find freezed games. Freezed games will be handled with
# the following strategy:
# 1. Simulate mouse click to close popups on virtual x display. (TODO)
# 2. Kill game. The game starting loop should restart the game.
# 3. If 2. fails restart with the previous save game.
#
# Requirements:
# - python3 -m pip install scapy
#
# Notes:
# - Script requires root/'sudo' to get access to the network traffic or…
# - … you can also use a copy of your python executable and run
#   sudo setcap cap_net_raw=+ep python3
#

import time
import socket
import sys
import os
import argparse
import logging
from collections import defaultdict
import traceback
import datetime
import subprocess
import shlex
from enum import Enum, unique

## Packets for sending fake client replies
# Add subfolders to python paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))
import ip as pyip_ip
import udp as pyip_udp

## Packet(s) for sniffing
from scapy.all import *

WATCHDOG_ARG_FILE = "pitboss_watchdog.args"


class PBNetworkConnection:
    def __init__(self, client_ip, client_port, server_ip, server_port,
                 packet_limit, now):
        self.client_ip = client_ip
        self.client_port = client_port
        self.server_ip = server_ip
        self.server_port = server_port

        self.packet_limit = packet_limit
        self.activity_timeout = 5 * 60

        self.number_unanswered_outgoing_packets = 0
        self.number_unanswered_incoming_packets = 0
        # Just unix timestamps
        self.time_last_outgoing_packet = time.time()
        self.time_last_incoming_packet = time.time()
        self.time_disconnected = None

        # This timestamp will be updated for a subset of all
        # outgoing packages.
        # We assume an active server due the creation of this object
        # to avoid false detection of inactivity.
        self.watchdog_last_active_server_ts = self.time_last_outgoing_packet

        logging.debug("Detecting new connection {}".format(self))

    def __str__(self):
        return 'connection[{}:{}->{}:{}]'.format(
            self.client_ip, self.client_port,
            self.server_ip, self.server_port)

    def __repr__(self):
        s = self.__str__()
        s += "#p: {}, t_in: {}, t_out: {}".format(
            self.number_unanswered_outgoing_packets,
            self.time_last_incoming_packet,
            self.time_last_outgoing_packet)
        if not self.is_active():
            s += ' inactive'
        return s

    def handle_server_to_client(self, payload, game, now):
        self.number_unanswered_outgoing_packets += 1
        self.time_last_outgoing_packet = now

        # logging.info("Package from Server, len={}".format( len(payload)))
        # logging.info("Content: {}".format(payload.hex()))

        # == Watchdog functionality ==
        # If the game hangs with a "save error" popup only packages with
        # payload length 3 or 8 will be send. For examples:
        #     (fefe) 640009
        #     (fefe) 0000590009dcdc01
        #     (fefe) 64000a
        #     (fefe) 00005a000adcdc01
        # udp prefix
        #
        # If the game runs normal most idle packages has a
        # payload length of 23, i. e
        # (fefe) 00023b000bfdffffff01ffffffff143f02003d02000001
        #
        # Thus, if we ignore packages with length 3 and 8 we've
        # got an indicator for the server sanity.

        if len(payload) not in [3, 8]:
            self.watchdog_last_active_server_ts = self.time_last_outgoing_packet
            game.network_reply()

        # TODO Check if we can also use different payload sizes here, but we
        # need to make sure the specific information about the
        # two 16bit numbers "A, B" is available.
        if len(payload) not in [23, 35]:
            return

        # This package could be indicate an upload error. Add the payload
        # for this client (destination IP) to an set. Force analysis
        # of the packages if an sufficient amount of packages reached.
        #
        # The length 35 occurs if the connections was aborted during the loading
        # of a game.

        if self.number_unanswered_outgoing_packets < self.packet_limit:
            return

        # TODO We could also check the time here,
        # but the packet count seems do be the better metric.
        self.disconnect(payload)

    def handle_client_to_server(self, payload, game, now):
        if self.number_unanswered_outgoing_packets > 100:
            logging.debug('Received client data at {} after {} server packets / {} seconds.'.
                          format(self,
                                 self.number_unanswered_outgoing_packets,
                                 now - self.time_last_incoming_packet))

        # logging.info("Package to Server, len={}".format(len(payload)))

        # Check if server is available. First check guarantee that
        # first package of new client do not produce false positives.
        #
        # Note: This simple approach does only work for periods > 20s!
        # If a single client try to join a blockaded game, at most
        # 20 seconds elapse between two packages.
        if(now - self.time_last_incoming_packet < 22
           and now - self.watchdog_last_active_server_ts > 18):
            game.no_network_reply()

        self.number_unanswered_outgoing_packets = 0
        self.time_last_incoming_packet = now

    def disconnect(self, payload):
        # TODO Throttle disconnects!
        # Send fake packet to stop upload
        # Structure of content:
        #     254 254 06 B (A+1) (7 bytes)
        #
        # First 2 bytes marks it as udp paket(?!)
        # Thrid bytes is command (close connection to client)
        #   B and A+1 are to 16 bit numbers where A and B
        #   are content of 'payload'

        aHi, aLow = payload[1], payload[2]
        bHi, bLow = payload[3], payload[4]
        a_plus_1 = (aHi * 256 + aLow + 1) % 65536

        data = bytes([254, 254, 6, bHi, bLow,
                      int(a_plus_1/256), (a_plus_1%256)])

        logging.info('Disconnecting client at {!r}'.format(self))
        upacket = pyip_udp.Packet()
        upacket.sport = self.client_port
        upacket.dport = self.server_port
        upacket.data = data

        ipacket = pyip_ip.Packet()
        ipacket.src = self.client_ip
        ipacket.dst = self.server_ip
        ipacket.df = 1
        ipacket.ttl = 64
        ipacket.p = 17

        ipacket.data = pyip_udp.assemble(upacket, False)
        raw_ip = pyip_ip.assemble(ipacket, 1)

        # Send fake packet to the PB server that looks like its coming from the client
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        except socket.error as e:
            logging.error('Socket could not be created: {}'.format(e))

        sock.sendto(raw_ip, (ipacket.dst, 0))
        self.time_disconnected = time.time()
        self.number_unanswered_outgoing_packets = 0

    def is_active(self):
        now = time.time()
        inactive_time = now - max(self.time_last_incoming_packet, self.time_last_outgoing_packet)
        return inactive_time < self.activity_timeout


class PBNetworkConnectionRegister:

    def __init__(self, packet_limit):
        self.packet_limit = packet_limit
        self.connections = {}
        self.last_cleanup = time.time()
        self.cleanup_interval = 2 * 60

    def get(self, client_ip, client_port, server_ip, server_port, now):
        # This is more efficient than .get, because then we don't have to create a useless Client object if
        # Already exists
        connection_id = (client_ip, client_port, server_ip, server_port)
        if connection_id not in self.connections:
            self.connections[connection_id] = PBNetworkConnection(
                client_ip=client_ip, client_port=client_port,
                server_ip=server_ip, server_port=server_port,
                packet_limit=self.packet_limit,
                now=now)
        return self.connections[connection_id]

    def cleanup(self):
        if (time.time() - self.last_cleanup) < self.cleanup_interval:
            return

        logging.debug('Starting cleanup for {} connections.'.format(len(self.connections)))
        keys_to_del = []
        for (con_id, con) in self.connections.items():
            logging.debug('{!r}'.format(con))
            if not con.is_active():
                keys_to_del.append(con_id)

        for con_id in keys_to_del:
            del self.connections[con_id]
        self.last_cleanup = time.time()


# Converts portlist in 2056-2060,2070 format to pcap filter format
# Note: Filter does not respect PB host ip"
def portlist_to_filter(portlist_str):
    port_str = "udp and ( "
    portlist_first = True
    portlist = str(portlist_str).split(',')
    for p in portlist:
        if p == "-1":
            logging.debug("Skip negative port number. "
                          "Check given arguments for invalid port/game folder.")
            continue

        portrange = p.split('-')
        if not portlist_first:
            port_str += " or "
        else:
            portlist_first = False

        if len(portrange) == 2:
            port_str += "portrange {}-{}".format(int(portrange[0]), int(portrange[1]))
        elif len(portrange) == 1:
            port_str += "port {}".format(int(portrange[0]))
        else:
            raise Exception("Failed to parse portlist '{}'".format(portlist_str))

    port_str += " )"
    
    if portlist_first:
        raise Exception("Failed to parse portlist '{}'. No valid ports given?!"
                        "".format(portlist_str))

    return port_str


# === Analyse Traffic ===
# Ideally this function should run forever, but in case of odd errors we return outside to wait a bit
def analyze_udp_traffic(device, ip_address, pcap_filter, connections, games, pcap_timeout):
    def pb_traffic_monitor_callback(pkt):

        if not (IP in pkt and UDP in pkt):
            # May be true if some port scanner knocks on PBServer port?!
            # The current traffic filter prevent getting such packets here.
            return

        assert IP in pkt, "No IP packet"
        assert UDP in pkt, "Packet is no UDP traffic"
        # print(pkt.summary())
        print("." if pkt[IP].src == ip_address else "c", end="", flush=True)

        ip = pkt[IP]
        udp = pkt[UDP]
        payload = udp.load
        now = time.time()  # In pycap already part of 'pkt' but not in scapy


        if ip.src == ip_address:
            game = games.get(udp.sport)
            connections.get(ip.dst, udp.dport,
                            ip.src, udp.sport,
                            now).handle_server_to_client(payload, game, now)
        elif ip.dst == ip_address:
            game = games.get(udp.dport)
            connections.get(ip.src, udp.sport,
                            ip.dst, udp.dport,
                            now).handle_client_to_server(payload, game, now)
        else:
            logging.warning('PB server matches neither source ({}) nor destination ({})'.
                            format(ip.src, ip.dst))


    continuous_capture_error_count = 0
    while True:
        connections.cleanup()
        try:
            if continuous_capture_error_count > 20:
                return

            sniff(prn=pb_traffic_monitor_callback
                  , filter=pcap_filter
                  , timeout=pcap_timeout
                  , store=0
                  , count=1
                  , iface=device  # None for sniffing on all.
                 )

        except Exception as e:
            logging.info('Capture.error: {}'.format(e))
            continuous_capture_error_count += 1
            continue

        # Capture looks good, lets reset error count
        continuous_capture_error_count = 0

# Strategies of watchdog
@unique
class Strategies(Enum):
    NO_STRATEGY = 0
    POPUP_CONFIRM = 1
    RESTART_SAVE = 2
    RESTART_OLD_SAVE = 3
    STOP_PB_SERVER = 4


# Store data for watchdog functionality
class ServerStatus:

    def __init__(self, altroot_and_port_str):
        path_port = altroot_and_port_str.split('=')

        self.path = path_port[0]
        self.game_id = os.path.basename(self.path)

        # Waiting time until next strategy will be used.
        self.strategy_timeout_s = 30
        self.latest_strategy = Strategies.NO_STRATEGY
        self.latest_strategy_ts = time.time()

        try:
            self.port = int(path_port[1])
        except Exception as e:
            self.port = self.get_port_from_ini(self.path)

    @staticmethod
    def get_port_from_ini(path):
        port = -1
        ini_path = os.path.join(path, "CivilizationIV.ini")
        try:
            f = open(ini_path, 'r')
            for line in f:
                if "Port=" in line[:5]:
                    port = int(line[5:])
                    break
            f.close()
        except IOError as e:
            logging.info("Can not read port from {}. Wrong altroot path?".format(ini_path))

        return port

    # Server is active. Reset watchdog
    def network_reply(self):
        if(self.latest_strategy != Strategies.NO_STRATEGY):
            logging.info("Server of game {} is online again. Reset strategies.".format(str(self.game_id)))
            self.latest_strategy = Strategies.NO_STRATEGY
            self.latest_strategy_ts = time.time()  # Reset on strategy changes only should be fine.

    # Server not responding. Try several awakening strategies.
    def no_network_reply(self):
        now = time.time()
        if(now - self.latest_strategy_ts < self.strategy_timeout_s):
            return
        self.latest_strategy_ts = now

        if self.latest_strategy == Strategies.NO_STRATEGY:
            self.latest_strategy = Strategies.POPUP_CONFIRM
            logging.info("Simulate mouse click in game {}.".format(str(self.game_id)))
            self.popup_confirm()
        elif self.latest_strategy == Strategies.POPUP_CONFIRM:
            self.latest_strategy = Strategies.RESTART_SAVE
            logging.info("Restart game {} with current save.".format(str(self.game_id)))
            self.restart_game(False)
        elif self.latest_strategy == Strategies.RESTART_SAVE:
            self.latest_strategy = Strategies.RESTART_OLD_SAVE
            logging.info("Restart game {} with previous save.".format(str(self.game_id)))
            self.restart_game(True)
        elif self.latest_strategy == Strategies.RESTART_OLD_SAVE:
            self.latest_strategy = Strategies.STOP_PB_SERVER
            logging.info("All restart strategies failed. Kill game {} and wait for manual recovery.".format(str(self.game_id)))
            self.stop_game()

    def popup_confirm(self):
        subprocess.call(os.path.join(os.path.dirname(__file__), ".",
                                     "confirmPopup.sh {}".format(self.game_id)), shell=True)

    def restart_game(self, previous_save=False):
        previous = "-p" if previous_save else ""
        subprocess.call(os.path.join(os.path.dirname(__file__), ".",
                                     "killPitboss.sh {} {}".format(previous, self.game_id)), shell=True)

    def stop_game(self):
        subprocess.call(os.path.join(os.path.dirname(__file__), ".",
                                     "killPitboss.sh -s {}".format(self.game_id)), shell=True)


class ServerStatuses:

    def __init__(self, game_list):
        self.games = {}
        games_str = str(game_list).split(',')
        for game_str in games_str:
            game = ServerStatus(game_str)
            self.games[game.port] = game

    def get_ports(self):
        p = [str(g.port) for g in self.games.values()]
        return ",".join(p)

    def get(self, key):
        return self.games[key]


def read_watchdog_args():
    try:
        args = ""
        with open(WATCHDOG_ARG_FILE, "r") as f:
            args = f.read()

        args = shlex.split(args)

    except IOError as e:
        logging.info("Can not read arguments from "
                     "'{}'.".format(WATCHDOG_ARG_FILE))
        args = sys.argv[1:]

    return args

class ErrorCatchingArgumentParser(argparse.ArgumentParser):
    bNoExit = False
    def exit(self, status=0, message=None):
        if status and self.bNoExit:
            raise Exception(message)
            return
        else:
            super().exit(status, message)
        exit(status)

    def parse_args(self, bNoExit=False, *largs, **kwargs):
        self.bNoExit = bNoExit
        return super().parse_args(*largs, **kwargs)

    def print_usage(self, *largs):
        if self.bNoExit:
            return
        super().print_usage(*largs)

def parse_arguments():    
    parser = ErrorCatchingArgumentParser(
        description='Tame the Civilization Pitboss Server to avoid spamming'
        'network packets to dead clients')

    parser.add_argument('network_interface', metavar='INTERFACE', type=str, help='The interface to listen to, e.g. eth0.')
    parser.add_argument('ip_address', metavar='IP', type=str, help='The IP address used for the PB server.')
    # parser.add_argument('port_list', metavar='PORTS', type=str, default='2056',
    #                    help='List of ports of the PB server, e.g. 2056-2060,2070.')
    parser.add_argument('game_list', metavar='GAMES', type=str, default='~/PBs/PB1[=2056]',
                        help='List of altroot directories. Syntax:\n Path[=Port][,...]\nThe port will read from CivilizationIV.ini if not given.')
    parser.add_argument('-c', '--packet_limit', metavar='COUNT', type=int, default=2000,
                        help='Number of stray packets after which the client is disconnected.')

    # Read args from stdin and fall back on content from
    # from pitboss_watchdog.args. 
    # The second variant will be used by the systemd unit.
    try:
        args = parser.parse_args(True, args=sys.argv[1:])
    except Exception as e:
        args = None
    else:
        logging.debug("Parsing of input arguments succeeds.")

    if not args:
        logging.debug("Parsing of input arguments failed. "
              "Fetch arguments from '{}'.".format(WATCHDOG_ARG_FILE))
        args = parser.parse_args(args=read_watchdog_args())

    return args


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    args = parse_arguments()
    games = ServerStatuses(args.game_list)
    port_list = games.get_ports()

    connections = PBNetworkConnectionRegister(packet_limit=args.packet_limit)

    logging.info("Pitboss upload killer running.")
    logging.info("Listening on: {} for ip: {}, ports: {}".format(args.network_interface, args.ip_address, port_list))

    while True:
        try:
            analyze_udp_traffic(args.network_interface, args.ip_address,
                                portlist_to_filter(port_list),
                                connections, games, pcap_timeout=500)
        except Exception as e:
            logging.error("Caught exception {}".format(e))
            traceback.print_exc()
        logging.warning("Taking a break before resuming analysis.")
        time.sleep(10)

main()

