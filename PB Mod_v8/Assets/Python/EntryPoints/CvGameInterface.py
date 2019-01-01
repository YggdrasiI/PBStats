## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## #####   WARNING - MODIFYING THE FUNCTION NAMES OF THIS FILE IS PROHIBITED  #####
## 
## The app specifically calls the functions as they are named. Use this file to pass 
## args to another file that contains your modifications
##
## MODDERS - If you create a GameUtils file, update the CvGameInterfaceFile reference to point to your new file

#
import CvUtil
import CvGameUtils
import CvGameInterfaceFile
import CvEventInterface
from CvPythonExtensions import *

# novice:
# Added imports for getGameStateString:
import string
import time
from PyHelpers import PyGame, PyPlayer

# globals
gc = CyGlobalContext()
normalGameUtils = CvGameInterfaceFile.GameUtils

# novice: Added entry point getGameStateString to be called from the C++ code.
def getGameStateString(argslist):
	try:
		#print("Dumping game state...")
		religionCount = 7
		buildingCount = 159
		promotionTypeCount = 54
		specialistTypeCount = 14
		technologyCount = gc.getNumTechInfos()
		cyMap = CyMap()
		cyGame = CyGame()
		pyGame = PyGame()
		#testvar = 123/0
		plots = []
		players = []
		#print(".Dumping player state...")
		for p in pyGame.getCivPlayerList():
			team = p.getTeam()
			pp = p.getPlayer()
			contacts = []
			#print("..Dumping player " + str(p.getID()) + " contacts...")
			for op in range(gc.getMAX_CIV_PLAYERS()):
				if pp.canContact(op):
					contacts.append(op)
			#print("..Dumping player " + str(p.getID()) + " techs...")
			techProgress = []
			for t in range(technologyCount-1):
				techProgress.append(team.getResearchProgress(t))
			cities = []
			#print("..Dumping player " + str(p.getID()) + " cities...")
			for c in p.getCityList():
				cc = c.GetCy()
				buildings = []
				buildQueue = []
				religions = []
				holyCities = []
				freeSpecialists = []
				specialists = []
				for s in range(specialistTypeCount-1):
					for i in range(cc.getAddedFreeSpecialistCount(s)):
						freeSpecialists.append(s)
					for i in range(cc.getSpecialistCount(s)):
						specialists.append(s)
				for r in range(religionCount-1):
					if(cc.isHasReligion(r)):
						religions.append(r)
					if(cc.isHolyCityByType(r)):
						holyCities.append(r)
				for b in range(buildingCount-1):
					if cc.getNumBuilding(b) > 0:
						buildings.append(b)
				for q in range(cc.getOrderQueueLength()):
					order = cc.getOrderFromQueue(q)
					buildQueue.append({"save": order.bSave, "type": int(order.eOrderType), "data1": order.iData1, "data2": order.iData2})
				cities.append({
					"ID": c.getID(),
					"x": c.getX(),
					"y": c.getY(),
					#"index": c.getIndex(),
					"name": c.getName().replace("'", ""),
					"owner": c.getOwner(),
					"isBarbarian" : c.isBarbarian(),
					"size" : c.getPopulation(),
					"maintenance" : { "colony": cc.calculateColonyMaintenanceTimes100(), "distance": cc.calculateDistanceMaintenanceTimes100(), "numCities": cc.calculateNumCitiesMaintenanceTimes100(), "corps" : cc.calculateCorporationMaintenanceTimes100() },
					"food" : { "fpt": cc.getYieldRate(0), "food" : cc.getFood(), "difference" : cc.foodDifference(False), "foodKept" : cc.getFoodKept(), "foodTurnsLeft" : cc.getFoodTurnsLeft() },
					"happy" : { "espionageCounter": cc.getEspionageHappinessCounter(), "extra": cc.getExtraHappiness(), "totalHappy" : cc.happyLevel(), "angryPopulation" : cc.angryPopulation(0) }, #"fromBuildings" : cc.getBuildingHappiness(), "fromReligionGood": cc.getReligionGoodHappiness(), "fromReligionBad": cc.getReligionBadHappiness() },  # "totalGood": cc.calculateTotalCityHappiness(), "totalBad": cc.calculateTotalCityUnhappiness(), 
					"health" : { "espionageCounter": cc.getEspionageHealthCounter(), "goodHealth": cc.goodHealth(), "badHealth" : cc.badHealth(false), "fromResourcesGood" : cc.getBonusGoodHealth(), "fromResourcesBad" : cc.getBonusBadHealth(), "extra" : cc.getExtraHealth(), "fromBuildingsGood" : cc.getBuildingGoodHealth(), "fromBuildingsBad" : cc.getBuildingBadHealth()}, # "totalGood": cc.calculateTotalCityHealthiness (), "totalBad": cc.calculateTotalCityUnhealthiness(), 
					"production" : { "hpt": cc.getYieldRate(1), "isFood" : cc.isFoodProduction(), "overflow" : cc.getOverflowProduction(), "hammersInBox" : cc.getProduction(), "hammersNeeded" : cc.getProductionNeeded(), "name" : cc.getProductionName(), "process": cc.getProductionProcess(), "project": cc.getProductionProject(), "building": cc.getProductionBuilding(), "unit" : cc.getProductionUnit(), "turnsLeft": cc.getProductionTurnsLeft()},
					"commerce" : { "cpt" : cc.getYieldRate(2) },
					"specialists": specialists,
					"freeSpecialists": freeSpecialists,
					"buildings": buildings,
					"buildQueue": buildQueue,
					"religions": religions,
					"holyCities": holyCities
				})
			#print("..Dumping player " + str(p.getID()) + " player info...")
			currentResearch = pp.getCurrentResearch()
			currentTechTurnsLeft = 0
			if currentResearch >= 0:
				currentTechTurnsLeft = pp.getResearchTurnsLeft(currentResearch, True)
			players.append({
				"isAlive" : p.isAlive(),
				"ID" : p.getID(),
				"name" : p.getName(),
				"handicap" : int(pp.getHandicapType()),
				"color" : pp.getPlayerColor(),
				"team" : p.getTeamID(),
				"contacts" : contacts,
				"civics" : p.getCurrentCivicList(),
				"gold" : p.getGold(),
				"maintenanceCosts" : p.getTotalMaintenance(),
				"unitCosts": p.calculateUnitCost(),
				"unitSupply" : p.calculateUnitSupply(),
				"goldCommerceRate" : p.getGoldCommerceRate(),
				"researchCommerceRate" : p.getResearchCommerceRate(),
				"cultureCommerceRate" : p.getCultureCommerceRate(),
				"espionageCommerceRate" : pp.getCommerceRate(CommerceTypes.COMMERCE_ESPIONAGE),
				"beakersPerTurn" : p.calculateResearchRate(),
				"goldPerTurn" : p.getGoldPerTurn(),
				"techs" : p.getResearchedTechList(),
				"techProgress" : techProgress,
				"currentTechName" : p.getCurrentTechName(),
				"currentTech" : currentResearch,
				"overflowResearch" : pp.getOverflowResearch(),
				"currentTechTurnsLeft" : currentTechTurnsLeft,
				"civType" : pp.getCivilizationType(),
				"civDescription" : p.getCivDescription().replace("'", ""),
				"civName" : p.getCivilizationName().replace("'", ""),
				"civShortDescription" : p.getCivilizationShortDescription().replace("'", ""),
				"civAdjective": p.getCivilizationAdjective().replace("'", ""),
				"leaderName" : p.getLeaderName().replace("'", ""),
				"leaderType": p.getLeaderType(),
				"sliders": { "gold": pp.getCommercePercent(0), "research": pp.getCommercePercent(1), "culture": pp.getCommercePercent(2), "espionage": pp.getCommercePercent(3) },
				"cities": cities
			})
		#print(".Dumping map state...")
		for x in range(cyMap.getGridWidth()):
			for y in range(cyMap.getGridHeight()):
				plot = cyMap.plot(x, y)
				wc = plot.getWorkingCity()
				wcid = -1
				if not wc is None:
					wcid = wc.getID()
				visible = []
				revealed = []
				culture = []
				units = []
				for u in range(plot.getNumUnits()):
					unit = plot.getUnit(u)
					transportUnitID = -1
					if(not unit.getTransportUnit() is None):
						transportUnitID = unit.getTransportUnit().getID()
					promotions = []
					for pr in range(promotionTypeCount-1):
						if unit.isHasPromotion(pr):
							promotions.append(pr)
					units.append({
						"cargo": unit.getCargo(),
						"damage": unit.getDamage(),
						"buildType" : int(unit.getBuildType()),
						"xp": unit.getExperience(),
						"level": unit.getLevel(),
						"name" : unit.getName(),
						"moves" : unit.getMoves(),
						"owner" : unit.getOwner(),
						"ID" : unit.getID(),
						"transportUnit" : transportUnitID,
						"unitType" : unit.getUnitType(),
						"fortifyTurns" : unit.getFortifyTurns(),
						"promotions": promotions
					})
				for p in range(len(players)):
					culture.append(plot.getCulture(p))
				for t in range(cyGame.countCivTeamsEverAlive()):
					revealed.append(plot.isRevealed(t, False))
					visible.append(plot.isVisible(t, False))
				plots.append({"x": x, "y": y,
					"wcid": wcid,
					"worked": plot.isBeingWorked(),
					"bonus": plot.getBonusType(plot.getTeam()),
					"terrain": plot.getTerrainType(),
					"improvement": plot.getImprovementType(),
					"feature": { "type" : plot.getFeatureType(), "variety": plot.getFeatureVariety() },
					"river" : { "id" : plot.getRiverID(), "isNOfRiver" : plot.isNOfRiver(), "isWOfRiver": plot.isWOfRiver(), "isRiverSide" : plot.isRiverSide(), "nsDir" : int(plot.getRiverNSDirection()), "weDir" : int(plot.getRiverWEDirection()) },
					"isGoody": plot.isGoody(),
					"isImpassable" : plot.isImpassable(),
					"isFreshWater" : plot.isFreshWater(),
					"isIrrigated" : plot.isIrrigated(),
					"routeType" : plot.getRouteType(),
					"plotType" : int(plot.getPlotType()),
					"visible": visible,
					"revealed": revealed,
					"culture" : culture,
					"owner" : plot.calculateCulturalOwner(),
					"units" : units
				})
		#print(".Dumping game settings state...")
		jsondata = {
			"game": {
				"name": cyGame.getName().replace("'", ""),
				"turn": cyGame.getGameTurn(),
				"year": cyGame.getGameTurnYear(),
				"isCircumnavigated" : cyGame.isCircumnavigated(),
				"speed" : int(cyGame.getGameSpeedType()),
				"startEra" : int(cyGame.getStartEra()),
				"playerCount" : cyGame.countCivPlayersEverAlive(),
				"isPbem" : cyGame.isPbem(),
				"isPitboss" : cyGame.isPitboss(),
				"isPitbossHost" : cyGame.isPitbossHost()
			},
			"players" : players,
			"map": {
					"isWrapX" : cyMap.isWrapX(),
					"isWrapY" : cyMap.isWrapY(),
					"width" : cyMap.getGridWidth(),
					"height" : cyMap.getGridHeight(),
					"worldSize" : int(cyMap.getWorldSize()),
					"plots": plots
			}
		}
		#print(".Creating json file...")
		#print(".Using file name " + filename + "...")
		jsonstring = str(jsondata)
		jsonstring = jsonstring.replace(": u'", ": \"")
		jsonstring = jsonstring.replace("'", "\"")
		jsonstring = jsonstring.replace("False", "false")
		jsonstring = jsonstring.replace("True", "true")
		jsonstring = jsonstring.replace("}", "}\n")
		return jsonstring
	except Exception, err:
		return "{ \"error\": \"" + str(err) + "\" }"

def gameUtils():
	' replace normalGameUtils with your mod version'
	return normalGameUtils
		
def isVictoryTest():
	#CvUtil.pyPrint( "CvGameInterface.isVictoryTest" )
	return gameUtils().isVictoryTest()

def isVictory(argsList):
	return gameUtils().isVictory(argsList)

def isPlayerResearch(argsList):
	#CvUtil.pyPrint( "CvGameInterface.isPlayerResearch" )
	return gameUtils().isPlayerResearch(argsList)

def getExtraCost(argsList):
	#CvUtil.pyPrint( "CvGameInterface.getExtraCost" )
	return gameUtils().getExtraCost(argsList)

def createBarbarianCities():
	#CvUtil.pyPrint( "CvGameInterface.createBarbarianCities" )
	return gameUtils().createBarbarianCities()

def createBarbarianUnits():
	#CvUtil.pyPrint( "CvGameInterface.createBarbarianUnits" )
	return gameUtils().createBarbarianUnits()

def skipResearchPopup(argsList):
	#CvUtil.pyPrint( "CvGameInterface.skipResearchPopup" )
	return gameUtils().skipResearchPopup(argsList)

def showTechChooserButton(argsList):
	#CvUtil.pyPrint( "CvGameInterface.showTechChooserButton" )
	return gameUtils().showTechChooserButton(argsList)

def getFirstRecommendedTech(argsList):
	#CvUtil.pyPrint( "CvGameInterface.getFirstRecommendedTech" )
	return gameUtils().getFirstRecommendedTech(argsList)

def getSecondRecommendedTech(argsList):
	#CvUtil.pyPrint( "CvGameInterface.getSecondRecommendedTech" )
	return gameUtils().getSecondRecommendedTech(argsList)

def skipProductionPopup(argsList):
	#CvUtil.pyPrint( "CvGameInterface.skipProductionPopup" )
	return gameUtils().skipProductionPopup(argsList)

def canRazeCity(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canRazeCity" )
	return gameUtils().canRazeCity(argsList)

def canDeclareWar(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canRazeCity" )
	return gameUtils().canDeclareWar(argsList)

def showExamineCityButton(argsList):
	#CvUtil.pyPrint( "CvGameInterface.showExamineCityButton" )
	return gameUtils().showExamineCityButton(argsList)

def getRecommendedUnit(argsList):
	#CvUtil.pyPrint( "CvGameInterface.getRecommendedUnit" )
	return gameUtils().getRecommendedUnit(argsList)

def getRecommendedBuilding(argsList):
	#CvUtil.pyPrint( "CvGameInterface.getRecommendedBuilding" )
	return gameUtils().getRecommendedBuilding(argsList)

def updateColoredPlots():
	#CvUtil.pyPrint( "CvGameInterface.updateColoredPlots" )
	return gameUtils().updateColoredPlots()

def isActionRecommended(argsList):
	#CvUtil.pyPrint( "CvGameInterface.isActionRecommended" )
	return gameUtils().isActionRecommended(argsList)

def unitCannotMoveInto(argsList):
	return gameUtils().unitCannotMoveInto(argsList)

def cannotHandleAction(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotHandleAction" )
	return gameUtils().cannotHandleAction(argsList)

def canBuild(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canBuild" )
	return gameUtils().canBuild(argsList)

def cannotFoundCity(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotHandleAction" )
	return gameUtils().cannotFoundCity(argsList)

def cannotSelectionListMove(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotSelectionListMove" )
	return gameUtils().cannotSelectionListMove(argsList)

def cannotSelectionListGameNetMessage(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotSelectionListGameNetMessage" )
	return gameUtils().cannotSelectionListGameNetMessage(argsList)

def cannotDoControl(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotDoControl" )
	return gameUtils().cannotDoControl(argsList)

def canResearch(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canResearch" )
	return gameUtils().canResearch(argsList)

def cannotResearch(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotResearch" )
	return gameUtils().cannotResearch(argsList)

def canDoCivic(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canDoCivic" )
	return gameUtils().canDoCivic(argsList)

def cannotDoCivic(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotDoCivic" )
	return gameUtils().cannotDoCivic(argsList)

def canTrain(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canTrain" )
	return gameUtils().canTrain(argsList)

def cannotTrain(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotTrain" )
	return gameUtils().cannotTrain(argsList)

def canConstruct(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canConstruct" )
	return gameUtils().canConstruct(argsList)

def cannotConstruct(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotConstruct" )
	return gameUtils().cannotConstruct(argsList)

def canCreate(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canCreate" )
	return gameUtils().canCreate(argsList)

def cannotCreate(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotCreate" )
	return gameUtils().cannotCreate(argsList)

def canMaintain(argsList):
	#CvUtil.pyPrint( "CvGameInterface.canMaintain" )
	return gameUtils().canMaintain(argsList)

def cannotMaintain(argsList):
	#CvUtil.pyPrint( "CvGameInterface.cannotMaintain" )
	return gameUtils().cannotMaintain(argsList)

def AI_chooseTech(argsList):
	'AI chooses what to research'
	#CvUtil.pyPrint( "CvGameInterface.AI_chooseTech" )
	return gameUtils().AI_chooseTech(argsList)

def AI_chooseProduction(argsList):
	'AI chooses city production'
	#CvUtil.pyPrint( "CvGameInterface.AI_chooseProduction" )
	return gameUtils().AI_chooseProduction(argsList)

def AI_unitUpdate(argsList):
	'AI moves units - return 0 to let AI handle it, return 1 to say that the move is handled in python '
	#CvUtil.pyPrint( "CvGameInterface.AI_unitUpdate" )
	return gameUtils().AI_unitUpdate(argsList)

def AI_doWar(argsList):
	'AI decides whether to make war or peace - return 0 to let AI handle it, return 1 to say that the move is handled in python '
	#CvUtil.pyPrint( "CvGameInterface.AI_doWar" )
	return gameUtils().AI_doWar(argsList)

def AI_doDiplo(argsList):
	'AI decides does diplomacy for the turn - return 0 to let AI handle it, return 1 to say that the move is handled in python '
	#CvUtil.pyPrint( "CvGameInterface.AI_doDiplo" )
	return gameUtils().AI_doDiplo(argsList)

def calculateScore(argsList):
	return gameUtils().calculateScore(argsList)

def doHolyCity():
	#CvUtil.pyPrint( "CvGameInterface.doHolyCity" )
	return gameUtils().doHolyCity()

def doHolyCityTech(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doHolyCityTech" )
	return gameUtils().doHolyCityTech(argsList)

def doGold(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doGold" )
	return gameUtils().doGold(argsList)

def doResearch(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doResearch" )
	return gameUtils().doResearch(argsList)

def doGoody(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doGoody" )
	return gameUtils().doGoody(argsList)

def doGrowth(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doGrowth" )
	return gameUtils().doGrowth(argsList)

def doProduction(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doProduction" )
	return gameUtils().doProduction(argsList)

def doCulture(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doCulture" )
	return gameUtils().doCulture(argsList)

def doPlotCulture(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doPlotCulture" )
	return gameUtils().doPlotCulture(argsList)

def doReligion(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doReligion" )
	return gameUtils().doReligion(argsList)

def doGreatPeople(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doGreatPeople" )
	return gameUtils().doGreatPeople(argsList)

def doMeltdown(argsList):
	#CvUtil.pyPrint( "CvGameInterface.doMeltdown" )
	return gameUtils().doMeltdown(argsList)

def doReviveActivePlayer(argsList):
	return gameUtils().doReviveActivePlayer(argsList)

def doPillageGold(argsList):
	return gameUtils().doPillageGold(argsList)

def doCityCaptureGold(argsList):
	return gameUtils().doCityCaptureGold(argsList)

def citiesDestroyFeatures(argsList):
	return gameUtils().citiesDestroyFeatures(argsList)

def canFoundCitiesOnWater(argsList):
	return gameUtils().canFoundCitiesOnWater(argsList)

def doCombat(argsList):
	return gameUtils().doCombat(argsList)

def getConscriptUnitType(argsList):
	return gameUtils().getConscriptUnitType(argsList)

def getCityFoundValue(argsList):
	return gameUtils().getCityFoundValue(argsList)

def canPickPlot(argsList):
	return gameUtils().canPickPlot(argsList)

def getUnitCostMod(argsList):
	return gameUtils().getUnitCostMod(argsList)

def getBuildingCostMod(argsList):
	return gameUtils().getBuildingCostMod(argsList)

def canUpgradeAnywhere(argsList):
	return gameUtils().canUpgradeAnywhere(argsList)
	
def getWidgetHelp(argsList):
	return gameUtils().getWidgetHelp(argsList)
	
def getUpgradePriceOverride(argsList):
	return gameUtils().getUpgradePriceOverride(argsList)

def getExperienceNeeded(argsList):
	return gameUtils().getExperienceNeeded(argsList)