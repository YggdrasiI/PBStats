#include "CvGameCoreDLL.h"
#include "CyMap.h"
#include "CyArea.h"
#include "CyCity.h"
#include "CySelectionGroup.h"
#include "CyUnit.h"
#include "CyPlot.h"
//#include "CvStructs.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>

//
// published python interface for CyMap
//

void CyMapPythonInterface()
{
	OutputDebugString("Python Extension Module - CyMapPythonInterface\n");

	python::class_<CyMap>("CyMap")
		.def("isNone", &CyMap::isNone, "bool () - valid CyMap() interface")

		.def("erasePlots", &CyMap::erasePlots, "void () - erases the plots")
		.def("setRevealedPlots", &CyMap::setRevealedPlots, "void (int (TeamTypes) eTeam, bool bNewValue, bool bTerrainOnly) - reveals the plots to eTeam")
		.def("setAllPlotTypes", &CyMap::setAllPlotTypes, "void (int (PlotTypes) ePlotType) - sets all plots to ePlotType")

		.def("updateVisibility", &CyMap::updateVisibility, "void () - updates the plots visibility")
		.def("syncRandPlot", &CyMap::syncRandPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int iFlags, int iArea, int iMinUnitDistance, int iTimeout) - random plot based on conditions")
		.def("findCity", &CyMap::findCity, python::return_value_policy<python::manage_new_object>(), "CyCity* (int iX, int iY, int (PlayerTypes) eOwner, int (TeamTypes) eTeam, bool bSameArea, bool bCoastalOnly, int (TeamTypes) eTeamAtWarWith, int (DirectionTypes) eDirection, CyCity* pSkipCity) - finds city")
		.def("findSelectionGroup", &CyMap::findSelectionGroup, python::return_value_policy<python::manage_new_object>(), "CySelectionGroup* (int iX, int iY, int (PlayerTypes) eOwner, bool bReadyToSelect, bool bWorkers)")

		.def("findBiggestArea", &CyMap::findBiggestArea, python::return_value_policy<python::manage_new_object>(), "CyArea* (bool bWater)")

		.def("getMapFractalFlags", &CyMap::getMapFractalFlags, "int ()")
		.def("findWater", &CyMap::findWater, "bool (CyPlot* pPlot, int iRange, bool bFreshWater)")
		.def("isPlot", &CyMap::isPlot, "bool (int iX, int iY) - is (iX, iY) a valid plot?")
		.def("numPlots", &CyMap::numPlots, "int () - total plots in the map")
		.def("plotNum", &CyMap::plotNum, "int (int iX, int iY) - the index for a given plot")
		.def("plotX", &CyMap::plotX, "int (int iIndex) - given the index of a plot, returns its X coordinate")
		.def("plotY", &CyMap::plotY, "int (int iIndex) - given the index of a plot, returns its Y coordinate")
		.def("getGridWidth", &CyMap::getGridWidth, "int () - the width of the map, in plots")
		.def("getGridHeight", &CyMap::getGridHeight, "int () - the height of the map, in plots")

		.def("getLandPlots", &CyMap::getLandPlots, "int () - total land plots")
		.def("getOwnedPlots", &CyMap::getOwnedPlots, "int () - total owned plots")

		.def("getTopLatitude", &CyMap::getTopLatitude, "int () - top latitude (usually 90)")
		.def("getBottomLatitude", &CyMap::getBottomLatitude, "int () - bottom latitude (usually -90)")

		.def("getNextRiverID", &CyMap::getNextRiverID, "int ()")
		.def("incrementNextRiverID", &CyMap::incrementNextRiverID, "void ()")

		.def("isWrapX", &CyMap::isWrapX, "bool () - whether the map wraps in the X axis")
		.def("isWrapY", &CyMap::isWrapY, "bool () - whether the map wraps in the Y axis")
		.def("getMapScriptName", &CyMap::getMapScriptName, "wstring getMapScriptName() () - name of the map script")
		.def("getWorldSize", &CyMap::getWorldSize, "WorldSizeTypes () - size of the world")
		.def("getClimate", &CyMap::getClimate, "ClimateTypes () - climate of the world")
		.def("getSeaLevel", &CyMap::getSeaLevel, "SeaLevelTypes () - sealevel of the world")

		.def("getNumCustomMapOptions", &CyMap::getNumCustomMapOptions, "int () - number of custom map settings")
		.def("getCustomMapOption", &CyMap::getCustomMapOption, "CustomMapOptionTypes (int iOption) - user defined map setting at this option id")

		.def("getNumBonuses", &CyMap::getNumBonuses, "int (int ( BonusTypes ) eIndex) - total bonuses")
		.def("getNumBonusesOnLand", &CyMap::getNumBonusesOnLand, "int (int ( BonusTypes ) eIndex) - total bonuses on land plots")

		.def("plotByIndex", &CyMap::plotByIndex, python::return_value_policy<python::manage_new_object>(), "CyPlot* (int iIndex) - get a plot by its Index")
		.def("sPlotByIndex", &CyMap::sPlotByIndex, python::return_value_policy<python::reference_existing_object>(), "CyPlot* (int iIndex) - static - get plot by iIndex")
		.def("plot", &CyMap::plot, python::return_value_policy<python::manage_new_object>(), "int (int iX, int iY) - get CyPlot at (iX,iY)")
		.def("sPlot", &CyMap::sPlot, python::return_value_policy<python::reference_existing_object>(), "CyPlot* (int iIndex) - static - get CyPlot at (iX,iY)")
		.def("pointToPlot", &CyMap::pointToPlot,"CyPlot* (float fX, float fY)" 
		.def("getIndexAfterLastArea", &CyMap::getIndexAfterLastArea, "int () - index for handling NULL areas")
		.def("getNumAreas", &CyMap::getNumAreas, "int () - total areas")
		.def("getNumLandAreas", &CyMap::getNumLandAreas, "int () - total land areas")
		.def("getArea", &CyMap::getArea, python::return_value_policy<python::manage_new_object>(), "CyArea* (int iID) - get CyArea at iID")
		.def("recalculateAreas", &CyMap::recalculateAreas, "void () - Recalculates the areaID for each plot. Should be preceded by CyMap.setPlotTypes(...)")
		.def("resetPathDistance", &CyMap::resetPathDistance, "void ()")

		.def("calculatePathDistance", &CyMap::calculatePathDistance, "int (CyPlot* pSource, CyPlot* pDest)")
		.def("rebuild", &CyMap::rebuild, "void (int iGridW, int iGridH, int iTopLatitude, int iBottomLatitude, bool bWrapX, bool bWrapY, WorldSizeTypes eWorldSize, ClimateTypes eClimate, SeaLevelTypes eSeaLevel, int iNumCustomMapOptions, CustomMapOptionTypes * aeCustomMapOptions)")
		.def("regenerateGameElements", &CyMap::regenerateGameElements, "void ()")
		.def("updateFog", &CyMap::updateFog, "void ()")
		.def("updateMinimapColor", &CyMap::updateMinimapColor, "void ()")
		.def("updateMinOriginalStartDist", &CyMap::updateMinOriginalStartDist, "void (CyArea* pArea)")
		;
}
