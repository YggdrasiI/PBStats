import socket
import sys
import ip
import udp

ClientHost = '192.168.0.22'
ServerHost = '192.168.0.22'
ClientPort = 2057 
ServerPort = 2056

upacket = udp.Packet()
upacket.sport = ClientPort
upacket.dport = ServerPort
upacket.data = "\xfe\xfe\x00\x06"
#upacket.data = "Hello Server"

ipacket = ip.Packet()
ipacket.src = ClientHost
ipacket.dst = ServerHost
ipacket.df = 1
ipacket.ttl = 64
ipacket.p = 17

ipacket.data = udp.assemble(upacket, False)
raw_ip = ip.assemble(ipacket, 1)

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
except socket.error , msg:
	print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

sock.sendto(raw_ip, (ipacket.dst, 0))

