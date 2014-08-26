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

import sys ; sys.path.insert(0, '..')

import unittest
import udp
import ip
import icmp

class udpSelfVerifyingTestCase(unittest.TestCase):
    
    def setUp(self):
        self.simple = udp.Packet()
        self.simple.sport = 3213
        self.simple.dport = 1232
        self.simple.data = "ddd"
        
    def testSimplePacket(self):
        buf = udp.assemble(self.simple, 1)
        new = udp.disassemble(buf, 1)
        self.assertEqual(self.simple, new)

class udpInIcmpTestCase(unittest.TestCase):
    
    def setUp(self):
        self.pkt = 'E\xc0\x008\x84\xf1\x00\x00\xfe\x01\x91G\n\xf9OB\n\xf9@\x98\x0b\x00g\x8d\x00\x00\x00\x00E\x00\x00&\xfc\xfb\x00\x00\x01\x11\xf4\xa9\n\xf9@\x98\xcfD\xadL\x9c\xe4\x82\x9b\x00\x12m\xe0'
        
    def testUdpPortWronlyParsed(self):
        ip_reply = ip.disassemble(self.pkt)
        icmp_reply = icmp.disassemble(ip_reply.data)                #ICMP is payload of IP
        inner_ip = icmp_reply.get_embedded_ip()

        self.assertEqual('10.249.64.152', inner_ip.src)
        self.assertEqual('207.68.173.76', inner_ip.dst)
        
        udp_in_icmp = udp.disassemble(inner_ip.data, 0)
        self.assertEqual(40164, udp_in_icmp.sport)
        self.assertEqual(33435, udp_in_icmp.dport)
