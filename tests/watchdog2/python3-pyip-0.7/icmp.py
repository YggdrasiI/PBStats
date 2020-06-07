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
import ip
import array
import struct

ICMP_MINLEN = 8
ICMP_MASKLEN = 12
ICMP_ECHOREPLY = 0
ICMP_UNREACH = 3
ICMP_UNREACH_NET = 0
ICMP_UNREACH_HOST = 1
ICMP_UNREACH_PROTOCOL = 2
ICMP_UNREACH_PORT = 3
ICMP_UNREACH_NEEDFRAG = 4
ICMP_UNREACH_SRCFAIL = 5
ICMP_SOURCEQUENCH = 4
ICMP_REDIRECT = 5
ICMP_REDIRECT_NET = 0
ICMP_REDIRECT_HOST = 1
ICMP_REDIRECT_TOSNET = 2
ICMP_REDIRECT_TOSHOST = 3
ICMP_ECHO = 8
ICMP_TIMXCEED = 11
ICMP_TIMXCEED_INTRANS = 0
ICMP_TIMXCEED_REASS = 1
ICMP_PARAMPROB = 12
ICMP_TSTAMP = 13
ICMP_TSTAMPREPLY = 14
ICMP_IREQ = 15
ICMP_IREQREPLY = 16
ICMP_MASKREQ = 17
ICMP_MASKREPLY = 18
HDR_SIZE_IN_BYTES = 8

class Packet:
    """Basic ICMP packet definition. It defines fields that are common to all ICMP packets:
        type, code, and cksum
        This class also defines the method to assemble into a byte sequence ready for 
        sending over the network
    """

    def __init__(self, type, code):
        self.__type = type
        self.__code = code
        self.__cksum = 0        #cksum should be calcualted upon assemble
        self.__raw_packet = ''

    def __repr__(self):
        return "<ICMP packet %d %d>" % (self.get_type(), self.get_code())

    def __eq__(self, other):
        if not isinstance(other, Packet):
            return 0
        
        return self.get_code() == other.get_code() and \
                self.get_type() == other.get_type() and \
                self.get_cksum() == other.get_cksum() and \
                self.__raw_packet == other.__raw_packet

    def _assemble(self, cksum):
        """ method to assemble into a byte sequence that is ready for being sent
             This method will call the virtual method _get_icmp_data from its concrete
             sub-class to get its payload
        """
        
        packet = chr(self.get_type()) + chr(self.get_code()) + '\000\000' + self._get_icmp_data()
        if cksum:
            self.__cksum = struct.pack('H', inetutils.cksum(packet))
        else:
            self.__cksum = '\000\000'
            
        self.__raw_packet = chr(self.get_type()) + chr(self.get_code()) + self.get_cksum() + self._get_icmp_data()

        # Don't need to do any byte-swapping, because idseq is
        # appplication defined and others are single byte values.
        return self.__raw_packet

    def _disassemble(self, buffer, cksum):
        type, code = ord(buffer[0]), ord(buffer[1])
        # when this method is called, type and code should be set correctly already
        assert self.get_type() == type, "Mismatched type %d : %d" % (self.get_type(), type)
        assert self.get_code() == code, "Mismatched code %d : %d" % (self.get_code(), code)
        
        #only field let to puplate is cksum
        if cksum and 0 != inetutils.cksum(buffer):
            raise ValueError, "CheckSum Error!"
        self.__cksum = buffer[2:4]
        self.__raw_packet = buffer
    
    def get_type(self): return self.__type
    
    def get_code(self): return self.__code
    
    def get_cksum(self): return self.__cksum
    

class IdAndSeqPacket(Packet):
    """ ICMP packet of "id + seq + data", Echo and EchoReply as examples.
    """
    
    def __init__(self, type, code, id, seq, data):
        Packet.__init__(self, type = type, code = code)
        self.__id = id
        self.__seq = seq
        self.__data = data

    def __eq__(self, other):
        if not Packet.__eq__(self, other):
            return 0

        if not isinstance(other, type(self)):
            return 0
        
        return self.get_id() == other.get_id() and \
                self.get_seq() == other.get_seq() and \
                self.get_data() == other.get_data()
    

    def _get_icmp_data(self):
        return struct.pack('HH', self.get_id(), self.get_seq()) + self.get_data()

    def _disassemble(self, buffer, cksum):
        if len(buffer) < 8:
            raise ValueError, "Invalid ICMP Packet length: %d" % len(buffer)
        
        (self.__id, self.__seq) = struct.unpack('HH', buffer[4:8])
        self.__data = buffer[8:]
        Packet._disassemble(self, buffer, cksum)

    def get_id(self): return self.__id
    
    def get_seq(self): return self.__seq
    
    def get_data(self): return self.__data


class Echo(IdAndSeqPacket):
    def __init__(self, id=0, seq=0, data=''):
        IdAndSeqPacket.__init__(self,
                                  type = ICMP_ECHO, 
                                  code = 0, 
                                  id = id, 
                                  seq = seq, 
                                  data = data)
    
    def _disassemble(self, buffer, cksum):
        type, code = ord(buffer[0]), ord(buffer[1])
        if type != ICMP_ECHO or code != 0:
            raise ValueError, "Invalid Echo ICMP type: %d or code: %d" % (type, code)
        IdAndSeqPacket._disassemble(self, buffer, cksum)

  
class EchoReply(IdAndSeqPacket):
    
    def __init__(self, id=0, seq=0, data=''):
        IdAndSeqPacket.__init__(self,
                                  type = ICMP_ECHOREPLY, 
                                  code = 0, 
                                  id = id, 
                                  seq = seq, 
                                  data = data)

    def _disassemble(self, buffer, cksum):
        type, code = ord(buffer[0]), ord(buffer[1])
        if type != ICMP_ECHOREPLY or code != 0:
            raise ValueError, "Invalid EchoReply ICMP type: %d or code: %d" % (type, code)
        IdAndSeqPacket._disassemble(self, buffer, cksum)
        

class IPEmbeddedPacket(Packet):
    def __init__(self, type, code, embedded_ip):
        Packet.__init__(self, type = type, code = code)
        self.__unused = '\000\000\000\000'
        self.__embedded_ip = embedded_ip

    def __eq__(self, other):
        if not Packet.__eq__(self, other):
            return 0

        if not isinstance(other, type(self)):
            return 0
        
        return self.get_embedded_ip() == other.get_embedded_ip()
    
    def _get_icmp_data(self):
        assert self.__embedded_ip, "Embedded IP should not be None"
        return  self.__unused + ip.assemble(self.get_embedded_ip())
 
    def _disassemble(self, buffer, cksum):
        code = ord(buffer[1])
        self.__embedded_ip = ip.disassemble(buffer[8:])
        Packet._disassemble(self, buffer, cksum)
   
    def get_embedded_ip(self): return self.__embedded_ip


class TimeExceeded(IPEmbeddedPacket):
    
    def __init__(self, code=0, embedded_ip=None):
        IPEmbeddedPacket.__init__(self,
                                  type = ICMP_TIMXCEED,
                                  code = code,
                                  embedded_ip = embedded_ip)
    
    def _disassemble(self, buffer, cksum):
        type = ord(buffer[0])
        if type != ICMP_TIMXCEED:
            raise ValueError, "Invalid TimeExceeded ICMP type: %d" % type
        IPEmbeddedPacket._disassemble(self, buffer, cksum)

    
class Unreachable(IPEmbeddedPacket):        #Unreachable is the same with TimeExceeded except the type
    
    def __init__(self, code=0, embedded_ip=None):
        IPEmbeddedPacket.__init__(self,
                                  type = ICMP_UNREACH,
                                  code = code,
                                  embedded_ip = embedded_ip)

    def _disassemble(self, buffer, cksum):
        type = ord(buffer[0])
        if type != ICMP_UNREACH:
            raise ValueError, "Invalid Unreachable ICMP type: %d" % type
        IPEmbeddedPacket._disassemble(self, buffer, cksum)

def assemble(packet, cksum=1):
    return packet._assemble(cksum)
    
def disassemble(buffer, cksum=1):
    type, code = ord(buffer[0]), ord(buffer[1])
    
    if type == ICMP_ECHO:
        packet = Echo()
    elif type == ICMP_ECHOREPLY:
        packet = EchoReply()
    elif type == ICMP_TIMXCEED:
        packet = TimeExceeded(code = code)
    elif type == ICMP_UNREACH:
        packet = Unreachable(code = code)
    else:
        raise ValueError, "Unrecognized type: %d" % type
    
    packet._disassemble(buffer, cksum)
    return packet
