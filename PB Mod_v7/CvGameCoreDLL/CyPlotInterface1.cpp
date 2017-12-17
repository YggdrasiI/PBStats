#include "CvGameCoreDLL.h"
#include "CyPlot.h"
#include "CyCity.h"
#include "CyArea.h"
#include "CyUnit.h"
#include "CvPlot.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyPlot
//

void CyPlotPythonInterface1(python::class_<CyPlot>& x)
{
	OutputDebugString("Python Extension Module - CyPlotPythonInterface1\n");

	x
		.def("isNone", &CyPlot::isNone, "bool ()")
		.def("erase", &CyPlot::erase, "void ()")
		.def("getPoint", &CyPlot::getPoint, "NiPoint3 ()")
		.def("getTeam", &CyPlot::getTeam, "int ()")

		.def("nukeExplosion", &CyPlot::nukeExplosion, "void (int iRange, CyUnit* pNukeUnit)")

		.def("isConnectedTo", &CyPlot::isConnectedTo, "bool (CyCity* pCity) - returns whether this plot is connected to the provided city")
		.def("isConnectedToCapital", &CyPlot::isConnectedToCapital, "bool (int (PlayerTypes) ePlayer) - returns whether this plot is connected to the capital of the provided player")
		.def("getPlotGroupConnectedBonus", &CyPlot::getPlotGroupConnectedBonus, "int (int (PlayerTypes) ePlayer, int (BonusTypes) eBonus)")
		.def("isPlotGroupConnectedBonus", &CyPlot::isPlotGroupConnectedBonus, "bool (int (PlayerTypes) ePlayer, int (BonusTypes) eBonus)")
		.def("isAdjacentPlotGroupConnectedBonus", &CyPlot::isAdjacentPlotGroupConnectedBonus, "bool (int (PlayerTypes) ePlayer, int (BonusTypes) eBonus)")

		.def("updateVisibility", &CyPlot::updateVisibility, "void ()")
		.def("isAdjacentToArea", &CyPlot::isAdjacentToArea, "bool (CyArea* pArea)")
		.def("shareAdjacentArea", &CyPlot::shareAdjacentArea, "bool (CyPlot* pPlot)")
		.def("isAdjacentToLand", &CyPlot::isAdjacentToLand, "bool ()")
		.def("isCoastalLand", &CyPlot::isCoastalLand, "bool ()")
		
		.def("isWithinTeamCityRadius", &CyPlot::isWithinTeamCityRadius, "bool (int (TeamTypes) eTeam, int (PlayerTypes) eIgnorePlayer)")

		.def("isLake", &CyPlot::isLake, "bool ()")
		.def("isFreshWater", &CyPlot::isFreshWater, "bool ()")
		.def("isPotentialIrrigation", &CyPlot::isPotentialIrrigation, "bool ()")
		.def("canHavePotentialIrrigation", &CyPlot::canHavePotentialIrrigation, "bool ()")
		.def("isIrrigationAvailable", &CyPlot::isIrrigationAvailable, "bool (bool bIgnoreSelf)")

		.def("isRiverSide", &CyPlot::isRiverSide, "bool ()")
		.def("isRiver", &CyPlot::isRiver, "bool ()")
		.def("isRiverConnection", &CyPlot::isRiverConnection, "bool (int (DirectionTypes) eDirection)")

		.def("getNearestLandArea", &CyPlot::getNearestLandArea, "int ()")
		.def("getNearestLandPlot", &CyPlot::getNearestLandPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* ()")
		.def("seeFromLevel", &CyPlot::seeFromLevel, "int (int (TeamTypes) eTeam)")
		.def("seeThroughLevel", &CyPlot::seeThroughLevel, "int ()")
		.def("canHaveBonus", &CyPlot::canHaveBonus, "bool (int (BonusTypes) eBonus, bool bIgnoreLatitude)")
		.def("canHaveImprovement", &CyPlot::canHaveImprovement, "bool (int ( ImprovementTypes ) eImprovement, int (TeamTypes) eTeam, bool bPotential)")
		.def("canBuild", &CyPlot::canBuild, "bool (int (BuildTypes) eBuild, int (PlayerTypes) ePlayer, bool bTestVisible)")
		.def("getBuildTime", &CyPlot::getBuildTime, "int (int ( BuildTypes ) eBuild)")
		.def("getBuildTurnsLeft", &CyPlot::getBuildTurnsLeft, "int (int (BuildTypes) eBuild, int iNowExtra, int iThenExtra)")
		.def("getFeatureProduction", &CyPlot::getFeatureProduction, "int (int (BuildTypes) eBuild, int (TeamTypes) eTeam, CyCity* ppCity)")

		.def("getBestDefender", &CyPlot::getBestDefender, python::return_value_policy<python::manage_new_object>(), "CyUnit* (int (PlayerTypes) eOwner, int (PlayerTypes) eAttackingPlayer, CyUnit* pAttacker, bool bTestAtWar, bool bTestPotentialEnemy, bool bTestCanMove)")
		.def("getSelectedUnit", &CyPlot::getSelectedUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* ()")
		.def("getUnitPower", &CyPlot::getUnitPower, "int (int ( PlayerTypes ) eOwner)")

		.def("defenseModifier", &CyPlot::defenseModifier, "int (int iDefendTeam, bool bIgnoreBuilding, bool bHelp)")
		.def("movementCost", &CyPlot::movementCost, "int (CyUnit* pUnit, CyPlot* pFromPlot)")

		.def("getExtraMovePathCost", &CyPlot::getExtraMovePathCost, "int ()")
		.def("changeExtraMovePathCost", &CyPlot::changeExtraMovePathCost, "void (int iChange)")

		.def("isAdjacentOwned", &CyPlot::isAdjacentOwned, "bool ()")
		.def("isAdjacentPlayer", &CyPlot::isAdjacentPlayer, "bool (int (PlayerTypes) ePlayer, bool bLandOnly)")
		.def("isAdjacentTeam", &CyPlot::isAdjacentTeam, "bool (int (TeamTypes) ePlayer, bool bLandOnly)")
		.def("isWithinCultureRange", &CyPlot::isWithinCultureRange, "bool (int (PlayerTypes) ePlayer)")
		.def("getNumCultureRangeCities", &CyPlot::getNumCultureRangeCities, "int (int (PlayerTypes) ePlayer)")
		.def("calculateCulturalOwner", &CyPlot::calculateCulturalOwner, "int (PlayerTypes*/ ()")
		.def("isOwned", &CyPlot::isOwned, "bool ()")
		.def("isBarbarian", &CyPlot::isBarbarian, "bool ()")
		.def("isRevealedBarbarian", &CyPlot::isRevealedBarbarian, "bool ()")
		.def("isVisible", &CyPlot::isVisible, "bool (int (TeamTypes) eTeam, bool bDebug)")
		.def("isActiveVisible", &CyPlot::isActiveVisible, "bool (bool bDebug)")
		.def("isVisibleToWatchingHuman", &CyPlot::isVisibleToWatchingHuman, "bool ()")
		.def("isAdjacentVisible", &CyPlot::isAdjacentVisible, "bool (int (TeamTypes) eTeam, bool bDebug)")
		.def("isAdjacentNonvisible", &CyPlot::isAdjacentNonvisible, "bool (int (TeamTypes) eTeam)")
		.def("isAdjacentNonrevealed", &CyPlot::isAdjacentNonrevealed, "bool (int (TeamTypes) eTeam)")
		.def("isAdjacentRevealed", &CyPlot::isAdjacentRevealed, "bool (int (TeamTypes) eTeam)")

		.def("removeGoody", &CyPlot::removeGoody, "void ()")
		.def("isGoody", &CyPlot::isGoody, "bool ()")
		.def("isRevealedGoody", &CyPlot::isRevealedGoody, "bool (int (TeamTypes) eTeam)")

		.def("isCity", &CyPlot::isCity, "bool ()")
		.def("isFriendlyCity", &CyPlot::isFriendlyCity, "bool (CyUnit* pUnit, bool bCheckImprovement)")
		.def("isEnemyCity", &CyPlot::isEnemyCity, "bool (CyUnit* pUnit)")
		.def("isOccupation", &CyPlot::isOccupation, "bool ()")
		.def("isBeingWorked", &CyPlot::isBeingWorked, "bool ()")

		.def("isUnit", &CyPlot::isUnit, "bool ()")
		.def("isInvestigate", &CyPlot::isInvestigate, "bool (int (TeamTypes) eTeam)")
		.def("isVisibleEnemyDefender", &CyPlot::isVisibleEnemyDefender, "bool (CyUnit* pUnit)")
		.def("getNumDefenders", &CyPlot::getNumDefenders, "int (int (PlayerTypes) ePlayer)")
		.def("getNumVisibleEnemyDefenders", &CyPlot::getNumVisibleEnemyDefenders, "int (CyUnit* pUnit)")
		.def("getNumVisiblePotentialEnemyDefenders", &CyPlot::getNumVisiblePotentialEnemyDefenders, "int (CyUnit* pUnit)")
		.def("isVisibleEnemyUnit", &CyPlot::isVisibleEnemyUnit, "bool (int (PlayerTypes) ePlayer)")
		.def("isVisibleOtherUnit", &CyPlot::isVisibleOtherUnit, "bool (int (PlayerTypes) ePlayer)")
		.def("isFighting", &CyPlot::isFighting, "bool ()")

		.def("canHaveFeature", &CyPlot::canHaveFeature, "bool (int (FeatureTypes) eFeature)")
		.def("isRoute", &CyPlot::isRoute, "bool ()")
		.def("isNetworkTerrain", &CyPlot::isNetworkTerrain, "bool (int (TeamTypes) eTeam)")
		.def("isBonusNetwork", &CyPlot::isBonusNetwork, "bool (int (TeamTypes) eTeam)")

		.def("isTradeNetworkImpassable", &CyPlot::isTradeNetworkImpassable, "bool (int (TeamTypes) eTeam)")
		.def("isTradeNetwork", &CyPlot::isTradeNetwork, "bool (int (TeamTypes) eTeam)")
		.def("isTradeNetworkConnected", &CyPlot::isTradeNetworkConnected, "bool (CyPlot* pPlot, int (TeamTypes) eTeam)")
		.def("isValidDomainForLocation", &CyPlot::isValidDomainForLocation, "bool (CyUnit* pUnit)")
		.def("isValidDomainForAction", &CyPlot::isValidDomainForAction, "bool (CyUnit* pUnit)")
		.def("isImpassable", &CyPlot::isImpassable, "bool ()")

		.def("getX", &CyPlot::getX, "int ()")
		.def("getY", &CyPlot::getY, "int ()")
		.def("at", &CyPlot::at, "bool (int iX, int iY)")
		.def("getLatitude", &CyPlot::getLatitude, "int ()")
		.def("area", &CyPlot::area, python::return_value_policy<python::manage_new_object>(), "CyArea* ()")
		.def("waterArea", &CyPlot::waterArea, python::return_value_policy<python::manage_new_object>(), "CyArea* ()")
		.def("getArea", &CyPlot::getArea, "int ()")
		.def("getFeatureVariety", &CyPlot::getFeatureVariety, "int ()")

		.def("getOwnershipDuration", &CyPlot::getOwnershipDuration, "int ()")
		.def("isOwnershipScore", &CyPlot::isOwnershipScore, "bool ()")
		.def("setOwnershipDuration", &CyPlot::setOwnershipDuration, "void (int iNewValue)")
		.def("changeOwnershipDuration", &CyPlot::changeOwnershipDuration, "void (int iChange)")

		.def("getImprovementDuration", &CyPlot::getImprovementDuration, "int ()")
		.def("setImprovementDuration", &CyPlot::setImprovementDuration, "void (int iNewValue)")
		.def("changeImprovementDuration", &CyPlot::changeImprovementDuration, "void (int iChange)")

		.def("getUpgradeProgress", &CyPlot::getUpgradeProgress, "int ()")
		.def("getUpgradeTimeLeft", &CyPlot::getUpgradeTimeLeft, "int (int (ImprovementTypes) eImprovement, int (PlayerTypes) ePlayer)")

		.def("setUpgradeProgress", &CyPlot::setUpgradeProgress, "void (int iNewValue)")
		.def("changeUpgradeProgress", &CyPlot::changeUpgradeProgress, "void (int iChange)")

		.def("getForceUnownedTimer", &CyPlot::getForceUnownedTimer, "int ()")
		.def("isForceUnowned", &CyPlot::isForceUnowned, "bool ()")
		.def("setForceUnownedTimer", &CyPlot::setForceUnownedTimer, "void (int iNewValue)")
		.def("changeForceUnownedTimer", &CyPlot::changeForceUnownedTimer, "void (int iChange)")

		.def("getCityRadiusCount", &CyPlot::getCityRadiusCount, "int ()")
		.def("isCityRadius", &CyPlot::isCityRadius, "int ()")

		.def("isStartingPlot", &CyPlot::isStartingPlot, "bool ()")
		.def("setStartingPlot", &CyPlot::setStartingPlot, "void (bool bNewValue)")
		.def("isNOfRiver", &CyPlot::isNOfRiver, "bool ()")
		.def("setNOfRiver", &CyPlot::setNOfRiver, "void (bool bNewValue, CardinalDirectionTypes eRiverDir)")
		.def("isWOfRiver", &CyPlot::isWOfRiver, "bool ()")
		.def("setWOfRiver", &CyPlot::setWOfRiver, "void (bool bNewValue, CardinalDirectionTypes eRiverDir)")
		.def("getRiverWEDirection", &CyPlot::getRiverWEDirection, "CardinalDirectionTypes ()")
		.def("getRiverNSDirection", &CyPlot::getRiverNSDirection, "CardinalDirectionTypes ()")
		.def("isIrrigated", &CyPlot::isIrrigated, "bool ()")

		.def("isPotentialCityWork", &CyPlot::isPotentialCityWork, "bool ()")
		.def("isPotentialCityWorkForArea", &CyPlot::isPotentialCityWorkForArea, "bool (CyArea* pArea)")

		.def("isFlagDirty", &CyPlot::isFlagDirty, "bool ()")
		.def("setFlagDirty", &CyPlot::setFlagDirty, "void (bool bNewValue)")

		.def("getOwner", &CyPlot::getOwner, "int ()")
		.def("setOwner", &CyPlot::setOwner, "void (int (PlayerTypes) eNewValue)")
		.def("setOwnerNoUnitCheck", &CyPlot::setOwnerNoUnitCheck, "void (int (PlayerTypes) eNewValue)")
		.def("getPlotType", &CyPlot::getPlotType, "PlotTypes ()")
		.def("isWater", &CyPlot::isWater, "bool ()")
		.def("isFlatlands", &CyPlot::isFlatlands, "bool ()")
		.def("isHills", &CyPlot::isHills, "bool ()")
		.def("isPeak", &CyPlot::isPeak, "bool ()")
		.def("setPlotType", &CyPlot::setPlotType, "void (PlotTypes eNewValue, bool bRecalculate, bool bRebuildGraphics)")
		.def("getTerrainType", &CyPlot::getTerrainType, "int (TerrainTypes*/ ()")
		.def("setTerrainType", &CyPlot::setTerrainType, "void (int (TerrainTypes) eNewValue, bool bRecalculate, bool bRebuildGraphics)")
		.def("getFeatureType", &CyPlot::getFeatureType, "int (FeatureTypes*/ ()")
		.def("setFeatureType", &CyPlot::setFeatureType, "void (int (FeatureTypes) eNewValue, int iVariety)")
		.def("setFeatureDummyVisibility", &CyPlot::setFeatureDummyVisibility, "void (string dummyTag, bool show)")
		.def("addFeatureDummyModel", &CyPlot::addFeatureDummyModel, "void (string dummyTag, string modelTag)")
		.def("setFeatureDummyTexture", &CyPlot::setFeatureDummyTexture, "void (string dummyTag, string textureTag)")
		.def("pickFeatureDummyTag", &CyPlot::pickFeatureDummyTag, "string (int mouseX, int mouseY)")
		.def("resetFeatureModel", &CyPlot::resetFeatureModel, "void ()")
		.def("getBonusType", &CyPlot::getBonusType, "int ( BonusTypes */ (int (TeamTypes) eTeam)")
		.def("getNonObsoleteBonusType", &CyPlot::getNonObsoleteBonusType, "int ( BonusTypes */ (int (TeamTypes) eTeam)")
		.def("setBonusType", &CyPlot::setBonusType, "void (int ( BonusTypes ) eNewValue)")
		.def("getImprovementType", &CyPlot::getImprovementType, "int ( ImprovementTypes */ ()")
		.def("setImprovementType", &CyPlot::setImprovementType, "void (int ( ImprovementTypes ) eNewValue)")
		.def("getRouteType", &CyPlot::getRouteType, "int ( RouteTypes */ ()")
		.def("setRouteType", &CyPlot::setRouteType, "void (int (RouteTypes) eNewValue)")

		.def("getPlotCity", &CyPlot::getPlotCity, python::return_value_policy<python::manage_new_object>(), "CyCity* ()")
		.def("getWorkingCity", &CyPlot::getWorkingCity, python::return_value_policy<python::manage_new_object>(), "CyCity* ()")
		.def("getWorkingCityOverride", &CyPlot::getWorkingCityOverride, python::return_value_policy<python::manage_new_object>(), "CyCity* ()")
		.def("getRiverID", &CyPlot::getRiverID, "int ()")
		.def("setRiverID", &CyPlot::setRiverID, "void (int iNewValue)")
		.def("getMinOriginalStartDist", &CyPlot::getMinOriginalStartDist, "int ()")
		.def("getReconCount", &CyPlot::getReconCount, "int ()")
		.def("getRiverCrossingCount", &CyPlot::getRiverCrossingCount, "int ()")
		.def("getYield", &CyPlot::getYield, "int (YieldTypes eIndex)")
		.def("calculateNatureYield", &CyPlot::calculateNatureYield, "int (YieldTypes eIndex, TeamTypes eTeam, bool bIgnoreFeature)")
		.def("calculateBestNatureYield", &CyPlot::calculateBestNatureYield, "int (YieldTypes eIndex, TeamTypes eTeam)")
		.def("calculateTotalBestNatureYield", &CyPlot::calculateTotalBestNatureYield, "int (TeamTypes eTeam)")
		.def("calculateImprovementYieldChange", &CyPlot::calculateImprovementYieldChange, "int (int (ImprovementTypes) eImprovement, YieldTypes eYield, int (PlayerTypes) ePlayer, bool bOptimal)")
		.def("calculateYield", &CyPlot::calculateYield, "int (YieldTypes eIndex, bool bDisplay)")
		.def("hasYield", &CyPlot::hasYield, "bool ()")

		.def("getCulture", &CyPlot::getCulture, "int (int (PlayerTypes) eIndex)")
		.def("countTotalCulture", &CyPlot::countTotalCulture, "int ()")
		.def("findHighestCultureTeam", &CyPlot::findHighestCultureTeam, "int (TeamTypes*/ ()")

		.def("calculateCulturePercent", &CyPlot::calculateCulturePercent, "int (int (PlayerTypes) eIndex)")
		.def("calculateTeamCulturePercent", &CyPlot::calculateTeamCulturePercent, "int (int (TeamTypes) eIndex)")
		.def("setCulture", &CyPlot::setCulture, "void (int (PlayerTypes) eIndex, int iChange, bool bUpdate)")
		.def("changeCulture", &CyPlot::changeCulture, "void (int (PlayerTypes) eIndex, int iChange, bool bUpdate)")

		.def("countNumAirUnits", &CyPlot::countNumAirUnits, "int (int (TeamTypes) eTeam)")

		.def("getFoundValue", &CyPlot::getFoundValue, "int (int (PlayerTypes) eIndex)")
		.def("isBestAdjacentFound", &CyPlot::isBestAdjacentFound, "bool (int (PlayerTypes) eIndex)")

		.def("getPlayerCityRadiusCount", &CyPlot::getPlayerCityRadiusCount, "int (int (PlayerTypes) eIndex)")
		.def("isPlayerCityRadius", &CyPlot::isPlayerCityRadius, "bool (int (PlayerTypes) eIndex)")

		.def("getVisibilityCount", &CyPlot::getVisibilityCount, "int (int (TeamTypes) eTeam)")
		.def("changeVisibilityCount", &CyPlot::changeVisibilityCount, "void (int (TeamTypes) eTeam, int iChange, int (InvisibleTypes) eSeeInvisible)")

		.def("getStolenVisibilityCount", &CyPlot::getStolenVisibilityCount, "int (int (TeamTypes) eTeam)")

		.def("getRevealedOwner", &CyPlot::getRevealedOwner, "int (PlayerTypes*/ (int (TeamTypes) eTeam, bool bDebug)")
		.def("getRevealedTeam", &CyPlot::getRevealedTeam, "int (TeamTypes*/ (int (TeamTypes) eTeam, bool bDebug)")
		
		.def("isRiverCrossing", &CyPlot::isRiverCrossing, "bool (DirectionTypes eIndex)")

		.def("isRevealed", &CyPlot::isRevealed, "bool ()")
		.def("setRevealed", &CyPlot::setRevealed, "void (int (TeamTypes) eTeam, bool bNewValue, bool bTerrainOnly, int (TeamTypes) eFromTeam)")
		.def("getRevealedImprovementType", &CyPlot::getRevealedImprovementType, "int ( ImprovementTypes */ (int (TeamTypes) eTeam, bool bDebug)")
		.def("getRevealedRouteType", &CyPlot::getRevealedRouteType, "int ( RouteTypes */ (int (TeamTypes) eTeam, bool bDebug)")
		.def("getBuildProgress", &CyPlot::getBuildProgress, "int (int (BuildTypes) eBuild)")
		.def("changeBuildProgress", &CyPlot::changeBuildProgress, "bool (int (BuildTypes) eBuild, int iChange, int (TeamTypes) eTeam)")

		.def("getCultureRangeCities", &CyPlot::getCultureRangeCities, "int (int (PlayerTypes) eOwnerIndex, int iRangeIndex)")
		.def("isCultureRangeCity", &CyPlot::isCultureRangeCity, "bool (int (PlayerTypes) eOwnerIndex, int iRangeIndex)")

		.def("getInvisibleVisibilityCount", &CyPlot::getInvisibleVisibilityCount, "int (int (TeamTypes) eTeam, int (InvisibleTypes) eInvisible)")
		.def("isInvisibleVisible", &CyPlot::isInvisibleVisible, "bool (int (TeamTypes) eTeam, int (InvisibleTypes) eInvisible)")
		.def("changeInvisibleVisibilityCount", &CyPlot::changeInvisibleVisibilityCount, "void (int (TeamTypes) eTeam, int (InvisibleTypes) eInvisible, int iChange)")

		.def("getNumUnits", &CyPlot::getNumUnits, "int ()")
		.def("getUnit", &CyPlot::getUnit, python::return_value_policy<python::manage_new_object>(), "int (int ( PlayerTypes ) eOwner)")

		.def("getScriptData", &CyPlot::getScriptData, "string getScriptData() - Get stored custom data")
		.def("setScriptData", &CyPlot::setScriptData, "void (string szNewValue) - Set stored custom data")
	;
}
