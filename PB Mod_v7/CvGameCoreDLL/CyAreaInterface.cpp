#include "CvGameCoreDLL.h"
#include "CyArea.h"
#include "CyCity.h"
//
// published python interface for CyArea
//

void CyAreaPythonInterface()
{
	OutputDebugString("Python Extension Module - CyAreaPythonInterface\n");

	python::class_<CyArea>("CyArea")
		.def("isNone", &CyArea::isNone, "bool () - Returns whether the pointer points to a real Area")
		
		.def("calculateTotalBestNatureYield", &CyArea::calculateTotalBestNatureYield, "int () - Returns the total tile yield from the area")
		.def("countCoastalLand", &CyArea::countCoastalLand, "int ()")
		.def("countNumUniqueBonusTypes", &CyArea::countNumUniqueBonusTypes, "int () - Returns the number of unique bonus types in this area")
		.def("countHasReligion", &CyArea::countHasReligion, "int (int (ReligionTypes) eReligion, int (PlayerTypes) eOwner)")
		.def("countHasCorporation", &CyArea::countHasCorporation, "int (int (CorporationTypes) eCorporation, int (PlayerTypes) eOwner)")
		.def("getID", &CyArea::getID, "int () - Return's the Areas ID")
		.def("getNumTiles", &CyArea::getNumTiles, "int () - Returns the number of tiles in this area")
		.def("isLake", &CyArea::isLake, "bool () - Returns whether the area is a fresh water lake")
		.def("getNumOwnedTiles", &CyArea::getNumOwnedTiles, "int () - Returns the number of owned tiles in this area")
		.def("getNumUnownedTiles", &CyArea::getNumUnownedTiles, "int () - Returns the number of unowned tiles in this area")
		.def("getNumRiverEdges", &CyArea::getNumRiverEdges, "int () - Returns the number of River Edges in this area")
		.def("getNumCities", &CyArea::getNumCities, "int () - Returns the total number of cities for all players in this area")
		.def("getNumUnits", &CyArea::getNumUnits, "int () - Returns the total number of units for all players in this area")
		.def("getTotalPopulation", &CyArea::getTotalPopulation, "int () - Returns the total population for all players in this area")
		.def("getNumStartingPlots", &CyArea::getNumStartingPlots, "int () - total number of players that are starting on this area")
		.def("isWater", &CyArea::isWater, "bool () - Returns whether or not this area is water")

		.def("getUnitsPerPlayer", &CyArea::getUnitsPerPlayer, "int (int (PlayerTypes) eIndex) - Returns the number of units in this area for this player")
		.def("getAnimalsPerPlayer", &CyArea::getAnimalsPerPlayer, "int (int (PlayerTypes) eIndex) - Returns the number of animal units in this area for this player")
		.def("getCitiesPerPlayer", &CyArea::getCitiesPerPlayer, "int (int (PlayerTypes) eIndex) - Returns the number of cities in this area for this player")
		.def("getPopulationPerPlayer", &CyArea::getPopulationPerPlayer, "int (int (PlayerTypes) eIndex) - Returns the total population of this area for this player")
		.def("getBuildingGoodHealth", &CyArea::getBuildingGoodHealth, "int (int (PlayerTypes) eIndex) - Returns ?")
		.def("getBuildingBadHealth", &CyArea::getBuildingBadHealth, "int (int (PlayerTypes) eIndex) - Returns ?")
		.def("getBuildingHappiness", &CyArea::getBuildingHappiness, "int (int (PlayerTypes) eIndex) - Returns ?")
		.def("getFreeSpecialist", &CyArea::getFreeSpecialist, "int (int (PlayerTypes) eIndex) - Returns ?")
		.def("getPower", &CyArea::getPower, "int (int (PlayerTypes) eIndex) - Returns power of this area for this player")
		.def("getBestFoundValue", &CyArea::getBestFoundValue, "int (int (PlayerTypes) eIndex) - Returns the best found value for a plot in this area")

		.def("getNumRevealedTiles", &CyArea::getNumRevealedTiles, "int (int (TeamTypes) eIndex) - Returns the number of revealed tiles for this team")
		.def("getNumUnrevealedTiles", &CyArea::getNumUnrevealedTiles, "int (int (TeamTypes) eIndex) - Returns the number of unrevealed tiles for this team")

		.def("isCleanPower", &CyArea::isCleanPower, "bool (int (TeamTypes) eIndex)")
		.def("isBorderObstacle", &CyArea::isBorderObstacle, "bool (int (TeamTypes) eIndex)")

		.def("getAreaAIType", &CyArea::getAreaAIType, "int (AreaAITypes*/ (int (TeamTypes) eIndex) - Returns the AreaAIType for this team in this area")
		.def("getTargetCity", &CyArea::getTargetCity, python::return_value_policy<python::reference_existing_object>(), "CyCity* (int (PlayerTypes) eIndex) - Returns ?")
		.def("getYieldRateModifier", &CyArea::getYieldRateModifier, "int (int (PlayerTypes) eIndex1, int (YieldTypes) eIndex2) - Returns ?")
		.def("getNumTrainAIUnits", &CyArea::getNumTrainAIUnits, "int (int (PlayerTypes) eIndex1, int (UnitAITypes) eIndex2) - Returns ?")
		.def("getNumAIUnits", &CyArea::getNumAIUnits, "int (int (PlayerTypes) eIndex1, int (UnitAITypes) eIndex2) - Returns the number of units for this AI which have this AI type")

		.def("getNumBonuses", &CyArea::getNumBonuses, "int (int (BonusTypes) eBonus) - total # of BonusID")
		.def("getNumTotalBonuses", &CyArea::getNumTotalBonuses, "int () - total number of bonuses, of all types")
		.def("getNumImprovements", &CyArea::getNumImprovements, "int (int (ImprovementTypes) eImprovement) - total # of ImprovementID")
	;
}
