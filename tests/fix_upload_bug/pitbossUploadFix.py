#!/usr/bin/python2
#
# This script analyse your network traffic to
# detect the 'upload bug' which cause a massive paket spamming
# from a Civ4 Pitboss server. After a detection it fakes a udp paket
# with the content 'player X quit connection'. 
#
# Requirements: 
# -	Libraries + Headers ( I.e. libnet1-dev and libpcap0.8-dev )
# - Python-Wrapper http://sourceforge.net/projects/pyip/
# - Python-Wrapper https://github.com/Onuonga/pycap 
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
server_ip = "192.168.0.22" # Value not used
server_portLow = 2056 # Default value if you use no arguments

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



# === Analyse Traffic === 
# device: "eth0" or other devicename (string)
# server: (ip,port) tuple or (ip,port1,port2) triple for port range
# clients: List
# timeout: Waiting time on package
def analyseUdpTraffic(device, server, clients, timeout):

	# Note: I disable filtering by host.
	if( len(server)>2 ):
		filter = "(udp src portrange {port1}-{port2} )".format( host = server[0], port1 = server[1], port2 = server[1])
	else:
		filter = "(udp src port {port} )".format( host = server[0], port = server[1])

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

			# Anlayse content if payload is at least 20 chars long
			pl = len(payload)
			if pl == 25 and ord(payload[0]) == 254 and ord(payload[1]) == 254:
				# Structure of searched payload:
				# 254 254 00
				# [2 bytes number: A]
				# [2 bytes number: B]
				# [11 bytes: content]
				# [7 bytes: not analysed]

				clist = clients.get(client,[])
				clist.append( payload )
				clients[client] = clist 

				N = len(clist)
				if N > 10:
					#Check if B + content is always the same -> upload bug detected
					bugFound = True
					for n in xrange(N-10,N):
						if clist[N-1][5:18] != clist[n][5:18] :
							bugFound = False
							break

					# Flush list
					clients[client] = []

					#print ("Upload-Bug found?! ", bugFound )
					if bugFound:
						#print packet
						# Send fake packet(s) to stop upload
						# Structure of content: 
						# 254 254 64 (A+1)  (5 bytes)
						# 254 254 06 B (A+1) (7 bytes)
						A = clist[N-1][3:5] # String!
						B = clist[N-1][5:7]
						a1 = ord(A[0])*255 + ord(A[1])+1
						A1 = chr(a1/255) + chr(a1%255)
						#print (a1,A1,A)

						src = (packet[1].destination,packet[2].destinationport)
						dst = (packet[1].source,packet[2].sourceport)
						data = chr(254)+chr(254)+chr(06) + B + A1

						print "Upload bug detected send fake packet for client %s:%s to server %s:%s" % (src[0], src[1], dst[0], dst[1])
						sendUdpReply(src,dst,data)

						# End detection for all clients
						break


# === Main === 
if len(sys.argv) < 2:
	print "Usage: ./", sys.argv[0] , "[port]", "[port]" #, "[pitboss server ip]" 
	print "No arguments given. Assume default value port=%i and continue." % (server_portLow)
else:
	server_portLow = int(sys.argv[1])

if len(sys.argv) > 2:
	server_portHigh = int(sys.argv[2])
else:
	server_portHigh = server_portLow

while True:
	analyseUdpTraffic(device, (server_ip,server_portLow,server_portHigh), clients, timeout)
	time.sleep(60)
