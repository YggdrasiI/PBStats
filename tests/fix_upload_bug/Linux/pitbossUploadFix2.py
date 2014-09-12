#!/usr/bin/python2
#
# This script analyse your network traffic to
# detect the 'upload bug' which cause a massive paket spamming
# from a Civ4 Pitboss server. After a detection it fakes a udp paket
# with the content 'player X quit connection'. 
#
# Requirements: 
# -	sudo apt-get install libnet1-dev libpcap0.8-dev 
# - Python wrapper http://sourceforge.net/projects/pyip/
# - Python wrapper https://github.com/Onuonga/pycap 
#
# Notes:
# - Script requires 'sudo' to get access to the network traffic.
# - If you get the following error message:
#     '[...]ImportError: No module named sll'
#   , then remove 'ssl' from list in pycap/constants/__init__.py. 
#
#

import time, socket, sys, os

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


# === Configuration === 

device = "eth0" # Interface name
#server_ip = "148.251.126.92" # Ip of your PB Server
server_ip = "192.168.0.35" # Ip of your PB Server
server_portLow = 2056 # Default value if you use no arguments
server_portHigh = server_portLow 
logfileName = "detections.log" # Default logfile name

ttl = 100
timeouts = {}
timeout = 500
clients = {}



# === Send Fake Paket === 
# Inject paket, but fake client ip
# src,dst : (ip,port) tuple
def sendUdpReply(src,dst,data):
	upacket = udp2.Packet()
	upacket.sport = src[1]
	upacket.dport = dst[1]
	upacket.data = data

	ipacket = ip2.Packet()
	ipacket.src = src[0]
	ipacket.dst = dst[0]
	ipacket.df = 1
	ipacket.ttl = 64
	ipacket.p = 17

	ipacket.data = udp2.assemble(upacket, False)
	raw_ip = ip2.assemble(ipacket, 1)

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
	except socket.error , msg:
		print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

	sock.sendto(raw_ip, (ipacket.dst, 0))
	#print ipacket


# === Analyse Traffic === 
# device: "eth0" or other devicename (string)
# server: (ip,port) tuple or (ip,port1,port2) triple for port range
# clients: List
# timeout: Waiting time on package
def analyseUdpTraffic(device, server, clients, timeout):

	# Note: I disable filtering by host.
	if( len(server)>2 ):
		filter = "(udp portrange {port1}-{port2} )".format( host = server[0], port1 = server[1], port2 = server[1])
	else:
		filter = "(udp port {port} )".format( host = server[0], port = server[1])

	pcap = pycap.capture.capture(device, timeout = timeout)
	pcap.filter(filter);

	nCaptureErrors = 0

	while True:
		try:
			if nCaptureErrors > 20 :
				# Sleep a minute
				break
			packet = pcap.next()
		except pycap.capture.error:
			nCaptureErrors += 1
			continue
		if packet is None:
			nCaptureErrors += 1
			continue

		nCaptureErrors = 0

		ip = packet[1]
		udp = packet[2]
		payload = packet[3]
		assert isinstance(ip, pycap.protocol.ip)
		assert isinstance(udp, pycap.protocol.udp)

		if (ip.source == server[0]):
			client = ip.destination

			t = timeouts.get(client, 0)
			t += 1
			timeouts[client] = t

			if t > ttl:
				#print packet
				# Send fake packet to stop upload
				# Structure of content: 
				# 254 254 06 B (A+1) (7 bytes)
				A = payload[3:5] # String!
				B = payload[5:7]
				a1 = ord(A[0])*256 + ord(A[1])+1
				A1 = chr(a1/256) + chr(a1%256)
				#print (a1,A1,A)
				src = (packet[1].destination,packet[2].destinationport)
				dst = (packet[1].source,packet[2].sourceport)
				data = chr(254)+chr(254)+chr(06) + B + A1

				msg = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()) 
				msg += " | %s:%s | %s:%s \n" % (src[0], src[1], dst[0], dst[1])

				print msg,
				if logfile != None:
					logfile.write(msg)
					logfile.flush()

				sendUdpReply(src,dst,data)
				# End detection for all clients
				break

		if (ip.destination == server[0]):
			#Use this package as client heartbeat and flush the history of tracked packages.
			client = ip.source
			timeouts[client] = 0
#			print "Heartbeat!"


# === Main === 
if len(sys.argv) < 3:
	print "Usage: ./", sys.argv[0] , "[port]", "[port]", "[network device]", "[logfile]" 
	print "No arguments given. Assume default interface %s,\n Pitboss server portrange=%i-%i, and \n Logfile %s." % (device, server_portLow, server_portHigh, logfileName)
else:
	server_portLow = int(sys.argv[1])

	if len(sys.argv) > 2:
		server_portHigh = int(sys.argv[2])
	else:
		server_portHigh = server_portLow

	if len(sys.argv) > 3:
		device = sys.argv[3]

	if len(sys.argv) > 4:
		logfileName = sys.argv[4]

	if len(logfileName) > 0:
		logfile = file(logfileName,"a")
	else:
		logfile = None

	print "Use network device %s and Pitboss server portrange=%i-%i." % (device, server_portLow, server_portHigh)
	print "\n\n"
	print " List of detected upload bugs"

	msg = "      Timestamp           |    Client         |    Server          \n"
	print msg,
	if logfile != None:
		logfile.write(msg)
		logfile.flush()


while True:
	analyseUdpTraffic(device, (server_ip,server_portLow,server_portHigh), clients, timeout)
	time.sleep(60)
