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

from sys import stdout
import sys
import ip, icmp, udp
import socket
import select
import time
import os
import getopt
import string

#Exit code definition
ERR_USAGE = 1
ERR_RESOLVE = 1
ERR_TRACE = 2

# debug level
DEBUG = 0

# Exception occurred during tracing
class TraceError(Exception): pass

class TraceParameters:
    """ Class to capture command line options
        All parameters will be assigned default value, which can be overwritten by command line options.
        So it is guarantted that no invalid value will be returned for any parameter
        This class is designed this way so that it is detached from the way parameters are specified. So it is possible
        to extend it to capture GUI options for example.
    """
    
    def __init__(self):
        self.resolve_host = 1                # IPs need to be resolved to hostname
        self.style_newline = 0                # Output style with new line
            
        # the following will break if the local host does not have its own name resolved 
        #  correctly. How to reliably get local host primary IP address remains unknown.
        self.src_addr = socket.gethostbyname(socket.gethostname())
            
        self.first_ttl = 1                # TTL to set at the beginning
        self.dont_frag = 0                # Set the "don't fragment" bit
        self.check_sum = 0                # Checksume is not calculatd by default
        self.max_ttl = 30                # Max ttl to set
        self.def_port = 32768 + 666        # Starting port to probe
        self.num_probe = 3                # Number of probes for each hop
        self.max_wait = 5.0                # Maxium time waiting for probe result
        self.pause_msec = 0             # Pause (in milliseconds) between probes
        self.verbose = 0                # ICMP packets other than IME_EXCEEDED and UNREACHABLE won't be listed by default
        self.probe_with_icmp = 0        # Use ICMP ECHO packet, rather than UDP packet, to probe
        self.packet_len = 38            # length of probe packet
        
        self.print_help = 0             # whether '-h' is specified or not


    def usage(self):
        usage = \
    """Usage: traceroute.py [ -dFhInvx ] [ -f first_ttl ] [-m max_ttl] [-p port] [-q nqueries] [ -s src_addr ] 
                            [-w waittime] [ -z pausemsecs ]
                            host [packetlen]
    """
        return usage


    def from_commandline_options(self, args):
        """ Factory Method. Parse command line options into TraceParameter object
        Return empty list upon bad command line options
        """
            
        global DEBUG

        try:
            opts, args = getopt.getopt(args, 'dFhInvxf:sm:p:q:w:')
        except getopt.GetoptError, msg:
            print msg
            return []
    
        for k, v in opts:
            if k == '-d':
                DEBUG = 1
                
            elif k == '-F':
                self.dont_frag = 1
                
            elif k == '-h':
                self.print_help = 1
                
            elif k == '-I':
                self.probe_with_icmp = 1
                
            elif k == '-n':
                self.resolve_host = 0
                
            elif k == '-v':
                self.verbose = 1
                
            elif k == '-x':
                self.check_sum = 1
                
            elif k == '-l':
                    self.style_newline = 1
                    
            elif k == '-f':
                try:
                    first_ttl = int(v)
                    self.first_ttl = first_ttl
                except ValueError:
                    print "invalid first_ttl value", v
                    return []
            
            elif k == '-m':
                try:
                    hops = int(v)
                    self.max_ttl = hops
                except ValueError:
                    print "invalid max_ttl value", v
                    return []
                    
            elif k == '-p':
                global def_port
                try:
                    port = int(v)
                    self.def_port = port
                except ValueError:
                    print "invalid port", v
                    return []
                    
            elif k == '-q':
                try:
                    n = int(v)
                    self.num_probe = n
                except ValueError:
                    print "invalid number of queries", v
                    return []
                    
            elif k == '-s':
                self.src_addr = v
                
            elif k == '-w':
                try:
                    w = float(v)
                    self.max_wait = w
                except ValueError:
                    print "invalid timeout", v
                    return []

            elif k == '-z':
                try:
                    pause = int(v)
                    self.pause_msec = pause
                except ValueError:
                    print "invalid pausemsec value", v
                    return []
      
        # the optional arg at the end will be packlen
        if len(args) == 2:
            try:
                packet_len = int(args[1])
                self.packet_len = packet_len
                del args[1]
            except ValueError:
                print "invalid pausemsec value", args[1]
                return []
        
        return args
    
    
class Probe:
    """ class to represent a probe, meaning a outgoing/incoming packet pair
    """
    
    def __init__(self):
            # data for outgoing packet
        self.src_addr = None
        self.dst_addr = None
        self.src_port = None
        self.dst_port = None
        self.ttl = None
        self.dont_frag = 0
        self.check_sum = 0
        self.packet_len = 0
        self.verbose = 0

        # date for incoming packet
        self.gateway = None
        self.timestamp_sent = None
        self.timestamp_received = None
        self.dst_reached = 0

    def is_dst_reached(self):
        """ decide if destination is reached or not from the probe result
        """
        return self.dst_reached
    
    def sent(self):
        self.timestamp_sent = time.time()
            
    def get_round_trip_time(self):
    
        if not self.gateway:        # We didn't hear back from gateway
            return "*"
        else:
            return ("%.3f" % ((self.timestamp_received - self.timestamp_sent)*1000.0)) + " ms"

    def probe_packet(self):
        """ Build the outgoing probe packet
        """
        
        assert 0, "probe_packet should be implemented by Probe's subclass"
            
    def received(self, pkt, gateway):
        """ Upon received an incoming ICMP, determine if the packet is of our interest
             If it is, populate related fields, and return 1
             otherwise return 0
        """

        assert 0, "received should be implemented by Probe's subclass"
 
class UDPProbe(Probe):
                
    def probe_packet(self):
        """ Build the outgoing probe packet
        """
        
        # build the packet, then set its length 
        probe_ip = ip.Packet()
        
        probe_ip.src = self.src_addr
        probe_ip.dst = self.dst_addr
        probe_ip.p = socket.IPPROTO_UDP
        probe_ip.ttl = self.ttl
        probe_ip.df = self.dont_frag

        # build UPD packet as the payload of IP packet
        probe_udp = udp.Packet()
        
        # Because more than 1 traceroute can be running at the same time, we need to 
        #   distinguish the packets responding to this traceroute instance. We do this
        #   by setting source port in UDP header to our process id. As ICMP will include
        #   UDP header that triggers it in the payload, we will be able to compare the
        #   UDP source port embedded in returned ICMP packet with our process id and 
        #   determine if the packet is of our interest.
        probe_udp.sport = self.src_port
        probe_udp.dport = self.dst_port
        # calculate the length of UDP data
        header_len = len(udp.assemble(probe_udp) + ip.assemble(probe_ip))
        if self.packet_len <= header_len:
            raise TraceError, "packet length must be > %d" % (header_len)
    
        probe_udp.data = '\000' * (self.packet_len - header_len)
        
        probe_ip.data = udp.assemble(probe_udp)
        return ip.assemble(probe_ip, self.check_sum)        

    def received(self, pkt, gateway):
        """ Upon received an incoming ICMP, determine if the packet is of our interest
             If it is, populate related fields, and return 1
             otherwise return 0
        """
        
        ip_reply = ip.disassemble(pkt)
        if icmp.HDR_SIZE_IN_BYTES > len(ip_reply.data):
            return 0                #IP payload is not long enough to hold ICMP
     
        try:
            icmp_reply = icmp.disassemble(ip_reply.data)                #ICMP is payload of IP
        except ValueError, msg:
            if DEBUG:
                stdout.write("Bad Packet received!")
            return 0
         
        if DEBUG:
            stdout.write("recvfrom %s: ICMP_type: %d ICMP_code: %d" % (gateway, icmp_reply.get_type(), icmp_reply.get_code()))
        
        # 2 conditions interest us:
        #   1. ICMP_TIMEEXCEED, probe packet dropped by gateway in the middle,
        #      which then send ICMP_TIMEEXCEED back to us
        #   2. ICMP_UNREACH, probe packet reach destination host, which (we assume)
        #      is not listening on the port hence send ICMP_UNREACH back to us
        if (isinstance(icmp_reply, icmp.TimeExceeded) \
                    and icmp_reply.get_code() == icmp.ICMP_TIMXCEED_INTRANS) \
                    or isinstance(icmp_reply, icmp.Unreachable) :

            inner_ip = icmp_reply.get_embedded_ip()
            if inner_ip.src != self.src_addr or inner_ip.dst != self.dst_addr:
                return 0
         
            if udp.HDR_SIZE_IN_BYTES > len(inner_ip.data):
                return 0        #Not enough data for UDP
            
            udp_in_icmp = udp.disassemble(inner_ip.data, 0)
            if udp_in_icmp.sport == self.src_port \
                       and udp_in_icmp.dport == self.dst_port:
                self.gateway = gateway
                self.timestamp_received = time.time()
                if icmp_reply.get_type() == icmp.ICMP_UNREACH:
                    self.dst_reached = 1
                return 1

            if self.verbose:                # In verbose mode, ICMP packets other than IME_EXCEEDED and UNREACHABLE are listed
                stdout.write("recvfrom %s: ICMP_type: %d ICMP_code: %d" % (gateway, icmp_reply.get_type(), icmp_reply.get_code()))
             
        return 0             


class ICMPProbe(Probe):
    def probe_packet(self):
        """ Build the outgoing probe packet
        """
        id = 0
        seq = 0
        probe_icmp = icmp.Echo(id, seq, '')

        # calculate the length of ICMP data
        header_len = len(icmp.assemble(probe_icmp))
        if self.packet_len <= header_len:
            raise TraceError, "packet length must be > %d" % (header_len)
        data = '\000' * (self.packet_len - header_len)

        # I can't figure out how to determine how to distinguish the respones to different probe packet, 

        return icmp.assemble(icmp.Echo(id, seq, data), self.check_sum)        


    def received(self, pkt, gateway):
        """ Upon received an incoming ICMP, determine if the packet is of our interest
             If it is, populate related fields, and return 1
             otherwise return 0
        """
         
        ip_reply = ip.disassemble(pkt)
        if icmp.HDR_SIZE_IN_BYTES > len(ip_reply.data):
            return 0                #IP payload is not long enough to hold ICMP
         
        icmp_reply = icmp.disassemble(ip_reply.data)                #ICMP is payload of IP
         
        if DEBUG:
            stdout.write("recvfrom %s: ICMP_type: %d ICMP_code: %d" % (gateway, icmp_reply.get_type(), icmp_reply.get_code()))
        
        # 2 conditions interest us:
        #   1. ICMP_TIMEEXCEED, probe packet dropped by gateway in the middle,
        #      which then send ICMP_TIMEEXCEED back to us
        #   2. ICMP_ECHOREPLY, probe packet reach destination host, 
        if (icmp_reply.get_type() == icmp.ICMP_TIMXCEED \
                    and icmp_reply.get_code() == icmp.ICMP_TIMXCEED_INTRANS) \
                    or icmp_reply.get_type() == icmp.ICMP_ECHOREPLY:
            if ip.MIN_HDR_SIZE_IN_BYTES > len(icmp_reply.data):
                return 0        #ICMP payload is not long enough for inner IP
                    
            inner_ip = ip.disassemble(icmp_reply.data)
             
            if inner_ip.src != self.src_addr or inner_ip.dst != self.dst_addr:
                return 0
             
            self.gateway = gateway
            self.timestamp_received = time.time()
            if icmp_reply.get_type() == icmp.ICMP_ECHOREPLY:
                self.dst_reached = 1
            return 1
         
        if self.verbose:                # In verbose mode, ICMP packets other than IME_EXCEEDED and UNREACHABLE are listed
            stdout.write("recvfrom %s: ICMP_type: %d ICMP_code: %d" % (gateway, icmp_reply.get_type(), icmp_reply.get_code()))
             
        return 0             

            
class CommandLineReporter:
    """ Report tracing result on command line. 
        This class is designed so that UI can be decoupled as much as possible, and minimize the effort
        to migrate this tool to GUI when needed.
    """

    def __init__(self, resolve_host, style_newline):
        self.resolve_host = resolve_host
        self.style_newline = style_newline
        self.last_gateway = None
        
    def _print_host(self, host):
        """ print host name/address pair on console
        """
        if self.resolve_host:
            try:
                name, aliases, ipaddrs = socket.gethostbyaddr(host)
                addr = ipaddrs[0]
            except socket.error:
                name = addr = host
            stdout.write("%s (%s)" % (name, addr))
        else:
            stdout.write("%s" % (host))

    def report_header(self, dst, max_ttl, pkt_len):
        """ report header
        """
        
        stdout.write("traceroute to ")
        self._print_host(dst)
        stdout.write(", %d hops max, %d byte packets" % (max_ttl, pkt_len))
    
    def report_hop(self, ttl):
        """ called before new hop is to be probed
        """
        
        self.last_gateway = None
        stdout.write("\n %d " % (ttl))
        
    def report_probe(self, probe):
        """ function to report this probe result
        """
        
        # Sometimes (for example route is changed) different gateways respond to the same TTL probe. 
        #  If this happens, we print gateway again. We do this by saving the gateway received previously,
        #  and compare it with the current one. If they are different, we print the gateway name/address
        #  Also at the begining of each hop, last_gateway is set to None, which ensure gateway will be printed.
        if self.last_gateway != probe.gateway:
            self._print_host(probe.gateway)
            self.last_gateway = probe.gateway
    
        stdout.write(" %s " % (probe.get_round_trip_time()))

        if self.style_newline:
            stdout.write("\n")
            
        stdout.flush()
        
    def report_trail(self):
        stdout.write("\n")
        stdout.flush()
        
    def report_fatal_error(self, err_code, err_msg):
        stdout.write("traceroute: %s" % err_msg)
        sys.exit(err_code)
            
class Tracer:
    """ The class to control the overall flow of tracing route.
    """

    def __init__(self, host, params, reporter):
        self.params = params
        self.id = (os.getpid() & 0xffff) | 0x8000
        self.reporter = reporter
        
        try:
            self.dst_addr = socket.gethostbyname(host)
        except:
            self.reporter.report_fatal_error(ERR_RESOLVE, "unknown host '%s'" % host)
       
 
    def _open_sockets(self):
        # might want to do setuid(getuid) when we're done with this
        self.receive_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                       socket.IPPROTO_ICMP)
        self.receive_sock.sendto("", ("localhost", 0))  # Python (2.5 so far) requires 'bind' first in order to receive ICMP packets

        if self.params.probe_with_icmp:
            self.probe_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                       socket.IPPROTO_ICMP)
        else:
            self.probe_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                     socket.IPPROTO_RAW)
            #self.probe_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF,
            #                        self.packlen) 
            self.probe_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)             

    def _probe(self):
        """  return a UDPProbe or ICMPProbe instance according to if '-I' is specified
        """
        if self.params.probe_with_icmp:
            probe = ICMPProbe()
        else:
            probe = UDPProbe()
            
        return probe
     
    def _waitfor_appropriate_reply(self, probe):
        """ Wait for the ICMP packets of our interest until time out.
              Packets that appear to be irrelevant will be siliently dropped 
              (unless specified otherwise)                  
        """
            
        BUFFER_SIZE = 4096
        
        start = time.time()
        timeout = self.params.max_wait
 
        while 1:
            rd, wt, er = select.select([self.receive_sock], [], [],
                                       timeout)
            
            arrived = time.time()
            timeout = (start + self.params.max_wait) - time.time()
            if timeout < 0:        # Timeout calculation needs revision for better accuracy
                return
           
            if rd:
                try:
                    pkt, (who, port) = self.receive_sock.recvfrom(BUFFER_SIZE)
                except socket.error:
                    continue
                
                if probe.received(pkt, who):
                    return
                        
    def _probe_packet_len(self):
        """ construct a fake packet and get the length
        """
        probe = self._probe()
        probe.src_addr = "0.0.0.0"
        probe.dst_addr = "0.0.0.0"
        probe.src_port = 0
        probe.dst_port = 0
        probe.ttl = 0
        probe.packet_len = self.params.packet_len
        
        return len(probe.probe_packet())
                

    def trace(self):
        """ Entrance of tracing the route to host.
            This method will:
            1. control the (nested) loop of probing using different ttl
            2. create Probe object and use it to construct probing packet and parsing incoming ICMP
            3. create reporter and report result
            4. passing parameters to appropriate recepients
        """
        
        FAKE_PORT = 0
        MILLI_PER_SECOND = 1000.0
            
        # Open sockets to send and receive packets
        self._open_sockets()
            
        self.reporter.report_header(self.dst_addr, self.params.max_ttl, self._probe_packet_len())
        
        dst_reached = 0
        dst_port = self.params.def_port                # destination port for the first probe
        for ttl in range(self.params.first_ttl, self.params.max_ttl+1):

            if dst_reached:
                return
        
            self.reporter.report_hop(ttl)
            
            for i in range(self.params.num_probe):
                    
                dst_port += 1                # Each probe dst_port is increased by 1, so that the ICMP packet
                                        #  corresponding to this probe can be differentiated from others
                
                # construct a new Probe and set parameters
                probe = self._probe()
            
                probe.src_addr = self.params.src_addr
                probe.dst_addr = self.dst_addr
                probe.ttl = ttl
                probe.src_port = self.id        # src_port is set to this pid so that the replying ICMP packets of
                                                #  this process can be differentiated from other traceroute process
                                                #  running at the same time
                probe.dst_port = dst_port
                probe.dont_frag = self.params.dont_frag
                probe.packet_len = self.params.packet_len
                    
                pkt = probe.probe_packet()
                ret = self.probe_sock.sendto(pkt, (self.dst_addr, FAKE_PORT))
             
                if DEBUG:
                    stdout.write("\nsendto %s: %d bytes, ret = %d\n" % (self.dst_addr, len(pkt), ret))
                    
                probe.sent()        
                     
                self._waitfor_appropriate_reply(probe)
                dst_reached = probe.is_dst_reached()
                     
                self.reporter.report_probe(probe)
                     
                time.sleep(self.params.pause_msec * MILLI_PER_SECOND)         

        self.reporter.report_trail()
    
        
def main():
    import sys
    params = TraceParameters()
    host = params.from_commandline_options(sys.argv[1:])

    rptr = CommandLineReporter(params.resolve_host, params.style_newline)

    if params.print_help or len(host) != 1:
        rptr.report_fatal_error(ERR_USAGE, params.usage())

    try:
        t = Tracer(host[0], params, rptr)
        t.trace()
    except TraceError, err_msg:
        rptr.report_fatal_error(ERR_TRACE, err_msg)

if __name__ == "__main__":
    main()
