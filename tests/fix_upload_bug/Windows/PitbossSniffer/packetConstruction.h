/* Adaption of http://www.codeproject.com/Articles/31920/How-to-craft-UDP-packets-and-send-them-with-WinPCa */

typedef struct RawPacket_t {
	unsigned int userDataLen;
	unsigned char *finalPacket;
	unsigned int finalPacketLen;
	unsigned short totalLen;
} RawPacket;

//Helper functions for checksums
unsigned short bytesToShort(unsigned char X, unsigned char Y);
unsigned short caluculateIPChecksum(unsigned char  *finalPacket );
unsigned short caluculateUDPChecksum (
		unsigned char* finalPacket,
		unsigned char* userdata,
		int userdataLen,
		unsigned char Protocol);

/*
 * Create UDP Packet and setup all headers
 * and checksums.
 *
 * MAC's: 6 bytes, IP's: 4 bytes, Ports: 2 bytes. */
RawPacket *rawPacket_create (
		unsigned char* sourceMAC,
		unsigned char* destinationMAC,
		unsigned char*   sourceIP,
		unsigned char*   destinationIP,
		unsigned short sourcePort,
		unsigned short destinationPort,
		unsigned char* userdata,
		unsigned int   userdataLen );

void rawPacket_destroy(RawPacket *rawPacket);


