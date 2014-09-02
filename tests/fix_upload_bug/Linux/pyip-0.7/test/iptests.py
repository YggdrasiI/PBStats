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
import ip

class ipSelfVerifyingTestCase(unittest.TestCase):
    
    def setUp(self):
        self.simple = ip.Packet()
        self.simple.src = '127.0.0.1'
        self.simple.dst = '0.0.0.0'
        
    def testSimplePacket(self):
        buf = ip.assemble(self.simple, 1)
        new = ip.disassemble(buf, 1)
        self.assertEqual(self.simple, new)
