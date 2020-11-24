#include "CvGameCoreDLL.h"
#include "CyGame.h"
#include "CvRandom.h"
#include "CyCity.h"
#include "CyDeal.h"
#include "CyReplayInfo.h"

//
// published python interface for CyGame
// 

void CyGamePythonInterface()
{
	OutputDebugString("Python Extension Module - CyGamePythonInterface\n");

	python::class_<CyGame>("CyGame")
		.def("isNone", &CyGame::isNone, "CyGame* () - is the instance valid?")

		.def("updateScore", &CyGame::updateScore, "void (bool bForce)")
		.def("cycleCities", &CyGame::cycleCities, "void (bool bForward, bool bAdd)")
		.def("cycleSelectionGroups", &CyGame::cycleSelectionGroups, "void (bool bClear, bool bForward, bool bWorkers)")
		.def("cyclePlotUnits", &CyGame::cyclePlotUnits, "bool (CyPlot* pPlot, bool bForward, bool bAuto, int iCount)")

		.def("selectionListMove", &CyGame::selectionListMove, "void (CyPlot* pPlot, bool bAlt, bool bShift, bool bCtrl)")
		.def("selectionListGameNetMessage", &CyGame::selectionListGameNetMessage, "void (int eMessage, int iData2, int iData3, int iData4, int iFlags, bool bAlt, bool bShift)")
		.def("selectedCitiesGameNetMessage", &CyGame::selectedCitiesGameNetMessage, "void (int eMessage, int iData2, int iData3, int iData4, bool bOption, bool bAlt, bool bShift, bool bCtrl)")
		.def("cityPushOrder", &CyGame::cityPushOrder, "void (CyCity* pCity, OrderTypes eOrder, int iData, bool bAlt, bool bShift, bool bCtrl)")

		.def("getSymbolID", &CyGame::getSymbolID, "int (int iSymbol)")

		.def("getProductionPerPopulation", &CyGame::getProductionPerPopulation, "int (int (HurryTypes) eHurry)")

		.def("getAdjustedPopulationPercent", &CyGame::getAdjustedPopulationPercent, "int (int (VictoryTypes) eVictory)")
		.def("getAdjustedLandPercent", &CyGame::getAdjustedLandPercent, "int (int ( VictoryTypes) eVictory)")

		.def("isTeamVote", &CyGame::isTeamVote, "bool (int (VoteTypes) eVote)")
		.def("isChooseElection", &CyGame::isChooseElection, "bool (int (VoteTypes) eVote)")
		.def("isTeamVoteEligible", &CyGame::isTeamVoteEligible, "bool (int (TeamTypes) eTeam, int (VoteSourceTypes) eVoteSource)")
		.def("countPossibleVote", &CyGame::countPossibleVote, "int (int (VoteTypes) eVote, int (VoteSourceTypes) eVoteSource)")
		.def("getVoteRequired", &CyGame::getVoteRequired, "int (int (VoteTypes) eVote, int (VoteSourceTypes) eVoteSource)")
		.def("getSecretaryGeneral", &CyGame::getSecretaryGeneral, "int (int (VoteSourceTypes) eVoteSource)")
		.def("canHaveSecretaryGeneral", &CyGame::canHaveSecretaryGeneral, "bool (int (VoteSourceTypes) eVoteSource)")
		.def("getVoteSourceReligion", &CyGame::getVoteSourceReligion, "int (int (VoteSourceTypes) eVoteSource)")
		.def("setVoteSourceReligion", &CyGame::setVoteSourceReligion, "void (int (VoteSourceTypes) eVoteSource, int (ReligionTypes) eReligion, bool bAnnounce)")

		.def("countCivPlayersAlive", &CyGame::countCivPlayersAlive, "int ()")
		.def("countCivPlayersEverAlive", &CyGame::countCivPlayersEverAlive, "int ()")
		.def("countCivTeamsAlive", &CyGame::countCivTeamsAlive, "int ()")
		.def("countCivTeamsEverAlive", &CyGame::countCivTeamsEverAlive, "int ()")
		.def("countHumanPlayersAlive", &CyGame::countHumanPlayersAlive, "int ()")

		.def("countTotalCivPower", &CyGame::countTotalCivPower, "int ()")
		.def("countTotalNukeUnits", &CyGame::countTotalNukeUnits, "int ()")
		.def("countKnownTechNumTeams", &CyGame::countKnownTechNumTeams, "int (int (TechTypes) eTech)")
		.def("getNumFreeBonuses", &CyGame::getNumFreeBonuses, "int (int (BuildingTypes) eBuilding)")

		.def("countReligionLevels", &CyGame::countReligionLevels, "int (int (ReligionTypes) eReligion)")
		.def("calculateReligionPercent", &CyGame::calculateReligionPercent, "int (int (ReligionTypes) eReligion)")
		.def("countCorporationLevels", &CyGame::countCorporationLevels, "int (int (CorporationTypes) eCorporation)")

		.def("goldenAgeLength", &CyGame::goldenAgeLength, "int ()")
		.def("victoryDelay", &CyGame::victoryDelay, "int (int iVictory)")
		.def("getImprovementUpgradeTime", &CyGame::getImprovementUpgradeTime, "int (int (ImprovementTypes) eImprovement)")
		.def("canTrainNukes", &CyGame::canTrainNukes, "bool ()")

		.def("getCurrentEra", &CyGame::getCurrentEra, "int ()")

		.def("getActiveTeam", &CyGame::getActiveTeam, "int () - returns ID for the group")
		.def("getActiveCivilizationType", &CyGame::getActiveCivilizationType, "int () - returns CivilizationID")
		.def("isNetworkMultiPlayer", &CyGame::isNetworkMultiPlayer, "bool () - NetworkMultiplayer()? ")
		.def("isGameMultiPlayer", &CyGame::isGameMultiPlayer, "bool () - GameMultiplayer()? ")
		.def("isTeamGame", &CyGame::isTeamGame, "bool ()")
		.def("getNumHumanPlayers", &CyGame::getNumHumanPlayers, "int () - # of human players in-game")

		.def("isModem", &CyGame::isModem, "bool () - Using a modem? ")
		.def("setModem", &CyGame::setModem, "void (bool bModem) - Use a modem! (or don't)")

		.def("reviveActivePlayer", &CyGame::reviveActivePlayer, "void ()")

		.def("getGameTurn", &CyGame::getGameTurn, "int () - current game turn")
		.def("setGameTurn", &CyGame::setGameTurn, "void (int iNewValue) - set current game turn")
		.def("getTurnYear", &CyGame::getTurnYear, "int (int iGameTurn) - turn Time")
		.def("getGameTurnYear", &CyGame::getGameTurnYear, "int ()")
		.def("getElapsedGameTurns", &CyGame::getElapsedGameTurns, "int () - Elapsed turns thus far")
		.def("getMaxTurns", &CyGame::getMaxTurns, "int ()")
		.def("setMaxTurns", &CyGame::setMaxTurns, "void (int iNewValue)")
		.def("changeMaxTurns", &CyGame::changeMaxTurns, "void (int iChange)")
		.def("getMaxCityElimination", &CyGame::getMaxCityElimination, "int ()")
		.def("setMaxCityElimination", &CyGame::setMaxCityElimination, "void (int iNewValue)")
		.def("getNumAdvancedStartPoints", &CyGame::getNumAdvancedStartPoints, "int ()")
		.def("setNumAdvancedStartPoints", &CyGame::setNumAdvancedStartPoints, "void (int iNewValue)")
		.def("getStartTurn", &CyGame::getStartTurn, "int () - Returns the starting Turn (0 unless a scenario or advanced era start)")
		.def("getStartYear", &CyGame::getStartYear, "int () - Returns the starting year (e.g. -4000)")
		.def("setStartYear", &CyGame::setStartYear, "void (int iNewValue) - Sets the starting year (e.g. -4000)")
		.def("getEstimateEndTurn", &CyGame::getEstimateEndTurn, "int ()")
		.def("setEstimateEndTurn", &CyGame::setEstimateEndTurn, "void (int iNewValue)")
		.def("getTurnSlice", &CyGame::getTurnSlice, "int ()")
		.def("incrementTurnTimer", &CyGame::incrementTurnTimer, "void (int iNumTurnSlices)")
		.def("getMinutesPlayed", &CyGame::getMinutesPlayed, "int ()")
		.def("getTargetScore", &CyGame::getTargetScore, "int ()")
		.def("setTargetScore", &CyGame::setTargetScore, "void (int iNewValue)")

		.def("getNumGameTurnActive", &CyGame::getNumGameTurnActive, "int ()")
		.def("countNumHumanGameTurnActive", &CyGame::countNumHumanGameTurnActive, "int ()")
		.def("getNumCities", &CyGame::getNumCities, "int () - total cities in Game")
		.def("getNumCivCities", &CyGame::getNumCivCities, "int () - total non-barbarian cities in Game")
		.def("getTotalPopulation", &CyGame::getTotalPopulation, "int () - total game population")

		.def("getTradeRoutes", &CyGame::getTradeRoutes, "int ()")
		.def("changeTradeRoutes", &CyGame::changeTradeRoutes, "void (int iChange)")
		.def("getFreeTradeCount", &CyGame::getFreeTradeCount, "int ()")
		.def("isFreeTrade", &CyGame::isFreeTrade, "bool ()")
		.def("changeFreeTradeCount", &CyGame::changeFreeTradeCount, "void (int iChange)")
		.def("getNoNukesCount", &CyGame::getNoNukesCount, "int ()")
		.def("isNoNukes", &CyGame::isNoNukes, "bool ()")
		.def("changeNoNukesCount", &CyGame::changeNoNukesCount, "void (int iChange)")
		.def("getSecretaryGeneralTimer", &CyGame::getSecretaryGeneralTimer, "int (int iVoteSource)")
		.def("getVoteTimer", &CyGame::getVoteTimer, "int (int iVoteSource)")
		.def("getNukesExploded", &CyGame::getNukesExploded, "int ()")
		.def("changeNukesExploded", &CyGame::changeNukesExploded, "void (int iChange)")

		.def("getMaxPopulation", &CyGame::getMaxPopulation, "int ()")
		.def("getMaxLand", &CyGame::getMaxLand, "int ()")
		.def("getMaxTech", &CyGame::getMaxTech, "int ()")
		.def("getMaxWonders", &CyGame::getMaxWonders, "int ()")
		.def("getInitPopulation", &CyGame::getInitPopulation, "int ()")
		.def("getInitLand", &CyGame::getInitLand, "int ()")
		.def("getInitTech", &CyGame::getInitTech, "int ()")
		.def("getInitWonders", &CyGame::getInitWonders, "int ()")

		.def("getAIAutoPlay", &CyGame::getAIAutoPlay, "int ()")
		.def("setAIAutoPlay", &CyGame::setAIAutoPlay, "void (int iNewValue)")

		.def("isScoreDirty", &CyGame::isScoreDirty, "bool ()")
		.def("setScoreDirty", &CyGame::setScoreDirty, "void (bool bNewValue)")
		.def("isCircumnavigated", &CyGame::isCircumnavigated, "bool () - is the globe circumnavigated?")
		.def("makeCircumnavigated", &CyGame::makeCircumnavigated, "void ()")
		.def("isDiploVote", &CyGame::isDiploVote, "bool (int (VoteSourceTypes) eVoteSource)")
		.def("changeDiploVote", &CyGame::changeDiploVote, "void (int (VoteSourceTypes) eVoteSource, int iChange)")
		.def("isDebugMode", &CyGame::isDebugMode, "bool () - is the game in Debug Mode?")
		.def("toggleDebugMode", &CyGame::toggleDebugMode, "void ()")

		.def("getPitbossTurnTime", &CyGame::getPitbossTurnTime, "int ()")
		.def("setPitbossTurnTime", &CyGame::setPitbossTurnTime, "void (int iHours)")
		.def("isHotSeat", &CyGame::isHotSeat, "bool ()")
		.def("isPbem", &CyGame::isPbem, "bool ()")
		.def("isPitboss", &CyGame::isPitboss, "bool ()")
		.def("isPitbossShortNames", &CyGame::isPitbossShortNames, "bool ()")
		.def("setPitbossShortNames", &CyGame::setPitbossShortNames, "void (bool bShort, int maxLenName, int maxLenDesc)")
		.def("isSimultaneousTeamTurns", &CyGame::isSimultaneousTeamTurns, "bool ()")

		.def("isFinalInitialized", &CyGame::isFinalInitialized, "bool () - Returns whether or not the game initialization process has ended (game has started)")

		.def("getActivePlayer", &CyGame::getActivePlayer, "int (PlayerTypes*/ ()")
		.def("setActivePlayer", &CyGame::setActivePlayer, "void (int (PlayerTypes) eNewValue, bool bForceHotSeat)")
		.def("getPausePlayer", &CyGame::getPausePlayer, "int () - will get who paused us")
		.def("setPausePlayer", &CyGame::setPausePlayer, "void (int (PlayerTypes) eNewValue)")
		.def("isPaused", &CyGame::isPaused, "bool () - will say if the game is paused")
		.def("getBestLandUnit", &CyGame::getBestLandUnit, "int (PlayerTypes*/ ()")
		.def("getBestLandUnitCombat", &CyGame::getBestLandUnitCombat, "int ()")

		.def("getWinner", &CyGame::getWinner, "int (TeamTypes*/ ()")
		.def("getVictory", &CyGame::getVictory, "int (VictoryTypes*/ ()")
		.def("setWinner", &CyGame::setWinner, "void (int (TeamTypes) eNewWinner, int (VictoryTypes) eNewVictory)")
		.def("getGameState", &CyGame::getGameState, "int (GameStateTypes*/ ()")
		.def("getHandicapType", &CyGame::getHandicapType, "int ( HandicapTypes */ () - difficulty level settings")
		.def("getCalendar", &CyGame::getCalendar, "CalendarTypes ()")
		.def("getStartEra", &CyGame::getStartEra, "int (EraTypes*/ ()")
		.def("getGameSpeedType", &CyGame::getGameSpeedType, "int (GameSpeedTypes*/ ()")
		.def("getRankPlayer", &CyGame::getRankPlayer, "int (PlayerTypes*/ (int iRank)")
		.def("getPlayerRank", &CyGame::getPlayerRank, "int (int (PlayerTypes) ePlayer)")
		.def("getPlayerScore", &CyGame::getPlayerScore, "int (int (PlayerTypes) ePlayer)")
		.def("getRankTeam", &CyGame::getRankTeam, "int (TeamTypes*/ (int iRank)")
		.def("getTeamRank", &CyGame::getTeamRank, "int (int (TeamTypes) eTeam)")
		.def("getTeamScore", &CyGame::getTeamScore, "int (int (TeamTypes) eTeam)")
		.def("isOption", &CyGame::isOption, "bool (int (GameOptionTypes) eIndex) - returns whether Game Option is valid")
		.def("setOption", &CyGame::setOption, "void (int (GameOptionTypes) eIndex, bool bEnabled) - sets a Game Option")
		.def("isMPOption", &CyGame::isMPOption, "bool (int (MultiplayerOptionTypes) eIndex) - returns whether MP Option is valid")
		.def("setMPOption", &CyGame::setMPOption, "void (int (MultiplayerOptionTypes) eIndex, bool enabled) - sets  MP Option during running game on Pitboss host")
		.def("isForcedControl", &CyGame::isForcedControl, "bool (int (ForceControlTypes) eIndex) - returns whether Control should be forced")
		.def("getUnitCreatedCount", &CyGame::getUnitCreatedCount, "int (int (UnitTypes) eIndex) - returns number of this unit type created (?)")
		.def("getUnitClassCreatedCount", &CyGame::getUnitClassCreatedCount, "int (int (UnitClassTypes) eIndex) - returns number of this unit class type created (?)")
		.def("isUnitClassMaxedOut", &CyGame::isUnitClassMaxedOut, "bool (int (UnitClassTypes) eIndex, int iExtra) - returns whether or not this unit class is maxed out (e.g. spies)")
		.def("getBuildingClassCreatedCount", &CyGame::getBuildingClassCreatedCount, "int (int (BuildingClassTypes) eIndex) - building Class count")
		.def("isBuildingClassMaxedOut", &CyGame::isBuildingClassMaxedOut, "bool (int (BuildingClassTypes) eIndex, int iExtra) - max # reached?")

		.def("getProjectCreatedCount", &CyGame::getProjectCreatedCount, "int (int (ProjectTypes) eIndex)")
		.def("isProjectMaxedOut", &CyGame::isProjectMaxedOut, "bool (int (ProjectTypes) eIndex, int iExtra)")

		.def("getForceCivicCount", &CyGame::getForceCivicCount, "int (int (CivicTypes) eIndex)")
		.def("isForceCivic", &CyGame::isForceCivic, "bool (int (CivicTypes) eIndex)")
		.def("isForceCivicOption", &CyGame::isForceCivicOption, "bool (int (CivicOptionTypes) eCivicOption)")

		.def("getVoteOutcome", &CyGame::getVoteOutcome, "int (int (VoteTypes) eIndex)")

		.def("getReligionGameTurnFounded", &CyGame::getReligionGameTurnFounded, "int (int (ReligionTypes) eIndex)")
		.def("isReligionFounded", &CyGame::isReligionFounded, "bool (int (ReligionTypes) eIndex) - is religion founded?")
		.def("isReligionSlotTaken", &CyGame::isReligionSlotTaken, "bool (int (ReligionTypes) eIndex) - is religion in that tech slot founded?")
		.def("getCorporationGameTurnFounded", &CyGame::getCorporationGameTurnFounded, "int (int (CorporationTypes) eIndex)")
		.def("isCorporationFounded", &CyGame::isCorporationFounded, "bool (int (CorporationTypes) eIndex) - is corporation founded?")
		.def("isVictoryValid", &CyGame::isVictoryValid, "bool (int (VictoryTypes) eIndex)")
		.def("isVotePassed", &CyGame::isVotePassed, "bool (int (VoteTypes) eIndex)")
		.def("isSpecialUnitValid", &CyGame::isSpecialUnitValid, "bool (int (SpecialUnitTypes) eSpecialUnitType)")
		.def("makeSpecialUnitValid", &CyGame::makeSpecialUnitValid, "void (int (SpecialUnitTypes) eSpecialUnitType)")

		.def("isSpecialBuildingValid", &CyGame::isSpecialBuildingValid, "bool (int (SpecialBuildingTypes) eIndex)")
		.def("makeSpecialBuildingValid", &CyGame::makeSpecialBuildingValid, "void (int (SpecialBuildingTypes) eIndex)")

		.def("isNukesValid", &CyGame::isNukesValid, "bool ()")
		.def("makeNukesValid", &CyGame::makeNukesValid, "void (bool bValid)")

		.def("isInAdvancedStart", &CyGame::isInAdvancedStart, "bool ()")

		.def("getHolyCity", &CyGame::getHolyCity, python::return_value_policy<python::manage_new_object>(), "CyCity* (int (ReligionTypes) eIndex)")
		.def("setHolyCity", &CyGame::setHolyCity, "void (int (ReligionTypes) eIndex, CyCity* pNewValue, bool bAnnounce) - Sets holy city for religion eIndex to pNewValue")
		.def("clearHolyCity", &CyGame::clearHolyCity, "void (int (ReligionTypes) eIndex) - clears the holy city for religion eIndex")

		.def("getHeadquarters", &CyGame::getHeadquarters, python::return_value_policy<python::manage_new_object>(), "CyCity* (int (CorporationTypes) eIndex)")
		.def("setHeadquarters", &CyGame::setHeadquarters, "void (int (CorporationTypes) eIndex, CyCity* pNewValue, bool bAnnounce) - Sets headquarters for corporation eIndex to pNewValue")
		.def("clearHeadquarters", &CyGame::clearHeadquarters, "void (int (CorporationTypes) eIndex) - clears the headquarters for corporation eIndex")

		.def("getPlayerVote", &CyGame::getPlayerVote, "int (int (PlayerTypes) eOwnerIndex, int iVoteId)")

		.def("getScriptData", &CyGame::getScriptData, "string getScriptData() - Returns ScriptData member (used to store custom data)")
		.def("setScriptData", &CyGame::setScriptData, "void (string szNewValue) - Sets ScriptData member (used to store custom data)")

		.def("setName", &CyGame::setName, "void (TCHAR* szNewValue)")
		.def("getName", &CyGame::getName, "wstring ()")
		.def("getIndexAfterLastDeal", &CyGame::getIndexAfterLastDeal, "int ()")
		.def("getNumDeals", &CyGame::getNumDeals, "int ()")
		.def("getDeal", &CyGame::getDeal, python::return_value_policy<python::manage_new_object> (), "CyDeal* (int iID)")
		.def("addDeal", &CyGame::addDeal, python::return_value_policy<python::manage_new_object> (), "CyDeal* ()")
		.def("getMapRand", &CyGame::getMapRand, python::return_value_policy<python::reference_existing_object>(), "CvRandom ()")
		.def("getMapRandNum", &CyGame::getMapRandNum, "int (int iNum, TCHAR* pszLog)")
		.def("getSorenRand", &CyGame::getSorenRand, python::return_value_policy<python::reference_existing_object>(), "CvRandom ()")
		.def("getSorenRandNum", &CyGame::getSorenRandNum, "int (int iNum, TCHAR* pszLog)")
		.def("calculateSyncChecksum", &CyGame::calculateSyncChecksum, "int ()")
		.def("calculateOptionsChecksum", &CyGame::calculateOptionsChecksum, "int ()")

		.def("GetWorldBuilderMode", &CyGame::GetWorldBuilderMode, "bool ()")
		.def("isPitbossHost", &CyGame::isPitbossHost, "bool ()")
		.def("getCurrentLanguage", &CyGame::getCurrentLanguage, "int ()")
		.def("setCurrentLanguage", &CyGame::setCurrentLanguage, "void (int iNewLanguage)")

		.def("getReplayMessageTurn", &CyGame::getReplayMessageTurn, "int (int i)")
		.def("getReplayMessageType", &CyGame::getReplayMessageType, "ReplayMessageTypes (int i)")
		.def("getReplayMessagePlotX", &CyGame::getReplayMessagePlotX, "int (int i)")
		.def("getReplayMessagePlotY", &CyGame::getReplayMessagePlotY, "int (int i)")
		.def("getReplayMessagePlayer", &CyGame::getReplayMessagePlayer, "int (int i)")
		.def("getReplayMessageColor", &CyGame::getReplayMessageColor, "ColorTypes (int i)")
		.def("getReplayMessageText", &CyGame::getReplayMessageText, "wstring getReplayMessageText(int i) (int i)")
		.def("getNumReplayMessages", &CyGame::getNumReplayMessages, "uint ()")
		.def("getReplayInfo", &CyGame::getReplayInfo, python::return_value_policy<python::manage_new_object> (), "CyReplayInfo* ()")

		.def("hasSkippedSaveChecksum", &CyGame::hasSkippedSaveChecksum, "bool ()")
		.def("saveReplay", &CyGame::saveReplay, "void (int iPlayer)")
		.def("addPlayer", &CyGame::addPlayer, "void (int eNewPlayer, int eLeader, int eCiv)")
		.def("getCultureThreshold", &CyGame::getCultureThreshold, "int (int eLevel)")

		.def("setPlotExtraYield", &CyGame::setPlotExtraYield, "void (int iX, int iY, int (YieldTypes) eYield, int iExtraYield)")
		.def("changePlotExtraCost", &CyGame::changePlotExtraCost, "void (int iX, int iY, int iCost)")

		.def("isCivEverActive", &CyGame::isCivEverActive, "bool (int (CivilizationTypes) eCivilization)")
		.def("isLeaderEverActive", &CyGame::isLeaderEverActive, "bool (int (LeaderHeadTypes) eLeader)")
		.def("isUnitEverActive", &CyGame::isUnitEverActive, "bool (int (UnitTypes) eUnit)")
		.def("isBuildingEverActive", &CyGame::isBuildingEverActive, "bool (int (BuildingTypes) eBuilding)")

		.def("isEventActive", &CyGame::isEventActive, "bool (int (EventTriggerTypes) eTrigger)")
		.def("doControl", &CyGame::doControl, "void (int iControl)")
		.def("setCivPassword", &CyGame::setCivPassword, "int (int ePlayer, const char *szNewPw, const char *szAdminPw) - Allows change of passwords over webinterface")
		.def("isDiploScreenUp", &CyGame::isDiploScreenUp, "bool ()")
		.def("doControlWithoutWidget", &CyGame::doControlWithoutWidget, "void ()")
		.def("sendTurnCompletePB", &CyGame::sendTurnCompletePB, "void (int iPlayer)")
		.def("getModPath", &CyGame::getModPath, "wstring getModPath() - Return absolute path to folder of used CvGameCoreDLL.dll.")
		.def("unzipModUpdate", &CyGame::unzipModUpdate, "int (wstring zipFilename) - Unzip file into the Mod installation folder.")
		.def("delayedPythonCall", &CyGame::delayedPythonCall, "int (int milliseconds, int arg1, int arg2) - Call function delayed (unblocked).")
		.def("setAdminPassword", &CyGame::setAdminPassword, "int (const char *szNewPw, const char *szAdminPw) - Allows change of admin password over webinterface")
		.def("fixTradeRoutes", &CyGame::fixTradeRoutes, "void (void) - Re-evauate used cities in trade routes.")
		.def("getCorporationFactor100", &CyGame::getCorporationFactor100_, "int (int numCorpLocationsOfPlayer, int numPlayersWithCorp, int (CorporationTypes) eCorporation) - Percent modifier for corporation yield in relation to its distribution.")
		;

	python::class_<CyDeal>("CyDeal")
		.def("isNone", &CyDeal::isNone, "bool ()")
		.def("getID", &CyDeal::getID, "int ()")
		.def("getInitialGameTurn", &CyDeal::getInitialGameTurn, "int ()")
		.def("getFirstPlayer", &CyDeal::getFirstPlayer, "int ()")
		.def("getSecondPlayer", &CyDeal::getSecondPlayer, "int ()")
		.def("getLengthFirstTrades", &CyDeal::getLengthFirstTrades, "int ()")
		.def("getLengthSecondTrades", &CyDeal::getLengthSecondTrades, "int ()")
		.def("getFirstTrade", &CyDeal::getFirstTrade, python::return_value_policy<python::reference_existing_object>(), "TradeData* (int i)")
		.def("getSecondTrade", &CyDeal::getSecondTrade, python::return_value_policy<python::reference_existing_object>(), "TradeData* (int i)")
		.def("kill", &CyDeal::kill, "void ()")
		;
}
