import ROOT
from xAH_config import xAH_config
import sys, os

import shlex
import argparse

parser = argparse.ArgumentParser(description='Test for extra options')
parser.add_argument('--doResolvedSys',       dest='doResolvedSys',   action="store_true", default=False)
parser.add_argument('--doBoostedSys',        dest='doBoostedSys',    action="store_true", default=False)
parser.add_argument('--doLepTopSys',         dest='doLepTopSys',     action="store_true", default=False)
o = parser.parse_args(shlex.split(args.extra_options))

sys.path.insert(0, os.environ['ROOTCOREBIN']+"/user_scripts/XhhCommon/")

#from XhhResolved_config import *
from resolved_config    import *
from XhhBoosted_config  import *
from XhhLepTop_config   import *

c = xAH_config()
#
# Basic Setup 
#
triggersList = ['HLT_j420.*',
                'HLT_j440.*',
                'HLT_j400.*',
                'HLT_j360.*',
                'HLT_j380.*',
                'HLT_j100',
                'HLT_j110',
                'HLT_j150',
                'HLT_j175',
                'HLT_j200',
                'HLT_j260',
                ]



triggers = ",".join(triggersList)
c.setalg("BasicEventSelection", { "m_name"                  : "basicEventSel",
                                  "m_debug"                 : False,
                                  "m_derivationName"        : "EXOT8Kernel",
                                  "m_applyGRLCut"           : False,
                                  "m_doPUreweighting"       : False, 
                                  "m_vertexContainerName"   : "PrimaryVertices",
                                  "m_PVNTrack"              : 2,
                                  "m_truthLevelOnly"        : False,
                                  "m_applyPrimaryVertexCut" : True,
                                  "m_derivationName"        : "EXOT8Kernel", 
                                  "m_applyEventCleaningCut" : True,
                                  "m_applyCoreFlagsCut"     : True,
                                  "m_triggerSelection"      : triggers, 
                                  "m_storeTrigDecisions"    : True,
                                  "m_useMetaData"           : True,
                                  "m_applyTriggerCut"       : False,
                                  "m_storePassL1"           : True,
                                  "m_storePassHLT"          : True,
                                  "m_storeTrigKeys"         : True,
                                  } )


doSystematics = False
if not doSystematics:
    systName = "Nominal"
    systVal  = 0
else:
    systName = "All"
    systVal  = 1



#
#  Jet Calibration
#
c.setalg("JetCalibrator", { "m_name"                  : "XhhBoosted_JetCalibrator",
                            "m_inContainerName"       : "AntiKt10LCTopoTrimmedPtFrac5SmallR20Jets",
                            "m_jetAlgo"               : "AntiKt10LCTopoTrimmedPtFrac5SmallR20",
                            "m_outputAlgo"            : "AntiKt10LCTopoTrimmedPtFrac5SmallR20_Calib_Algo_JES",
                            "m_outContainerName"      : "calibCaloJets_JES",
                            "m_debug"                 : False,
                            "m_verbose"               : False,
                            "m_sort"                  : True,
                            "m_saveAllCleanDecisions" : True,
                            "m_calibConfigFullSim"    : "JES_MC15recommendation_FatJet_June2015.config",
                            "m_calibConfigData"       : "JES_MC15recommendation_FatJet_June2015.config",
                            "m_doCleaning"            : False, #don't clean large R jets
                            "m_JESUncertConfig"       : "$ROOTCOREBIN/data/JetUncertainties/UJ_2015/ICHEP2016/HbbTagging_strong.config",
                            "m_JESUncertMCType"       : "MC15C",
                            "m_calibSequence"         : "EtaJES_JMS",
                            "m_setAFII"               : False,
                            "m_jetCleanCutLevel"      : "LooseBad",
                            "m_jetCleanUgly"          : True,
                            "m_cleanParent"           : True,
                            "m_applyFatJetPreSel"     : True,    # make sure fat-jet uncertainty is applied only in valid region
                            # Add me when large-R uncertainties become available.
                            "m_systName"              : systName,
                            "m_systVal"               : systVal,
                            })

#
# JER Smearing
#
c.setalg("FatJetJERTool", { "m_name"                  : "XhhBoosted_FatJetJERSmearing",
                            "m_inContainerName"       : "calibCaloJets_JES",
                            "m_outContainerName"      : "calibCaloJets",
                            "m_TruthJetContainerName" : "AntiKt10TruthTrimmedPtFrac5SmallR20Jets",
                            "m_jetAlgo"               : "AntiKt10LCTopoTrimmedPtFrac5SmallR20",
                            "m_inputAlgo"             : "AntiKt10LCTopoTrimmedPtFrac5SmallR20_Calib_Algo_JES",
                            "m_outputAlgo"            : "AntiKt10LCTopoTrimmedPtFrac5SmallR20_Calib_Algo",
                            "m_JERConfig"             : "$ROOTCOREBIN/data/XhhBoosted/JERConfig.root",
                            "m_runJERSmearing"        : doSystematics,
                            "m_sort"                  : True,
                            "m_userSeed"              : 0,
                            "m_systName"              : "Nominal",      # don't change this
                            "m_systVal"               : 0,
                            })

#
#  Jet Selection
#
c.setalg("JetSelector", { "m_name"                    : "XhhBoosted_selectCaloJets",
                          "m_inContainerName"         : "calibCaloJets",
                          "m_inputAlgo"               : "AntiKt10LCTopoTrimmedPtFrac5SmallR20_Calib_Algo",
                          "m_outContainerName"        : "selCaloJets",
                          "m_outputAlgo"              : "selCaloJets_Algo",
                          "m_decorateSelectedObjects" : False,  
                          "m_createSelectedContainer" : True,  
                          "m_cleanJets"               : True,
                          "m_pT_min"                  : 250e3,
                          #"m_pT_max"                  : 1500e3,
                          "m_eta_max"                 : 2.0,
                          #"m_mass_min"                : 50e3,  # 0.1,
                          "m_mass_min"                : 0.1, 
                          "m_useCutFlow"              : True,
                          "m_doJVF"                   : False
                          } )

c.setalg("JetSelector", { "m_name"                    : "XhhBoosted_selectTrackJets",
                          "m_inContainerName"         : "AntiKt2PV0TrackJets",
                          "m_outContainerName"        : "selTrackJets",
                          "m_decorateSelectedObjects" : False,  
                          "m_createSelectedContainer" : True,  
                          "m_cleanJets"               : True,
                          "m_pT_min"                  : 10e3,
                          "m_eta_max"                 : 2.5,
                          "m_useCutFlow"              : True,
                          "m_doJVF"                   : False
                          } )


c.setalg("BJetEfficiencyCorrector", { "m_name"                    : "XhhBoosted_postselectTrackJets",
                                      "m_inContainerName"         : "selTrackJets",
                                      "m_systName"                : ("" if systName == "Nominal" else systName),   # a bit special for b-tagging SF, since "Nominal" will NOT be converted to "" internally 
                                      "m_systVal"                 : systVal,
                                      "m_outputSystName"          : "FTSys",
                                      "m_operatingPt"             : "FixedCutBEff_77",
                                      "m_operatingPtCDI"          : "FixedCutBEff_77",
                                      "m_corrFileName"            : "$ROOTCOREBIN/data/xAODAnaHelpers/2016-20_7-13TeV-MC15-CDI-July12_v1.root",
                                      "m_jetAuthor"               : "AntiKt2PV0TrackJets",
                                      "m_taggerName"              : "MV2c10",
                                      "m_decor"                   : "BTag",
                                      "m_debug"                   : False,
                                      } )




#
#  ak4 Jet Calibration
#
c.setalg("JetCalibrator", { "m_name"                   : "AntiKt4TopoEM", 
                            "m_systName"               : "", 
                            "m_systVal"                : 1,
                            "m_inContainerName"        : "AntiKt4EMTopoJets",
                            "m_outContainerName"       : "AntiKt4EMTopoJets_Calib", 
                            "m_sort"                   : True,
                            "m_jetAlgo"                : "AntiKt4EMTopo",
                            "m_outputAlgo"             : "AntiKt4EMTopoJets_Calib_Algo",
                            "m_calibSequence"          : "JetArea_Residual_Origin_EtaJES_GSC",
                            "m_calibConfigFullSim"     : "JES_MC15Prerecommendation_April2015.config",
                            "m_calibConfigData"        : "JES_MC15cRecommendation_May2016.config",
                            "m_calibConfigAFII"        : "JES_MC15Prerecommendation_AFII_June2015.config",
                            "m_jetCleanCutLevel"       : "LooseBad",
                             "m_JESUncertConfig"        : "$ROOTCOREBIN/data/JetUncertainties/JES_2015/Prerec/PrerecJES2015_3NP_Scenario1_25ns.config",
                            "m_JESUncertConfig"        : "$ROOTCOREBIN/data/JetUncertainties/JES_2015/ICHEP2016/JES2015_SR_Scenario1.config",
                            "m_JESUncertMCType"        : "MC15",
                            "m_saveAllCleanDecisions"  : True,                         
                            "m_setAFII"                : False,
                            "m_JERUncertConfig"        : "JetResolution/Prerec2015_xCalib_2012JER_ReducedTo9NP_Plots_v2.root",
                            "m_JERApplyNominal"        : False,
                            "m_redoJVT"                : True,
                            "m_systName"               : systName,
                            "m_systVal"                : systVal,
                            } )
c.setalg("JetHistsAlgo", {"m_name":"jets_all/", "m_inContainerName":"AntiKt4EMTopoJets_Calib", 
                          "m_detailStr":"kinematic clean energy"} )

#
#  Jet Selection
#
c.setalg("JetSelector", { "m_name"                    :  "preSelJetsEMTopoJets",
                          "m_inContainerName"         :  "AntiKt4EMTopoJets_Calib",
                          "m_inputAlgo"               :  "AntiKt4EMTopoJets_Calib_Algo",
                          "m_outContainerName"        :  "AntiKt4EMTopoJets_Calib_preSel",
                          "m_outputAlgo"              :  "AntiKt4EMTopoJets_Calib_preSel_Algo",
                          "m_decorateSelectedObjects" :  False, 
                          "m_createSelectedContainer" :  True, 
                          "m_cleanJets"               :  False, 
                          "m_pT_min"                  :  250e3,
                          "m_eta_max"                 :  2.5,
                          "m_useCutFlow"              :  True,
                          "m_doJVT"                   :  True,
                          "m_jetScaleType"            :  "JetConstitScaleMomentum",
                          } )
c.setalg("JetHistsAlgo", {"m_name":"jets_preSel/", "m_inContainerName":"AntiKt4EMTopoJets_Calib_preSel"
                          , "m_detailStr":"kinematic clean energy"} )



#
#  Muon Calibration
#
c.setalg("MuonCalibrator", { "m_name"                : "Muons", 
                             "m_inContainerName"     : "Muons", 
                             "m_outContainerName"    : "Muons_Calib", 
                             "m_outputAlgoSystNames" : "MuonCalibrator_Syst",
                             #"m_release"             : "Recs2016_08_07",
                             "m_debug"               : False,
                             "m_forceDataCalib"      : True,
                             } )

c.setalg("MuonHistsAlgo", {"m_name":"Muons_Calib/",    "m_inContainerName":"Muons_Calib",  
                           "m_detailStr" : "kinematic energyLoss", } )

#
#  Muon Presel
#
c.setalg("MuonSelector", { "m_name"                    : "MuonPreSelector", 
                           "m_inContainerName"         : "Muons_Calib", 
                           "m_outContainerName"        : "Muons_PreSelected", 
                           "m_createSelectedContainer" : True,
                           "m_pT_min"                  : 10*1000,
                           "m_eta_max"                 : 2.5,
                           "m_muonQualityStr"          : "Medium",
                           "m_d0sig_max"               : 3,
                           "m_z0sintheta_max"          : 1.0,
                           "m_MinIsoWPCut"             : "Loose", 
                       } )

c.setalg("MuonHistsAlgo", {"m_name":"Muons_PreSelected/", "m_inContainerName":"Muons_PreSelected",  
                           "m_detailStr" : "kinematic quality energyLoss isolation", } )


#
#  MeT Calibration
#
c.setalg("METConstructor", {"m_name"                  : "METBuilding",
                            "m_referenceMETContainer" : "MET_Reference_AntiKt4EMTopo",
                            "m_mapName"               : "METAssoc_AntiKt4EMTopo",
                            "m_coreName"              : "MET_Core_AntiKt4EMTopo",
                            "m_outputContainer"       : "RefFinalEM",
                            "m_inputJets"             : "AntiKt4EMTopoJets_Calib",
                            "m_inputMuons"            : "Muons_PreSelected", 
                            "m_doMuonCuts"            : False,
                            "m_doMuonEloss"           : True,
                            "m_doIsolMuonEloss"       : True
                            } )
c.setalg("MetHistsAlgo", {"m_name":"Met_RefFinalEM/",    "m_inContainerName":"RefFinalEM",
                          "m_detailStr" : "kinematic", } )





#
# Ntuples
#
c.setalg("XhhTestBoostedNtuple", { "m_name"                       : "TestNtuples",
                                   "m_debug"                      : False,
                                   "m_trigDetailStr"              : "passTriggers",
                                   "m_inTruthParticleName"        : "TruthParticles",
                                   "m_inFatJetName"               : "selCaloJets",
                                   "m_inJetName"                  : "AntiKt4EMTopoJets_Calib_preSel", 
                                   "m_jetDetailStr"               : "kinematic clean trackPV flavorTag",
                                   "m_inTruthFatJetName"          : "AntiKt10TruthTrimmedPtFrac5SmallR20Jets",
                                   "m_fatJetDetailStr"            : "kinematic substructure constituent bosonCount VTags trackJetName_GhostAntiKt2TrackJet",
                                   "m_truthDetailStr"             : "kinematic type bVtx parents children",
                                   "m_evtDetailStr"               : "pileup",
                                   "m_boostedSysName"             : "AntiKt10LCTopoTrimmedPtFrac5SmallR20_Calib_Algo",
                                   "m_metContainerName"           : "RefFinalEM",
                                   "m_metDetailStr"               : "",
                                   } )
