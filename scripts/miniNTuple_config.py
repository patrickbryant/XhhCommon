import ROOT
from xAH_config import xAH_config
import sys, os

sys.path.insert(0, os.environ['ROOTCOREBIN']+"/user_scripts/XhhCommon/")

from resolved_config    import *
from XhhBoosted_config  import *
from XhhLepTop_config   import *

c = xAH_config()


#
# Basic Setup 
#
triggersList = ['L1_4J20',
                'L1_J100',
                'L1_3J25.0ETA23',
                'L1_4J15.0ETA25',
                'L1_J75_3J20',
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
                'HLT_j400',
                'HLT_j360',
                'HLT_j100',
                'HLT_j110',
                'HLT_j150',
                'HLT_j175',
                'HLT_j200',
                'HLT_j260',
                'HLT_.*bperf.*',
                'HLT_3j.*',
                'HLT_4j.*',
                'HLT_j3.*a10.*',
                'HLT_j4.*a10.*',
                'HLT_j100_2j55_bmedium',
                'HLT_e24_lhtight_iloose',
                'HLT_mu26_imedium']

# triggersList = ['L1_4J20',
#                 'L1_J100',
#                 'L1_3J25.0ETA23',
#                 'L1_4J15.0ETA25',
#                 'HLT_j70_bmedium_3j70_L13J25.0ETA23',
#                 'HLT_2j35_btight_2j35_L13J25.0ETA23',
#                 'HLT_2j45_bmedium_2j45_L13J25.0ETA23',
#                 'HLT_j100_2j55_bmedium',
#                 'HLT_j225_bloose',
#                 'HLT_ht850.*',
#                 'HLT_j175_bmedium_j60_bmedium',
#                 ]



triggers = ",".join(triggersList)
c.setalg("BasicEventSelection", { "m_name"                  : "basicEventSel",
                                  "m_applyGRLCut"           : False,
                                  "m_doPUreweighting"       : False, 
                                  "m_vertexContainerName"   : "PrimaryVertices",
                                  "m_PVNTrack"              : 2,
                                  "m_truthLevelOnly"        : False,
                                  "m_applyPrimaryVertexCut" : True,
                                  "m_derivationName"        : "EXOT8", 
                                  "m_triggerSelection"      : triggers, 
                                  "m_storeTrigDecisions"    : True,
                                  "m_useMetaData"           : True,
                                  "m_applyTriggerCut"       : False,
                                  "m_storePassL1"           : True,
                                  "m_storePassHLT"          : True,
                                  "m_storeTrigKeys"         : True,
                                  } )



c.setalg("MuonCalibrator", { "m_name"                : "Muons", 
                             "m_inContainerName"     : "Muons", 
                             "m_outContainerName"    : "Muons_Calib", 
                             "m_outputAlgoSystNames" : "MuonCalibrator_Syst",
                             "m_debug"               : False,
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
                           } )
c.setalg("MuonHistsAlgo", {"m_name":"Muons_Selected/", "m_inContainerName":"Muons_Selected",  
                           "m_detailStr" : "kinematic quality energyLoss isolation", } )
                           
                    
#doSystematics = args.is_MC
doSystematics = False

#
#  Set up resolved Analysis
#
config_ResolvedAnalysis(c, args, doSystematics, isMC)

#
#  Set up Boosted Analysis
#
config_BoostedAnalysis(c, args, doSystematics)

#
#  Set up Leptonic Top Analysis
#
config_LepTopAnalysis(c, args, doSystematics)


#
# Ntuples
#
c.setalg("XhhMiniNtuple", { "m_name"                       : "MiniNTuple",
                            "m_boostedHcandName"           : "finalBoostedJets",
                            "m_resolvedJetsName"           : "AntiKt4EMTopoJets_Calib_preSel",
                            "m_resolvedHcandName"          : "PreDiJets",
                            "m_lepTopCandName"             : "LepTops",
                            "m_debug"                      : False,
                            "m_trigDetailStr"              : "passTriggers",
                            "m_inTruthParticleName"        : "TruthParticles",
                            "m_resolvedJetDetailStr"       : "kinematic clean trackPV flavorTag sfFTagFix70",
                            "m_lepTopJetDetailStr"         : "kinematic clean trackPV flavorTag sfFTagFix70",
                            "m_evtDetailStr"               : "pileup",
                            "m_resolvedSysName"            : "PreDiJets_Algo",
                            "m_boostedSysName"             : "finalBoostedJets_Algo",
                            "m_muonContainerName"          : "Muons_Selected", 
                            "m_muonDetailStr"              : "kinematic quality energyLoss isolation", 
                            "m_doResolutionStudy"          : False,
                            } )



