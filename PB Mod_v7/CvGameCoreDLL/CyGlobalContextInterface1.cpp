//
// published python interface for CyGlobalContext
// Author - Mustafa Thamer
//

#include "CvGameCoreDLL.h"
#include "CyMap.h"
#include "CyPlayer.h"
#include "CyGame.h"
#include "CyGlobalContext.h"
#include "CvRandom.h"
//#include "CvStructs.h"
#include "CvInfos.h"
#include "CyTeam.h"


void CyGlobalContextPythonInterface1(python::class_<CyGlobalContext>& x)
{
	OutputDebugString("Python Extension Module - CyGlobalContextPythonInterface1\n");

	x
		.def("isDebugBuild", &CyGlobalContext::isDebugBuild, "bool () - returns true if running a debug build")
		.def("getGame", &CyGlobalContext::getCyGame, python::return_value_policy<python::reference_existing_object>(), "CyGame* () - CyGame()")
		.def("getMap", &CyGlobalContext::getCyMap, python::return_value_policy<python::reference_existing_object>(), "CyMap* () - CyMap()")
		.def("getPlayer", &CyGlobalContext::getCyPlayer, python::return_value_policy<python::reference_existing_object>(), "CyPlayer* (int idx) - iPlayer instance")
		.def("getActivePlayer", &CyGlobalContext::getCyActivePlayer, python::return_value_policy<python::reference_existing_object>(), "CyPlayer* () - active player instance")
		.def("getASyncRand", &CyGlobalContext::getCyASyncRand, python::return_value_policy<python::reference_existing_object>(), "CvRandom ()")
		.def("getTeam", &CyGlobalContext::getCyTeam, python::return_value_policy<python::reference_existing_object>(), "CyTeam* (int i) - iTeam instance")

		// infos
		.def("getNumEffectInfos", &CyGlobalContext::getNumEffectInfos, "int () - Number of effect infos")
		.def("getEffectInfo", &CyGlobalContext::getEffectInfo, python::return_value_policy<python::reference_existing_object>(), "CvEffectInfo* (int (EffectTypes) i) - CvInfo for EffectID")

		.def("getNumTerrainInfos", &CyGlobalContext::getNumTerrainInfos, "() - Total Terrain Infos XML\\Terrain\\CIV4TerrainInfos.xml")
		.def("getTerrainInfo", &CyGlobalContext::getTerrainInfo, python::return_value_policy<python::reference_existing_object>(), "CvTerrainInfo* (int (TerrainTypes) i) - CvInfo for TerrainID")

		.def("getBonusClassInfo", &CyGlobalContext::getBonusClassInfo, python::return_value_policy<python::reference_existing_object>(), "CvBonusClassInfo* (int (BonusClassTypes) i) - CvInfo for BonusID")

		.def("getNumBonusInfos", &CyGlobalContext::getNumBonusInfos, "() - Total Bonus Infos XML\\Terrain\\CIV4BonusInfos.xml")
		.def("getBonusInfo", &CyGlobalContext::getBonusInfo, python::return_value_policy<python::reference_existing_object>(), "CvBonusInfo* (int ((BonusTypes) - CvInfo for BonusID")

		.def("getNumFeatureInfos", &CyGlobalContext::getNumFeatureInfos, "() - Total Feature Infos XML\\Terrain\\CIV4FeatureInfos.xml")
		.def("getFeatureInfo", &CyGlobalContext::getFeatureInfo, python::return_value_policy<python::reference_existing_object>(), "CvFeatureInfo* (int i) - CvInfo for FeatureID")

		.def("getNumUpkeepInfos", &CyGlobalContext::getNumUpkeepInfos, "int () - Number of upkeep infos")
		.def("getUpkeepInfo", &CyGlobalContext::getUpkeepInfo, python::return_value_policy<python::reference_existing_object>(), "CvUpkeepInfo* (int i) - CvInfo for upkeep info")

		.def("getNumCultureLevelInfos", &CyGlobalContext::getNumCultureLevelInfos, "int () - Number of culture level infos")
		.def("getCultureLevelInfo", &CyGlobalContext::getCultureLevelInfo, python::return_value_policy<python::reference_existing_object>(), "CvCultureLevelInfo* (int i) - CvInfo for CultureLevelID")

		.def("getNumEraInfos", &CyGlobalContext::getNumEraInfos, "int () - Number of era infos")
		.def("getEraInfo", &CyGlobalContext::getEraInfo,"CvEraInfo* (int i)" 

		.def("getNumWorldInfos", &CyGlobalContext::getNumWorldInfos, "int () - Number of world infos")
		.def("getWorldInfo", &CyGlobalContext::getWorldInfo, python::return_value_policy<python::reference_existing_object>(), "CvWorldInfo* (int i) - (WorldTypeID)")

		.def("getNumClimateInfos", &CyGlobalContext::getNumClimateInfos, "int () - Number of climate infos")
		.def("getClimateInfo", &CyGlobalContext::getClimateInfo, python::return_value_policy<python::reference_existing_object>(), "CvClimateInfo* (int i) - (ClimateTypeID)")

		.def("getNumSeaLevelInfos", &CyGlobalContext::getNumSeaLevelInfos, "int () - Number of seal level infos")
		.def("getSeaLevelInfo", &CyGlobalContext::getSeaLevelInfo, python::return_value_policy<python::reference_existing_object>(), "CvSeaLevelInfo* (int i) - (SeaLevelTypeID)")

		.def("getNumPlayableCivilizationInfos", &CyGlobalContext::getNumPlayableCivilizationInfos, "() - Total # of Playable Civs")
		.def("getNumCivilizationInfos", &CyGlobalContext::getNumCivilizatonInfos, "() - Total Civilization Infos XML\\Civilizations\\CIV4CivilizationInfos.xml")
		.def("getCivilizationInfo", &CyGlobalContext::getCivilizationInfo, python::return_value_policy<python::reference_existing_object>(), "CvCivilizationInfo* (int i) - CvInfo for CivilizationID")

		.def("getNumLeaderHeadInfos", &CyGlobalContext::getNumLeaderHeadInfos, "() - Total LeaderHead Infos XML\\Civilizations\\CIV4LeaderHeadInfos.xml")
		.def("getLeaderHeadInfo", &CyGlobalContext::getLeaderHeadInfo, python::return_value_policy<python::reference_existing_object>(), "CvLeaderHeadInfo* (int i) - CvInfo for LeaderHeadID")

		.def("getNumTraitInfos", &CyGlobalContext::getNumTraitInfos, "() - Total Civilization Infos XML\\Civilizations\\CIV4TraitInfos.xml")
		.def("getTraitInfo", &CyGlobalContext::getTraitInfo, python::return_value_policy<python::reference_existing_object>(), "CvTraitInfo* (int i) - CvInfo for TraitID")

		.def("getNumUnitInfos", &CyGlobalContext::getNumUnitInfos, "() - Total Unit Infos XML\\Units\\CIV4UnitInfos.xml")
		.def("getUnitInfo", &CyGlobalContext::getUnitInfo, python::return_value_policy<python::reference_existing_object>(), "CvUnitInfo* (int i) - CvInfo for UnitID")

		.def("getNumSpecialUnitInfos", &CyGlobalContext::getNumSpecialUnitInfos, "() - Total SpecialUnit Infos XML\\Units\\CIV4SpecialUnitInfos.xml")
		.def("getSpecialUnitInfo", &CyGlobalContext::getSpecialUnitInfo, python::return_value_policy<python::reference_existing_object>(), "CvSpecialUnitInfo* (int i) - CvInfo for UnitID")

		.def("getYieldInfo", &CyGlobalContext::getYieldInfo, python::return_value_policy<python::reference_existing_object>(), "CvYieldInfo* (int i) - CvInfo for YieldID")

		.def("getCommerceInfo", &CyGlobalContext::getCommerceInfo, python::return_value_policy<python::reference_existing_object>(), "CvCommerceInfo* (int i) - CvInfo for CommerceID")

		.def("getNumRouteInfos", &CyGlobalContext::getNumRouteInfos, "() - Total Route Infos XML\\Misc\\CIV4RouteInfos.xml")
		.def("getRouteInfo", &CyGlobalContext::getRouteInfo, python::return_value_policy<python::reference_existing_object>(), "CvRouteInfo* (int i) - CvInfo for RouteID")

		.def("getNumImprovementInfos", &CyGlobalContext::getNumImprovementInfos, "() - Total Improvement Infos XML\\Terrain\\CIV4ImprovementInfos.xml")
		.def("getImprovementInfo", &CyGlobalContext::getImprovementInfo, python::return_value_policy<python::reference_existing_object>(), "CvImprovementInfo* (int i) - CvInfo for ImprovementID")

		.def("getNumGoodyInfos", &CyGlobalContext::getNumGoodyInfos, "() - Total Goody Infos XML\\GameInfo\\CIV4GoodyInfos.xml")
		.def("getGoodyInfo", &CyGlobalContext::getGoodyInfo, python::return_value_policy<python::reference_existing_object>(), "CvGoodyInfo* (int i) - CvInfo for GoodyID")

		.def("getNumBuildInfos", &CyGlobalContext::getNumBuildInfos, "() - Total Build Infos XML\\Units\\CIV4BuildInfos.xml")
		.def("getBuildInfo", &CyGlobalContext::getBuildInfo, python::return_value_policy<python::reference_existing_object>(), "CvBuildInfo* (int i) - CvInfo for BuildID")

		.def("getNumHandicapInfos", &CyGlobalContext::getNumHandicapInfos, "() - Total Handicap Infos XML\\GameInfo\\CIV4HandicapInfos.xml")
		.def("getHandicapInfo", &CyGlobalContext::getHandicapInfo, python::return_value_policy<python::reference_existing_object>(), "CvHandicapInfo* (int i) - CvInfo for HandicapID")

		.def("getNumGameSpeedInfos", &CyGlobalContext::getNumGameSpeedInfos, "() - Total Game speed Infos XML\\GameInfo\\CIV4GameSpeedInfo.xml")
		.def("getGameSpeedInfo", &CyGlobalContext::getGameSpeedInfo, python::return_value_policy<python::reference_existing_object>(), "CvGameSpeedInfo* (int i) - CvInfo for GameSpeedID")

		.def("getNumTurnTimerInfos", &CyGlobalContext::getNumTurnTimerInfos, "() - Total Turn timer Infos XML\\GameInfo\\CIV4TurnTimerInfo.xml")
		.def("getTurnTimerInfo", &CyGlobalContext::getTurnTimerInfo, python::return_value_policy<python::reference_existing_object>(), "CvTurnTimerInfo* (int i) - CvInfo for TurnTimerID")

		.def("getNumBuildingClassInfos", &CyGlobalContext::getNumBuildingClassInfos, "() - Total Building Class Infos XML\\Buildings\\CIV4BuildingClassInfos.xml")
		.def("getBuildingClassInfo", &CyGlobalContext::getBuildingClassInfo, python::return_value_policy<python::reference_existing_object>(), "CvBuildingClassInfo* (int i) - CvInfo for BuildingClassID")

		.def("getNumBuildingInfos", &CyGlobalContext::getNumBuildingInfos, "() - Total Building Infos XML\\Buildings\\CIV4BuildingInfos.xml")
		.def("getBuildingInfo", &CyGlobalContext::getBuildingInfo, python::return_value_policy<python::reference_existing_object>(), "CvBuildingInfo* (int i) - CvInfo for BuildingID")

		.def("getNumUnitClassInfos", &CyGlobalContext::getNumUnitClassInfos, "() - Total Unit Class Infos XML\\Units\\CIV4UnitClassInfos.xml")
		.def("getUnitClassInfo", &CyGlobalContext::getUnitClassInfo, python::return_value_policy<python::reference_existing_object>(), "CvUnitClassInfo* (int i) - CvInfo for UnitClassID")

		.def("getNumUnitCombatInfos", &CyGlobalContext::getNumUnitCombatInfos, "() - Total Unit Combat Infos XML\\Units\\CIV4UnitCombatInfos.xml")
		.def("getUnitCombatInfo", &CyGlobalContext::getUnitCombatInfo, python::return_value_policy<python::reference_existing_object>(), "CvInfoBase* (int i) - CvInfo for UnitCombatID")

		.def("getDomainInfo", &CyGlobalContext::getDomainInfo, python::return_value_policy<python::reference_existing_object>(), "CvInfoBase* (int i) - CvInfo for DomainID")

		.def("getNumActionInfos", &CyGlobalContext::getNumActionInfos, "() - Total Action Infos XML\\Units\\CIV4ActionInfos.xml")
		.def("getActionInfo", &CyGlobalContext::getActionInfo, python::return_value_policy<python::reference_existing_object>(), "CvActionInfo* (int i) - CvInfo for ActionID")
	;
}
