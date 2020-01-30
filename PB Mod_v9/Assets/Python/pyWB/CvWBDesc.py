from CvPythonExtensions import *
import os
import sys
import CvUtil
from array import *

from CvWBKeys import *

try:
    import CvPlatyBuilderScreen
    WITH_PLATY = True
except:
    WITH_PLATY = False

# globals
gc = CyGlobalContext()
version = 11
#fileencoding = "latin_1" # aka "iso-8859-1" # previous value
fileencoding = "utf-8"
fileencodingOld = "latin_1"
localText = CyTranslator()

""" Flag to disable tech/building workaround
  for first szenario loading. At first startup, it
  would start many events (wonder build, religion found, etc).
"""
global bFirstWrite
bFirstWrite = True

#############
def getPlayer(idx):
    "helper function which wraps get player in case of bad index"
    if (gc.getPlayer(idx).isAlive()):
        return gc.getPlayer(idx)
    return None

"""
Remove high Ids which does not matching to the loaded DLL version
Moreover, shift Barbarian civ (highest id) on last position.
Assume that the input list is ordered (=>highest value at the end).
"""
NUM_CIV_PLAYERS = gc.getMAX_CIV_PLAYERS() # 18 or 40 or 52
barb_idWB = None # No constant value. Will be set during loading of WBSave.

def filterPlayerIds(list_of_ids, barb_id):
    """ Identity function on player ids and remap of barbarian_id """
    if barb_id is not None:
        l = filter(lambda x: x < NUM_CIV_PLAYERS, list_of_ids)
        if len(list_of_ids) > 0 and list_of_ids[-1] == barb_id:
            if len(list_of_ids) == len(l):
                l[-1] = NUM_CIV_PLAYERS
            else:  # Case used if 52/40 WBSave loaded without DLL
                l.append(NUM_CIV_PLAYERS)

        return l
    else:
        return filter(lambda x: x <= NUM_CIV_PLAYERS, list_of_ids)

def filterPlayerIds2(list_of_ids, barb_id):
    # Same as above but compare id with sub-entry.
    if barb_id is not None:
        l = filter(lambda x: x[0] < NUM_CIV_PLAYERS, list_of_ids)
        if len(list_of_ids) > 0 and list_of_ids[-1][0] == barb_id:
            b = [NUM_CIV_PLAYERS]
            b.extend(list_of_ids[-1][1:])
            if len(list_of_ids) == len(l):
                l[-1] = b
            else:  # Case used if 52/40 WBSave loaded without DLL
                l.append(b)

        return l
    else:
        return filter(lambda x: x[0] <= NUM_CIV_PLAYERS, list_of_ids)

def init_filter():

    global filterPlayerIds
    global filterPlayerIds2
    filterPlayerIds = _filterPlayerIds
    filterPlayerIds2 = _filterPlayerIds2

# Note that getText() returns "x:y:z:w" for civ adjectives.
def findKey(keylist, value):
    value = value.encode(fileencoding)
    for key in keylist:
        if(value in localText.getText(key,()).encode(fileencoding).split(":")):
            return key
    return None

#############
class CvWBParser:
    "parser functions for WB desc"
    def getTokens(self, line):
        "return a list of (comma separated) tokens from the line.  Strip whitespace on each token"
        if line == None:
            return list()

        # Do not split ScriptData lines
        if "ScriptData" in line:
                toks = [line]
        else:
                toks=line.split(",")
        toksOut=list()
        for tok in toks:
            toksOut.append(tok.strip())
        return toksOut

    def findToken(self, toks, item):
        "return True if item exists in list of tokens"
        for tok in toks:
            if (tok == item):
                return True
        return False

    def findTokenValue(self, toks, item):
        "Search for a token of the form item=value in the list of toks, and return value, or -1 if not found"
        for tok in toks:
            l=tok.split("=")
            if (item == l[0]):
                if (len(l) == 1):
                    return item
                return l[1]
        return -1   # failed

    def getNextLine(self, f):
        "return the next line from the list of lines"
        return f.readline()

    def findNextToken(self, f, item):
        "Find the next line that contains the token item, return False if not found"
        while True:
            line = self.getNextLine(f)
            if (not line):
                return False  # EOF
            toks=self.getTokens(line)
            if (self.findToken(toks, item)):
                return True
        return False

    def findNextTokenValue(self, f, item):
        "Find the next line that contains item=value, return value or -1 if not found"
        while True:
            line = self.getNextLine(f)
            if (not line):
                return -1   # EOF
            toks=self.getTokens(line)
            val=self.findTokenValue(toks, item)
            if (val != -1):
                return val
        return -1

#############
class CvGameDesc:
    "class for serializing game data"
    def __init__(self):
        self.eraType = "NONE"
        self.speedType = "NONE"
        self.calendarType = "CALENDAR_DEFAULT"
        self.options = ()
        self.mpOptions = ()
        self.forceControls = ()
        self.victories = ()
        self.gameTurn = 0
        self.maxTurns = 0
        self.maxCityElimination = 0
        self.numAdvancedStartPoints = 0
        self.targetScore = 0
        self.iStartYear = -4000
        self.szDescription = ""
        self.szModPath = ""
        self.iRandom = 0

    def apply(self):
        "after reading, apply the game data"
        gc.getGame().setStartYear(self.iStartYear)

    def write(self, f):
        "write out game data"
        f.write("BeginGame\n")
        f.write("\tEra=%s\n" %(gc.getEraInfo(gc.getGame().getStartEra()).getType(),))
        f.write("\tSpeed=%s\n" %(gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getType(),))
        f.write("\tCalendar=%s\n" %(gc.getCalendarInfo(gc.getGame().getCalendar()).getType(),))

        # write options
        for i in range(gc.getNumGameOptionInfos()):
            if (gc.getGame().isOption(i)):
                f.write("\tOption=%s\n" %(gc.getGameOptionInfo(i).getType()))

        # write mp options
        for i in range(gc.getNumMPOptionInfos()):
            if (gc.getGame().isMPOption(i)):
                f.write("\tMPOption=%s\n" %(gc.getMPOptionInfo(i).getType()))

        # write force controls
        for i in range(gc.getNumForceControlInfos()):
            if (gc.getGame().isForcedControl(i)):
                f.write("\tForceControl=%s\n" %(gc.getForceControlInfo(i).getType()))

        # write victories
        for i in range(gc.getNumVictoryInfos()):
            if (gc.getGame().isVictoryValid(i)):
                if (not gc.getVictoryInfo(i).isPermanent()):
                    f.write("\tVictory=%s\n" %(gc.getVictoryInfo(i).getType()))

        f.write("\tGameTurn=%d\n" %(gc.getGame().getGameTurn(),))
        f.write("\tMaxTurns=%d\n" %(gc.getGame().getMaxTurns(),))
        f.write("\tMaxCityElimination=%d\n" %(gc.getGame().getMaxCityElimination(),))
        f.write("\tNumAdvancedStartPoints=%d\n" %(gc.getGame().getNumAdvancedStartPoints(),))
        f.write("\tTargetScore=%d\n" %(gc.getGame().getTargetScore(),))

        f.write("\tStartYear=%d\n" %(gc.getGame().getStartYear(),))
        f.write("\tDescription=%s\n" % (self.szDescription,))
        f.write("\tModPath=%s\n" % (self.szModPath,))
        f.write("EndGame\n")

    def read(self, f):
        "read in game data"
        self.__init__()

        parser = CvWBParser()
        if (parser.findNextTokenValue(f, "BeginGame")!=-1):
            while True:
                nextLine = parser.getNextLine(f)
                toks = parser.getTokens(nextLine)
                if (len(toks) == 0):
                    break

                v = parser.findTokenValue(toks, "Era")
                if v!=-1:
                    self.eraType = v
                    continue

                v = parser.findTokenValue(toks, "Speed")
                if v!=-1:
                    self.speedType = v
                    continue

                v = parser.findTokenValue(toks, "Calendar")
                if v!=-1:
                    self.calendarType = v
                    continue

                v = parser.findTokenValue(toks, "Option")
                if v!=-1:
                    self.options = self.options + (v,)
                    continue

                v = parser.findTokenValue(toks, "MPOption")
                if v!=-1:
                    self.mpOptions = self.mpOptions + (v,)
                    continue

                v = parser.findTokenValue(toks, "ForceControl")
                if v!=-1:
                    self.forceControls = self.forceControls + (v,)
                    continue

                v = parser.findTokenValue(toks, "Victory")
                if v!=-1:
                    self.victories = self.victories + (v,)
                    continue

                v = parser.findTokenValue(toks, "GameTurn")
                if v!=-1:
                    self.gameTurn = int(v)
                    continue

                v = parser.findTokenValue(toks, "MaxTurns")
                if v!=-1:
                    self.maxTurns = int(v)
                    continue

                v = parser.findTokenValue(toks, "MaxCityElimination")
                if v!=-1:
                    self.maxCityElimination = int(v)
                    continue

                v = parser.findTokenValue(toks, "NumAdvancedStartPoints")
                if v!=-1:
                    self.numAdvancedStartPoints = int(v)
                    continue

                v = parser.findTokenValue(toks, "TargetScore")
                if v!=-1:
                    self.targetScore = int(v)
                    continue

                v = parser.findTokenValue(toks, "StartYear")
                if v!=-1:
                    self.iStartYear = int(v)
                    continue

                v = parser.findTokenValue(toks, "Description")
                if v!=-1:
                    self.szDescription = v
                    continue

                v = parser.findTokenValue(toks, "ModPath")
                if v!=-1:
                    self.szModPath = v
                    continue

                v = parser.findTokenValue(toks, "Random")
                if v!=-1:
                    self.iRandom = int(v)
                    continue

                if parser.findTokenValue(toks, "EndGame") != -1:
                    break

#############
class CvTeamDesc:
    def __init__(self):
        self.techTypes = ()
        self.aaiEspionageAgainstTeams = []
        self.bContactWithTeamList = ()
        self.bWarWithTeamList = ()
        self.bPermanentWarPeaceList = ()
        self.bOpenBordersWithTeamList = ()
        self.bDefensivePactWithTeamList = ()
        self.bVassalOfTeamList = ()
        self.projectType = []
        self.bRevealMap = 0
        self.iMasterPower = 0
        self.iVassalPower = 0
        self.iEspionageEver = 0
    ## Platy Builder ##
        self.bMapCentering = 0
        self.bMapTrading = 0
        self.bTechTrading = 0
        self.bGoldTrading = 0
        self.bOpenBordersTrading = 0
        self.bDefensivePactTrading = 0
        self.bPermanentAllianceTrading = 0
        self.bVassalStateTrading = 0
        self.bBridgeBuilding = 0
        self.bIrrigation = 0
        self.bIgnoreIrrigation = 0
        self.bWaterWork = 0
        self.bExtraWaterSeeFrom = 0
        self.iNukeInterception = 0
        self.iEnemyWarWeariness = 0
        self.lDomainMoves = []
        self.lRouteMoves = []
        self.lImprovementYield = []

    def write(self, f, idx):
        "write out team data"
        f.write("BeginTeam\n")
        pTeam = gc.getTeam(idx)

        # Team ID (to make things easier to mess with in the text)
        f.write("\tTeamID=%d\n" %(idx))

        # write techs
        global teamTechs
        techs = teamTechs[idx]
        for i in techs:
            f.write("\tTech=%s\n" %(gc.getTechInfo(i).getType()))

            if gc.getTechInfo(i).isRepeat():
                for j in range(pTeam.getTechCount(i)):
                    f.write("\tTech=%s\n" %(gc.getTechInfo(i).getType()))


        # write Espionage against other teams
        for i in range(gc.getMAX_TEAMS()):
            if pTeam.getEspionagePointsAgainstTeam(i) > 0:
                f.write("\tEspionageTeam=%d, EspionageAmount=%d\n" %(i, gc.getTeam(idx).getEspionagePointsAgainstTeam(i)))

        # write Espionage Ever against other teams
        if pTeam.getEspionagePointsEver() > 0:
            f.write("\tEspionageEverAmount=%d\n" %(gc.getTeam(idx).getEspionagePointsEver()))
    ## Platy Builder ##
        for i in range(gc.getMAX_TEAMS()):
            if i == idx: continue
            if gc.getTeam(i).isBarbarian(): continue
            if pTeam.isHasMet(i):
                f.write("\tContactWithTeam=%d\n" %(i))
    ## Platy Builder ##
        # write warring teams
        for i in range(gc.getMAX_TEAMS()):
            if gc.getTeam(i).isBarbarian(): continue
            if pTeam.isAtWar(i):
                f.write("\tAtWar=%d\n" %(i))

        # write permanent war/peace teams
        for i in range(gc.getMAX_TEAMS()):
            if pTeam.isPermanentWarPeace(i):
                f.write("\tPermanentWarPeace=%d\n" %(i))

        # write open borders other teams
        for i in range(gc.getMAX_TEAMS()):
            if pTeam.isOpenBorders(i):
                f.write("\tOpenBordersWithTeam=%d\n" %(i))

        # write defensive pact other teams
        for i in range(gc.getMAX_TEAMS()):
            if pTeam.isDefensivePact(i):
                f.write("\tDefensivePactWithTeam=%d\n" %(i))

        # write vassal state
        for i in range(gc.getMAX_TEAMS()):
            if pTeam.isVassal(i):
                f.write("\tVassalOfTeam=%d\n" %(i))

        for i in range(gc.getNumProjectInfos()):
            for j in range(pTeam.getProjectCount(i)):
                f.write("\tProjectType=%s\n" %(gc.getProjectInfo(i).getType()))

        f.write("\tRevealMap=%d\n" %(0))

        if gc.getTeam(idx).getVassalPower() != 0:
            f.write("\tVassalPower=%d\n" %(pTeam.getVassalPower()))
        if gc.getTeam(idx).getMasterPower() != 0:
            f.write("\tMasterPower=%d\n" %(pTeam.getMasterPower()))
    ## Platy Builder ##
        if pTeam.isMapCentering():
            f.write("\tMapCentering=1\n")
        if pTeam.isMapTrading():
            f.write("\tMapTrading=1\n")
        if pTeam.isTechTrading():
            f.write("\tTechTrading=1\n")
        if pTeam.isGoldTrading():
            f.write("\tGoldTrading=1\n")
        if pTeam.isOpenBordersTrading():
            f.write("\tOpenBordersTrading=1\n")
        if pTeam.isDefensivePactTrading():
            f.write("\tDefensivePactTrading=1\n")
        if pTeam.isPermanentAllianceTrading():
            f.write("\tPermanentAllianceTrading=1\n")
        if pTeam.isVassalStateTrading():
            f.write("\tVassalStateTrading=1\n")
        if pTeam.isBridgeBuilding():
            f.write("\tBridgeBuilding=1\n")
        if pTeam.isIrrigation():
            f.write("\tIrrigation=1\n")
        if pTeam.isIgnoreIrrigation():
            f.write("\tIgnoreIrrigation=1\n")
        if pTeam.isWaterWork():
            f.write("\tWaterWork=1\n")
        if pTeam.isExtraWaterSeeFrom():
            f.write("\tExtraWaterSeeFrom=1\n")
        if pTeam.getNukeInterception() != 0:
            f.write("\tNukeInterception=%d\n" %(pTeam.getNukeInterception()))
        if pTeam.getEnemyWarWearinessModifier() != 0:
            f.write("\tEnemyWarWeariness=%d\n" %(pTeam.getEnemyWarWearinessModifier()))

        for item in xrange(DomainTypes.NUM_DOMAIN_TYPES):
            if pTeam.getExtraMoves(item) != 0:
                f.write("\tDomainType=%s, ExtraMoves=%d\n" %(gc.getDomainInfo(item).getType(), pTeam.getExtraMoves(item)))
        for item in xrange(gc.getNumRouteInfos()):
            if pTeam.getRouteChange(item) != 0:
                f.write("\tRouteType=%s, ExtraMoves=%d\n" %(gc.getRouteInfo(item).getType(), pTeam.getRouteChange(item)))
        for item in xrange(gc.getNumImprovementInfos()):
            for k in xrange(YieldTypes.NUM_YIELD_TYPES):
                if pTeam.getImprovementYieldChange(item, k) != 0:
                    f.write("\tImprovementType=%s, YieldType=%s, ExtraYield=%d\n" %(gc.getImprovementInfo(item).getType(), gc.getYieldInfo(k).getType(), pTeam.getImprovementYieldChange(item, k)))

        # Restore Techs
        for i in techs:
            pTeam.setHasTech(i, True, PlayerTypes.NO_PLAYER, False, False)

        f.write("EndTeam\n")

    def read(self, f):
        "read in team data"
        self.__init__()

        parser = CvWBParser()
        if (parser.findNextTokenValue(f, "BeginTeam") != -1):
            while True:
                nextLine = parser.getNextLine(f)
                toks = parser.getTokens(nextLine)
                if (len(toks) == 0):
                    break

                v = parser.findTokenValue(toks, "Tech")
                if v!=-1:
                    self.techTypes = self.techTypes + (v,)
                    continue

                v = parser.findTokenValue(toks, "EspionageTeam")
                if v!=-1:
                    iTeam = int(v)

                    iExtra = int(parser.findTokenValue(toks, "EspionageAmount"))
                    self.aaiEspionageAgainstTeams.append([iTeam,iExtra])
                    continue

                v = parser.findTokenValue(toks, "EspionageEverAmount")
                if v!=-1:
                    self.iEspionageEver = int(v)
                    continue

                v = parser.findTokenValue(toks, "ContactWithTeam")
                if v!=-1:
                    self.bContactWithTeamList = self.bContactWithTeamList + (int(v),)
                    continue

                v = parser.findTokenValue(toks, "AtWar")
                if v!=-1:
                    self.bWarWithTeamList = self.bWarWithTeamList + (int(v),)
                    continue

                v = parser.findTokenValue(toks, "PermanentWarPeace")
                if v!=-1:
                    self.bPermanentWarPeaceList = self.bPermanentWarPeaceList + (int(v),)
                    continue

                v = parser.findTokenValue(toks, "OpenBordersWithTeam")
                if v!=-1:
                    self.bOpenBordersWithTeamList = self.bOpenBordersWithTeamList + (int(v),)
                    continue

                v = parser.findTokenValue(toks, "DefensivePactWithTeam")
                if v!=-1:
                    self.bDefensivePactWithTeamList = self.bDefensivePactWithTeamList + (int(v),)
                    continue

                v = parser.findTokenValue(toks, "VassalOfTeam")
                if v!=-1:
                    self.bVassalOfTeamList = self.bVassalOfTeamList + (int(v),)
                    continue

                v = parser.findTokenValue(toks, "ProjectType")
                if v!=-1:
                    self.projectType.append(v)
                    continue

                v = parser.findTokenValue(toks, "RevealMap")
                if v!=-1:
                    self.bRevealMap = int(v)
                    continue

                v = parser.findTokenValue(toks, "VassalPower")
                if v!=-1:
                    self.iVassalPower = int(v)
                    continue

                v = parser.findTokenValue(toks, "MasterPower")
                if v!=-1:
                    self.iMasterPower = int(v)
                    continue
            ## Platy Builder
                v = parser.findTokenValue(toks, "MapCentering")
                if v!=-1:
                    self.bMapCentering = int(v)
                    continue
                v = parser.findTokenValue(toks, "MapTrading")
                if v!=-1:
                    self.bMapTrading = int(v)
                    continue
                v = parser.findTokenValue(toks, "TechTrading")
                if v!=-1:
                    self.bTechTrading = int(v)
                    continue
                v = parser.findTokenValue(toks, "GoldTrading")
                if v!=-1:
                    self.bGoldTrading = int(v)
                    continue
                v = parser.findTokenValue(toks, "OpenBordersTrading")
                if v!=-1:
                    self.bOpenBordersTrading = int(v)
                    continue
                v = parser.findTokenValue(toks, "DefensivePactTrading")
                if v!=-1:
                    self.bDefensivePactTrading = int(v)
                    continue
                v = parser.findTokenValue(toks, "PermanentAllianceTrading")
                if v!=-1:
                    self.bPermanentAllianceTrading = int(v)
                    continue
                v = parser.findTokenValue(toks, "VassalStateTrading")
                if v!=-1:
                    self.bVassalStateTrading = int(v)
                    continue
                v = parser.findTokenValue(toks, "BridgeBuilding")
                if v!=-1:
                    self.bBridgeBuilding = int(v)
                    continue
                v = parser.findTokenValue(toks, "Irrigation")
                if v!=-1:
                    self.bIrrigation = int(v)
                    continue
                v = parser.findTokenValue(toks, "IgnoreIrrigation")
                if v!=-1:
                    self.bIgnoreIrrigation = int(v)
                    continue
                v = parser.findTokenValue(toks, "WaterWork")
                if v!=-1:
                    self.bWaterWork = int(v)
                    continue
                v = parser.findTokenValue(toks, "ExtraWaterSeeFrom")
                if v!=-1:
                    self.bExtraWaterSeeFrom = int(v)
                    continue
                v = parser.findTokenValue(toks, "NukeInterception")
                if v!=-1:
                    self.iNukeInterception = int(v)
                    continue
                v = parser.findTokenValue(toks, "EnemyWarWeariness")
                if v!=-1:
                    self.iEnemyWarWeariness = int(v)
                    continue
                v = parser.findTokenValue(toks, "DomainType")
                if v!=-1:
                    item = gc.getInfoTypeForString(v)
                    iExtra = int(parser.findTokenValue(toks, "ExtraMoves"))
                    self.lDomainMoves.append([item,iExtra])
                    continue
                v = parser.findTokenValue(toks, "RouteType")
                if v!=-1:
                    item = gc.getInfoTypeForString(v)
                    iExtra = int(parser.findTokenValue(toks, "ExtraMoves"))
                    self.lRouteMoves.append([item,iExtra])
                    continue
                v = parser.findTokenValue(toks, "ImprovementType")
                if v!=-1:
                    item = gc.getInfoTypeForString(v)
                    iYield = gc.getInfoTypeForString(parser.findTokenValue(toks, "YieldType"))
                    iExtra = int(parser.findTokenValue(toks, "ExtraYield"))
                    self.lImprovementYield.append([item,iYield,iExtra])
                    continue

                if parser.findTokenValue(toks, "EndTeam") != -1:
                    return True   # completed successfully

        return False  # failed


#############
class CvPlayerDesc:
    def __init__(self):
        self.szCivDesc = ""
        self.szCivShortDesc = ""
        self.szLeaderName = ""
        self.szCivAdjective = ""
        self.szFlagDecal = ""
        self.isWhiteFlag = 0

        self.leaderType = "NONE"
        self.civType = "NONE"
        self.handicap = gc.getHandicapInfo(gc.getDefineINT("STANDARD_HANDICAP")).getType()
        self.team = -1    # team index
        self.color = "NONE"
        self.artStyle = "NONE"
        self.isPlayableCiv = 1
        self.isMinorNationCiv = 0
        self.iStartingGold = 0
        self.iStartingX = -1
        self.iStartingY = -1
        self.stateReligion = ""
        self.szStartingEra = ""
        self.bRandomStartLocation = "false"

        self.aaiCivics = []
        self.aaiAttitudeExtras = []
        self.aszCityList = []

    ## Platy Builder ##
        self.iGoldenAge = 0
        self.iAnarchy = 0
        self.iCombatXP = 0
        self.iCoastalTradeRoute = 0
        self.iStateReligionUnit = 0
        self.iStateReligionBuilding = 0
        self.szScriptData = ""

    def write(self, f, idx):
        "write out player data"
        f.write("BeginPlayer\n")
        pPlayer = gc.getPlayer(idx)

        # write team
        f.write("\tTeam=%d\n" %(int(pPlayer.getTeam())))

    ## Platy Builder ##
        if pPlayer.getLeaderType() != LeaderHeadTypes.NO_LEADER:
            leaderheadInfo = gc.getLeaderHeadInfo(pPlayer.getLeaderType())
            f.write("\tLeaderType=%s\n" %(leaderheadInfo.getType()))

            leaderName = pPlayer.getNameKey()
            defaultLeaderName = leaderheadInfo.getDescription()
            defaultLeaderKey = leaderheadInfo.getTextKey()
            if(leaderName == defaultLeaderName):
                f.write("\tLeaderName=%s\n" %(defaultLeaderKey.encode(fileencoding)))
            else:
                leaderKey = findKey(LeaderKeys, leaderName)
                if(leaderKey) :
                    f.write("\tLeaderName=%s\n" %(leaderKey.encode(fileencoding)))
                else:
                    f.write("\tLeaderName=%s\n" %(leaderName.encode(fileencoding)))

        if pPlayer.getCivilizationType() != CivilizationTypes.NO_CIVILIZATION:
            civInfo = gc.getCivilizationInfo(pPlayer.getCivilizationType())
            civDesc = pPlayer.getCivilizationDescription(0) # PAE: Note that Planty used getCivilizationDescriptionKey()
            civShortDesc = pPlayer.getCivilizationShortDescription(0) # PAE: Note that Planty used getCivilizationShortDescriptionKey()
            civAdjective = pPlayer.getCivilizationAdjective(0) # PAE: Note that Planty used getCivilizationAdjectiveKey()
            defaultDesc = civInfo.getDescription()
            defaultShortDesc = civInfo.getShortDescription(0)
            defaultAdjective = civInfo.getAdjective(0)

            if(civDesc.encode(fileencoding) == defaultDesc.encode(fileencoding)):
                f.write("\tCivDesc=%s\n" %(civInfo.getTextKey().encode(fileencoding)))
            else:
                descKey = findKey(CivDescKeys, civDesc)
                if(descKey):
                    f.write("\tCivDesc=%s\n" %(descKey.encode(fileencoding)))
                else:
                    f.write("\tCivDesc=%s\n" %(civDesc.encode(fileencoding)))

            if(civShortDesc == defaultShortDesc):
                f.write("\tCivShortDesc=%s\n" %(civInfo.getShortDescriptionKey().encode(fileencoding)))
            else:
                shortDescKey = findKey(CivDescKeys, civShortDesc)
                if(shortDescKey):
                    f.write("\tCivShortDesc=%s\n" %(shortDescKey.encode(fileencoding)))
                else:
                    f.write("\tCivShortDesc=%s\n" %(civShortDesc.encode(fileencoding)))

            if(False and civAdjective == defaultAdjective):
                # The required function getCivilizationAdjectiveKey() does not exists!
                f.write("\tCivAdjective=%s\n" %(pPlayer.getCivilizationAdjective(0).encode(fileencoding)))
            else:
                adjectiveKey = findKey(CivAdjectiveKeys, civAdjective)
                if(adjectiveKey):
                    f.write("\tCivAdjective=%s\n" %(adjectiveKey.encode(fileencoding)))
                else:
                    f.write("\tCivAdjective=%s\n" %(civAdjective.encode(fileencoding)))

            f.write("\tFlagDecal=%s\n" %(pPlayer.getFlagDecal().encode(fileencoding)))
            f.write("\tWhiteFlag=%d\n" %(pPlayer.isWhiteFlag(),))
            f.write("\tCivType=%s\n" %(civInfo.getType()))
            f.write("\tColor=%s\n" %(gc.getPlayerColorInfo(pPlayer.getPlayerColor()).getType()))
            f.write("\tArtStyle=%s\n" %(gc.getArtStyleTypes(pPlayer.getArtStyleType())))
            f.write("\tPlayableCiv=%d\n" %(int(pPlayer.isPlayable())))
            f.write("\tMinorNationStatus=%d\n" %(pPlayer.isMinorCiv()))
            f.write("\tStartingGold=%d\n" %(pPlayer.getGold()))

            if pPlayer.isAlive():
                pPlot = pPlayer.getStartingPlot()
                if not pPlot.isNone():
                    f.write("\tStartingX=%d, StartingY=%d\n" %(pPlot.getX(), pPlot.getY()))

            pPlayerReligionInfo = gc.getReligionInfo(pPlayer.getStateReligion())
            if pPlayerReligionInfo:
                f.write("\tStateReligion=%s\n" %(pPlayerReligionInfo.getType()))

            f.write("\tStartingEra=%s\n" %(gc.getEraInfo(pPlayer.getCurrentEra()).getType()))

            f.write("\tRandomStartLocation=false\n")

            # write Civics
            for iCivicOptionLoop in range(gc.getNumCivicOptionInfos()):
                iCivic = pPlayer.getCivics(iCivicOptionLoop)
                f.write("\tCivicOption=%s, Civic=%s\n" %(gc.getCivicOptionInfo(iCivicOptionLoop).getType(), gc.getCivicInfo(iCivic).getType()))

            # write Attitude Extra
            for i in range(gc.getMAX_PLAYERS()):
                if pPlayer.AI_getAttitudeExtra(i) != 0:
                    f.write("\tAttitudePlayer=%d, AttitudeExtra=%d\n" %(i, pPlayer.AI_getAttitudeExtra(i)))

            # write City List
            for i in range(pPlayer.getNumCityNames()):
                f.write("\tCityList=%s\n" %(pPlayer.getCityName(i)))

        if pPlayer.getHandicapType() != HandicapTypes.NO_HANDICAP:
            f.write("\tHandicap=%s\n" %(gc.getHandicapInfo(pPlayer.getHandicapType()).getType()))
        ## Platy Builder ##
            if pPlayer.getGoldenAgeTurns() > 0:
                f.write("\tGoldenAge=%d\n" %(pPlayer.getGoldenAgeTurns()))
            if pPlayer.getAnarchyTurns() > 0:
                f.write("\tAnarchy=%d\n" %(pPlayer.getAnarchyTurns()))
            if pPlayer.getCombatExperience() > 0:
                f.write("\tCombatXP=%d\n" %(pPlayer.getCombatExperience()))
            if pPlayer.getCoastalTradeRoutes() != 0:
                f.write("\tCoastalTradeRoute=%d\n" %(pPlayer.getCoastalTradeRoutes()))
            if pPlayer.getStateReligionUnitProductionModifier() != 0:
                f.write("\tStateReligionUnit=%d\n" %(pPlayer.getStateReligionUnitProductionModifier()))
            if pPlayer.getStateReligionBuildingProductionModifier() != 0:
                f.write("\tStateReligionBuilding=%d\n" %(pPlayer.getStateReligionBuildingProductionModifier()))
            if pPlayer.getScriptData() != "":
                f.write("\tScriptData=%s\n" %(pPlayer.getScriptData()))
        f.write("EndPlayer\n")

    def read(self, f):
        "read in player data"
        self.__init__()
        parser = CvWBParser()
        if (parser.findNextTokenValue(f, "BeginPlayer")!=-1):
            while True:
                nextLine = parser.getNextLine(f)
                toks = parser.getTokens(nextLine)
                if (len(toks) == 0):
                    break

                v = parser.findTokenValue(toks, "CivDesc")
                if v!=-1:
                    try:
                        self.szCivDesc = v.decode(fileencodingOld)
                    except UnicodeDecodeError:
                        self.szCivDesc = v.decode(fileencoding)
                    continue

                v = parser.findTokenValue(toks, "CivShortDesc")
                if v!=-1:
                    try:
                        self.szCivShortDesc = v.decode(fileencoding)
                    except UnicodeDecodeError:
                        self.szCivShortDesc = v.decode(fileencodingOld)
                    continue

                v = parser.findTokenValue(toks, "LeaderName")
                if v!=-1:
                    try:
                        self.szLeaderName = v.decode(fileencoding)
                    except UnicodeDecodeError:
                        self.szLeaderName = v.decode(fileencodingOld)
                    continue

                v = parser.findTokenValue(toks, "CivAdjective")
                if v!=-1:
                    try:
                        self.szCivAdjective = v.decode(fileencoding)
                    except UnicodeDecodeError:
                        self.szCivAdjective = v.decode(fileencodingOld)
                    continue

                v = parser.findTokenValue(toks, "FlagDecal")
                if v!=-1:
                    try:
                        self.szFlagDecal = v.decode(fileencoding)
                    except UnicodeDecodeError:
                        self.szFlagDecal = v.decode(fileencodingOld)
                    continue

                v = parser.findTokenValue(toks, "WhiteFlag")
                if v!=-1:
                    self.isWhiteFlag = int(v)
                    continue

                v = parser.findTokenValue(toks, "LeaderType")
                if v!=-1:
                    self.leaderType = v
                    continue

                v = parser.findTokenValue(toks, "CivType")
                if v!=-1:
                    self.civType = v
                    continue

                v = parser.findTokenValue(toks, "Team")
                if v!=-1:
                    self.team = int(v)
                    continue

                v = parser.findTokenValue(toks, "Handicap")
                if v!=-1:
                    self.handicap = v
                    continue

                v = parser.findTokenValue(toks, "Color")
                if v!=-1:
                    self.color = v
                    continue

                v = parser.findTokenValue(toks, "ArtStyle")
                if v!=-1:
                    self.artStyle = v
                    continue

                v = parser.findTokenValue(toks, "PlayableCiv")
                if v!=-1:
                    self.isPlayableCiv = int(v)
                    continue

                v = parser.findTokenValue(toks, "MinorNationStatus")
                if v!=-1:
                    self.isMinorNationCiv = int(v)
                    continue

                v = parser.findTokenValue(toks, "StartingGold")
                if v!=-1:
                    self.iStartingGold = int(v)
                    continue

                vX = parser.findTokenValue(toks, "StartingX")
                vY = parser.findTokenValue(toks, "StartingY")
                if vX!=-1 and vY!=-1:
                    self.iStartingX = int(vX)
                    self.iStartingY = int(vY)
                    continue

                v = parser.findTokenValue(toks, "StateReligion")
                if v!=-1:
                    self.stateReligion = v
                    continue

                v = parser.findTokenValue(toks, "StartingEra")
                if v!=-1:
                    self.szStartingEra = v
                    continue

                v = parser.findTokenValue(toks, "RandomStartLocation")
                if v!=-1:
                    self.bRandomStartLocation = v
                    # self.bRandomStartLocation = (v in ["true", "True", "TRUE", "1"])
                    continue

                v = parser.findTokenValue(toks, "CivicOption")
                if v!=-1:
                    iCivicOptionType = gc.getInfoTypeForString(v)

                    v = parser.findTokenValue(toks, "Civic")
                    if v!=-1:
                        iCivicType = gc.getInfoTypeForString(v)
                        self.aaiCivics.append([iCivicOptionType,iCivicType])
                        continue

                v = parser.findTokenValue(toks, "AttitudePlayer")
                if v!=-1:
                    iPlayer = int(v)

                    iExtra = int(parser.findTokenValue(toks, "AttitudeExtra"))
                    self.aaiAttitudeExtras.append([iPlayer,iExtra])
                    continue

                v = parser.findTokenValue(toks, "CityList")
                if v!=-1:
                    self.aszCityList.append(v)
                    continue

            ## Platy Builder ##
                v = parser.findTokenValue(toks, "GoldenAge")
                if v!=-1:
                    self.iGoldenAge = max(0, int(v))
                    continue
                v = parser.findTokenValue(toks, "Anarchy")
                if v!=-1:
                    self.iAnarchy = max(0, int(v))
                    continue
                v = parser.findTokenValue(toks, "CombatXP")
                if v!=-1:
                    self.iCombatXP = max(0, int(v))
                    continue
                v = parser.findTokenValue(toks, "CoastalTradeRoute")
                if v!=-1:
                    self.iCoastalTradeRoute = int(v)
                    continue
                v = parser.findTokenValue(toks, "StateReligionUnit")
                if v!=-1:
                    self.iStateReligionUnit = int(v)
                    continue
                v = parser.findTokenValue(toks, "StateReligionBuilding")
                if v!=-1:
                    self.iStateReligionBuilding = int(v)
                    continue
                v = parser.findTokenValue(toks, "ScriptData")
                if v!=-1:
                    self.szScriptData = v
                    continue

                if parser.findTokenValue(toks, "EndPlayer") != -1:
                    break
        else:
            return False
        return True

#############
class CvUnitDesc:
    "unit WB serialization"
    def __init__(self):
        self.plotX = -1
        self.plotY = -1
        self.unitType = None
        self.szName = None
        self.leaderUnitType = None
        self.owner =-1
        self.damage = 0
        self.level = 0
        self.experience = 0
        self.promotionType = []
        self.facingDirection = DirectionTypes.NO_DIRECTION;
        self.isSleep = False
        self.isIntercept = False
        self.isPatrol = False
        self.isPlunder = False
        self.szUnitAIType = "NO_UNITAI"

    ## Platy Builder ##
        self.szScriptData = ""
        self.iImmobile = 0
        self.iBaseCombatStr = -1
        self.iExtraCargo = 0

    def write(self, f, unit, plot):
        "save unit desc to a file"
        Info = gc.getUnitInfo(unit.getUnitType())
        f.write("\tBeginUnit\n")
        # PAE, use BARBARIAN keyword for last id
        unit_owner = unit.getOwner()
        if unit_owner == gc.getMAX_PLAYERS()-1:
            f.write("\t\tUnitType=%s, UnitOwner=BARBARIAN\n" %(Info.getType(),))
        else:
            f.write("\t\tUnitType=%s, UnitOwner=%d\n" %(Info.getType(),unit_owner))
        if (len(unit.getNameNoDesc()) > 0):
            unitName = unit.getNameNoDesc()
            unitDesc = Info.getDescription()
            # Compare unit name with default name of current language
            # and skip name saving if both matching.
            if(unitName != unitDesc):
                f.write("\t\tUnitName=%s\n" %(unitName.encode(fileencoding),))
            else:
                f.write("\t\tUnitDesc=%s\n" %(unitDesc.encode(fileencoding),))
        if unit.getLeaderUnitType() != -1:
            f.write("\t\tLeaderUnitType=%s\n" %(gc.getUnitInfo(unit.getLeaderUnitType()).getType()))
        if unit.getDamage() > 0:
            f.write("\t\tDamage=%d\n" %(unit.getDamage(),))
        f.write("\t\tLevel=%d, Experience=%d\n" %(unit.getLevel(), unit.getExperience()))
        for i in xrange(gc.getNumPromotionInfos()):
            if unit.isHasPromotion(i):
                f.write("\t\tPromotionType=%s\n" %(gc.getPromotionInfo(i).getType()))

        f.write("\t\tFacingDirection=%d\n" %(unit.getFacingDirection(),))
        if (unit.getGroup().getActivityType() == ActivityTypes.ACTIVITY_SLEEP):
            f.write("\t\tSleep\n")
        if (unit.getGroup().getActivityType() == ActivityTypes.ACTIVITY_HOLD):
            f.write("\t\tSleep\n") # Yes, same keyword
        elif (unit.getGroup().getActivityType() == ActivityTypes.ACTIVITY_INTERCEPT):
            f.write("\t\tIntercept\n")
        elif (unit.getGroup().getActivityType() == ActivityTypes.ACTIVITY_PATROL):
            f.write("\t\tPatrol\n")
        elif (unit.getGroup().getActivityType() == ActivityTypes.ACTIVITY_PLUNDER):
            f.write("\t\tPlunder\n")
        f.write("\t\tUnitAIType=%s\n" %(gc.getUnitAIInfo(unit.getUnitAIType()).getType()))
        if unit.getScriptData():
            f.write("\t\tScriptData=%s\n" %unit.getScriptData())

    ## Platy Builder ##
        if unit.getImmobileTimer() > 0:
            f.write("\t\tImmobile=%d\n" %(unit.getImmobileTimer()))
        if unit.baseCombatStr() != Info.getCombat():
            f.write("\t\tCombatStr=%d\n" %(unit.baseCombatStr()))
        if unit.cargoSpace() != Info.getCargoSpace():
            f.write("\t\tExtraCargo=%d\n" %(unit.cargoSpace() - Info.getCargoSpace()))

        f.write("\tEndUnit\n")

    def read(self, f, pX, pY):
        "read in unit data - at this point the first line 'BeginUnit' has already been read"
        self.__init__()
        self.plotX = pX
        self.plotY = pY
        CvUtil.pyAssert(self.plotX >= 0 and self.plotY >= 0, "invalid plot coords")

        parser = CvWBParser()
        while True:
            nextLine = parser.getNextLine(f)
            toks = parser.getTokens(nextLine)
            if (len(toks) == 0):
                break

            v = parser.findTokenValue(toks, "UnitType")
            vOwner = parser.findTokenValue(toks, "UnitOwner")
            if (v!=-1 and vOwner != -1):
                self.unitType = v
                # PAE, use BARBARIAN keyword for last id
                if(vOwner == "BARBARIAN"):
                    self.owner = gc.getMAX_PLAYERS()-1
                else:
                    self.owner = int(vOwner)
                continue

            v = parser.findTokenValue(toks, "UnitName")
            if (v != -1):
                try:
                    self.szName = v.decode(fileencoding)
                except UnicodeDecodeError:
                    self.szName = v.decode(fileencodingOld)
                continue

            v = parser.findTokenValue(toks, "LeaderUnitType")
            if (v != -1):
                self.leaderUnitType = v
                continue

            v = parser.findTokenValue(toks, "Damage")
            if (v != -1):
                self.damage = (int(v))
                continue

            v = parser.findTokenValue(toks, "Level")
            if (v != -1):
                self.level = (int(v))
                self.experience = int(parser.findTokenValue(toks, "Experience"))
                continue

            # Units - Promotions
            v = parser.findTokenValue(toks, "PromotionType")
            if v!=-1:
                self.promotionType.append(v)
                continue

            v = parser.findTokenValue(toks, "FacingDirection")
            if (v != -1):
                self.facingDirection = (DirectionTypes(v))
                continue

            if (parser.findTokenValue(toks, "Sleep"))!=-1:
                self.isSleep = True
                continue

            if (parser.findTokenValue(toks, "Intercept"))!=-1:
                self.isIntercept = True
                continue

            if (parser.findTokenValue(toks, "Patrol"))!=-1:
                self.isPatrol = True
                continue

            if (parser.findTokenValue(toks, "Plunder"))!=-1:
                self.isPlunder = True
                continue

            v = parser.findTokenValue(toks, "UnitAIType")
            if (v != -1):
                self.szUnitAIType = v
                continue

            v = parser.findTokenValue(toks, "ScriptData")
            if v!=-1:
                print("found script data: %s" %(v))
                self.szScriptData = v
                continue
        ## Platy Builder ##
            v = parser.findTokenValue(toks, "Immobile")
            if v != -1:
                self.iImmobile = int(v)
                continue
            v = parser.findTokenValue(toks, "CombatStr")
            if v != -1:
                self.iBaseCombatStr = int(v)
                continue
            v = parser.findTokenValue(toks, "ExtraCargo")
            if v != -1:
                self.iExtraCargo = int(v)
                continue

            if parser.findTokenValue(toks, "EndUnit") != -1:
                break

    def apply(self):
        "after reading, this will actually apply the data"

        player = getPlayer(self.owner)
        if (player):
            # print("unit apply %d %d" %(self.plotX, self.plotY))
            CvUtil.pyAssert(self.plotX >= 0 and self.plotY >= 0, "invalid plot coords")
            unitTypeNum = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), self.unitType)
            if (unitTypeNum < 0):
                unit = None
            else:
                if (self.szUnitAIType != "NO_UNITAI"):
                    eUnitAI = CvUtil.findInfoTypeNum(gc.getUnitAIInfo, UnitAITypes.NUM_UNITAI_TYPES, self.szUnitAIType) #pUnitAI.getType()
                else:
                    eUnitAI = UnitAITypes.NO_UNITAI

                unit = player.initUnit(unitTypeNum, self.plotX, self.plotY, UnitAITypes(eUnitAI), self.facingDirection)
            if unit:
                if (self.szName is not None):
                    unit.setName(self.szName)
                #leader unit type
                if(self.leaderUnitType is not None):
                    leaderUnitTypeNum = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), self.leaderUnitType)
                    if leaderUnitTypeNum >= 0:
                        unit.setLeaderUnitType(leaderUnitTypeNum);

                #other properties
                if self.damage != 0:
                    unit.setDamage(self.damage, PlayerTypes.NO_PLAYER)
                if self.level != -1:
                    unit.setLevel(self.level)
                if self.experience != -1:
                    unit.setExperience(self.experience, -1)
                for promo in self.promotionType:
                    promotionTypeNum = CvUtil.findInfoTypeNum(gc.getPromotionInfo, gc.getNumPromotionInfos(), promo)
                    unit.setHasPromotion(promotionTypeNum, True)
                if self.isSleep:
                    if unit.canFortify(unit.plot()):
                        unit.getGroup().setActivityType(ActivityTypes.ACTIVITY_HOLD)
                    else:
                        unit.getGroup().setActivityType(ActivityTypes.ACTIVITY_SLEEP)
                elif self.isIntercept:
                    unit.getGroup().setActivityType(ActivityTypes.ACTIVITY_INTERCEPT)
                elif self.isPatrol:
                    unit.getGroup().setActivityType(ActivityTypes.ACTIVITY_PATROL)
                elif self.isPlunder:
                    unit.getGroup().setActivityType(ActivityTypes.ACTIVITY_PLUNDER)

            ## Platy Builder ##
                if self.szScriptData != "":
                    unit.setScriptData(self.szScriptData)  # Usage of CvUtil.setScriptData would be wrong!
                unit.setImmobileTimer(self.iImmobile)
                if self.iBaseCombatStr > -1:
                    unit.setBaseCombatStr(self.iBaseCombatStr)
                if self.iExtraCargo != 0:
                    unit.changeCargoSpace(self.iExtraCargo)

############
class CvCityDesc:
    "serializes city data"
    def __init__(self):
        self.city = None
        self.owner = None
        self.name = None
        self.population = 0
        self.productionUnit = "NONE"
        self.productionBuilding = "NONE"
        self.productionProject = "NONE"
        self.productionProcess = "NONE"
        self.bldgType = []
        self.religions = []
        self.holyCityReligions = []
        self.corporations = []
        self.headquarterCorporations = []
        self.freeSpecialists = []
        self.plotX=-1
        self.plotY=-1
    ## Platy Builder ##
        self.szScriptData = ""
        self.lCulture = []
        self.iDamage = 0
        self.iOccupation = 0
        self.iExtraHappiness = 0
        self.iExtraHealth = 0
        self.iExtraTrade = 0
        self.lBuildingYield = []
        self.lBuildingCommerce = []
        self.lBuildingHappy = []
        self.lBuildingHealth = []
        self.lFreeBonus = []
        self.lNoBonus = []

    def write(self, f, plot):
        "write out city data"
        city = plot.getPlotCity()
        CvUtil.pyAssert(city.isNone() == 0, "null city?")
        f.write("\tBeginCity\n")
        # PAE, use BARBARIAN keyword for last id
        city_owner = city.getOwner()
        if city_owner == gc.getMAX_PLAYERS()-1:
            f.write("\t\tCityOwner=BARBARIAN\n")
        else:
            f.write("\t\tCityOwner=%d\n" %(city_owner,))

        cityName = city.getNameKey().encode(fileencoding)
        """
        #Better key lookup. Uncomment it if necessary.
        if cityName[0:7] != "TXT_KEY":
            cityKey = findKey(CityKeys, cityName)
            if(cityKey):
                f.write("\t\tCityName=%s\n" %(cityKey))
            else:
                f.write("\t\tCityName=%s\n" %(cityName))
        """
        f.write("\t\tCityName=%s\n" %(cityName))

        f.write("\t\tCityPopulation=%d\n" %(city.getPopulation(),))
        if (city.isProductionUnit()):
            f.write("\t\tProductionUnit=%s\n" %(gc.getUnitInfo(city.getProductionUnit()).getType(),))
        elif (city.isProductionBuilding()):
            f.write("\t\tProductionBuilding=%s\n" %(gc.getBuildingInfo(city.getProductionBuilding()).getType(),))
        elif (city.isProductionProject()):
            f.write("\t\tProductionProject=%s\n" %(gc.getProjectInfo(city.getProductionProject()).getType(),))
        elif (city.isProductionProcess()):
            f.write("\t\tProductionProcess=%s\n" %(gc.getProcessInfo(city.getProductionProcess()).getType(),))

        global cityBuildings
        iGridH = CyMap().getGridHeight()
        buildings = cityBuildings[ plot.getX()*iGridH + plot.getY() ]
        for iI in buildings:
            f.write("\t\tBuildingType=%s\n" %(gc.getBuildingInfo(iI).getType()))

        for iI in range(gc.getNumReligionInfos()):
            if city.isHasReligion(iI):
                f.write("\t\tReligionType=%s\n" %(gc.getReligionInfo(iI).getType()))
            if (city.isHolyCityByType(iI)):
                f.write("\t\tHolyCityReligionType=%s\n" %(gc.getReligionInfo(iI).getType()))

        for iI in range(gc.getNumCorporationInfos()):
            if city.isHasCorporation(iI):
                f.write("\t\tCorporationType=%s\n" %(gc.getCorporationInfo(iI).getType()))
            if (city.isHeadquartersByType(iI)):
                f.write("\t\tHeadquarterCorporationType=%s\n" %(gc.getCorporationInfo(iI).getType()))

        for iI in range(gc.getNumSpecialistInfos()):
            for iJ in range(city.getAddedFreeSpecialistCount(iI)):
                f.write("\t\tFreeSpecialistType=%s\n" %(gc.getSpecialistInfo(iI).getType()))

        if city.getScriptData():
            f.write("\t\tScriptData=%s\n" %city.getScriptData())

        # Player culture
        for iPlayerLoop in range(gc.getMAX_PLAYERS()):
            iPlayerCulture = city.getCulture(iPlayerLoop)
            if (iPlayerCulture > 0):
                f.write("\t\tPlayer%dCulture=%d\n" %(iPlayerLoop, iPlayerCulture))
        if city.getDefenseDamage() > 0:
            f.write("\t\tDamage=%d\n" %(city.getDefenseDamage(),))
        if city.getOccupationTimer() > 0:
            f.write("\t\tOccupation=%d\n" %(city.getOccupationTimer(),))
        if city.getExtraHappiness() != 0:
            f.write("\t\tExtraHappiness=%d\n" %(city.getExtraHappiness(),))
        if city.getExtraHealth() != 0:
            f.write("\t\tExtraHealth=%d\n" %(city.getExtraHealth(),))
        if city.getExtraTradeRoutes() != 0:
            f.write("\t\tExtraTrade=%d\n" %(city.getExtraTradeRoutes(),))
        for item in xrange(gc.getNumBuildingClassInfos()):
            for k in xrange(YieldTypes.NUM_YIELD_TYPES):
                if city.getBuildingYieldChange(item, k) != 0:
                    f.write("\t\tModifiedBuilding=%s, Yield=%s, Amount=%s\n" %(gc.getBuildingClassInfo(item).getType(), gc.getYieldInfo(k).getType(), city.getBuildingYieldChange(item, k)))
            for k in xrange(CommerceTypes.NUM_COMMERCE_TYPES):
                if city.getBuildingCommerceChange(item, k) != 0:
                    f.write("\t\tModifiedBuilding=%s, Commerce=%s, Amount=%s\n" %(gc.getBuildingClassInfo(item).getType(), gc.getCommerceInfo(k).getType(), city.getBuildingCommerceChange(item, k)))
            if city.getBuildingHappyChange(item) != 0:
                f.write("\t\tModifiedBuilding=%s, Happy=%s\n" %(gc.getBuildingClassInfo(item).getType(), city.getBuildingHappyChange(item)))
            if city.getBuildingHealthChange(item) != 0:
                f.write("\t\tModifiedBuilding=%s, Health=%s\n" %(gc.getBuildingClassInfo(item).getType(), city.getBuildingHealthChange(item)))
        for item in xrange(gc.getNumBonusInfos()):
            if city.getFreeBonus(item) > 0:
                f.write("\t\tFreeBonus=%s, Amount=%s\n" %(gc.getBonusInfo(item).getType(), city.getFreeBonus(item)))
            if city.isNoBonus(item):
                f.write("\t\tNoBonus=%s\n" % gc.getBonusInfo(item).getType())

        f.write("\tEndCity\n")

    def read(self, f, iX, iY):
        "read in city data - at this point the first line 'BeginCity' has already been read"
        self.__init__()
        self.plotX=iX
        self.plotY=iY
        parser = CvWBParser()
        while True:
            nextLine = parser.getNextLine(f)
            toks = parser.getTokens(nextLine)
            if (len(toks) == 0):
                break

            # City - Owner
            vOwner=parser.findTokenValue(toks, "CityOwner")
            if (vOwner != -1):
                # PAE, use BARBARIAN keyword for last id
                if(vOwner == "BARBARIAN"):
                    self.owner = gc.getMAX_PLAYERS()-1
                else:
                    self.owner = int(vOwner)
                continue

            # City - Name
            vName=parser.findTokenValue(toks, "CityName")
            if (vName != -1):
                try:
                    self.name = (vName).decode(fileencoding)
                except UnicodeDecodeError:
                    self.name = (vName).decode(fileencodingOld)
                continue

            # City - Population
            v=parser.findTokenValue(toks, "CityPopulation")
            if v!=-1:
                self.population = (int(v))
                continue

            # City - Production Unit
            v=parser.findTokenValue(toks, "ProductionUnit")
            if v!=-1:
                self.productionUnit = v
                continue

            # City - Production Building
            v=parser.findTokenValue(toks, "ProductionBuilding")
            if v!=-1:
                self.productionBuilding = v
                continue

            # City - Production Project
            v=parser.findTokenValue(toks, "ProductionProject")
            if v!=-1:
                self.productionProject = v
                continue

            # City - Production Process
            v=parser.findTokenValue(toks, "ProductionProcess")
            if v!=-1:
                self.productionProcess = v
                continue

            # City - Buildings
            v=parser.findTokenValue(toks, "BuildingType")
            if v!=-1:
                self.bldgType.append(v)
                continue

            # City - Religions
            v=parser.findTokenValue(toks, "ReligionType")
            if v!=-1:
                self.religions.append(v)
                continue

            # City - HolyCity
            v=parser.findTokenValue(toks, "HolyCityReligionType")
            if v!=-1:
                self.holyCityReligions.append(v)
                continue

            # City - Corporations
            v=parser.findTokenValue(toks, "CorporationType")
            if v!=-1:
                self.corporations.append(v)
                continue

            # City - Headquarters
            v=parser.findTokenValue(toks, "HeadquarterCorporationType")
            if v!=-1:
                self.headquarterCorporations.append(v)
                continue

            # City - Free Specialist
            v=parser.findTokenValue(toks, "FreeSpecialistType")
            if v!=-1:
                self.freeSpecialists.append(v)
                continue

            # City - ScriptData
            v=parser.findTokenValue(toks, "ScriptData")
            if v!=-1:
                self.szScriptData = v
                continue

        ## Platy Builder ##
            for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):
                szCityTag = ("Player%dCulture" %(iPlayerLoop))
                v = parser.findTokenValue(toks, szCityTag)
                if v!=-1:
                    if int(v) > 0:
                        self.lCulture.append([iPlayerLoop, int(v)])
                    continue
            v=parser.findTokenValue(toks, "Damage")
            if v!=-1:
                self.iDamage = int(v)
                continue
            v=parser.findTokenValue(toks, "Occupation")
            if v!=-1:
                self.iOccupation = int(v)
                continue
            v=parser.findTokenValue(toks, "ExtraHappiness")
            if v!=-1:
                self.iExtraHappiness = int(v)
                continue
            v=parser.findTokenValue(toks, "ExtraHealth")
            if v!=-1:
                self.iExtraHealth = int(v)
                continue
            v=parser.findTokenValue(toks, "ExtraTrade")
            if v!=-1:
                self.iExtraTrade = int(v)
                continue
            v = parser.findTokenValue(toks, "ModifiedBuilding")
            if v != -1:
                iBuildingClass = gc.getInfoTypeForString(v)
                v = parser.findTokenValue(toks, "Yield")
                if v != -1:
                    iYield = gc.getInfoTypeForString(v)
                    iAmount = int(parser.findTokenValue(toks, "Amount"))
                    self.lBuildingYield.append([iBuildingClass, iYield, iAmount])
                    continue
                v = parser.findTokenValue(toks, "Commerce")
                if v != -1:
                    iCommerce = gc.getInfoTypeForString(v)
                    iAmount = int(parser.findTokenValue(toks, "Amount"))
                    self.lBuildingCommerce.append([iBuildingClass, iCommerce, iAmount])
                    continue
                v = parser.findTokenValue(toks, "Happy")
                if v != -1:
                    self.lBuildingHappy.append([iBuildingClass, int(v)])
                    continue
                v = parser.findTokenValue(toks, "Health")
                if v != -1:
                    self.lBuildingHealth.append([iBuildingClass, int(v)])
                    continue
            v = parser.findTokenValue(toks, "FreeBonus")
            if v != -1:
                item = gc.getInfoTypeForString(v)
                iAmount = int(parser.findTokenValue(toks, "Amount"))
                self.lFreeBonus.append([item, iAmount])
                continue
            v = parser.findTokenValue(toks, "NoBonus")
            if v != -1:
                self.lNoBonus.append(gc.getInfoTypeForString(v))
                continue

            if parser.findTokenValue(toks, "EndCity")!=-1:
                break

    def apply(self):
        "after reading, this will actually apply the data"

        # PAE adapt player ids in arrays
        self.lCulture = filterPlayerIds2(self.lCulture, barb_idWB)

        player = getPlayer(self.owner)
        if (player):
            try:
                self.city = player.initCity(self.plotX, self.plotY)

                if (self.name is not None):
                    self.city.setName(self.name, False)

                if self.population > -1:
                    self.city.setPopulation(self.population)

                for item in self.lCulture:
                    self.city.setCulture(item[0], item[1], True)

                for bldg in (self.bldgType):
                    bldgTypeNum = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), bldg)
                    self.city.setNumRealBuilding(bldgTypeNum, 1)

                for religion in (self.religions):
                    religionTypeNum = CvUtil.findInfoTypeNum(gc.getReligionInfo, gc.getNumReligionInfos(), religion)
                    self.city.setHasReligion(religionTypeNum, True, False, True)

                for holyCityRel in (self.holyCityReligions):
                    religionTypeNum = CvUtil.findInfoTypeNum(gc.getReligionInfo, gc.getNumReligionInfos(), holyCityRel)
                    gc.getGame().setHolyCity(religionTypeNum, self.city, False)

                for corporation in (self.corporations):
                    corporationTypeNum = CvUtil.findInfoTypeNum(gc.getCorporationInfo, gc.getNumCorporationInfos(), corporation)
                    self.city.setHasCorporation(corporationTypeNum, True, False, True)

                for headquarters in (self.headquarterCorporations):
                    corporationTypeNum = CvUtil.findInfoTypeNum(gc.getCorporationInfo, gc.getNumCorporationInfos(), headquarters)
                    gc.getGame().setHeadquarters(corporationTypeNum, self.city, False)

                for iSpecialist in self.freeSpecialists:
                    specialistTypeNum = CvUtil.findInfoTypeNum(gc.getSpecialistInfo, gc.getNumSpecialistInfos(), iSpecialist)
                    self.city.changeFreeSpecialistCount(specialistTypeNum, 1)

                unitTypeNum = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), self.productionUnit)
                buildingTypeNum = CvUtil.findInfoTypeNum(gc.getBuildingInfo, gc.getNumBuildingInfos(), self.productionBuilding)
                projectTypeNum = CvUtil.findInfoTypeNum(gc.getProjectInfo, gc.getNumProjectInfos(), self.productionProject)
                processTypeNum = CvUtil.findInfoTypeNum(gc.getProcessInfo, gc.getNumProcessInfos(), self.productionProcess)

                if (unitTypeNum != UnitTypes.NO_UNIT):
                    self.city.pushOrder(OrderTypes.ORDER_TRAIN, unitTypeNum, -1, False, False, False, True)
                elif (buildingTypeNum != BuildingTypes.NO_BUILDING):
                    self.city.pushOrder(OrderTypes.ORDER_CONSTRUCT, buildingTypeNum, -1, False, False, False, True)
                elif (projectTypeNum != ProjectTypes.NO_PROJECT):
                    self.city.pushOrder(OrderTypes.ORDER_CREATE, projectTypeNum, -1, False, False, False, True)
                elif (processTypeNum != ProcessTypes.NO_PROCESS):
                    self.city.pushOrder(OrderTypes.ORDER_MAINTAIN, processTypeNum, -1, False, False, False, True)

                if self.szScriptData:
                    self.city.setScriptData(self.szScriptData)  # Usage of CvUtil.setScriptData would be wrong!
            ## Platy Builder ##
                if self.iDamage > 0:
                    self.city.changeDefenseDamage(self.iDamage)
                if self.iOccupation > 0:
                    self.city.setOccupationTimer(self.iOccupation)
                self.city.changeExtraHappiness(self.iExtraHappiness)
                self.city.changeExtraHealth(self.iExtraHealth)
                self.city.changeExtraTradeRoutes(self.iExtraTrade)
                for item in self.lBuildingYield:
                    self.city.setBuildingYieldChange(item[0], item[1], item[2])
                for item in self.lBuildingCommerce:
                    self.city.setBuildingCommerceChange(item[0], item[1], item[2])
                for item in self.lBuildingHappy:
                    self.city.setBuildingHappyChange(item[0], item[1])
                for item in self.lBuildingHealth:
                    self.city.setBuildingHealthChange(item[0], item[1])
                for item in self.lFreeBonus:
                    self.city.changeFreeBonus(item[0], item[1])
                for item in self.lNoBonus:
                    self.city.changeNoBonusCount(item, 1)

            except Exception:
                pass


###########
class CvPlotDesc:
    "serializes plot data"
    def __init__(self):
        self.iX = -1
        self.iY = -1
        self.riverNSDirection = CardinalDirectionTypes.NO_CARDINALDIRECTION
        self.isNOfRiver = 0
        self.riverWEDirection = CardinalDirectionTypes.NO_CARDINALDIRECTION
        self.isWOfRiver = 0
        self.isStartingPlot = 0
        self.bonusType = None
        self.improvementType = None
        self.featureType = None
        self.featureVariety = 0
        self.routeType = None
        self.terrainType = None
        self.plotType = PlotTypes.NO_PLOT
        self.unitDescs = list()
        self.cityDesc = None
        self.szLandmark = ""
    ## Platy Builder ##
        self.szScriptData = ""
        self.abTeamPlotRevealed = []
        self.lCulture = []

    def needToWritePlot(self, plot):
        "returns True if this plot needs to be written out."
        return True

    def preApply(self):
        "apply plot and terrain type"
        plot = CyMap().plot(self.iX, self.iY)
        if (self.plotType != PlotTypes.NO_PLOT):
            plot.setPlotType(self.plotType, False, False)
        if (self.terrainType):
            terrainTypeNum = CvUtil.findInfoTypeNum(gc.getTerrainInfo, gc.getNumTerrainInfos(), self.terrainType)
            plot.setTerrainType(terrainTypeNum, False, False)

    def write(self, f, plot):
        "save plot desc to a file"
        f.write("BeginPlot\n")
        f.write("\tx=%d,y=%d\n" %(plot.getX(), plot.getY()))

        # scriptData
        if (plot.getScriptData() != ""):
            f.write("\tScriptData=%s\n" %plot.getScriptData())
        # rivers
        if (plot.getRiverNSDirection() != CardinalDirectionTypes.NO_CARDINALDIRECTION):
            f.write("\tRiverNSDirection=%d\n" %(int(plot.getRiverNSDirection()),))
        if (plot.isNOfRiver()):
            f.write("\tisNOfRiver\n")
        if (plot.getRiverWEDirection() != CardinalDirectionTypes.NO_CARDINALDIRECTION):
            f.write("\tRiverWEDirection=%d\n" %(int(plot.getRiverWEDirection()),))
        if (plot.isWOfRiver()):
            f.write("\tisWOfRiver\n")
        # extras
        if (plot.isStartingPlot()):
            f.write("\tStartingPlot\n")
        if (plot.getBonusType(-1)!=-1):
            f.write("\tBonusType=%s\n" %(gc.getBonusInfo(plot.getBonusType(-1)).getType()))
        if (plot.getImprovementType()!=-1):
            f.write("\tImprovementType=%s\n" %(gc.getImprovementInfo(plot.getImprovementType()).getType()))
        if (plot.getFeatureType()!=-1):
            f.write("\tFeatureType=%s, FeatureVariety=%d\n"
            %(gc.getFeatureInfo(plot.getFeatureType()).getType(), plot.getFeatureVariety(),))
        if (plot.getRouteType()!=-1):
            f.write("\tRouteType=%s\n" %(gc.getRouteInfo(plot.getRouteType()).getType()))
        if (plot.getTerrainType()!=-1):
            f.write("\tTerrainType=%s\n" %(gc.getTerrainInfo(plot.getTerrainType()).getType()))
        if (plot.getPlotType()!=PlotTypes.NO_PLOT):
            f.write("\tPlotType=%d\n" %(int(plot.getPlotType()),))

        # units
        for i in range(plot.getNumUnits()):
            unit=plot.getUnit(i)
            if unit.getUnitType() == -1:
                continue
            CvUnitDesc().write(f, unit, plot)
        # city
        if (plot.isCity()):
            CvCityDesc().write(f, plot)

        # Fog of War
        bFirstReveal=True
        for iTeamLoop in range(gc.getMAX_TEAMS()):
            if gc.getTeam(iTeamLoop).isAlive():
                if plot.isRevealed(iTeamLoop,0):
                    # Plot is revealed for this Team so write out the fact that it is; if not revealed don't write anything
                    if bFirstReveal:
                        f.write("\tTeamReveal=")
                        bFirstReveal=False
                    f.write("%d," %(iTeamLoop))
        if bFirstReveal == False:
            f.write("\n") # terminate reveal line
    ## Platy Builder ##
        for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):
            iPlayerCulture = plot.getCulture(iPlayerLoop)
            if iPlayerCulture > 0:
                f.write("\tPlayer%dCulture=%d\n" %(iPlayerLoop, iPlayerCulture))

        f.write("EndPlot\n")

    def read(self, f):
        "read in a plot desc"
        self.__init__()
        parser = CvWBParser()
        if parser.findNextToken(f, "BeginPlot") == False:
            return False  # no more plots
        while (True):
            nextLine = parser.getNextLine(f)
            toks = parser.getTokens(nextLine)
            if (len(toks) == 0):
                break

            x = parser.findTokenValue(toks, "x")
            y = parser.findTokenValue(toks, "y")
            if (x!=-1 and y!=-1):
                self.iX = int(x)
                self.iY = int(y)
                # print("plot read %d %d" %(self.iX, self.iY))
                continue

            v = parser.findTokenValue(toks, "Landmark")
            if v!=-1:
                self.szLandmark=v
                continue

            v = parser.findTokenValue(toks, "ScriptData")
            if v!=-1:
                self.szScriptData=v
                continue

            v = parser.findTokenValue(toks, "RiverNSDirection")
            if v!=-1:
                self.riverNSDirection = (CardinalDirectionTypes(v))
                continue

            if (parser.findTokenValue(toks, "isNOfRiver"))!=-1:
                self.isNOfRiver = (True)
                continue

            v = parser.findTokenValue(toks, "RiverWEDirection")
            if v!=-1:
                self.riverWEDirection = (CardinalDirectionTypes(v))
                continue

            if (parser.findTokenValue(toks, "isWOfRiver"))!=-1:
                self.isWOfRiver = (True)
                continue

            if (parser.findTokenValue(toks, "StartingPlot"))!=-1:
                self.isStartingPlot = (True)
                continue

            v = parser.findTokenValue(toks, "BonusType")
            if v!=-1:
                self.bonusType = v
                continue

            v = parser.findTokenValue(toks, "ImprovementType")
            if v!=-1:
                self.improvementType = v
                continue

            v = parser.findTokenValue(toks, "FeatureType")
            if v!=-1:
                self.featureType = v
                v = parser.findTokenValue(toks, "FeatureVariety")
                if v!=-1:
                    self.featureVariety = int(v)
                continue

            v = parser.findTokenValue(toks, "RouteType")
            if v!=-1:
                self.routeType = v
                continue

            v = parser.findTokenValue(toks, "TerrainType")
            if v!=-1:
                self.terrainType = v
                continue

            v = parser.findTokenValue(toks, "PlotType")
            if v!=-1:
                self.plotType = PlotTypes(v)
                continue

            # Units
            v = parser.findTokenValue(toks, "BeginUnit")
            if v!=-1:
                unitDesc = CvUnitDesc()
                unitDesc.read(f, self.iX, self.iY)
                if unitDesc.owner <= NUM_CIV_PLAYERS:
                    self.unitDescs.append(unitDesc)
                continue

            # City
            v = parser.findTokenValue(toks, "BeginCity")
            if v!=-1:
                self.cityDesc = CvCityDesc()
                self.cityDesc.read(f, self.iX, self.iY)
                if self.cityDesc.owner > NUM_CIV_PLAYERS:
                    self.cityDesc = None
                continue

            # Fog of War

            v = parser.findTokenValue(toks, "TeamReveal")
            if v!=-1:
                for iTeamLoop in toks:
                    iTeamLoop = iTeamLoop.lstrip('TeamReveal=')
                    if len(iTeamLoop):
                        self.abTeamPlotRevealed.append(int(iTeamLoop))
                continue

            if parser.findTokenValue(toks, "EndPlot")!=-1:
                break

        ## Platy Builder ##
            for iPlayerLoop in xrange(gc.getMAX_PLAYERS()):
                szCityTag = ("Player%dCulture" %(iPlayerLoop))
                v = parser.findTokenValue(toks, szCityTag)
                if v!=-1:
                    if int(v) > 0:
                        self.lCulture.append([iPlayerLoop, int(v)])
                    continue
        return True

    def apply(self):
        "after reading, this will actually apply the data"

        # PAE, adapt player ids in arrays
        # Note: Platy uses this arrays at an external position. Filtering was moved, too.
        #self.abTeamPlotRevealed = filterPlayerIds(self.abTeamPlotRevealed, barb_idWB)
        #self.lCulture = filterPlayerIds2(self.lCulture, barb_idWB)

        #print("apply plot %d %d" %(self.iX, self.iY))
        plot = CyMap().plot(self.iX, self.iY)
        plot.setNOfRiver(self.isNOfRiver, self.riverWEDirection)
        plot.setWOfRiver(self.isWOfRiver, self.riverNSDirection)
        plot.setStartingPlot(self.isStartingPlot)
        if (self.bonusType):
            bonusTypeNum = CvUtil.findInfoTypeNum(gc.getBonusInfo, gc.getNumBonusInfos(), self.bonusType)
            plot.setBonusType(bonusTypeNum)
        if (self.improvementType):
            improvementTypeNum = CvUtil.findInfoTypeNum(gc.getImprovementInfo, gc.getNumImprovementInfos(), self.improvementType)
            plot.setImprovementType(improvementTypeNum)
        if (self.featureType):
            featureTypeNum = CvUtil.findInfoTypeNum(gc.getFeatureInfo, gc.getNumFeatureInfos(), self.featureType)
            plot.setFeatureType(featureTypeNum, self.featureVariety)
        if (self.routeType):
            routeTypeNum = CvUtil.findInfoTypeNum(gc.getRouteInfo, gc.getNumRouteInfos(), self.routeType)
            plot.setRouteType(routeTypeNum)

        if (self.szLandmark != ""):
            CyEngine().addLandmark(CyMap().plot(self.iX, self.iY), "%s" %(self.szLandmark))

        if (self.szScriptData != ""):
            plot.setScriptData(self.szScriptData)  # Usage of CvUtil.setScriptData would be wrong!

    def applyUnits(self):
        #print("--apply units")
        for u in self.unitDescs:
            u.apply()

    def applyCity(self):
        if self.cityDesc:
            #print("--apply city")
            self.cityDesc.apply()

################
class CvMapDesc:
    "serialize map data"
    def __init__(self):
        self.iGridW = 0
        self.iGridH = 0
        self.iTopLatitude = 0
        self.iBottomLatitude = 0
        self.bWrapX = 0
        self.bWrapY = 0
        self.worldSize = None
        self.climate = None
        self.seaLevel = None
        self.numPlotsWritten = 0
        self.numSignsWritten = 0
        self.bRandomizeResources = "false"

    def write(self, f):
        "write map data"
        map = CyMap()
        iGridW = map.getGridWidth()
        iGridH = map.getGridHeight()
        iNumPlots = iGridW * iGridH
        iNumSigns = CyEngine().getNumSigns()

        f.write("BeginMap\n")
        f.write("\tgrid width=%d\n" %(map.getGridWidth(),))
        f.write("\tgrid height=%d\n" %(map.getGridHeight(),))
        f.write("\ttop latitude=%d\n" %(map.getTopLatitude(),))
        f.write("\tbottom latitude=%d\n" %(map.getBottomLatitude(),))
        f.write("\twrap X=%d\n" %(map.isWrapX(),))
        f.write("\twrap Y=%d\n" %(map.isWrapY(),))
        f.write("\tworld size=%s\n" %(gc.getWorldInfo(map.getWorldSize()).getType(),))
        f.write("\tclimate=%s\n" %(gc.getClimateInfo(map.getClimate()).getType(),))
        f.write("\tsealevel=%s\n" %(gc.getSeaLevelInfo(map.getSeaLevel()).getType(),))
        f.write("\tnum plots written=%d\n" %(iNumPlots,))
        f.write("\tnum signs written=%d\n" %(iNumSigns,))
        f.write("\tRandomize Resources=false\n")
        f.write("EndMap\n")

    def read(self, f):
        "read map data"
        self.__init__()
        parser = CvWBParser()
        if parser.findNextToken(f, "BeginMap") == False:
            print("can't find map")
            return
        while (True):
            nextLine = parser.getNextLine(f)
            toks = parser.getTokens(nextLine)
            if (len(toks) == 0):
                break

            v = parser.findTokenValue(toks, "grid width")
            if v!=-1:
                self.iGridW = int(v)
                continue

            v = parser.findTokenValue(toks, "grid height")
            if v!=-1:
                self.iGridH = int(v)
                continue

            v = parser.findTokenValue(toks, "top latitude")
            if v!=-1:
                self.iTopLatitude = int(v)
                continue

            v = parser.findTokenValue(toks, "bottom latitude")
            if v!=-1:
                self.iBottomLatitude = int(v)
                continue

            v = parser.findTokenValue(toks, "wrap X")
            if v!=-1:
                self.bWrapX = int(v)
                continue

            v = parser.findTokenValue(toks, "wrap Y")
            if v!=-1:
                self.bWrapY = int(v)
                continue

            v = parser.findTokenValue(toks, "world size")
            if v!=-1:
                self.worldSize = v
                continue

            v = parser.findTokenValue(toks, "climate")
            if v!=-1:
                self.climate = v
                continue

            v = parser.findTokenValue(toks, "sealevel")
            if v!=-1:
                self.seaLevel = v
                continue

            v = parser.findTokenValue(toks, "num plots written")
            if v!=-1:
                self.numPlotsWritten = int(v)
                continue

            v = parser.findTokenValue(toks, "num signs written")
            if v!=-1:
                self.numSignsWritten = int(v)
                continue

            v = parser.findTokenValue(toks, "Randomize Resources")
            if v!=-1:
                self.bRandomizeResources = v
                continue

            if parser.findTokenValue(toks, "EndMap")!=-1:
                break

################
class CvSignDesc:
    "serialize map data"
    def __init__(self):
        self.iPlotX = 0
        self.iPlotY = 0
        self.playerType = 0
        self.szCaption = ""

    def apply(self):
        # PAE, ignore signs for unused ids
        if self.playerType > NUM_CIV_PLAYERS:
            return
        plot = CyMap().plot(self.iPlotX, self.iPlotY)
        CyEngine().addSign(plot, self.playerType, self.szCaption)

    def write(self, f, sign):
        "write sign data"
        f.write("BeginSign\n")
        f.write("\tplotX=%d\n" %(sign.getPlot().getX(),))
        f.write("\tplotY=%d\n" %(sign.getPlot().getY(),))
        f.write("\tplayerType=%d\n" %(sign.getPlayerType(),))
        f.write("\tcaption=%s\n" %(sign.getCaption().encode('utf-8'),))
        f.write("EndSign\n")

    def read(self, f):
        "read sign data"
        self.__init__()
        parser = CvWBParser()
        if parser.findNextToken(f, "BeginSign") == False:
            print("can't find sign")
            return
        while (True):
            nextLine = parser.getNextLine(f)
            toks = parser.getTokens(nextLine)
            if (len(toks) == 0):
                break

            v = parser.findTokenValue(toks, "plotX")
            if v!=-1:
                self.iPlotX = int(v)
                continue

            v = parser.findTokenValue(toks, "plotY")
            if v!=-1:
                self.iPlotY = int(v)
                continue

            v = parser.findTokenValue(toks, "playerType")
            if v!=-1:
                self.playerType = int(v)
                continue

            v = parser.findTokenValue(toks, "caption")
            if v!=-1:
                self.szCaption = v.decode('utf-8').encode('cp1252')
                continue

            if parser.findTokenValue(toks, "EndSign")!=-1:
                break

        return True

class CvWBDesc:
    "handles saving/loading a worldbuilder description file"
    def __init__(self):
        # game data
        self.gameDesc = CvGameDesc()
        self.playersDesc = None
        self.plotDesc = None  # list
        self.signDesc = None  # list
        self.mapDesc = CvMapDesc()

    def getVersion(self):
        return version

    def getDescFileName(self, fileName):
        return fileName+getWBSaveExtension()

    def write(self, fileName):
        "Save out a high-level desc of the world, and height/terrainmaps"
        fileName = os.path.normpath(fileName)
        fileName,ext = os.path.splitext(fileName)
        CvUtil.pyPrint('saveDesc:%s, curDir:%s' %(fileName,os.getcwd()))

        f = file(self.getDescFileName(fileName), "w")   # open text file
    ## Platy Builder ##
        f.write("%s\n" %("Platy Builder"))
    ## Platy Builder ##
        f.write("Version=%d\n" %(self.getVersion(),))
        self.gameDesc.write(f)  # write game info

        """ Prelude:
        Backup Techs and Buildings. This is required to distinct between
        bonues which are given by techs/buildings and other sources.
        The techs/buildings will be restored after the writing of the save game.
        This should not call any Python-Events (bad side effect).
        """
        if WITH_PLATY:
            backup_bPython =  CvPlatyBuilderScreen.bPython
            CvPlatyBuilderScreen.bPython = False

        global teamTechs
        global cityBuildings
        global bFirstWrite
        teamTechs = []
        cityBuildings = []
        for i in range(gc.getMAX_TEAMS()):
            pTeam = gc.getTeam(i)
            techs = []
            for i in range(gc.getNumTechInfos()):
                if pTeam.isHasTech(i):
                    techs.append(i)
                    if not bFirstWrite:
                        pTeam.setHasTech(i, False, PlayerTypes.NO_PLAYER, False, False)
            teamTechs.append(techs)

        iGridW = CyMap().getGridWidth()
        iGridH = CyMap().getGridHeight()
        for iX in range(iGridW):
            for iY in range(iGridH):
                plot = CyMap().plot(iX, iY)
                if (plot.isCity()):
                    city = plot.getPlotCity()
                    buildings = []
                    for iI in range(gc.getNumBuildingInfos()):
                        if city.getNumRealBuilding(iI) > 0:
                            if not bFirstWrite:
                                city.setNumRealBuilding(iI, 0)
                            buildings.append(iI)
                    cityBuildings.append(buildings)
                else:
                    cityBuildings.append(None)
        """ End of Prelude """

        for i in range(gc.getMAX_TEAMS()):
            CvTeamDesc().write(f, i)    # write team info

        for i in range(gc.getMAX_PLAYERS()):
            CvPlayerDesc().write(f, i)    # write player info

        self.mapDesc.write(f) # write map info

        f.write("\n### Plot Info ###\n")
        iGridW = CyMap().getGridWidth()
        iGridH = CyMap().getGridHeight()
        for iX in range(iGridW):
            for iY in range(iGridH):
                plot = CyMap().plot(iX, iY)
                pDesc = CvPlotDesc()
                if pDesc.needToWritePlot(plot):
                    pDesc.write(f, plot)

        f.write("\n### Sign Info ###\n")
        iNumSigns = CyEngine().getNumSigns()
        for i in range(iNumSigns):
            sign = CyEngine().getSignByIndex(i)
            pDesc = CvSignDesc()
            pDesc.write(f, sign)

        f.close()

        """ Restore buildings and techs """
        if not bFirstWrite:
            iGridW = CyMap().getGridWidth()
            iGridH = CyMap().getGridHeight()
            for iX in range(iGridW):
                for iY in range(iGridH):
                    plot = CyMap().plot(iX, iY)
                    if (plot.isCity()):
                        city = plot.getPlotCity()
                        buildings = cityBuildings[ iX*iGridH + iY ]
                        if buildings is None:
                            continue
                        for iI in buildings:
                            city.setNumRealBuilding(iI, 1)

            for i in range(gc.getMAX_TEAMS()):
                pTeam = gc.getTeam(i)
                techs = teamTechs[i]
                for i in techs:
                    pTeam.setHasTech(i, True, PlayerTypes.NO_PLAYER, False, False)
        else:
            bFirstWrite = False;

        if WITH_PLATY:
            CvPlatyBuilderScreen.bPython = backup_bPython
        """ End, Restore buildings and techs """

        print("WBSave done\n")
        return 0  # success

    def applyMap(self):
        "after reading setup the map"

        self.gameDesc.apply()

        # recreate map
        print("map rebuild. gridw=%d, gridh=%d" %(self.mapDesc.iGridW, self.mapDesc.iGridH))
        worldSizeType = CvUtil.findInfoTypeNum(gc.getWorldInfo, gc.getNumWorldInfos(), self.mapDesc.worldSize)
        climateType = CvUtil.findInfoTypeNum(gc.getClimateInfo, gc.getNumClimateInfos(), self.mapDesc.climate)
        seaLevelType = CvUtil.findInfoTypeNum(gc.getSeaLevelInfo, gc.getNumSeaLevelInfos(), self.mapDesc.seaLevel)
        CyMap().rebuild(self.mapDesc.iGridW, self.mapDesc.iGridH, self.mapDesc.iTopLatitude, self.mapDesc.iBottomLatitude, self.mapDesc.bWrapX, self.mapDesc.bWrapY, WorldSizeTypes(worldSizeType), ClimateTypes(climateType), SeaLevelTypes(seaLevelType), 0, None)

        print("preapply plots")
        for pDesc in self.plotDesc:
            pDesc.preApply()  # set plot type / terrain type

        print("map apply - recalc areas/regions")
        CyMap().recalculateAreas()

        print("apply plots")
        for pDesc in self.plotDesc:
            pDesc.apply()

        print("apply signs")
        for pDesc in self.signDesc:
            pDesc.apply()

        print("Randomize Resources")
        if (self.mapDesc.bRandomizeResources != "false"):
            for iPlotLoop in range(CyMap().numPlots()):
                pPlot = CyMap().plotByIndex(iPlotLoop)
                pPlot.setBonusType(BonusTypes.NO_BONUS)
            CyMapGenerator().addBonuses()

        print("WB apply done\n")
        return 0  # ok

## Platy Builder ##
    def getAssignedStartingPlots(self):
        for iPlayerLoop in xrange(len(self.playersDesc)):

            pPlayer = gc.getPlayer(iPlayerLoop)
            pWBPlayer = self.playersDesc[iPlayerLoop]

            # Random Start Location
            if (pPlayer.getLeaderType() != -1 and pWBPlayer.bRandomStartLocation != "false"):
                pPlayer.setStartingPlot(pPlayer.findStartingPlot(True), True)

            else:

                # Player's starting plot
                if ((pWBPlayer.iStartingX != -1) and (pWBPlayer.iStartingY != -1)):
                    pPlayer.setStartingPlot(CyMap().plot(pWBPlayer.iStartingX, pWBPlayer.iStartingY), True)

        return 0  # ok

    def applyInitialItems(self):
        for iTeamLoop in xrange(len(self.teamsDesc)):
            pTeam = gc.getTeam(iTeamLoop)
            pWBTeam = self.teamsDesc[iTeamLoop]

            # PAE, adapt player ids in arrays
            pWBTeam.aaiEspionageAgainstTeams = filterPlayerIds2(pWBTeam.aaiEspionageAgainstTeams, barb_idWB)
            pWBTeam.bContactWithTeamList = filterPlayerIds(pWBTeam.bContactWithTeamList, barb_idWB)
            pWBTeam.bWarWithTeamList = filterPlayerIds(pWBTeam.bWarWithTeamList, barb_idWB)
            pWBTeam.bPermanentWarPeaceList = filterPlayerIds(pWBTeam.bPermanentWarPeaceList, barb_idWB)
            pWBTeam.bOpenBordersWithTeamList = filterPlayerIds(pWBTeam.bOpenBordersWithTeamList, barb_idWB)
            pWBTeam.bDefensivePactWithTeamList = filterPlayerIds(pWBTeam.bDefensivePactWithTeamList, barb_idWB)
            pWBTeam.bVassalOfTeamList = filterPlayerIds(pWBTeam.bVassalOfTeamList, barb_idWB)

            for techTypeTag in pWBTeam.techTypes:
                techType = CvUtil.findInfoTypeNum(gc.getTechInfo, gc.getNumTechInfos(), techTypeTag)
                pTeam.setHasTech(techType, True, PlayerTypes.NO_PLAYER, False, False)
            for item in pWBTeam.aaiEspionageAgainstTeams:
                pTeam.setEspionagePointsAgainstTeam(item[0], item[1])
            for item in pWBTeam.bContactWithTeamList:
                pTeam.meet(item, False)
            for item in pWBTeam.bWarWithTeamList:
                pTeam.declareWar(item, False, WarPlanTypes.NO_WARPLAN)
            for item in pWBTeam.bPermanentWarPeaceList:
                pTeam.setPermanentWarPeace(item, True)
            for item in pWBTeam.bOpenBordersWithTeamList:
                pTeam.signOpenBorders(item)
            for item in pWBTeam.bDefensivePactWithTeamList:
                pTeam.signDefensivePact(item)
            for item in pWBTeam.bVassalOfTeamList:
                #pTeam.assignVassal(item, True)
                pTeam.setVassal(item, True, True)
            for project in pWBTeam.projectType:
                projectTypeNum = CvUtil.findInfoTypeNum(gc.getProjectInfo, gc.getNumProjectInfos(), project)
                pTeam.changeProjectCount(projectTypeNum, 1)
                projectCount = pTeam.getProjectCount(projectTypeNum)
                pTeam.setProjectArtType(projectTypeNum, projectCount - 1, 0)

        ## Platy Builder ##
            pTeam.setMapCentering(pWBTeam.bMapCentering)
            pTeam.changeMapTradingCount(pWBTeam.bMapTrading)
            pTeam.changeTechTradingCount(pWBTeam.bTechTrading)
            pTeam.changeGoldTradingCount(pWBTeam.bGoldTrading)
            pTeam.changeOpenBordersTradingCount(pWBTeam.bOpenBordersTrading)
            pTeam.changeDefensivePactTradingCount(pWBTeam.bDefensivePactTrading)
            pTeam.changePermanentAllianceTradingCount(pWBTeam.bPermanentAllianceTrading)
            pTeam.changeVassalTradingCount(pWBTeam.bVassalStateTrading)
            pTeam.changeBridgeBuildingCount(pWBTeam.bBridgeBuilding)
            pTeam.changeIrrigationCount(pWBTeam.bIrrigation)
            pTeam.changeIgnoreIrrigationCount(pWBTeam.bIgnoreIrrigation)
            pTeam.changeWaterWorkCount(pWBTeam.bWaterWork)
            pTeam.changeNukeInterception(pWBTeam.iNukeInterception)
            pTeam.changeEnemyWarWearinessModifier(pWBTeam.iEnemyWarWeariness)
            for item in pWBTeam.lDomainMoves:
                pTeam.changeExtraMoves(item[0], item[1])
            for item in pWBTeam.lRouteMoves:
                pTeam.changeRouteChange(item[0], item[1])
            for item in pWBTeam.lImprovementYield:
                pTeam.changeImprovementYieldChange(item[0], item[1], item[2])

    ## Platy Builder ##
        for iPlayerLoop in xrange(len(self.playersDesc)):
            pPlayer = gc.getPlayer(iPlayerLoop)
            pWBPlayer = self.playersDesc[iPlayerLoop]

            pWBPlayer.aaiAttitudeExtras = filterPlayerIds2(pWBPlayer.aaiAttitudeExtras, barb_idWB)

            pPlayer.setGold(pWBPlayer.iStartingGold)
            if ((pWBPlayer.iStartingX != -1) and (pWBPlayer.iStartingY != -1)):
                pPlayer.setStartingPlot(CyMap().plot(pWBPlayer.iStartingX, pWBPlayer.iStartingY), True)

            if (pWBPlayer.stateReligion != ""):
                iStateReligionID = gc.getInfoTypeForString(pWBPlayer.stateReligion)
                pPlayer.setLastStateReligion(iStateReligionID)

            if (pWBPlayer.szStartingEra != ""):
                iStartingEra = gc.getInfoTypeForString(pWBPlayer.szStartingEra)
                pPlayer.setCurrentEra(iStartingEra)

            if (pWBPlayer.bRandomStartLocation != "false"):
                pPlayer.setStartingPlot(pPlayer.findStartingPlot(True), True)
                print("Setting player %d starting location to (%d,%d)", pPlayer.getID(), pPlayer.getStartingPlot().getX(), pPlayer.getStartingPlot().getY())

            for item in pWBPlayer.aaiCivics:
                pPlayer.setCivics(item[0],item[1])
            for item in pWBPlayer.aaiAttitudeExtras:
                pPlayer.AI_setAttitudeExtra(item[0],item[1])
            for item in pWBPlayer.aszCityList:
                pPlayer.addCityName(item)

        ## Platy Builder ##
            pPlayer.changeGoldenAgeTurns(pWBPlayer.iGoldenAge)
            pPlayer.changeAnarchyTurns(pWBPlayer.iAnarchy)
            pPlayer.setCombatExperience(pWBPlayer.iCombatXP)
            pPlayer.changeCoastalTradeRoutes(pWBPlayer.iCoastalTradeRoute)
            #pPlayer.changeStateReligionUnitProductionModifier(pWBPlayer.iStateReligionUnit)
            #pPlayer.changeStateReligionBuildingProductionModifier(pWBPlayer.iStateReligionBuilding)
            pPlayer.setScriptData(pWBPlayer.szScriptData)  # Usage of CvUtil.setScriptData would be wrong!

        # cities
        for pDesc in self.plotDesc:
            pDesc.applyCity()

        for iTeamLoop in xrange(len(self.teamsDesc)):
            pTeam = gc.getTeam(iTeamLoop)
            pWBTeam = self.teamsDesc[iTeamLoop]
            if pWBTeam.bRevealMap:
                CyMap().setRevealedPlots(iTeamLoop, True, False)
            if pWBTeam.iVassalPower > 0:
                pTeam.setVassalPower(pWBTeam.iVassalPower)
            if pWBTeam.iMasterPower > 0:
                pTeam.setMasterPower(pWBTeam.iMasterPower)
            if pWBTeam.iEspionageEver > 0:
                pTeam.setEspionagePointsEver(pWBTeam.iEspionageEver)

    ## Platy Builder ##
        for iPlotLoop in range(self.mapDesc.numPlotsWritten):
            pWBPlot = self.plotDesc[iPlotLoop]
            pWBPlot.lCulture = filterPlayerIds2(pWBPlot.lCulture, barb_idWB)

            pPlot = CyMap().plot(pWBPlot.iX, pWBPlot.iY)
            for item in pWBPlot.lCulture:
                pPlot.setCulture(item[0], item[1], True)

        for iPlotLoop in range(self.mapDesc.numPlotsWritten):
            pWBPlot = self.plotDesc[iPlotLoop]
            pWBPlot.abTeamPlotRevealed = filterPlayerIds(pWBPlot.abTeamPlotRevealed, barb_idWB)
            for iTeamLoop in pWBPlot.abTeamPlotRevealed:
                pPlot = CyMap().plot(pWBPlot.iX, pWBPlot.iY)
                pPlot.setRevealed(iTeamLoop, True, False, TeamTypes.NO_TEAM)

        # units
        for pDesc in self.plotDesc:
            pDesc.applyUnits()

        return 0  # ok

    def read(self, fileName):
        "Load in a high-level desc of the world, and height/terrainmaps"
        fileName = os.path.normpath(fileName)
        fileName,ext=os.path.splitext(fileName)
        if len(ext) == 0:
            ext = getWBSaveExtension()
        CvUtil.pyPrint('loadDesc:%s, curDir:%s' %(fileName,os.getcwd()))

        if (not os.path.isfile(fileName+ext)):
            CvUtil.pyPrint("Error: file %s does not exist" %(fileName+ext,))
            return -1 # failed

        f=file(fileName+ext, "r")   # open text file

        global barb_idWB
        ## Platy Builder ##
        parser = CvWBParser()
        filePos = f.tell()
        #iNumPlayersDLL = gc.getMAX_CIV_PLAYERS()
        #iNumTeamsDLL = gc.getMAX_CIV_TEAMS()
        line = parser.getNextLine(f)
        if line.find("Platy") > -1:
            # WBSave stores barbarian player/team, too.
            iNumPlayersDLL = gc.getMAX_PLAYERS()
            iNumTeamsDLL = gc.getMAX_TEAMS()
        else:
            iNumPlayersDLL = gc.getMAX_PLAYERS()
            iNumTeamsDLL = gc.getMAX_TEAMS()
            f.seek(filePos)

        version = int(parser.findNextTokenValue(f, "Version"))
        if (version != self.getVersion()):
            CvUtil.pyPrint("Error: wrong WorldBuilder save version.  Expected %d, got %d" %(self.getVersion(), version))
            return -1 # failed

        print("Reading game desc")
        self.gameDesc.read(f) # read game info

        print("Reading teams desc")
        filePos = f.tell()
        self.teamsDesc = []
        numTeamsWB = 0
        for i in range(iNumTeamsDLL):
            teamDesc = CvTeamDesc()
            if (teamDesc.read(f) == False):         # read team info
                f.seek(filePos)               # abort and backup
                break
            print("reading team %d" %(i))
            self.teamsDesc.append(teamDesc)
            numTeamsWB += 1

        # PAE, Extend to 52 entries regardless if they will be used
        if numTeamsWB < iNumTeamsDLL:
            for i in range(numTeamsWB, iNumTeamsDLL):
                teamDesc = CvTeamDesc()
                print("append team %d" %(i))
                self.teamsDesc.append(teamDesc)


        print("Reading players desc")
        self.playersDesc = []
        numPlayersWB = 0
        for i in range(iNumPlayersDLL):
            filePos = f.tell()
            playerDesc = CvPlayerDesc()
            # read player info
            if playerDesc.read(f) == False: # Not all entries filled
                f.seek(filePos)               # abort and backup
                break;

            print("reading player %d" %(i))
            self.playersDesc.append(playerDesc)
            numPlayersWB += 1
            if playerDesc.leaderType == "LEADER_BARBARIAN":
                barb_idWB = numPlayersWB - 1

        # PAE; If the WB save was written with the 52er DLL the Barbarian entry is != 18, but 52.
        # Shift it forward on position 18.
        # Possible Trap: This could be problematic if some trades, etc with the original player of slot 18 was made.
        barbarianDesc = None
        while True:
            filePos = f.tell()
            playerDesc = CvPlayerDesc()
            if playerDesc.read(f):
                print("reading EXTRA player %d" %(i))
                numPlayersWB += 1
                if playerDesc.leaderType == "LEADER_BARBARIAN":
                    barbarianDesc = playerDesc
                    barb_idWB = numPlayersWB - 1
                continue

            # Last player slot was already passed. Abort and move up
            f.seek(filePos)
            break

        # PAE Expand to 52 entries if extended DLL is used
        if numPlayersWB < iNumPlayersDLL:
            for i in range(numPlayersWB, iNumPlayersDLL):
                print("append player %d" %(i))
                playerDesc = CvPlayerDesc()
                #playerDesc.team = i
                #playerDesc.bRandomStartLocation = True
                #playerDesc.isPlayableCiv = 0 # 1 is default
                self.playersDesc.append(playerDesc)


            if (len(self.playersDesc) >= numPlayersWB and
                    self.playersDesc[numPlayersWB-1].leaderType == "LEADER_BARBARIAN"):
                # Clear AtWar and Contact fields of barbarian
                # TODO: Stimmt der Index auch bei Verkleinerung?
                # print("Shift barb player at index %d to %d" %(numPlayersWB-1, iNumPlayersDLL-1))
                barb_idWB = numPlayersWB - 1
                """
                iBarbTeamWB = self.playersDesc[numPlayersWB-1].team
                self.teamsDesc[iNumPlayersDLL-1] = self.teamsDesc[iBarbTeamWB]
                self.teamsDesc[iBarbTeamWB] = CvTeamDesc()
                self.playersDesc[iNumPlayersDLL-1] = self.playersDesc[barb_idWB]
                self.playersDesc[barb_idWB] = CvPlayerDesc()
                """

        print("Debug status:")
        print("   numPlayersWB: %d" %(numPlayersWB))
        print("   iNumPlayersDLL: %d" %(iNumPlayersDLL))
        print("   barb_idWB: %s" %(str(barb_idWB)))
        #init_filter()

        # PAE, Szenario with many players loaded without DLL.
        if barbarianDesc is not None:
            print("Shift barbarian player to lower id...")
            self.playersDesc[iNumPlayersDLL - 1] = barbarianDesc
            # iBarbTeamWB = barbarianDesc.team
            # self.teamsDesc[iBarbTeamWB] = CvTeamDesc()

        # PAE, if player 18 is Barbarian, swap this slot with player 52.
        # We assume here that non-barb teams has no 'AtWar' and 'ContactWithTeam' entries for barbarian teams.
        if barb_idWB is not None:
            if numPlayersWB < iNumPlayersDLL and self.playersDesc[barb_idWB].leaderType == "LEADER_BARBARIAN":
                if self.playersDesc[iNumPlayersDLL-1].leaderType == "LEADER_BARBARIAN" or True:
                    # Two barbarian entries, remove first
                    print("Remove barbarian player at slot %d" %(barb_idWB))
                    barbTeam = self.playersDesc[barb_idWB].team
                    self.teamsDesc[barbTeam] = CvTeamDesc()
                    newPlayerDesc = CvPlayerDesc()
                    newPlayerDesc.team = barbTeam
                    self.playersDesc[barb_idWB] = newPlayerDesc
                else:
                    # Swap barb to from position 18 to 52
                    print("Shift barbarian player from slot %d to %d" %(barb_idWB, iNumPlayersDLL-1))
                    barbTeam = self.playersDesc[barb_idWB].team
                    self.teamsDesc[barbTeam], self.teamsDesc[iNumTeamsDLL-1] = self.teamsDesc[iNumTeamsDLL-1], self.teamsDesc[barbTeam]
                    self.playersDesc[barb_idWB].team = iNumTeamsDLL-1
                    #       self.playersDesc[iNumPlayersDLL-1].team = barbTeam
                    self.playersDesc[barb_idWB], self.playersDesc[iNumPlayersDLL-1] = self.playersDesc[iNumPlayersDLL-1], self.playersDesc[18]

            else:
                # Set barbarian slot manually ?!
                pass


        print("Reading map desc")
        self.mapDesc.read(f)  # read map info

        print("Reading/creating %d plot descs" %(self.mapDesc.numPlotsWritten,))
        self.plotDesc = []
        for i in range(self.mapDesc.numPlotsWritten):
            pDesc = CvPlotDesc()
            if pDesc.read(f):
                self.plotDesc.append(pDesc)
            else:
                break

        print("Reading/creating %d sign descs" %(self.mapDesc.numSignsWritten,))
        self.signDesc = []
        for i in range(self.mapDesc.numSignsWritten):
            pDesc = CvSignDesc()
            if pDesc.read(f):
                self.signDesc.append(pDesc)
            else:
                break

        f.close()
        print("WB read done\n")
        return 0
