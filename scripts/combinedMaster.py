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
from XhhResolved_config    import *
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
                'L1_HT.*',
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
                'HLT_.*bmv2c20.*',
                'HLT_mu26_imedium']





triggers = ",".join(triggersList)
c.setalg("BasicEventSelection", { "m_name"                  : "basicEventSel",
                                  "m_derivationName"        : "EXOT8Kernel",
                                  "m_applyGRLCut"           : False,
                                  "m_doPUreweighting"       : args.is_MC,
                                  "m_lumiCalcFileNames"     :  "$ROOTCOREBIN/data/XhhCommon/ilumicalc_histograms_None_266904-267639_periodA+B1_DetStatus-v62-pro18_DQDefects-00-01-02_PHYS_StandardGRL_All_Good.root",
                                  "m_PRWFileNames"          : "dev/PileupReweighting/mc15c_v2_defaults.NotRecommended.prw.root",
                                  "m_PVNTrack"              : 2,
                                  "m_applyPrimaryVertexCut" : True,
                                  "m_applyEventCleaningCut" : True,
                                  "m_applyCoreFlagsCut"     : True,
                                  "m_trigDecTool_name"      : "TrigDecTool",
                                  "m_triggerSelection"      : triggers, 
                                  "m_storeTrigDecisions"    : True,
                                  "m_useMetaData"           : True,
                                  "m_applyTriggerCut"       : False,
                                  "m_storePassL1"           : True,
                                  "m_storePassHLT"          : True,
                                  "m_storeTrigKeys"         : True,
                                  } )

#
# BJet Trigger Emulation
#
if args.is_MC:
    c.setalg("BJetTriggerEmulationAlg", { "m_name"                       : "BJetTriggerEmulationAlg",
                                          "m_onlyLoadhh4bChains"         : False,
                                          "m_load2016Chains"             : True,
                                          "m_load2015Chains"             : True,
                                          "m_testMCMenu"                 : True,
                                          } )




c.setalg("MuonCalibrator", { "m_name"                : "Muons", 
                             "m_inContainerName"     : "Muons", 
                             "m_outContainerName"    : "Muons_Calib", 
                             "m_outputAlgoSystNames" : "MuonCalibrator_Syst",
                             #"m_release"             : "Recs2016_08_07",
                             "m_forceDataCalib"      : True,
                             } )

c.setalg("MuonHistsAlgo", {"m_name":"Muons_Calib/",    "m_inContainerName":"Muons_Calib",  
                           "m_detailStr" : "kinematic energyLoss", } )

#
#  For muon in Jet Selection
#
c.setalg("MuonSelector", { "m_name"                    : "MuonSelector", 
                           "m_inContainerName"         : "Muons_Calib", 
                           "m_outContainerName"        : "Muons_Selected", 
                           "m_createSelectedContainer" : True,
                           "m_pT_min"                  : 4*1000,
                           "m_eta_max"                 : 2.5,
                           "m_muonQualityStr"          : "Medium",
                           } )

c.setalg("MuonHistsAlgo", {"m_name":"Muons_Selected/", "m_inContainerName":"Muons_Selected",  
                           "m_detailStr" : "kinematic quality energyLoss isolation", } )

                           
                    
#
#  Set up resolved Analysis
#
config_ResolvedAnalysis(c, args, o.doResolvedSys)

#
#  Set up Boosted Analysis
#
config_BoostedAnalysis(c, args, o.doBoostedSys)


#
# Ntuples
#
c.setalg("XhhMiniNtuple", { "m_name"                       : "MiniNTuple",
                            "m_boostedHcandName"           : "finalBoostedJets",
                            "m_resolvedJetsName"           : "AntiKt4EMTopoJets_Calib_preSel",
                            #"m_writeAll"                   : True,
                            "m_trigDetailStr"              : "passTriggers",
                            "m_inTruthParticleName"        : "TruthParticles",
                            "m_resolvedJetDetailStr"       : "kinematic clean trackPV flavorTag sfFTagFix70 JVC",
                            "m_boostedJetDetailStr"        : "kinematic substructure constituent",
                            "m_truthDetailStr"             : "kinematic type bVtx parents children",
                            "m_evtDetailStr"               : "pileup",
                            "m_resolvedSysName"            : "AntiKt4EMTopoJets_Calib_Algo",
                            "m_boostedSysName"             : "finalBoostedJets_Algo",
                            "m_doXhhTagging"               : False,
                            "m_muonContainerName"          : "Muons_Selected", 
                            "m_promptMuonContainerName"    : "Muons_Prompt", 
                            "m_muonDetailStr"              : "kinematic quality energyLoss isolation trackparams", 
                            "m_elecContainerName"          : "Electrons_Selected", 
                            "m_elecDetailStr"              : "kinematic quality PID isolation trackparams", 
                            "m_metContainerName"           : "RefFinalEM",
                            "m_metDetailStr"               : "refEle refMuons refJet softClus softTrk",
                            "m_doResolutionStudy"          : False,
                            "m_storeTruth"                 : True,
                            "m_doResolved"                 : True,
                            "m_doBoosted"                  : True,
                            "m_doLeptop"                   : True,
                            } )



