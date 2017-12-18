# Extracted from CvDLLUtilityIFaceBase.h
# There exists no Python interface file, but at least
# a subset of this function is available after 
# 'from CvPythonExtensions import *' 

# class CvPythonExtensions:
"""
// accessors for other abstract interfaces
virtual CvDLLEntityIFaceBase* getEntityIFace() = 0;
virtual CvDLLInterfaceIFaceBase* getInterfaceIFace() = 0;
virtual CvDLLEngineIFaceBase* getEngineIFace() = 0;
virtual CvDLLIniParserIFaceBase* getIniParserIFace() = 0;
virtual CvDLLSymbolIFaceBase* getSymbolIFace() = 0;
virtual CvDLLFeatureIFaceBase* getFeatureIFace() = 0;
virtual CvDLLRouteIFaceBase* getRouteIFace() = 0;
virtual CvDLLPlotBuilderIFaceBase* getPlotBuilderIFace() = 0;
virtual CvDLLRiverIFaceBase* getRiverIFace() = 0;
virtual CvDLLFAStarIFaceBase* getFAStarIFace() = 0;
virtual CvDLLXmlIFaceBase* getXMLIFace() = 0;
virtual CvDLLFlagEntityIFaceBase* getFlagEntityIFace() = 0;
virtual CvDLLPythonIFaceBase* getPythonIFace() = 0;

virtual void delMem(void *p) = 0;
virtual void* newMem(size_t size) = 0;

virtual void delMem(void *p, const char* pcFile, int iLine) = 0;
virtual void* newMem(size_t size, const char* pcFile, int iLine) = 0;

virtual void delMemArray(void *p, const char* pcFile, int iLine) = 0;
virtual void* newMemArray(size_t size, const char* pcFile, int iLine) = 0;

virtual void* reallocMem(void* a, unsigned int uiBytes, const char* pcFile, int iLine) = 0; 
virtual unsigned int memSize(void* a) = 0;

virtual void clearVector(std::vector<int>& vec) = 0;
virtual void clearVector(std::vector<byte>& vec) = 0;
virtual void clearVector(std::vector<float>& vec) = 0;
"""

def getAssignedNetworkID(iPlayerID):
    return int()

def isConnected(iNetID):
    return bool()

def isGameActive():
    return bool()

def GetLocalNetworkID():
    return int()

def GetSyncOOS(iNetID):
    return int()

def GetOptionsOOS(iNetID):
    return int()

def GetLastPing(iNetID):
    return int()


def IsModem():
    return bool()

def SetModem(bModem):
    pass


def AcceptBuddy(szName, iRequestID):
    pass

def RejectBuddy(szName, iRequestID):
    pass

def messageControlLog(s):
    pass

def getChtLvl():
    return int()

def setChtLvl(iLevel):
    pass

def GetWorldBuilderMode():
    return bool()

def getCurrentLanguage():
    return int()

def setCurrentLanguage(iNewLanguage):
    pass

def isModularXMLLoading():
    return bool()

def IsPitbossHost():
    return bool()

def GetPitbossSmtpHost():
    return str()

def GetPitbossSmtpLogin():
    return str()

def GetPitbossSmtpPassword():
    return str()

def GetPitbossEmail():
    return str()

def sendMessageData(pData):  #  CvMessageData* 
    pass

def sendPlayerInfo(eActivePlayer):
    pass

def sendGameInfo(szGameName, szAdminPassword):
    pass

def sendPlayerOption(eOption, bValue):
    pass

def sendChat(szChatString, eTarget):
    pass

def sendPause(iPauseID):
    pass

def sendMPRetire():
    pass

def sendToggleTradeMessage(eWho, eItemType, iData, iOtherWho, bAIOffer, bSendToAll):
    return bool()

def sendClearTableMessage(eWhoTradingWith):
    pass

# virtual void sendImplementDealMessage(PlayerTypes eOtherWho, CLinkList<TradeData>* pOurList, CLinkList<TradeData>* pTheirList) = 0;

def sendContactCiv(eContactType, eWho):
    pass

def sendOffer():
    pass

def sendDiploEvent(eWhoTradingWith, eDiploEvent, iData1, iData2):
    pass

def sendRenegotiate(eWhoTradingWith):
    pass

def sendRenegotiateThisItem(ePlayer2, eItemType, iData):
    pass

def sendExitTrade():
    pass

def sendKillDeal(iDealID, bFromDiplomacy):
    return int()

def sendDiplomacy(ePlayer, pParams):  # CvDiploParameters*
    pass

def sendPopup(ePlayer, pInfo):  # CvPopupInfo*
    pass

def getMillisecsPerTurn():
    return int()

def getSecsPerTurn():
    return float()

def getTurnsPerSecond():
    return int()

def getTurnsPerMinute():
    return int()


def openSlot(eID):
    pass

def closeSlot(eID):
    pass


def getMapScriptName():
    return str()

def getTransferredMap():
    return bool()

def isDescFileName(szFileName):
    return bool()

def isWBMapScript():
    return bool()

def isWBMapNoPlayers():
    return bool()

def pythonMapExists(szMapName):
    return bool()

def stripSpecialCharacters(szName):
    pass

def initGlobals():
    pass

def uninitGlobals():
    pass

def callUpdater():
    pass

# virtual bool Uncompress(byte** bufIn, unsigned long* bufLenIn, unsigned long maxBufLenOut, int offset=0) = 0;
# virtual bool Compress(byte** bufIn, unsigned long* bufLenIn, int offset=0) = 0;

def NiTextOut(szText):
    pass

def MessageBox(szText, szCaption):
    pass

def SetDone(bDone):
    pass

def GetDone():
    return bool()

def GetAutorun():
    return bool()

def beginDiplomacy(pDiploParams, ePlayer):  # CvDiploParameters*
    pass

def endDiplomacy():
    pass

def isDiplomacy():
    return bool()

def getDiplomacyPlayer():
    return int()

def updateDiplomacyAttitude(bForce):
    pass

def isMPDiplomacy():
    return bool()

def isMPDiplomacyScreenUp():
    return bool()
    pass

def getMPDiplomacyPlayer():
    return int()

def beginMPDiplomacy(eWhoTalkingTo, bRenegotiate, bSimultaneous):
    pass

def endMPDiplomacy():
    pass

def getAudioDisabled():
    return bool()
    pass

def getAudioTagIndex(szTag, iScriptType):
    return int()


def DoSound(iScriptId):
    pass

def Do3DSound( iScriptId, vPosition ):  # NiPoint3
    pass

"""
virtual FDataStreamBase* createFileStream() = 0;
virtual void destroyDataStream(FDataStreamBase*& stream) = 0;

virtual CvCacheObject* createGlobalTextCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createGlobalDefinesCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createTechInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createBuildingInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createUnitInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createLeaderHeadInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createCivilizationInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createPromotionInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createDiplomacyInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createEventInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createEventTriggerInfoCacheObject(const TCHAR* szCacheFileName) = 0;

virtual CvCacheObject* createCivicInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createHandicapInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createBonusInfoCacheObject(const TCHAR* szCacheFileName) = 0;
virtual CvCacheObject* createImprovementInfoCacheObject(const TCHAR* szCacheFileName) = 0;

virtual bool cacheRead(CvCacheObject* pCache, const TCHAR* szSourceFileName=NULL) = 0;
virtual bool cacheWrite(CvCacheObject* pCache) = 0;
virtual void destroyCache(CvCacheObject*& pCache) = 0;

virtual bool fileManagerEnabled() = 0;
"""


def logMsg(pLogFileName, pBuf, bWriteToConsole, bTimeStamp):
    pass

def logMemState(msg):
    pass

# In CyGame
# virtual int getSymbolID(int iID) = 0;

# virtual void setSymbolID(int iID, int iValue) = 0;

# In CyTranslator
# virtual CvWString getText(CvWString szIDTag, ...) = 0;
# virtual CvWString getObjectText(CvWString szIDTag, uint uiForm, bool bNoSubs = false) = 0;

# virtual void addText(const TCHAR* szIDTag, const wchar* szString, const wchar* szGender = L"N", const wchar* szPlural = L"false") = 0;		
#virtual uint getNumForms(CvWString szIDTag) = 0;

# In CyMap
# virtual WorldSizeTypes getWorldSize() = 0;

"""
virtual uint getFrameCounter() const = 0;

virtual bool altKey() = 0;
virtual bool shiftKey() = 0;
virtual bool ctrlKey() = 0;
virtual bool scrollLock() = 0;
virtual bool capsLock() = 0;
virtual bool numLock() = 0;

virtual void ProfilerBegin()=0;
virtual void ProfilerEnd()=0;
virtual void BeginSample(ProfileSample *pSample)=0;
virtual void EndSample(ProfileSample *pSample)=0;
virtual bool isGameInitializing() = 0;

virtual void enumerateFiles(std::vector<CvString>& files, const char* szPattern) = 0;
virtual void enumerateModuleFiles(std::vector<CvString>& aszFiles, const CvString& refcstrRootDirectory,	const CvString&	refcstrModularDirectory, const CvString& refcstrExtension, bool bSearchSubdirectories) = 0;

virtual void SaveGame(SaveGameTypes eSaveGame) = 0;
virtual void LoadGame() = 0;
virtual int loadReplays(std::vector<CvReplayInfo*>& listReplays) = 0;
virtual void QuickSave() = 0;
virtual void QuickLoad() = 0;
virtual void sendPbemTurn(PlayerTypes ePlayer) = 0;
virtual void getPassword(PlayerTypes ePlayer) = 0;
"""

# In CyUserProfile
# virtual bool getGraphicOption(GraphicOptionTypes eGraphicOption) = 0;
# virtual bool getPlayerOption(PlayerOptionTypes ePlayerOption) = 0;


"""
virtual int getMainMenu() = 0;

virtual bool isFMPMgrHost() = 0;
virtual bool isFMPMgrPublic() = 0;
virtual void handleRetirement(PlayerTypes ePlayer) = 0;
virtual PlayerTypes getFirstBadConnection() = 0;
virtual int getConnState(PlayerTypes ePlayer) = 0;

virtual bool ChangeINIKeyValue(const char* szGroupKey, const char* szKeyValue, const char* szOut) = 0;

virtual char* md5String(char* szString) = 0;
"""

# In CyPitboss
# virtual const char* getModName(bool bFullPath = true) const = 0;

# In CyGame
# virtual bool hasSkippedSaveChecksum() const = 0;

#virtual void reportStatistics() = 0;
