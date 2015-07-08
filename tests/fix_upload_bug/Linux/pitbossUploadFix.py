#!/usr/bin/python2
#
# This script analyse your network traffic to
# detect the 'upload bug' which cause a massive paket spamming
# from a Civ4 Pitboss server. After a detection it fakes a udp paket
# with the content 'player X quit connection'.
#
# Requirements:
# - sudo apt-get install libnet1-dev libpcap0.8-dev
# - Python wrapper http://sourceforge.net/projects/pyip/
# - Python wrapper https://github.com/Onuonga/pycap
#
# Notes:
# - Script requires root/'sudo' to get access to the network traffic.
# - Alternative you can use a copy of your python executable and run
#   sudo setcap cap_net_raw=+ep python2
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
import time
import traceback

# Add subfolders to python paths for imports
# Remove this lines if you has install the packages
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyip-0.7'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'pycap-2.0'))
# Add pycap and pyip
import pycap.capture
import pycap.protocol
import pycap.inject
import pycap.constants
import ip as ip2
import udp as udp2


class PBNetworkConnection:
    # outgoing means Server to Client because this program runs on the server :-)
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
        pass

    def __str__(self):
        return 'connection[{}:{}->{}:{}]'.format(self.client_ip, self.client_port,
                                                 self.server_ip, self.server_port)

    def __repr__(self):
        s = self.__str__()
        s += '#p: {}, t_in: {}, t_out: {}'.format(self.number_unanswered_outgoing_packets,
                                                  self.time_last_incoming_packet,
                                                  self.time_last_outgoing_packet)
        if not self.is_active():
            s += ' inactive'
        return s

    def handle_server_to_client(self, payload, now):
        self.number_unanswered_outgoing_packets += 1
        self.time_last_outgoing_packet = now

        # TODO Check if we can also use different payload sizes here, but we need to make sure the specific
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

    def handle_client_to_server(self, payload, now):
        if self.number_unanswered_outgoing_packets > 100:
            logging.debug('Received client data at {} after {} server packets / {} seconds.'.
                          format(self,
                                 self.number_unanswered_outgoing_packets,
                                 now - self.time_last_incoming_packet))

        self.number_unanswered_outgoing_packets = 0
        self.time_last_incoming_packet = now

    def disconnect(self, payload):
        # Send fake packet to stop upload
        # Structure of content:
        # 254 254 06 B (A+1) (7 bytes)
        A = payload[3:5] # String!
        B = payload[5:7]
        a1 = ord(A[0]) * 256 + ord(A[1]) + 1
        A1 = chr(a1 / 256) + chr(a1 % 256)
        data = chr(254) + chr(254) + chr(06) + B + A1

        logging.info('Disconnecting client at {}'.format(self))
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
        except socket.error as err:
            logging.error('Socket could not be created: {}'.format(err))

        sock.sendto(raw_ip, (ipacket.dst, 0))
        self.time_disconnected = time.time()

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
    pcap = pycap.capture.capture(device, timeout=pcap_timeout)
    pcap.filter(pcap_filter)

    continuous_capture_error_count = 0
    while True:
        connections.cleanup()
        try:
            if continuous_capture_error_count > 20:
                return
            packet = pcap.next()
        except pycap.capture.error as ex:
            logging.info('pycap.capture.error: {}'.format(ex))
            continuous_capture_error_count += 1
            continue
        if packet is None:
            # This is fine. Simply traffic. Don't need to wait, timeout does that
            continue

        # Capture looks good, lets reset error count
        continuous_capture_error_count = 0

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
