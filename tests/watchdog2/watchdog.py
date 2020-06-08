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
# - If you get the following error message:
#     '[...]ImportError: No module named sll'
#   , then remove 'ssl' from list in pycap/constants/__init__.py.
#
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

## Packets for sending fake client replies
# Add subfolders to python paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'python3-pyip-0.7'))
import ip as ip2
import udp as udp2

## Packet(s) for sniffing
from scapy.all import *


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

        # == Watchdog functionality ==
        # If the game hangs with a "save error" popup only packages with
        # payload length 5 or 10 will be send. Four examples:
        # fefe640009
        # fefe0000590009dcdc01
        # fefe64000a
        # fefe00005a000adcdc01
        #
        # If the game runs normal most idle packages has a
        # payload length of 25, i. e
        # fefe00023b000bfdffffff01ffffffff143f02003d02000001
        #
        # Thus, if we ignore packages with length 5 and 10 we've
        # got an indicator for the server sanity.
        #  logging.info("Package from Server, len={}".format(len(payload)))
        if len(payload) not in [5, 10]:
            self.watchdog_last_active_server_ts = self.time_last_outgoing_packet
            game.network_reply()

        # TODO Check if we can also use different payload sizes here, but we
        # need to make sure the specific
        # payload information "A, B" is available for this kind of packet!
        if len(payload) != 25 and len(payload) != 37:
            return

        # This package could be indicate an upload error. Add the payload
        # for this client (destination ip) to an set. Force analysation
        # of the packages if an sufficient amount of packages reached.
        #
        # The length 37 occours if the connections was aborted during the loading
        # of a game.

        if self.number_unanswered_outgoing_packets < self.packet_limit:
            return

        # TODO We could also check the time here,
        # but the packet count is a much better metric, because with the the packet rate is much higher than usually
        self.disconnect(payload)

    def handle_client_to_server(self, payload, game, now):
        if self.number_unanswered_outgoing_packets > 100:
            logging.debug('Received client data at {} after {} server packets / {} seconds.'.
                          format(self,
                                 self.number_unanswered_outgoing_packets,
                                 now - self.time_last_incoming_packet))

        # Check if server is available. First check guarantee that
        # first package of new client do not produce false positives.
        #
        # Note: This simple approach does only work for periods > 20s!
        # If a single client try to join a blockaded game, at most
        # 20 seconds elapse between two packages.
        # logging.info("Package to Server, len={}".format(len(payload)))
        if(now - self.time_last_incoming_packet < 22
           and now - self.watchdog_last_active_server_ts > 18):
            game.no_network_reply()

        self.number_unanswered_outgoing_packets = 0
        self.time_last_incoming_packet = now

    def disconnect(self, payload):
        # TODO Throttle disconnects!
        # Send fake packet to stop upload
        # Structure of content:
        # 254 254 06 B (A+1) (7 bytes)
        A = payload[3:5]  # String!
        B = payload[5:7]
        a1 = ord(A[0]) * 256 + ord(A[1]) + 1
        A1 = chr(int(a1 / 256)) + chr(a1 % 256)
        data = chr(254) + chr(254) + chr(6) + B + A1

        logging.info('Disconnecting client at {!r}'.format(self))
        upacket = udp2.Packet()
        upacket.sport = self.client_port
        upacket.dport = self.server_port
        upacket.data = data

        ipacket = ip2.Packet()
        ipacket.src = self.client_ip
        ipacket.dst = self.server_ip
        ipacket.df = 1
        ipacket.ttl = 64
        ipacket.p = 17

        ipacket.data = udp2.assemble(upacket, False)
        raw_ip = ip2.assemble(ipacket, 1)

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
            self.connections[connection_id] = PBNetworkConnection(client_ip=client_ip, client_port=client_port,
                                                                  server_ip=server_ip, server_port=server_port,
                                                                  packet_limit=self.packet_limit, now=now)
        return self.connections[connection_id]

    def cleanup(self):
        if (time.time() - self.last_cleanup) < self.cleanup_interval:
            return

        logging.debug('Starting cleanup for {} connections.'.format(len(self.connections)))
        for (con_id, con) in self.connections.items():
            logging.debug('{!r}'.format(con))
            if not con.is_active():
                del self.connections[con_id]
        self.last_cleanup = time.time()


# Converts portlist in 2056-2060,2070 format to pcap filter format
# Note: Filter does not respect PB host ip"
def portlist_to_filter(portlist_str):
    port_str = "udp and ( "
    portlist_first = True
    portlist = str(portlist_str).split(',')
    for p in portlist:
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
            raise Exception("Failed to parse portlist '{}'".format(port_str))

    port_str += " )"
    return port_str


# === Analyse Traffic ===
# Ideally this function should run forever, but in case of odd errors we return outside to wait a bit
def analyze_udp_traffic(device, ip_address, pcap_filter, connections, pcap_timeout):
    def pb_traffic_monitor_callback(paket):
        if packet is None:
            # Rueckstand von altem pcap-Ansatz.
            # Vllt jetzt bei Timeout ausgeloest.
            # This is fine. Simply traffic. Don't need to wait, timeout does that
            assert False, "Empty packet"
            return

        ip = packet[1]
        udp = packet[2]
        payload = packet[3]
        now = packet[4]
        assert isinstance(ip, pycap.protocol.ip)
        assert isinstance(udp, pycap.protocol.udp)

        if ip.source == ip_address:
            connections.get(ip.destination, udp.destinationport, ip.source, udp.sourceport, now).handle_server_to_client(payload, now)
        elif ip.destination == ip_address:
            connections.get(ip.source, udp.sourceport, ip.destination, udp.destinationport, now).handle_client_to_server(payload, now)
        else:
            logging.warning('PB server matches neither source ({}) nor destination ({})'.
                            format(ip.source, ip.destination))


    continuous_capture_error_count = 0
    while True:
        connections.cleanup()
        try:
            if continuous_capture_error_count > 20:
                return

            sniff(prn=pb_traffic_monitor_callback
                  # , filter="(port 8080 or port 8888)"
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


# Store data for watchdog functionalty
class ServerStatus:
    # Strategies of watchdog
    # (No Enum class in Python 2.7 available)
    NO_STRATEGY, POPUP_CONFIRM, RESTART_SAVE, RESTART_OLD_SAVE, STOP_PB_SERVER = range(5)

    def __init__(self, altroot_and_port_str):
        path_port = altroot_and_port_str.split('=')

        self.path = path_port[0]
        self.game_id = os.path.basename(self.path)

        # Waiting time until next strategy will be used.
        self.strategy_timeout_s = 30
        self.latest_strategy = ServerStatus.NO_STRATEGY
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
        if(self.latest_strategy != ServerStatus.NO_STRATEGY):
            logging.info("Server of game {} is online again. Reset strategies.".format(str(self.game_id)))
            self.latest_strategy = ServerStatus.NO_STRATEGY
            self.latest_strategy_ts = time.time()  # Reset on strategy changes only should be fine.

    # Server not responding. Try several awakening strategies.
    def no_network_reply(self):
        now = time.time()
        if(now - self.latest_strategy_ts < self.strategy_timeout_s):
            return
        self.latest_strategy_ts = now

        if self.latest_strategy == ServerStatus.NO_STRATEGY:
            self.latest_strategy = ServerStatus.POPUP_CONFIRM
            logging.info("Simulate mouse click in game {}.".format(str(self.game_id)))
            self.popup_confirm()
        elif self.latest_strategy == ServerStatus.POPUP_CONFIRM:
            self.latest_strategy = ServerStatus.RESTART_SAVE
            logging.info("Restart game {} with current save.".format(str(self.game_id)))
            self.restart_game(False)
        elif self.latest_strategy == ServerStatus.RESTART_SAVE:
            self.latest_strategy = ServerStatus.RESTART_OLD_SAVE
            logging.info("Restart game {} with previous save.".format(str(self.game_id)))
            self.restart_game(True)
        elif self.latest_strategy == ServerStatus.RESTART_OLD_SAVE:
            self.latest_strategy = ServerStatus.STOP_PB_SERVER
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


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        description='Tame the Civilization Pitboss Server to avoid spamming network packets to dead clients')

    parser.add_argument('network_interface', metavar='INTERFACE', type=str, help='The interface to listen to, e.g. eth0.')
    parser.add_argument('ip_address', metavar='IP', type=str, help='The IP address used for the PB server.')
    # parser.add_argument('port_list', metavar='PORTS', type=str, default='2056',
    #                    help='List of ports of the PB server, e.g. 2056-2060,2070.')
    parser.add_argument('game_list', metavar='GAMES', type=str, default='~/PBs/PB1[=2056]',
                        help='List of altroot directories. Syntax:\n Path[=Port][,...]\nThe port will read from CivilizationIV.ini if not given.')
    parser.add_argument('-c', '--packet_limit', metavar='COUNT', type=int, default=2000,
                        help='Number of stray packets after which the client is disconnected.')

    args = parser.parse_args()

    games = ServerStatuses(args.game_list)
    port_list = games.get_ports()

    connections = PBNetworkConnectionRegister(packet_limit=args.packet_limit)

    logging.info("Pitboss upload killer running.")
    logging.info("Listening on: {} for ip: {}, ports: {}".format(args.network_interface, args.ip_address, port_list))

    while True:
        try:
            analyze_udp_traffic(args.network_interface, args.ip_address,
                                portlist_to_filter(port_list),
                                connections, pcap_timeout=500)
        except Exception as e:
            logging.error("Caught exception {}".format(e))
            traceback.print_exc()
        logging.warning("Taking a break before resuming analysis.")
        time.sleep(10)

main()

