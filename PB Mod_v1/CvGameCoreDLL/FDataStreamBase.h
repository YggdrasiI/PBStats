//	$Revision: #4 $		$Author: mbreitkreutz $ 	$DateTime: 2005/06/13 13:35:55 $
//---------------------------------------------------------------------------------------
//  Copyright (c) 2004 Firaxis Games, Inc. All rights reserved.
//---------------------------------------------------------------------------------------

/*
*
* FILE:    FDataStreamBase.h
* DATE:    7/15/2004
* AUTHOR: Mustafa Thamer
* PURPOSE: Base Classe of Stream classes for file, null and mem streams.
*
*		Easily read and write data to those kinds of streams using the same baseclass interface.
*		FStrings not used since this is a public dll header.
*
*/

#ifndef		FDATASTREAMBASE_H
#define		FDATASTREAMBASE_H
#pragma		once

//
// Stream abstract base class
//
class FDataStreamBase
{
public:
	virtual void	Rewind() = 0;
	virtual bool	AtEnd() = 0;
	virtual void	FastFwd() = 0;
	virtual unsigned int  GetPosition() const =  0;
	virtual void    SetPosition(unsigned int position) = 0;
	virtual void    Truncate() = 0;
	virtual void	Flush() = 0;
	virtual unsigned int	GetEOF() const = 0;
	virtual unsigned int			GetSizeLeft() const = 0;
	virtual void	CopyToMem(void* mem) = 0;
	
	virtual unsigned int	WriteString(const wchar *szName) = 0;
	virtual unsigned int	WriteString(const char *szName) = 0;
	virtual unsigned int	WriteString(const std::string& szName) = 0;
	virtual unsigned int	WriteString(const std::wstring& szName) = 0;
	virtual unsigned int	WriteString(int count, std::string values[]) = 0;
	virtual unsigned int	WriteString(int count, std::wstring values[]) = 0;
	
	virtual unsigned int	ReadString(char *szName) = 0;
	virtual unsigned int	ReadString(wchar *szName) = 0;
	virtual unsigned int	ReadString(std::string& szName) = 0;
	virtual unsigned int	ReadString(std::wstring& szName) = 0;
	virtual unsigned int	ReadString(int count, std::string values[]) = 0;
	virtual unsigned int	ReadString(int count, std::wstring values[]) = 0;
	
	virtual char *			ReadString() = 0;		// allocates memory 
	virtual wchar *		ReadWideString() = 0;	// allocates memory 

	virtual void		Read(char *) = 0;
	virtual void		Read(byte *) = 0;
	virtual void		Read(int count, char values[]) = 0;
	virtual void		Read(int count, byte values[]) = 0;
	virtual void		Read(bool *) = 0;
	virtual void		Read(int count, bool values[]) = 0;
	virtual void		Read(short	*s) = 0;
	virtual void		Read(unsigned short	*s)  = 0;
	virtual void		Read(int count, short values[]) = 0;
	virtual void		Read(int count, unsigned short values[]) = 0;
	virtual void		Read(int* i) = 0;
	virtual void		Read(unsigned int* i) = 0;
	virtual void 		Read(int count, int values[]) = 0;
	virtual void 		Read(int count, unsigned int values[]) = 0;

	virtual void		Read(long* l) = 0;
	virtual void		Read(unsigned long* l)  = 0;
	virtual void 		Read(int count, long values[]) = 0;
	virtual void 		Read(int count, unsigned long values[])  = 0;

	virtual void		Read(float* value) = 0;
	virtual void		Read(int count, float values[]) = 0;

	virtual void		Read(double* value) = 0;
	virtual void		Read(int count, double values[]) = 0;

	virtual void		Write( char value) = 0;
	virtual void		Write(byte value) = 0;
	virtual void		Write(int count, const  char values[]) = 0;
	virtual void		Write(int count, const  byte values[]) = 0;

	virtual void		Write(bool value) = 0;
	virtual void		Write(int count, const bool values[]) = 0;

	virtual void		Write(short value) = 0;
	virtual void		Write(unsigned short value) = 0;
	virtual void		Write(int count, const short values[]) = 0;
	virtual void		Write(int count, const unsigned short values[])  = 0;

	virtual void		Write(int value) = 0;
	virtual void		Write(unsigned int value)  = 0;
	virtual void 		Write(int count, const int values[]) = 0;
	virtual void		Write(int count, const unsigned int values[])  = 0;

	virtual void		Write(long value) = 0;
	virtual void		Write(unsigned long  value)  = 0;
	virtual void 		Write(int count, const long values[]) = 0;
	virtual void		Write(int count, const unsigned long values[])  = 0;

	virtual void		Write(float value) = 0;
	virtual void		Write(int count, const float values[]) = 0;

	virtual void		Write(double value) = 0;
	virtual void		Write(int count, const double values[]) = 0;


//Hilfsfunktion zum Auslesen von Arrays

//count can be int or char. Type is important for ->Read.
#define READ_PACKED(COUNT, ARRAYNAME, DECLTYPE, COUNT_READ)\
	SAFE_DELETE_ARRAY(ARRAYNAME); \
	COUNT_READ \
	if (COUNT > 0) \
	{ \
		/*ARRAYNAME = new decltype(ARRAYNAME[0])[COUNT]; */\
		ARRAYNAME = new DECLTYPE[COUNT]; \
		pStream->Read(COUNT, ARRAYNAME); \
	}else if( COUNT < 0){ \
		/*ARRAYNAME = new decltype(ARRAYNAME[0])[-COUNT]; */\
		ARRAYNAME = new DECLTYPE[-COUNT]; \
		pStream->ReadPacked((int)(-COUNT), ARRAYNAME); \
	} \

#define READ_PACKED_DEFAULT(COUNT, ARRAYNAME, DECLTYPE, COUNT_READ, DEFAULT_VALUE)\
	READ_PACKED(COUNT, ARRAYNAME, DECLTYPE, COUNT_READ)\
	else{ \
		ARRAYNAME = DEFAULT_VALUE; \
	} \

#define ReadPackedCharCounter(COUNT, ARRAYNAME, DECLTYPE)\
	READ_PACKED(COUNT, ARRAYNAME, DECLTYPE, pStream->Read((unsigned char*)&COUNT); ) \

#define ReadPackedIntCounter(COUNT, ARRAYNAME, DECLTYPE)\
	READ_PACKED(COUNT, ARRAYNAME, DECLTYPE, pStream->Read(&COUNT); ) \

#define ReadPackedCharCounter_Default(COUNT, ARRAYNAME, DECLTYPE, DEFAULT_VALUE)\
	ReadPackedCharCounter(COUNT, ARRAYNAME, DECLTYPE) \
	else{ \
		ARRAYNAME = DEFAULT_VALUE; \
	} \

#define ReadPackedIntCounter_Default(COUNT, ARRAYNAME, DECLTYPE, DEFAULT_VALUE)\
	ReadPackedIntCounter(COUNT, ARRAYNAME, DECLTYPE) \
	else{ \
		ARRAYNAME = DEFAULT_VALUE; \
	} \

//Liest Arrayindex vor Arraywert aus
//Theoretisch könnte man bei Int-Werten beides auch zusammen auslesen,
//indem man ein paar Bits abzweigt. 
//Aber, dazu müsste man nach dem Datentyp unterscheiden.
#define READ_PACKED_ARRAY \
		for( int i=0; i<count; ++i) values[i] = 0; \
		const bool bShortIndex = ( count < 127 ); \
		if( bShortIndex ){ \
			char cPackedLen; \
			Read(&cPackedLen); \
			for( char i=0; i<cPackedLen; ++i){ \
				char cPos; \
				Read(&cPos); \
				Read(&(values[cPos])); \
			} \
		}else{ \
			int iPackedLen; \
			Read(&iPackedLen); \
			for( char i=0; i<iPackedLen; ++i){ \
				int iPos; \
				Read(&iPos); \
				Read(&(values[iPos])); \
			} \
		} \

	void ReadPacked(int count, char values[]) {
		READ_PACKED_ARRAY
	};
	void ReadPacked(int count, byte values[]){
		READ_PACKED_ARRAY
	};
	void ReadPacked(int count, bool values[]){
		READ_PACKED_ARRAY
	};
	void ReadPacked(int count, short values[]){
		//READ_PACKED_ARRAY
		for( int i=0; i<count; ++i) values[i] = 0; 
		const bool bShortIndex = ( count < 127 ); 
		if( bShortIndex ){ 
			char cPackedLen; 
			Read(&cPackedLen); 
			for( char i=0; i<cPackedLen; ++i){ 
				char cPos; 
				Read(&cPos); 
				Read(&(values[cPos])); 
			} 
		}else{ 
			int iPackedLen; 
			Read(&iPackedLen); 
			for( char i=0; i<iPackedLen; ++i){ 
				int iPos; 
				Read(&iPos); 
				Read(&(values[iPos])); 
			} 
		} 
	};
	void ReadPacked(int count, unsigned short values[]){
		READ_PACKED_ARRAY
	};
	void 		ReadPacked(int count, int values[]){
		READ_PACKED_ARRAY
	};
	void 		ReadPacked(int count, unsigned int values[]){
		READ_PACKED_ARRAY
	};
	void 		ReadPacked(int count, long values[]){
		READ_PACKED_ARRAY
	};
	void 		ReadPacked(int count, unsigned long values[]){
		READ_PACKED_ARRAY
	};
	void ReadPacked(int count, float values[]){
		READ_PACKED_ARRAY
	};
	void ReadPacked(int count, double values[]){
		READ_PACKED_ARRAY
	};

	/* Note to COUNT_WRITE:
	 * There exists a bug due writing negative signed chars.
	 * The next readed value would be wrong!!
	 * To omit that, char values will be casted unsigned before they are written.
	 */
#define WRITE_PACKED_ARRAY(COUNT_WRITE) { \
	const int iCount = (int) count; \
	const bool bShortIndex = (iCount < 127); \
	int iPackedLen = 0; \
	for( int i=0; i<iCount; ++i){ \
		if( values[i] != 0 ) ++iPackedLen; \
	} \
	const int sizeNormalSave = sizeof(values[0])*count; \
	const int sizePackedSave = ((bShortIndex?1:4)+sizeof(values[0]))*iPackedLen; \
	\
	if( sizeNormalSave <= sizePackedSave ){ \
		Write(count); \
		Write(count, values); \
	}else{ \
		COUNT_WRITE \
		if( bShortIndex ){ \
			Write((char)iPackedLen); \
			if( iPackedLen ) \
			for( int i=0; i<iCount; ++i){ \
				if( values[i] != 0 ){ \
					Write((char)i); \
					Write(values[i]); \
				} \
			} \
		}else{ \
			Write(iPackedLen); \
			if( iPackedLen )/*redundant*/ \
			for( int i=0; i<iCount; ++i){ \
				if( values[i] != 0 ){ \
					Write(i); \
					Write(values[i]); \
				} \
			} \
		} \
	} \
} \

#define WRITE_PACKED_ARRAY_CHAR  \
	WRITE_PACKED_ARRAY( Write( (unsigned char) -count ); ) \

#define WRITE_PACKED_ARRAY_INT  \
	WRITE_PACKED_ARRAY( Write( -count ); ) \

void WritePacked(char count, const  char values[]) {
	WRITE_PACKED_ARRAY_CHAR
};
void WritePacked(char count, const  byte values[]) {
	WRITE_PACKED_ARRAY_CHAR
};
void WritePacked(char count, const bool values[]) {
	WRITE_PACKED_ARRAY_CHAR
};
void WritePacked(char count, const short values[]) {
	WRITE_PACKED_ARRAY_CHAR
};

void WritePacked(char count, const unsigned short values[])  {
	WRITE_PACKED_ARRAY_CHAR
};
void 		WritePacked(char count, const int values[]) {
	WRITE_PACKED_ARRAY_CHAR
};
void WritePacked(char count, const unsigned int values[])  {
	WRITE_PACKED_ARRAY_CHAR
};
void 		WritePacked(char count, const long values[]) {
	WRITE_PACKED_ARRAY_CHAR
};
void WritePacked(char count, const unsigned long values[])  {
	WRITE_PACKED_ARRAY_CHAR
};
void WritePacked(char count, const float values[]) {
	WRITE_PACKED_ARRAY_CHAR
};
void WritePacked(char count, const double values[]) {
	WRITE_PACKED_ARRAY_CHAR
};

void WritePacked(int count, const  char values[]) {
	WRITE_PACKED_ARRAY_INT
};
void WritePacked(int count, const  byte values[]) {
	WRITE_PACKED_ARRAY_INT
};
void WritePacked(int count, const bool values[]) {
	WRITE_PACKED_ARRAY_INT
};
void WritePacked(int count, const short values[]) {
	WRITE_PACKED_ARRAY_INT
};
void WritePacked(int count, const unsigned short values[])  {
	WRITE_PACKED_ARRAY_INT
};
void 		WritePacked(int count, const int values[]) {
	WRITE_PACKED_ARRAY_INT
};
void WritePacked(int count, const unsigned int values[])  {
	WRITE_PACKED_ARRAY_INT
};
void 		WritePacked(int count, const long values[]) {
	WRITE_PACKED_ARRAY_INT
};
void WritePacked(int count, const unsigned long values[])  {
	WRITE_PACKED_ARRAY_INT
};
void WritePacked(int count, const float values[]) {
	WRITE_PACKED_ARRAY_INT
};
void WritePacked(int count, const double values[]) {
	WRITE_PACKED_ARRAY_INT
};

};

#endif	//FDATASTREAMBASE_H
