import ROOT
from xAH_config import xAH_config
import sys, os

sys.path.insert(0, os.environ['ROOTCOREBIN']+"/user_scripts/XhhCommon/")

from XhhResolved_config_VHqqbb        import *
from XhhBoosted_config_VHqqbb         import *
from XhhLepTop_config                 import *

c = xAH_config()


#
# Basic Setup 
#
triggersList = ['L1_4J20',
                'L1_J100',
                'L1_3J25.0ETA23',
                'L1_4J15.0ETA25',
                'L1_J75_3J20',
                'HLT_.*bmv2c20.*',
                'HLT_ht.*',
                'HLT_j65_bt.*',
                'HLT_j70_bt.*',
                'HLT_j75_bt.*',
                'HLT_j175_bt.*',
                'HLT_2j35_bt.*',
                'HLT_2j45_bt.*',
                'HLT_2j55_bt.*',
                'HLT_2j65_bt.*',
                'HLT_2j70_bt.*',
                'HLT_2j75_bt.*',
                'HLT_j65_bm.*',
                'HLT_j70_bm.*',
                'HLT_j75_bm.*',
                'HLT_j175_bm.*',
                'HLT_2j35_bm.*',
                'HLT_2j45_bm.*',
                'HLT_2j55_bm.*',
                'HLT_2j65_bm.*',
                'HLT_2j70_bm.*',
                'HLT_2j75_bm.*',
                'HLT_j225_bl.*',
                'HLT_j300_bl.*',
                'HLT_j420.*',
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
                'HLT_.*bperf.*',
                'HLT_.*boffperf.*',
                'HLT_3j.*',
                'HLT_4j.*',
                'HLT_j3.*a10.*',
                'HLT_j4.*a10.*',
                'HLT_j100_2j55_bmedium',
                'HLT_e24_lhtight_iloose',
                'HLT_mu26_imedium']



triggers = ",".join(triggersList)
c.setalg("BasicEventSelection", { "m_name"                  : "basicEventSel",
                                  "m_debug"                 : False,
                                  "m_applyGRLCut"           : False,
                                  "m_doPUreweighting"       : False, 
                                  "m_vertexContainerName"   : "PrimaryVertices",
                                  "m_PVNTrack"              : 2,
                                  "m_truthLevelOnly"        : False,
                                  "m_applyPrimaryVertexCut" : True,
                                  "m_derivationName"        : "EXOT3Kernel",
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

# muon for Higgs mass correction purpose

c.setalg("MuonCalibrator", { "m_name"                : "Muons", 
                             "m_inContainerName"     : "Muons", 
                             "m_outContainerName"    : "Muons_Calib", 
                             "m_outputAlgoSystNames" : "MuonCalibrator_Syst",
                             # "m_release"             : "PreRecs2016_05_23",
                             "m_debug"               : False,
                             "m_forceDataCalib"      : True,
                             } )

c.setalg("MuonHistsAlgo", {"m_name":"Muons_Calib/",    "m_inContainerName":"Muons_Calib",  
                           "m_detailStr" : "kinematic energyLoss", } )


c.setalg("MuonSelector", { "m_name"                    : "MuonSelector", 
                           "m_inContainerName"         : "Muons_Calib", 
                           "m_outContainerName"        : "Muons_Selected", 
                           "m_createSelectedContainer" : True,
                           "m_pT_min"                  : 4*1000,
                           "m_eta_max"                 : 2.5,
                           "m_muonType"                : "Combined",
                           "m_muonQualityStr"          : "Medium",
                           "m_debug"                   : False,
                           } )
c.setalg("MuonHistsAlgo", {"m_name":"Muons_Selected/", "m_inContainerName":"Muons_Selected",  
                           "m_detailStr" : "kinematic quality energyLoss isolation", } )
                           

# muons for veto purpose

c.setalg("MuonSelector", { "m_name"                    : "MuonSelector_Veto", 
                           "m_inContainerName"         : "Muons_Calib", 
                           "m_outContainerName"        : "Muons_Veto", 
                           "m_createSelectedContainer" : True,
                           "m_pT_min"                  : 7*1000,
                           "m_eta_max"                 : 2.7,
                           "m_muonType"                : "Combined",
                           "m_muonQualityStr"          : "Loose",
                           "m_MinIsoWPCut"             : "LooseTrackOnly",
                           "m_d0sig_max"               : 3.,
                           "m_z0sintheta_max"          : 0.5,
                           "m_debug"                   : False,
                           } )

# electrons for veto purpose

c.setalg("ElectronCalibrator", { "m_name"                : "Electrons",
                                 "m_inContainerName"     : "Electrons",
                                 "m_outContainerName"    : "Electrons_Calib_Veto",
                                 "m_outputAlgoSystNames" : "ElectronCalibrator_Veto_Syst",
                                 "m_esModel"             : "es2016PRE",
                                 "m_decorrelationModel"  : "FULL_v1",    # this one is randomly assigned ... should not matter ... 
                                 "m_debug"               : False,
                               })

c.setalg("ElectronSelector", { "m_name"                    : "ElectronSelector_Veto",
                               "m_inContainerName"         : "Electrons_Calib_Veto",
                               "m_outContainerName"        : "Electrons_Veto",
                               "m_createSelectedContainer" : True,
                               "m_doLHPID"                 : True,
                               "m_doLHPIDcut"              : True,
                               "m_LHOperatingPoint"        : "Loose",
                               "m_MinIsoWPCut"             : "LooseTrackOnly",
                               "m_d0sig_max"               : 5.,
                               "m_z0sintheta_max"          : 0.5,
                               "m_pT_min"                  : 7*1000.,
                               "m_eta_max"                 : 2.47,
                               "m_debug"                   : False,
                             })

#
#  Set up resolved Analysis
#
#config_ResolvedAnalysis(c, args, doSystematics = args.is_MC)
config_ResolvedAnalysis(c, args, doSystematics = False)

#
#  Set up Boosted Analysis
#
# config_BoostedAnalysis(c, args, doSystematics = args.is_MC)
config_BoostedAnalysis(c, args, doSystematics = False)

#
#  Set up Leptonic Top Analysis
#
#config_LepTopAnalysis(c, args, doSystematics = args.is_MC)
config_LepTopAnalysis(c, args, doSystematics = False)

# MET for veto purpose
# Must be placed after AKT4 jets are reconstructed!

c.setalg("METConstructor", { "m_name"            : "METConstructor_Veto",

                             "m_mapName"         : "METAssoc_AntiKt4EMTopo",
                             "m_coreName"        : "MET_Core_AntiKt4EMTopo",
                             "m_outputContainer" : "MET_Veto",

                             "m_inputJets"       : "AntiKt4EMTopoJets_Calib",
                             "m_inputElectrons"  : "Electrons_Veto",
                             "m_inputMuons"      : "Muons_Veto",
                             # no photon/tau

                             # no additional selection

                             "m_useCaloJetTerm"  : True,
                             "m_useTrackJetTerm" : False,

                             "m_debug"           : False,
                           })

# OR
c.setalg("OverlapRemover", {"m_name"                        : "ORConstructor_qqbb",

                            "m_inContainerName_Muons"       : "Muons_Veto",
                            "m_inContainerName_Electrons"   : "Electrons_Veto",
                            "m_inContainerName_Jets"        : "AntiKt4EMTopoJets_Calib",

                            "m_inputAlgoJets"               : "AntiKt4EMTopoJets_Calib_Algo",

                            "m_createSelectedContainers"    : True,
                            "m_decorateSelectedObjects"     : True,
                            "m_outContainerName_Muons"      : "Muons_Veto_OR",
                            "m_outContainerName_Electrons"  : "Electrons_Veto_OR",
                            "m_outContainerName_Jets"       : "AntiKt4EMTopoJets_Calib_OR",

                            "m_outputAlgo"                  : "OR_Alg_qqbb",

                            "m_outputLabel"                 : "passOR_qqbb",
                            "m_masterToolName"              : "OverlapRemovalTool_qqbb",
                            "m_useCutFlow"                  : False,
                            "m_useSelected"                 : False,

                            "m_debug"                       : False,
                           })

#
# Ntuples
#
c.setalg("XhhMiniNtuple", { "m_name"                       : "MiniNTuple",
                            "m_boostedHcandName"           : "finalBoostedJets",
                            "m_resolvedJetsName"           : "AntiKt4EMTopoJets_Calib_preSel",
                            "m_lepTopCandName"             : "LepTops",
                            "m_debug"                      : False,
                            "m_trigDetailStr"              : "passTriggers",
                            "m_inTruthParticleName"        : "TruthParticles",
                            "m_resolvedJetDetailStr"       : "kinematic clean trackPV flavorTag sfFTagFix70 JVC",
                            "m_boostedJetDetailStr"        : "kinematic substructure constituent",
                            "m_lepTopJetDetailStr"         : "kinematic clean trackPV flavorTag sfFTagFix70",
                            "m_truthDetailStr"             : "kinematic type bVtx parents children",
                            "m_evtDetailStr"               : "pileup",
                            "m_resolvedSysName"            : "AntiKt4EMTopoJets_Calib_Algo",
                            "m_boostedSysName"             : "finalBoostedJets_Algo",
                            "m_doXhhTagging"               : True,       # specific for VHqqbb
                            "m_FatJetMassCut"              : 50.,        # specific for VHqqbb
                            "m_TrackJetWP"                 : "77",       # specific for VHqqbb
                            "m_muonContainerName"          : "Muons_Selected", 
                            "m_muonDetailStr"              : "kinematic quality energyLoss isolation trackparams", 
                            "m_elecContainerName"          : "Electrons_Selected", 
                            "m_elecDetailStr"              : "kinematic quality PID isolation trackparams", 
                            "m_metContainerName"           : "RefFinalEM",
                            "m_metDetailStr"               : "refEle refMuons refJet softClus softTrk",
                            "m_doResolutionStudy"          : True,
                            "m_doResolved"                 : True,
                            "m_doBoosted"                  : True,
                            "m_doLeptop"                   : True,
                            "m_storeLeptonVeto"            : True,       # specific for VHqqbb analysis
                            "m_storeMETVeto"               : True,       # specific for VHqqbb analysis
                            "m_storeTruth"                 : True,
                            } )



