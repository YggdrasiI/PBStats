#include "CvGameCoreDLL.h"
#include "CyArtFileMgr.h"
#include "CvInfos.h"

//
// published python interface for CyArea
//

void CyArtFileMgrPythonInterface()
{
	OutputDebugString("Python Extension Module - CyArtFileMgrPythonInterface\n");

	python::class_<CyArtFileMgr>("CyArtFileMgr")
		.def("isNone", &CyArtFileMgr::isNone, "bool () - Checks to see if pointer points to a real object")

		.def("Reset", &CyArtFileMgr::Reset, "void ()")
		.def("buildArtFileInfoMaps", &CyArtFileMgr::buildArtFileInfoMaps, "void ()")

		.def("getInterfaceArtInfo", &CyArtFileMgr::getInterfaceArtInfo,  python::return_value_policy<python::reference_existing_object>(), "CvArtInfoInterface* ( const char * szArtDefineTag )")
		.def("getMovieArtInfo", &CyArtFileMgr::getMovieArtInfo,  python::return_value_policy<python::reference_existing_object>(), "CvArtInfoMovie* ( const char * szArtDefineTag )")
		.def("getMiscArtInfo", &CyArtFileMgr::getMiscArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoMisc* ( const char * szArtDefineTag )")
		.def("getUnitArtInfo", &CyArtFileMgr::getUnitArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoUnit* ( const char * szArtDefineTag )")
		.def("getBuildingArtInfo", &CyArtFileMgr::getBuildingArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoBuilding* ( const char * szArtDefineTag )")
		.def("getCivilizationArtInfo", &CyArtFileMgr::getCivilizationArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoCivilization* ( const char * szArtDefineTag )")
		.def("getLeaderheadArtInfo", &CyArtFileMgr::getLeaderheadArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoLeaderhead* ( const char * szArtDefineTag )")
		.def("getBonusArtInfo", &CyArtFileMgr::getBonusArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoBonus* ( const char * szArtDefineTag )")
		.def("getImprovementArtInfo", &CyArtFileMgr::getImprovementArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoImprovement* ( const char * szArtDefineTag )")
		.def("getTerrainArtInfo", &CyArtFileMgr::getTerrainArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoTerrain* ( const char * szArtDefineTag )")
		.def("getFeatureArtInfo", &CyArtFileMgr::getFeatureArtInfo, python::return_value_policy<python::reference_existing_object>(), "CvArtInfoFeature* ( const char * szArtDefineTag )")
	;
}

