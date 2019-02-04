import ROOT
from xAH_config import *

def config_BoostedAnalysis(c, args, doSystematics):

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
                                "m_sort"                  : True,
                                "m_saveAllCleanDecisions" : True,
                                "m_calibConfigFullSim"    : "JES_MC15recommendation_FatJet_Nov2016_QCDCombinationUncorrelatedWeights.config",
                                "m_calibConfigData"       : "JES_MC15recommendation_FatJet_Nov2016_QCDCombinationUncorrelatedWeights.config",
                                "m_doCleaning"            : False, #don't clean large R jets
                                "m_JESUncertConfig"       : "$ROOTCOREBIN/data/JetUncertainties/UJ_2016/Moriond2017/UJ2016_CombinedMass_strong.config",
                                "m_JESUncertMCType"       : "MC15c",
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
                                "m_JERConfig"             : "$ROOTCOREBIN/data/XhhBoosted/JERConfig_20170122.root",
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
                                          "m_operatingPt"             : "FixedCutBEff_70", #FixedCutBEff_70
                                          "m_operatingPtCDI"          : "FixedCutBEff_70", #FixedCutBEff_70
                                          "m_corrFileName"            :"xAODBTaggingEfficiency/13TeV/2016-20_7-13TeV-MC15-CDI-2017-06-07_v2.root",
                                          "m_jetAuthor"               : "AntiKt2PV0TrackJets",
                                          "m_taggerName"              : "MV2c10",
                                          "m_decor"                   : "BTag",
                                          } )

    #
    #  Event Cuts
    #
    c.setalg("XhhBoosted.SetXhhEventCuts", { "m_name"               : "XhhBoosted_setXhhEventCuts", 
                                             "m_inJetName"          : "selCaloJets",
                                             "m_leadingJetPtCut"    : 350e3,
                                             "m_subleadingJetPtCut" : 250e3,
                                             "m_dEtaCut"            : 1.7,
                                             "m_trackJet"           : "GhostAntiKt2TrackJet", #GhostVR30Rmax4Rmin02TrackJet
                                             "m_trackJetPtCut"      : 10e3,
                                             "m_trackJetEtaCut"     : 2.5,
                                             "m_outJetName"         : "finalBoostedJets",
                                             "m_inputAlgo"          : "selCaloJets_Algo",
                                             "m_outputAlgo"         : "finalBoostedJets_Algo",
                                             "m_dothirdJet"         : True,
                                             "m_dothirdTrkJet"      : True,
                                             } ) 

    #
    # Event Hists
    #
    c.setalg("PlotXhhEvent", { "m_name"        : "noCuts/", 
                               "m_eventCuts"   : "",                 
                               "m_inJetName"   : "selCaloJets",
                               "m_inDiJetName" : "finalBoostedJets"} )

    c.setalg("PlotXhhEvent", { "m_name"        : "Cut_2j/", 
                               "m_signalRegionCut" : "BoostedPass_SignalMass",
                               "m_eventCuts"   : "BoostedPass_AtLeast2Jets", 
                               "m_inJetName"   : "selCaloJets",
                               "m_inDiJetName" : "finalBoostedJets"} )
