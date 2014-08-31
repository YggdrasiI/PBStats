#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <Winsock2.h>
#include "packetConstruction.h"
/* Adaption of http://www.codeproject.com/Articles/31920/How-to-craft-UDP-packets-and-send-them-with-WinPCa */

//Helper functions for checksums
unsigned short bytesToShort(unsigned char X, unsigned char Y)
{
     unsigned short tmp = X;
     tmp = tmp << 8;
     tmp = tmp | Y; 
     return tmp;
}
unsigned short caluculateIPChecksum(unsigned char  *finalPacket )
{
    unsigned short checksum = 0;
		int i;
    for( i = 14;i<34;i+=2)
    {
        unsigned short tmp = bytesToShort(finalPacket[i], finalPacket[i+1]);
        unsigned short difference = 65535 - checksum;
        checksum += tmp;
        if(tmp > difference){checksum += 1;}
    }
    checksum = ~checksum;
    return htons(checksum);
}


unsigned short caluculateUDPChecksum (
		unsigned char* finalPacket,
		unsigned char* userdata,
		int userdataLen,
		unsigned char Protocol)
{
    unsigned short checksum = 0;
    unsigned short pseudoHeaderLen = userdataLen + 8 + 9; //Length of pseudoHeader =
                                                        //Data Length + 8 bytes UDP header
                                                        //+ Two 4 byte IP's + 1 byte protocol

    pseudoHeaderLen += pseudoHeaderLen % 2; //If bytes are not an even number, add an extra.

    unsigned short Length = userdataLen + 8; // This is just UDP + Data length. 
                                             //needed for actual data in udp header

		//Init with 0;
    unsigned char* pseudoHeader = (unsigned char*) calloc(sizeof(char),pseudoHeaderLen);

    pseudoHeader[0] = Protocol; // Protocol

    memcpy((void*)(pseudoHeader+1), (void*)(finalPacket+26), 8); // Source and Dest IP

    Length = htons(Length); // Length is not network byte order yet
    memcpy((void*)(pseudoHeader+9), (void*)&Length, 2); //Included twice
    memcpy((void*)(pseudoHeader+11), (void*)&Length, 2); 

    memcpy((void*)(pseudoHeader+13), (void*)(finalPacket+34), 2);//Source Port
    memcpy((void*)(pseudoHeader+15), (void*)(finalPacket+36), 2); // Dest Port

    memcpy((void*)(pseudoHeader+17), (void*)userdata, userdataLen); 

		int i;
    for( i = 0; i < pseudoHeaderLen; i+=2 )
    {
        unsigned short tmp = bytesToShort(pseudoHeader[i], pseudoHeader[i+1]);
        unsigned short difference = 65535 - checksum;
        checksum += tmp;
        if(tmp > difference){checksum += 1;}
    }
    checksum = ~checksum; //One's complement

		free(pseudoHeader);
    return checksum;
}


RawPacket *rawPacket_create (
		unsigned char* sourceMAC,
		unsigned char* destinationMAC,
		unsigned char*   sourceIP,
		unsigned char*   destinationIP,
		unsigned short sourcePort,
		unsigned short destinationPort,
		unsigned char* userdata,
		unsigned int   userdataLen )
{
	RawPacket *rawPacket = (RawPacket*) malloc(sizeof(RawPacket));
	rawPacket->userDataLen = userdataLen;

	// DataLength + 42 Bytes of Headers
	rawPacket->finalPacketLen = rawPacket->userDataLen+42;
	rawPacket->finalPacket = (unsigned char*) calloc(sizeof(char), (rawPacket->userDataLen+42) );
	void* const fp = (void*) rawPacket->finalPacket;

	//Len for IPHeader (UDPLen + IPLen + DataLen)
	rawPacket->totalLen = rawPacket->userDataLen + 20 + 8;

	//Beginning of Ethernet II Header
	//DestMAC
	memcpy(fp   , (void*)destinationMAC, 6 );
	//SrcMAC
	memcpy(fp+6 , (void*)sourceMAC, 6 );

	// Type: IPv4
	const unsigned short protocolType = 8;
	memcpy(fp+12, (void*)&protocolType, 2 ); 

	// Beginning of IP Header
	// First 4 bits = Version (4)
	// Last 4 bits = HeaderLen (20)
	memcpy(fp+14, (void*)"\x45", 1 );

	//Differntiated services field. Usually 0 
	memcpy(fp+15, (void*)"\x00", 1 );

	//Total length
	const unsigned short totalLen = htons(rawPacket->totalLen);
	memcpy(fp+16, (void*)&totalLen, 2);

	// ID Number. Usually not needed
	const unsigned short packetIdNumber = htons(0x0000);
	memcpy(fp+18, (void*)&packetIdNumber, 2);

	// Flags. Used more by TCP. Set Nofragment-Flag. 010 0 0000
	memcpy(fp+20, (void*)"\x40", 1);
	// Fragment Offset. NOt much use in udp
	memcpy(fp+21, (void*)"\x00", 1);
	// Time To Live. I see 128 alot, Civ4 uses 64
	memcpy(fp+22, (void*)"\x40", 1);

	// Protocol. UDP is 0x11;TCP is 6;ICMP is 1 etc
	const unsigned char udpProtocolId = 0x11;
	memcpy(fp+23, (void*)&udpProtocolId, 1);

	//checksum, should be zero before 
	// checksum calculation
	memcpy(fp+24, (void*)"\x00\x00", 2);

	//inet_addr does htonl() for us
	// if inet_addr not used, use htonl()
	memcpy(fp+26, (void*)sourceIP, 4);
	memcpy(fp+30, (void*)destinationIP, 4);

	//Beginning of UDP Header
	const unsigned short sourcePort_ = htons(sourcePort);
	memcpy(fp+34, (void*)&sourcePort_, 2);
	const unsigned short destinationPort_ = htons(destinationPort);
	memcpy(fp+36, (void*)&destinationPort_, 2);

	// UDP Len + DataLen
	const unsigned short UDPTotalLen = htons(userdataLen + 8);
	memcpy(fp+38, (void*)&UDPTotalLen, 2);
	//Finally append our own data
	memcpy(fp+42, (void*)userdata, userdataLen);

	// The UDP Checksum
	const unsigned short UDPChecksum = 0*caluculateUDPChecksum(
			rawPacket->finalPacket,
			userdata, 
			userdataLen, udpProtocolId );
	memcpy(fp+40, (void*)&UDPChecksum, 2);

	// The Ip Checksum
	//const unsigned short IPChecksum = htons(caluculateIPChecksum(rawPacket->finalPacket));
	const unsigned short IPChecksum = caluculateIPChecksum(rawPacket->finalPacket);
	memcpy(fp+24, (void*)&IPChecksum, 2);

	return rawPacket;

}

void rawPacket_destroy(RawPacket *rawPacket){
	free(rawPacket->finalPacket);
	free(rawPacket);
}


