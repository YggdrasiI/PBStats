#
# pyip is a Python package offering assembling/disassembling of raw ip packet
# including ip, udp, and icmp. Also it includes 2 utilities based on raw ip,
# traceroute and ping.
# 
# pyip is released under PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2, and is
# a project inspired by 'ping' written by Jeremy Hylton.
#
A# Author: Kenneth Jiang, kenneth.jiang@gmail.com
#

import sys ; sys.path.insert(0, '..')

import unittest
import icmp
import ip

class icmpSelfVerifyingTestCase(unittest.TestCase):
    
    def setUp(self):
        embedded = ip.Packet()
        embedded.src = '127.0.0.1'
        embedded.dst = '0.0.0.0'
        
        self.echo = icmp.Echo(1234, 1343, 'python pinger')
        self.echo_reply = icmp.EchoReply(1234, 1343, 'python pinger')
        self.time_exceeded = icmp.TimeExceeded(code = 1, embedded_ip = embedded)
        self.unreachable = icmp.Unreachable(code = 2, embedded_ip = embedded)
        
    def testEcho(self):
        buf = icmp.assemble(self.echo, cksum = 1)
        new = icmp.disassemble(buf, cksum = 1)
        self.assertEqual(self.echo, new)

    def testEchoNotCksum(self):
        buf = icmp.assemble(self.echo, cksum = 0)
        new = icmp.disassemble(buf, cksum = 0)
        self.assertEqual(self.echo, new)

    def testEchoReply(self):
        buf = icmp.assemble(self.echo_reply, cksum = 1)
        new = icmp.disassemble(buf, cksum = 1)
        self.assertEqual(self.echo_reply, new)

    def testEchoReplyNotCksum(self):
        buf = icmp.assemble(self.echo_reply, cksum = 0)
        new = icmp.disassemble(buf, cksum = 0)
        self.assertEqual(self.echo_reply, new)

    def testUnreachable(self):
        buf = icmp.assemble(self.unreachable, cksum = 1)
        new = icmp.disassemble(buf, cksum = 1)
        self.assertEqual(self.unreachable, new)

    def testUnreachableNotCksum(self):
        buf = icmp.assemble(self.unreachable, cksum = 0)
        new = icmp.disassemble(buf, cksum = 0)
        self.assertEqual(self.unreachable, new)

    def testTimeExceeded(self):
        buf = icmp.assemble(self.time_exceeded, cksum = 1)
        new = icmp.disassemble(buf, cksum = 1)
        self.assertEqual(self.time_exceeded, new)

