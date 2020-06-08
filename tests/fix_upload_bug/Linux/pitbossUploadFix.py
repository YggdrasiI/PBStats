#!/usr/bin/python3
#
# This script analyse your network traffic to
# detect the 'upload bug' which cause a massive paket spamming
# from a Civ4 Pitboss server. After a detection it fakes a udp paket
# with the content 'player X quit connection'.
#
# Requirements:
# - python3 -m pip install scapy
#
# Notes:
# - Script requires root/'sudo' to get access to the network traffici or… 
# - … you can also use a copy of your python executable and run
#   sudo setcap cap_net_raw=+ep python3
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
from enum import Enum, unique

## Packets for sending fake client replies
# Add subfolders to python paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'python3-pyip-0.7'))
import ip as ip2
import udp as udp2

## Packet(s) for sniffing
from scapy.all import *

class PBNetworkConnection:
    def __init__(self, client_ip, client_port, server_ip, server_port, packet_limit, now):
        self.client_ip = client_ip
        self.client_port = client_port
        self.server_ip = server_ip
        self.server_port = server_port

        self.packet_limit = packet_limit
        self.activity_timeout = 5 * 60

        self.number_unanswered_outgoing_packets = 0
        # Just unix timestamps
        self.time_last_outgoing_packet = None
        self.time_last_incoming_packet = None
        self.time_disconnected = None

        logging.debug("Detecting new connection {}".format(self))

    def __str__(self):
        return 'connection[{}:{}->{}:{}]'.format(self.client_ip, self.client_port,
                                                 self.server_ip, self.server_port)

    def __repr__(self):
        s = self.__str__()
        s += "#p: {}, t_in: {}, t_out: {}".format(self.number_unanswered_outgoing_packets,
                                                  self.time_last_incoming_packet,
                                                  self.time_last_outgoing_packet)
        if not self.is_active():
            s += ' inactive'
        return s

    def handle_server_to_client(self, payload, now):
        self.number_unanswered_outgoing_packets += 1
        self.time_last_outgoing_packet = now

        # need to make sure the specific information about the
        # two 16bit numbers "A, B" is available.
        if len(payload) not in [23, 35]:
            return

        # This package could be indicate an upload error. Add the payload
        # for this client (destination IP) to an set. Force analysis
        # of the packages if an sufficient amount of packages reached.
        #
        # The length 35 occours if the connections was aborted during the loading
        # of a game.

        if self.number_unanswered_outgoing_packets < self.packet_limit:
            return

        # TODO We could also check the time here,
        # but the packet count seems do be the better metric.
        self.disconnect(payload)

    def handle_client_to_server(self, payload, now):
        if self.number_unanswered_outgoing_packets > 100:
            logging.debug('Received client data at {} after {} server packets / {} seconds.'.
                          format(self,
                                 self.number_unanswered_outgoing_packets,
                                 now - self.time_last_incoming_packet))

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
            self.connections[connection_id] = PBNetworkConnection(
                client_ip=client_ip, client_port=client_port,
                server_ip=server_ip, server_port=server_port,
                packet_limit=self.packet_limit, now=now)
        return self.connections[connection_id]

    def cleanup(self):
        if (time.time() - self.last_cleanup) < self.cleanup_interval:
            return

        logging.debug('Starting cleanup for {} connections.'.format(len(self.connections)))
        keys_to_del = []
        for (con_id, con) in self.connections.items():
            logging.debug('{!r}'.format(con))
            if not con.is_active():
                del self.connections[con_id]
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



def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser(
        description='Tame the Civilization Pitboss Server to avoid spamming network packets to dead clients')
    # server_portlist contains list (seperated by ,)
    # of single ports (P) or portranges (P1-P2).
    #
    # format: (P|P1-P2)[,Q|Q1-Q2[,...]]
    #
    parser.add_argument('network_interface', metavar='INTERFACE', type=str, help='The interface to listen to, e.g. eth0.')
    parser.add_argument('ip_address', metavar='IP', type=str, help='The IP address used for the PB server.')
    parser.add_argument('port_list', metavar='PORTS', type=str, default='2056',
                        help='List of ports of the PB server, e.g. 2056-2060,2070.')
    parser.add_argument('-c', '--packet_limit', metavar='COUNT', type=int, default=2000,
                        help='Number of stray packets after which the client is disconnected.')

    args = parser.parse_args()

    connections = PBNetworkConnectionRegister(packet_limit=args.packet_limit)

    logging.info("Pitboss upload killer running.")
    logging.info("Listening on: {} for ip: {}, ports: {}".format(args.network_interface, args.ip_address, args.port_list))

    while True:
        try:
            analyze_udp_traffic(args.network_interface, args.ip_address, portlist_to_filter(args.port_list),
                                connections, pcap_timeout=500)
        except Exception as e:
            logging.error("Caught exception {}".format(e))
            traceback.print_exc()
        logging.warning("Taking a break before resuming analysis.")
        time.sleep(10)

main()

