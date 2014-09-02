#
# pyip is a Python package offering assembling/disassembling of raw ip packet
# including ip, udp, and icmp. Also it includes 2 utilities based on raw ip,
# traceroute and ping.
# 
# pyip is released under PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2, and is
# a project inspired by 'ping' written by Jeremy Hylton.
#
# Author: Kenneth Jiang, kenneth.jiang@gmail.com
#


import inetutils
import struct
import string

HDR_SIZE_IN_BYTES = 8

class Packet:

    def __init__(self,
                 sport = 0,
                 dport = 0,
                 ulen = 8,
                 sum = 0,
                 data = ''):
        self.sport = sport
        self.dport = dport
        self.ulen = ulen
        self.sum = sum
        self.data = data

    def __repr__(self):
        begin = "<UDP %d->%d len=%d " % (self.sport, self.dport, self.ulen)
        if self.ulen == 8:
            rep = begin + "\'\'>"
        elif self.ulen < 18:
            rep = begin + "%s>" % repr(self.data)
        else:
            rep = begin + "%s>" % repr(self.data[:10] + '...')
        return rep
    
    def __eq__(self, other):
        if not isinstance(other, Packet):
            return 0
        
        return self.sport == other.sport and \
                self.dport == other.dport and \
                self.ulen == other.ulen and \
                self.sum == other.sum and \
                self.data == other.data


    def _assemble(self, cksum=1):
        self.ulen = 8 + len(self.data)
        begin = struct.pack('HHH', self.sport, self.dport, self.ulen)
        packet = begin + '\000\000' + self.data
        if cksum:
            self.sum = inetutils.cksum(packet)
            packet = begin + struct.pack('H', self.sum) + self.data
        self.__packet = inetutils.udph2net(packet)
        return self.__packet

    def _disassemble(self, raw_packet, cksum=1):
        packet = inetutils.net2updh(raw_packet)
        if cksum and packet[6:8] != '\000\000':
            our_cksum = inetutils.cksum(packet)
            if our_cksum != 0:
                raise ValueError, packet
        elts = map(lambda x:x & 0xffff, struct.unpack('HHHH', packet[:8]))
        [self.sport, self.dport, self.ulen, self.sum] = elts
        self.data = packet[8:]


def assemble(packet, cksum=1):
    return packet._assemble(cksum)
    
def disassemble(buffer, cksum=1):
    packet = Packet()
    packet._disassemble(buffer, cksum)
    return packet
