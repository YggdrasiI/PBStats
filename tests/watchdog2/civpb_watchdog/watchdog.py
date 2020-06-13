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
# - pip install scapy
#
# Notes:
# - Script requires root/"sudo" to get access to the network traffic or…
# - … you can also use a copy of your python executable and run
#   sudo setcap cap_net_raw=+ep python3
#

import time
import socket
import sys
import os
import logging
from collections import defaultdict
import traceback
import datetime
import subprocess
import shlex
from enum import Enum, unique

import click
import click_log
import click_config_file

import toml

# Packets for sending fake client replies
from .pyip import ip as pyip_ip
from .pyip import udp as pyip_udp

# Packet(s) for sniffing
from scapy.all import sniff, IP, UDP

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


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

        logger.debug("Detecting new connection {}".format(self))

    def __str__(self):
        return "connection[{}:{}->{}:{}]".format(
            self.client_ip, self.client_port,
            self.server_ip, self.server_port)

    def __repr__(self):
        s = self.__str__()
        s += "#p: {}, t_in: {}, t_out: {}".format(
            self.number_unanswered_outgoing_packets,
            self.time_last_incoming_packet,
            self.time_last_outgoing_packet)
        if not self.is_active():
            s += " inactive"
        return s

    def handle_server_to_client(self, payload, game, now):
        self.number_unanswered_outgoing_packets += 1
        self.time_last_outgoing_packet = now

        # logger.info("Package from Server, len={}".format( len(payload)))
        # logger.info("Content: {}".format(payload.hex()))

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
        # Thus, if we ignore packages with length 3 and 8 we"ve
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
            logger.debug("Received client data at {} after {} server packets / {} seconds.".
                          format(self,
                                 self.number_unanswered_outgoing_packets,
                                 now - self.time_last_incoming_packet))

        # logger.info("Package to Server, len={}".format(len(payload)))

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
        #   are content of "payload"

        aHi, aLow = payload[1], payload[2]
        bHi, bLow = payload[3], payload[4]
        a_plus_1 = (aHi * 256 + aLow + 1) % 65536

        data = bytes([254, 254, 6, bHi, bLow,
                      int(a_plus_1/256), (a_plus_1%256)])

        logger.info("Disconnecting client at {!r}".format(self))
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
            logger.error("Socket could not be created: {}".format(e))

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
        # This is more efficient than .get, because then we don"t have to create a useless Client object if
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

        logger.debug("Starting cleanup for {} connections.".format(len(self.connections)))
        keys_to_del = []
        for (con_id, con) in self.connections.items():
            logger.debug("{!r}".format(con))
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
    portlist = str(portlist_str).split(",")
    for p in portlist:
        if p == "-1":
            logger.debug("Skip negative port number. "
                          "Check given arguments for invalid port/game folder.")
            continue

        portrange = p.split("-")
        if not portlist_first:
            port_str += " or "
        else:
            portlist_first = False

        if len(portrange) == 2:
            port_str += "portrange {}-{}".format(int(portrange[0]), int(portrange[1]))
        elif len(portrange) == 1:
            port_str += "port {}".format(int(portrange[0]))
        else:
            raise Exception('Failed to parse portlist "{}"'.format(portlist_str))

    port_str += " )"
    
    if portlist_first:
        raise Exception('Failed to parse portlist "{}". No valid ports given?!'
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
        # print("." if pkt[IP].src == ip_address else "c", end="", flush=True)

        ip = pkt[IP]
        udp = pkt[UDP]
        payload = udp.load
        now = time.time()  # In pycap already part of "pkt" but not in scapy

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
            logger.warning("PB server matches neither source ({}) nor destination ({})".
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
            logger.info("Capture.error: {}".format(e))
            continuous_capture_error_count += 1
            continue

        # Capture looks good, lets reset error count
        continuous_capture_error_count = 0

# Strategies of civpb_watchdog
@unique
class Strategies(Enum):
    NO_STRATEGY = 0
    POPUP_CONFIRM = 1
    RESTART_SAVE = 2
    RESTART_OLD_SAVE = 3
    STOP_PB_SERVER = 4


# Store data for civpb_watchdog functionality
class ServerStatus:
    def __init__(self, altroot_and_port_str, script_path):
        self.script_path = script_path
        path_port = altroot_and_port_str.split("=")

        self.path = path_port[0]
        self.game_id = os.path.basename(os.path.realpath(self.path))

        # Waiting time until next strategy will be used.
        self.strategy_timeout_s = 30
        self.latest_strategy = Strategies.NO_STRATEGY
        self.latest_strategy_ts = time.time()

        try:
            self.port = int(path_port[1])
        except IndexError:
            self.port = self.get_port_from_ini(self.path)
        logger.info(f"Setup ServerStatus game_id: {self.game_id} path: {self.path} port: {self.port}")

    @staticmethod
    def get_port_from_ini(path):
        port = None
        ini_path = os.path.join(path, "CivilizationIV.ini")
        try:
            with open(ini_path, "r") as f:
                for line in f:
                    if "Port=" in line[:5]:
                        port = int(line[5:])
                        break
        except IOError:
            logger.warning("Could not read port from {}. Wrong altroot path?".format(ini_path))
        if port is None:
            raise RuntimeError(f"No port found in ini file {ini_path}")
        return port

    # Server is active. Reset civpb_watchdog
    def network_reply(self):
        if self.latest_strategy != Strategies.NO_STRATEGY:
            logger.info("Server of game {} is online again. Reset strategies.".format(str(self.game_id)))
            self.latest_strategy = Strategies.NO_STRATEGY
            self.latest_strategy_ts = time.time()  # Reset on strategy changes only should be fine.

    # Server not responding. Try several awakening strategies.
    def no_network_reply(self):
        now = time.time()
        if (now - self.latest_strategy_ts) < self.strategy_timeout_s:
            return
        self.latest_strategy_ts = now

        if self.latest_strategy == Strategies.NO_STRATEGY:
            self.latest_strategy = Strategies.POPUP_CONFIRM
            logger.info("Simulate mouse click in game {}.".format(str(self.game_id)))
            self.popup_confirm()
        elif self.latest_strategy == Strategies.POPUP_CONFIRM:
            self.latest_strategy = Strategies.RESTART_SAVE
            logger.info("Restart game {} with current save.".format(str(self.game_id)))
            self.restart_game(False)
        elif self.latest_strategy == Strategies.RESTART_SAVE:
            self.latest_strategy = Strategies.RESTART_OLD_SAVE
            logger.info("Restart game {} with previous save.".format(str(self.game_id)))
            self.restart_game(True)
        elif self.latest_strategy == Strategies.RESTART_OLD_SAVE:
            self.latest_strategy = Strategies.STOP_PB_SERVER
            logger.info("All restart strategies failed. Kill game {} and wait for manual recovery.".format(str(self.game_id)))
            self.stop_game()

    def popup_confirm(self):
        subprocess.call([os.path.join(self.script_path, "civpb-confirm-popup"), str(self.game_id)])

    def restart_game(self, previous_save=False):
        args = ["-p"] if previous_save else []
        args.append(str(self.game_id))
        subprocess.call([os.path.join(self.script_path, "civpb-kill"), *args])

    def stop_game(self):
        subprocess.call([os.path.join(self.script_path, "civpb-kill"), "-s", str(self.game_id)])


class ServerStatuses:
    def __init__(self, games_str, script_path):
        self.games = {}
        for game_str in games_str:
            game = ServerStatus(game_str, script_path)
            self.games[game.port] = game

    def get_ports(self):
        p = [str(g.port) for g in self.games.values()]
        return ",".join(p)

    def get(self, key):
        return self.games[key]


def toml_provider(file_path, cmd_name):
    return toml.load(file_path)


@click.command()
@click.option("--interface", type=str, required=True, metavar="INTERFACE", help="The interface to listen to, e.g., eth0")
@click.option("--address", type=str, required=True, metavar="IP", help="The IP address used for the PB server.")
@click.option("-g", "--games", type=str, required=True, multiple=True, metavar="GAME",
              help="Altroot directory to a Pitboss game, syntax:\n Path[=Port]\nIf omitted, the port will read from CivilizationIV.ini.")
@click.option("-c", "--packet-limit", metavar="COUNT", type=int, default=2000,
              help="Number of stray packets after which the client is disconnected.")
@click.option("--script-path", default=sys.path[0], "path containing civpb-confirm-popup and civpb-kill scripts")
@click_config_file.configuration_option(provider=toml_provider)
@click_log.simple_verbosity_option()
def main(interface, address, games, packet_limit, script_path):
    print(games, script_path)
    servers = ServerStatuses(games, script_path=script_path)
    port_list = servers.get_ports()

    connections = PBNetworkConnectionRegister(packet_limit=packet_limit)

    logger.info("Pitboss upload killer running.")
    logger.info("Listening on: {} for ip: {}, ports: {}".format(interface, address, port_list))

    while True:
        try:
            analyze_udp_traffic(interface, address, portlist_to_filter(port_list),
                                connections, servers, pcap_timeout=500)
        except Exception as e:
            logger.error("Caught exception {}".format(e))
            traceback.print_exc()
        logger.warning("Taking a break before resuming analysis.")
        time.sleep(10)


if __name__ == "__main__":
    main()
