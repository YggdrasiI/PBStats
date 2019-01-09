""" Export of Civ4:BTS Python interfaces.

Useful options for pylint:
--disable=line-too-long,missing-docstring,too-many-lines,no-init,old-style-class,n
o-self-use,unused-argument,too-few-public-methods,too-many-pub
lic-methods,interface-not-implemented,too-many-arguments
"""

from CvTypes import *
# from CvGameCoreUtils import *
from CvDLLUtilityIFaceBase import *

# Extensions/Mods
PB_MOD = True

class CombatDetails:

    eOwner = int()
    eVisualOwner = int()
    iAIAnimalCombatModifierAA = int()
    iAIAnimalCombatModifierTA = int()
    iAIBarbarianCombatModifierAB = int()
    iAIBarbarianCombatModifierTB = int()
    iAmphibAttackModifier = int()
    iAnimalCombatModifierA = int()
    iAnimalCombatModifierAA = int()
    iAnimalCombatModifierT = int()
    iAnimalCombatModifierTA = int()
    iBarbarianCombatModifierAB = int()
    iBarbarianCombatModifierTB = int()
    iBaseCombatStr = int()
    iCityAttackModifier = int()
    iCityBarbarianDefenseModifier = int()
    iCityDefenseModifier = int()
    iClassAttackModifier = int()
    iClassDefenseModifier = int()
    iCombat = int()
    iCombatModifierA = int()
    iCombatModifierT = int()
    iCurrCombatStr = int()
    iCurrHitPoints = int()
    iDomainDefenseModifier = int()
    iDomainModifierA = int()
    iDomainModifierT = int()
    iExtraCombatPercent = int()
    iFeatureAttackModifier = int()
    iFeatureDefenseModifier = int()
    iFortifyModifier = int()
    iHillsAttackModifier = int()
    iHillsDefenseModifier = int()
    iKamikazeModifier = int()
    iMaxCombatStr = int()
    iMaxHitPoints = int()
    iModifierTotal = int()
    iPlotDefenseModifier = int()
    iRiverAttackModifier = int()
    iTerrainAttackModifier = int()
    iTerrainDefenseModifier = int()
    sUnitName = str()


class CvAssetInfoBase:

    @staticmethod
    def getPath():
        return str()

    @staticmethod
    def getTag():
        return str()

    @staticmethod
    def setPath(szDesc):
        pass

    @staticmethod
    def setTag(szDesc):
        pass
class CvArtInfoAsset(CvAssetInfoBase):

    @staticmethod
    def getButton():
        return str()

    @staticmethod
    def getKFM():
        return str()

    @staticmethod
    def getNIF():
        return str()

    @staticmethod
    def setButton(szVal):
        pass

    @staticmethod
    def setKFM(szDesc):
        pass

    @staticmethod
    def setNIF(szDesc):
        pass


class CvArtInfoScalableAsset(CvArtInfoAsset):
    pass


class CvActionInfo:

    @staticmethod
    def getAutomateType():
        return int()

    @staticmethod
    def getButton():
        return str()

    @staticmethod
    def getCommandData():
        return int()

    @staticmethod
    def getCommandType():
        return int()

    @staticmethod
    def getControlType():
        return int()

    @staticmethod
    def getHotKey():
        return str()

    @staticmethod
    def getInterfaceModeType():
        return int()

    @staticmethod
    def getMissionData():
        return int()

    @staticmethod
    def getMissionType():
        return int()

    @staticmethod
    def isConfirmCommand():
        return bool()

    @staticmethod
    def isVisible():
        return bool()




class CvArtInfoBonus(CvArtInfoScalableAsset):
    pass


class CvArtInfoBuilding(CvArtInfoScalableAsset):

    @staticmethod
    def isAnimated():
        return bool()


class CvArtInfoCivilization(CvArtInfoAsset):

    @staticmethod
    def isWhiteFlag():
        return bool()


class CvArtInfoFeature(CvArtInfoScalableAsset):

    @staticmethod
    def getFeatureDummyNodeName(variety, tagName):
        return str()

    @staticmethod
    def isAnimated():
        return bool()

    @staticmethod
    def isRiverArt():
        return bool()


class CvArtInfoImprovement(CvArtInfoScalableAsset):

    @staticmethod
    def isExtraAnimations():
        return bool()


class CvArtInfoInterface(CvArtInfoAsset):
    pass


class CvArtInfoLeaderhead(CvArtInfoAsset):
    pass


class CvArtInfoMisc(CvArtInfoAsset):
    pass


class CvArtInfoMovie(CvArtInfoAsset):
    pass


class CvArtInfoTerrain(CvArtInfoAsset):
    pass


class CvArtInfoUnit(CvArtInfoScalableAsset):

    @staticmethod
    def getInterfaceScale():
        return float()


class CvInfoBase:

    @staticmethod
    def getButton():
        return str()

    @staticmethod
    def getCivilopedia():
        return str()

    @staticmethod
    def getDescription():
        return str()

    @staticmethod
    def getDescriptionForm(uiForm):
        return str()

    @staticmethod
    def getHelp():
        return str()

    @staticmethod
    def getStrategy():
        return str()

    @staticmethod
    def getText():
        return str()

    @staticmethod
    def getTextKey():
        return str()

    @staticmethod
    def getType():
        return str()

    @staticmethod
    def isGraphicalOnly():
        return bool()

    @staticmethod
    def isMatchForLink(szLink, bKeysOnly):
        return bool()


class CvAutomateInfo(CvInfoBase):
    pass


class CvBonusClassInfo(CvInfoBase):

    @staticmethod
    def getUniqueRange():
        return int()


class CvBonusInfo(CvInfoBase):

    @staticmethod
    def getAIObjective():
        return int()

    @staticmethod
    def getAITradeModifier():
        return int()

    @staticmethod
    def getArtDefineTag():
        return str()

    @staticmethod
    def getArtInfo():
        return CvArtInfoBonus()

    @staticmethod
    def getBonusClassType():
        return int()

    @staticmethod
    def getButton():
        return str()

    @staticmethod
    def getChar():
        return int()

    @staticmethod
    def getConstAppearance():
        return int()

    @staticmethod
    def getGroupRand():
        return int()

    @staticmethod
    def getGroupRange():
        return int()

    @staticmethod
    def getHappiness():
        return int()

    @staticmethod
    def getHealth():
        return int()

    @staticmethod
    def getMaxLatitude():
        return int()

    @staticmethod
    def getMinAreaSize():
        return int()

    @staticmethod
    def getMinLandPercent():
        return int()

    @staticmethod
    def getMinLatitude():
        return int()

    @staticmethod
    def getPercentPerPlayer():
        return int()

    @staticmethod
    def getPlacementOrder():
        return int()

    @staticmethod
    def getRandAppearance1():
        return int()

    @staticmethod
    def getRandAppearance2():
        return int()

    @staticmethod
    def getRandAppearance3():
        return int()

    @staticmethod
    def getRandAppearance4():
        return int()

    @staticmethod
    def getTechCityTrade():
        return int()

    @staticmethod
    def getTechObsolete():
        return int()

    @staticmethod
    def getTechReveal():
        return int()

    @staticmethod
    def getTilesPer():
        return int()

    @staticmethod
    def getUniqueRange():
        return int()

    @staticmethod
    def getYieldChange(i):
        return int()

    @staticmethod
    def isFeature(i):
        return bool()

    @staticmethod
    def isFeatureTerrain(i):
        return bool()

    @staticmethod
    def isFlatlands():
        return bool()

    @staticmethod
    def isHills():
        return bool()

    @staticmethod
    def isNoRiverSide():
        return bool()

    @staticmethod
    def isNormalize():
        return bool()

    @staticmethod
    def isOneArea():
        return bool()

    @staticmethod
    def isTerrain(i):
        return bool()


class CvBuildInfo(CvInfoBase):

    @staticmethod
    def getCost():
        return int()

    @staticmethod
    def getEntityEvent():
        return int()

    @staticmethod
    def getFeatureProduction(i):
        return int()

    @staticmethod
    def getFeatureTech(i):
        return int()

    @staticmethod
    def getFeatureTime(i):
        return int()

    @staticmethod
    def getImprovement():
        return int()

    @staticmethod
    def getMissionType():
        return int()

    @staticmethod
    def getRoute():
        return int()

    @staticmethod
    def getTechPrereq():
        return int()

    @staticmethod
    def getTime():
        return int()

    @staticmethod
    def isFeatureRemove(i):
        return bool()

    @staticmethod
    def isKill():
        return bool()


class CvBuildingClassInfo(CvInfoBase):

    @staticmethod
    def getDefaultBuildingIndex():
        return int()

    @staticmethod
    def getExtraPlayerInstances():
        return int()

    @staticmethod
    def getMaxGlobalInstances():
        return int()

    @staticmethod
    def getMaxPlayerInstances():
        return int()

    @staticmethod
    def getMaxTeamInstances():
        return int()

    @staticmethod
    def getVictoryThreshold(i):
        return int()

    @staticmethod
    def isMonument():
        return bool()

    @staticmethod
    def isNoLimit():
        return bool()


class CvBuildingInfo(CvInfoBase):

    @staticmethod
    def getAIWeight():
        return int()

    @staticmethod
    def getAdvisorType():
        return int()

    @staticmethod
    def getAirModifier():
        return int()

    @staticmethod
    def getAirUnitCapacity():
        return int()

    @staticmethod
    def getAirlift():
        return int()

    @staticmethod
    def getAllCityDefenseModifier():
        return int()

    @staticmethod
    def getAnarchyModifier():
        return int()

    @staticmethod
    def getAreaFreeSpecialist():
        return int()

    @staticmethod
    def getAreaHappiness():
        return int()

    @staticmethod
    def getAreaHealth():
        return int()

    @staticmethod
    def getArtDefineTag():
        return str()

    @staticmethod
    def getArtInfo():
        return CvArtInfoBuilding()

    @staticmethod
    def getAssetValue():
        return int()

    @staticmethod
    def getBombardDefenseModifier():
        return int()

    @staticmethod
    def getBonusHappinessChanges(i):
        return int()

    @staticmethod
    def getBonusHealthChanges(i):
        return int()

    @staticmethod
    def getBonusProductionModifier(i):
        return int()

    @staticmethod
    def getBonusYieldModifier(i, j):
        return int()

    @staticmethod
    def getBuildingClassType():
        return int()

    @staticmethod
    def getBuildingHappinessChanges(i):
        return int()

    @staticmethod
    def getCivic():
        return int()

    @staticmethod
    def getCoastalTradeRoutes():
        return int()

    @staticmethod
    def getCommerceChange(i):
        return int()

    @staticmethod
    def getCommerceChangeDoubleTime(i):
        return int()

    @staticmethod
    def getCommerceHappiness(i):
        return int()

    @staticmethod
    def getCommerceModifier(i):
        return int()

    @staticmethod
    def getConquestProbability():
        return int()

    @staticmethod
    def getConstructSound():
        return str()

    @staticmethod
    def getDefenseModifier():
        return int()

    @staticmethod
    def getDomainFreeExperience(i):
        return int()

    @staticmethod
    def getDomainProductionModifier(i):
        return int()

    @staticmethod
    def getDomesticGreatGeneralRateModifier():
        return int()

    @staticmethod
    def getEnemyWarWearinessModifier():
        return int()

    @staticmethod
    def getEspionageDefenseModifier():
        return int()

    @staticmethod
    def getFlavorValue(i):
        return int()

    @staticmethod
    def getFoodKept():
        return int()

    @staticmethod
    def getForeignTradeRouteModifier():
        return int()

    @staticmethod
    def getFoundsCorporation():
        return int()

    @staticmethod
    def getFreeBonus():
        return int()

    @staticmethod
    def getFreeBuildingClass():
        return int()

    @staticmethod
    def getFreeExperience():
        return int()

    @staticmethod
    def getFreePromotion():
        return int()

    @staticmethod
    def getFreeSpecialist():
        return int()

    @staticmethod
    def getFreeSpecialistCount(i):
        return int()

    @staticmethod
    def getFreeStartEra():
        return int()

    @staticmethod
    def getFreeTechs():
        return int()

    @staticmethod
    def getGlobalCommerceModifier(i):
        return int()

    @staticmethod
    def getGlobalCorporationCommerce():
        return int()

    @staticmethod
    def getGlobalFreeExperience():
        return int()

    @staticmethod
    def getGlobalFreeSpecialist():
        return int()

    @staticmethod
    def getGlobalGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getGlobalHappiness():
        return int()

    @staticmethod
    def getGlobalHealth():
        return int()

    @staticmethod
    def getGlobalHurryModifier():
        return int()

    @staticmethod
    def getGlobalPopulationChange():
        return int()

    @staticmethod
    def getGlobalReligionCommerce():
        return int()

    @staticmethod
    def getGlobalSeaPlotYieldChange(i):
        return int()

    @staticmethod
    def getGlobalSpaceProductionModifier():
        return int()

    @staticmethod
    def getGlobalTradeRoutes():
        return int()

    @staticmethod
    def getGlobalWarWearinessModifier():
        return int()

    @staticmethod
    def getGlobalYieldModifier(i):
        return int()

    @staticmethod
    def getGoldenAgeModifier():
        return int()

    @staticmethod
    def getGreatGeneralRateModifier():
        return int()

    @staticmethod
    def getGreatPeopleRateChange():
        return int()

    @staticmethod
    def getGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getGreatPeopleUnitClass():
        return int()

    @staticmethod
    def getHappiness():
        return int()

    @staticmethod
    def getHappinessTraits(i):
        return int()

    @staticmethod
    def getHealRateChange():
        return int()

    @staticmethod
    def getHealth():
        return int()

    @staticmethod
    def getHolyCity():
        return int()

    @staticmethod
    def getHotKey():
        return str()

    @staticmethod
    def getHotKeyDescription():
        return str()

    @staticmethod
    def getHurryAngerModifier():
        return int()

    @staticmethod
    def getHurryCostModifier():
        return int()

    @staticmethod
    def getImprovementFreeSpecialist(i):
        return int()

    @staticmethod
    def getMaintenanceModifier():
        return int()

    @staticmethod
    def getMaxLatitude():
        return int()

    @staticmethod
    def getMaxStartEra():
        return int()

    @staticmethod
    def getMilitaryProductionModifier():
        return int()

    @staticmethod
    def getMinAreaSize():
        return int()

    @staticmethod
    def getMinLatitude():
        return int()

    @staticmethod
    def getMissionType():
        return int()

    @staticmethod
    def getMovie():
        return str()

    @staticmethod
    def getMovieDefineTag():
        return str()

    @staticmethod
    def getNoBonus():
        return int()

    @staticmethod
    def getNukeExplosionRand():
        return int()

    @staticmethod
    def getNukeModifier():
        return int()

    @staticmethod
    def getNumCitiesPrereq():
        return int()

    @staticmethod
    def getNumFreeBonuses():
        return int()

    @staticmethod
    def getNumTeamsPrereq():
        return int()

    @staticmethod
    def getObsoleteSafeCommerceChange(i):
        return int()

    @staticmethod
    def getObsoleteTech():
        return int()

    @staticmethod
    def getPowerBonus():
        return int()

    @staticmethod
    def getPowerValue():
        return int()

    @staticmethod
    def getPowerYieldModifier(i):
        return int()

    @staticmethod
    def getPrereqAndBonus():
        return int()

    @staticmethod
    def getPrereqAndTech():
        return int()

    @staticmethod
    def getPrereqAndTechs(i):
        return int()

    @staticmethod
    def getPrereqCorporation():
        return int()

    @staticmethod
    def getPrereqNumOfBuildingClass(i):
        return int()

    @staticmethod
    def getPrereqOrBonuses(i):
        return int()

    @staticmethod
    def getPrereqReligion():
        return int()

    @staticmethod
    def getProductionCost():
        return int()

    @staticmethod
    def getProductionTraits(i):
        return int()

    @staticmethod
    def getReligionChange(i):
        return int()

    @staticmethod
    def getReligionType():
        return int()

    @staticmethod
    def getRiverPlotYieldChange(i):
        return int()

    @staticmethod
    def getSeaPlotYieldChange(i):
        return int()

    @staticmethod
    def getSpaceProductionModifier():
        return int()

    @staticmethod
    def getSpecialBuildingType():
        return int()

    @staticmethod
    def getSpecialistCount(i):
        return int()

    @staticmethod
    def getSpecialistYieldChange(i, j):
        return int()

    @staticmethod
    def getStateReligion():
        return int()

    @staticmethod
    def getStateReligionCommerce(i):
        return int()

    @staticmethod
    def getStateReligionHappiness():
        return int()

    @staticmethod
    def getTradeRouteModifier():
        return int()

    @staticmethod
    def getTradeRoutes():
        return int()

    @staticmethod
    def getUnitCombatFreeExperience(i):
        return int()

    @staticmethod
    def getUnitLevelPrereq():
        return int()

    @staticmethod
    def getVictoryPrereq():
        return int()

    @staticmethod
    def getVoteSourceType():
        return int()

    @staticmethod
    def getWarWearinessModifier():
        return int()

    @staticmethod
    def getWorkerSpeedModifier():
        return int()

    @staticmethod
    def getYieldChange(i):
        return int()

    @staticmethod
    def getYieldModifier(i):
        return int()

    @staticmethod
    def isAllowsNukes():
        return bool()

    @staticmethod
    def isAreaBorderObstacle():
        return bool()

    @staticmethod
    def isAreaCleanPower():
        return bool()

    @staticmethod
    def isBuildingClassNeededInCity(i):
        return bool()

    @staticmethod
    def isBuildingOnlyHealthy():
        return bool()

    @staticmethod
    def isCapital():
        return bool()

    @staticmethod
    def isCenterInCity():
        return bool()

    @staticmethod
    def isCommerceChangeOriginalOwner(i):
        return bool()

    @staticmethod
    def isCommerceFlexible(i):
        return bool()

    @staticmethod
    def isDirtyPower():
        return bool()

    @staticmethod
    def isForceTeamVoteEligible():
        return bool()

    @staticmethod
    def isGoldenAge():
        return bool()

    @staticmethod
    def isGovernmentCenter():
        return bool()

    @staticmethod
    def isMapCentering():
        return bool()

    @staticmethod
    def isNeverCapture():
        return bool()

    @staticmethod
    def isNoUnhappiness():
        return bool()

    @staticmethod
    def isNoUnhealthyPopulation():
        return bool()

    @staticmethod
    def isNukeImmune():
        return bool()

    @staticmethod
    def isPower():
        return bool()

    @staticmethod
    def isPrereqReligion():
        return bool()

    @staticmethod
    def isRiver():
        return bool()

    @staticmethod
    def isStateReligion():
        return bool()

    @staticmethod
    def isTeamShare():
        return bool()

    @staticmethod
    def isWater():
        return bool()


class CvCivicInfo(CvInfoBase):

    @staticmethod
    def getAIWeight():
        return int()

    @staticmethod
    def getAnarchyLength():
        return int()

    @staticmethod
    def getBaseFreeMilitaryUnits():
        return int()

    @staticmethod
    def getBaseFreeUnits():
        return int()

    @staticmethod
    def getBuildingHappinessChanges(i):
        return int()

    @staticmethod
    def getBuildingHealthChanges(i):
        return int()

    @staticmethod
    def getCapitalCommerceModifier(i):
        return int()

    @staticmethod
    def getCapitalYieldModifier(i):
        return int()

    @staticmethod
    def getCivicOptionType():
        return int()

    @staticmethod
    def getCivicPercentAnger():
        return int()

    @staticmethod
    def getCommerceModifier(i):
        return int()

    @staticmethod
    def getCorporationMaintenanceModifier():
        return int()

    @staticmethod
    def getDistanceMaintenanceModifier():
        return int()

    @staticmethod
    def getDomesticGreatGeneralRateModifier():
        return int()

    @staticmethod
    def getExpInBorderModifier():
        return int()

    @staticmethod
    def getExtraHealth():
        return int()

    @staticmethod
    def getFeatureHappinessChanges(i):
        return int()

    @staticmethod
    def getFreeExperience():
        return int()

    @staticmethod
    def getFreeMilitaryUnitsPopulationPercent():
        return int()

    @staticmethod
    def getFreeSpecialist():
        return int()

    @staticmethod
    def getFreeUnitsPopulationPercent():
        return int()

    @staticmethod
    def getGoldPerMilitaryUnit():
        return int()

    @staticmethod
    def getGoldPerUnit():
        return int()

    @staticmethod
    def getGreatGeneralRateModifier():
        return int()

    @staticmethod
    def getGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getHappyPerMilitaryUnit():
        return int()

    @staticmethod
    def getImprovementUpgradeRateModifier():
        return int()

    @staticmethod
    def getImprovementYieldChanges(i, j):
        return int()

    @staticmethod
    def getLargestCityHappiness():
        return int()

    @staticmethod
    def getMaxConscript():
        return int()

    @staticmethod
    def getMilitaryProductionModifier():
        return int()

    @staticmethod
    def getNonStateReligionHappiness():
        return int()

    @staticmethod
    def getNumCitiesMaintenanceModifier():
        return int()

    @staticmethod
    def getSpecialistExtraCommerce(i):
        return int()

    @staticmethod
    def getStateReligionBuildingProductionModifier():
        return int()

    @staticmethod
    def getStateReligionFreeExperience():
        return int()

    @staticmethod
    def getStateReligionGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getStateReligionHappiness():
        return int()

    @staticmethod
    def getStateReligionUnitProductionModifier():
        return int()

    @staticmethod
    def getTechPrereq():
        return int()

    @staticmethod
    def getTradeRoutes():
        return int()

    @staticmethod
    def getTradeYieldModifier(i):
        return int()

    @staticmethod
    def getUpkeep():
        return int()

    @staticmethod
    def getWarWearinessModifier():
        return int()

    @staticmethod
    def getWorkerSpeedModifier():
        return int()

    @staticmethod
    def getYieldModifier(i):
        return int()

    @staticmethod
    def isBuildingOnlyHealthy():
        return bool()

    @staticmethod
    def isHurry(i):
        return bool()

    @staticmethod
    def isMilitaryFoodProduction():
        return bool()

    @staticmethod
    def isNoCorporations():
        return bool()

    @staticmethod
    def isNoForeignCorporations():
        return bool()

    @staticmethod
    def isNoForeignTrade():
        return bool()

    @staticmethod
    def isNoNonStateReligionSpread():
        return bool()

    @staticmethod
    def isNoUnhealthyPopulation():
        return bool()

    @staticmethod
    def isSpecialBuildingNotRequired(i):
        return bool()

    @staticmethod
    def isSpecialistValid(i):
        return bool()

    @staticmethod
    def isStateReligion():
        return bool()

    @staticmethod
    def pyGetWeLoveTheKing():
        return str()


class CvCivicOptionInfo(CvInfoBase):

    @staticmethod
    def getTraitNoUpkeep(i):
        return bool()


class CvCivilizationInfo(CvInfoBase):

    @staticmethod
    def getActionSoundScriptId():
        return int()

    @staticmethod
    def getAdjective(uiForm):
        return str()

    @staticmethod
    def getArtDefineTag():
        return str()

    @staticmethod
    def getArtStyleType():
        return int()

    @staticmethod
    def getButton():
        return str()

    @staticmethod
    def getCityNames(i):
        return str()

    @staticmethod
    def getCivilizationBuildings(i):
        return int()

    @staticmethod
    def getCivilizationFreeUnitsClass(i):
        return int()

    @staticmethod
    def getCivilizationInitialCivics(i):
        return int()

    @staticmethod
    def getCivilizationUnits(i):
        return int()

    @staticmethod
    def getDefaultPlayerColor():
        return int()

    @staticmethod
    def getDerivativeCiv():
        return int()

    @staticmethod
    def getFlagTexture():
        return str()

    @staticmethod
    def getNumCityNames():
        return int()

    @staticmethod
    def getNumLeaders():
        return int()

    @staticmethod
    def getSelectionSoundScriptId():
        return int()

    @staticmethod
    def getShortDescription(uiForm):
        return str()

    @staticmethod
    def getShortDescriptionKey():
        return str()

    @staticmethod
    def isAIPlayable():
        return bool()

    @staticmethod
    def isCivilizationDisableTechs(i):
        return bool()

    @staticmethod
    def isCivilizationFreeBuildingClass(i):
        return bool()

    @staticmethod
    def isCivilizationFreeTechs(i):
        return bool()

    @staticmethod
    def isLeaders(i):
        return bool()

    @staticmethod
    def isPlayable():
        return bool()


class CvClimateInfo(CvInfoBase):

    @staticmethod
    def getDesertBottomLatitudeChange():
        return float()

    @staticmethod
    def getDesertPercentChange():
        return int()

    @staticmethod
    def getDesertTopLatitudeChange():
        return float()

    @staticmethod
    def getGrassLatitudeChange():
        return float()

    @staticmethod
    def getHillRange():
        return int()

    @staticmethod
    def getIceLatitude():
        return float()

    @staticmethod
    def getJungleLatitude():
        return int()

    @staticmethod
    def getPeakPercent():
        return int()

    @staticmethod
    def getRandIceLatitude():
        return float()

    @staticmethod
    def getSnowLatitudeChange():
        return float()

    @staticmethod
    def getTundraLatitudeChange():
        return float()


class CvColorInfo(CvInfoBase):

    @staticmethod
    def getColor():
        return NiColorA(0, 0, 0, 0)


class CvCommandInfo(CvInfoBase):
    pass


class CvCommerceInfo(CvInfoBase):

    @staticmethod
    def getAIWeightPercent():
        return int()

    @staticmethod
    def getChar():
        return int()

    @staticmethod
    def getInitialHappiness():
        return int()

    @staticmethod
    def getInitialPercent():
        return int()

    @staticmethod
    def isFlexiblePercent():
        return bool()


class CvControlInfo(CvInfoBase):

    @staticmethod
    def getActionInfoIndex():
        return int()


class CvCorporationInfo(CvInfoBase):

    @staticmethod
    def getChar():
        return int()

    @staticmethod
    def getCommerceProduced(i):
        return int()

    @staticmethod
    def getFreeUnitClass():
        return int()

    @staticmethod
    def getHeadquarterChar():
        return int()

    @staticmethod
    def getHeadquarterCommerce(i):
        return int()

    @staticmethod
    def getMaintenance():
        return int()

    @staticmethod
    def getMissionType():
        return int()

    @staticmethod
    def getMovieFile():
        return str()

    @staticmethod
    def getMovieSound():
        return str()

    @staticmethod
    def getPrereqBonus(i):
        return int()

    @staticmethod
    def getSound():
        return str()

    @staticmethod
    def getSpreadCost():
        return int()

    @staticmethod
    def getSpreadFactor():
        return int()

    @staticmethod
    def getTechPrereq():
        return int()

    @staticmethod
    def getYieldProduced(i):
        return int()


class CvCultureLevelInfo(CvInfoBase):

    @staticmethod
    def getCityDefenseModifier():
        return int()

    @staticmethod
    def getSpeedThreshold(i):
        return int()


class CvDiplomacyInfo(CvInfoBase):

    @staticmethod
    def getAttitudeTypes(i, j):
        return bool()

    @staticmethod
    def getCivilizationTypes(i, j):
        return bool()

    @staticmethod
    def getDiplomacyPowerTypes(i, j):
        return bool()

    @staticmethod
    def getDiplomacyText(i, j):
        return str()

    @staticmethod
    def getLeaderHeadTypes(i, j):
        return bool()

    @staticmethod
    def getNumDiplomacyText(i):
        return int()

    @staticmethod
    def getNumResponses():
        return int()

    @staticmethod
    def getResponse(iNum):
        return CvDiplomacyResponse()


class CvDiplomacyResponse:

    # def getAttitudeTypes(self):
    #    return bool()

    @staticmethod
    def getAttitudeTypes(i=-1):
        return bool()

    # def getCivilizationTypes(self):
    #     return bool()

    @staticmethod
    def getCivilizationTypes(i=-1):
        return bool()

    # def getDiplomacyPowerTypes(self):
    #     return bool()

    @staticmethod
    def getDiplomacyPowerTypes(i=-1):
        return bool()

    # def getDiplomacyText(self):
    #     return str()

    @staticmethod
    def getDiplomacyText(i=-1):
        return str()

    # def getLeaderHeadTypes(self):
    #     return bool()

    @staticmethod
    def getLeaderHeadTypes(i=-1):
        return bool()

    @staticmethod
    def getNumDiplomacyText():
        return int()

    @staticmethod
    def setAttitudeTypes(i, bVal):
        pass

    @staticmethod
    def setCivilizationTypes(i, bVal):
        pass

    @staticmethod
    def setDiplomacyPowerTypes(i, bVal):
        pass

    @staticmethod
    def setLeaderHeadTypes(i, bVal):
        pass

    @staticmethod
    def setNumDiplomacyText(i):
        pass


class CvDiplomacyTextInfo(CvInfoBase):

    @staticmethod
    def getAttitudeTypes(i, j):
        return bool()

    @staticmethod
    def getCivilizationTypes(i, j):
        return bool()

    @staticmethod
    def getDiplomacyPowerTypes(i, j):
        return bool()

    @staticmethod
    def getDiplomacyText(i, j):
        return str()

    @staticmethod
    def getLeaderHeadTypes(i, j):
        return bool()

    @staticmethod
    def getNumDiplomacyText(i):
        return int()

    @staticmethod
    def getNumResponses():
        return int()

    @staticmethod
    def getResponse(iNum):
        return Response()


class CvEffectInfo(CvInfoBase):

    @staticmethod
    def getPath():
        return str()

    @staticmethod
    def setPath(szVal):
        pass


class CvEmphasizeInfo(CvInfoBase):

    @staticmethod
    def getCommerceChange(i):
        return int()

    @staticmethod
    def getYieldChange(i):
        return int()

    @staticmethod
    def isAvoidGrowth():
        return bool()

    @staticmethod
    def isGreatPeople():
        return bool()


class CvEraInfo(CvInfoBase):

    @staticmethod
    def getAnarchyPercent():
        return int()

    @staticmethod
    def getAudioUnitDefeatScript():
        return str()

    @staticmethod
    def getAudioUnitVictoryScript():
        return str()

    @staticmethod
    def getBuildPercent():
        return int()

    @staticmethod
    def getCitySoundscapeSciptId(i):
        return int()

    @staticmethod
    def getConstructPercent():
        return int()

    @staticmethod
    def getCreatePercent():
        return int()

    @staticmethod
    def getEventChancePerTurn():
        return int()

    @staticmethod
    def getFreePopulation():
        return int()

    @staticmethod
    def getGreatPeoplePercent():
        return int()

    @staticmethod
    def getGrowthPercent():
        return int()

    @staticmethod
    def getImprovementPercent():
        return int()

    @staticmethod
    def getNumSoundtracks():
        return int()

    @staticmethod
    def getResearchPercent():
        return int()

    @staticmethod
    def getSoundtrackSpace():
        return int()

    @staticmethod
    def getSoundtracks(i):
        return int()

    @staticmethod
    def getStartPercent():
        return int()

    @staticmethod
    def getStartingDefenseUnits():
        return int()

    @staticmethod
    def getStartingExploreUnits():
        return int()

    @staticmethod
    def getStartingGold():
        return int()

    @staticmethod
    def getStartingUnitMultiplier():
        return int()

    @staticmethod
    def getStartingWorkerUnits():
        return int()

    @staticmethod
    def getTrainPercent():
        return int()

    @staticmethod
    def isFirstSoundtrackFirst():
        return bool()

    @staticmethod
    def isNoAnimals():
        return bool()

    @staticmethod
    def isNoBarbCities():
        return bool()

    @staticmethod
    def isNoBarbUnits():
        return bool()

    @staticmethod
    def isNoGoodies():
        return bool()


class CvEspionageMissionInfo(CvInfoBase):

    @staticmethod
    def getBuyCityCostFactor():
        return int()

    @staticmethod
    def getBuyTechCostFactor():
        return int()

    @staticmethod
    def getBuyUnitCostFactor():
        return int()

    @staticmethod
    def getCityInsertCultureAmountFactor():
        return int()

    @staticmethod
    def getCityInsertCultureCostFactor():
        return int()

    @staticmethod
    def getCityPoisonWaterCounter():
        return int()

    @staticmethod
    def getCityRevoltCounter():
        return int()

    @staticmethod
    def getCityUnhappinessCounter():
        return int()

    @staticmethod
    def getCost():
        return int()

    @staticmethod
    def getCounterespionageMod():
        return int()

    @staticmethod
    def getCounterespionageNumTurns():
        return int()

    @staticmethod
    def getDestroyBuildingCostFactor():
        return int()

    @staticmethod
    def getDestroyUnitCostFactor():
        return int()

    @staticmethod
    def getDifficultyMod():
        return int()

    @staticmethod
    def getPlayerAnarchyCounter():
        return int()

    @staticmethod
    def getStealTreasuryTypes():
        return int()

    @staticmethod
    def getSwitchCivicCostFactor():
        return int()

    @staticmethod
    def getSwitchReligionCostFactor():
        return int()

    @staticmethod
    def getTechPrereq():
        return int()

    @staticmethod
    def getVisibilityLevel():
        return int()

    @staticmethod
    def isDestroyImprovement():
        return bool()

    @staticmethod
    def isInvestigateCity():
        return bool()

    @staticmethod
    def isNoActiveMissions():
        return bool()

    @staticmethod
    def isPassive():
        return bool()

    @staticmethod
    def isSeeDemographics():
        return bool()

    @staticmethod
    def isSeeResearch():
        return bool()

    @staticmethod
    def isSelectPlot():
        return bool()

    @staticmethod
    def isTargetsCity():
        return bool()

    @staticmethod
    def isTwoPhases():
        return bool()


class CvEventInfo(CvInfoBase):

    @staticmethod
    def getAIValue():
        return int()

    @staticmethod
    def getAdditionalEventChance(i):
        return int()

    @staticmethod
    def getAdditionalEventTime(i):
        return int()

    @staticmethod
    def getAttitudeModifier():
        return int()

    @staticmethod
    def getBonus():
        return int()

    @staticmethod
    def getBonusChange():
        return int()

    @staticmethod
    def getBonusGift():
        return int()

    @staticmethod
    def getBonusRevealed():
        return int()

    @staticmethod
    def getBuildingChange():
        return int()

    @staticmethod
    def getBuildingClass():
        return int()

    @staticmethod
    def getBuildingCommerceChange(iBuildingClass, iCommerce):
        return int()

    @staticmethod
    def getBuildingHappyChange(iBuildingClass):
        return int()

    @staticmethod
    def getBuildingHealthChange(iBuildingClass):
        return int()

    @staticmethod
    def getBuildingYieldChange(iBuildingClass, iYield):
        return int()

    @staticmethod
    def getClearEventChance(i):
        return int()

    @staticmethod
    def getConvertOtherCities():
        return int()

    @staticmethod
    def getConvertOwnCities():
        return int()

    @staticmethod
    def getCulture():
        return int()

    @staticmethod
    def getEspionagePoints():
        return int()

    @staticmethod
    def getFeature():
        return int()

    @staticmethod
    def getFeatureChange():
        return int()

    @staticmethod
    def getFood():
        return int()

    @staticmethod
    def getFoodPercent():
        return int()

    @staticmethod
    def getFreeSpecialistCount(i):
        return int()

    @staticmethod
    def getFreeUnitSupport():
        return int()

    @staticmethod
    def getGold():
        return int()

    @staticmethod
    def getHappy():
        return int()

    @staticmethod
    def getHappyTurns():
        return int()

    @staticmethod
    def getHealth():
        return int()

    @staticmethod
    def getHurryAnger():
        return int()

    @staticmethod
    def getImprovement():
        return int()

    @staticmethod
    def getImprovementChange():
        return int()

    @staticmethod
    def getInflationModifier():
        return int()

    @staticmethod
    def getMaxNumReligions():
        return int()

    @staticmethod
    def getMaxPillage():
        return int()

    @staticmethod
    def getMinPillage():
        return int()

    @staticmethod
    def getNumBuildingCommerceChanges():
        return int()

    @staticmethod
    def getNumBuildingHappyChanges():
        return int()

    @staticmethod
    def getNumBuildingHealthChanges():
        return int()

    @staticmethod
    def getNumBuildingYieldChanges():
        return int()

    @staticmethod
    def getNumUnits():
        return int()

    @staticmethod
    def getOurAttitudeModifier():
        return int()

    @staticmethod
    def getPlotExtraYield(i):
        return int()

    @staticmethod
    def getPopulationChange():
        return int()

    @staticmethod
    def getPrereqTech():
        return int()

    @staticmethod
    def getRandomGold():
        return int()

    @staticmethod
    def getRevoltTurns():
        return int()

    @staticmethod
    def getRoute():
        return int()

    @staticmethod
    def getRouteChange():
        return int()

    @staticmethod
    def getSpaceProductionModifier():
        return int()

    @staticmethod
    def getTech():
        return int()

    @staticmethod
    def getTechCostPercent():
        return int()

    @staticmethod
    def getTechFlavorValue(i):
        return int()

    @staticmethod
    def getTechMinTurnsLeft():
        return int()

    @staticmethod
    def getTechPercent():
        return int()

    @staticmethod
    def getTheirEnemyAttitudeModifier():
        return int()

    @staticmethod
    def getUnitClass():
        return int()

    @staticmethod
    def getUnitClassPromotion(i):
        return int()

    @staticmethod
    def getUnitCombatPromotion(i):
        return int()

    @staticmethod
    def getUnitExperience():
        return int()

    @staticmethod
    def getUnitImmobileTurns():
        return int()

    @staticmethod
    def getUnitPromotion():
        return int()

    @staticmethod
    def isCityEffect():
        return bool()

    @staticmethod
    def isDeclareWar():
        return bool()

    @staticmethod
    def isDisbandUnit():
        return bool()

    @staticmethod
    def isGlobal():
        return bool()

    @staticmethod
    def isGoldToPlayer():
        return bool()

    @staticmethod
    def isGoldenAge():
        return bool()

    @staticmethod
    def isOtherPlayerCityEffect():
        return bool()

    @staticmethod
    def isQuest():
        return bool()

    @staticmethod
    def isTeam():
        return bool()


class CvEventTriggerInfo(CvInfoBase):

    @staticmethod
    def getAngry():
        return int()

    @staticmethod
    def getBonusRequired(i):
        return int()

    @staticmethod
    def getBuildingRequired(i):
        return int()

    @staticmethod
    def getCityFoodWeight():
        return int()

    @staticmethod
    def getCivic():
        return int()

    @staticmethod
    def getCorporationRequired(i):
        return int()

    @staticmethod
    def getEvent(i):
        return int()

    @staticmethod
    def getFeatureRequired(i):
        return int()

    @staticmethod
    def getImprovementRequired(i):
        return int()

    @staticmethod
    def getMaxOurLandmass():
        return int()

    @staticmethod
    def getMaxPopulation():
        return int()

    @staticmethod
    def getMinDifficulty():
        return int()

    @staticmethod
    def getMinMapLandmass():
        return int()

    @staticmethod
    def getMinOurLandmass():
        return int()

    @staticmethod
    def getMinPopulation():
        return int()

    @staticmethod
    def getMinTreasury():
        return int()

    @staticmethod
    def getNumBonusesRequired():
        return int()

    @staticmethod
    def getNumBuildings():
        return int()

    @staticmethod
    def getNumBuildingsGlobal():
        return int()

    @staticmethod
    def getNumBuildingsRequired():
        return int()

    @staticmethod
    def getNumCorporations():
        return int()

    @staticmethod
    def getNumCorporationsRequired():
        return int()

    @staticmethod
    def getNumEvents():
        return int()

    @staticmethod
    def getNumFeaturesRequired():
        return int()

    @staticmethod
    def getNumImprovementsRequired():
        return int()

    @staticmethod
    def getNumObsoleteTechs():
        return int()

    @staticmethod
    def getNumPlotsRequired():
        return int()

    @staticmethod
    def getNumPrereqAndTechs():
        return int()

    @staticmethod
    def getNumPrereqEvents():
        return int()

    @staticmethod
    def getNumPrereqOrTechs():
        return int()

    @staticmethod
    def getNumReligions():
        return int()

    @staticmethod
    def getNumReligionsRequired():
        return int()

    @staticmethod
    def getNumRoutesRequired():
        return int()

    @staticmethod
    def getNumTerrainsRequired():
        return int()

    @staticmethod
    def getNumUnits():
        return int()

    @staticmethod
    def getNumUnitsGlobal():
        return int()

    @staticmethod
    def getNumUnitsRequired():
        return int()

    @staticmethod
    def getObsoleteTech(i):
        return int()

    @staticmethod
    def getOtherPlayerHasTech():
        return int()

    @staticmethod
    def getOtherPlayerShareBorders():
        return int()

    @staticmethod
    def getPercentGamesActive():
        return int()

    @staticmethod
    def getPlotsType():
        return int()

    @staticmethod
    def getPrereqAndTechs(i):
        return int()

    @staticmethod
    def getPrereqEvent(i):
        return int()

    @staticmethod
    def getPrereqOrTechs(i):
        return int()

    @staticmethod
    def getProbability():
        return int()

    @staticmethod
    def getReligionRequired(i):
        return int()

    @staticmethod
    def getRouteRequired(i):
        return int()

    @staticmethod
    def getTerrainRequired(i):
        return int()

    @staticmethod
    def getUnhealthy():
        return int()

    @staticmethod
    def getUnitDamagedWeight():
        return int()

    @staticmethod
    def getUnitDistanceWeight():
        return int()

    @staticmethod
    def getUnitExperienceWeight():
        return int()

    @staticmethod
    def getUnitRequired(i):
        return int()

    @staticmethod
    def isGlobal():
        return bool()

    @staticmethod
    def isOtherPlayerAI():
        return bool()

    @staticmethod
    def isOtherPlayerHasOtherReligion():
        return bool()

    @staticmethod
    def isOtherPlayerHasReligion():
        return bool()

    @staticmethod
    def isOwnPlot():
        return bool()

    @staticmethod
    def isPickCity():
        return bool()

    @staticmethod
    def isPickOtherPlayerCity():
        return bool()

    @staticmethod
    def isPickPlayer():
        return bool()

    @staticmethod
    def isPickReligion():
        return bool()

    @staticmethod
    def isPrereqEventCity():
        return bool()

    @staticmethod
    def isProbabilityBuildingMultiply():
        return bool()

    @staticmethod
    def isProbabilityUnitMultiply():
        return bool()

    @staticmethod
    def isRecurring():
        return bool()

    @staticmethod
    def isSinglePlayer():
        return bool()

    @staticmethod
    def isStateReligion():
        return bool()

    @staticmethod
    def isTeam():
        return bool()

    @staticmethod
    def isUnitsOnPlot():
        return bool()


class CvFeatureInfo(CvInfoBase):

    @staticmethod
    def getAdvancedStartRemoveCost():
        return int()

    @staticmethod
    def getAppearanceProbability():
        return int()

    @staticmethod
    def getDefenseModifier():
        return int()

    @staticmethod
    def getDisappearanceProbability():
        return int()

    @staticmethod
    def getGrowthProbability():
        return int()

    @staticmethod
    def getHealthPercent():
        return int()

    @staticmethod
    def getHillsYieldChange(i):
        return int()

    @staticmethod
    def getMovementCost():
        return int()

    @staticmethod
    def getNumVarieties():
        return int()

    @staticmethod
    def getRiverYieldChange(i):
        return int()

    @staticmethod
    def getSeeThroughChange():
        return int()

    @staticmethod
    def getTurnDamage():
        return int()

    @staticmethod
    def getYieldChange(i):
        return int()

    @staticmethod
    def isAddsFreshWater():
        return bool()

    @staticmethod
    def isImpassable():
        return bool()

    @staticmethod
    def isNoAdjacent():
        return bool()

    @staticmethod
    def isNoCity():
        return bool()

    @staticmethod
    def isNoCoast():
        return bool()

    @staticmethod
    def isNoImprovement():
        return bool()

    @staticmethod
    def isNoRiver():
        return bool()

    @staticmethod
    def isNukeImmune():
        return bool()

    @staticmethod
    def isRequiresFlatlands():
        return bool()

    @staticmethod
    def isRequiresRiver():
        return bool()

    @staticmethod
    def isTerrain(i):
        return bool()

    @staticmethod
    def isVisibleAlways():
        return bool()


class CvForceControlInfo(CvInfoBase):

    @staticmethod
    def getDefault():
        return bool()


class CvGameOptionInfo(CvInfoBase):

    @staticmethod
    def getDefault():
        return bool()

    @staticmethod
    def getVisible():
        return bool()


class CvGameSpeedInfo(CvInfoBase):

    @staticmethod
    def getAnarchyPercent():
        return int()

    @staticmethod
    def getBarbPercent():
        return int()

    @staticmethod
    def getBuildPercent():
        return int()

    @staticmethod
    def getConstructPercent():
        return int()

    @staticmethod
    def getCreatePercent():
        return int()

    @staticmethod
    def getFeatureProductionPercent():
        return int()

    @staticmethod
    def getGameTurnInfo(iIndex):
        return GameTurnInfo()

    @staticmethod
    def getGoldenAgePercent():
        return int()

    @staticmethod
    def getGreatPeoplePercent():
        return int()

    @staticmethod
    def getGrowthPercent():
        return int()

    @staticmethod
    def getHurryConscriptAngerPercent():
        return int()

    @staticmethod
    def getHurryPercent():
        return int()

    @staticmethod
    def getImprovementPercent():
        return int()

    @staticmethod
    def getInflationOffset():
        return int()

    @staticmethod
    def getInflationPercent():
        return int()

    @staticmethod
    def getNumTurnIncrements():
        return int()

    @staticmethod
    def getResearchPercent():
        return int()

    @staticmethod
    def getTrainPercent():
        return int()

    @staticmethod
    def getUnitDiscoverPercent():
        return int()

    @staticmethod
    def getUnitGreatWorkPercent():
        return int()

    @staticmethod
    def getUnitHurryPercent():
        return int()

    @staticmethod
    def getUnitTradePercent():
        return int()

    @staticmethod
    def getVictoryDelayPercent():
        return int()


class CvGameText(CvInfoBase):

    @staticmethod
    def getNumLanguages():
        return int()

    @staticmethod
    def getText():
        return str()

    @staticmethod
    def setText(szText):
        pass


class CvGoodyInfo(CvInfoBase):

    @staticmethod
    def getBarbarianUnitClass():
        return int()

    @staticmethod
    def getBarbarianUnitProb():
        return int()

    @staticmethod
    def getDamagePrereq():
        return int()

    @staticmethod
    def getExperience():
        return int()

    @staticmethod
    def getGold():
        return int()

    @staticmethod
    def getGoldRand1():
        return int()

    @staticmethod
    def getGoldRand2():
        return int()

    @staticmethod
    def getHealing():
        return int()

    @staticmethod
    def getMapOffset():
        return int()

    @staticmethod
    def getMapProb():
        return int()

    @staticmethod
    def getMapRange():
        return int()

    @staticmethod
    def getMinBarbarians():
        return int()

    @staticmethod
    def getSound():
        return str()

    @staticmethod
    def getUnitClassType():
        return int()

    @staticmethod
    def isBad():
        return bool()

    @staticmethod
    def isTech():
        return bool()


class CvGraphicOptionInfo(CvInfoBase):

    @staticmethod
    def getDefault():
        return bool()


class CvHandicapInfo(CvInfoBase):

    @staticmethod
    def getAIAdvancedStartPercent():
        return int()

    @staticmethod
    def getAIAnimalCombatModifier():
        return int()

    @staticmethod
    def getAIBarbarianCombatModifier():
        return int()

    @staticmethod
    def getAICivicUpkeepPercent():
        return int()

    @staticmethod
    def getAIConstructPercent():
        return int()

    @staticmethod
    def getAICreatePercent():
        return int()

    @staticmethod
    def getAIDeclareWarProb():
        return int()

    @staticmethod
    def getAIGrowthPercent():
        return int()

    @staticmethod
    def getAIInflationPercent():
        return int()

    @staticmethod
    def getAIPerEraModifier():
        return int()

    @staticmethod
    def getAIStartingDefenseUnits():
        return int()

    @staticmethod
    def getAIStartingExploreUnits():
        return int()

    @staticmethod
    def getAIStartingUnitMultiplier():
        return int()

    @staticmethod
    def getAIStartingWorkerUnits():
        return int()

    @staticmethod
    def getAITrainPercent():
        return int()

    @staticmethod
    def getAIUnitCostPercent():
        return int()

    @staticmethod
    def getAIUnitSupplyPercent():
        return int()

    @staticmethod
    def getAIUnitUpgradePercent():
        return int()

    @staticmethod
    def getAIWarWearinessPercent():
        return int()

    @staticmethod
    def getAIWorkRateModifier():
        return int()

    @staticmethod
    def getAIWorldConstructPercent():
        return int()

    @staticmethod
    def getAIWorldCreatePercent():
        return int()

    @staticmethod
    def getAIWorldTrainPercent():
        return int()

    @staticmethod
    def getAnimalAttackProb():
        return int()

    @staticmethod
    def getAnimalCombatModifier():
        return int()

    @staticmethod
    def getAttitudeChange():
        return int()

    @staticmethod
    def getBarbarianCityCreationProb():
        return int()

    @staticmethod
    def getBarbarianCityCreationTurnsElapsed():
        return int()

    @staticmethod
    def getBarbarianCombatModifier():
        return int()

    @staticmethod
    def getBarbarianCreationTurnsElapsed():
        return int()

    @staticmethod
    def getBarbarianInitialDefenders():
        return int()

    @staticmethod
    def getCivicUpkeepPercent():
        return int()

    @staticmethod
    def getColonyMaintenancePercent():
        return int()

    @staticmethod
    def getCorporationMaintenancePercent():
        return int()

    @staticmethod
    def getDistanceMaintenancePercent():
        return int()

    @staticmethod
    def getFreeUnits():
        return int()

    @staticmethod
    def getFreeWinsVsBarbs():
        return int()

    @staticmethod
    def getGoodies(i):
        return int()

    @staticmethod
    def getHappyBonus():
        return int()

    @staticmethod
    def getHealthBonus():
        return int()

    @staticmethod
    def getInflationPercent():
        return int()

    @staticmethod
    def getMaxColonyMaintenance():
        return int()

    @staticmethod
    def getMaxNumCitiesMaintenance():
        return int()

    @staticmethod
    def getNoTechTradeModifier():
        return int()

    @staticmethod
    def getNumCitiesMaintenancePercent():
        return int()

    @staticmethod
    def getNumGoodies():
        return int()

    @staticmethod
    def getResearchPercent():
        return int()

    @staticmethod
    def getStartingDefenseUnits():
        return int()

    @staticmethod
    def getStartingExploreUnits():
        return int()

    @staticmethod
    def getStartingGold():
        return int()

    @staticmethod
    def getStartingLocationPercent():
        return int()

    @staticmethod
    def getStartingWorkerUnits():
        return int()

    @staticmethod
    def getTechTradeKnownModifier():
        return int()

    @staticmethod
    def getUnitCostPercent():
        return int()

    @staticmethod
    def getUnownedTilesPerBarbarianCity():
        return int()

    @staticmethod
    def getUnownedTilesPerBarbarianUnit():
        return int()

    @staticmethod
    def getUnownedTilesPerGameAnimal():
        return int()

    @staticmethod
    def getUnownedWaterTilesPerBarbarianUnit():
        return int()

    @staticmethod
    def isAIFreeTechs(i):
        return int()

    @staticmethod
    def isFreeTechs(i):
        return int()


class CvHurryInfo(CvInfoBase):

    @staticmethod
    def getGoldPerProduction():
        return int()

    @staticmethod
    def getProductionPerPopulation():
        return int()

    @staticmethod
    def isAnger():
        return bool()


class CvImprovementBonusInfo(CvInfoBase):

    @staticmethod
    def getDiscoverRand():
        return int()

    @staticmethod
    def getYieldChange(i):
        return int()

    @staticmethod
    def isBonusMakesValid():
        return bool()

    @staticmethod
    def isBonusTrade():
        return bool()


class CvImprovementInfo(CvInfoBase):

    @staticmethod
    def getAirBombDefense():
        return int()

    @staticmethod
    def getArtDefineTag():
        return str()

    @staticmethod
    def getDefenseModifier():
        return int()

    @staticmethod
    def getFeatureGrowthProbability():
        return int()

    @staticmethod
    def getFeatureMakesValid(i):
        return bool()

    @staticmethod
    def getGoodyUniqueRange():
        return int()

    @staticmethod
    def getHappiness():
        return int()

    @staticmethod
    def getHillsYieldChange(i):
        return int()

    @staticmethod
    def getImprovementBonusDiscoverRand(i):
        return int()

    @staticmethod
    def getImprovementBonusYield(i, j):
        return int()

    @staticmethod
    def getImprovementPillage():
        return int()

    @staticmethod
    def getImprovementUpgrade():
        return int()

    @staticmethod
    def getIrrigatedYieldChange(i):
        return int()

    @staticmethod
    def getPillageGold():
        return int()

    @staticmethod
    def getPrereqNatureYield(i):
        return int()

    @staticmethod
    def getRiverSideYieldChange(i):
        return int()

    @staticmethod
    def getRouteYieldChanges(i, j):
        return int()

    @staticmethod
    def getTechYieldChanges(i, j):
        return int()

    @staticmethod
    def getTerrainMakesValid(i):
        return bool()

    @staticmethod
    def getTilesPerGoody():
        return int()

    @staticmethod
    def getUpgradeTime():
        return int()

    @staticmethod
    def getYieldChange(i):
        return int()

    @staticmethod
    def isActsAsCity():
        return bool()

    @staticmethod
    def isCarriesIrrigation():
        return bool()

    @staticmethod
    def isFreshWaterMakesValid():
        return bool()

    @staticmethod
    def isGoody():
        return bool()

    @staticmethod
    def isHillsMakesValid():
        return bool()

    @staticmethod
    def isImprovementBonusMakesValid(i):
        return bool()

    @staticmethod
    def isImprovementBonusTrade(i):
        return bool()

    @staticmethod
    def isNoFreshWater():
        return bool()

    @staticmethod
    def isOutsideBorders():
        return bool()

    @staticmethod
    def isPermanent():
        return bool()

    @staticmethod
    def isRequiresFeature():
        return bool()

    @staticmethod
    def isRequiresFlatlands():
        return bool()

    @staticmethod
    def isRequiresIrrigation():
        return bool()

    @staticmethod
    def isRequiresRiverSide():
        return bool()

    @staticmethod
    def isRiverSideMakesValid():
        return bool()

    @staticmethod
    def isWater():
        return bool()


class CvInterfaceModeInfo(CvInfoBase):

    @staticmethod
    def getCursorIndex():
        return int()

    @staticmethod
    def getGotoPlot():
        return bool()

    @staticmethod
    def getHighlightPlot():
        return bool()

    @staticmethod
    def getMissionType():
        return int()

    @staticmethod
    def getSelectAll():
        return bool()

    @staticmethod
    def getSelectType():
        return bool()

    @staticmethod
    def getVisible():
        return bool()


class CvLeaderHeadInfo(CvInfoBase):

    @staticmethod
    def getAdoptCivicRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getArtDefineTag():
        return str()

    @staticmethod
    def getAtPeaceAttitudeChangeLimit():
        return int()

    @staticmethod
    def getAtPeaceAttitudeDivisor():
        return int()

    @staticmethod
    def getAtWarAttitudeChangeLimit():
        return int()

    @staticmethod
    def getAtWarAttitudeDivisor():
        return int()

    @staticmethod
    def getAttackOddsChangeRand():
        return int()

    @staticmethod
    def getBaseAttackOddsChange():
        return int()

    @staticmethod
    def getBaseAttitude():
        return int()

    @staticmethod
    def getBasePeaceWeight():
        return int()

    @staticmethod
    def getBetterRankDifferenceAttitudeChange():
        return int()

    @staticmethod
    def getBonusTradeAttitudeChangeLimit():
        return int()

    @staticmethod
    def getBonusTradeAttitudeDivisor():
        return int()

    @staticmethod
    def getBuildUnitProb():
        return int()

    @staticmethod
    def getButton():
        return str()

    @staticmethod
    def getCloseBordersAttitudeChange():
        return int()

    @staticmethod
    def getContactDelay(i):
        return int()

    @staticmethod
    def getContactRand(i):
        return int()

    @staticmethod
    def getConvertReligionRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getDeclareWarRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getDeclareWarThemRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getDeclareWarTradeRand():
        return int()

    @staticmethod
    def getDefensivePactAttitudeChangeLimit():
        return int()

    @staticmethod
    def getDefensivePactAttitudeDivisor():
        return int()

    @staticmethod
    def getDefensivePactRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getDemandRebukedSneakProb():
        return int()

    @staticmethod
    def getDemandRebukedWarProb():
        return int()

    @staticmethod
    def getDemandTributeAttitudeThreshold():
        return int()

    @staticmethod
    def getDifferentReligionAttitudeChange():
        return int()

    @staticmethod
    def getDifferentReligionAttitudeChangeLimit():
        return int()

    @staticmethod
    def getDifferentReligionAttitudeDivisor():
        return int()

    @staticmethod
    def getDiploPeaceIntroMusicScriptIds(i):
        return int()

    @staticmethod
    def getDiploPeaceMusicScriptIds(i):
        return int()

    @staticmethod
    def getDiploWarIntroMusicScriptIds(i):
        return int()

    @staticmethod
    def getDiploWarMusicScriptIds(i):
        return int()

    @staticmethod
    def getDogpileWarRand():
        return int()

    @staticmethod
    def getEspionageWeight():
        return int()

    @staticmethod
    def getFavoriteCivic():
        return int()

    @staticmethod
    def getFavoriteCivicAttitudeChange():
        return int()

    @staticmethod
    def getFavoriteCivicAttitudeChangeLimit():
        return int()

    @staticmethod
    def getFavoriteCivicAttitudeDivisor():
        return int()

    @staticmethod
    def getFavoriteReligion():
        return int()

    @staticmethod
    def getFlavorValue(i):
        return int()

    @staticmethod
    def getFreedomAppreciation():
        return int()

    @staticmethod
    def getHappinessBonusRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getHealthBonusRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getImprovementWeightModifier(i):
        return int()

    @staticmethod
    def getLeaderHead():
        return str()

    @staticmethod
    def getLimitedWarPowerRatio():
        return int()

    @staticmethod
    def getLimitedWarRand():
        return int()

    @staticmethod
    def getLostWarAttitudeChange():
        return int()

    @staticmethod
    def getMakePeaceRand():
        return int()

    @staticmethod
    def getMapRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getMaxGoldPerTurnTradePercent():
        return int()

    @staticmethod
    def getMaxGoldTradePercent():
        return int()

    @staticmethod
    def getMaxWarDistantPowerRatio():
        return int()

    @staticmethod
    def getMaxWarMinAdjacentLandPercent():
        return int()

    @staticmethod
    def getMaxWarNearbyPowerRatio():
        return int()

    @staticmethod
    def getMaxWarRand():
        return int()

    @staticmethod
    def getMemoryAttitudePercent(i):
        return int()

    @staticmethod
    def getMemoryDecayRand(i):
        return int()

    @staticmethod
    def getNoGiveHelpAttitudeThreshold():
        return int()

    @staticmethod
    def getNoTechTradeThreshold():
        return int()

    @staticmethod
    def getNoWarAttitudeProb(i):
        return int()

    @staticmethod
    def getOpenBordersAttitudeChangeLimit():
        return int()

    @staticmethod
    def getOpenBordersAttitudeDivisor():
        return int()

    @staticmethod
    def getOpenBordersRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getPeaceWeightRand():
        return int()

    @staticmethod
    def getPermanentAllianceRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getRazeCityProb():
        return int()

    @staticmethod
    def getRefuseToTalkWarThreshold():
        return int()

    @staticmethod
    def getSameReligionAttitudeChange():
        return int()

    @staticmethod
    def getSameReligionAttitudeChangeLimit():
        return int()

    @staticmethod
    def getSameReligionAttitudeDivisor():
        return int()

    @staticmethod
    def getShareWarAttitudeChange():
        return int()

    @staticmethod
    def getShareWarAttitudeChangeLimit():
        return int()

    @staticmethod
    def getShareWarAttitudeDivisor():
        return int()

    @staticmethod
    def getStopTradingRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getStopTradingThemRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getStrategicBonusRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getTechRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getTechTradeKnownPercent():
        return int()

    @staticmethod
    def getUnitAIWeightModifier(i):
        return int()

    @staticmethod
    def getVassalPowerModifier():
        return int()

    @staticmethod
    def getVassalRefuseAttitudeThreshold():
        return int()

    @staticmethod
    def getWarmongerRespect():
        return int()

    @staticmethod
    def getWonderConstructRand():
        return int()

    @staticmethod
    def getWorseRankDifferenceAttitudeChange():
        return int()

    @staticmethod
    def hasTrait(i):
        return bool()


class CvMPOptionInfo(CvInfoBase):

    @staticmethod
    def getDefault():
        return bool()


class CvMainMenuInfo(CvInfoBase):

    @staticmethod
    def getLoading():
        return str()

    @staticmethod
    def getLoadingSlideshow():
        return str()

    @staticmethod
    def getScene():
        return str()

    @staticmethod
    def getSceneNoShader():
        return str()

    @staticmethod
    def getSoundtrack():
        return str()


class CvMissionInfo(CvInfoBase):

    @staticmethod
    def getTime():
        return int()

    @staticmethod
    def getVisible():
        return bool()

    @staticmethod
    def getWaypoint():
        return str()

    @staticmethod
    def isBuild():
        return bool()

    @staticmethod
    def isSound():
        return bool()

    @staticmethod
    def isTarget():
        return bool()


class CvPlayerColorInfo(CvInfoBase):

    @staticmethod
    def getColorTypePrimary():
        return int()

    @staticmethod
    def getColorTypeSecondary():
        return int()

    @staticmethod
    def getTextColorType():
        return int()


class CvPlayerOptionInfo(CvInfoBase):

    @staticmethod
    def getDefault():
        return bool()


class CvProcessInfo(CvInfoBase):

    @staticmethod
    def getProductionToCommerceModifier(i):
        return int()

    @staticmethod
    def getTechPrereq():
        return int()


class CvProjectInfo(CvInfoBase):

    @staticmethod
    def getAnyoneProjectPrereq():
        return int()

    @staticmethod
    def getBonusProductionModifier(i):
        return int()

    @staticmethod
    def getCreateSound():
        return str()

    @staticmethod
    def getEveryoneSpecialBuilding():
        return int()

    @staticmethod
    def getEveryoneSpecialUnit():
        return int()

    @staticmethod
    def getMaxGlobalInstances():
        return int()

    @staticmethod
    def getMaxTeamInstances():
        return int()

    @staticmethod
    def getMovieArtDef():
        return str()

    @staticmethod
    def getNukeInterception():
        return int()

    @staticmethod
    def getProductionCost():
        return int()

    @staticmethod
    def getProjectsNeeded(i):
        return int()

    @staticmethod
    def getSuccessRate():
        return int()

    @staticmethod
    def getTechPrereq():
        return int()

    @staticmethod
    def getTechShare():
        return int()

    @staticmethod
    def getVictoryDelayPercent():
        return int()

    @staticmethod
    def getVictoryMinThreshold(i):
        return int()

    @staticmethod
    def getVictoryPrereq():
        return int()

    @staticmethod
    def getVictoryThreshold(i):
        return int()

    @staticmethod
    def isAllowsNukes():
        return bool()

    @staticmethod
    def isSpaceship():
        return bool()


class CvPromotionInfo(CvInfoBase):

    @staticmethod
    def getActionInfoIndex():
        return int()

    @staticmethod
    def getAdjacentTileHealChange():
        return int()

    @staticmethod
    def getAirRangeChange():
        return int()

    @staticmethod
    def getBombardRateChange():
        return int()

    @staticmethod
    def getCargoChange():
        return int()

    @staticmethod
    def getChanceFirstStrikesChange():
        return int()

    @staticmethod
    def getCityAttackPercent():
        return int()

    @staticmethod
    def getCityDefensePercent():
        return int()

    @staticmethod
    def getCollateralDamageChange():
        return int()

    @staticmethod
    def getCollateralDamageProtection():
        return int()

    @staticmethod
    def getCombatPercent():
        return int()

    @staticmethod
    def getCommandType():
        return int()

    @staticmethod
    def getDomainModifierPercent(i):
        return int()

    @staticmethod
    def getEnemyHealChange():
        return int()

    @staticmethod
    def getEvasionChange():
        return int()

    @staticmethod
    def getExperiencePercent():
        return int()

    @staticmethod
    def getFeatureAttackPercent(i):
        return int()

    @staticmethod
    def getFeatureDefensePercent(i):
        return int()

    @staticmethod
    def getFeatureDoubleMove(i):
        return bool()

    @staticmethod
    def getFirstStrikesChange():
        return int()

    @staticmethod
    def getFriendlyHealChange():
        return int()

    @staticmethod
    def getHillsAttackPercent():
        return int()

    @staticmethod
    def getHillsDefensePercent():
        return int()

    @staticmethod
    def getInterceptChange():
        return int()

    @staticmethod
    def getKamikazePercent():
        return int()

    @staticmethod
    def getMoveDiscountChange():
        return int()

    @staticmethod
    def getMovesChange():
        return int()

    @staticmethod
    def getNeutralHealChange():
        return int()

    @staticmethod
    def getPillageChange():
        return int()

    @staticmethod
    def getPrereqOrPromotion1():
        return int()

    @staticmethod
    def getPrereqOrPromotion2():
        return int()

    @staticmethod
    def getPrereqPromotion():
        return int()

    @staticmethod
    def getRevoltProtection():
        return int()

    @staticmethod
    def getSameTileHealChange():
        return int()

    @staticmethod
    def getSound():
        return str()

    @staticmethod
    def getStateReligionPrereq():
        return int()

    @staticmethod
    def getTechPrereq():
        return int()

    @staticmethod
    def getTerrainAttackPercent(i):
        return int()

    @staticmethod
    def getTerrainDefensePercent(i):
        return int()

    @staticmethod
    def getTerrainDoubleMove(i):
        return bool()

    @staticmethod
    def getUnitCombat(i):
        return bool()

    @staticmethod
    def getUnitCombatModifierPercent(i):
        return int()

    @staticmethod
    def getUpgradeDiscount():
        return int()

    @staticmethod
    def getVisibilityChange():
        return int()

    @staticmethod
    def getWithdrawalChange():
        return int()

    @staticmethod
    def isAlwaysHeal():
        return bool()

    @staticmethod
    def isAmphib():
        return bool()

    @staticmethod
    def isBlitz():
        return bool()

    @staticmethod
    def isEnemyRoute():
        return bool()

    @staticmethod
    def isHillsDoubleMove():
        return bool()

    @staticmethod
    def isImmuneToFirstStrikes():
        return bool()

    @staticmethod
    def isLeader():
        return bool()

    @staticmethod
    def isRiver():
        return bool()


class CvQuestInfo(CvInfoBase):

    @staticmethod
    def getNumQuestLinks():
        return int()

    @staticmethod
    def getNumQuestMessages():
        return int()

    @staticmethod
    def getNumQuestSounds():
        return int()

    @staticmethod
    def getQuestBodyText():
        return str()

    @staticmethod
    def getQuestLinkName(iIndex):
        return str()

    @staticmethod
    def getQuestLinkType(iIndex):
        return str()

    @staticmethod
    def getQuestMessages(iIndex):
        return str()

    @staticmethod
    def getQuestObjective():
        return str()

    @staticmethod
    def getQuestSounds(iIndex):
        return str()

    @staticmethod
    def setNumQuestMessages(iNum):
        pass

    @staticmethod
    def setQuestBodyText(szText):
        pass

    @staticmethod
    def setQuestMessages(iIndex, szText):
        pass

    @staticmethod
    def setQuestObjective(szText):
        pass


class CvReligionInfo(CvInfoBase):

    @staticmethod
    def getAdjectiveKey():
        return str()

    @staticmethod
    def getButtonDisabled():
        return str()

    @staticmethod
    def getChar():
        return int()

    @staticmethod
    def getFreeUnitClass():
        return int()

    @staticmethod
    def getGenericTechButton():
        return str()

    @staticmethod
    def getGlobalReligionCommerce(i):
        return int()

    @staticmethod
    def getHolyCityChar():
        return int()

    @staticmethod
    def getHolyCityCommerce(i):
        return int()

    @staticmethod
    def getMissionType():
        return int()

    @staticmethod
    def getMovieFile():
        return str()

    @staticmethod
    def getMovieSound():
        return str()

    @staticmethod
    def getNumFreeUnits():
        return int()

    @staticmethod
    def getSound():
        return str()

    @staticmethod
    def getSpreadFactor():
        return int()

    @staticmethod
    def getStateReligionCommerce(i):
        return int()

    @staticmethod
    def getTechButton():
        return str()

    @staticmethod
    def getTechPrereq():
        return int()


class CvRouteInfo(CvInfoBase):

    @staticmethod
    def getFlatMovementCost():
        return int()

    @staticmethod
    def getMovementCost():
        return int()

    @staticmethod
    def getPrereqBonus():
        return int()

    @staticmethod
    def getPrereqOrBonus(i):
        return int()

    @staticmethod
    def getTechMovementChange(i):
        return int()

    @staticmethod
    def getValue():
        return int()

    @staticmethod
    def getYieldChange(i):
        return int()


class CvRouteModelInfo(CvInfoBase):

    @staticmethod
    def getConnectString():
        return str()

    @staticmethod
    def getModelConnectString():
        return str()

    @staticmethod
    def getModelFile():
        return str()

    @staticmethod
    def getModelFileKey():
        return str()

    @staticmethod
    def getRotateString():
        return str()

    @staticmethod
    def setModelFile(szVal):
        pass

    @staticmethod
    def setModelFileKey(szVal):
        pass


class CvScalableInfo:

    @staticmethod
    def getScale():
        return float()

    @staticmethod
    def setScale(fScale):
        pass


class CvSeaLevelInfo(CvInfoBase):

    @staticmethod
    def getSeaLevelChange():
        return int()


class CvSpecialBuildingInfo(CvInfoBase):

    @staticmethod
    def getObsoleteTech():
        return int()

    @staticmethod
    def getProductionTraits(i):
        return int()

    @staticmethod
    def getTechPrereq():
        return int()

    @staticmethod
    def isValid():
        return bool()


class CvSpecialUnitInfo(CvInfoBase):

    @staticmethod
    def getProductionTraits(i):
        return int()

    @staticmethod
    def isCarrierUnitAIType(i):
        return bool()

    @staticmethod
    def isCityLoad():
        return bool()

    @staticmethod
    def isValid():
        return bool()


class CvSpecialistInfo(CvInfoBase):

    @staticmethod
    def getCommerceChange(i):
        return int()

    @staticmethod
    def getExperience():
        return int()

    @staticmethod
    def getFlavorValue(i):
        return int()

    @staticmethod
    def getGreatPeopleRateChange():
        return int()

    @staticmethod
    def getGreatPeopleUnitClass():
        return int()

    @staticmethod
    def getMissionType():
        return int()

    @staticmethod
    def getTexture():
        return str()

    @staticmethod
    def getYieldChange(i):
        return int()

    @staticmethod
    def isVisible():
        return bool()


class CvTechInfo(CvInfoBase):

    @staticmethod
    def getAITradeModifier():
        return int()

    @staticmethod
    def getAIWeight():
        return int()

    @staticmethod
    def getAdvisorType():
        return int()

    @staticmethod
    def getAssetValue():
        return int()

    @staticmethod
    def getDomainExtraMoves(i):
        return int()

    @staticmethod
    def getEra():
        return int()

    @staticmethod
    def getFeatureProductionModifier():
        return int()

    @staticmethod
    def getFirstFreeTechs():
        return int()

    @staticmethod
    def getFirstFreeUnitClass():
        return int()

    @staticmethod
    def getFlavorValue(i):
        return int()

    @staticmethod
    def getGridX():
        return int()

    @staticmethod
    def getGridY():
        return int()

    @staticmethod
    def getHappiness():
        return int()

    @staticmethod
    def getHealth():
        return int()

    @staticmethod
    def getPowerValue():
        return int()

    @staticmethod
    def getPrereqAndTechs(i):
        return int()

    @staticmethod
    def getPrereqOrTechs(i):
        return int()

    @staticmethod
    def getQuote():
        return str()

    @staticmethod
    def getResearchCost():
        return int()

    @staticmethod
    def getSound():
        return str()

    @staticmethod
    def getSoundMP():
        return str()

    @staticmethod
    def getTradeRoutes():
        return int()

    @staticmethod
    def getWorkerSpeedModifier():
        return int()

    @staticmethod
    def isBridgeBuilding():
        return bool()

    @staticmethod
    def isCommerceFlexible(i):
        return bool()

    @staticmethod
    def isDefensivePactTrading():
        return bool()

    @staticmethod
    def isDisable():
        return bool()

    @staticmethod
    def isExtraWaterSeeFrom():
        return bool()

    @staticmethod
    def isGoldTrading():
        return bool()

    @staticmethod
    def isGoodyTech():
        return bool()

    @staticmethod
    def isIgnoreIrrigation():
        return bool()

    @staticmethod
    def isIrrigation():
        return bool()

    @staticmethod
    def isMapCentering():
        return bool()

    @staticmethod
    def isMapTrading():
        return bool()

    @staticmethod
    def isMapVisible():
        return bool()

    @staticmethod
    def isOpenBordersTrading():
        return bool()

    @staticmethod
    def isPermanentAllianceTrading():
        return bool()

    @staticmethod
    def isRepeat():
        return bool()

    @staticmethod
    def isRiverTrade():
        return bool()

    @staticmethod
    def isTechTrading():
        return bool()

    @staticmethod
    def isTerrainTrade(i):
        return bool()

    @staticmethod
    def isTrade():
        return bool()

    @staticmethod
    def isVassalStateTrading():
        return bool()

    @staticmethod
    def isWaterWork():
        return bool()


class CvTerrainInfo(CvInfoBase):

    @staticmethod
    def getBuildModifier():
        return int()

    @staticmethod
    def getDefenseModifier():
        return int()

    @staticmethod
    def getHillsYieldChange(i):
        return int()

    @staticmethod
    def getMovementCost():
        return int()

    @staticmethod
    def getRiverYieldChange(i):
        return int()

    @staticmethod
    def getSeeFromLevel():
        return int()

    @staticmethod
    def getSeeThroughLevel():
        return int()

    @staticmethod
    def getYield(i):
        return int()

    @staticmethod
    def isFound():
        return bool()

    @staticmethod
    def isFoundCoast():
        return bool()

    @staticmethod
    def isFoundFreshWater():
        return bool()

    @staticmethod
    def isImpassable():
        return bool()

    @staticmethod
    def isWater():
        return bool()


class CvTraitInfo(CvInfoBase):

    @staticmethod
    def getCommerceChange(i):
        return int()

    @staticmethod
    def getCommerceModifier(i):
        return int()

    @staticmethod
    def getDomesticGreatGeneralRateModifier():
        return int()

    @staticmethod
    def getExtraYieldThreshold(i):
        return int()

    @staticmethod
    def getGreatGeneralRateModifier():
        return int()

    @staticmethod
    def getGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getHappiness():
        return int()

    @staticmethod
    def getHealth():
        return int()

    @staticmethod
    def getLevelExperienceModifier():
        return int()

    @staticmethod
    def getMaxAnarchy():
        return int()

    @staticmethod
    def getMaxGlobalBuildingProductionModifier():
        return int()

    @staticmethod
    def getMaxPlayerBuildingProductionModifier():
        return int()

    @staticmethod
    def getMaxTeamBuildingProductionModifier():
        return int()

    @staticmethod
    def getShortDescription():
        return str()

    @staticmethod
    def getTradeYieldModifier(i):
        return int()

    @staticmethod
    def getUpkeepModifier():
        return int()

    @staticmethod
    def isFreePromotion(i):
        return int()


class CvTurnTimerInfo(CvInfoBase):

    @staticmethod
    def getBaseTime():
        return int()

    @staticmethod
    def getCityBonus():
        return int()

    @staticmethod
    def getFirstTurnMultiplier():
        return int()

    @staticmethod
    def getUnitBonus():
        return int()


class CvTutorialInfo(CvInfoBase):

    @staticmethod
    def getNextTutorialInfoType():
        return str()

    @staticmethod
    def getNumTutorialMessages():
        return int()

    @staticmethod
    def getTutorialMessage(iIndex):
        return CvTutorialMessage()


class CvTutorialMessage:

    @staticmethod
    def getImage():
        return str()

    @staticmethod
    def getNumTutorialScripts():
        return int()

    @staticmethod
    def getSound():
        return str()

    @staticmethod
    def getText():
        return str()

    @staticmethod
    def getTutorialScriptByIndex(i):
        return str()


class CvUnitArtStyleTypeInfo(CvInfoBase):
    # Created because referred by
    # CyGlobalContext.getUnitArtStyleTypeInfo()
    pass


class CvUnitClassInfo(CvInfoBase):

    @staticmethod
    def getDefaultUnitIndex():
        return int()

    @staticmethod
    def getInstanceCostModifier():
        return int()

    @staticmethod
    def getMaxGlobalInstances():
        return int()

    @staticmethod
    def getMaxPlayerInstances():
        return int()

    @staticmethod
    def getMaxTeamInstances():
        return int()


class CvUnitInfo(CvInfoBase):

    @staticmethod
    def getAIWeight():
        return int()

    @staticmethod
    def getAdvisorType():
        return int()

    @staticmethod
    def getAirCombat():
        return int()

    @staticmethod
    def getAirCombatLimit():
        return int()

    @staticmethod
    def getAirRange():
        return int()

    @staticmethod
    def getAirUnitCap():
        return int()

    @staticmethod
    def getAnimalCombatModifier():
        return int()

    @staticmethod
    def getArtInfo(i, eEra, eStyle):
        return CvArtInfoUnit()

    @staticmethod
    def getAssetValue():
        return int()

    @staticmethod
    def getBaseDiscover():
        return int()

    @staticmethod
    def getBaseHurry():
        return int()

    @staticmethod
    def getBaseTrade():
        return int()

    @staticmethod
    def getBombRate():
        return int()

    @staticmethod
    def getBombardRate():
        return int()

    @staticmethod
    def getBonusProductionModifier(i):
        return int()

    @staticmethod
    def getBuildings(i):
        return bool()

    @staticmethod
    def getBuilds(i):
        return bool()

    @staticmethod
    def getCargoSpace():
        return int()

    @staticmethod
    def getChanceFirstStrikes():
        return int()

    @staticmethod
    def getCityAttackModifier():
        return int()

    @staticmethod
    def getCityDefenseModifier():
        return int()

    @staticmethod
    def getCollateralDamage():
        return int()

    @staticmethod
    def getCollateralDamageLimit():
        return int()

    @staticmethod
    def getCollateralDamageMaxUnits():
        return int()

    @staticmethod
    def getCombat():
        return int()

    @staticmethod
    def getCombatLimit():
        return int()

    @staticmethod
    def getCommandType():
        return int()

    @staticmethod
    def getConscriptionValue():
        return int()

    @staticmethod
    def getCorporationSpreads(i):
        return int()

    @staticmethod
    def getCultureGarrisonValue():
        return int()

    @staticmethod
    def getDefaultUnitAIType():
        return int()

    @staticmethod
    def getDefenderUnitClass(i):
        return bool()

    @staticmethod
    def getDefenderUnitCombat(i):
        return bool()

    @staticmethod
    def getDiscoverMultiplier():
        return int()

    @staticmethod
    def getDomainCargo():
        return int()

    @staticmethod
    def getDomainModifier(i):
        return int()

    @staticmethod
    def getDomainType():
        return int()

    @staticmethod
    def getDropRange():
        return int()

    @staticmethod
    def getEarlyArtDefineTag(i, eStyle):
        return str()

    @staticmethod
    def getEvasionProbability():
        return int()

    @staticmethod
    def getExtraCost():
        return int()

    @staticmethod
    def getFeatureAttackModifier(i):
        return int()

    @staticmethod
    def getFeatureDefenseModifier(i):
        return int()

    @staticmethod
    def getFeatureImpassable(i):
        return bool()

    @staticmethod
    def getFeatureNative(i):
        return bool()

    @staticmethod
    def getFeaturePassableTech(i):
        return int()

    @staticmethod
    def getFirstStrikes():
        return int()

    @staticmethod
    def getFlankingStrikeUnitClass(i):
        return int()

    @staticmethod
    def getFlavorValue(i):
        return int()

    @staticmethod
    def getForceBuildings(i):
        return bool()

    @staticmethod
    def getFreePromotions(i):
        return bool()

    @staticmethod
    def getGreatPeoples(i):
        return bool()

    @staticmethod
    def getGreatWorkCulture():
        return int()

    @staticmethod
    def getGroupDefinitions():
        return int()

    @staticmethod
    def getGroupSize():
        return int()

    @staticmethod
    def getHillsAttackModifier():
        return int()

    @staticmethod
    def getHillsDefenseModifier():
        return int()

    @staticmethod
    def getHolyCity():
        return int()

    @staticmethod
    def getHurryCostModifier():
        return int()

    @staticmethod
    def getHurryMultiplier():
        return int()

    @staticmethod
    def getInterceptionProbability():
        return int()

    @staticmethod
    def getInvisibleType():
        return int()

    @staticmethod
    def getLateArtDefineTag(i, eStyle):
        return str()

    @staticmethod
    def getLeaderExperience():
        return int()

    @staticmethod
    def getLeaderPromotion():
        return int()

    @staticmethod
    def getMeleeWaveSize():
        return int()

    @staticmethod
    def getMiddleArtDefineTag(i, eStyle):
        return str()

    @staticmethod
    def getMinAreaSize():
        return int()

    @staticmethod
    def getMoves():
        return int()

    @staticmethod
    def getNotUnitAIType(i):
        return bool()

    @staticmethod
    def getNukeRange():
        return int()

    @staticmethod
    def getNumSeeInvisibleTypes():
        return int()

    @staticmethod
    def getNumUnitNames():
        return int()

    @staticmethod
    def getPowerValue():
        return int()

    @staticmethod
    def getPrereqAndBonus():
        return int()

    @staticmethod
    def getPrereqAndTech():
        return int()

    @staticmethod
    def getPrereqAndTechs(i):
        return int()

    @staticmethod
    def getPrereqBuilding():
        return int()

    @staticmethod
    def getPrereqCorporation():
        return int()

    @staticmethod
    def getPrereqOrBonuses(i):
        return int()

    @staticmethod
    def getPrereqReligion():
        return int()

    @staticmethod
    def getProductionCost():
        return int()

    @staticmethod
    def getProductionTraits(i):
        return int()

    @staticmethod
    def getRangedWaveSize():
        return int()

    @staticmethod
    def getReligionSpreads(i):
        return int()

    @staticmethod
    def getReligionType():
        return int()

    @staticmethod
    def getSeeInvisibleType(i):
        return int()

    @staticmethod
    def getSpecialCargo():
        return int()

    @staticmethod
    def getSpecialUnitType():
        return int()

    @staticmethod
    def getStateReligion():
        return int()

    @staticmethod
    def getTargetUnitClass(i):
        return bool()

    @staticmethod
    def getTargetUnitCombat(i):
        return bool()

    @staticmethod
    def getTerrainAttackModifier(i):
        return int()

    @staticmethod
    def getTerrainDefenseModifier(i):
        return int()

    @staticmethod
    def getTerrainImpassable(i):
        return bool()

    @staticmethod
    def getTerrainNative(i):
        return bool()

    @staticmethod
    def getTerrainPassableTech(i):
        return int()

    @staticmethod
    def getTradeMultiplier():
        return int()

    @staticmethod
    def getUnitAIType(i):
        return bool()

    @staticmethod
    def getUnitCaptureClassType():
        return int()

    @staticmethod
    def getUnitClassAttackModifier(i):
        return int()

    @staticmethod
    def getUnitClassDefenseModifier(i):
        return int()

    @staticmethod
    def getUnitClassType():
        return int()

    @staticmethod
    def getUnitCombatModifier(i):
        return int()

    @staticmethod
    def getUnitCombatType():
        return int()

    @staticmethod
    def getUnitGroupRequired(i):
        return int()

    @staticmethod
    def getUnitMaxSpeed():
        return float()

    @staticmethod
    def getUnitNames(i):
        return str()

    @staticmethod
    def getUnitPadTime():
        return float()

    @staticmethod
    def getUpgradeUnitClass(i):
        return bool()

    @staticmethod
    def getWithdrawalProbability():
        return int()

    @staticmethod
    def getWorkRate():
        return int()

    @staticmethod
    def getXPValueAttack():
        return int()

    @staticmethod
    def getXPValueDefense():
        return int()

    @staticmethod
    def isAlwaysHostile():
        return bool()

    @staticmethod
    def isAnimal():
        return bool()

    @staticmethod
    def isCanMoveAllTerrain():
        return bool()

    @staticmethod
    def isCanMoveImpassable():
        return bool()

    @staticmethod
    def isCounterSpy():
        return bool()

    @staticmethod
    def isDestroy():
        return bool()

    @staticmethod
    def isFirstStrikeImmune():
        return bool()

    @staticmethod
    def isFlatMovementCost():
        return bool()

    @staticmethod
    def isFoodProduction():
        return bool()

    @staticmethod
    def isFound():
        return bool()

    @staticmethod
    def isGoldenAge():
        return bool()

    @staticmethod
    def isHiddenNationality():
        return bool()

    @staticmethod
    def isIgnoreBuildingDefense():
        return bool()

    @staticmethod
    def isIgnoreTerrainCost():
        return bool()

    @staticmethod
    def isInvestigate():
        return bool()

    @staticmethod
    def isInvisible():
        return bool()

    @staticmethod
    def isLineOfSight():
        return bool()

    @staticmethod
    def isMechUnit():
        return bool()

    @staticmethod
    def isMilitaryHappiness():
        return bool()

    @staticmethod
    def isMilitaryProduction():
        return bool()

    @staticmethod
    def isMilitarySupport():
        return bool()

    @staticmethod
    def isNoBadGoodies():
        return bool()

    @staticmethod
    def isNoCapture():
        return bool()

    @staticmethod
    def isNoDefensiveBonus():
        return bool()

    @staticmethod
    def isNukeImmune():
        return bool()

    @staticmethod
    def isPillage():
        return bool()

    @staticmethod
    def isPrereqBonuses():
        return bool()

    @staticmethod
    def isPrereqReligion():
        return bool()

    @staticmethod
    def isRenderBelowWater():
        return bool()

    @staticmethod
    def isRivalTerritory():
        return bool()

    @staticmethod
    def isSabotage():
        return bool()

    @staticmethod
    def isSpy():
        return bool()

    @staticmethod
    def isStealPlans():
        return bool()

    @staticmethod
    def isSuicide():
        return bool()

    @staticmethod
    def setCombat(iNum):
        pass

    @staticmethod
    def setInvisible(bEnable):
        pass


class CvUpkeepInfo(CvInfoBase):

    @staticmethod
    def getCityPercent():
        return int()

    @staticmethod
    def getPopulationPercent():
        return int()


class CvVictoryInfo(CvInfoBase):

    @staticmethod
    def getCityCulture():
        return int()

    @staticmethod
    def getLandPercent():
        return int()

    @staticmethod
    def getMinLandPercent():
        return int()

    @staticmethod
    def getMovie():
        return str()

    @staticmethod
    def getNumCultureCities():
        return int()

    @staticmethod
    def getPopulationPercentLead():
        return int()

    @staticmethod
    def getReligionPercent():
        return int()

    @staticmethod
    def getTotalCultureRatio():
        return int()

    @staticmethod
    def getVictoryDelayTurns():
        return int()

    @staticmethod
    def isConquest():
        return bool()

    @staticmethod
    def isDiploVote():
        return bool()

    @staticmethod
    def isEndScore():
        return bool()

    @staticmethod
    def isPermanent():
        return bool()

    @staticmethod
    def isTargetScore():
        return bool()


class CvVoteInfo(CvInfoBase):

    @staticmethod
    def getMinVoters():
        return int()

    @staticmethod
    def getPopulationThreshold():
        return int()

    @staticmethod
    def getStateReligionVotePercent():
        return int()

    @staticmethod
    def getTradeRoutes():
        return int()

    @staticmethod
    def isAssignCity():
        return bool()

    @staticmethod
    def isCityVoting():
        return bool()

    @staticmethod
    def isCivVoting():
        return bool()

    @staticmethod
    def isDefensivePact():
        return bool()

    @staticmethod
    def isForceCivic(i):
        return bool()

    @staticmethod
    def isForceNoTrade():
        return bool()

    @staticmethod
    def isForcePeace():
        return bool()

    @staticmethod
    def isForceWar():
        return bool()

    @staticmethod
    def isFreeTrade():
        return bool()

    @staticmethod
    def isNoNukes():
        return bool()

    @staticmethod
    def isOpenBorders():
        return bool()

    @staticmethod
    def isSecretaryGeneral():
        return bool()

    @staticmethod
    def isVictory():
        return bool()

    @staticmethod
    def isVoteSourceType(i):
        return bool()


class CvVoteSourceInfo(CvInfoBase):

    @staticmethod
    def getCivic():
        return int()

    @staticmethod
    def getFreeSpecialist():
        return int()

    @staticmethod
    def getReligionCommerce(i):
        return int()

    @staticmethod
    def getReligionYield(i):
        return int()

    @staticmethod
    def getSecretaryGeneralText():
        return str()

    @staticmethod
    def getVoteInterval():
        return int()


class CvWorldInfo(CvInfoBase):

    @staticmethod
    def getBuildingClassPrereqModifier():
        return int()

    @staticmethod
    def getColonyMaintenancePercent():
        return int()

    @staticmethod
    def getCorporationMaintenancePercent():
        return int()

    @staticmethod
    def getDefaultPlayers():
        return int()

    @staticmethod
    def getDistanceMaintenancePercent():
        return int()

    @staticmethod
    def getFeatureGrainChange():
        return int()

    @staticmethod
    def getGridHeight():
        return int()

    @staticmethod
    def getGridWidth():
        return int()

    @staticmethod
    def getMaxConscriptModifier():
        return int()

    @staticmethod
    def getNumCitiesAnarchyPercent():
        return int()

    @staticmethod
    def getNumCitiesMaintenancePercent():
        return int()

    @staticmethod
    def getNumFreeBuildingBonuses():
        return int()

    @staticmethod
    def getResearchPercent():
        return int()

    @staticmethod
    def getTargetNumCities():
        return int()

    @staticmethod
    def getTerrainGrainChange():
        return int()

    @staticmethod
    def getTradeProfitPercent():
        return int()

    @staticmethod
    def getUnitNameModifier():
        return int()

    @staticmethod
    def getWarWearinessModifier():
        return int()


class CvYieldInfo(CvInfoBase):

    @staticmethod
    def getAIWeightPercent():
        return int()

    @staticmethod
    def getChar():
        return int()

    @staticmethod
    def getCityChange():
        return int()

    @staticmethod
    def getColorType():
        return int()

    @staticmethod
    def getGoldenAgeYield():
        return int()

    @staticmethod
    def getGoldenAgeYieldThreshold():
        return int()

    @staticmethod
    def getHillsChange():
        return int()

    @staticmethod
    def getLakeChange():
        return int()

    @staticmethod
    def getMinCity():
        return int()

    @staticmethod
    def getPeakChange():
        return int()

    @staticmethod
    def getPopulationChangeDivisor():
        return int()

    @staticmethod
    def getPopulationChangeOffset():
        return int()

    @staticmethod
    def getTradeModifier():
        return int()


class CyArea:

    @staticmethod
    def calculateTotalBestNatureYield():
        return int()

    @staticmethod
    def countCoastalLand():
        return int()

    @staticmethod
    def countHasCorporation(eCorporation, eOwner):
        return int()

    @staticmethod
    def countHasReligion(eReligion, eOwner):
        return int()

    @staticmethod
    def countNumUniqueBonusTypes():
        return int()

    @staticmethod
    def getAnimalsPerPlayer(eIndex):
        return int()

    @staticmethod
    def getAreaAIType(eIndex):
        return -1  # Type

    @staticmethod
    def getBestFoundValue(eIndex):
        return int()

    @staticmethod
    def getBuildingBadHealth(eIndex):
        return int()

    @staticmethod
    def getBuildingGoodHealth(eIndex):
        return int()

    @staticmethod
    def getBuildingHappiness(eIndex):
        return int()

    @staticmethod
    def getCitiesPerPlayer(eIndex):
        return int()

    @staticmethod
    def getFreeSpecialist(eIndex):
        return int()

    @staticmethod
    def getID():
        return int()

    @staticmethod
    def getNumAIUnits(eIndex1, eIndex2):
        return int()

    @staticmethod
    def getNumBonuses(eBonus):
        return int()

    @staticmethod
    def getNumCities():
        return int()

    @staticmethod
    def getNumImprovements(eImprovement):
        return int()

    @staticmethod
    def getNumOwnedTiles():
        return int()

    @staticmethod
    def getNumRevealedTiles(eIndex):
        return int()

    @staticmethod
    def getNumRiverEdges():
        return int()

    @staticmethod
    def getNumStartingPlots():
        return int()

    @staticmethod
    def getNumTiles():
        return int()

    @staticmethod
    def getNumTotalBonuses():
        return int()

    @staticmethod
    def getNumTrainAIUnits(eIndex1, eIndex2):
        return int()

    @staticmethod
    def getNumUnits():
        return int()

    @staticmethod
    def getNumUnownedTiles():
        return int()

    @staticmethod
    def getNumUnrevealedTiles(eIndex):
        return int()

    @staticmethod
    def getPopulationPerPlayer(eIndex):
        return int()

    @staticmethod
    def getPower(eIndex):
        return int()

    @staticmethod
    def getTargetCity(eIndex):
        return CyCity()

    @staticmethod
    def getTotalPopulation():
        return int()

    @staticmethod
    def getUnitsPerPlayer(eIndex):
        return int()

    @staticmethod
    def getYieldRateModifier(eIndex1, eIndex2):
        return int()

    @staticmethod
    def isBorderObstacle(eIndex):
        return bool()

    @staticmethod
    def isCleanPower(eIndex):
        return bool()

    @staticmethod
    def isLake():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isWater():
        return bool()


class CyArtFileMgr:

    @staticmethod
    def Reset():
        pass

    @staticmethod
    def buildArtFileInfoMaps():
        pass

    @staticmethod
    def getBonusArtInfo(szArtDefineTag):
        return CvArtInfoBonus()

    @staticmethod
    def getBuildingArtInfo(szArtDefineTag):
        return CvArtInfoBuilding()

    @staticmethod
    def getCivilizationArtInfo(szArtDefineTag):
        return CvArtInfoCivilization()

    @staticmethod
    def getFeatureArtInfo(szArtDefineTag):
        return CvArtInfoFeature()

    @staticmethod
    def getImprovementArtInfo(szArtDefineTag):
        return CvArtInfoImprovement()

    @staticmethod
    def getInterfaceArtInfo(szArtDefineTag):
        return CvArtInfoInterface()

    @staticmethod
    def getLeaderheadArtInfo(szArtDefineTag):
        return CvArtInfoLeaderhead()

    @staticmethod
    def getMiscArtInfo(szArtDefineTag):
        return CvArtInfoMisc()

    @staticmethod
    def getMovieArtInfo(szArtDefineTag):
        return CvArtInfoMovie()

    @staticmethod
    def getTerrainArtInfo(szArtDefineTag):
        return CvArtInfoTerrain()

    @staticmethod
    def getUnitArtInfo(szArtDefineTag):
        return CvArtInfoUnit()

    @staticmethod
    def isNone():
        return bool()


class CyAudioGame:

    @staticmethod
    def Destroy2DSound(soundhandle):
        pass

    @staticmethod
    def Destroy3DSound(soundhandle):
        pass

    @staticmethod
    def Is2DSoundPlaying(soundhandle):
        return bool()

    @staticmethod
    def Is3DSoundPlaying(soundhandle):
        return bool()

    @staticmethod
    def Play2DSound(scriptname):
        return int()

    @staticmethod
    def Play2DSoundWithId(scriptId):
        return int()

    @staticmethod
    def Play3DSound(scriptname, x, y, z):
        return int()

    @staticmethod
    def Play3DSoundWithId(scriptId, x, y, z):
        return int()

    @staticmethod
    def Set2DSoundVolume(soundhandle, volume):
        pass

    @staticmethod
    def Set3DSoundPosition(soundhandle, x, y, z):
        pass

    @staticmethod
    def Set3DSoundVolume(soundhandle, volume):
        pass


class CyCamera:

    @staticmethod
    def GetBasePitch():
        return float()

    @staticmethod
    def GetBaseTurn():
        return float()

    @staticmethod
    def GetCameraMovementSpeed():
        return float()

    @staticmethod
    def GetCurrentPosition():
        return NiPoint3(0, 0, 0)

    @staticmethod
    def GetDefaultViewPortCenter():
        return NiPoint2(0, 0)

    @staticmethod
    def GetDestinationPosition():
        return NiPoint3(0, 0, 0)

    @staticmethod
    def GetLookAt(pt3LookAt):
        pass

    @staticmethod
    def GetLookAtSpeed():
        return float()

    @staticmethod
    def GetTargetDestination():
        return NiPoint3(0, 0, 0)

    @staticmethod
    def GetZoom():
        return float()

    @staticmethod
    def JustLookAt(p3LookAt):
        pass

    @staticmethod
    def JustLookAtPlot(pPlot):
        pass

    @staticmethod
    def LookAt(pt3LookAt, CameraType, attackDirection):
        pass

    @staticmethod
    def LookAtUnit(unit):
        pass

    @staticmethod
    def MoveBaseTurnLeft(increment):
        pass

    @staticmethod
    def MoveBaseTurnRight(increment):
        pass

    @staticmethod
    def ReleaseLockedCamera():
        pass

    @staticmethod
    def ResetZoom():
        pass

    @staticmethod
    def SetBasePitch(fBasePitch):
        pass

    @staticmethod
    def SetBaseTurn(baseTurn):
        pass

    @staticmethod
    def SetCameraMovementSpeed(eSpeed):
        pass

    @staticmethod
    def SetCurrentPosition(point):
        pass

    @staticmethod
    def SetDestinationPosition(point):
        pass

    @staticmethod
    def SetLookAtSpeed(fSpeed):
        pass

    @staticmethod
    def SetTargetDestination(point):
        pass

    @staticmethod
    def SetViewPortCenter(pt2Center):
        pass

    @staticmethod
    def SetZoom(zoom):
        pass

    @staticmethod
    def SimpleLookAt(position, target):
        pass

    @staticmethod
    def Translate(translation):
        pass

    @staticmethod
    def ZoomIn(increment):
        pass

    @staticmethod
    def ZoomOut(increment):
        pass

    @staticmethod
    def isMoving():
        return bool()

    @staticmethod
    def setOrthoCamera(bNewValue):
        pass


class CyCity:

    @staticmethod
    def AI_avoidGrowth():
        return bool()

    @staticmethod
    def AI_cityValue():
        return int()

    @staticmethod
    def AI_countBestBuilds(pArea):
        return int()

    @staticmethod
    def AI_isEmphasize(iEmphasizeType):
        return bool()

    @staticmethod
    def addProductionExperience(pUnit, bConscript):
        pass

    @staticmethod
    def allUpgradesAvailable(eUnit, iUpgradeCount):
        return -1  # Type

    @staticmethod
    def alterSpecialistCount(eIndex, iChange):
        pass

    @staticmethod
    def alterWorkingPlot(iIndex):
        pass

    @staticmethod
    def angryPopulation(iExtra):
        return int()

    @staticmethod
    def area():
        return CyArea()

    @staticmethod
    def at(iX, iY):
        return bool()

    @staticmethod
    def atPlot(pPlot):
        return bool()

    @staticmethod
    def badHealth(bNoAngry):
        return int()

    @staticmethod
    def calculateColonyMaintenance():
        return int()

    @staticmethod
    def calculateColonyMaintenanceTimes100():
        return int()

    @staticmethod
    def calculateCorporationMaintenance():
        return int()

    @staticmethod
    def calculateCorporationMaintenanceTimes100():
        return int()

    @staticmethod
    def calculateCulturePercent(eIndex):
        return int()

    @staticmethod
    def calculateDistanceMaintenance():
        return int()

    @staticmethod
    def calculateDistanceMaintenanceTimes100():
        return int()

    @staticmethod
    def calculateNumCitiesMaintenance():
        return int()

    @staticmethod
    def calculateNumCitiesMaintenanceTimes100():
        return int()

    @staticmethod
    def calculateTeamCulturePercent(eIndex):
        return int()

    @staticmethod
    def calculateTradeProfit(pCity):
        return int()

    @staticmethod
    def calculateTradeYield(eIndex, iTradeProfit):
        return int()

    @staticmethod
    def canConscript():
        return bool()

    @staticmethod
    def canConstruct(iBuilding, bContinue, bTestVisible, bIgnoreCost):
        return bool()

    @staticmethod
    def canContinueProduction(order):
        return bool()

    @staticmethod
    def canCreate(iProject, bContinue, bTestVisible):
        return bool()

    @staticmethod
    def canHurry(iHurry, bTestVisible):
        return bool()

    @staticmethod
    def canJoin():
        return bool()

    @staticmethod
    def canMaintain(iProcess, bContinue):
        return bool()

    @staticmethod
    def canTrain(iUnit, bContinue, bTestVisible):
        return bool()

    @staticmethod
    def canWork(pPlot):
        return bool()

    @staticmethod
    def changeBaseGreatPeopleRate(iChange):
        pass

    @staticmethod
    def changeBaseYieldRate(eIndex, iNewValue):
        pass

    @staticmethod
    def changeBuildingProduction(iIndex, iChange):
        pass

    @staticmethod
    def changeBuildingProductionTime(eIndex, iChange):
        pass

    @staticmethod
    def changeConscriptAngerTimer(iChange):
        pass

    @staticmethod
    def changeCulture(eIndex, iChange, bPlots):
        pass

    @staticmethod
    def changeCultureTimes100(eIndex, iChange, bPlots):
        pass

    @staticmethod
    def changeCultureUpdateTimer(iChange):
        pass

    @staticmethod
    def changeDefenseDamage(iChange):
        pass

    @staticmethod
    def changeDefyResolutionAngerTimer(iChange):
        pass

    @staticmethod
    def changeEspionageHappinessCounter(iChange):
        pass

    @staticmethod
    def changeEspionageHealthCounter(iChange):
        pass

    @staticmethod
    def changeExtraHappiness(iChange):
        pass

    @staticmethod
    def changeExtraHealth(iChange):
        pass

    @staticmethod
    def changeExtraTradeRoutes(iChange):
        pass

    @staticmethod
    def changeFood(iChange):
        pass

    @staticmethod
    def changeForceSpecialistCount(eIndex, iChange):
        pass

    @staticmethod
    def changeFreeBonus(eIndex, iChange):
        pass

    @staticmethod
    def changeFreeSpecialistCount(eIndex, iChange):
        pass

    @staticmethod
    def changeGreatPeopleProgress(iChange):
        pass

    @staticmethod
    def changeGreatPeopleUnitProgress(iIndex, iChange):
        pass

    @staticmethod
    def changeHappinessTimer(iChange):
        pass

    @staticmethod
    def changeHealRate(iChange):
        pass

    @staticmethod
    def changeHurryAngerTimer(iChange):
        pass

    @staticmethod
    def changeImprovementFreeSpecialists(iIndex, iChange):
        pass

    @staticmethod
    def changeNoBonusCount(eBonus, iChange):
        pass

    @staticmethod
    def changeOccupationTimer(iChange):
        pass

    @staticmethod
    def changePopulation(iChange):
        pass

    @staticmethod
    def changeProduction(iChange):
        pass

    @staticmethod
    def changeReligionInfluence(iIndex, iChange):
        pass

    @staticmethod
    def changeSpecialistCommerce(eIndex, iChange):
        pass

    @staticmethod
    def changeStateReligionHappiness(eIndex, iChange):
        pass

    @staticmethod
    def changeUnitProduction(iIndex, iChange):
        pass

    @staticmethod
    def chooseProduction(eTrainUnit, eConstructBuilding, eCreateProject, bFinish, bFront):
        pass

    @staticmethod
    def clearOrderQueue():
        pass

    @staticmethod
    def clearWorkingOverride(iIndex):
        pass

    @staticmethod
    def conscript():
        pass

    @staticmethod
    def conscriptMinCityPopulation():
        return int()

    @staticmethod
    def countNumImprovedPlots():
        return int()

    @staticmethod
    def countNumRiverPlots():
        return int()

    @staticmethod
    def countNumWaterPlots():
        return int()

    @staticmethod
    def countTotalCultureTimes100():
        return int()

    @staticmethod
    def createGreatPeople(eGreatPersonUnit, bIncrementThreshold, bIncrementExperience):
        pass

    @staticmethod
    def cultureDistance(iDX, iDY):
        return int()

    @staticmethod
    def cultureGarrison(ePlayer):
        return int()

    @staticmethod
    def cultureStrength(ePlayer):
        return int()

    @staticmethod
    def doTask(eTask, iData1, iData2, bOption):
        pass

    @staticmethod
    def extraFreeSpecialists():
        return int()

    @staticmethod
    def extraPopulation():
        return int()

    @staticmethod
    def extraSpecialists():
        return int()

    @staticmethod
    def findBaseYieldRateRank(eYield):
        return int()

    @staticmethod
    def findCommerceRateRank(eCommerce):
        return int()

    @staticmethod
    def findHighestCulture():
        return -1  # Type

    @staticmethod
    def findPopulationRank():
        return int()

    @staticmethod
    def findYieldRateRank(eYield):
        return int()

    @staticmethod
    def flatConscriptAngerLength():
        return int()

    @staticmethod
    def flatDefyResolutionAngerLength():
        return int()

    @staticmethod
    def flatHurryAngerLength():
        return int()

    @staticmethod
    def foodConsumption(bNoAngry, iExtra):
        return int()

    @staticmethod
    def foodDifference(bBottom):
        return int()

    @staticmethod
    def getAddedFreeSpecialistCount(eIndex):
        return int()

    @staticmethod
    def getAirModifier():
        return int()

    @staticmethod
    def getAirUnitCapacity(eTeam):
        return int()

    @staticmethod
    def getArtStyleType():
        return -1  # Type

    @staticmethod
    def getBaseCommerceRate(eIndex):
        return int()

    @staticmethod
    def getBaseCommerceRateTimes100(eIndex):
        return int()

    @staticmethod
    def getBaseGreatPeopleRate():
        return int()

    @staticmethod
    def getBaseYieldRate(eIndex):
        return int()

    @staticmethod
    def getBaseYieldRateModifier(eIndex, iExtra):
        return int()

    @staticmethod
    def getBonusBadHealth():
        return int()

    @staticmethod
    def getBonusGoodHappiness():
        return int()

    @staticmethod
    def getBonusGoodHealth():
        return int()

    @staticmethod
    def getBonusHappiness(iBonus):
        return int()

    @staticmethod
    def getBonusHealth(iBonus):
        return int()

    @staticmethod
    def getBonusPower(eBonus, bDirty):
        return int()

    @staticmethod
    def getBonusYieldRateModifier(eIndex, eBonus):
        return int()

    @staticmethod
    def getBuildingBadHappiness():
        return int()

    @staticmethod
    def getBuildingBadHealth():
        return int()

    @staticmethod
    def getBuildingBombardDefense():
        return int()

    @staticmethod
    def getBuildingCommerce(eIndex):
        return int()

    @staticmethod
    def getBuildingCommerceByBuilding(eIndex, iBuilding):
        return int()

    @staticmethod
    def getBuildingCommerceChange(eBuildingClass, eCommerce):
        return int()

    @staticmethod
    def getBuildingDefense():
        return int()

    @staticmethod
    def getBuildingGoodHappiness():
        return int()

    @staticmethod
    def getBuildingGoodHealth():
        return int()

    @staticmethod
    def getBuildingHappiness(iBuilding):
        return int()

    @staticmethod
    def getBuildingHappyChange(eBuildingClass):
        return int()

    @staticmethod
    def getBuildingHealth(iBuilding):
        return int()

    @staticmethod
    def getBuildingHealthChange(eBuildingClass):
        return int()

    @staticmethod
    def getBuildingOriginalOwner(iIndex):
        return int()

    @staticmethod
    def getBuildingOriginalTime(iIndex):
        return int()

    @staticmethod
    def getBuildingProduction(iIndex):
        return int()

    @staticmethod
    def getBuildingProductionModifier(iBuilding):
        return int()

    @staticmethod
    def getBuildingProductionTime(eIndex):
        return int()

    @staticmethod
    def getBuildingProductionTurnsLeft(iBuilding, iNum):
        return int()

    @staticmethod
    def getBuildingYieldChange(eBuildingClass, eYield):
        return int()

    @staticmethod
    def getCityIndexPlot(iIndex):
        return CyPlot()

    @staticmethod
    def getCityPlotIndex(pPlot):
        return int()

    @staticmethod
    def getCitySizeType():
        return -1  # Type

    @staticmethod
    def getCivilizationType():
        return -1  # Type

    @staticmethod
    def getCommerceFromPercent(eIndex, iYieldRate):
        return int()

    @staticmethod
    def getCommerceHappiness():
        return int()

    @staticmethod
    def getCommerceHappinessByType(eIndex):
        return int()

    @staticmethod
    def getCommerceHappinessPer(eIndex):
        return int()

    @staticmethod
    def getCommerceRate(eIndex):
        return int()

    @staticmethod
    def getCommerceRateModifier(eIndex):
        return int()

    @staticmethod
    def getCommerceRateTimes100(eIndex):
        return int()

    @staticmethod
    def getConscriptAngerTimer():
        return int()

    @staticmethod
    def getConscriptPopulation():
        return int()

    @staticmethod
    def getConscriptUnit():
        return -1  # Type

    @staticmethod
    def getCorporationCommerce(eIndex):
        return int()

    @staticmethod
    def getCorporationCommerceByCorporation(eIndex, iCorporation):
        return int()

    @staticmethod
    def getCorporationYield(eIndex):
        return int()

    @staticmethod
    def getCorporationYieldByCorporation(eIndex, iCorporation):
        return int()

    @staticmethod
    def getCulture(eIndex):
        return int()

    @staticmethod
    def getCultureLevel():
        return -1  # Type

    @staticmethod
    def getCulturePercentAnger():
        return int()

    @staticmethod
    def getCultureThreshold():
        return int()

    @staticmethod
    def getCultureTimes100(eIndex):
        return int()

    @staticmethod
    def getCultureUpdateTimer():
        return int()

    @staticmethod
    def getCurrAirlift():
        return int()

    @staticmethod
    def getCurrentProductionDifference(bIgnoreFood, bOverflow):
        return int()

    @staticmethod
    def getCurrentStateReligionHappiness():
        return int()

    @staticmethod
    def getDefenseDamage():
        return int()

    @staticmethod
    def getDefenseModifier(bIgnoreBuilding):
        return int()

    @staticmethod
    def getDefyResolutionAngerTimer():
        return int()

    @staticmethod
    def getDomainFreeExperience(eIndex):
        return int()

    @staticmethod
    def getDomainProductionModifier(eIndex):
        return int()

    @staticmethod
    def getEspionageDefenseModifier():
        return int()

    @staticmethod
    def getEspionageHappinessCounter():
        return int()

    @staticmethod
    def getEspionageHealthCounter():
        return int()

    @staticmethod
    def getEspionageVisibility(eIndex):
        return bool()

    @staticmethod
    def getExtraBuildingBadHappiness():
        return int()

    @staticmethod
    def getExtraBuildingGoodHappiness():
        return int()

    @staticmethod
    def getExtraHappiness():
        return int()

    @staticmethod
    def getExtraHealth():
        return int()

    @staticmethod
    def getExtraProductionDifference(iExtra):
        return int()

    @staticmethod
    def getExtraSpecialistYield(eIndex):
        return int()

    @staticmethod
    def getExtraSpecialistYieldOfType(eIndex, eSpecialist):
        return int()

    @staticmethod
    def getExtraTradeRoutes():
        return int()

    @staticmethod
    def getFeatureBadHappiness():
        return int()

    @staticmethod
    def getFeatureBadHealth():
        return int()

    @staticmethod
    def getFeatureGoodHappiness():
        return int()

    @staticmethod
    def getFeatureGoodHealth():
        return int()

    @staticmethod
    def getFeatureProduction():
        return int()

    @staticmethod
    def getFirstBuildingOrder(eBuilding):
        return int()

    @staticmethod
    def getFirstProjectOrder(eProject):
        return int()

    @staticmethod
    def getFirstUnitOrder(eUnit):
        return int()

    @staticmethod
    def getFood():
        return int()

    @staticmethod
    def getFoodKept():
        return int()

    @staticmethod
    def getFoodTurnsLeft():
        return int()

    @staticmethod
    def getForceSpecialistCount(eIndex):
        return int()

    @staticmethod
    def getForeignTradeRouteModifier():
        return int()

    @staticmethod
    def getFreeBonus(eIndex):
        return int()

    @staticmethod
    def getFreeExperience():
        return int()

    @staticmethod
    def getFreePromotionCount(eIndex):
        return int()

    @staticmethod
    def getFreeSpecialist():
        return int()

    @staticmethod
    def getFreeSpecialistCount(eIndex):
        return int()

    @staticmethod
    def getFreshWaterBadHealth():
        return int()

    @staticmethod
    def getFreshWaterGoodHealth():
        return int()

    @staticmethod
    def getGameTurnAcquired():
        return int()

    @staticmethod
    def getGameTurnFounded():
        return int()

    @staticmethod
    def getGeneralProductionTurnsLeft():
        return int()

    @staticmethod
    def getGreatPeopleProgress():
        return int()

    @staticmethod
    def getGreatPeopleRate():
        return int()

    @staticmethod
    def getGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getGreatPeopleUnitProgress(iIndex):
        return int()

    @staticmethod
    def getGreatPeopleUnitRate(iIndex):
        return int()

    @staticmethod
    def getHandicapType():
        return -1  # Type

    @staticmethod
    def getHappinessTimer():
        return int()

    @staticmethod
    def getHighestPopulation():
        return int()

    @staticmethod
    def getHurryAngerModifier():
        return int()

    @staticmethod
    def getHurryAngerTimer():
        return int()

    @staticmethod
    def getID():
        return int()

    @staticmethod
    def getImprovementFreeSpecialists(iIndex):
        return int()

    @staticmethod
    def getLargestCityHappiness():
        return int()

    @staticmethod
    def getLiberationPlayer(bConquest):
        return int()

    @staticmethod
    def getMaintenance():
        return int()

    @staticmethod
    def getMaintenanceModifier():
        return int()

    @staticmethod
    def getMaintenanceTimes100():
        return int()

    @staticmethod
    def getMaxAirlift():
        return int()

    @staticmethod
    def getMaxFoodKeptPercent():
        return int()

    @staticmethod
    def getMaxSpecialistCount(eIndex):
        return int()

    @staticmethod
    def getMilitaryHappiness():
        return int()

    @staticmethod
    def getMilitaryHappinessUnits():
        return int()

    @staticmethod
    def getMilitaryProductionModifier():
        return int()

    @staticmethod
    def getName():
        return str()

    @staticmethod
    def getNameForm(iForm):
        return str()

    @staticmethod
    def getNameKey():
        return str()

    @staticmethod
    def getNaturalDefense():
        return int()

    @staticmethod
    def getNoMilitaryPercentAnger():
        return int()

    @staticmethod
    def getNukeModifier():
        return int()

    @staticmethod
    def getNumActiveBuilding(iIndex):
        return int()

    @staticmethod
    def getNumBonuses(iBonus):
        return int()

    @staticmethod
    def getNumBuilding(iIndex):
        return int()

    @staticmethod
    def getNumBuildings():
        return int()

    @staticmethod
    def getNumFreeBuilding(iIndex):
        return int()

    @staticmethod
    def getNumGreatPeople():
        return int()

    @staticmethod
    def getNumNationalWonders():
        return int()

    @staticmethod
    def getNumRealBuilding(iIndex):
        return int()

    @staticmethod
    def getNumTeamWonders():
        return int()

    @staticmethod
    def getNumWorldWonders():
        return int()

    @staticmethod
    def getOccupationTimer():
        return int()

    @staticmethod
    def getOrderQueueLength():
        return int()

    @staticmethod
    def getOriginalOwner():
        return -1  # Type

    @staticmethod
    def getOvercrowdingPercentAnger(iExtra):
        return int()

    @staticmethod
    def getOverflowProduction():
        return int()

    @staticmethod
    def getOwner():
        return -1  # Type

    @staticmethod
    def getPersonalityType():
        return -1  # Type

    @staticmethod
    def getPopulation():
        return int()

    @staticmethod
    def getPowerBadHealth():
        return int()

    @staticmethod
    def getPowerGoodHealth():
        return int()

    @staticmethod
    def getPreviousOwner():
        return -1  # Type

    @staticmethod
    def getProduction():
        return int()

    @staticmethod
    def getProductionBuilding():
        return -1  # Type

    @staticmethod
    def getProductionExperience(eUnit):
        return int()

    @staticmethod
    def getProductionModifier():
        return int()

    @staticmethod
    def getProductionName():
        return str()

    @staticmethod
    def getProductionNameKey():
        return str()

    @staticmethod
    def getProductionNeeded():
        return int()

    @staticmethod
    def getProductionProcess():
        return -1  # Type

    @staticmethod
    def getProductionProject():
        return -1  # Type

    @staticmethod
    def getProductionToCommerceModifier(eIndex):
        return int()

    @staticmethod
    def getProductionTurnsLeft():
        return int()

    @staticmethod
    def getProductionUnit():
        return -1  # Type

    @staticmethod
    def getProductionUnitAI():
        return -1  # Type

    @staticmethod
    def getProjectProductionModifier():
        return int()

    @staticmethod
    def getProjectProductionTurnsLeft(eProject, iNum):
        return int()

    @staticmethod
    def getRallyPlot():
        return CyPlot()

    @staticmethod
    def getRealPopulation():
        return int()

    @staticmethod
    def getReligionBadHappiness():
        return int()

    @staticmethod
    def getReligionCommerce(eIndex):
        return int()

    @staticmethod
    def getReligionCommerceByReligion(eIndex, iReligion):
        return int()

    @staticmethod
    def getReligionGoodHappiness():
        return int()

    @staticmethod
    def getReligionHappiness(iReligion):
        return int()

    @staticmethod
    def getReligionInfluence(iIndex):
        return int()

    @staticmethod
    def getReligionPercentAnger():
        return int()

    @staticmethod
    def getRiverPlotYield(eIndex):
        return int()

    @staticmethod
    def getScriptData():
        return str()

    @staticmethod
    def getSeaPlotYield(eIndex):
        return int()

    @staticmethod
    def getSpaceProductionModifier():
        return int()

    @staticmethod
    def getSpecialistCommerce(eIndex):
        return int()

    @staticmethod
    def getSpecialistCount(eIndex):
        return int()

    @staticmethod
    def getSpecialistFreeExperience():
        return int()

    @staticmethod
    def getSpecialistPopulation():
        return int()

    @staticmethod
    def getStateReligionHappiness(eIndex):
        return int()

    @staticmethod
    def getTeam():
        return -1  # Type

    @staticmethod
    def getTotalCommerceRateModifier(eIndex):
        return int()

    @staticmethod
    def getTotalDefense(bIgnoreBuilding):
        return int()

    @staticmethod
    def getTotalGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getTradeCity(iIndex):
        return CyCity()

    @staticmethod
    def getTradeRouteModifier():
        return int()

    @staticmethod
    def getTradeRoutes():
        return int()

    @staticmethod
    def getTradeYield(eIndex):
        return int()

    @staticmethod
    def getUnitCombatFreeExperience(eIndex):
        return int()

    @staticmethod
    def getUnitProduction(iIndex):
        return int()

    @staticmethod
    def getUnitProductionModifier(iUnit):
        return int()

    @staticmethod
    def getUnitProductionTurnsLeft(iUnit, iNum):
        return int()

    @staticmethod
    def getWallOverridePoints():
        return tuple()

    @staticmethod
    def getWarWearinessModifier():
        return int()

    @staticmethod
    def getWarWearinessPercentAnger():
        return int()

    @staticmethod
    def getWorkingPopulation():
        return int()

    @staticmethod
    def getX():
        return int()

    @staticmethod
    def getY():
        return int()

    @staticmethod
    def getYieldRate(eIndex):
        return int()

    @staticmethod
    def getYieldRateModifier(eIndex):
        return int()

    @staticmethod
    def goodHealth():
        return int()

    @staticmethod
    def growthThreshold():
        return int()

    @staticmethod
    def happyLevel():
        return int()

    @staticmethod
    def hasBonus(iBonus):
        return bool()

    @staticmethod
    def hasTrait(iTrait):
        return bool()

    @staticmethod
    def healthRate(bNoAngry, iExtra):
        return int()

    @staticmethod
    def hurry(iHurry):
        pass

    @staticmethod
    def hurryAngerLength(iHurry):
        return int()

    @staticmethod
    def hurryCost(bExtra):
        return int()

    @staticmethod
    def hurryGold(iHurry):
        return int()

    @staticmethod
    def hurryPopulation(iHurry):
        return int()

    @staticmethod
    def hurryProduction(iHurry):
        return int()

    @staticmethod
    def isActiveCorporation(eCorporation):
        return bool()

    @staticmethod
    def isAirliftTargeted():
        return bool()

    @staticmethod
    def isAreaCleanPower():
        return bool()

    @staticmethod
    def isBarbarian():
        return bool()

    @staticmethod
    def isBombardable(pUnit):
        return bool()

    @staticmethod
    def isBombarded():
        return bool()

    @staticmethod
    def isBuildingOnlyHealthy():
        return bool()

    @staticmethod
    def isBuildingsMaxed():
        return bool()

    @staticmethod
    def isCapital():
        return bool()

    @staticmethod
    def isCitizensAutomated():
        return bool()

    @staticmethod
    def isCoastal(iMinWaterSize):
        return bool()

    @staticmethod
    def isConnectedTo(pCity):
        return bool()

    @staticmethod
    def isConnectedToCapital(ePlayer):
        return bool()

    @staticmethod
    def isDirtyPower():
        return bool()

    @staticmethod
    def isDisorder():
        return bool()

    @staticmethod
    def isDrafted():
        return bool()

    @staticmethod
    def isEverOwned(eIndex):
        return bool()

    @staticmethod
    def isFoodProduction():
        return bool()

    @staticmethod
    def isFreePromotion(eIndex):
        return bool()

    @staticmethod
    def isGovernmentCenter():
        return bool()

    @staticmethod
    def isHasBuilding(iIndex):
        return bool()

    @staticmethod
    def isHasCorporation(iIndex):
        return bool()

    @staticmethod
    def isHasReligion(iIndex):
        return bool()

    @staticmethod
    def isHeadquarters():
        return bool()

    @staticmethod
    def isHeadquartersByType(iIndex):
        return bool()

    @staticmethod
    def isHolyCity():
        return bool()

    @staticmethod
    def isHolyCityByType(iIndex):
        return bool()

    @staticmethod
    def isHuman():
        return bool()

    @staticmethod
    def isNationalWondersMaxed():
        return bool()

    @staticmethod
    def isNeverLost():
        return bool()

    @staticmethod
    def isNoBonus(eBonus):
        return bool()

    @staticmethod
    def isNoUnhappiness():
        return bool()

    @staticmethod
    def isNoUnhealthyPopulation():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isOccupation():
        return bool()

    @staticmethod
    def isPlundered():
        return bool()

    @staticmethod
    def isPower():
        return bool()

    @staticmethod
    def isProduction():
        return bool()

    @staticmethod
    def isProductionAutomated():
        return bool()

    @staticmethod
    def isProductionBuilding():
        return bool()

    @staticmethod
    def isProductionLimited():
        return bool()

    @staticmethod
    def isProductionProcess():
        return bool()

    @staticmethod
    def isProductionProject():
        return bool()

    @staticmethod
    def isProductionUnit():
        return bool()

    @staticmethod
    def isRevealed(eIndex, bDebug):
        return bool()

    @staticmethod
    def isSpecialistForced():
        return bool()

    @staticmethod
    def isSpecialistValid(eIndex, iExtra):
        return bool()

    @staticmethod
    def isTeamWondersMaxed():
        return bool()

    @staticmethod
    def isTradeRoute(eIndex):
        return bool()

    @staticmethod
    def isUnitFoodProduction(iUnit):
        return bool()

    @staticmethod
    def isVisible(eTeam, bDebug):
        return bool()

    @staticmethod
    def isWallOverride():
        return bool()

    @staticmethod
    def isWorkingPlot(pPlot):
        return bool()

    @staticmethod
    def isWorkingPlotByIndex(iIndex):
        return bool()

    @staticmethod
    def isWorldWondersMaxed():
        return bool()

    @staticmethod
    def kill():
        pass

    @staticmethod
    def liberate(bConquest):
        pass

    @staticmethod
    def maxHurryPopulation():
        return int()

    @staticmethod
    def plot():
        return CyPlot()

    @staticmethod
    def popOrder(iNum, bFinish, bChoose):
        pass

    @staticmethod
    def productionLeft():
        return int()

    @staticmethod
    def pushOrder(eOrder, iData1, iData2, bSave, bPop, bAppend, bForce):
        pass

    @staticmethod
    def setAirliftTargeted(iNewValue):
        pass

    @staticmethod
    def setBaseYieldRate(eIndex, iNewValue):
        pass

    @staticmethod
    def setBombarded(iNewValue):
        pass

    @staticmethod
    def setBuildingCommerceChange(eBuildingClass, eCommerce, iChange):
        pass

    @staticmethod
    def setBuildingHappyChange(eBuildingClass, iChange):
        pass

    @staticmethod
    def setBuildingHealthChange(eBuildingClass, iChange):
        pass

    @staticmethod
    def setBuildingProduction(iIndex, iNewValue):
        pass

    @staticmethod
    def setBuildingProductionTime(eIndex, iNewValue):
        pass

    @staticmethod
    def setBuildingYieldChange(eBuildingClass, eYield, iChange):
        pass

    @staticmethod
    def setCitizensAutomated(bNewValue):
        pass

    @staticmethod
    def setCitySizeBoost(iBoost):
        pass

    @staticmethod
    def setCulture(eIndex, iNewValue, bPlots):
        pass

    @staticmethod
    def setCultureTimes100(eIndex, iNewValue, bPlots):
        pass

    @staticmethod
    def setDrafted(iNewValue):
        pass

    @staticmethod
    def setFeatureProduction(iNewValue):
        pass

    @staticmethod
    def setFood(iNewValue):
        pass

    @staticmethod
    def setForceSpecialistCount(eIndex, iNewValue):
        pass

    @staticmethod
    def setFreeSpecialistCount(eIndex, iNewValue):
        pass

    @staticmethod
    def setGreatPeopleUnitProgress(iIndex, iNewValue):
        pass

    @staticmethod
    def setHasCorporation(iIndex, bNewValue, bAnnounce, bArrows):
        pass

    @staticmethod
    def setHasReligion(iIndex, bNewValue, bAnnounce, bArrows):
        pass

    @staticmethod
    def setHighestPopulation(iNewValue):
        pass

    @staticmethod
    def setName(szNewValue, bFound):
        pass

    @staticmethod
    def setNeverLost(iNewValue):
        pass

    @staticmethod
    def setNumRealBuilding(iIndex, iNewValue):
        pass

    @staticmethod
    def setOccupationTimer(iNewValue):
        pass

    @staticmethod
    def setOverflowProduction(iNewValue):
        pass

    @staticmethod
    def setPlundered(bNewValue):
        pass

    @staticmethod
    def setPopulation(iNewValue):
        pass

    @staticmethod
    def setProduction(iNewValue):
        pass

    @staticmethod
    def setProductionAutomated(bNewValue):
        pass

    @staticmethod
    def setRevealed(eIndex, bNewValue):
        pass

    @staticmethod
    def setScriptData(szNewValue):
        pass

    @staticmethod
    def setUnitProduction(iIndex, iNewValue):
        pass

    @staticmethod
    def setWallOverride(bOverride):
        pass

    @staticmethod
    def setWallOverridePoints(kPoints):
        pass

    @staticmethod
    def totalBadBuildingHealth():
        return int()

    @staticmethod
    def totalFreeSpecialists():
        return int()

    @staticmethod
    def totalGoodBuildingHealth():
        return int()

    @staticmethod
    def totalTradeModifier():
        return int()

    @staticmethod
    def unhappyLevel(iExtra):
        return int()

    @staticmethod
    def unhealthyPopulation(bNoAngry, iExtra):
        return int()

    @staticmethod
    def visiblePopulation():
        return int()

    @staticmethod
    def waterArea():
        return CyArea()


class CyDeal:

    @staticmethod
    def getFirstPlayer():
        return int()

    @staticmethod
    def getFirstTrade(i):
        return TradeData()

    @staticmethod
    def getID():
        return int()

    @staticmethod
    def getInitialGameTurn():
        return int()

    @staticmethod
    def getLengthFirstTrades():
        return int()

    @staticmethod
    def getLengthSecondTrades():
        return int()

    @staticmethod
    def getSecondPlayer():
        return int()

    @staticmethod
    def getSecondTrade(i):
        return TradeData()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def kill():
        pass


class CyDiplomacy:

    @staticmethod
    def addUserComment(eComment, iData1, iData2, szString, txtArgs):
        pass

    @staticmethod
    def atWar():
        return bool()

    @staticmethod
    def clearUserComments():
        pass

    @staticmethod
    def closeScreen():
        pass

    @staticmethod
    def counterPropose():
        return bool()

    @staticmethod
    def declareWar():
        pass

    @staticmethod
    def diploEvent(iDiploEvent, iData1, iData2):
        pass

    @staticmethod
    def endTrade():
        pass

    @staticmethod
    def getData():
        return int()

    @staticmethod
    def getOpponentCivName():
        return str()

    @staticmethod
    def getOpponentName():
        return str()

    @staticmethod
    def getOurCivName():
        return str()

    @staticmethod
    def getOurName():
        return str()

    @staticmethod
    def getOurScore():
        return int()

    @staticmethod
    def getPlayerTradeOffer(iIndex):
        return TradeData()

    @staticmethod
    def getTheirScore():
        return int()

    @staticmethod
    def getTheirTradeOffer(iIndex):
        return TradeData()

    @staticmethod
    def getWhoTradingWith():
        return -1  # Type

    @staticmethod
    def hasAnnualDeal():
        return bool()

    @staticmethod
    def implementDeal():
        pass

    @staticmethod
    def isAIOffer():
        return bool()

    @staticmethod
    def isSeparateTeams():
        return bool()

    @staticmethod
    def makePeace():
        pass

    @staticmethod
    def offerDeal():
        return bool()

    @staticmethod
    def ourOfferEmpty():
        return bool()

    @staticmethod
    def performHeadAction(eAction):
        pass

    @staticmethod
    def setAIComment(iComment):
        pass

    @staticmethod
    def setAIOffer(bOffer):
        pass

    @staticmethod
    def setAIString(szString, txtArgs):
        pass

    @staticmethod
    def showAllTrade(bShow):
        pass

    @staticmethod
    def startTrade(iComment, bRenegotiate):
        pass

    @staticmethod
    def theirOfferEmpty():
        return bool()

    @staticmethod
    def theirVassalTribute():
        return bool()


class CyEngine:

    @staticmethod
    def addColoredPlot(plotX, plotY, color, iLayer):
        pass

    @staticmethod
    def addColoredPlotAlt(plotX, plotY, iPlotStyle, iLayer, szColor, fAlpha):
        pass

    @staticmethod
    def addLandmark(pPlot, caption):
        pass

    @staticmethod
    def addLandmarkPopup(pPlot):
        pass

    @staticmethod
    def addSign(plot, playerType, caption):
        pass

    @staticmethod
    def clearAreaBorderPlots(iLayer):
        pass

    @staticmethod
    def clearColoredPlots(iLayer):
        pass

    @staticmethod
    def fillAreaBorderPlot(plotX, plotY, color, iLayer):
        pass

    @staticmethod
    def fillAreaBorderPlotAlt(plotX, plotY, iLayer, szColor, fAlpha):
        pass

    @staticmethod
    def getCityBillboardVisibility():
        return bool()

    @staticmethod
    def getCultureVisibility():
        return bool()

    @staticmethod
    def getNumSigns():
        return int()

    @staticmethod
    def getSelectionCursorVisibility():
        return bool()

    @staticmethod
    def getSignByIndex(index):
        return CySign()

    @staticmethod
    def getUnitFlagVisibility():
        return bool()

    @staticmethod
    def getUpdateRate():
        return float()

    @staticmethod
    def isDirty(eBit):
        return bool()

    @staticmethod
    def isGlobeviewUp():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def reloadEffectInfos():
        pass

    @staticmethod
    def removeLandmark(pPlot):
        pass

    @staticmethod
    def removeSign(pPlot, playerType):
        pass

    @staticmethod
    def setCityBillboardVisibility(bState):
        pass

    @staticmethod
    def setCultureVisibility(bState):
        pass

    @staticmethod
    def setDirty(eBit, bNewValue):
        pass

    @staticmethod
    def setFogOfWar(bState):
        pass

    @staticmethod
    def setSelectionCursorVisibility(bState):
        pass

    @staticmethod
    def setUnitFlagVisibility(bState):
        pass

    @staticmethod
    def setUpdateRate(fUpdateRate):
        pass

    @staticmethod
    def toggleGlobeview():
        pass

    @staticmethod
    def triggerEffect(iEffect, plotPoint):
        pass


class CyFractal:
    class FracValClass:
        DEFAULT_FRAC_X_EXP = -1
        DEFAULT_FRAC_Y_EXP = -1
        FRAC_INVERT_HEIGHTS = -1
        FRAC_POLAR = -1
        FRAC_CENTER_RIFT = -1
        FRAC_WRAP_X = -1
        FRAC_WRAP_Y = -1

    FracVals = FracValClass()

    @staticmethod
    def fracInit(iNewXs, iNewYs, iGrain, random, iFlags, iFracXExp, iFracYExp):
        pass

    @staticmethod
    def fracInitHints(iNewXs, iNewYs, iGrain, random, iFlags, pRifts, iFracXExp, iFracYExp):
        pass

    @staticmethod
    def fracInitRifts(iNewXs, iNewYs, iGrain, random, iFlags, hintsData, iFracXExp, iFracYExp):
        pass

    @staticmethod
    def getHeight(x, y):
        return int()

    @staticmethod
    def getHeightFromPercent(iPercent):
        return int()


class CyGFlyoutMenu:

    @staticmethod
    def addTextItem(szLabel, szPythonCBModule, szPythonCBFxn):
        pass

    @staticmethod
    def create():
        pass

    @staticmethod
    def destroy():
        pass

    @staticmethod
    def hide():
        pass

    @staticmethod
    def show():
        pass


class CyGInterfaceScreen:

    @staticmethod
    def addBonusGraphicGFC(szName, iBonus, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, fxRotation, fzRotation, fScale, bShowBackground):
        pass

    @staticmethod
    def addBuildingGraphicGFC(szName, iBuilding, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, fxRotation, fzRotation, fScale, bShowBackground):
        pass

    @staticmethod
    def addCheckBoxGFC(szName, szTexture, szHiliteTexture, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, eStyle):
        pass

    @staticmethod
    def addCheckBoxGFCAt(szName, szTexture, szHiliteTexture, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, eStyle, bSafeFocus):
        pass

    @staticmethod
    def addDDSGFC(szName, szTexture, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addDDSGFCAt(szName, szAttachTo, szTexture, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, bOption):
        pass

    @staticmethod
    def addDrawControl(szName, szTexture, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addDrawControlAt(szName, szAttachTo, szTexture, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addDropDownBoxGFC(szName, iX, iY, iWidth, eWidgetType, iData1, iData2, eFontType):
        pass

    @staticmethod
    def addEditBoxGFC(szName, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, eFont):
        pass

    @staticmethod
    def addFlagWidgetGFC(szName, iX, iY, iWidth, iHeight, iOwner, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addGraphData(szName, fX, fY, uiLayer):
        pass

    @staticmethod
    def addGraphLayer(szName, uiLayer, iColor):
        pass

    @staticmethod
    def addGraphWidget(szName, szAttachTo, szFile, fX, fY, fZ, fWidth, fHeight, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addImprovementGraphicGFC(szName, iImprovement, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, fxRotation, fzRotation, fScale, bShowBackground):
        pass

    @staticmethod
    def addItemToTableGFC(szAttachTo, szText, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addLeaderheadGFC(szName, eWho, eInitAttitude, iX, iY, iWidth, iHeight, eWidget, iData1, iData2):
        pass

    @staticmethod
    def addLineGFC(szDrawCtrlName, szName, iStartX, iStartY, iEndX, iEndY, eColor):
        pass

    @staticmethod
    def addListBoxGFC(szName, helpText, iX, iY, iWidth, iHeight, eStyle):
        pass

    @staticmethod
    def addModelGraphicGFC(szName, szFile, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, fxRotation, fzRotation, fScale):
        pass

    @staticmethod
    def addMultiListControlGFC(szName, helpText, iX, iY, iWidth, iHeight, numLists, defaultWidth, defaultHeight, eStyle):
        pass

    @staticmethod
    def addMultiListControlGFCAt(szName, helpText, iX, iY, iWidth, iHeight, numLists, defaultWidth, defaultHeight, eStyle):
        pass

    @staticmethod
    def addMultilineText(szName, szText, iX, iY, iWidth, iHeight, eType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def addPanel(szName, title, helpText, bVerticalLayout, bScrollable, iX, iY, iWidth, iHeight, eStyle):
        pass

    @staticmethod
    def addPlotGraphicGFC(szName, iX, iY, iWidth, iHeight, pPlot, iDistance, renderUnits, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addPullDownString(szName, szString, iType, iData, bSelected):
        pass

    @staticmethod
    def addReligionMovieWidgetGFC(szName, szFile, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addScrollPanel(szName, title, iX, iY, iWidth, iHeight, eStyle):
        pass

    @staticmethod
    def addSimpleTableControlGFC(szName, iX, iY, iWidth, iHeight, eStyle):
        pass

    @staticmethod
    def addSlider(szName, iX, iY, iWidth, iHeight, iDefault, iMin, iMax, eWidgetType, iData1, iData2, bIsVertical):
        pass

    @staticmethod
    def addSpaceShipWidgetGFC(szName, iX, iY, iWidth, iHeight, projectType, artType, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addSpecificUnitGraphicGFC(szName, pUnit, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, fxRotation, fzRotation, fScale, bShowBackground):
        pass

    @staticmethod
    def addStackedBarGFC(szName, iX, iY, iWidth, iHeight, iNumBars, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addStackedBarGFCAt(szName, szAttachTo, iX, iY, iWidth, iHeight, iNumBars, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addTableControlGFC(szName, numColumns, iX, iY, iWidth, iHeight, bIncludeHeaders, bDrawGrid, iconWidth, iconHeight, style):
        pass

    @staticmethod
    def addTableControlGFCWithHelp(szName, numColumns, iX, iY, iWidth, iHeight, bIncludeHeaders, bDrawGrid, iconWidth, iconHeight, style, szHelpText):
        pass

    @staticmethod
    def addTableHeaderGFC(szAttachTo, szText, iCol, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def addToModelGraphicGFC(szName, szFile):
        pass

    @staticmethod
    def addUnitGraphicGFC(szName, iUnit, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2, fxRotation, fzRotation, fScale, bShowBackground):
        pass

    @staticmethod
    def appendListBoxString(szAttachTo, item, eType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def appendListBoxStringNoUpdate(szAttachTo, item, eType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def appendMultiListButton(szAttachTo, szTexture, listId, eWidgetType, iData1, iData2, bOption):
        pass

    @staticmethod
    def appendTableRow(szName):
        return int()

    @staticmethod
    def attachButtonGFC(szAttachTo, szName, szText, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def attachCheckBoxGFC(szAttachTo, szName, szTexture, szHiliteTexture, iWidth, iHeight, eWidgetType, iData1, iData2, eStyle):
        pass

    @staticmethod
    def attachControlToTableCell(szControlName, szTableName, iRow, iColumn):
        pass

    @staticmethod
    def attachDropDownBoxGFC(szAttachTo, szName, bExpand):
        pass

    @staticmethod
    def attachImageButton(szAttachTo, szName, szTexture, eSize, eWidgetType, iData1, iData2, bOption):
        pass

    @staticmethod
    def attachLabel(szAttachTo, szName, szText):
        pass

    @staticmethod
    def attachListBoxGFC(szAttachTo, szName, helpText, eStyle):
        pass

    @staticmethod
    def attachMultiListControlGFC(szAttachTo, szName, helpText, numLists, defaultWidth, defaultHeight, eStyle):
        pass

    @staticmethod
    def attachMultilineText(szAttachTo, szName, szText, eType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def attachPanel(szAttachTo, szName, title, helpText, bVerticalLayout, bScrollable, eStyle):
        pass

    @staticmethod
    def attachPanelAt(szAttachTo, szName, title, helpText, bVerticalLayout, bScrollable, eStyle, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def attachSeparator(szAttachTo, szName, bVertical):
        pass

    @staticmethod
    def attachSlider(szAttachTo, szName, iX, iY, iWidth, iHeight, iDefault, iMin, iMax, eWidgetType, iData1, iData2, bIsVertical):
        pass

    @staticmethod
    def attachTableControlGFC(szAttachTo, szName, numColumns, bIncludeHeaders, bDrawGrid, iconWidth, iconHeight, style):
        pass

    @staticmethod
    def attachTextGFC(szAttachTo, szName, text, eFont, eType, iData1, iData2):
        pass

    @staticmethod
    def bringMinimapToFront():
        pass

    @staticmethod
    def centerX(iX):
        return int()

    @staticmethod
    def centerY(iY):
        return int()

    @staticmethod
    def changeDDSGFC(szName, szTexture):
        pass

    @staticmethod
    def changeDrawControl(szName, szTexture):
        pass

    @staticmethod
    def changeImageButton(szName, szTexture):
        pass

    @staticmethod
    def changeModelGraphicTextureGFC(szName, szFile):
        pass

    @staticmethod
    def clearGraphData(szName, uiLayer):
        pass

    @staticmethod
    def clearListBoxGFC(szListBoxName):
        pass

    @staticmethod
    def clearMultiList(szName):
        pass

    @staticmethod
    def commitTableRow(szAttachTo):
        pass

    @staticmethod
    def deleteWidget(pszName):
        pass

    @staticmethod
    def disableMultiListButton(szName, iListId, iIndexId, szTexture):
        pass

    @staticmethod
    def enable(szName, bEnable):
        pass

    @staticmethod
    def enableGridlines(szName, bVertical, bHorizontal):
        pass

    @staticmethod
    def enableMultiListPulse(szName, bEnable, listId, iIndexId):
        pass

    @staticmethod
    def enableSelect(szControlName, bEnable):
        pass

    @staticmethod
    def enableSort(szName):
        pass

    @staticmethod
    def enableWorldSounds(bEnable):
        pass

    @staticmethod
    def getCheckBoxState(szName):
        return bool()

    @staticmethod
    def getCurrentTime():
        return int()

    @staticmethod
    def getEditBoxString(szName):
        return str()

    @staticmethod
    def getPullDownData(szName, iIndex):
        return int()

    @staticmethod
    def getPullDownType(szName, iIndex):
        return int()

    @staticmethod
    def getPythonFileID():
        return int()

    @staticmethod
    def getRenderInterfaceOnly():
        return bool()

    @staticmethod
    def getScreenGroup():
        return int()

    @staticmethod
    def getSelectedPullDownID(szName):
        return int()

    @staticmethod
    def getTableNumColumns(szName):
        return int()

    @staticmethod
    def getTableNumRows(szName):
        return int()

    @staticmethod
    def getTableText(szName, iColumn, iRow):
        pass

    @staticmethod
    def getXResolution():
        return int()

    @staticmethod
    def getYResolution():
        return int()

    @staticmethod
    def hide(szName):
        pass

    @staticmethod
    def hideEndTurn(szName):
        pass

    @staticmethod
    def hideList(iID):
        pass

    @staticmethod
    def hideScreen():
        pass

    @staticmethod
    def initMinimap(iLeft, iRight, iTop, iBottom, fZ):
        pass

    @staticmethod
    def isActive():
        return bool()

    @staticmethod
    def isAlwaysShown():
        return bool()

    @staticmethod
    def isPersistent():
        return bool()

    @staticmethod
    def isRequiredForcedRedraw():
        return bool()

    @staticmethod
    def isRowSelected(szName, iRow):
        return bool()

    @staticmethod
    def leaderheadKeyInput(szName, key):
        pass

    @staticmethod
    def markMinimapTexturePlotDirty(iPlotX, iPlotY):
        pass

    @staticmethod
    def markRenderTexturesDirty():
        pass

    @staticmethod
    def minimapClearAllFlashingTiles():
        pass

    @staticmethod
    def minimapFlashPlot(iX, iY, eColor, fSeconds):
        pass

    @staticmethod
    def modifyLabel(szName, szText, uiFlags):
        pass

    @staticmethod
    def modifyString(szName, szText, uiFlags):
        pass

    @staticmethod
    def moveBackward(szName):
        pass

    @staticmethod
    def moveForward(szName):
        pass

    @staticmethod
    def moveItem(szName, fX, fY, fZ):
        pass

    @staticmethod
    def moveToBack(szName):
        pass

    @staticmethod
    def moveToFront(szName):
        pass

    @staticmethod
    def performLeaderheadAction(szName, eAction):
        pass

    @staticmethod
    def playMovie(szMovieName, fX, fY, fWidth, fHeight, fZ):
        pass

    @staticmethod
    def prependListBoxString(szAttachTo, item, eType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def registerHideList(szNames, iSize, iID):
        pass

    @staticmethod
    def removeLineGFC(szDrawCtrlName, szName):
        pass

    @staticmethod
    def renderMinimapWorldTexture():
        pass

    @staticmethod
    def selectMultiList(szName, iListID):
        pass

    @staticmethod
    def selectRow(szName, iRow, bSelected):
        pass

    @staticmethod
    def setActivation(szName, activation):
        pass

    @staticmethod
    def setAlwaysShown(bAlwaysShown):
        pass

    @staticmethod
    def setBarPercentage(szName, iBar, fPercent):
        pass

    @staticmethod
    def setButtonGFC(szName, szText, szTexture, iX, iY, imageWidth, imageHeight, eWidgetType, iData1, iData2, eStyle):
        pass

    @staticmethod
    def setCloseOnEscape(bCloseOnEscape):
        pass

    @staticmethod
    def setDimensions(iX, iY, iWidth, iHeight):
        pass

    @staticmethod
    def setDying(bDying):
        pass

    @staticmethod
    def setEditBoxMaxCharCount(szName, maxCharCount, preferredCharCount):
        pass

    @staticmethod
    def setEditBoxString(szName, szString):
        pass

    @staticmethod
    def setEditBoxTextColor(szName, kColor):
        pass

    @staticmethod
    def setEndTurnState(szName, szText):
        pass

    @staticmethod
    def setExitText(szText, uiFlags, fX, fY, fZ, eFont):
        pass

    @staticmethod
    def setFocus(szName):
        pass

    @staticmethod
    def setForcedRedraw(bRequiresForcedRedraw):
        pass

    @staticmethod
    def setGraphGrid(szName, fXstart, fdX, fYstart, fdY):
        pass

    @staticmethod
    def setGraphLabelX(szName, szLabel):
        pass

    @staticmethod
    def setGraphLabelY(szName, szLabel):
        pass

    @staticmethod
    def setGraphXDataRange(szName, fXmin, fXmax):
        pass

    @staticmethod
    def setGraphYDataRange(szName, fYmin, fYmax):
        pass

    @staticmethod
    def setHelpLabel(szName, szAtttachTo, szText, uiFlags, fX, fY, fZ, eFont, szHelpText):
        pass

    @staticmethod
    def setHelpTextArea(fWidth, eFont, fX, fY, fZ, bFloating, szArtFile, bExpandRight, bExpandDown, uiFlags, iMinWidth):
        pass

    @staticmethod
    def setHelpTextString(szString):
        pass

    @staticmethod
    def setHitTest(szName, hitTest):
        pass

    @staticmethod
    def setImageButton(szName, szTexture, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def setImageButtonAt(szName, szAttachTo, szTexture, iX, iY, iWidth, iHeight, eWidgetType, iData1, iData2):
        pass

    @staticmethod
    def setLabel(szName, szAtttachTo, szText, uiFlags, fX, fY, fZ, eFont, eType, iData1, iData2):
        pass

    @staticmethod
    def setLabelAt(szName, szAttachTo, szText, uiFlags, fX, fY, fZ, eFont, eType, iData1, iData2):
        pass

    @staticmethod
    def setLeaderheadAdvisor(szName, eAdvisor):
        pass

    @staticmethod
    def setLeaderheadMood(szName, eAttitude):
        pass

    @staticmethod
    def setListBoxStringGFC(szName, item, szText, eType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def setMainInterface(bMain):
        pass

    @staticmethod
    def setMinimapColor(eMinimapMode, iX, iY, iColor, fAlpha):
        pass

    @staticmethod
    def setMinimapMap(pReplayInfo, iLeft, iRight, iTop, iBottom, fZ):
        pass

    @staticmethod
    def setMinimapMode(eMode):
        pass

    @staticmethod
    def setMinimapNoRender(value):
        pass

    @staticmethod
    def setMinimapSectionOverride(left, bottom, right, top):
        pass

    @staticmethod
    def setModelGraphicRotationRateGFC(szName, rate):
        pass

    @staticmethod
    def setPanelColor(szName, iRed, iGreen, iBlue):
        pass

    @staticmethod
    def setPanelSize(szName, iX, iY, iWidth, iHeight):
        pass

    @staticmethod
    def setPersistent(bPersistent):
        pass

    @staticmethod
    def setRenderInterfaceOnly(val):
        pass

    @staticmethod
    def setScreenGroup(iGroup):
        pass

    @staticmethod
    def setSelectedListBoxStringGFC(szName, item):
        pass

    @staticmethod
    def setShowFor(i):
        pass

    @staticmethod
    def setSound(pszSound):
        pass

    @staticmethod
    def setSoundId(iSoundId):
        pass

    @staticmethod
    def setSpaceShip(projectType):
        pass

    @staticmethod
    def setStackedBarColors(szName, iBar, eColor):
        pass

    @staticmethod
    def setStackedBarColorsAlpha(szName, iBar, eColor, fAlpha):
        pass

    @staticmethod
    def setStackedBarColorsRGB(szName, iBar, iRed, iGreen, iBlue, fAlpha):
        pass

    @staticmethod
    def setState(szName, eState):
        pass

    @staticmethod
    def setStyle(szName, szStyle):
        pass

    @staticmethod
    def setTableColumnHeader(szName, iColumn, header, iWidth):
        pass

    @staticmethod
    def setTableColumnRightJustify(szName, iCol):
        pass

    @staticmethod
    def setTableDate(szName, iColumn, iRow, text, szIcon, eWidgetType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def setTableInt(szName, iColumn, iRow, text, szIcon, eWidgetType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def setTableNumRows(szName, numRows):
        pass

    @staticmethod
    def setTableRowHeight(szName, iRow, iHeight):
        pass

    @staticmethod
    def setTableText(szName, iColumn, iRow, text, szIcon, eWidgetType, iData1, iData2, iJustify):
        pass

    @staticmethod
    def setTableTextKey(szName, iColumn, szKey, iRowTest, text, eWidgetType, iData1, iData2, iJustify, iNumRows):
        pass

    @staticmethod
    def setText(szName, szAtttachTo, szText, uiFlags, fX, fY, fZ, eFont, eType, iData1, iData2):
        pass

    @staticmethod
    def setTextAt(szName, szAttachTo, szText, uiFlags, fX, fY, fZ, eFont, eType, iData1, iData2):
        pass

    @staticmethod
    def setToolTipAlignment(szName, alignment):
        pass

    @staticmethod
    def setViewMin(szName, iWidth, iHeight):
        pass

    @staticmethod
    def show(szName):
        pass

    @staticmethod
    def showEndTurn(szName):
        pass

    @staticmethod
    def showRange(szName, iLow, iHigh):
        pass

    @staticmethod
    def showScreen(bState, bPassInput):
        pass

    @staticmethod
    def showWindowBackground(bShow):
        pass

    @staticmethod
    def spaceShipCanChangeType(projectType):
        return bool()

    @staticmethod
    def spaceShipChangeType(projectType):
        pass

    @staticmethod
    def spaceShipFinalize():
        pass

    @staticmethod
    def spaceShipLaunch():
        pass

    @staticmethod
    def spaceShipZoom(projectType):
        pass

    @staticmethod
    def updateAppropriateCitySelection(szName, iNumRows):
        pass

    @staticmethod
    def updateListBox(szAttachTo):
        pass

    @staticmethod
    def updateMinimap(fTime):
        pass

    @staticmethod
    def updateMinimapColorFromMap(eMode, fAlpha):
        pass

    @staticmethod
    def updateMinimapSection(bWholeMap):
        pass

    @staticmethod
    def updateMinimapVisibility():
        pass


class CyGTabCtrl:

    @staticmethod
    def addSectionButton(szLabel, szPythonCBModule, szPythonCBFxn, szPythonID, iTabIndex):
        pass

    @staticmethod
    def addSectionCheckbox(szLabel, szPythonCBModule, szPythonCBFxn, szPythonID, iTabIndex, bInitialState):
        pass

    @staticmethod
    def addSectionDropdown(szItems, szPythonCBModule, szPythonCBFxn, szPythonID, iTabIndex, iInitialSelection):
        pass

    @staticmethod
    def addSectionEditCtrl(szLabel, szPythonCBModule, szPythonCBFxn, szPythonID, iTabIndex):
        pass

    @staticmethod
    def addSectionLabel(szLabel, iTabIndex):
        pass

    @staticmethod
    def addSectionRadioButton(szLabel, szPythonCBModule, szPythonCBFxn, szPythonID, iTabIndex, bInitialState):
        pass

    @staticmethod
    def addSectionSeparator(iTab):
        pass

    @staticmethod
    def addSectionSlider(szLabel, szPythonCBModule, szPythonCBFxn, szPythonID, iTabIndex, iMin, iMax, iInitialVal, iFormatNumber, iFormatDecimal):
        pass

    @staticmethod
    def addSectionSpinner(szLabel, szPythonCBModule, szPythonCBFxn, szPythonID, iTabIndex, fMin, fMax, fInc, fInitialVal):
        pass

    @staticmethod
    def addTabSection(szLabel):
        pass

    @staticmethod
    def attachButton(szParent, szName, szLabel, szPythonCBModule, szPythonCBFxn, szPythonID):
        pass

    @staticmethod
    def attachCheckBox(szParent, szName, szLabel, szPythonCBModule, szPythonCBFxn, szPythonID, bInitialState):
        pass

    @staticmethod
    def attachDropDown(szParent, szName, szID, szItems, szPythonCBModule, szPythonCBFxn, szPythonID, iInitialSelection):
        pass

    @staticmethod
    def attachEdit(szParent, szName, szLabel, szPythonCBModule, szPythonCBFxn, szPythonID):
        pass

    @staticmethod
    def attachExpandSpacer(szParent):
        pass

    @staticmethod
    def attachFixedSpacer(szParent, iSize):
        pass

    @staticmethod
    def attachHBox(szParent, szName):
        pass

    @staticmethod
    def attachHSeparator(szParent, szName):
        pass

    @staticmethod
    def attachHSlider(szParent, szName, szPythonCBModule, szPythonCBFxn, szPythonID, iMin, iMax, iInitialVal):
        pass

    @staticmethod
    def attachImage(szParent, szName, szFilename):
        pass

    @staticmethod
    def attachLabel(szParent, szName, szLabel):
        pass

    @staticmethod
    def attachPanel(szParent, szName):
        pass

    @staticmethod
    def attachRadioButton(szParent, szName, szLabel, szPythonCBModule, szPythonCBFxn, szPythonID, bInitialState):
        pass

    @staticmethod
    def attachScrollPanel(szParent, szName):
        pass

    @staticmethod
    def attachSpacer(szParent):
        pass

    @staticmethod
    def attachSpinner(szParent, szName, szPythonCBModule, szPythonCBFxn, szPythonID, fMin, fMax, fInc, fInitialVal, iFormatNumber, iFormatDecimal):
        pass

    @staticmethod
    def attachTabItem(szName, szLabel):
        pass

    @staticmethod
    def attachTitledPanel(szParent, szName, szLabel):
        pass

    @staticmethod
    def attachVBox(szParent, szName):
        pass

    @staticmethod
    def attachVSeparator(szParent, szName):
        pass

    @staticmethod
    def attachVSlider(szParent, szName, szPythonCBModule, szPythonCBFxn, szPythonID, iMin, iMax, iInitialVal):
        pass

    @staticmethod
    def changeDropdownContents(szID, szItems):
        pass

    @staticmethod
    def create():
        pass

    @staticmethod
    def createByName(name):
        pass

    @staticmethod
    def destroy():
        pass

    @staticmethod
    def enable(bVal):
        pass

    @staticmethod
    def getActiveTab():
        return bool()

    @staticmethod
    def getCheckBoxState(szTabName, szButtonText):
        pass

    @staticmethod
    def getControlsExpanding():
        return bool()

    @staticmethod
    def getDropDownSelection(szTabName, szID):
        pass

    @staticmethod
    def getRadioButtonState(szTabName, szButtonText):
        pass

    @staticmethod
    def getRadioValue(szName):
        return float()

    @staticmethod
    def getText(szName):
        return str()

    @staticmethod
    def getValue(szName):
        return float()

    @staticmethod
    def isEnabled():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def setActivation(szName, szActivationType):
        pass

    @staticmethod
    def setCheckBoxState(szTabName, szButtonText, bState):
        pass

    @staticmethod
    def setColumnLength(iSize):
        pass

    @staticmethod
    def setControlFlag(szName, szFlag):
        pass

    @staticmethod
    def setControlsExpanding(bExp):
        pass

    @staticmethod
    def setDropDownSelection(szTabName, szID, iSelection):
        pass

    @staticmethod
    def setEditCtrlText(szTabName, szEditCtrlText, szNewText):
        pass

    @staticmethod
    def setEnabled(szName, bEnabled):
        pass

    @staticmethod
    def setFocus(szName):
        pass

    @staticmethod
    def setHitTest(szName, szHitTestType):
        pass

    @staticmethod
    def setKeyFocus(szName, szKey, szTarget):
        pass

    @staticmethod
    def setLayoutFlag(szName, szFlag):
        pass

    @staticmethod
    def setModal(modal):
        pass

    @staticmethod
    def setNumColumns(iSize):
        pass

    @staticmethod
    def setRadioButtonState(szTabName, szButtonText, bState):
        pass

    @staticmethod
    def setRadioValue(szName, fValue):
        pass

    @staticmethod
    def setSize(width, height):
        pass

    @staticmethod
    def setSliderWidth(szName, iWidth):
        pass

    @staticmethod
    def setStyle(szName, szStyle):
        pass

    @staticmethod
    def setTabFocus(szName, szNext, szPrev):
        pass

    @staticmethod
    def setText(szName, szText):
        pass

    @staticmethod
    def setToolTip(szName, szHelpText):
        pass

    @staticmethod
    def setValue(szName, fValue):
        pass

    @staticmethod
    def toggle():
        pass


class CyGame:

    @staticmethod
    def GetWorldBuilderMode():
        return bool()

    @staticmethod
    def addDeal():
        return CyDeal()

    @staticmethod
    def addPlayer(eNewPlayer, eLeader, eCiv):
        pass

    @staticmethod
    def calculateOptionsChecksum():
        return int()

    @staticmethod
    def calculateReligionPercent(eReligion):
        return int()

    @staticmethod
    def calculateSyncChecksum():
        return int()

    @staticmethod
    def canHaveSecretaryGeneral(eVoteSource):
        return bool()

    @staticmethod
    def canTrainNukes():
        return bool()

    @staticmethod
    def changeDiploVote(eVoteSource, iChange):
        pass

    @staticmethod
    def changeFreeTradeCount(iChange):
        pass

    @staticmethod
    def changeMaxTurns(iChange):
        pass

    @staticmethod
    def changeNoNukesCount(iChange):
        pass

    @staticmethod
    def changeNukesExploded(iChange):
        pass

    @staticmethod
    def changePlotExtraCost(iX, iY, iExtraCost):
        pass

    @staticmethod
    def changeTradeRoutes(iChange):
        pass

    @staticmethod
    def cityPushOrder(pCity, eOrder, iData, bAlt, bShift, bCtrl):
        pass

    @staticmethod
    def clearHeadquarters(eIndex):
        pass

    @staticmethod
    def clearHolyCity(eIndex):
        pass

    @staticmethod
    def countCivPlayersAlive():
        return int()

    @staticmethod
    def countCivPlayersEverAlive():
        return int()

    @staticmethod
    def countCivTeamsAlive():
        return int()

    @staticmethod
    def countCivTeamsEverAlive():
        return int()

    @staticmethod
    def countCorporationLevels(eCorporation):
        return int()

    @staticmethod
    def countHumanPlayersAlive():
        return int()

    @staticmethod
    def countKnownTechNumTeams(eTech):
        return int()

    @staticmethod
    def countNumHumanGameTurnActive():
        return int()

    @staticmethod
    def countPossibleVote(eVote, eVoteSource):
        return int()

    @staticmethod
    def countReligionLevels(eReligion):
        return int()

    @staticmethod
    def countTotalCivPower():
        return int()

    @staticmethod
    def countTotalNukeUnits():
        return int()

    @staticmethod
    def cycleCities(bForward, bAdd):
        pass

    @staticmethod
    def cyclePlotUnits(pPlot, bForward, bAuto, iCount):
        return bool()

    @staticmethod
    def cycleSelectionGroups(bClear, bForward, bWorkers):
        pass

    @staticmethod
    def getAIAutoPlay():
        return int()

    @staticmethod
    def getActiveCivilizationType():
        return -1  # Type

    @staticmethod
    def getActivePlayer():
        return -1  # Type

    @staticmethod
    def getActiveTeam():
        return int()

    @staticmethod
    def getAdjustedLandPercent(eVictory):
        return int()

    @staticmethod
    def getAdjustedPopulationPercent(eVictory):
        return int()

    @staticmethod
    def getBestLandUnit():
        return -1  # Type

    @staticmethod
    def getBestLandUnitCombat():
        return int()

    @staticmethod
    def getBuildingClassCreatedCount(eIndex):
        return int()

    @staticmethod
    def getCalendar():
        return -1  # Type

    @staticmethod
    def getCorporationGameTurnFounded(eIndex):
        return int()

    @staticmethod
    def getCurrentEra():
        return -1  # Type

    @staticmethod
    def getCurrentLanguage():
        return int()

    @staticmethod
    def getDeal(iID):
        return CyDeal()

    @staticmethod
    def getElapsedGameTurns():
        return int()

    @staticmethod
    def getEstimateEndTurn():
        return int()

    @staticmethod
    def getForceCivicCount(eIndex):
        return int()

    @staticmethod
    def getFreeTradeCount():
        return int()

    @staticmethod
    def getGameSpeedType():
        return -1  # Type

    @staticmethod
    def getGameState():
        return -1  # Type

    @staticmethod
    def getGameTurn():
        return int()

    @staticmethod
    def getGameTurnYear():
        return int()

    @staticmethod
    def getHandicapType():
        return -1  # Type

    @staticmethod
    def getHeadquarters(eIndex):
        return CyCity()

    @staticmethod
    def getHolyCity(eIndex):
        return CyCity()

    @staticmethod
    def getImprovementUpgradeTime(eImprovement):
        return int()

    @staticmethod
    def getIndexAfterLastDeal():
        return int()

    @staticmethod
    def getInitLand():
        return int()

    @staticmethod
    def getInitPopulation():
        return int()

    @staticmethod
    def getInitTech():
        return int()

    @staticmethod
    def getInitWonders():
        return int()

    @staticmethod
    def getMapRand():
        return CyRandom()

    @staticmethod
    def getMapRandNum(iNum, pszLog):
        return int()

    @staticmethod
    def getMaxCityElimination():
        return int()

    @staticmethod
    def getMaxLand():
        return int()

    @staticmethod
    def getMaxPopulation():
        return int()

    @staticmethod
    def getMaxTech():
        return int()

    @staticmethod
    def getMaxTurns():
        return int()

    @staticmethod
    def getMaxWonders():
        return int()

    @staticmethod
    def getMinutesPlayed():
        return int()

    @staticmethod
    def getName():
        return str()

    @staticmethod
    def getNoNukesCount():
        return int()

    @staticmethod
    def getNukesExploded():
        return int()

    @staticmethod
    def getNumAdvancedStartPoints():
        return int()

    @staticmethod
    def getNumCities():
        return int()

    @staticmethod
    def getNumCivCities():
        return int()

    @staticmethod
    def getNumDeals():
        return int()

    @staticmethod
    def getNumFreeBonuses(eBuilding):
        return int()

    @staticmethod
    def getNumGameTurnActive():
        return int()

    @staticmethod
    def getNumHumanPlayers():
        return int()

    @staticmethod
    def getNumReplayMessages():
        return int()

    @staticmethod
    def getPausePlayer():
        return int()

    @staticmethod
    def getPitbossTurnTime():
        return int()

    @staticmethod
    def getPlayerRank(iIndex):
        return int()

    @staticmethod
    def getPlayerScore(iIndex):
        return int()

    @staticmethod
    def getPlayerVote(eOwnerIndex, iVoteId):
        return int()

    @staticmethod
    def getProductionPerPopulation(eHurry):
        return int()

    @staticmethod
    def getProjectCreatedCount(eIndex):
        return int()

    @staticmethod
    def getRankPlayer(iRank):
        return int()

    @staticmethod
    def getRankTeam(iRank):
        return -1  # Type

    @staticmethod
    def getReligionGameTurnFounded(eIndex):
        return int()

    @staticmethod
    def getReplayInfo():
        return CyReplayInfo()

    @staticmethod
    def getReplayMessageColor(i):
        return -1  # Type

    @staticmethod
    def getReplayMessagePlayer(i):
        return int()

    @staticmethod
    def getReplayMessagePlotX(i):
        return int()

    @staticmethod
    def getReplayMessagePlotY(i):
        return int()

    @staticmethod
    def getReplayMessageText(i):
        return str()

    @staticmethod
    def getReplayMessageTurn(i):
        return int()

    @staticmethod
    def getReplayMessageType(i):
        return -1  # Type

    @staticmethod
    def getScriptData():
        return str()

    @staticmethod
    def getSecretaryGeneral(eVoteSource):
        return int()

    @staticmethod
    def getSecretaryGeneralTimer(iVoteSource):
        return int()

    @staticmethod
    def getSorenRand():
        return CyRandom()

    @staticmethod
    def getSorenRandNum(iNum, pszLog):
        return int()

    @staticmethod
    def getStartEra():
        return -1  # Type

    @staticmethod
    def getStartTurn():
        return int()

    @staticmethod
    def getStartYear():
        return int()

    @staticmethod
    def getSymbolID(iSymbol):
        return int()

    @staticmethod
    def getTargetScore():
        return int()

    @staticmethod
    def getTeamRank(iIndex):
        return int()

    @staticmethod
    def getTeamScore(iIndex):
        return int()

    @staticmethod
    def getTotalPopulation():
        return int()

    @staticmethod
    def getTradeRoutes():
        return int()

    @staticmethod
    def getTurnSlice():
        return int()

    @staticmethod
    def getTurnYear(iGameTurn):
        return int()

    @staticmethod
    def getUnitClassCreatedCount(eIndex):
        return int()

    @staticmethod
    def getUnitCreatedCount(eIndex):
        return int()

    @staticmethod
    def getVictory():
        return -1  # Type

    @staticmethod
    def getVoteOutcome(eIndex):
        return int()

    @staticmethod
    def getVoteRequired(eVote, eVoteSource):
        return int()

    @staticmethod
    def getVoteSourceReligion(eVoteSource):
        return int()

    @staticmethod
    def getVoteTimer(iVoteSource):
        return int()

    @staticmethod
    def getWinner():
        return -1  # Type

    @staticmethod
    def goldenAgeLength():
        return int()

    @staticmethod
    def hasSkippedSaveChecksum():
        return bool()

    @staticmethod
    def isBuildingClassMaxedOut(eIndex, iExtra):
        return bool()

    @staticmethod
    def isBuildingEverActive(eBuilding):
        return bool()

    @staticmethod
    def isChooseElection(eVote):
        return bool()

    @staticmethod
    def isCircumnavigated():
        return bool()

    @staticmethod
    def isCivEverActive(eCivilization):
        return bool()

    @staticmethod
    def isCorporationFounded(eIndex):
        return bool()

    @staticmethod
    def isDebugMode():
        return bool()

    @staticmethod
    def isDiploVote(eVoteSource):
        return bool()

    @staticmethod
    def isEventActive(eTrigger):
        return bool()

    @staticmethod
    def isFinalInitialized():
        return bool()

    @staticmethod
    def isForceCivic(eIndex):
        return bool()

    @staticmethod
    def isForceCivicOption(eCivicOption):
        return bool()

    @staticmethod
    def isForcedControl(eIndex):
        return bool()

    @staticmethod
    def isFreeTrade():
        return bool()

    @staticmethod
    def isGameMultiPlayer():
        return bool()

    @staticmethod
    def isHotSeat():
        return bool()

    @staticmethod
    def isInAdvancedStart():
        return bool()

    @staticmethod
    def isLeaderEverActive(eLeader):
        return bool()

    @staticmethod
    def isMPOption(eIndex):
        return bool()

    @staticmethod
    def isModem():
        return bool()

    @staticmethod
    def isNetworkMultiPlayer():
        return bool()

    @staticmethod
    def isNoNukes():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isNukesValid():
        return bool()

    @staticmethod
    def isOption(eIndex):
        return bool()

    @staticmethod
    def isPaused():
        return bool()

    @staticmethod
    def isPbem():
        return bool()

    @staticmethod
    def isPitboss():
        return bool()

    @staticmethod
    def isPitbossHost():
        return bool()

    @staticmethod
    def isProjectMaxedOut(eIndex, iExtra):
        return bool()

    @staticmethod
    def isReligionFounded(eIndex):
        return bool()

    @staticmethod
    def isReligionSlotTaken(eIndex):
        return bool()

    @staticmethod
    def isScoreDirty():
        return bool()

    @staticmethod
    def isSimultaneousTeamTurns():
        return bool()

    @staticmethod
    def isSpecialBuildingValid(eIndex):
        return bool()

    @staticmethod
    def isSpecialUnitValid(eSpecialUnitType):
        return bool()

    @staticmethod
    def isTeamGame():
        return bool()

    @staticmethod
    def isTeamVote(eVote):
        return bool()

    @staticmethod
    def isTeamVoteEligible(eTeam, eVoteSource):
        return bool()

    @staticmethod
    def isUnitClassMaxedOut(eIndex, iExtra):
        return bool()

    @staticmethod
    def isUnitEverActive(eUnit):
        return bool()

    @staticmethod
    def isVictoryValid(eIndex):
        return bool()

    @staticmethod
    def isVotePassed(eIndex):
        return bool()

    @staticmethod
    def makeCircumnavigated():
        pass

    @staticmethod
    def makeNukesValid(bValid):
        pass

    @staticmethod
    def makeSpecialBuildingValid(eIndex):
        pass

    @staticmethod
    def makeSpecialUnitValid(eSpecialUnitType):
        pass

    @staticmethod
    def reviveActivePlayer():
        pass

    @staticmethod
    def saveReplay(iPlayer):
        pass

    @staticmethod
    def selectedCitiesGameNetMessage(eMessage, iData2, iData3, iData4, bOption, bAlt, bShift, bCtrl):
        pass

    @staticmethod
    def selectionListGameNetMessage(eMessage, iData2, iData3, iData4, iFlags, bAlt, bShift):
        pass

    @staticmethod
    def selectionListMove(pPlot, bAlt, bShift, bCtrl):
        pass

    @staticmethod
    def setAIAutoPlay(iNewValue):
        pass

    @staticmethod
    def setActivePlayer(eNewValue, bForceHotSeat):
        pass

    @staticmethod
    def setCurrentLanguage(iNewLanguage):
        pass

    @staticmethod
    def setEstimateEndTurn(iNewValue):
        pass

    @staticmethod
    def setGameTurn(iNewValue):
        pass

    @staticmethod
    def setHeadquarters(eIndex, pNewValue, bAnnounce):
        pass

    @staticmethod
    def setHolyCity(eIndex, pNewValue, bAnnounce):
        pass

    @staticmethod
    def setMaxCityElimination(iNewValue):
        pass

    @staticmethod
    def setMaxTurns(iNewValue):
        pass

    @staticmethod
    def setModem(bModem):
        pass

    @staticmethod
    def setName(szName):
        pass

    @staticmethod
    def setNumAdvancedStartPoints(iNewValue):
        pass

    @staticmethod
    def setOption(eIndex, bEnabled):
        pass

    @staticmethod
    def setPitbossTurnTime(iHours):
        pass

    @staticmethod
    def setPlotExtraYield(iX, iY, eYield, iExtraYield):
        pass

    @staticmethod
    def setScoreDirty(bNewValue):
        pass

    @staticmethod
    def setScriptData(szNewValue):
        pass

    @staticmethod
    def setStartYear(iNewValue):
        pass

    @staticmethod
    def setTargetScore(iNewValue):
        pass

    @staticmethod
    def setVoteSourceReligion(eVoteSource, eReligion, bAnnounce):
        pass

    @staticmethod
    def setWinner(eNewWinner, eNewVictory):
        pass

    @staticmethod
    def toggleDebugMode():
        pass

    @staticmethod
    def updateScore(bForce):
        pass

    @staticmethod
    def victoryDelay(eVictory):
        return int()

    @staticmethod
    def doControl(eControlType):
        pass

    if PB_MOD:
        @staticmethod
        def setPausePlayer(iPlayer):
            pass

        @staticmethod
        def incrementTurnTimer(iFrames):
            pass

        @staticmethod
        def setCivPassword(iPlayer, sNewPassword, sAdminPasswordHash):
            return int()

        @staticmethod
        def setAdminPassword(sNewPassword, sAdminPasswordHash):
            return int()

        @staticmethod
        def setPitbossShortNames(bEnable, iLenName, iLenDesc):
            pass

        @staticmethod
        def sendTurnCompletePB(iPlayer):
            pass

        @staticmethod
        def getModPath():
            return str()

        @staticmethod
        def delayedPythonCall(iMilliseconds, iArg1, iArg2):
            return int()

        @staticmethod
        def unzipModUpdate(zip_path):
            return int()

        @staticmethod
        def fixTradeRoutes():
            pass


class CyGameTextMgr:

    @staticmethod
    def Reset():
        pass

    @staticmethod
    def buildHintsList():
        return str()

    @staticmethod
    def getActiveDealsString(iThisPlayer, iOtherPlayer):
        return str()

    @staticmethod
    def getAttitudeString(iPlayer, iTargetPlayer):
        return str()

    @staticmethod
    def getBonusHelp(iBonus, bCivilopediaText):
        return str()

    @staticmethod
    def getBuildingHelp(iBuilding, bCivilopediaText, bStrategyText, bTechChooserText, pCity):
        return str()

    @staticmethod
    def getCorporationHelpCity(iCorporation, pCity, bCityScreen, bForceCorporation):
        return str()

    @staticmethod
    def getDateStr(iGameTurn, bSave, eCalendar, iStartYear, eSpeed):
        return str()

    @staticmethod
    def getDealString(pDeal, iPlayerPerspective):
        return str()

    @staticmethod
    def getFeatureHelp(iFeature, bCivilopediaText):
        return str()

    @staticmethod
    def getGoldStr(iPlayer):
        return str()

    @staticmethod
    def getImprovementHelp(iImprovement, bCivilopediaText):
        return str()

    @staticmethod
    def getInterfaceTimeStr(iPlayer):
        return str()

    @staticmethod
    def getNetStats(iPlayer):
        return str()

    @staticmethod
    def getOOSSeeds(iPlayer):
        return str()

    @staticmethod
    def getProjectHelp(iProject, bCivilopediaText, pCity):
        return str()

    @staticmethod
    def getPromotionHelp(iPromotion, bCivilopediaText):
        return str()

    @staticmethod
    def getReligionHelpCity(iReligion, pCity, bCityScreen, bForceReligion, bForceState, bNoStateReligion):
        return str()

    @staticmethod
    def getResearchStr(iPlayer):
        return str()

    @staticmethod
    def getSpecialistHelp(iSpecialist, bCivilopediaText):
        return str()

    @staticmethod
    def getSpecificUnitHelp(pUnit, bOneLine, bShort):
        return str()

    @staticmethod
    def getTechHelp(iTech, bCivilopediaText, bPlayerContext, bStrategyText, bTreeInfo, iFromTech):
        return str()

    @staticmethod
    def getTerrainHelp(iTerrain, bCivilopediaText):
        return str()

    @staticmethod
    def getTimeStr(iGameTurn, bSave):
        return str()

    @staticmethod
    def getTradeString(pTradeData, iPlayer1, iPlayer2):
        return str()

    @staticmethod
    def getUnitHelp(iUnit, bCivilopediaText, bStrategyText, bTechChooserText, pCity):
        return str()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def parseCivInfos(iCivilization, bDawnOfMan):
        return str()

    @staticmethod
    def parseCivicInfo(iCivicType, bCivilopediaText, bPlayerContext, bSkipName):
        return str()

    @staticmethod
    def parseCorporationInfo(iCorporationType, bCivilopediaText):
        return str()

    @staticmethod
    def parseLeaderTraits(iLeader, iCivilization, bDawnOfMan, bCivilopediaText):
        return str()

    @staticmethod
    def parseReligionInfo(iReligionType, bCivilopediaText):
        return str()

    @staticmethod
    def setConvertHelp(iPlayer, iReligion):
        return str()

    @staticmethod
    def setRevolutionHelp(iPlayer):
        return str()

    @staticmethod
    def setVassalRevoltHelp(iMaster, iVassal):
        return str()


class CyGlobalContext:

    @staticmethod
    def getAIR_BOMB_HEIGHT():
        return float()

    @staticmethod
    def getAMPHIB_ATTACK_MODIFIER():
        return int()

    @staticmethod
    def getASyncRand():
        return CyRandom()

    @staticmethod
    def getActionInfo(i):
        return CvActionInfo()

    @staticmethod
    def getActivePlayer():
        return CyPlayer()

    @staticmethod
    def getAnimationOperatorTypes(i):
        return str()

    @staticmethod
    def getArtStyleTypes(i):
        return str()

    @staticmethod
    def getAttitudeInfo(i):
        return CvInfoBase()

    @staticmethod
    def getAutomateInfo(i):
        return CvAutomateInfo()

    @staticmethod
    def getBARBARIAN_PLAYER():
        return int()

    @staticmethod
    def getBARBARIAN_TEAM():
        return int()

    @staticmethod
    def getBonusArtInfo(i):
        return CvArtInfoBonus()

    @staticmethod
    def getBonusClassInfo(i):
        return CvBonusClassInfo()

    @staticmethod
    def getBonusInfo(i):
        return CvBonusInfo()

    @staticmethod
    def getBuildInfo(i):
        return CvBuildInfo()

    @staticmethod
    def getBuildingArtInfo(i):
        return CvArtInfoBuilding()

    @staticmethod
    def getBuildingClassInfo(i):
        return CvBuildingClassInfo()

    @staticmethod
    def getBuildingInfo(i):
        return CvBuildingInfo()

    @staticmethod
    def getCAMERA_FAR_CLIP_Z_HEIGHT():
        return float()

    @staticmethod
    def getCAMERA_LOWER_PITCH():
        return float()

    @staticmethod
    def getCAMERA_MAX_TRAVEL_DISTANCE():
        return float()

    @staticmethod
    def getCAMERA_MAX_TURN_OFFSET():
        return float()

    @staticmethod
    def getCAMERA_MAX_YAW():
        return float()

    @staticmethod
    def getCAMERA_MIN_DISTANCE():
        return float()

    @staticmethod
    def getCAMERA_MIN_YAW():
        return float()

    @staticmethod
    def getCAMERA_SPECIAL_PITCH():
        return float()

    @staticmethod
    def getCAMERA_START_DISTANCE():
        return float()

    @staticmethod
    def getCAMERA_UPPER_PITCH():
        return float()

    @staticmethod
    def getCITY_HOME_PLOT():
        return int()

    @staticmethod
    def getCITY_MAX_NUM_BUILDINGS():
        return int()

    @staticmethod
    def getCalendarInfo(i):
        return CvInfoBase()

    @staticmethod
    def getCitySizeTypes(i):
        return str()

    @staticmethod
    def getCityTabInfo(i):
        return CvInfoBase()

    @staticmethod
    def getCivicInfo(i):
        return CvCivicInfo()

    @staticmethod
    def getCivicOptionInfo(i):
        return CvCivicOptionInfo()

    @staticmethod
    def getCivilizationArtInfo(i):
        return CvArtInfoCivilization()

    @staticmethod
    def getCivilizationInfo(idx):
        return CvCivilizationInfo()

    @staticmethod
    def getClimateInfo(i):
        return CvClimateInfo()

    @staticmethod
    def getColorInfo(i):
        return CvColorInfo()

    @staticmethod
    def getCommandInfo(i):
        return CvCommandInfo()

    @staticmethod
    def getCommerceInfo(i):
        return CvCommerceInfo()

    @staticmethod
    def getConceptInfo(i):
        return CvInfoBase()

    @staticmethod
    def getContactTypes(i):
        return str()

    @staticmethod
    def getControlInfo(i):
        return CvControlInfo()

    @staticmethod
    def getCorporationInfo(i):
        return CvCorporationInfo()

    @staticmethod
    def getCultureLevelInfo(i):
        return CvCultureLevelInfo()

    @staticmethod
    def getDefineFLOAT(szName):
        return float()

    @staticmethod
    def getDefineINT(szName):
        return int()

    @staticmethod
    def getDefineSTRING(szName):
        return str()

    @staticmethod
    def getDenialInfo(i):
        return CvInfoBase()

    @staticmethod
    def getDiplomacyInfo(i):
        return CvDiplomacyInfo()

    @staticmethod
    def getDiplomacyPowerTypes(i):
        return str()

    @staticmethod
    def getDomainInfo(i):
        return CvInfoBase()

    @staticmethod
    def getEVENT_MESSAGE_TIME():
        return int()

    @staticmethod
    def getEffectInfo(i):
        return CvEffectInfo()

    @staticmethod
    def getEmphasizeInfo(i):
        return CvEmphasizeInfo()

    @staticmethod
    def getEntityEventType(i):
        return str()

    @staticmethod
    def getEraInfo(i):
        return CvEraInfo()

    @staticmethod
    def getEspionageMissionInfo(i):
        return CvEspionageMissionInfo()

    @staticmethod
    def getEventInfo(i):
        return CvEventInfo()

    @staticmethod
    def getEventTriggerInfo(i):
        return CvEventTriggerInfo()

    @staticmethod
    def getFEATURE_GROWTH_MODIFIER():
        return int()

    @staticmethod
    def getFIELD_OF_VIEW():
        return float()

    @staticmethod
    def getFOOD_CONSUMPTION_PER_POPULATION():
        return int()

    @staticmethod
    def getFORTIFY_MODIFIER_PER_TURN():
        return int()

    @staticmethod
    def getFeatureArtInfo(i):
        return CvArtInfoFeature()

    @staticmethod
    def getFeatureInfo(i):
        return CvFeatureInfo()

    @staticmethod
    def getFlavorTypes(i):
        return str()

    @staticmethod
    def getForceControlInfo(i):
        return CvInfoBase()

    @staticmethod
    def getFunctionTypes(i):
        return str()

    @staticmethod
    def getGame():
        return CyGame()

    @staticmethod
    def getGameOptionInfo(i):
        return CvInfoBase()

    @staticmethod
    def getGameSpeedInfo(i):
        return CvGameSpeedInfo()

    @staticmethod
    def getGoodyInfo(i):
        return CvGoodyInfo()

    @staticmethod
    def getGraphicOptionsInfo(i):
        return CvGraphicOptionInfo()

    @staticmethod
    def getGraphicOptionsInfoByIndex(i):
        return CvGraphicOptionInfo()

    @staticmethod
    def getHILLS_EXTRA_DEFENSE():
        return int()

    @staticmethod
    def getHILLS_EXTRA_MOVEMENT():
        return int()

    @staticmethod
    def getHILLS_SEE_FROM_CHANGE():
        return int()

    @staticmethod
    def getHILLS_SEE_THROUGH_CHANGE():
        return int()

    @staticmethod
    def getHandicapInfo(i):
        return CvHandicapInfo()

    @staticmethod
    def getHints(i):
        return CvInfoBase()

    @staticmethod
    def getHurryInfo(i):
        return CvHurryInfo()

    @staticmethod
    def getINVALID_PLOT_COORD():
        return int()

    @staticmethod
    def getImprovementArtInfo(i):
        return CvArtInfoImprovement()

    @staticmethod
    def getImprovementInfo(i):
        return CvImprovementInfo()

    @staticmethod
    def getInfoTypeForString(szInfoType):
        return int()

    @staticmethod
    def getInterfaceArtInfo(i):
        return CvArtInfoInterface()

    @staticmethod
    def getLAKE_MAX_AREA_SIZE():
        return int()

    @staticmethod
    def getLeaderHeadInfo(i):
        return CvLeaderHeadInfo()

    @staticmethod
    def getLeaderheadArtInfo(i):
        return CvArtInfoLeaderhead()

    @staticmethod
    def getMAX_CITY_DEFENSE_DAMAGE():
        return int()

    @staticmethod
    def getMAX_CIV_PLAYERS():
        return int()

    @staticmethod
    def getMAX_CIV_TEAMS():
        return int()

    @staticmethod
    def getMAX_HIT_POINTS():
        return int()

    @staticmethod
    def getMAX_PLAYERS():
        return int()

    @staticmethod
    def getMAX_PLOT_LIST_ROWS():
        return int()

    @staticmethod
    def getMAX_TEAMS():
        return int()

    @staticmethod
    def getMIN_CITY_RANGE():
        return int()

    @staticmethod
    def getMIN_WATER_SIZE_FOR_OCEAN():
        return int()

    @staticmethod
    def getMOVE_DENOMINATOR():
        return int()

    @staticmethod
    def getMPOptionInfo(i):
        return CvInfoBase()

    @staticmethod
    def getMainMenus(i):
        return CvMainMenuInfo()

    @staticmethod
    def getMap():
        return CyMap()

    @staticmethod
    def getMemoryInfo(i):
        return CvInfoBase()

    @staticmethod
    def getMiscArtInfo(i):
        return CvArtInfoMisc()

    @staticmethod
    def getMissionInfo(i):
        return CvMissionInfo()

    @staticmethod
    def getMonthInfo(i):
        return CvInfoBase()

    @staticmethod
    def getMovieArtInfo(i):
        return CvArtInfoMovie()

    @staticmethod
    def getNUM_AND_TECH_PREREQS():
        return int()

    @staticmethod
    def getNUM_BUILDING_AND_TECH_PREREQS():
        return int()

    @staticmethod
    def getNUM_BUILDING_PREREQ_OR_BONUSES():
        return int()

    @staticmethod
    def getNUM_CITY_PLOTS():
        return int()

    @staticmethod
    def getNUM_CORPORATION_PREREQ_BONUSES():
        return int()

    @staticmethod
    def getNUM_OR_TECH_PREREQS():
        return int()

    @staticmethod
    def getNUM_ROUTE_PREREQ_OR_BONUSES():
        return int()

    @staticmethod
    def getNUM_UNIT_AND_TECH_PREREQS():
        return int()

    @staticmethod
    def getNUM_UNIT_PREREQ_OR_BONUSES():
        return int()

    @staticmethod
    def getNewConceptInfo(i):
        return CvInfoBase()

    @staticmethod
    def getNumActionInfos():
        return int()

    @staticmethod
    def getNumAnimationOperatorTypes():
        return int()

    @staticmethod
    def getNumArtStyleTypes():
        return int()

    @staticmethod
    def getNumAutomateInfos():
        return int()

    @staticmethod
    def getNumBonusArtInfos():
        return int()

    @staticmethod
    def getNumBonusInfos():
        return int()

    @staticmethod
    def getNumBuildInfos():
        return int()

    @staticmethod
    def getNumBuildingArtInfos():
        return int()

    @staticmethod
    def getNumBuildingClassInfos():
        return int()

    @staticmethod
    def getNumBuildingInfos():
        return int()

    @staticmethod
    def getNumCalendarInfos():
        return int()

    @staticmethod
    def getNumCitySizeTypes():
        return int()

    @staticmethod
    def getNumCityTabInfos():
        return int()

    @staticmethod
    def getNumCivicInfos():
        return int()

    @staticmethod
    def getNumCivicOptionInfos():
        return int()

    @staticmethod
    def getNumCivilizationArtInfos():
        return int()

    @staticmethod
    def getNumCivilizationInfos():
        return int()

    @staticmethod
    def getNumClimateInfos():
        return int()

    @staticmethod
    def getNumCommandInfos():
        return int()

    @staticmethod
    def getNumConceptInfos():
        return int()

    @staticmethod
    def getNumControlInfos():
        return int()

    @staticmethod
    def getNumCorporationInfos():
        return int()

    @staticmethod
    def getNumCultureLevelInfos():
        return int()

    @staticmethod
    def getNumDenialInfos():
        return int()

    @staticmethod
    def getNumDiplomacyInfos():
        return int()

    @staticmethod
    def getNumEffectInfos():
        return int()

    @staticmethod
    def getNumEmphasizeInfos():
        return int()

    @staticmethod
    def getNumEntityEventTypes():
        return int()

    @staticmethod
    def getNumEraInfos():
        return int()

    @staticmethod
    def getNumEspionageMissionInfos():
        return int()

    @staticmethod
    def getNumEventInfos():
        return int()

    @staticmethod
    def getNumEventTriggerInfos():
        return int()

    @staticmethod
    def getNumFeatureArtInfos():
        return int()

    @staticmethod
    def getNumFeatureInfos():
        return int()

    @staticmethod
    def getNumFlavorTypes():
        return int()

    @staticmethod
    def getNumForceControlInfos():
        return int()

    @staticmethod
    def getNumGameOptionInfos():
        return int()

    @staticmethod
    def getNumGameSpeedInfos():
        return int()

    @staticmethod
    def getNumGoodyInfos():
        return int()

    @staticmethod
    def getNumHandicapInfos():
        return int()

    @staticmethod
    def getNumHints():
        return int()

    @staticmethod
    def getNumHurryInfos():
        return int()

    @staticmethod
    def getNumImprovementArtInfos():
        return int()

    @staticmethod
    def getNumImprovementInfos():
        return int()

    @staticmethod
    def getNumInterfaceArtInfos():
        return int()

    @staticmethod
    def getNumLeaderHeadInfos():
        return int()

    @staticmethod
    def getNumLeaderheadArtInfos():
        return int()

    @staticmethod
    def getNumMPOptionInfos():
        return int()

    @staticmethod
    def getNumMainMenus():
        return int()

    @staticmethod
    def getNumMiscArtInfos():
        return int()

    @staticmethod
    def getNumMissionInfos():
        return int()

    @staticmethod
    def getNumMonthInfos():
        return int()

    @staticmethod
    def getNumMovieArtInfos():
        return int()

    @staticmethod
    def getNumNewConceptInfos():
        return int()

    @staticmethod
    def getNumPlayableCivilizationInfos():
        return int()

    @staticmethod
    def getNumPlayerColorInfos():
        return int()

    @staticmethod
    def getNumPlayerOptionInfos():
        return int()

    @staticmethod
    def getNumProcessInfos():
        return int()

    @staticmethod
    def getNumProjectInfos():
        return int()

    @staticmethod
    def getNumPromotionInfos():
        return int()

    @staticmethod
    def getNumQuestInfos():
        return int()

    @staticmethod
    def getNumReligionInfos():
        return int()

    @staticmethod
    def getNumRouteInfos():
        return int()

    @staticmethod
    def getNumSeaLevelInfos():
        return int()

    @staticmethod
    def getNumSeasonInfos():
        return int()

    @staticmethod
    def getNumSpecialBuildingInfos():
        return int()

    @staticmethod
    def getNumSpecialUnitInfos():
        return int()

    @staticmethod
    def getNumSpecialistInfos():
        return int()

    @staticmethod
    def getNumTechInfos():
        return int()

    @staticmethod
    def getNumTerrainArtInfos():
        return int()

    @staticmethod
    def getNumTerrainInfos():
        return int()

    @staticmethod
    def getNumTraitInfos():
        return int()

    @staticmethod
    def getNumTurnTimerInfos():
        return int()

    @staticmethod
    def getNumTutorialInfos():
        return int()

    @staticmethod
    def getNumUnitArtInfos():
        return int()

    @staticmethod
    def getNumUnitArtStyleTypeInfos():
        return int()

    @staticmethod
    def getNumUnitClassInfos():
        return int()

    @staticmethod
    def getNumUnitCombatInfos():
        return int()

    @staticmethod
    def getNumUnitInfos():
        return int()

    @staticmethod
    def getNumUpkeepInfos():
        return int()

    @staticmethod
    def getNumVictoryInfos():
        return int()

    @staticmethod
    def getNumVoteInfos():
        return int()

    @staticmethod
    def getNumVoteSourceInfos():
        return int()

    @staticmethod
    def getNumWorldInfos():
        return int()

    @staticmethod
    def getPEAK_SEE_FROM_CHANGE():
        return int()

    @staticmethod
    def getPEAK_SEE_THROUGH_CHANGE():
        return int()

    @staticmethod
    def getPERCENT_ANGER_DIVISOR():
        return int()

    @staticmethod
    def getPLOT_SIZE():
        return float()

    @staticmethod
    def getPlayer(idx):
        return CyPlayer()

    @staticmethod
    def getPlayerColorInfo(i):
        return CvPlayerColorInfo()

    @staticmethod
    def getPlayerOptionsInfo(i):
        return CvPlayerOptionInfo()

    @staticmethod
    def getPlayerOptionsInfoByIndex(i):
        return CvPlayerOptionInfo()

    @staticmethod
    def getProcessInfo(i):
        return CvProcessInfo()

    @staticmethod
    def getProjectInfo(i):
        return CvProjectInfo()

    @staticmethod
    def getPromotionInfo(i):
        return CvPromotionInfo()

    @staticmethod
    def getQuestInfo(i):
        return CvQuestInfo()

    @staticmethod
    def getRIVER_ATTACK_MODIFIER():
        return int()

    @staticmethod
    def getROUTE_FEATURE_GROWTH_MODIFIER():
        return int()

    @staticmethod
    def getReligionInfo(i):
        return CvReligionInfo()

    @staticmethod
    def getRouteInfo(i):
        return CvRouteInfo()

    @staticmethod
    def getSEAWATER_SEE_FROM_CHANGE():
        return int()

    @staticmethod
    def getSHADOW_SCALE():
        return float()

    @staticmethod
    def getSeaLevelInfo(i):
        return CvSeaLevelInfo()

    @staticmethod
    def getSeasonInfo(i):
        return CvInfoBase()

    @staticmethod
    def getSpecialBuildingInfo(i):
        return CvSpecialBuildingInfo()

    @staticmethod
    def getSpecialUnitInfo(i):
        return CvSpecialUnitInfo()

    @staticmethod
    def getSpecialistInfo(i):
        return CvSpecialistInfo()

    @staticmethod
    def getTeam(i):
        return CyTeam()

    @staticmethod
    def getTechInfo(i):
        return CvTechInfo()

    @staticmethod
    def getTerrainArtInfo(i):
        return CvArtInfoTerrain()

    @staticmethod
    def getTerrainInfo(i):
        return CvTerrainInfo()

    @staticmethod
    def getTraitInfo(i):
        return CvTraitInfo()

    @staticmethod
    def getTurnTimerInfo(i):
        return CvTurnTimerInfo()

    @staticmethod
    def getTutorialInfo(i):
        return CvTutorialInfo()

    @staticmethod
    def getTypesEnum(szType):
        return int()

    @staticmethod
    def getUNIT_MULTISELECT_DISTANCE():
        return float()

    @staticmethod
    def getUNIT_MULTISELECT_MAX():
        return int()

    @staticmethod
    def getUSE_SPIES_NO_ENTER_BORDERS():
        return int()

    @staticmethod
    def getUnitAIInfo(i):
        return CvInfoBase()

    @staticmethod
    def getUnitArtInfo(i):
        return CvArtInfoUnit()

    @staticmethod
    def getUnitArtStyleTypeInfo(i):
        return CvUnitArtStyleTypeInfo()

    @staticmethod
    def getUnitClassInfo(i):
        return CvUnitClassInfo()

    @staticmethod
    def getUnitCombatInfo(i):
        return CvInfoBase()

    @staticmethod
    def getUnitInfo(i):
        return CvUnitInfo()

    @staticmethod
    def getUpkeepInfo(i):
        return CvUpkeepInfo()

    @staticmethod
    def getVictoryInfo(i):
        return CvVictoryInfo()

    @staticmethod
    def getVoteInfo(i):
        return CvVoteInfo()

    @staticmethod
    def getVoteSourceInfo(i):
        return CvVoteSourceInfo()

    @staticmethod
    def getWorldInfo(i):
        return CvWorldInfo()

    @staticmethod
    def getYieldInfo(i):
        return CvYieldInfo()

    @staticmethod
    def isDebugBuild():
        return bool()

    @staticmethod
    def setDefineFLOAT(szName, fValue):
        pass

    @staticmethod
    def setDefineINT(szName, iValue):
        pass

    @staticmethod
    def setDefineSTRING(szName, szValue):
        pass

    if PB_MOD:
        @staticmethod
        def getAltrootDir():
            return str()

        @staticmethod
        def sendPause(iPlayer):
            pass

        @staticmethod
        def sendChat(sMsg, eChatTargetType):
            pass


class CyGlobeLayer:

    @staticmethod
    def getButtonStyle():
        return str()

    @staticmethod
    def getCurrentOption():
        return int()

    @staticmethod
    def getName():
        return str()

    @staticmethod
    def getNumOptions():
        return int()

    @staticmethod
    def getOptionButton(iOptionID):
        return str()

    @staticmethod
    def getOptionName(iOptionID):
        return str()

    @staticmethod
    def isGlobeviewRequired():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def needsPlayerFilter():
        return bool()

    @staticmethod
    def registerGlobeLayer():
        pass

    @staticmethod
    def shouldCitiesZoom():
        return bool()


class CyGlobeLayerManager:

    @staticmethod
    def getCurrentLayer():
        return CyGlobeLayer()

    @staticmethod
    def getCurrentLayerID():
        return int()

    @staticmethod
    def getCurrentLayerName():
        return str()

    @staticmethod
    def getLayer(i):
        return CyGlobeLayer()

    @staticmethod
    def getLayerID(layer):
        return int()

    @staticmethod
    def getNumLayers():
        return int()

    @staticmethod
    def setCurrentLayer():
        pass


class CyHallOfFameInfo:

    @staticmethod
    def getNumGames():
        return int()

    @staticmethod
    def getReplayInfo(i):
        return CyReplayInfo()

    @staticmethod
    def loadReplays():
        pass


class CyInterface:

    @staticmethod
    def DoSoundtrack(szSoundtrackScript):
        return bool()

    @staticmethod
    def addCombatMessage(ePlayer, szString):
        pass

    @staticmethod
    def addImmediateMessage(szString, szSound):
        pass

    @staticmethod
    def addMessage(ePlayer, bForce, iLength, szString, szSound, eType, szIcon, eFlashColor, iFlashX, iFlashY, bShowOffScreenArrows, bShowOnScreenArrows):
        pass

    @staticmethod
    def addQuestMessage(ePlayer, szString):
        pass

    @staticmethod
    def addSelectedCity(pNewValue):
        pass

    @staticmethod
    def cacheInterfacePlotUnits(pPlot):
        pass

    @staticmethod
    def canCreateGroup():
        return bool()

    @staticmethod
    def canDeleteGroup():
        return bool()

    @staticmethod
    def canHandleAction(iAction, bTestVisible):
        return bool()

    @staticmethod
    def canSelectHeadUnit():
        return bool()

    @staticmethod
    def checkFlashReset(ePlayer):
        pass

    @staticmethod
    def checkFlashUpdate():
        return bool()

    @staticmethod
    def clearSelectedCities():
        pass

    @staticmethod
    def clearSelectionList():
        pass

    @staticmethod
    def countEntities(iI):
        return int()

    @staticmethod
    def determineWidth(szBuffer):
        return int()

    @staticmethod
    def doPing(iX, iY, ePlayer):
        pass

    @staticmethod
    def endTimer(szOutputText):
        pass

    @staticmethod
    def exitingToMainMenu(szLoadFile):
        pass

    @staticmethod
    def getActionsToShow():
        return tuple()

    @staticmethod
    def getCachedInterfacePlotUnit(iIndex):
        return CyUnit()

    @staticmethod
    def getCityTabSelectionRow():
        return int()

    @staticmethod
    def getCursorPlot():
        return CyPlot()

    @staticmethod
    def getEndTurnState():
        return -1

    @staticmethod
    def getGotoPlot():
        return CyPlot()

    @staticmethod
    def getHeadSelectedCity():
        return CyCity()

    @staticmethod
    def getHeadSelectedUnit():
        return CyUnit()

    @staticmethod
    def getHelpString():
        return str()

    @staticmethod
    def getHighlightPlot():
        return CyPlot()

    @staticmethod
    def getInterfaceMode():
        return -1  # Type

    @staticmethod
    def getInterfacePlotUnit():
        return CyUnit()

    @staticmethod
    def getLengthSelectionList():
        return int()

    @staticmethod
    def getMouseOverPlot():
        return CyPlot()

    @staticmethod
    def getMousePos():
        return POINT()

    @staticmethod
    def getNumCachedInterfacePlotUnits():
        return int()

    @staticmethod
    def getNumOrdersQueued():
        return int()

    @staticmethod
    def getNumVisibleUnits():
        return int()

    @staticmethod
    def getOrderNodeData1(iNode):
        return int()

    @staticmethod
    def getOrderNodeData2(iNode):
        return int()

    @staticmethod
    def getOrderNodeSave(iNode):
        return bool()

    @staticmethod
    def getOrderNodeType(iNode):
        return -1  # Type

    @staticmethod
    def getPlotListColumn():
        return int()

    @staticmethod
    def getPlotListOffset():
        return int()

    @staticmethod
    def getSelectionPlot():
        return CyPlot()

    @staticmethod
    def getSelectionUnit():
        return CyUnit()

    @staticmethod
    def getShowInterface():
        return -1

    @staticmethod
    def insertIntoSelectionList(pUnit, bClear, bToggle, bGroup, bSound):
        pass

    @staticmethod
    def isCityScreenUp():
        return bool()

    @staticmethod
    def isCitySelected(pCity):
        return bool()

    @staticmethod
    def isCitySelection():
        return bool()

    @staticmethod
    def isDirty(eDirty):
        return bool()

    @staticmethod
    def isFlashing():
        return bool()

    @staticmethod
    def isFlashingPlayer(iPlayer):
        return bool()

    @staticmethod
    def isFocusedWidget():
        return bool()

    @staticmethod
    def isFocused():
        return bool()

    @staticmethod
    def isInAdvancedStart():
        return bool()

    @staticmethod
    def isInMainMenu():
        return bool()

    @staticmethod
    def isLeftMouseDown():
        return bool()

    @staticmethod
    def isNetStatsVisible():
        return bool()

    @staticmethod
    def isOOSVisible():
        return bool()

    @staticmethod
    def isOneCitySelected():
        return bool()

    @staticmethod
    def isRightMouseDown():
        return bool()

    @staticmethod
    def isScoresMinimized():
        return bool()

    @staticmethod
    def isScoresVisible():
        return bool()

    @staticmethod
    def isScreenUp(iEnumVal):
        return bool()

    @staticmethod
    def isUnitFocus():
        return bool()

    @staticmethod
    def isYieldVisibleMode():
        return bool()

    @staticmethod
    def lookAtCityBuilding(iCity, iBuilding):
        pass

    @staticmethod
    def lookAtCityOffset(iCity):
        pass

    @staticmethod
    def makeInterfaceDirty():
        pass

    @staticmethod
    def mirrorsSelectionGroup():
        return bool()

    @staticmethod
    def noTechSplash():
        return bool()

    @staticmethod
    def playAdvisorSound(pszSound):
        pass

    @staticmethod
    def playGeneralSound(pszSound):
        pass

    @staticmethod
    def playGeneralSoundAtPlot(iScriptID, pPlot):
        pass

    @staticmethod
    def playGeneralSoundByID(iScriptID):
        pass

    @staticmethod
    def removeFromSelectionList(pUnit):
        pass

    @staticmethod
    def selectAll(pPlot):
        pass

    @staticmethod
    def selectCity(pNewValue, bTestProduction):
        pass

    @staticmethod
    def selectGroup(pUnit, bShift, bCtrl, bAlt):
        pass

    @staticmethod
    def selectHotKeyUnit(iHotKeyNumber):
        return int()

    @staticmethod
    def selectUnit(pUnit, bClear, bToggle, bSound):
        pass

    @staticmethod
    def setBusy(bBusy):
        pass

    @staticmethod
    def setCityTabSelectionRow(eIndex):
        pass

    @staticmethod
    def setDirty(eDirty, bDirty):
        pass

    @staticmethod
    def setInterfaceMode(eMode):
        pass

    @staticmethod
    def setPausedPopups(bPausedPopups):
        pass

    @staticmethod
    def setShowInterface(eInterfaceVisibility):
        pass

    @staticmethod
    def setSoundSelectionReady(bReady):
        pass

    @staticmethod
    def setWorldBuilder(bTurnOn):
        pass

    @staticmethod
    def shiftKey():
        return bool()

    @staticmethod
    def shouldDisplayEndTurn():
        return bool()

    @staticmethod
    def shouldDisplayEndTurnButton():
        return bool()

    @staticmethod
    def shouldDisplayFlag():
        return bool()

    @staticmethod
    def shouldDisplayReturn():
        return bool()

    @staticmethod
    def shouldDisplayUnitModel():
        return bool()

    @staticmethod
    def shouldDisplayWaitingOthers():
        return bool()

    @staticmethod
    def shouldDisplayWaitingYou():
        return bool()

    @staticmethod
    def shouldFlash(iPlayer):
        return bool()

    @staticmethod
    def shouldShowAction(iAction):
        return bool()

    @staticmethod
    def shouldShowChangeResearchButton():
        return bool()

    @staticmethod
    def shouldShowResearchButtons():
        return bool()

    @staticmethod
    def shouldShowSelectionButtons():
        return bool()

    @staticmethod
    def shouldShowYieldVisibleButton():
        return bool()

    @staticmethod
    def startTimer():
        pass

    @staticmethod
    def stop2DSound():
        pass

    @staticmethod
    def stopAdvisorSound():
        pass

    @staticmethod
    def toggleBareMapMode():
        pass

    @staticmethod
    def toggleMusicOn():
        pass

    @staticmethod
    def toggleNetStatsVisible():
        pass

    @staticmethod
    def toggleScoresMinimized():
        pass

    @staticmethod
    def toggleScoresVisible():
        pass

    @staticmethod
    def toggleYieldVisibleMode():
        pass


class CyMap:

    @staticmethod
    def calculatePathDistance(pSource, pDest):
        return int()

    @staticmethod
    def erasePlots():
        pass

    @staticmethod
    def findBiggestArea(bWater):
        return CyArea()

    @staticmethod
    def findCity(iX, iY, eOwner, eTeam, bSameArea, bCoastalOnly, eTeamAtWarWith, eDirection, pSkipCity):
        return CyCity()

    @staticmethod
    def findSelectionGroup(iX, iY, eOwner, bReadyToSelect, bWorkers):
        return CySelectionGroup()

    @staticmethod
    def findWater(pPlot, iRange, bFreshWater):
        return bool()

    @staticmethod
    def getArea(iID):
        return CyArea()

    @staticmethod
    def getBottomLatitude():
        return int()

    @staticmethod
    def getClimate():
        return -1  # Type

    @staticmethod
    def getCustomMapOption(iOption):
        return -1  # Type

    @staticmethod
    def getGridHeight():
        return int()

    @staticmethod
    def getGridWidth():
        return int()

    @staticmethod
    def getIndexAfterLastArea():
        return int()

    @staticmethod
    def getLandPlots():
        return int()

    @staticmethod
    def getMapFractalFlags():
        return int()

    @staticmethod
    def getMapScriptName():
        return str()

    @staticmethod
    def getNextRiverID():
        return int()

    @staticmethod
    def getNumAreas():
        return int()

    @staticmethod
    def getNumBonuses(eIndex):
        return int()

    @staticmethod
    def getNumBonusesOnLand(eIndex):
        return int()

    @staticmethod
    def getNumCustomMapOptions():
        return int()

    @staticmethod
    def getCustomMapOptionName(iOption, sMapName):
        return str()

    @staticmethod
    def getNumCustomMapOptionValues(iOption, sMapName):
        return int()

    @staticmethod
    def getCustomMapOptionDescAt(iOption, iValue, sMapName):
        return str()

    @staticmethod
    def getNumLandAreas():
        return int()

    @staticmethod
    def getOwnedPlots():
        return int()

    @staticmethod
    def getSeaLevel():
        return -1  # Type

    @staticmethod
    def getTopLatitude():
        return int()

    @staticmethod
    def getWorldSize():
        return -1  # Type

    @staticmethod
    def incrementNextRiverID():
        pass

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isPlot(iX, iY):
        return bool()

    @staticmethod
    def isWrapX():
        return bool()

    @staticmethod
    def isWrapY():
        return bool()

    @staticmethod
    def numPlots():
        return int()

    @staticmethod
    def plot(iX, iY):
        return CyPlot()

    @staticmethod
    def plotByIndex(iIndex):
        return CyPlot()

    @staticmethod
    def plotNum(iX, iY):
        return int()

    @staticmethod
    def plotX(iIndex):
        return int()

    @staticmethod
    def plotY(iIndex):
        return int()

    @staticmethod
    def pointToPlot(fX, fY):
        return CyPlot()

    @staticmethod
    def rebuild(iGridW, iGridH, iTopLatitude, iBottomLatitude, bWrapX, bWrapY, eWorldSize, eClimate, eSeaLevel, iNumCustomMapOptions, aeCustomMapOptions):
        pass

    @staticmethod
    def recalculateAreas():
        pass

    @staticmethod
    def regenerateGameElements():
        pass

    @staticmethod
    def resetPathDistance():
        pass

    @staticmethod
    def sPlot(iX, iY):
        return CyPlot()

    @staticmethod
    def sPlotByIndex(iIndex):
        return CyPlot()

    @staticmethod
    def setAllPlotTypes(ePlotType):
        pass

    @staticmethod
    def setRevealedPlots(eTeam, bNewValue, bTerrainOnly):
        pass

    @staticmethod
    def syncRandPlot(iFlags, iArea, iMinUnitDistance, iTimeout):
        return CyPlot()

    @staticmethod
    def updateFog():
        pass

    @staticmethod
    def updateMinOriginalStartDist(pArea):
        pass

    @staticmethod
    def updateMinimapColor():
        pass

    @staticmethod
    def updateVisibility():
        pass


class CyMapGenerator:

    @staticmethod
    def addBonuses():
        pass

    @staticmethod
    def addFeatures():
        pass

    @staticmethod
    def addGameElements():
        pass

    @staticmethod
    def addGoodies():
        pass

    @staticmethod
    def addLakes():
        pass

    @staticmethod
    def addNonUniqueBonusType(eBonusType):
        pass

    @staticmethod
    def addRivers():
        pass

    @staticmethod
    def addUniqueBonusType(eBonusType):
        pass

    @staticmethod
    def afterGeneration():
        pass

    @staticmethod
    def canPlaceBonusAt(eBonus, iX, iY, bIgnoreLatitude):
        return bool()

    @staticmethod
    def canPlaceGoodyAt(eImprovement, iX, iY):
        return bool()

    @staticmethod
    def doRiver(pStartPlot, eCardinalDirection):
        pass

    @staticmethod
    def eraseBonuses():
        pass

    @staticmethod
    def eraseFeatures():
        pass

    @staticmethod
    def eraseGoodies():
        pass

    @staticmethod
    def eraseRivers():
        pass

    @staticmethod
    def generatePlotTypes():
        pass

    @staticmethod
    def generateRandomMap():
        pass

    @staticmethod
    def generateTerrain():
        pass

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def setPlotTypes(listPlotTypes):
        pass


class CyMessageControl:

    @staticmethod
    def GetConnState(iPlayer):
        return int()

    @staticmethod
    def GetFirstBadConnection():
        return int()

    @staticmethod
    def sendAdvancedStartAction(eAction, ePlayer, iX, iY, iData, bAdd):
        pass

    @staticmethod
    def sendApplyEvent(iContextID, eContextType, userData):
        return bool()

    @staticmethod
    def sendConvert(iReligion):
        pass

    @staticmethod
    def sendDoTask(iCity, eTask, iData1, iData2, bOption, bAlt, bShift, bCtrl):
        pass

    @staticmethod
    def sendEmpireSplit(ePlayer, iAreaId):
        pass

    @staticmethod
    def sendEspionageSpendingWeightChange(eTargetTeam, iChange):
        pass

    @staticmethod
    def sendModNetMessage(iData1, iData2, iData3, iData4, iData5):
        pass

    @staticmethod
    def sendPlayerOption(eOption, bValue):
        pass

    @staticmethod
    def sendPushOrder(iCityID, eOrder, iData, bAlt, bShift, bCtrl):
        pass

    @staticmethod
    def sendResearch(eTech, bShift):
        pass

    @staticmethod
    def sendTurnComplete():
        pass

    @staticmethod
    def sendUpdateCivics(iCivics):
        pass

    if PB_MOD:
        @staticmethod
        def sendTurnCompleteAll():
            pass

class CyPlayer:

    @staticmethod
    def AI_changeAttitudeExtra(eIndex, iChange):
        pass

    @staticmethod
    def AI_changeMemoryCount(eIndex1, eIndex2, iChange):
        pass

    @staticmethod
    def AI_civicValue(eCivic):
        return int()

    @staticmethod
    def AI_demandRebukedWar(ePlayer):
        return bool()

    @staticmethod
    def AI_foundValue(iX, iY, iMinUnitRange, bStartingLoc):
        return int()

    @staticmethod
    def AI_getAttitude(ePlayer):
        return -1  # Type

    @staticmethod
    def AI_getAttitudeExtra(eIndex):
        return int()

    @staticmethod
    def AI_getExtraGoldTarget():
        return int()

    @staticmethod
    def AI_getMemoryCount(eIndex1, eIndex2):
        return int()

    @staticmethod
    def AI_getNumAIUnits(eIndex):
        return int()

    @staticmethod
    def AI_isFinancialTrouble():
        return bool()

    @staticmethod
    def AI_maxGoldPerTurnTrade(iPlayer):
        return int()

    @staticmethod
    def AI_maxGoldTrade(iPlayer):
        return int()

    @staticmethod
    def AI_setAttitudeExtra(eIndex, iNewValue):
        pass

    @staticmethod
    def AI_setExtraGoldTarget(iNewValue):
        pass

    @staticmethod
    def AI_totalAreaUnitAIs(pArea, eUnitAI):
        return int()

    @staticmethod
    def AI_totalUnitAIs(eUnitAI):
        return int()

    @staticmethod
    def AI_totalWaterAreaUnitAIs(pArea, eUnitAI):
        return int()

    @staticmethod
    def AI_unitValue(eUnit, eUnitAI, pArea):
        return int()

    @staticmethod
    def AI_updateFoundValues(bStartingLoc):
        pass

    @staticmethod
    def acquireCity(pCity, bConquest, bTrade):
        pass

    @staticmethod
    def addCityName(szName):
        pass

    @staticmethod
    def calculateBaseNetResearch():
        return int()

    @staticmethod
    def calculateGoldRate():
        return int()

    @staticmethod
    def calculateInflatedCosts():
        return int()

    @staticmethod
    def calculateInflationRate():
        return int()

    @staticmethod
    def calculatePreInflatedCosts():
        return int()

    @staticmethod
    def calculateResearchModifier(eTech):
        return int()

    @staticmethod
    def calculateResearchRate(eTech):
        return int()

    @staticmethod
    def calculateTotalCityHappiness():
        return int()

    @staticmethod
    def calculateTotalCityHealthiness():
        return int()

    @staticmethod
    def calculateTotalCityUnhappiness():
        return int()

    @staticmethod
    def calculateTotalCityUnhealthiness():
        return int()

    @staticmethod
    def calculateTotalCommerce():
        return int()

    @staticmethod
    def calculateTotalExports(eYield):
        return int()

    @staticmethod
    def calculateTotalImports(eYield):
        return int()

    @staticmethod
    def calculateTotalYield(eYield):
        return int()

    @staticmethod
    def calculateUnitCost():
        return int()

    @staticmethod
    def calculateUnitSupply():
        return int()

    @staticmethod
    def canBuild(pPlot, eBuild, bTestEra, bTestVisible):
        return bool()

    @staticmethod
    def canChangeReligion():
        return bool()

    @staticmethod
    def canConstruct(eBuilding, bContinue, bTestVisible, bIgnoreCost):
        return bool()

    @staticmethod
    def canContact(ePlayer):
        return bool()

    @staticmethod
    def canConvert(iIndex):
        return bool()

    @staticmethod
    def canCreate(eProject, bContinue, bTestVisible):
        return bool()

    @staticmethod
    def canDoCivics(eCivic):
        return bool()

    @staticmethod
    def canDoEspionageMission(eMission, eTargetPlayer, pPlot, iExtraData):
        return bool()

    @staticmethod
    def canDoReligion(eReligion):
        return bool()

    @staticmethod
    def canEverResearch(eTech):
        return bool()

    @staticmethod
    def canFound(iX, iY):
        return bool()

    @staticmethod
    def canHaveTradeRoutesWith(iPlayer):
        return bool()

    @staticmethod
    def canHurry(eIndex):
        return bool()

    @staticmethod
    def canMaintain(eProcess, bContinue):
        return bool()

    @staticmethod
    def canRaze(pCity):
        return bool()

    @staticmethod
    def canReceiveGoody(pPlot, eGoody, pUnit):
        return bool()

    @staticmethod
    def canResearch(eTech, bTrade):
        return bool()

    @staticmethod
    def canRevolution(paeNewCivics):
        return bool()

    @staticmethod
    def canSplitArea(iAreaId):
        return bool()

    @staticmethod
    def canSplitEmpire():
        return bool()

    @staticmethod
    def canStopTradingWithTeam(eTeam):
        return bool()

    @staticmethod
    def canTradeItem(eWhoTo, item, bTestDenial):
        return bool()

    @staticmethod
    def canTradeNetworkWith(iPlayer):
        return bool()

    @staticmethod
    def canTradeWith(eWhoTo):
        return bool()

    @staticmethod
    def canTrain(eUnit, bContinue, bTestVisible):
        return bool()

    @staticmethod
    def changeAdvancedStartPoints(iChange):
        pass

    @staticmethod
    def changeAnarchyTurns(iChange):
        pass

    @staticmethod
    def changeAssets(iChange):
        pass

    @staticmethod
    def changeCoastalTradeRoutes(iChange):
        pass

    @staticmethod
    def changeCombatExperience(iChange):
        pass

    @staticmethod
    def changeCommercePercent(eIndex, iChange):
        pass

    @staticmethod
    def changeConscriptCount(iChange):
        pass

    @staticmethod
    def changeEspionageSpendingWeightAgainstTeam(eIndex, iChange):
        pass

    @staticmethod
    def changeExtraHappiness(iChange):
        pass

    @staticmethod
    def changeGold(iChange):
        pass

    @staticmethod
    def changeGoldenAgeTurns(iChange):
        pass

    @staticmethod
    def changeNumUnitGoldenAges(iChange):
        pass

    @staticmethod
    def changeStateReligionBuildingProductionModifier(iChange):
        pass

    @staticmethod
    def changeStateReligionUnitProductionModifier(iChange):
        pass

    @staticmethod
    def chooseTech(iDiscover, szText, bFront):
        pass

    @staticmethod
    def clearResearchQueue():
        pass

    @staticmethod
    def contact(ePlayer):
        pass

    @staticmethod
    def convert(iIndex):
        pass

    @staticmethod
    def countCityFeatures(eFeature):
        return int()

    @staticmethod
    def countCorporations(eCorporation):
        return int()

    @staticmethod
    def countHeadquarters():
        return int()

    @staticmethod
    def countHolyCities():
        return int()

    @staticmethod
    def countNumBuildings(eBuilding):
        return int()

    @staticmethod
    def countNumCoastalCities():
        return int()

    @staticmethod
    def countNumCoastalCitiesByArea(pArea):
        return int()

    @staticmethod
    def countOwnedBonuses(eBonus):
        return int()

    @staticmethod
    def countPotentialForeignTradeCities(pIgnoreArea):
        return int()

    @staticmethod
    def countPotentialForeignTradeCitiesConnected():
        return int()

    @staticmethod
    def countTotalCulture():
        return int()

    @staticmethod
    def countTotalHasCorporation():
        return int()

    @staticmethod
    def countTotalHasReligion():
        return int()

    @staticmethod
    def countUnimprovedBonuses(pArea, pFromPlot):
        return int()

    @staticmethod
    def createGreatPeople(eGreatPersonUnit, bIncrementThreshold, bIncrementExperience, iX, iY):
        pass

    @staticmethod
    def disband(pCity):
        pass

    @staticmethod
    def disbandUnit(bAnnounce):
        pass

    @staticmethod
    def doEspionageMission(eMission, eTargetPlayer, pPlot, iExtraData, pUnit):
        pass

    @staticmethod
    def doGoody(pPlot, pUnit):
        pass

    @staticmethod
    def findBestFoundValue():
        return int()

    @staticmethod
    def findHighestHasReligionCount():
        return int()

    @staticmethod
    def findNewCapital():
        pass

    @staticmethod
    def findPathLength(eTech, bCost):
        return int()

    @staticmethod
    def findStartingPlot(bRandomize):
        return CyPlot()

    @staticmethod
    def firstCity(bRev):
        return tuple()

    @staticmethod
    def firstSelectionGroup(bRev):
        return tuple()

    @staticmethod
    def firstUnit(bRev):
        return tuple()

    @staticmethod
    def forcePeace(iPlayer):
        pass

    @staticmethod
    def found(iX, iY):
        pass

    @staticmethod
    def foundCorporation(eCorporation):
        pass

    @staticmethod
    def foundReligion(eReligion, iSlotReligion, bAward):
        pass

    @staticmethod
    def getAdvancedStartBuildingCost(eBuilding, bAdd, pCity):
        return int()

    @staticmethod
    def getAdvancedStartCityCost(bAdd, pPlot):
        return int()

    @staticmethod
    def getAdvancedStartCultureCost(bAdd, pCity):
        return int()

    @staticmethod
    def getAdvancedStartImprovementCost(eImprovement, bAdd, pPlot):
        return int()

    @staticmethod
    def getAdvancedStartPoints():
        return int()

    @staticmethod
    def getAdvancedStartPopCost(bAdd, pCity):
        return int()

    @staticmethod
    def getAdvancedStartRouteCost(eRoute, bAdd, pPlot):
        return int()

    @staticmethod
    def getAdvancedStartTechCost(eTech, bAdd):
        return int()

    @staticmethod
    def getAdvancedStartUnitCost(eUnit, bAdd, pPlot):
        return int()

    @staticmethod
    def getAdvancedStartVisibilityCost(bAdd, pPlot):
        return int()

    @staticmethod
    def getAgricultureHistory(iTurn):
        return int()

    @staticmethod
    def getAnarchyModifier():
        return int()

    @staticmethod
    def getAnarchyTurns():
        return int()

    @staticmethod
    def getArtStyleType():
        return -1  # Type

    @staticmethod
    def getAssets():
        return int()

    @staticmethod
    def getAveragePopulation():
        return int()

    @staticmethod
    def getBaseFreeMilitaryUnits():
        return int()

    @staticmethod
    def getBaseFreeUnits():
        return int()

    @staticmethod
    def getBestAttackUnitKey():
        return str()

    @staticmethod
    def getBestAttackUnitName(iForm):
        return str()

    @staticmethod
    def getBonusExport(iIndex):
        return int()

    @staticmethod
    def getBonusImport(iIndex):
        return int()

    @staticmethod
    def getBuildingBadHealth():
        return int()

    @staticmethod
    def getBuildingClassCount(iIndex):
        return int()

    @staticmethod
    def getBuildingClassCountPlusMaking(iIndex):
        return int()

    @staticmethod
    def getBuildingClassMaking(iIndex):
        return int()

    @staticmethod
    def getBuildingClassPrereqBuilding(eBuilding, ePrereqBuildingClass, iExtra):
        return int()

    @staticmethod
    def getBuildingGoodHealth():
        return int()

    @staticmethod
    def getBuildingHappiness():
        return int()

    @staticmethod
    def getBuildingProductionNeeded(iIndex):
        return int()

    @staticmethod
    def getCapitalCity():
        return CyCity()

    @staticmethod
    def getCapitalCommerceRateModifier(eIndex):
        return int()

    @staticmethod
    def getCapitalYieldRateModifier(eIndex):
        return int()

    @staticmethod
    def getCitiesLost():
        return int()

    @staticmethod
    def getCity(iID):
        return CyCity()

    @staticmethod
    def getCityDefenseModifier():
        return int()

    @staticmethod
    def getCityName(iIndex):
        return str()

    @staticmethod
    def getCivicAnarchyLength(paeNewCivics):
        return int()

    @staticmethod
    def getCivicPercentAnger(eCivic):
        return int()

    @staticmethod
    def getCivicUpkeep(paiCivics, bIgnoreAnarchy):
        return int()

    @staticmethod
    def getCivics(iIndex):
        return -1  # Type

    @staticmethod
    def getCivilizationAdjective(iForm):
        return str()

    @staticmethod
    def getCivilizationAdjectiveKey():
        return str()

    @staticmethod
    def getCivilizationDescription(iForm):
        return str()

    @staticmethod
    def getCivilizationDescriptionKey():
        return str()

    @staticmethod
    def getCivilizationShortDescription(iForm):
        return str()

    @staticmethod
    def getCivilizationShortDescriptionKey():
        return str()

    @staticmethod
    def getCivilizationType():
        return -1  # Type

    @staticmethod
    def getCoastalTradeRoutes():
        return int()

    @staticmethod
    def getCombatExperience():
        return int()

    @staticmethod
    def getCommercePercent(eIndex):
        return int()

    @staticmethod
    def getCommerceRate(eIndex):
        return int()

    @staticmethod
    def getCommerceRateModifier(eIndex):
        return int()

    @staticmethod
    def getConscriptCount():
        return int()

    @staticmethod
    def getConversionTimer():
        return int()

    @staticmethod
    def getCorporationMaintenanceModifier():
        return int()

    @staticmethod
    def getCultureHistory(iTurn):
        return int()

    @staticmethod
    def getCurrentEra():
        return int()

    @staticmethod
    def getCurrentResearch():
        return -1  # Type

    @staticmethod
    def getDistanceMaintenanceModifier():
        return int()

    @staticmethod
    def getDomesticGreatGeneralRateModifier():
        return int()

    @staticmethod
    def getEconomyHistory(iTurn):
        return int()

    @staticmethod
    def getEspionageHistory(iTurn):
        return int()

    @staticmethod
    def getEspionageMissionCost(eMission, eTargetPlayer, pPlot, iExtraData):
        return int()

    @staticmethod
    def getEspionageSpending(ePlayer):
        return int()

    @staticmethod
    def getEspionageSpendingWeightAgainstTeam(eIndex):
        return int()

    @staticmethod
    def getEventOccured(eEvent):
        return EventTriggeredData()

    @staticmethod
    def getEventTriggerWeight(eTrigger):
        return int()

    @staticmethod
    def getEventTriggered(iID):
        return EventTriggeredData()

    @staticmethod
    def getExpInBorderModifier():
        return bool()

    @staticmethod
    def getExtraBuildingHappiness(iIndex):
        return int()

    @staticmethod
    def getExtraBuildingHealth(iIndex):
        return int()

    @staticmethod
    def getExtraHappiness():
        return int()

    @staticmethod
    def getExtraHealth():
        return int()

    @staticmethod
    def getExtraUnitCost():
        return int()

    @staticmethod
    def getExtraYieldThreshold(eIndex):
        return int()

    @staticmethod
    def getFeatureHappiness(iIndex):
        return int()

    @staticmethod
    def getFeatureProductionModifier():
        return int()

    @staticmethod
    def getFlagDecal():
        return str()

    @staticmethod
    def getFreeCityCommerce(eIndex):
        return int()

    @staticmethod
    def getFreeExperience():
        return int()

    @staticmethod
    def getFreeMilitaryUnitsPopulationPercent():
        return int()

    @staticmethod
    def getFreeSpecialist():
        return int()

    @staticmethod
    def getFreeUnitsPopulationPercent():
        return int()

    @staticmethod
    def getGold():
        return int()

    @staticmethod
    def getGoldPerMilitaryUnit():
        return int()

    @staticmethod
    def getGoldPerTurn():
        return int()

    @staticmethod
    def getGoldPerTurnByPlayer(eIndex):
        return int()

    @staticmethod
    def getGoldPerUnit():
        return int()

    @staticmethod
    def getGoldenAgeLength():
        return int()

    @staticmethod
    def getGoldenAgeModifier():
        return int()

    @staticmethod
    def getGoldenAgeTurns():
        return int()

    @staticmethod
    def getGreatGeneralRateModifier():
        return int()

    @staticmethod
    def getGreatGeneralsCreated():
        return int()

    @staticmethod
    def getGreatGeneralsThresholdModifier():
        return int()

    @staticmethod
    def getGreatPeopleCreated():
        return int()

    @staticmethod
    def getGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getGreatPeopleThresholdModifier():
        return int()

    @staticmethod
    def getHandicapType():
        return -1  # Type

    @staticmethod
    def getHappyPerMilitaryUnit():
        return int()

    @staticmethod
    def getHasCorporationCount(eIndex):
        return int()

    @staticmethod
    def getHasReligionCount(eIndex):
        return int()

    @staticmethod
    def getHighestUnitLevel():
        return int()

    @staticmethod
    def getHurryCount(eIndex):
        return int()

    @staticmethod
    def getHurryModifier():
        return int()

    @staticmethod
    def getID():
        return int()

    @staticmethod
    def getImprovementCount(iIndex):
        return int()

    @staticmethod
    def getImprovementUpgradeRateModifier():
        return int()

    @staticmethod
    def getIndustryHistory(iTurn):
        return int()

    @staticmethod
    def getLandScore():
        return int()

    @staticmethod
    def getLargestCityHappiness():
        return int()

    @staticmethod
    def getLeaderType():
        return -1  # Type

    @staticmethod
    def getLengthResearchQueue():
        return int()

    @staticmethod
    def getLevelExperienceModifier():
        return int()

    @staticmethod
    def getMaxAnarchyTurns():
        return int()

    @staticmethod
    def getMaxConscript():
        return int()

    @staticmethod
    def getMaxGlobalBuildingProductionModifier():
        return int()

    @staticmethod
    def getMaxPlayerBuildingProductionModifier():
        return int()

    @staticmethod
    def getMaxTeamBuildingProductionModifier():
        return int()

    @staticmethod
    def getMilitaryProductionModifier():
        return int()

    @staticmethod
    def getName():
        return str()

    @staticmethod
    def getNameForm(iForm):
        return str()

    @staticmethod
    def getNameKey():
        return str()

    @staticmethod
    def getNewCityName():
        return str()

    @staticmethod
    def getNonStateReligionHappiness():
        return int()

    @staticmethod
    def getNumAvailableBonuses(eBonus):
        return int()

    @staticmethod
    def getNumCities():
        return int()

    @staticmethod
    def getNumCitiesMaintenanceModifier():
        return int()

    @staticmethod
    def getNumCityNames():
        return int()

    @staticmethod
    def getNumGovernmentCenters():
        return int()

    @staticmethod
    def getNumMilitaryUnits():
        return int()

    @staticmethod
    def getNumNukeUnits():
        return int()

    @staticmethod
    def getNumOutsideUnits():
        return int()

    @staticmethod
    def getNumSelectionGroups():
        return int()

    @staticmethod
    def getNumTradeBonusImports(ePlayer):
        return int()

    @staticmethod
    def getNumTradeableBonuses(eBonus):
        return int()

    @staticmethod
    def getNumUnitGoldenAges():
        return int()

    @staticmethod
    def getNumUnits():
        return int()

    @staticmethod
    def getOverflowResearch():
        return int()

    @staticmethod
    def getPersonalityType():
        return -1  # Type

    @staticmethod
    def getPlayerColor():
        return -1  # Type

    @staticmethod
    def getPlayerTextColorA():
        return int()

    @staticmethod
    def getPlayerTextColorB():
        return int()

    @staticmethod
    def getPlayerTextColorG():
        return int()

    @staticmethod
    def getPlayerTextColorR():
        return int()

    @staticmethod
    def setPlayerColor(eColor):
        pass

    @staticmethod
    def getPopScore():
        return int()

    @staticmethod
    def getPower():
        return int()

    @staticmethod
    def getPowerHistory(iTurn):
        return int()

    @staticmethod
    def getProjectProductionNeeded(iIndex):
        return int()

    @staticmethod
    def getQueuePosition(eTech):
        return int()

    @staticmethod
    def getRealPopulation():
        return int()

    @staticmethod
    def getReligionAnarchyLength():
        return int()

    @staticmethod
    def getResearchTurnsLeft(eTech, bOverflow):
        return int()

    @staticmethod
    def getRevolutionTimer():
        return int()

    @staticmethod
    def getScoreHistory(iTurn):
        return int()

    @staticmethod
    def getScriptData():
        return str()

    @staticmethod
    def getSeaPlotYield(eIndex):
        return int()

    @staticmethod
    def getSelectionGroup(iID):
        return CySelectionGroup()

    @staticmethod
    def getSingleCivicUpkeep(eCivic, bIgnoreAnarchy):
        return int()

    @staticmethod
    def getSpaceProductionModifier():
        return int()

    @staticmethod
    def getSpecialBuildingNotRequiredCount(eIndex):
        return int()

    @staticmethod
    def getSpecialistExtraCommerce(eIndex):
        return int()

    @staticmethod
    def getSpecialistExtraYield(eIndex1, eIndex2):
        return int()

    @staticmethod
    def getStartingPlot():
        return CyPlot()

    @staticmethod
    def getStateReligion():
        return int()

    @staticmethod
    def getStateReligionBuildingCommerce(eIndex):
        return int()

    @staticmethod
    def getStateReligionBuildingProductionModifier():
        return int()

    @staticmethod
    def getStateReligionFreeExperience():
        return int()

    @staticmethod
    def getStateReligionGreatPeopleRateModifier():
        return int()

    @staticmethod
    def getStateReligionHappiness():
        return int()

    @staticmethod
    def getStateReligionKey():
        return str()

    @staticmethod
    def getStateReligionName(iForm):
        return str()

    @staticmethod
    def getStateReligionUnitProductionModifier():
        return int()

    @staticmethod
    def getStrikeTurns():
        return int()

    @staticmethod
    def getTeam():
        return int()

    @staticmethod
    def getTechScore():
        return int()

    @staticmethod
    def getTotalLand():
        return int()

    @staticmethod
    def getTotalLandScored():
        return int()

    @staticmethod
    def getTotalMaintenance():
        return int()

    @staticmethod
    def getTotalPopulation():
        return int()

    @staticmethod
    def getTotalTimePlayed():
        return int()

    @staticmethod
    def getTradeDenial(eWhoTo, item):
        return -1  # Type

    @staticmethod
    def getTradeRoutes():
        return int()

    @staticmethod
    def getTradeYieldModifier(eIndex):
        return int()

    @staticmethod
    def getUnit(iID):
        return CyUnit()

    @staticmethod
    def getUnitButton(eUnit):
        return str()

    @staticmethod
    def getUnitClassCount(eIndex):
        return int()

    @staticmethod
    def getUnitClassCountPlusMaking(eIndex):
        return int()

    @staticmethod
    def getUnitClassMaking(eIndex):
        return int()

    @staticmethod
    def getUnitProductionNeeded(iIndex):
        return int()

    @staticmethod
    def getUpkeepCount(eIndex):
        return int()

    @staticmethod
    def getUpkeepModifier():
        return int()

    @staticmethod
    def getVotes(eVote, eVoteSource):
        return int()

    @staticmethod
    def getWarWearinessModifier():
        return int()

    @staticmethod
    def getWarWearinessPercentAnger():
        return int()

    @staticmethod
    def getWinsVsBarbs():
        return int()

    @staticmethod
    def getWondersScore():
        return int()

    @staticmethod
    def getWorkerSpeedModifier():
        return int()

    @staticmethod
    def getWorstEnemyName():
        return str()

    @staticmethod
    def getYieldRateModifier(eIndex):
        return int()

    @staticmethod
    def greatPeopleThreshold(bMilitary):
        return int()

    @staticmethod
    def hasBonus(eBonus):
        return bool()

    @staticmethod
    def hasHeadquarters(eCorporation):
        return bool()

    @staticmethod
    def hasHolyCity(eReligion):
        return bool()

    @staticmethod
    def hasTrait(iIndex):
        return bool()

    @staticmethod
    def initCity(x, y):
        return CyCity()

    @staticmethod
    def initTriggeredData(eEventTrigger, bFire, iCityId, iPlotX, iPlotY, eOtherPlayer, iOtherPlayerCityId, eReligion, eCorporation, iUnitId, eBuilding):
        return EventTriggeredData()

    @staticmethod
    def initUnit(iIndex, iX, iY, eUnitAI, eFacingDirection):
        return CyUnit()

    @staticmethod
    def isAlive():
        return bool()

    @staticmethod
    def isAnarchy():
        return bool()

    @staticmethod
    def isBarbarian():
        return bool()

    @staticmethod
    def isBuildingClassMaxedOut(iIndex, iExtra):
        return bool()

    @staticmethod
    def isBuildingFree(iIndex):
        return bool()

    @staticmethod
    def isBuildingOnlyHealthy():
        return bool()

    @staticmethod
    def isCivic(eCivic):
        return bool()

    @staticmethod
    def isCommerceFlexible(eIndex):
        return bool()

    @staticmethod
    def isCurrentResearchRepeat():
        return bool()

    @staticmethod
    def isEverAlive():
        return bool()

    @staticmethod
    def isExtendedGame():
        return bool()

    @staticmethod
    def isFeatAccomplished(eIndex):
        return bool()

    @staticmethod
    def isFoundedFirstCity():
        return bool()

    @staticmethod
    def isFullMember(eVoteSource):
        return bool()

    @staticmethod
    def isGoldenAge():
        return bool()

    @staticmethod
    def isHasCivicOption(eIndex):
        return bool()

    @staticmethod
    def isHuman():
        return bool()

    @staticmethod
    def isLoyalMember(eIndex):
        return bool()

    @staticmethod
    def isMilitaryFoodProduction():
        return bool()

    @staticmethod
    def isMinorCiv():
        return bool()

    @staticmethod
    def isNoCivicUpkeep(iIndex):
        return bool()

    @staticmethod
    def isNoCorporations():
        return bool()

    @staticmethod
    def isNoForeignCorporations():
        return bool()

    @staticmethod
    def isNoForeignTrade():
        return bool()

    @staticmethod
    def isNoNonStateReligionSpread():
        return bool()

    @staticmethod
    def isNoResearchAvailable():
        return bool()

    @staticmethod
    def isNoUnhealthyPopulation():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isOption(eIndex):
        return bool()

    @staticmethod
    def isPlayable():
        return bool()

    @staticmethod
    def isProductionMaxedBuildingClass(eBuildingClass, bAcquireCity):
        return bool()

    @staticmethod
    def isProductionMaxedProject(eProject):
        return bool()

    @staticmethod
    def isProductionMaxedUnitClass(eUnitClass):
        return bool()

    @staticmethod
    def isResearch():
        return bool()

    @staticmethod
    def isResearchingTech(iIndex):
        return bool()

    @staticmethod
    def isSpecialBuildingNotRequired(eIndex):
        return bool()

    @staticmethod
    def isSpecialistValid(iIndex):
        return bool()

    @staticmethod
    def isStateReligion():
        return bool()

    @staticmethod
    def isStrike():
        return bool()

    @staticmethod
    def isTurnActive():
        return bool()

    @staticmethod
    def isUnitClassMaxedOut(eIndex, iExtra):
        return bool()

    @staticmethod
    def isVotingMember(eVoteSource):
        return bool()

    @staticmethod
    def isWhiteFlag():
        return bool()

    @staticmethod
    def killAllDeals():
        pass

    @staticmethod
    def killCities():
        pass

    @staticmethod
    def killUnits():
        pass

    @staticmethod
    def nextCity(iterIn, bRev):
        return tuple()

    @staticmethod
    def nextSelectionGroup(iterIn, bRev):
        return tuple()

    @staticmethod
    def nextUnit(iterIn, bRev):
        return tuple()

    @staticmethod
    def popResearch(eTech):
        pass

    @staticmethod
    def pushResearch(iIndex, bClear):
        return bool()

    @staticmethod
    def raze(pCity):
        pass

    @staticmethod
    def receiveGoody(pPlot, eGoody, pUnit):
        pass

    @staticmethod
    def removeBuildingClass(eBuildingClass):
        pass

    @staticmethod
    def resetEventOccured(eEvent):
        pass

    @staticmethod
    def revolution(paeNewCivics, bForce):
        pass

    @staticmethod
    def setAdvancedStartPoints(iNewValue):
        pass

    @staticmethod
    def setCivics(eIndex, eNewValue):
        pass

    @staticmethod
    def setCombatExperience(iExperience):
        pass

    @staticmethod
    def setCommercePercent(eIndex, iNewValue):
        pass

    @staticmethod
    def setConscriptCount(iNewValue):
        pass

    @staticmethod
    def setCurrentEra(iNewValue):
        pass

    @staticmethod
    def setEspionageSpendingWeightAgainstTeam(eIndex, iValue):
        pass

    @staticmethod
    def setFeatAccomplished(eIndex, bNewValue):
        pass

    @staticmethod
    def setGold(iNewValue):
        pass

    @staticmethod
    def setLastStateReligion(iNewReligion):
        pass

    @staticmethod
    def setLoyalMember(eIndex, bNewValue):
        pass

    @staticmethod
    def setOption(eIndex, bNewValue):
        pass

    @staticmethod
    def setPersonalityType(eNewValue):
        pass

    @staticmethod
    def setPlayable(bNewValue):
        pass

    @staticmethod
    def setScriptData(szNewValue):
        pass

    @staticmethod
    def setStartingPlot(pPlot, bUpdateStartDist):
        pass

    @staticmethod
    def specialistCommerce(eSpecialist, eCommerce):
        return int()

    @staticmethod
    def specialistYield(eSpecialist, eCommerce):
        return int()

    @staticmethod
    def splitEmpire(iAreaId):
        return bool()

    @staticmethod
    def startingPlotRange():
        return int()

    @staticmethod
    def startingPlotWithinRange(pPlot, ePlayer, iRange, iPass):
        return bool()

    @staticmethod
    def stopTradingWithTeam(eTeam):
        pass

    @staticmethod
    def trigger(eEventTrigger):
        pass

    @staticmethod
    def unitsGoldenAgeCapable():
        return int()

    @staticmethod
    def unitsGoldenAgeReady():
        return int()

    @staticmethod
    def unitsRequiredForGoldenAge():
        return int()


class CyPlot:

    @staticmethod
    def addFeatureDummyModel(dummyTag, modelTag):
        pass

    @staticmethod
    def area():
        return CyArea()

    @staticmethod
    def at(iX, iY):
        return bool()

    @staticmethod
    def calculateBestNatureYield(eIndex, eTeam):
        return int()

    @staticmethod
    def calculateCulturalOwner():
        return -1  # Type

    @staticmethod
    def calculateCulturePercent(eIndex):
        return int()

    @staticmethod
    def calculateImprovementYieldChange(eImprovement, eYield, ePlayer, bOptimal):
        return int()

    @staticmethod
    def calculateNatureYield(eIndex, eTeam, bIgnoreFeature):
        return int()

    @staticmethod
    def calculateTeamCulturePercent(eIndex):
        return int()

    @staticmethod
    def calculateTotalBestNatureYield(eTeam):
        return int()

    @staticmethod
    def calculateYield(eIndex, bDisplay):
        return int()

    @staticmethod
    def canBuild(eBuild, ePlayer, bTestVisible):
        return bool()

    @staticmethod
    def canHaveBonus(eBonus, bIgnoreLatitude):
        return bool()

    @staticmethod
    def canHaveFeature(eFeature):
        return bool()

    @staticmethod
    def canHaveImprovement(eImprovement, eTeam, bPotential):
        return bool()

    @staticmethod
    def canHavePotentialIrrigation():
        return bool()

    @staticmethod
    def changeBuildProgress(eBuild, iChange, eTeam):
        return bool()

    @staticmethod
    def changeCulture(eIndex, iChange, bUpdate):
        pass

    @staticmethod
    def changeExtraMovePathCost(iChange):
        pass

    @staticmethod
    def changeForceUnownedTimer(iChange):
        pass

    @staticmethod
    def changeImprovementDuration(iChange):
        pass

    @staticmethod
    def changeInvisibleVisibilityCount(eTeam, eInvisible, iChange):
        pass

    @staticmethod
    def changeOwnershipDuration(iChange):
        pass

    @staticmethod
    def changeUpgradeProgress(iChange):
        pass

    @staticmethod
    def changeVisibilityCount(eTeam, iChange, eSeeInvisible):
        pass

    @staticmethod
    def countNumAirUnits(ePlayer):
        return int()

    @staticmethod
    def countTotalCulture():
        return int()

    @staticmethod
    def defenseModifier(iDefendTeam, bIgnoreBuilding, bHelp):
        return int()

    @staticmethod
    def erase():
        pass

    @staticmethod
    def findHighestCultureTeam():
        return -1  # Type

    @staticmethod
    def getArea():
        return int()

    @staticmethod
    def getBestDefender(eOwner, eAttackingPlayer, pAttacker, bTestAtWar, bTestPotentialEnemy, bTestCanMove):
        return CyUnit()

    @staticmethod
    def getBonusType(eTeam):
        return -1  # Type

    @staticmethod
    def getBuildProgress(eBuild):
        return int()

    @staticmethod
    def getBuildTime(eBuild):
        return int()

    @staticmethod
    def getBuildTurnsLeft(eBuild, iNowExtra, iThenExtra):
        return int()

    @staticmethod
    def getCityRadiusCount():
        return int()

    @staticmethod
    def getCulture(eIndex):
        return int()

    @staticmethod
    def getCultureRangeCities(eOwnerIndex, iRangeIndex):
        return int()

    @staticmethod
    def getExtraMovePathCost():
        return int()

    @staticmethod
    def getFeatureProduction(eBuild, eTeam, ppCity):
        return int()

    @staticmethod
    def getFeatureType():
        return -1  # Type

    @staticmethod
    def getFeatureVariety():
        return int()

    @staticmethod
    def getForceUnownedTimer():
        return int()

    @staticmethod
    def getFoundValue(eIndex):
        return int()

    @staticmethod
    def getImprovementDuration():
        return int()

    @staticmethod
    def getImprovementType():
        return -1  # Type

    @staticmethod
    def getInvisibleVisibilityCount(eTeam, eInvisible):
        return int()

    @staticmethod
    def getLatitude():
        return int()

    @staticmethod
    def getMinOriginalStartDist():
        return int()

    @staticmethod
    def getNearestLandArea():
        return int()

    @staticmethod
    def getNearestLandPlot():
        return CyPlot()

    @staticmethod
    def getNonObsoleteBonusType(eTeam):
        return -1  # Type

    @staticmethod
    def getNumCultureRangeCities(ePlayer):
        return int()

    @staticmethod
    def getNumDefenders(ePlayer):
        return int()

    @staticmethod
    def getNumUnits():
        return int()

    @staticmethod
    def getNumVisibleEnemyDefenders(pUnit):
        return int()

    @staticmethod
    def getNumVisiblePotentialEnemyDefenders(pUnit):
        return int()

    @staticmethod
    def getOwner():
        return -1  # Type

    @staticmethod
    def getOwnershipDuration():
        return int()

    @staticmethod
    def getPlayerCityRadiusCount(eIndex):
        return int()

    @staticmethod
    def getPlotCity():
        return CyCity()

    @staticmethod
    def getPlotGroupConnectedBonus(ePlayer, eBonus):
        return int()

    @staticmethod
    def getPlotType():
        return -1  # Type

    @staticmethod
    def getPoint():
        return NiPoint3(0, 0, 0)

    @staticmethod
    def getReconCount():
        return int()

    @staticmethod
    def getRevealedImprovementType(eTeam, bDebug):
        return -1  # Type

    @staticmethod
    def getRevealedOwner(eTeam, bDebug):
        return -1  # Type

    @staticmethod
    def getRevealedRouteType(eTeam, bDebug):
        return -1  # Type

    @staticmethod
    def getRevealedTeam(eTeam, bDebug):
        return -1  # Type

    @staticmethod
    def getRiverCrossingCount():
        return int()

    @staticmethod
    def getRiverID():
        return int()

    @staticmethod
    def getRiverNSDirection():
        return -1  # Type

    @staticmethod
    def getRiverWEDirection():
        return -1  # Type

    @staticmethod
    def getRouteType():
        return -1  # Type

    @staticmethod
    def getScriptData():
        return str()

    @staticmethod
    def getSelectedUnit():
        return CyUnit()

    @staticmethod
    def getStolenVisibilityCount(eTeam):
        return int()

    @staticmethod
    def getTeam():
        return int()

    @staticmethod
    def getTerrainType():
        return -1  # Type

    @staticmethod
    def getUnit(iIndex):
        return CyUnit()

    @staticmethod
    def getUnitPower(eOwner):
        return int()

    @staticmethod
    def getUpgradeProgress():
        return int()

    @staticmethod
    def getUpgradeTimeLeft(eImprovement, ePlayer):
        return int()

    @staticmethod
    def getVisibilityCount(eTeam):
        return int()

    @staticmethod
    def getWorkingCity():
        return CyCity()

    @staticmethod
    def getWorkingCityOverride():
        return CyCity()

    @staticmethod
    def getX():
        return int()

    @staticmethod
    def getY():
        return int()

    @staticmethod
    def getYield(eIndex):
        return int()

    @staticmethod
    def hasYield():
        return bool()

    @staticmethod
    def isActiveVisible(bDebug):
        return bool()

    @staticmethod
    def isAdjacentNonrevealed(eTeam):
        return bool()

    @staticmethod
    def isAdjacentNonvisible(eTeam):
        return bool()

    @staticmethod
    def isAdjacentOwned():
        return bool()

    @staticmethod
    def isAdjacentPlayer(ePlayer, bLandOnly):
        return bool()

    @staticmethod
    def isAdjacentPlotGroupConnectedBonus(ePlayer, eBonus):
        return bool()

    @staticmethod
    def isAdjacentRevealed(eTeam):
        return bool()

    @staticmethod
    def isAdjacentTeam(eTeam, bLandOnly):
        return bool()

    @staticmethod
    def isAdjacentToArea(pArea):
        return bool()

    @staticmethod
    def isAdjacentToLand():
        return bool()

    @staticmethod
    def isAdjacentVisible(eTeam, bDebug):
        return bool()

    @staticmethod
    def isBarbarian():
        return bool()

    @staticmethod
    def isBeingWorked():
        return bool()

    @staticmethod
    def isBestAdjacentFound(eIndex):
        return bool()

    @staticmethod
    def isBonusNetwork(eTeam):
        return bool()

    @staticmethod
    def isCity():
        return bool()

    @staticmethod
    def isCityRadius():
        return int()

    @staticmethod
    def isCoastalLand():
        return bool()

    @staticmethod
    def isConnectedTo(pCity):
        return bool()

    @staticmethod
    def isConnectedToCapital(ePlayer):
        return bool()

    @staticmethod
    def isCultureRangeCity(eOwnerIndex, iRangeIndex):
        return bool()

    @staticmethod
    def isEnemyCity(pUnit):
        return bool()

    @staticmethod
    def isFighting():
        return bool()

    @staticmethod
    def isFlagDirty():
        return bool()

    @staticmethod
    def isFlatlands():
        return bool()

    @staticmethod
    def isForceUnowned():
        return bool()

    @staticmethod
    def isFreshWater():
        return bool()

    @staticmethod
    def isFriendlyCity(pUnit, bCheckImprovement):
        return bool()

    @staticmethod
    def isGoody():
        return bool()

    @staticmethod
    def isHills():
        return bool()

    @staticmethod
    def isImpassable():
        return bool()

    @staticmethod
    def isInvestigate(eTeam):
        return bool()

    @staticmethod
    def isInvisibleVisible(eTeam, eInvisible):
        return bool()

    @staticmethod
    def isIrrigated():
        return bool()

    @staticmethod
    def isIrrigationAvailable(bIgnoreSelf):
        return bool()

    @staticmethod
    def isLake():
        return bool()

    @staticmethod
    def isNOfRiver():
        return bool()

    @staticmethod
    def isNetworkTerrain(eTeam):
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isOccupation():
        return bool()

    @staticmethod
    def isOwned():
        return bool()

    @staticmethod
    def isOwnershipScore():
        return bool()

    @staticmethod
    def isPeak():
        return bool()

    @staticmethod
    def isPlayerCityRadius(eIndex):
        return bool()

    @staticmethod
    def isPlotGroupConnectedBonus(ePlayer, eBonus):
        return bool()

    @staticmethod
    def isPotentialCityWork():
        return bool()

    @staticmethod
    def isPotentialCityWorkForArea(pArea):
        return bool()

    @staticmethod
    def isPotentialIrrigation():
        return bool()

    @staticmethod
    def isRevealed(eTeam, bDebug):
        return bool()

    @staticmethod
    def isRevealedBarbarian():
        return bool()

    @staticmethod
    def isRevealedGoody(eTeam):
        return bool()

    @staticmethod
    def isRiver():
        return bool()

    @staticmethod
    def isRiverConnection(eDirection):
        return bool()

    @staticmethod
    def isRiverCrossing(eIndex):
        return bool()

    @staticmethod
    def isRiverSide():
        return bool()

    @staticmethod
    def isRoute():
        return bool()

    @staticmethod
    def isStartingPlot():
        return bool()

    @staticmethod
    def isTradeNetwork(eTeam):
        return bool()

    @staticmethod
    def isTradeNetworkConnected(pPlot, eTeam):
        return bool()

    @staticmethod
    def isTradeNetworkImpassable(eTeam):
        return bool()

    @staticmethod
    def isUnit():
        return bool()

    @staticmethod
    def isValidDomainForAction(pUnit):
        return bool()

    @staticmethod
    def isValidDomainForLocation(pUnit):
        return bool()

    @staticmethod
    def isVisible(eTeam, bDebug):
        return bool()

    @staticmethod
    def isVisibleEnemyDefender(pUnit):
        return bool()

    @staticmethod
    def isVisibleEnemyUnit(ePlayer):
        return bool()

    @staticmethod
    def isVisibleOtherUnit(ePlayer):
        return bool()

    @staticmethod
    def isVisibleToWatchingHuman():
        return bool()

    @staticmethod
    def isWOfRiver():
        return bool()

    @staticmethod
    def isWater():
        return bool()

    @staticmethod
    def isWithinCultureRange(ePlayer):
        return bool()

    @staticmethod
    def isWithinTeamCityRadius(eTeam, eIgnorePlayer):
        return bool()

    @staticmethod
    def movementCost(pUnit, pFromPlot):
        return int()

    @staticmethod
    def nukeExplosion(iRange, pNukeUnit):
        pass

    @staticmethod
    def pickFeatureDummyTag(mouseX, mouseY):
        return str()

    @staticmethod
    def removeGoody():
        pass

    @staticmethod
    def resetFeatureModel():
        pass

    @staticmethod
    def seeFromLevel(eTeam):
        return int()

    @staticmethod
    def seeThroughLevel():
        return int()

    @staticmethod
    def setBonusType(eNewValue):
        pass

    @staticmethod
    def setCulture(eIndex, iNewValue, bUpdate):
        pass

    @staticmethod
    def setFeatureDummyTexture(dummyTag, textureTag):
        pass

    @staticmethod
    def setFeatureDummyVisibility(dummyTag, show):
        pass

    @staticmethod
    def setFeatureType(eNewValue, iVariety):
        pass

    @staticmethod
    def setFlagDirty(bNewValue):
        pass

    @staticmethod
    def setForceUnownedTimer(iNewValue):
        pass

    @staticmethod
    def setImprovementDuration(iNewValue):
        pass

    @staticmethod
    def setImprovementType(eNewValue):
        pass

    @staticmethod
    def setNOfRiver(bNewValue, eRiverDir):
        pass

    @staticmethod
    def setOwner(eNewValue):
        pass

    @staticmethod
    def setOwnerNoUnitCheck(eNewValue):
        pass

    @staticmethod
    def setOwnershipDuration(iNewValue):
        pass

    @staticmethod
    def setPlotType(eNewValue, bRecalculate, bRebuildGraphics):
        pass

    @staticmethod
    def setRevealed(eTeam, bNewValue, bTerrainOnly, eFromTeam):
        pass

    @staticmethod
    def setRiverID(iNewValue):
        pass

    @staticmethod
    def setRouteType(eNewValue):
        pass

    @staticmethod
    def setScriptData(szNewValue):
        pass

    @staticmethod
    def setStartingPlot(bNewValue):
        pass

    @staticmethod
    def setTerrainType(eNewValue, bRecalculate, bRebuildGraphics):
        pass

    @staticmethod
    def setUpgradeProgress(iNewValue):
        pass

    @staticmethod
    def setWOfRiver(bNewValue, eRiverDir):
        pass

    @staticmethod
    def shareAdjacentArea(pPlot):
        return bool()

    @staticmethod
    def updateVisibility():
        pass

    @staticmethod
    def waterArea():
        return CyArea()


class CyPopup:

    @staticmethod
    def addButton(szText):
        pass

    @staticmethod
    def addButtonXY(szText, iX, iY):
        pass

    @staticmethod
    def addDDS(szPathName, iX, iY, iWidth, iHeight):
        pass

    @staticmethod
    def addFixedSeparator(iSpace):
        pass

    @staticmethod
    def addLeaderhead(szPathName, eWho, eInitAttitude, iX, iY):
        pass

    @staticmethod
    def addListBoxString(szText, iID, iGroup):
        pass

    @staticmethod
    def addPullDownString(szText, iID, iGroup):
        pass

    @staticmethod
    def addPythonButton(szFunctionName, szBtnText, szHelpText, szArtFile, iData1, iData2, bOption):
        pass

    @staticmethod
    def addPythonButtonXY(szFunctionName, szBtnText, szHelpText, szArtFile, iData1, iData2, bOption, iX, iY):
        pass

    @staticmethod
    def addPythonDDS(szPathName, szText, iX, iY, iWidth, iHeight):
        pass

    @staticmethod
    def addSeparator():
        pass

    @staticmethod
    def addTableCellDDS(iRow, iCol, szFile, iX, iY, iWidth, iHeight, iGroup):
        pass

    @staticmethod
    def addTableCellImage(iRow, iCol, szFile, iGroup):
        pass

    @staticmethod
    def addTableCellText(iRow, iCol, szText, iGroup):
        pass

    @staticmethod
    def completeTableAndAttach(iGroup):
        pass

    @staticmethod
    def completeTableAndAttachXY(iGroup, iX, iY):
        pass

    @staticmethod
    def createCheckBoxes(iNumBoxes, iGroup):
        pass

    @staticmethod
    def createEditBox(szText, iGroup):
        pass

    @staticmethod
    def createEditBoxXY(szText, iGroup, iX, iY):
        pass

    @staticmethod
    def createListBox(iGroup):
        pass

    @staticmethod
    def createListBoxXY(iGroup, iX, iY):
        pass

    @staticmethod
    def createPullDown(iGroup):
        pass

    @staticmethod
    def createPullDownXY(iGroup, iX, iY):
        pass

    @staticmethod
    def createPythonCheckBoxes(iNumBoxes, iGroup):
        pass

    @staticmethod
    def createPythonEditBox(szText, szHelpText, iGroup):
        pass

    @staticmethod
    def createPythonEditBoxXY(szText, szHelpText, iGroup, iX, iY):
        pass

    @staticmethod
    def createPythonListBox(szText, iGroup):
        pass

    @staticmethod
    def createPythonListBoxXY(szText, iGroup, iX, iY):
        pass

    @staticmethod
    def createPythonPullDown(szText, iGroup):
        pass

    @staticmethod
    def createPythonPullDownXY(szText, iGroup, iX, iY):
        pass

    @staticmethod
    def createPythonRadioButtons(iNumButtons, iGroup):
        pass

    @staticmethod
    def createRadioButtons(iNumButtons, iGroup):
        pass

    @staticmethod
    def createSpinBox(iIndex, szHelpText, iDefault, iIncrement, iMax, iMin):
        pass

    @staticmethod
    def createTable(iRows, iCols, iGroup):
        pass

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def launch(bCreateOK, eState):
        return bool()

    @staticmethod
    def setBodyString(szText, uiFlags):
        pass

    @staticmethod
    def setCheckBoxText(iCheckBoxID, szText, iGroup):
        pass

    @staticmethod
    def setEditBoxMaxCharCount(maxCharCount, preferredCharCount, iGroup):
        pass

    @staticmethod
    def setHeaderString(szText, uiFlags):
        pass

    @staticmethod
    def setPosition(iX, iY):
        pass

    @staticmethod
    def setPythonBodyString(szDefText, szName, szText, uiFlags):
        pass

    @staticmethod
    def setPythonCheckBoxText(iCheckBoxID, szText, szHelpText, iGroup):
        pass

    @staticmethod
    def setPythonRadioButtonText(iRadioButtonID, szText, szHelpText, iGroup):
        pass

    @staticmethod
    def setRadioButtonText(iRadioButtonID, szText, iGroup):
        pass

    @staticmethod
    def setSelectedListBoxString(iID, iGroup):
        pass

    @staticmethod
    def setSelectedPulldownID(iID, iGroup):
        pass

    @staticmethod
    def setSize(iXS, iYS):
        pass

    @staticmethod
    def setTableCellSize(iCol, iPixels, iGroup):
        pass

    @staticmethod
    def setTableYSize(iRow, iSize, iGroup):
        pass

    @staticmethod
    def setTimer(uiTime):
        pass

    @staticmethod
    def setUserData(userData):
        pass


class CyPopupInfo:

    @staticmethod
    def addPopup(iPlayer):
        pass

    @staticmethod
    def addPythonButton(szText, szArt):
        pass

    @staticmethod
    def getButtonPopupType():
        return -1  # Type

    @staticmethod
    def getData1():
        return int()

    @staticmethod
    def getData2():
        return int()

    @staticmethod
    def getData3():
        return int()

    @staticmethod
    def getFlags():
        return int()

    @staticmethod
    def getNumPythonButtons():
        return int()

    @staticmethod
    def getOnClickedPythonCallback():
        return str()

    @staticmethod
    def getOnFocusPythonCallback():
        return str()

    @staticmethod
    def getOption1():
        return bool()

    @staticmethod
    def getOption2():
        return bool()

    @staticmethod
    def getPythonButtonArt():
        return str()

    @staticmethod
    def getPythonButtonText():
        return str()

    @staticmethod
    def getPythonModule():
        return str()

    @staticmethod
    def getText():
        return str()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def setButtonPopupType(eValue):
        pass

    @staticmethod
    def setData1(iValue):
        pass

    @staticmethod
    def setData2(iValue):
        pass

    @staticmethod
    def setData3(iValue):
        pass

    @staticmethod
    def setFlags(iValue):
        pass

    @staticmethod
    def setOnClickedPythonCallback(szOnFocus):
        pass

    @staticmethod
    def setOnFocusPythonCallback(szOnFocus):
        pass

    @staticmethod
    def setOption1(bValue):
        pass

    @staticmethod
    def setOption2(bValue):
        pass

    @staticmethod
    def setPythonModule(szOnFocus):
        pass

    @staticmethod
    def setText(szText):
        pass


class CyPopupReturn:

    @staticmethod
    def getButtonClicked(iGroup):
        return int()

    @staticmethod
    def getEditBoxString(iGroup):
        return str()

    @staticmethod
    def getSelectedListBoxValue(iGroup):
        return int()

    @staticmethod
    def getSelectedPullDownValue(iGroup):
        return int()

    @staticmethod
    def getSelectedRadioButton(iGroup):
        return int()

    @staticmethod
    def getSpinnerWidgetValue(iGroup):
        return int()

    @staticmethod
    def isNone():
        return bool()


class CyPythonMgr:

    @staticmethod
    def allowDefaultImpl():
        pass

    @staticmethod
    def debugMsg(msg):
        pass

    @staticmethod
    def debugMsgWide(msg):
        pass

    @staticmethod
    def errorMsg(msg):
        pass

    @staticmethod
    def errorMsgWide(msg):
        pass


class CyRandom:

    @staticmethod
    def get(usNum, pszLog):
        return int()

    @staticmethod
    def init(ulSeed):
        pass


class CyReplayInfo:

    @staticmethod
    def createInfo(iPlayer):
        pass

    @staticmethod
    def getActivePlayer():
        return int()

    @staticmethod
    def getCalendar():
        return int()

    @staticmethod
    def getCivAdjective():
        return str()

    @staticmethod
    def getCivDescription():
        return str()

    @staticmethod
    def getClimate():
        return int()

    @staticmethod
    def getColor(iPlayer):
        return int()

    @staticmethod
    def getDifficulty():
        return int()

    @staticmethod
    def getEra():
        return int()

    @staticmethod
    def getFinalAgriculture():
        return int()

    @staticmethod
    def getFinalDate():
        return str()

    @staticmethod
    def getFinalEconomy():
        return int()

    @staticmethod
    def getFinalIndustry():
        return int()

    @staticmethod
    def getFinalScore():
        return int()

    @staticmethod
    def getFinalTurn():
        return int()

    @staticmethod
    def getGameSpeed():
        return int()

    @staticmethod
    def getInitialTurn():
        return int()

    @staticmethod
    def getLeader(iPlayer):
        return int()

    @staticmethod
    def getLeaderName():
        return str()

    @staticmethod
    def getMapHeight():
        return int()

    @staticmethod
    def getMapScriptName():
        return str()

    @staticmethod
    def getMapWidth():
        return int()

    @staticmethod
    def getModName():
        return str()

    @staticmethod
    def getNormalizedScore():
        return int()

    @staticmethod
    def getNumPlayers():
        return int()

    @staticmethod
    def getNumReplayMessages():
        return int()

    @staticmethod
    def getPlayerAgriculture(iPlayer, iTurn):
        return int()

    @staticmethod
    def getPlayerEconomy(iPlayer, iTurn):
        return int()

    @staticmethod
    def getPlayerIndustry(iPlayer, iTurn):
        return int()

    @staticmethod
    def getPlayerScore(iPlayer, iTurn):
        return int()

    @staticmethod
    def getReplayMessageColor(i):
        return int()

    @staticmethod
    def getReplayMessagePlayer(i):
        return int()

    @staticmethod
    def getReplayMessagePlotX(i):
        return int()

    @staticmethod
    def getReplayMessagePlotY(i):
        return int()

    @staticmethod
    def getReplayMessageText(i):
        return str()

    @staticmethod
    def getReplayMessageTurn(i):
        return int()

    @staticmethod
    def getReplayMessageType(i):
        return int()

    @staticmethod
    def getSeaLevel():
        return int()

    @staticmethod
    def getShortCivDescription():
        return str()

    @staticmethod
    def getStartYear():
        return int()

    @staticmethod
    def getVictoryType():
        return int()

    @staticmethod
    def getWorldSize():
        return int()

    @staticmethod
    def isGameOption(iOption):
        return bool()

    @staticmethod
    def isMultiplayer():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isVictoryCondition(iVictory):
        return bool()


class CySelectionGroup:

    @staticmethod
    def alwaysInvisible():
        return bool()

    @staticmethod
    def area():
        return CyArea()

    @staticmethod
    def at(iX, iY):
        return bool()

    @staticmethod
    def atPlot(pPlot):
        return bool()

    @staticmethod
    def baseMoves():
        return int()

    @staticmethod
    def canAllMove():
        return bool()

    @staticmethod
    def canAnyMove():
        return bool()

    @staticmethod
    def canDefend():
        return bool()

    @staticmethod
    def canDoCommand(eCommand, iData1, iData2, bTestVisible):
        return bool()

    @staticmethod
    def canDoInterfaceMode(eInterfaceMode):
        return bool()

    @staticmethod
    def canDoInterfaceModeAt(eInterfaceMode, pPlot):
        return bool()

    @staticmethod
    def canEnterArea(eTeam, pArea, bIgnoreRightOfPassage):
        return bool()

    @staticmethod
    def canEnterTerritory(eTeam, bIgnoreRightOfPassage):
        return bool()

    @staticmethod
    def canFight():
        return bool()

    @staticmethod
    def canMoveInto(pPlot, bAttack):
        return bool()

    @staticmethod
    def canMoveOrAttackInto(pPlot, bDeclareWar):
        return bool()

    @staticmethod
    def canMoveThrough(pPlot):
        return bool()

    @staticmethod
    def canStartMission(iMission, iData1, iData2, pPlot, bTestVisible):
        return bool()

    @staticmethod
    def clearMissionQueue():
        pass

    @staticmethod
    def countNumUnitAIType(eUnitAI):
        return int()

    @staticmethod
    def generatePath(pFromPlot, pToPlot, iFlags, bReuse, piPathTurns):
        return bool()

    @staticmethod
    def getActivityType():
        return -1  # Type

    @staticmethod
    def getAutomateType():
        return -1  # Type

    @staticmethod
    def getBestBuildRoute(pPlot, peBestBuild):
        return -1  # Type

    @staticmethod
    def getHeadUnit():
        return CyUnit()

    @staticmethod
    def getID():
        return int()

    @staticmethod
    def getLengthMissionQueue():
        return int()

    @staticmethod
    def getMissionData1(iNode):
        return int()

    @staticmethod
    def getMissionData2(iNode):
        return int()

    @staticmethod
    def getMissionFromQueue(iIndex):
        return MissionData()

    @staticmethod
    def getMissionType(iNode):
        return int()

    @staticmethod
    def getNumUnits():
        return int()

    @staticmethod
    def getOwner():
        return -1  # Type

    @staticmethod
    def getPathEndTurnPlot():
        return CyPlot()

    @staticmethod
    def getPathFirstPlot():
        return CyPlot()

    @staticmethod
    def getTeam():
        return -1  # Type

    @staticmethod
    def getUnitAt(index):
        return CyUnit()

    @staticmethod
    def hasCargo():
        return bool()

    @staticmethod
    def hasMoved():
        return bool()

    @staticmethod
    def hasWorker():
        return bool()

    @staticmethod
    def isAmphibPlot(pPlot):
        return bool()

    @staticmethod
    def isAutomated():
        return bool()

    @staticmethod
    def isFull():
        return bool()

    @staticmethod
    def isHuman():
        return bool()

    @staticmethod
    def isInvisible(eTeam):
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isWaiting():
        return bool()

    @staticmethod
    def lastMissionPlot():
        return CyPlot()

    @staticmethod
    def plot():
        return CyPlot()

    @staticmethod
    def popMission():
        pass

    @staticmethod
    def pushMission(eMission, iData1, iData2, iFlags, bAppend, bManual, eMissionAI, pMissionAIPlot, pMissionAIUnit):
        pass

    @staticmethod
    def pushMoveToMission(iX, iY):
        pass

    @staticmethod
    def readyToAuto():
        return bool()

    @staticmethod
    def readyToMove(bAny):
        return bool()

    @staticmethod
    def readyToSelect(bAny):
        return bool()

    @staticmethod
    def resetPath():
        pass

    @staticmethod
    def setActivityType(eNewValue):
        pass

    @staticmethod
    def setAutomateType(eNewValue):
        pass


class CySign:

    @staticmethod
    def getCaption():
        return str()

    @staticmethod
    def getPlayerType():
        return -1  # Type

    @staticmethod
    def getPlot():
        return CyPlot()


class CyStatistics:

    @staticmethod
    def getPlayerNumBuildingsBuilt(iPlayerID, iBuildingID):
        return int()

    @staticmethod
    def getPlayerNumCitiesBuilt(iPlayerID):
        return int()

    @staticmethod
    def getPlayerNumCitiesRazed(iPlayerID):
        return int()

    @staticmethod
    def getPlayerNumGoldenAges(iPlayerID):
        return int()

    @staticmethod
    def getPlayerNumUnitsBuilt(iPlayerID, iUnitID):
        return int()

    @staticmethod
    def getPlayerNumUnitsKilled(iPlayerID, iUnitID):
        return int()

    @staticmethod
    def getPlayerNumUnitsLost(iPlayerID, iUnitID):
        return int()

    @staticmethod
    def getPlayerReligionFounded(iPlayerID, iReligionID):
        return bool()

    @staticmethod
    def getPlayerTimePlayed(iPlayerID):
        return int()


class CyTeam:

    @staticmethod
    def AI_getAtPeaceCounter(eTeam):
        return int()

    @staticmethod
    def AI_getAtWarCounter(eTeam):
        return int()

    @staticmethod
    def AI_getWarSuccess(eIndex):
        return int()

    @staticmethod
    def AI_setWarPlan(eIndex, eNewValue):
        pass

    @staticmethod
    def AI_shareWar(eTeam):
        return bool()

    @staticmethod
    def addTeam(eTeam):
        pass

    @staticmethod
    def assignVassal(eIndex, bSurrender):
        pass

    @staticmethod
    def canChangeWarPeace(eTeam):
        return bool()

    @staticmethod
    def canContact(eTeam):
        return bool()

    @staticmethod
    def canDeclareWar(eTeam):
        return bool()

    @staticmethod
    def canLaunch(eVictory):
        return bool()

    @staticmethod
    def changeBridgeBuildingCount(iChange):
        pass

    @staticmethod
    def changeCommerceFlexibleCount(eIndex, iChange):
        pass

    @staticmethod
    def changeCounterespionageModAgainstTeam(eIndex, iChange):
        pass

    @staticmethod
    def changeCounterespionageTurnsLeftAgainstTeam(eIndex, iChange):
        pass

    @staticmethod
    def changeDefensivePactTradingCount(iChange):
        pass

    @staticmethod
    def changeEnemyWarWearinessModifier(iChange):
        pass

    @staticmethod
    def changeEspionagePointsAgainstTeam(eIndex, iChange):
        pass

    @staticmethod
    def changeEspionagePointsEver(iChange):
        pass

    @staticmethod
    def changeExtraMoves(eIndex, iChange):
        pass

    @staticmethod
    def changeExtraWaterSeeFromCount(iChange):
        pass

    @staticmethod
    def changeForceTeamVoteEligibilityCount(eVoteSource, iChange):
        pass

    @staticmethod
    def changeGoldTradingCount(iChange):
        pass

    @staticmethod
    def changeIgnoreIrrigationCount(iChange):
        pass

    @staticmethod
    def changeImprovementYieldChange(eIndex1, eIndex2, iChange):
        pass

    @staticmethod
    def changeIrrigationCount(iChange):
        pass

    @staticmethod
    def changeMapTradingCount(iChange):
        pass

    @staticmethod
    def changeNukeInterception(iChange):
        pass

    @staticmethod
    def changeOpenBordersTradingCount(iChange):
        pass

    @staticmethod
    def changePermanentAllianceTradingCount(iChange):
        pass

    @staticmethod
    def changeProjectCount(eIndex, iChange):
        pass

    @staticmethod
    def changeResearchProgress(eIndex, iChange, ePlayer):
        pass

    @staticmethod
    def changeRouteChange(eIndex, iChange):
        pass

    @staticmethod
    def changeTechShareCount(iIndex, iChange):
        pass

    @staticmethod
    def changeTechTradingCount(iChange):
        pass

    @staticmethod
    def changeVassalTradingCount(iChange):
        pass

    @staticmethod
    def changeWarWeariness(eIndex, iChange):
        pass

    @staticmethod
    def changeWaterWorkCount(iChange):
        pass

    @staticmethod
    def countEnemyDangerByArea(pArea):
        return int()

    @staticmethod
    def countEnemyPowerByArea(pArea):
        return int()

    @staticmethod
    def countNumAIUnitsByArea(pArea, eUnitAI):
        return int()

    @staticmethod
    def countNumCitiesByArea(pArea):
        return int()

    @staticmethod
    def countNumUnitsByArea(pArea):
        return int()

    @staticmethod
    def countPowerByArea(pArea):
        return int()

    @staticmethod
    def countTotalCulture():
        return int()

    @staticmethod
    def countTotalPopulationByArea(pArea):
        return int()

    @staticmethod
    def declareWar(eTeam, bNewDiplo, eWarPlan):
        pass

    @staticmethod
    def freeVassal(eIndex):
        pass

    @staticmethod
    def getAnyWarPlanCount(bIgnoreMinors):
        return int()

    @staticmethod
    def getAssets():
        return int()

    @staticmethod
    def getAtWarCount(bIgnoreMinors):
        return int()

    @staticmethod
    def getBridgeBuildingCount():
        return int()

    @staticmethod
    def getBuildingClassCount(eIndex):
        return int()

    @staticmethod
    def getBuildingClassCountPlusMaking(eUnitClass):
        return int()

    @staticmethod
    def getBuildingClassMaking(eBuildingClass):
        return int()

    @staticmethod
    def getChosenWarCount(bIgnoreMinors):
        return int()

    @staticmethod
    def getCommerceFlexibleCount(eIndex):
        return int()

    @staticmethod
    def getCounterespionageModAgainstTeam(eIndex):
        return int()

    @staticmethod
    def getCounterespionageTurnsLeftAgainstTeam(eIndex):
        return int()

    @staticmethod
    def getDefensivePactCount():
        return int()

    @staticmethod
    def getDefensivePactTradingCount():
        return int()

    @staticmethod
    def getDefensivePower():
        return int()

    @staticmethod
    def getEnemyWarWearinessModifier():
        return int()

    @staticmethod
    def getEspionagePointsAgainstTeam(eIndex):
        return int()

    @staticmethod
    def getEspionagePointsEver():
        return int()

    @staticmethod
    def getExtraMoves(eIndex):
        return int()

    @staticmethod
    def getExtraWaterSeeFromCount():
        return int()

    @staticmethod
    def getForceTeamVoteEligibilityCount(eVoteSource):
        return int()

    @staticmethod
    def getGoldTradingCount():
        return int()

    @staticmethod
    def getHandicapType():
        return -1  # Type

    @staticmethod
    def getHasCorporationCount(eCorporation):
        return int()

    @staticmethod
    def getHasMetCivCount(bIgnoreMinors):
        return int()

    @staticmethod
    def getHasReligionCount(eReligion):
        return int()

    @staticmethod
    def getID():
        return int()

    @staticmethod
    def getIgnoreIrrigationCount():
        return int()

    @staticmethod
    def getImprovementYieldChange(eIndex, eIndex2):
        return int()

    @staticmethod
    def getIrrigationCount():
        return int()

    @staticmethod
    def getLaunchSuccessRate(eVictory):
        return int()

    @staticmethod
    def getLeaderID():
        return -1  # Type

    @staticmethod
    def getMapTradingCount():
        return int()

    @staticmethod
    def getMasterPower():
        return int()

    @staticmethod
    def getName():
        return str()

    @staticmethod
    def getNukeInterception():
        return int()

    @staticmethod
    def getNumCities():
        return int()

    @staticmethod
    def getNumMembers():
        return int()

    @staticmethod
    def getNumNukeUnits():
        return int()

    @staticmethod
    def getObsoleteBuildingCount(eIndex):
        return int()

    @staticmethod
    def getOpenBordersTradingCount():
        return int()

    @staticmethod
    def getPermanentAllianceTradingCount():
        return int()

    @staticmethod
    def getPower(bIncludeVassals):
        return int()

    @staticmethod
    def getProjectArtType(eIndex, number):
        return int()

    @staticmethod
    def getProjectCount(eIndex):
        return int()

    @staticmethod
    def getProjectDefaultArtType(eIndex):
        return int()

    @staticmethod
    def getProjectMaking(eIndex):
        return int()

    @staticmethod
    def getResearchCost(eTech):
        return int()

    @staticmethod
    def getResearchLeft(eTech):
        return int()

    @staticmethod
    def getResearchProgress(eIndex):
        return int()

    @staticmethod
    def getRouteChange(eIndex):
        return int()

    @staticmethod
    def getSecretaryID():
        return -1  # Type

    @staticmethod
    def getTechCount(eIndex):
        return int()

    @staticmethod
    def getTechShareCount(iIndex):
        return int()

    @staticmethod
    def getTechTradingCount():
        return int()

    @staticmethod
    def getTotalLand():
        return int()

    @staticmethod
    def getTotalPopulation():
        return int()

    @staticmethod
    def getUnitClassCount(eIndex):
        return int()

    @staticmethod
    def getUnitClassCountPlusMaking(eUnitClass):
        return int()

    @staticmethod
    def getUnitClassMaking(eUnitClass):
        return int()

    @staticmethod
    def getVassalPower():
        return int()

    @staticmethod
    def getVassalTradingCount():
        return int()

    @staticmethod
    def getVictoryCountdown(eVictory):
        return int()

    @staticmethod
    def getVictoryDelay(eVictory):
        return int()

    @staticmethod
    def getWarPlanCount(eWarPlan, bIgnoreMinors):
        return int()

    @staticmethod
    def getWarWeariness(eIndex):
        return int()

    @staticmethod
    def getWaterWorkCount():
        return int()

    @staticmethod
    def hasHeadquarters(eCorporation):
        return bool()

    @staticmethod
    def hasHolyCity(eReligion):
        return bool()

    @staticmethod
    def hasMetHuman():
        return bool()

    @staticmethod
    def isAVassal():
        return bool()

    @staticmethod
    def isAlive():
        return bool()

    @staticmethod
    def isAtWar(eIndex):
        return bool()

    @staticmethod
    def isBarbarian():
        return bool()

    @staticmethod
    def isBridgeBuilding():
        return bool()

    @staticmethod
    def isBuildingClassMaxedOut(eIndex, iExtra):
        return bool()

    @staticmethod
    def isCommerceFlexible(eIndex):
        return bool()

    @staticmethod
    def isDefensivePact(eIndex):
        return bool()

    @staticmethod
    def isDefensivePactTrading():
        return bool()

    @staticmethod
    def isEverAlive():
        return bool()

    @staticmethod
    def isExtraWaterSeeFrom():
        return bool()

    @staticmethod
    def isForcePeace(eIndex):
        return bool()

    @staticmethod
    def isForceTeamVoteEligible(eVoteSource):
        return bool()

    @staticmethod
    def isFreeTrade(eIndex):
        return bool()

    @staticmethod
    def isGoldTrading():
        return bool()

    @staticmethod
    def isHasMet(eIndex):
        return bool()

    @staticmethod
    def isHasTech(iIndex):
        return bool()

    @staticmethod
    def isHuman():
        return bool()

    @staticmethod
    def isIgnoreIrrigation():
        return bool()

    @staticmethod
    def isIrrigation():
        return bool()

    @staticmethod
    def isMapCentering():
        return bool()

    @staticmethod
    def isMapTrading():
        return bool()

    @staticmethod
    def isMinorCiv():
        return bool()

    @staticmethod
    def isNoTradeTech(iIndex):
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isObsoleteBuilding(eIndex):
        return bool()

    @staticmethod
    def isOpenBorders(eIndex):
        return bool()

    @staticmethod
    def isOpenBordersTrading():
        return bool()

    @staticmethod
    def isPermanentAllianceTrading():
        return bool()

    @staticmethod
    def isPermanentWarPeace(eIndex):
        return bool()

    @staticmethod
    def isProjectAndArtMaxedOut(eIndex):
        return bool()

    @staticmethod
    def isProjectMaxedOut(eIndex, iExtra):
        return bool()

    @staticmethod
    def isRiverTrade():
        return bool()

    @staticmethod
    def isStolenVisibility(eIndex):
        return bool()

    @staticmethod
    def isTechShare(iIndex):
        return bool()

    @staticmethod
    def isTechTrading():
        return bool()

    @staticmethod
    def isTerrainTrade(eIndex):
        return bool()

    @staticmethod
    def isUnitClassMaxedOut(eIndex, iExtra):
        return bool()

    @staticmethod
    def isVassal(eIndex):
        return bool()

    @staticmethod
    def isVassalStateTrading():
        return bool()

    @staticmethod
    def isWaterWork():
        return bool()

    @staticmethod
    def makePeace(eTeam):
        pass

    @staticmethod
    def meet(eTeam, bNewDiplo):
        pass

    @staticmethod
    def setCounterespionageModAgainstTeam(eIndex, iValue):
        pass

    @staticmethod
    def setCounterespionageTurnsLeftAgainstTeam(eIndex, iValue):
        pass

    @staticmethod
    def setEspionagePointsAgainstTeam(eIndex, iValue):
        pass

    @staticmethod
    def setEspionagePointsEver(iValue):
        pass

    @staticmethod
    def setHasTech(eIndex, bNewValue, ePlayer, bFirst, bAnnounce):
        pass

    @staticmethod
    def setMapCentering(bNewValue):
        pass

    @staticmethod
    def setMasterPower(iPower):
        pass

    @staticmethod
    def setNoTradeTech(eIndex, bNewValue):
        pass

    @staticmethod
    def setPermanentWarPeace(eIndex, bNewValue):
        pass

    @staticmethod
    def setProjectArtType(eIndex, number, value):
        pass

    @staticmethod
    def setProjectDefaultArtType(eIndex, value):
        pass

    @staticmethod
    def setResearchProgress(eIndex, iNewValue, ePlayer):
        pass

    @staticmethod
    def setVassal(eIndex, bVassal, bCapitulated):
        pass

    @staticmethod
    def setVassalPower(iPower):
        pass

    @staticmethod
    def setWarWeariness(eIndex, iNewValue):
        pass

    @staticmethod
    def signDefensivePact(eTeam):
        pass

    @staticmethod
    def signOpenBorders(eTeam):
        pass


class CyTranslator:

    @staticmethod
    def changeTextColor(szText, iColor):
        return str()

    @staticmethod
    def getColorText(szTag, args, iColor):
        return str()

    @staticmethod
    def getObjectText(szTag, i):
        return str()

    @staticmethod
    def getText(szTag, args):
        return str()

    @staticmethod
    def stripHTML(szText):
        return str()


class CyUnit:

    @staticmethod
    def IsSelected():
        return bool()

    @staticmethod
    def NotifyEntity(eMission):
        pass

    @staticmethod
    def airBaseCombatStr():
        return int()

    @staticmethod
    def airBombBaseRate():
        return int()

    @staticmethod
    def airBombCurrRate():
        return int()

    @staticmethod
    def airCombatDamage(pDefender):
        return int()

    @staticmethod
    def airCombatLimit():
        return int()

    @staticmethod
    def airCurrCombatStr(pOther):
        return int()

    @staticmethod
    def airCurrCombatStrFloat(pOther):
        return float()

    @staticmethod
    def airMaxCombatStr(pOther):
        return int()

    @staticmethod
    def airMaxCombatStrFloat(pOther):
        return float()

    @staticmethod
    def airRange():
        return int()

    @staticmethod
    def alwaysInvisible():
        return bool()

    @staticmethod
    def animalCombatModifier():
        return int()

    @staticmethod
    def area():
        return CyArea()

    @staticmethod
    def at(iX, iY):
        return bool()

    @staticmethod
    def atPlot(pPlot):
        return bool()

    @staticmethod
    def attackForDamage(pDefender, attakerDamageChange, defenderDamageChange):
        pass

    @staticmethod
    def attackXPValue():
        return int()

    @staticmethod
    def baseCombatStr():
        return int()

    @staticmethod
    def baseMoves():
        return int()

    @staticmethod
    def bestInterceptor(pPlot):
        return CyUnit()

    @staticmethod
    def bestSeaPillageInterceptor(pPlot):
        return CyUnit()

    @staticmethod
    def bombardRate():
        return int()

    @staticmethod
    def bombardTarget(pPlot):
        return CyCity()

    @staticmethod
    def canAcquirePromotion(ePromotion):
        return bool()

    @staticmethod
    def canAcquirePromotionAny():
        return bool()

    @staticmethod
    def canAirAttack():
        return bool()

    @staticmethod
    def canAirBomb(pPlot):
        return bool()

    @staticmethod
    def canAirBombAt(pPlot, iX, iY):
        return bool()

    @staticmethod
    def canAirDefend(pPlot):
        return bool()

    @staticmethod
    def canAirPatrol(pPlot):
        return bool()

    @staticmethod
    def canAirlift(pPlot):
        return bool()

    @staticmethod
    def canAirliftAt(pPlot, iX, iY):
        return bool()

    @staticmethod
    def canAttack():
        return bool()

    @staticmethod
    def canAutomate(eAutomate):
        return bool()

    @staticmethod
    def canBombard(pPlot):
        return bool()

    @staticmethod
    def canBuild(pPlot, eBuild, bTestVisible):
        return bool()

    @staticmethod
    def canBuildRoute():
        return bool()

    @staticmethod
    def canCargoAllMove():
        return bool()

    @staticmethod
    def canCoexistWithEnemyUnit(eTeam):
        return bool()

    @staticmethod
    def canConstruct(pPlot, eBuilding):
        return bool()

    @staticmethod
    def canDefend(pPlot):
        return bool()

    @staticmethod
    def canDestroy(pPlot, bTestVisible):
        return bool()

    @staticmethod
    def canDiscover(pPlot):
        return bool()

    @staticmethod
    def canDoCommand(eCommand, iData1, iData2, bTestVisible):
        return bool()

    @staticmethod
    def canEnterArea(eTeam, pArea, bIgnoreRightOfPassage):
        return bool()

    @staticmethod
    def canEnterTerritory(eTeam, bIgnoreRightOfPassage):
        return bool()

    @staticmethod
    def canEspionage(pPlot):
        return bool()

    @staticmethod
    def canFight():
        return bool()

    @staticmethod
    def canFortify(pPlot):
        return bool()

    @staticmethod
    def canFound(pPlot, bTestVisible):
        return bool()

    @staticmethod
    def canGift(bTestVisible):
        return bool()

    @staticmethod
    def canGiveExperience(pPlot):
        return int()

    @staticmethod
    def canGoldenAge(pPlot, bTestVisible):
        return bool()

    @staticmethod
    def canGreatWork(pPlot):
        return bool()

    @staticmethod
    def canHeal(pPlot):
        return bool()

    @staticmethod
    def canHold(pPlot):
        return bool()

    @staticmethod
    def canHurry(pPlot, bTestVisible):
        return bool()

    @staticmethod
    def canInfiltrate(pPlot, bTestVisible):
        return bool()

    @staticmethod
    def canJoin(pPlot, eSpecialist):
        return bool()

    @staticmethod
    def canLead(pPlot, iUnitId):
        return int()

    @staticmethod
    def canLoad(pPlot):
        return bool()

    @staticmethod
    def canLoadUnit(pUnit, pPlot):
        return bool()

    @staticmethod
    def canMove():
        return bool()

    @staticmethod
    def canMoveAllTerrain():
        return bool()

    @staticmethod
    def canMoveImpassable():
        return bool()

    @staticmethod
    def canMoveInto(pPlot, bAttack, bDeclareWar, bIgnoreLoad):
        return bool()

    @staticmethod
    def canMoveOrAttackInto(pPlot, bDeclareWar):
        return bool()

    @staticmethod
    def canMoveThrough(pPlot):
        return bool()

    @staticmethod
    def canNuke(pPlot):
        return bool()

    @staticmethod
    def canNukeAt(pPlot, iX, iY):
        return bool()

    @staticmethod
    def canPillage(pPlot):
        return bool()

    @staticmethod
    def canPlunder(pPlot):
        return bool()

    @staticmethod
    def canPromote(ePromotion, iLeaderUnitId):
        return bool()

    @staticmethod
    def canRecon(pPlot):
        return bool()

    @staticmethod
    def canReconAt(pPlot, iX, iY):
        return bool()

    @staticmethod
    def canSabotage(pPlot, bTestVisible):
        return bool()

    @staticmethod
    def canScrap():
        return bool()

    @staticmethod
    def canSeaPatrol(pPlot):
        return bool()

    @staticmethod
    def canSentry(pPlot):
        return bool()

    @staticmethod
    def canSiege(eTeam):
        return bool()

    @staticmethod
    def canSleep(pPlot):
        return bool()

    @staticmethod
    def canSpread(pPlot, eReligion, bTestVisible):
        return bool()

    @staticmethod
    def canStealPlans(pPlot, bTestVisible):
        return bool()

    @staticmethod
    def canTrade(pPlot, bTestVisible):
        return bool()

    @staticmethod
    def canUnload():
        return bool()

    @staticmethod
    def canUnloadAll():
        return bool()

    @staticmethod
    def canUpgrade(eUnit, bTestVisible):
        return bool()

    @staticmethod
    def cargoSpace():
        return int()

    @staticmethod
    def cargoSpaceAvailable(eSpecialCargo, eDomainCargo):
        return int()

    @staticmethod
    def centerCamera():
        pass

    @staticmethod
    def chanceFirstStrikes():
        return int()

    @staticmethod
    def changeCargoSpace(iChange):
        pass

    @staticmethod
    def changeDamage(iChange, ePlayer):
        pass

    @staticmethod
    def changeExperience(iChange, iMax, bFromCombat, bInBorders, bUpdateGlobal):
        pass

    @staticmethod
    def changeLevel(iChange):
        pass

    @staticmethod
    def changeMoves(iChange):
        pass

    @staticmethod
    def cityAttackModifier():
        return int()

    @staticmethod
    def cityDefenseModifier():
        return int()

    @staticmethod
    def collateralDamage():
        return int()

    @staticmethod
    def collateralDamageLimit():
        return int()

    @staticmethod
    def collateralDamageMaxUnits():
        return int()

    @staticmethod
    def combatLimit():
        return int()

    @staticmethod
    def convert(pUnit):
        pass

    @staticmethod
    def currCombatStr(pPlot, pAttacker):
        return int()

    @staticmethod
    def currCombatStrFloat(pPlot, pAttacker):
        return float()

    @staticmethod
    def currFirepower(pPlot, pAttacker):
        return int()

    @staticmethod
    def currHitPoints():
        return int()

    @staticmethod
    def currInterceptionProbability():
        return int()

    @staticmethod
    def defenseXPValue():
        return int()

    @staticmethod
    def destroyCost(pPlot):
        return int()

    @staticmethod
    def destroyProb(pPlot, eProbStyle):
        return int()

    @staticmethod
    def doCommand(eCommand, iData1, iData2):
        pass

    @staticmethod
    def domainCargo():
        return -1  # Type

    @staticmethod
    def domainModifier(eDomain):
        return int()

    @staticmethod
    def evasionProbability():
        return int()

    @staticmethod
    def experienceNeeded():
        return int()

    @staticmethod
    def featureAttackModifier(eFeature):
        return int()

    @staticmethod
    def featureDefenseModifier(eFeature):
        return int()

    @staticmethod
    def finishMoves():
        pass

    @staticmethod
    def firstStrikes():
        return int()

    @staticmethod
    def flatMovementCost():
        return bool()

    @staticmethod
    def flavorValue(eFlavor):
        return int()

    @staticmethod
    def fortifyModifier():
        return int()

    @staticmethod
    def generatePath(pToPlot, iFlags, bReuse, piPathTurns):
        return bool()

    @staticmethod
    def getAdjacentTileHeal():
        return int()

    @staticmethod
    def getAmphibCount():
        return int()

    @staticmethod
    def getArtInfo(i, eEra):
        return CvArtInfoUnit()

    @staticmethod
    def getBlitzCount():
        return int()

    @staticmethod
    def getBuildType():
        return -1  # Type

    @staticmethod
    def getButton():
        return str()

    @staticmethod
    def getCaptureUnitType(eCivilization):
        return -1  # Type

    @staticmethod
    def getCargo():
        return int()

    @staticmethod
    def getCivilizationType():
        return -1  # Type

    @staticmethod
    def getCollateralDamageProtection():
        return int()

    @staticmethod
    def getCombatOwner(iForTeam):
        return int()

    @staticmethod
    def getDamage():
        return int()

    @staticmethod
    def getDeclareWarMove(pPlot):
        return -1  # Type

    @staticmethod
    def getDiscoverResearch(eTech):
        return int()

    @staticmethod
    def getDiscoveryTech():
        return -1  # Type

    @staticmethod
    def getDomainType():
        return -1  # Type

    @staticmethod
    def getEspionagePoints(pPlot):
        return int()

    @staticmethod
    def getExperience():
        return int()

    @staticmethod
    def getExperiencePercent():
        return int()

    @staticmethod
    def getExtraAirRange():
        return int()

    @staticmethod
    def getExtraChanceFirstStrikes():
        return int()

    @staticmethod
    def getExtraCityAttackPercent():
        return int()

    @staticmethod
    def getExtraCityDefensePercent():
        return int()

    @staticmethod
    def getExtraCollateralDamage():
        return int()

    @staticmethod
    def getExtraCombatPercent():
        return int()

    @staticmethod
    def getExtraDomainModifier(eIndex):
        return int()

    @staticmethod
    def getExtraEnemyHeal():
        return int()

    @staticmethod
    def getExtraEvasion():
        return int()

    @staticmethod
    def getExtraFeatureAttackPercent(eIndex):
        return int()

    @staticmethod
    def getExtraFeatureDefensePercent(eIndex):
        return int()

    @staticmethod
    def getExtraFirstStrikes():
        return int()

    @staticmethod
    def getExtraFriendlyHeal():
        return int()

    @staticmethod
    def getExtraHillsAttackPercent():
        return int()

    @staticmethod
    def getExtraHillsDefensePercent():
        return int()

    @staticmethod
    def getExtraIntercept():
        return int()

    @staticmethod
    def getExtraMoveDiscount():
        return int()

    @staticmethod
    def getExtraMoves():
        return int()

    @staticmethod
    def getExtraNeutralHeal():
        return int()

    @staticmethod
    def getExtraTerrainAttackPercent(eIndex):
        return int()

    @staticmethod
    def getExtraTerrainDefensePercent(eIndex):
        return int()

    @staticmethod
    def getExtraUnitCombatModifier(eIndex):
        return int()

    @staticmethod
    def getExtraVisibilityRange():
        return int()

    @staticmethod
    def getExtraWithdrawal():
        return int()

    @staticmethod
    def getFacingDirection():
        return int()

    @staticmethod
    def getFortifyTurns():
        return int()

    @staticmethod
    def getGameTurnCreated():
        return int()

    @staticmethod
    def getGreatWorkCulture(pPlot):
        return int()

    @staticmethod
    def getGroup():
        return CySelectionGroup()

    @staticmethod
    def getGroupID():
        return int()

    @staticmethod
    def getHandicapType():
        return -1  # Type

    @staticmethod
    def getHotKeyNumber():
        return int()

    @staticmethod
    def getHurryProduction(pPlot):
        return int()

    @staticmethod
    def getID():
        return int()

    @staticmethod
    def getImmobileTimer():
        return int()

    @staticmethod
    def getInvisibleType():
        return -1  # Type

    @staticmethod
    def getKamikazePercent():
        return int()

    @staticmethod
    def getLeaderUnitType():
        return -1  # Type

    @staticmethod
    def getLevel():
        return int()

    @staticmethod
    def getMaxHurryProduction(pCity):
        return int()

    @staticmethod
    def getMoves():
        return int()

    @staticmethod
    def getName():
        return str()

    @staticmethod
    def getNameForm(iForm):
        return str()

    @staticmethod
    def getNameKey():
        return str()

    @staticmethod
    def getNameNoDesc():
        return str()

    @staticmethod
    def getNumSeeInvisibleTypes():
        return int()

    @staticmethod
    def getOwner():
        return int()

    @staticmethod
    def getPathEndTurnPlot():
        return CyPlot()

    @staticmethod
    def getPillageChange():
        return int()

    @staticmethod
    def getReconPlot():
        return CyPlot()

    @staticmethod
    def getRevoltProtection():
        return int()

    @staticmethod
    def getRiverCount():
        return int()

    @staticmethod
    def getSameTileHeal():
        return int()

    @staticmethod
    def getScriptData():
        return str()

    @staticmethod
    def getSeeInvisibleType(i):
        return -1  # Type

    @staticmethod
    def getSpecialUnitType():
        return -1  # Type

    @staticmethod
    def getTeam():
        return int()

    @staticmethod
    def getTradeGold(pPlot):
        return int()

    @staticmethod
    def getTransportUnit():
        return CyUnit()

    @staticmethod
    def getUnitAICargo(eUnitAI):
        return int()

    @staticmethod
    def getUnitAIType():
        return -1  # Type

    @staticmethod
    def getUnitClassType():
        return -1  # Type

    @staticmethod
    def getUnitCombatType():
        return -1  # Type

    @staticmethod
    def getUnitType():
        return -1  # Type

    @staticmethod
    def getUpgradeDiscount():
        return int()

    @staticmethod
    def getVisualOwner():
        return int()

    @staticmethod
    def getX():
        return int()

    @staticmethod
    def getY():
        return int()

    @staticmethod
    def giveExperience():
        return bool()

    @staticmethod
    def hasCargo():
        return bool()

    @staticmethod
    def hasMoved():
        return bool()

    @staticmethod
    def hasUpgrade(bSearch):
        return bool()

    @staticmethod
    def hillsAttackModifier():
        return int()

    @staticmethod
    def hillsDefenseModifier():
        return int()

    @staticmethod
    def ignoreBuildingDefense():
        return bool()

    @staticmethod
    def ignoreTerrainCost():
        return bool()

    @staticmethod
    def immuneToFirstStrikes():
        return bool()

    @staticmethod
    def isActionRecommended(i):
        return bool()

    @staticmethod
    def isAlwaysHeal():
        return bool()

    @staticmethod
    def isAmphib():
        return bool()

    @staticmethod
    def isAnimal():
        return bool()

    @staticmethod
    def isAttacking():
        return bool()

    @staticmethod
    def isAutomated():
        return bool()

    @staticmethod
    def isBarbarian():
        return bool()

    @staticmethod
    def isBetterDefenderThan(pDefender, pAttacker):
        return bool()

    @staticmethod
    def isBlitz():
        return bool()

    @staticmethod
    def isCargo():
        return bool()

    @staticmethod
    def isCombat():
        return bool()

    @staticmethod
    def isCounterSpy():
        return bool()

    @staticmethod
    def isDead():
        return bool()

    @staticmethod
    def isDefending():
        return bool()

    @staticmethod
    def isEnemyRoute():
        return bool()

    @staticmethod
    def isFeatureDoubleMove(eIndex):
        return bool()

    @staticmethod
    def isFighting():
        return bool()

    @staticmethod
    def isFortifyable():
        return bool()

    @staticmethod
    def isFound():
        return bool()

    @staticmethod
    def isFull():
        return bool()

    @staticmethod
    def isGoldenAge():
        return bool()

    @staticmethod
    def isGroupHead():
        return bool()

    @staticmethod
    def isHasPromotion(ePromotion):
        return bool()

    @staticmethod
    def isHillsDoubleMove():
        return bool()

    @staticmethod
    def isHuman():
        return bool()

    @staticmethod
    def isHurt():
        return bool()

    @staticmethod
    def isInGroup():
        return bool()

    @staticmethod
    def isInvestigate():
        return bool()

    @staticmethod
    def isInvisible(eTeam, bDebug):
        return bool()

    @staticmethod
    def isMadeAttack():
        return bool()

    @staticmethod
    def isMadeInterception():
        return bool()

    @staticmethod
    def isMilitaryHappiness():
        return bool()

    @staticmethod
    def isNeverInvisible():
        return bool()

    @staticmethod
    def isNoBadGoodies():
        return bool()

    @staticmethod
    def isNoCapture():
        return bool()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def isNukeImmune():
        return bool()

    @staticmethod
    def isNukeVictim(pPlot, eTeam):
        return bool()

    @staticmethod
    def isOnlyDefensive():
        return bool()

    @staticmethod
    def isPromotionReady():
        return bool()

    @staticmethod
    def isPromotionValid(ePromotion):
        return bool()

    @staticmethod
    def isRanged():
        return bool()

    @staticmethod
    def isRivalTerritory():
        return bool()

    @staticmethod
    def isRiver():
        return bool()

    @staticmethod
    def isTerrainDoubleMove(eIndex):
        return bool()

    @staticmethod
    def isWaiting():
        return bool()

    @staticmethod
    def jumpToNearestValidPlot():
        return bool()

    @staticmethod
    def kill(bDelay, ePlayer):
        pass

    @staticmethod
    def lead(iUnitId):
        return bool()

    @staticmethod
    def maxCombatStr(pPlot, pAttacker):
        return int()

    @staticmethod
    def maxCombatStrFloat(pPlot, pAttacker):
        return float()

    @staticmethod
    def maxFirstStrikes():
        return int()

    @staticmethod
    def maxHitPoints():
        return int()

    @staticmethod
    def maxInterceptionProbability():
        return int()

    @staticmethod
    def maxMoves():
        return int()

    @staticmethod
    def maxXPValue():
        return int()

    @staticmethod
    def movesLeft():
        return int()

    @staticmethod
    def noDefensiveBonus():
        return bool()

    @staticmethod
    def nukeRange():
        return int()

    @staticmethod
    def plot():
        return CyPlot()

    @staticmethod
    def promote(ePromotion, iLeaderUnitId):
        pass

    @staticmethod
    def rangeStrike(iX, iY):
        pass

    @staticmethod
    def rotateFacingDirectionClockwise():
        pass

    @staticmethod
    def rotateFacingDirectionCounterClockwise():
        pass

    @staticmethod
    def sabotageCost(pPlot):
        return int()

    @staticmethod
    def sabotageProb(pPlot, eProbStyle):
        return int()

    @staticmethod
    def setBaseCombatStr(iCombat):
        pass

    @staticmethod
    def setDamage(iNewValue, ePlayer):
        pass

    @staticmethod
    def setExperience(iNewValue, iMax):
        pass

    @staticmethod
    def setHasPromotion(eIndex, bNewValue):
        pass

    @staticmethod
    def setHotKeyNumber(iNewValue):
        pass

    @staticmethod
    def setImmobileTimer(iNewValue):
        pass

    @staticmethod
    def setLeaderUnitType(leaderUnitType):
        pass

    @staticmethod
    def setLevel(iNewLevel):
        pass

    @staticmethod
    def setMadeAttack(bNewValue):
        pass

    @staticmethod
    def setMadeInterception(bNewValue):
        pass

    @staticmethod
    def setMoves(iNewValue):
        pass

    @staticmethod
    def setName(szNewValue):
        pass

    @staticmethod
    def setPromotionReady(bNewValue):
        pass

    @staticmethod
    def setReconPlot(pNewValue):
        pass

    @staticmethod
    def setScriptData(szNewValue):
        pass

    @staticmethod
    def setTransportUnit(pTransportUnit):
        pass

    @staticmethod
    def setUnitAIType(iNewValue):
        pass

    @staticmethod
    def setXY(iX, iY, bGroup, bUpdate, bShow):
        pass

    @staticmethod
    def specialCargo():
        return -1  # Type

    @staticmethod
    def stealPlansCost(pPlot):
        return int()

    @staticmethod
    def stealPlansProb(pPlot, eProbStyle):
        return int()

    @staticmethod
    def terrainAttackModifier(eTerrain):
        return int()

    @staticmethod
    def terrainDefenseModifier(eTerrain):
        return int()

    @staticmethod
    def unitClassAttackModifier(eUnitClass):
        return int()

    @staticmethod
    def unitClassDefenseModifier(eUnitClass):
        return int()

    @staticmethod
    def unitCombatModifier(eUnitCombat):
        return int()

    @staticmethod
    def upgradeAvailable(eFromUnit, eToUnitClass, iCount):
        return bool()

    @staticmethod
    def upgradePrice(eUnit):
        return int()

    @staticmethod
    def visibilityRange():
        return int()

    @staticmethod
    def withdrawalProbability():
        return int()

    @staticmethod
    def workRate(bMax):
        return int()


class CyUnitEntity:

    @staticmethod
    def GetSubEntity(i):
        return CyUnitSubEntity()

    @staticmethod
    def GetSubEntityCount():
        return int()

    @staticmethod
    def GetUnitsCurrentlyAlive():
        return int()

    @staticmethod
    def MoveTo(x, y, z, rad):
        pass

    @staticmethod
    def NotifyEntity(e):
        pass

    @staticmethod
    def getScale():
        return float()

    @staticmethod
    def getUnit():
        return CyUnit()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def setScale(fScale):
        pass


class CyUnitSubEntity:

    @staticmethod
    def PlayAnimationPath(i):
        pass

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def setUnitShadow(b):
        pass

    @staticmethod
    def setVisible(b):
        pass


class CyUserProfile:

    @staticmethod
    def deleteProfileFile(szNewName):
        return bool()

    @staticmethod
    def getAmbienceVolume():
        return int()

    @staticmethod
    def getAntiAliasing():
        return int()

    @staticmethod
    def getAntiAliasingMaxMultiSamples():
        return int()

    @staticmethod
    def getCaptureDeviceDesc(iIndex):
        return str()

    @staticmethod
    def getCaptureDeviceIndex():
        return int()

    @staticmethod
    def getCaptureVolume():
        return int()

    @staticmethod
    def getCurrentVersion():
        return int()

    @staticmethod
    def getGlobeLayer():
        return int()

    @staticmethod
    def getGlobeViewRenderLevel():
        return int()

    @staticmethod
    def getGraphicOption(i):
        return bool()

    @staticmethod
    def getGraphicsLevel():
        return int()

    @staticmethod
    def getGrid():
        return bool()

    @staticmethod
    def getInterfaceVolume():
        return int()

    @staticmethod
    def getMainMenu():
        return int()

    @staticmethod
    def getMap():
        return bool()

    @staticmethod
    def getMasterVolume():
        return int()

    @staticmethod
    def getMaxCaptureVolume():
        return int()

    @staticmethod
    def getMaxPlaybackVolume():
        return int()

    @staticmethod
    def getMovieQualityLevel():
        return int()

    @staticmethod
    def getMusicPath():
        return str()

    @staticmethod
    def getMusicVolume():
        return int()

    @staticmethod
    def getNumCaptureDevices():
        return int()

    @staticmethod
    def getNumPlaybackDevices():
        return int()

    @staticmethod
    def getNumProfileFiles():
        return int()

    @staticmethod
    def getPlaybackDeviceDesc(iIndex):
        return str()

    @staticmethod
    def getPlaybackDeviceIndex():
        return int()

    @staticmethod
    def getPlaybackVolume():
        return int()

    @staticmethod
    def getPlayerOption(i):
        return bool()

    @staticmethod
    def getProfileFileName(iFileID):
        return str()

    @staticmethod
    def getProfileName():
        return str()

    @staticmethod
    def getProfileVersion():
        return int()

    @staticmethod
    def getRenderQualityLevel():
        return int()

    @staticmethod
    def getResolution():
        return int()

    @staticmethod
    def getResolutionMaxModes():
        return int()

    @staticmethod
    def getResolutionString(iResolution):
        return str()

    @staticmethod
    def getScores():
        return bool()

    @staticmethod
    def getSoundEffectsVolume():
        return int()

    @staticmethod
    def getSpeakerConfig():
        return str()

    @staticmethod
    def getSpeakerConfigFromList(iIndex):
        return str()

    @staticmethod
    def getSpeechVolume():
        return int()

    @staticmethod
    def getVolumeStops():
        return int()

    @staticmethod
    def getYields():
        return bool()

    @staticmethod
    def is24Hours():
        return bool()

    @staticmethod
    def isAmbienceNoSound():
        return bool()

    @staticmethod
    def isClockOn():
        return bool()

    @staticmethod
    def isInterfaceNoSound():
        return bool()

    @staticmethod
    def isMasterNoSound():
        return bool()

    @staticmethod
    def isMusicNoSound():
        return bool()

    @staticmethod
    def isProfileFileExist(szNewName):
        return bool()

    @staticmethod
    def isSoundEffectsNoSound():
        return bool()

    @staticmethod
    def isSpeechNoSound():
        return bool()

    @staticmethod
    def loadProfileFileNames():
        pass

    @staticmethod
    def musicPathDialogBox():
        pass

    @staticmethod
    def readFromFile(szFileName):
        return bool()

    @staticmethod
    def recalculateAudioSettings():
        pass

    @staticmethod
    def resetOptions(resetTab):
        pass

    @staticmethod
    def set24Hours(bValue):
        pass

    @staticmethod
    def setAmbienceNoSound(b):
        pass

    @staticmethod
    def setAmbienceVolume(i):
        pass

    @staticmethod
    def setAntiAliasing(i):
        pass

    @staticmethod
    def setCaptureDevice(device):
        pass

    @staticmethod
    def setCaptureVolume(volume):
        pass

    @staticmethod
    def setClockJustTurnedOn(bValue):
        pass

    @staticmethod
    def setClockOn(bValue):
        pass

    @staticmethod
    def setGlobeViewRenderLevel(level):
        pass

    @staticmethod
    def setGraphicOption(i, b):
        pass

    @staticmethod
    def setGraphicsLevel(i):
        pass

    @staticmethod
    def setInterfaceNoSound(b):
        pass

    @staticmethod
    def setInterfaceVolume(i):
        pass

    @staticmethod
    def setMainMenu(i):
        pass

    @staticmethod
    def setMasterNoSound(b):
        pass

    @staticmethod
    def setMasterVolume(i):
        pass

    @staticmethod
    def setMovieQualityLevel(level):
        pass

    @staticmethod
    def setMusicNoSound(b):
        pass

    @staticmethod
    def setMusicPath(szMusicPath):
        pass

    @staticmethod
    def setMusicVolume(i):
        pass

    @staticmethod
    def setPlaybackDevice(device):
        pass

    @staticmethod
    def setPlaybackVolume(volume):
        pass

    @staticmethod
    def setProfileName(szNewName):
        pass

    @staticmethod
    def setRenderQualityLevel(level):
        pass

    @staticmethod
    def setResolution(i):
        pass

    @staticmethod
    def setSoundEffectsNoSound(b):
        pass

    @staticmethod
    def setSoundEffectsVolume(i):
        pass

    @staticmethod
    def setSpeakerConfig(szConfigName):
        pass

    @staticmethod
    def setSpeechNoSound(b):
        pass

    @staticmethod
    def setSpeechVolume(i):
        pass

    @staticmethod
    def setUseVoice(b):
        pass

    @staticmethod
    def useVoice():
        return bool()

    @staticmethod
    def wasClockJustTurnedOn():
        return bool()

    @staticmethod
    def writeToFile(szFileName):
        pass


class CyVariableSystem:

    @staticmethod
    def getFirstVariableName():
        return str()

    @staticmethod
    def getNextVariableName():
        return str()

    @staticmethod
    def getValueFloat(szVarName):
        return float()

    @staticmethod
    def getValueInt(szVarName):
        return int()

    @staticmethod
    def getValueString(szVarName):
        return str()

    @staticmethod
    def getVariableType(szVariable):
        return str()

    @staticmethod
    def isNone():
        return bool()

    @staticmethod
    def setValueFloat(szVarName, fValue):
        pass

    @staticmethod
    def setValueInt(szVarName, iValue):
        pass

    @staticmethod
    def setValueString(szVarName, szValue):
        pass


class EventMessage:

    iExpirationTurn = int()

    @staticmethod
    def getDescription():
        return str()


class EventTriggeredData:

    eBuilding = int()
    eCorporation = int()
    eOtherPlayer = int()
    ePlayer = int()
    eReligion = int()
    eTrigger = int()
    iCityId = int()
    iId = int()
    iOtherPlayerCityId = int()
    iPlotX = int()
    iPlotY = int()
    iTurn = int()
    iUnitId = int()


class FOWVis:

    uiCount = int()

    @staticmethod
    def getOffsets(i):
        return POINT()


class GameTurnInfo:

    iMonthIncrement = int()
    iNumGameTurnsPerIncrement = int()


class IDInfo:

    eOwner = int()
    iID = int()


class MissionData:

    eMissionType = int()
    iData1 = int()
    iData2 = int()
    iFlags = int()
    iPushTurn = int()


class NiColorA:

    def __init__(self, r, g, b, a):
        pass

    a = float()
    b = float()
    g = float()
    r = float()


class NiMatrix3:

    @staticmethod
    def GetEntry(uiRow, uiCol):
        return float()

    @staticmethod
    def MakeIdentity():
        pass

    @staticmethod
    def SetEntry(uiRow, uiCol, fEntry):
        pass


class NiPoint2:

    def __init__(self, x, y):
        pass

    x = float()
    y = float()


class NiPoint3:

    def __init__(self, x, y, z):
        pass

    x = float()
    y = float()
    z = float()


class OrderData:

    bSave = bool()
    eOrderType = int()
    iData1 = int()
    iData2 = int()


class PBGameSetupData:

    iAdvancedStartPoints = int()
    iCityElimination = int()
    iClimate = int()
    iEra = int()
    iMaxTurns = int()
    iNumCustomMapOptions = int()
    iNumVictories = int()
    iSeaLevel = int()
    iSize = int()
    iSpeed = int()
    iTurnTime = int()

    @staticmethod
    def getCustomMapOption(iOption):
        return int()

    @staticmethod
    def getMPOptionAt(iOption):
        return bool()

    @staticmethod
    def getMapName():
        return str()

    @staticmethod
    def getOptionAt(iOption):
        return bool()

    @staticmethod
    def getVictory(iVictory):
        return bool()


class PBPlayerAdminData:

    bClaimed = bool()
    bHuman = bool()
    bTurnActive = bool()

    @staticmethod
    def getName():
        return str()

    @staticmethod
    def getPing():
        return str()

    @staticmethod
    def getScore():
        return str()


class PBPlayerSetupData:

    iCiv = int()
    iDifficulty = int()
    iLeader = int()
    iTeam = int()
    iWho = int()

    @staticmethod
    def getStatusText():
        return str()


class POINT:

    x = int()
    y = int()


class Response:
    pass


class TradeData:

    ItemType = int()
    bHidden = bool()
    bOffering = bool()
    iData = int()


class WidgetAnim:
    pass


class XYCoords:

    def __init__(self, iX, iY):
        pass

    iX = int()
    iY = int()


# class ColorTypes:
#     def __init__(self, eColor):
#         pass

class CyPitboss:
    # Extracted from PBWizard.py and PBAdmin.py
    @staticmethod
    def loadMod(sModname):
        pass

    @staticmethod
    def isCurrentMod():
        return bool()

    @staticmethod
    def getModName():
        return str()

    @staticmethod
    def getNumSizes():
        return int()

    @staticmethod
    def getSizeAt(iIndex):
        return str()

    @staticmethod
    def getNumClimates():
        return int()

    @staticmethod
    def getClimateAt(iIndex):
        return str()

    @staticmethod
    def getNumSeaLevels():
        return int()

    @staticmethod
    def getSeaLevelAt(iIndex):
        return str()

    @staticmethod
    def getNumEras():
        return int()

    @staticmethod
    def getEraAt(iIndex):
        return str()

    @staticmethod
    def getNumSpeeds():
        return int()

    @staticmethod
    def getSpeedAt(iIndex):
        return str()

    @staticmethod
    def getNumMods():
        return int()

    @staticmethod
    def getModAt(iIndex):
        return str()

    @staticmethod
    def getNumMapScripts():
        return int()

    @staticmethod
    def getMapNameAt(iIndex):
        return str()

    @staticmethod
    def getNumScenarios():
        return int()

    @staticmethod
    def getScenarioAt(iIndex):
        return str()

    @staticmethod
    def getNumCivs():
        return int()

    @staticmethod
    def getCivAt(iIndex):
        return str()

    @staticmethod
    def getNumHandicaps():
        return int()

    @staticmethod
    def getHandicapAt(iIndex):
        return str()

    @staticmethod
    def getNumOptions():
        return int()

    @staticmethod
    def getOptionDescAt(iIndex):
        return str()

    @staticmethod
    def getNumMPOptions():
        return int()

    @staticmethod
    def getMPOptionDescAt(iIndex):
        return str()

    @staticmethod
    def getNumVictories():
        return int()

    @staticmethod
    def getVictoryDescAt(iIndex):
        return str()

    @staticmethod
    def getSMTPLogin():
        return str()

    @staticmethod
    def getNumCustomMapOptions(sMapName):
        return int()

    @staticmethod
    def getNumCustomMapOptionValues(iOption, sMapName):
        return int()

    @staticmethod
    def getCustomMapOptionName(iOption, sMapName):
        return str()

    @staticmethod
    def getCustomMapOptionDescAt(iRow, iOption, sMapName):
        return int()

    @staticmethod
    def getNumLeaders(iCiv):
        return int()

    @staticmethod
    def getCivLeaderAt(iCiv, iLeader):
        return str()

    @staticmethod
    def getName(iPlayer):
        return str()

    @staticmethod
    def getEmail():
        return str()

    @staticmethod
    def getSMTPHost():
        return str()

    @staticmethod
    def setSMTPValues(sHost, sUser, sPassword, sEmail):
        pass

    @staticmethod
    def checkPatch():
        return bool()  # ?

    @staticmethod
    def downloadPatch(sPatchName, sPatchUrl):
        return bool()

    @staticmethod
    def installPatch(sPatchName):
        pass

    @staticmethod
    def login(sUser, sPassword):
        return bool()

    @staticmethod
    def load(sPath, sAdminPwd):
        return int()

    @staticmethod
    def reset():
        pass

    @staticmethod
    def logout():
        pass

    @staticmethod
    def setLoadFileName(sPath):
        pass

    @staticmethod
    def host(bPublic, bScenario):
        return bool()

    @staticmethod
    def setGamename(sGamename):
        pass

    @staticmethod
    def setGamePassword(sPassword):
        pass

    @staticmethod
    def loadScenarioInfo(iIndex):
        return bool()

    @staticmethod
    def isPendingInit():
        return bool()

    @staticmethod
    def getGameSetupData():
        return PBGameSetupData()

    @staticmethod
    def getPlayerSetupData(iPlayer):
        return PBPlayerSetupData()

    @staticmethod
    def getPlayerAdminData(iPlayer):
        return PBPlayerAdminData()

    @staticmethod
    def getGlobalLeaderIndex(iCiv, iLeader):
        return int()

    @staticmethod
    def gameParamChanged(sMap, iSize, iClimate, iEra,
                         iSpeed, iMaxTurns, bCityElimination,
                         iTurnTimer, sAdminPassword):
        pass

    @staticmethod
    def playerParamChanged(iSlot, iWho, iCiv, iTeam,
                           iDifficulty, iGlobalLeaderID):
        # iWho is slot status
        pass

    @staticmethod
    def gameOptionChanged(iVictoryID, iValue):
        pass

    @staticmethod
    def mpOptionChanged(iVictoryID, iValue):
        pass

    @staticmethod
    def customMapOptionChanged(iOptionID, iValue):
        pass

    @staticmethod
    def victoriesChanged(iVictoryID, iValue):
        pass

    @staticmethod
    def getTurnTimer():
        return bool()

    @staticmethod
    def turnTimerChanged(iChange):
        pass

    @staticmethod
    def getTurnTimeLeft():
        return int()

    @staticmethod
    def kick(iPlayer):
        pass

    @staticmethod
    def save(sPath):
        return bool()

    @staticmethod
    def quit():
        pass

    @staticmethod
    def consoleOut(sMsg):
        pass

    @staticmethod
    def sendChat(sMsg):
        pass

    @staticmethod
    def getGamename():
        return str()

    @staticmethod
    def getGamedate(bUnknownFlag):
        return str()

    @staticmethod
    def getGameturn():
        return int()

    @staticmethod
    def getVersion():
        return str()  # ?

    @staticmethod
    def getNoPlayersScenario():
        return bool()

    @staticmethod
    def getWho(iSlot):
        return int()  # iStatus (AI, Human, ...)

    @staticmethod
    def getCiv(iSlot):
        return int()  # iCiv

    @staticmethod
    def forceSpeed():
        return bool()

    @staticmethod
    def forceMaxTurns():
        return bool()

    @staticmethod
    def forceCityElimination():
        return bool()

    @staticmethod
    def forceOptions():
        return bool()

    @staticmethod
    def isOptionValid(iOption):
        return bool()

    @staticmethod
    def forceVictories():
        return bool()

    @staticmethod
    def forceDifficulty():
        return bool()

    @staticmethod
    def isPermanentVictory(iRow):
        return bool()

    @staticmethod
    def isPlayableCiv(iRow):
        return bool()

    @staticmethod
    def suggestPlayerSetup():
        pass

    @staticmethod
    def getCivLeaderIndex(iCiv, iLeader):
        return int()

    @staticmethod
    def resetAdvancedStartPoints():
        pass

    @staticmethod
    def getReady(iSlot):
        return bool()

    @staticmethod
    def getDone():
        return bool()

    @staticmethod
    def launch():
        pass

    @staticmethod
    def handleMessages():
        pass

    @staticmethod
    def cancelPatchDownload():
        pass


####################################################

# ("Python Extension Module - CyGameCoreUtilsPythonInterface\n"):


def cyIntRange(iNum, iLow, iHigh):
    return int()


def cyFloatRange(fNum, fLow, fHigh):
    return float()


def dxWrap(iDX):
    return int()


def dyWrap(iDY):
    return int()


def plotDistance(iX1, iY1, iX2, iY2):
    return int()


def stepDistance(iX1, iY1, iX2, iY2):
    return int()


def plotDirection(iX, iY, eDirection):
    return CyPlot()


def plotCardinalDirection(iX, iY, eCardDirection):
    return CyPlot()


def splotCardinalDirection(iX, iY, eCardDirection):
    return CyPlot()


def plotXY(iX, iY, iDX, iDY):
    return CyPlot()


def splotXY(iX, iY, iDX, iDY):
    return CyPlot()


def directionXY(iDX, iDY):
    pass


def directionXYFromPlot(pFromPlot, pToPlot):
    pass


def plotCity(iX, iY, iIndex):
    return CyPlot()


def plotCityXY(iDX, iDY):
    return int()


def plotCityXYFromCity(pCity, pPlot):
    return int()

# (Already in CvUtil)
# def getOppositeCardinalDirection(eDir):
#     return -1


def cardinalDirectionToDirection(eDir):
    return -1


def isCardinalDirection(eDirection):
    return bool()


def estimateDirection(iDX, iDY):
    return -1


def atWar(eTeamA, eTeamB):
    return bool()


def isPotentialEnemy(eOurTeam, eTheirTeam):
    return bool()


def getCity(cityInfo):
    return CyPlot()


def getUnit(unitInfo):
    return CyUnit()


def isPromotionValid(ePromotion, eUnit, bLeader):
    return bool()


def getPopulationAsset(iPopulation):
    return int()


def getLandPlotsAsset(iLandPlots):
    return int()


def getPopulationPower(iPopulation):
    return int()


def getPopulationScore(iPopulation):
    return int()


def getLandPlotsScore(iPopulation):
    return int()


def getTechScore(eTech):
    return int()


def getWonderScore(eWonderClass):
    return int()


def finalImprovementUpgrade(eImprovement, iCount):
    return int()


def getWorldSizeMaxConscript(eCivic):
    return int()


def isReligionTech(eTech):
    return int()


def isTechRequiredForUnit(eTech, eUnit):
    return bool()


def isTechRequiredForBuilding(eTech, eBuilding):
    return bool()


def isTechRequiredForProject(eTech, eProject):
    return bool()


def isWorldUnitClass(eUnitClass):
    return bool()


def isTeamUnitClass(eUnitClass):
    return bool()


def isNationalUnitClass(eUnitClass):
    return bool()


def isLimitedUnitClass(eUnitClass):
    return bool()


def isWorldWonderClass(eBuildingClass):
    return bool()


def isTeamWonderClass(eBuildingClass):
    return bool()


def isNationalWonderClass(eBuildingClass):
    return bool()


def isLimitedWonderClass(eBuildingClass):
    return bool()


def isWorldProject(eProject):
    return bool()


def isTeamProject(eProject):
    return bool()


def isLimitedProject(eProject):
    return bool()


def getCombatOdds(pAttacker, pDefender):
    return int()


def getEspionageModifier(iOurTeam, iTargetTeam):
    return int()


def shuffleList(num, rand, piShuffle):
    pass


def getClockText():
    return str()

# def NiTextOut(szText):
#    pass
#

def getWBSaveExtension():
    return str()
