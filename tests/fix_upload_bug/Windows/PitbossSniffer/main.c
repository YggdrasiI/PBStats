
//For pcap
//#define WIN32
#define WPCAP
#define HAVE_REMOTE


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <windows.h> //For Sleep
#include "hashmap.h"
#include "packetConstruction.h"

#include <pcap.h>
#include "ethernet_wpcap.h"

/* Required number of packets with same payload to force upload bug detection */
#define N_SAME_PAYLOAD 20
/* Default port range for pb servers */
#define PB_PORT_LOW 2056
#define PB_PORT_HIGH PB_PORT_LOW

//d store info about selected network device.
pcap_if_t *alldevs, *d;

/* Map char[6] (ip) on Clients struct */
Hashmap clients;
/* To compare previous packets with current one use this global var. */
char *current_packet;
int all_packets_identical;
int nHeartbeatCounter;

/* prototype of the packet handler */
void packet_handler(unsigned char *param, const struct pcap_pkthdr *header, const unsigned char *pkt_data);

typedef struct Client_t {
	Hashmap packets;
} Client;

/* Get client struct, but create if not exists.*/
Client *getClient( Hashmap clients, char *keyIp )
{
	void *client = hashmap_get(clients, keyIp );
	if( client == NULL ){
		//printf("Create new client ");
		Client *newClient = (Client*) malloc(sizeof(Client));
		newClient->packets = hashmap_create(N_SAME_PAYLOAD);
		hashmap_set( clients, keyIp, newClient );
		return (Client*) hashmap_get(clients, keyIp);
	}
	return (Client*)client;
}

/* Get length of sub-hashmaps */
void loop(void * value, void * key, int k)
{
	printf("(%d) %d - %s\n", k, ((Client*)value)->packets->count , (char *) key);
}

/* Delete all stored clients */
void freeClients(void * value, void * key, int k)
{
	Client *client = (Client*)value;
	hashmap_free(client->packets);
	free(client);
}

//Just for debugging
void printPackets(void * value, void * key, int k)
{
	int i;
	printf("%d : ", (int)key);
	for( i= 0; i<25; i++){
		if(i%4 == 0 ) printf(",");
		printf( "%2X ", *(((unsigned char*)value)+i));
	}
	printf("\n");
}

/* Check if the last N packets has the same
 * content as the newest packet. Newest
 * packet is global variable.
 * Ignore the first 5 bytes (fe fe 00 A1 A2)  and just check next 13 bytes ( B1 B2 [Content data] )
 */
void comparePackets(void * value, void * key, int k)
{
	//printPackets(value, key, k);
	if( memcmp( ((char*)value)+5, ((char*)current_packet)+5, 13) != 0){
		all_packets_identical = 0;
	}
}

void fill_in_macs(const unsigned char *pkt_data, unsigned char *smac, unsigned char *dmac ){
	//DstMAC
	memcpy( (void*)dmac, (void*)pkt_data, 6 );
	//SrcMAC
	memcpy( (void*)smac, (void*)(pkt_data+6), 6 );
}
/* Transform source and destination ips into strings of length 4.
*/
void fill_in_ips(const unsigned char *pkt_data, unsigned char *sip, unsigned char *dip ){
	memcpy( (void*)sip, (void*)(pkt_data+26), 4 );
	memcpy( (void*)dip, (void*)(pkt_data+30), 4 );
}

main(int argc, char **argv)
{
	pcap_t *fp;
	clients = hashmap_create(52);
	nHeartbeatCounter = 0;
	//pcap_if_t *alldevs, *d;
	u_int inum, i=0;
	char errbuf[PCAP_ERRBUF_SIZE];
	int res;
	struct pcap_pkthdr *header;
	const unsigned char *pkt_data;
	char filter[200];
	struct bpf_program fcode;
	bpf_u_int32 NetMask;
	pcap_t *adhandle;

	//Pitboss vars
	int server_portLow = PB_PORT_LOW;
	int server_portHigh = PB_PORT_HIGH;
	int interface_index = -1;

	if (argc > 1){
		server_portLow = atoi(argv[1]);
		server_portHigh = server_portLow;
	}
	if (argc > 2){
		server_portHigh = atoi(argv[2]);
	}
	if (argc > 3){
		interface_index = atoi(argv[3]);
	}
	printf("Selected Pitboss port range: %d-%d. Interface index: %d.\n\n", server_portLow, server_portHigh, interface_index);

	current_packet = calloc( 30, sizeof(unsigned char) );

	if( interface_index == -1 ){
		printf("\nNo adapter selected: printing the device list:\n");
	}
	/* The user didn't provide a packet source: Retrieve the local device list */
	if (pcap_findalldevs_ex(PCAP_SRC_IF_STRING, NULL, &alldevs, errbuf) == -1)
	{
		fprintf(stderr,"Error in pcap_findalldevs_ex: %s\n", errbuf);
		return -1;
	}

	/* Print the list */
	for(d=alldevs; d; d=d->next)
	{
		++i;
		if( interface_index == -1 ){
			printf("%d. %s\n    ", i, d->name);

			if (d->description)
				printf(" (%s)\n", d->description);
			else
				printf(" (No description available)\n");
		}
	}

	if (i==0)
	{
		fprintf(stderr,"No interfaces found! Exiting.\n");
		return -1;
	}

	if( interface_index == -1 ){
		printf("Enter the interface number (1-%d): ",i);
		scanf("%d", &inum);
	}else{
		inum = interface_index;
	}

	if (inum < 1 || inum > i)
	{
		printf("\nInterface number out of range.\n");

		/* Free the device list */
		pcap_freealldevs(alldevs);
		return -1;
	}

	/* Jump to the selected adapter */
	for (d=alldevs, i=0; i< inum-1 ;d=d->next, i++);

	/* Open the device */
	if ( (fp= pcap_open(d->name,
					100 /*snaplen*/,
					PCAP_OPENFLAG_PROMISCUOUS /*flags*/,
					20 /*read timeout*/,
					NULL /* remote authentication */,
					errbuf)
			 ) == NULL)
	{
		fprintf(stderr,"\nError opening adapter\n");
		return -1;
	}

	int portLow;
	int portHigh;
	portLow = 2056;
	portHigh = 2056;
	//sprintf(filter, "(udp src portrange %d-%d )", portLow, portHigh); //just outgoing packets. Not enought to detect heardbeat of clients
	sprintf(filter, "(udp portrange %d-%d )", portLow, portHigh); //incomming and outgoing packets

	if (filter != NULL)
	{
		// We should loop through the adapters returned by the pcap_findalldevs_ex()
		// in order to locate the correct one.
		//
		// Let's do things simpler: we suppose to be in a C class network ;-)
		NetMask=0xffffff;

		//compile the filter
		if(pcap_compile(fp, &fcode, filter, 1, NetMask) < 0)
		{
			fprintf(stderr,"\nError compiling filter: wrong syntax.\n");
			return 0;
		}

		//set the filter
		if(pcap_setfilter(fp, &fcode)<0)
		{
			fprintf(stderr,"\nError setting the filter\n");
			return 0;
		}

	}

	/* start the capture */
	pcap_loop(fp, 0, packet_handler, NULL);

	if(res == -1)
	{
		fprintf(stderr, "Error reading the packets: %s\n", pcap_geterr(fp));
		return -1;
	}

	//well, implict free for earlier returns...
	hashmap_each(clients, freeClients);
	hashmap_free(clients);

	return 0;
}


/* Send package on open, global device fp. */
void sendUdpReply( pcap_if_t* device,
		unsigned char *smac, unsigned char*dmac,
		unsigned char *sip, unsigned char *dip,
		unsigned short sport, unsigned short dport,
		unsigned char *data, size_t dataLen )
{
	printf("    MAC/IP/PORT\n");
	printf("SRC: %2X:%2X:%2X:%2X:%2X:%2X / %3u.%3u.%3u.%3u / %d \n",
			smac[0], smac[1], smac[2], smac[3], smac[4], smac[5], sip[0], sip[1], sip[2], sip[3], sport);
	printf("DST: %2X:%2X:%2X:%2X:%2X:%2X / %3u.%3u.%3u.%3u / %d \n\n",
			dmac[0], dmac[1], dmac[2], dmac[3], dmac[4], dmac[5], dip[0], dip[1], dip[2], dip[3], dport);
	//Create package
	RawPacket *rawPacket = rawPacket_create(smac,dmac,sip,dip,sport,dport,data,dataLen);

	//Print packet
	/*
		 printf(" Out Packet:");
		 int i;
		 for( i= 0; i<rawPacket->finalPacketLen; i++){
		 if(i%16 == 0 ) printf("\n");
		 printf( "%2X ", rawPacket->finalPacket[i]);
		 }
		 */

	//Sending here...
	if( device != NULL ){
		char Error[256];
		int i;
		for( i=0; i<255; i++){
			Error[i] = ' ';
		}
		pcap_t* t;
		if ( (t= pcap_open(device->name,
						100,                // portion of the packet to capture (only the first 100 bytes)
						PCAP_OPENFLAG_PROMISCUOUS,  // promiscuous mode
						1000,               // read timeout
						NULL,               // authentication on the remote machine
						Error              // error buffer
						) ) == NULL)
		{
			fprintf(stderr,"\nUnable to open the adapter. %s is not supported by WinPcap\n", device->name);
			for( i=0; i<255; i++){
				printf("%c", Error[i]);
			}
			printf("\n");
			return;
		}

		if (pcap_sendpacket(t,rawPacket->finalPacket, rawPacket->finalPacketLen) != 0)
		{
			fprintf(stderr,"\nError sending the packet: \n", pcap_geterr(t));
			return;
		}

		pcap_close(t);

	}


	//Destroy package
	rawPacket_destroy(rawPacket);
	rawPacket = NULL;
}

/* Callback function invoked by libpcap for every incoming packet */
void packet_handler(unsigned char *param, const struct pcap_pkthdr *header, const unsigned char *pkt_data)
{
	struct tm *ltime;
	char timestr[16];
	ip_header *ih;
	udp_header *uh;
	u_int ip_len;
	u_short sport,dport;
	time_t local_tv_sec;

	/*
	 * unused parameter
	 */
	(VOID)(param);

	/* retireve the position of the ip header */
	ih = (ip_header *) (pkt_data +
			14); //length of ethernet header

	/* retireve the position of the udp header */
	ip_len = (ih->ver_ihl & 0xf) * 4;
	uh = (udp_header *) ((unsigned char*)ih + ip_len);

	/* convert from network byte order to host byte order */
	sport = ntohs( uh->sport );
	dport = ntohs( uh->dport );

	/* define/compute udp payload (segment) offset */
	unsigned char *payload = (unsigned char *)(uh)+SIZE_UDP; /* Header has 8 oktets */

	/* compute udp payload (segment) size */
	int size_payload = header->len - SIZE_ETHERNET - SIZE_UDP - ip_len;

	/* Check if packet match with critical sturcture */
	if( payload[0] == 254 && payload[1] == 254 ){

		unsigned char smac[6];
		unsigned char dmac[6];
		fill_in_macs(pkt_data, smac, dmac);

		unsigned char sip[4];
		unsigned char dip[4];
		fill_in_ips(pkt_data, sip, dip);


		if( size_payload == 25 ){
			/* This package could be indicate an upload error. Add the payload
			 * for this client (destination ip) to an set. Force analysation
			 * of the packages if an sufficient amount of packages reached. */

			//Compare with existing packets
			all_packets_identical = 1;
			memcpy(current_packet, payload,25*sizeof(unsigned char));

			Client *cl1 = getClient(clients, dip);

			if( cl1->packets->count >= N_SAME_PAYLOAD ){
				//printf("Compare packets\n");
				hashmap_each(cl1->packets, comparePackets);

				if( all_packets_identical ){
					printf("Upload bug detected\n");

					unsigned short totalLen=0;
					memcpy( (void*)&totalLen, pkt_data+16, 2);
					totalLen = ntohs(totalLen);

					/*
						 printf(" In Packet %d:", totalLen);
						 int i;
						 for( i = 0; i<totalLen; i++){
						 if(i%16 == 0 ) printf("\n");
						 printf( "%2X ", pkt_data[i] );
						 }
						 printf("\n");
						 */

					/*
						 printf(" Payload:");
						 int i;
						 for( i= 0; i<25; i++){
						 if(i%4 == 0 ) printf(",");
						 printf( "%2X ", payload[i]);
						 }
						 printf("\n");
						 hashmap_each(cl1->packets, printPackets);
						 */

					/* Construct data for quitting of connection */
					u_short A = *((u_short*)(current_packet+3));
					//u_short B = *((u_short*)(current_packet+5));
					//First variable will be increment by 1.
					A++;

					//Construct payload of udp packet
					unsigned char r[8];
					r[0] = 0xFE; r[1] = 0xFE; r[2] = 0x06;
					//r[3] = B%256; r[4] = B/256;
					memcpy( (void*)(r)+3, (void*)current_packet+5, 2);//use B implicit
					//printf("%X %X vs %X %X\n", B%256, B/256, r[3], r[4]);
					r[5] = A%256; r[6] = A/256;
					r[7] = '\0';//not used.

					//Note: Flipping of source and destination ips and ports
					//Use Broadcast mac as destination for reply
					//sendUdpReply(d, dmac, smac, dip, sip, dport, sport, r,7);
					//unsigned char macUnicast[] = {0x00, 0x00, 0x03, 0x04, 0x00, 0x06};
					//unsigned char mac0[] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
					unsigned char macBroadcast[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
					sendUdpReply(d, &dmac, &macBroadcast, dip, sip, dport, sport, r,7);

				}

				//Clear stored packets for this client
				hashmap_free(cl1->packets);
				cl1->packets = hashmap_create(N_SAME_PAYLOAD);
			}else{

				//Store payload in client history
				char *mapvalue = (char*) malloc(25*sizeof(unsigned char));
				memcpy(mapvalue, payload, 25*sizeof(unsigned char));
				int *key = (int*) cl1->packets->count;
				hashmap_set( cl1->packets, key, mapvalue );

				//printf("Store packet %d\n", cl1->packets->count);
			}

		}else{
			/* This package does not have the right format for the upload bug dectetion. This does
			 * NOT indicate that everything is right, because the server sends packages with other
			 * length as 25, too.
			 * The program is stupid and does not know if this package was send by server or client.
			 * But if it's was send by client we can use it as heardbeat package by the client.
			 * (=> client ip = source ip.)
			 */
			Client *cl1 = getClient(clients, sip /*not dip!*/);
			void *item = hashmap_get(cl1->packets, 0 );
			if( item == NULL ){
				// add new, first package
				int *key = (int*) 0x0;
				char *mapvalue = (char*) calloc(25,sizeof(unsigned char));
				hashmap_set( cl1->packets, key, mapvalue );
			}else{
				//just rewrite a byte in existing package
				*(((char*)item)+5) = 0xFF;
			}
		}

		nHeartbeatCounter++;
		if( nHeartbeatCounter > 1000 ){
			/* Many activity on server sleep some time. */
			Sleep(300*1000);//Milliseconds
			nHeartbeatCounter = 0;
		}

	}

}

