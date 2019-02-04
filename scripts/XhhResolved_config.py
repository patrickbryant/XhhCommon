import ROOT

def config_ResolvedAnalysis(c, args, doSystematics):

    #
    #  Data Config
    #
    if not doSystematics:
        #doPUreweighting    = False
        systName           = "Nominal"
        systVal            = 0


    #
    #  MC Config
    #
    else:
        #doPUreweighting    = True        
        systName           = "All"
        systVal            = 1


    #
    #  Jet Calibration
    #
    c.setalg("JetCalibrator", { "m_name"                   : "AntiKt4TopoEM", 
                                "m_inContainerName"        : "AntiKt4EMTopoJets",
                                "m_outContainerName"       : "AntiKt4EMTopoJets_Calib", 
                                "m_outputAlgo"             : "AntiKt4EMTopoJets_Calib_Algo",
                                "m_jetAlgo"                : "AntiKt4EMTopo",
                                "m_sort"                   : True,
                                "m_saveAllCleanDecisions"  : True,                         
                                "m_calibConfigAFII"        : "JES_MC15Prerecommendation_AFII_June2015.config",
                                "m_calibConfigFullSim"     : "JES_data2016_data2015_Recommendation_Dec2016.config",
                                "m_calibConfigData"        : "JES_data2016_data2015_Recommendation_Dec2016.config",
                                "m_calibSequence"          : "JetArea_Residual_Origin_EtaJES_GSC",
                                "m_setAFII"                : False,
                                "m_JESUncertConfig"        : "JetUncertainties/JES_2016/Moriond2017/JES2016_SR_Scenario1.config",
                                "m_JESUncertMCType"        : "MC15",
                                "m_JERUncertConfig"        : "JetResolution/Prerec2015_xCalib_2012JER_ReducedTo9NP_Plots_v2.root",
                                "m_JERFullSys"              : False,
                                "m_JERApplyNominal"        : False,
                                "m_systName"               : systName,
                                "m_systVal"                : systVal,
                                } )
    c.setalg("JetHistsAlgo", {"m_name":"jets_all/", "m_inContainerName":"AntiKt4EMTopoJets_Calib", 
                              "m_detailStr":"kinematic clean energy"} )


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
                               "m_inputAlgoSystNames"      : "MuonCalibrator_Syst",
                               "m_outputAlgoSystNames"     : "MuonPreSelectAlgo",
                               "m_MinIsoWPCut"             : "Loose", 
                           } )

    c.setalg("MuonHistsAlgo", {"m_name":"Muons_PreSelected/", "m_inContainerName":"Muons_PreSelected",  
                               "m_detailStr" : "kinematic quality energyLoss isolation", } )

    #
    #  Electron Calibration
    #
    c.setalg("ElectronCalibrator", {"m_name"                : "electronCalib",
                                    "m_inContainerName"     : "Electrons",
                                    "m_outContainerName"    : "Electrons_Calib",
                                    "m_inputAlgoSystNames"  : "",
                                    "m_outputAlgoSystNames" : "ElectronCalibrator_Syst",
                                    "m_esModel"             : "es2016PRE",
                                    "m_decorrelationModel"  : "FULL_v1",
                                    } )
    c.setalg("ElectronHistsAlgo", {"m_name":"Electrons_Calib/",    "m_inContainerName":"Electrons_Calib",  
                                   "m_detailStr" : "kinematic PID", } )
    
    c.setalg("ElectronSelector", {"m_name"                    : "ElectronPreSelection",
                                  "m_inContainerName"         : "Electrons_Calib",
                                  "m_outContainerName"        : "Electrons_PreSelected",
                                  "m_createSelectedContainer" : True,                             
                                  "m_pT_min"                  : 10e3,
                                  "m_eta_max"                 : 2.47,
                                  "m_vetoCrack"               : False,
                                  "m_doAuthorCut"             : False,
                                  "m_doOQCut"                 : True,
                                  "m_readIDFlagsFromDerivation" : False,
                                  "m_doLHPIDcut"              : True,
                                  "m_LHOperatingPoint"        : "LooseBL",
                                  "m_MinIsoWPCut" : "", #no isolation required
                                  "m_inputAlgoSystNames"      : "ElectronCalibrator_Syst",
                                  "m_outputAlgoSystNames"     : "ElectronPreSelectAlgo",                               
                                  "m_IsoWPList"               : "LooseTrackOnly,Loose,Tight,Gradient,GradientLoose",
                                  }  )
    c.setalg("ElectronHistsAlgo", {"m_name":"Electrons_PreSelected/",    "m_inContainerName":"Electrons_PreSelected",  
                                   "m_detailStr" : "kinematic isolation", } )             

    #
    #  Event Cleaning Jet Selection 
    #
    c.setalg("JetSelector", { "m_name"                    :  "EMTopoJetCleaning",
                              "m_inContainerName"         :  "AntiKt4EMTopoJets_Calib",
                              "m_inputAlgo"               :  "AntiKt4EMTopoJets_Calib_Algo",
                              "m_outContainerName"        :  "AntiKt4EMTopoJets_Calib_forCleaning",
                              "m_outputAlgo"              :  "AntiKt4EMTopoJets_Calib_forCleaning_Algo",
                              "m_decorateSelectedObjects" :  False, 
                              "m_createSelectedContainer" :  True, 
                              "m_cleanJets"               :  True, 
                              "m_markCleanEvent"          :  True, 
                              "m_cleanEvent"              :  False, 
                              "m_pT_min"                  :  20e3,
                              "m_eta_max"                 :  2.5,
                              "m_useCutFlow"              :  False,
                              "m_doJVT"                   :  True,
                              } )


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
                              "m_pT_min"                  :  25e3,
                              "m_eta_max"                 :  2.5,
                              "m_useCutFlow"              :  True,
                              "m_doJVT"                   :  True,
                              } )
    c.setalg("JetHistsAlgo", {"m_name":"jets_preSel/", "m_inContainerName":"AntiKt4EMTopoJets_Calib_preSel"
                              , "m_detailStr":"kinematic clean energy"} )


    c.setalg("BJetEfficiencyCorrector", { "m_name"                    : "BJetEffCor_AntiKt4EMTopoJets",
                                          "m_inContainerName"         : "AntiKt4EMTopoJets_Calib_preSel",
                                          # a bit special for b-tagging SF, since "Nominal" will NOT be converted to "" internally 
                                          "m_systName"                : ("" if systName == "Nominal" else systName),   
                                          "m_systVal"                 : systVal,
                                          "m_outputSystName"          : "AntiKt4EM_FTSys",
                                          "m_operatingPt"             : "FixedCutBEff_70",
                                          "m_operatingPtCDI"          : "FixedCutBEff_70",
                                          "m_corrFileName"            : "xAODBTaggingEfficiency/13TeV/2016-20_7-13TeV-MC15-CDI-2017-06-07_v2.root",
                                          "m_jetAuthor"               : "AntiKt4EMTopoJets",
                                          "m_taggerName"              : "MV2c10",
                                          "m_decor"                   : "BTag",
                                          } )

    #
    # ONLY USED FOR CUTFLOW HIST. SEEMS SILLY. FIXME
    #
    c.setalg("JetSelector", { "m_name"                    : "bTaggedJets",
                              "m_inContainerName"         : "AntiKt4EMTopoJets_Calib_preSel",
                              "m_inputAlgo"               : "AntiKt4EMTopoJets_Calib_preSel_Algo",
                              "m_outContainerName"        : "AntiKt4EMTopoJets_Calib_btagged",
                              "m_outputAlgo"              : "AntiKt4EMTopoJets_Calib_btagged_Algo",
                              "m_decorateSelectedObjects" : True, 
                              "m_decor"                   : "isBJet",  
                              "m_createSelectedContainer" : True, 
                              "m_cleanJets"               : False, 
                              "m_doBTagCut"               : True,
                              "m_corrFileName"            : "xAODBTaggingEfficiency/13TeV/2016-20_7-13TeV-MC15-CDI-2017-06-07_v2.root",
                              "m_taggerName"              : "MV2c10",
                              "m_operatingPt"             : "FixedCutBEff_70",
                              "m_jetAuthor"               : "AntiKt4EMTopoJets",
                              "m_useCutFlow"              : True,
                              } )
    c.setalg("JetHistsAlgo", {"m_name":"jets_bJets/"      , "m_inContainerName":"AntiKt4EMTopoJets_Calib_btagged"               
                              , "m_detailStr":"kinematic clean energy"} )


    #
    #  Overlap Removal
    #
    c.setalg("OverlapRemover",  {"m_name"                       : "overlap",
                                 "m_inputAlgoMuons"             : "MuonPreSelectAlgo",
                                 "m_inputAlgoElectrons"         : "ElectronPreSelectAlgo",
                                 "m_inputAlgoJets"              : "AntiKt4EMTopoJets_Calib_preSel_Algo",
                                 #"m_outputAlgoElectrons"        : "ElectronORAlgo",
                                 #"m_outputAlgoMuons"            : "MuonORAlgo",
                                 #"m_outputAlgoJets"             : "JetORAlgo",
                                 "m_useCutFlow"                 : False,
                                 "m_decorateSelectedObjects"    : True,
                                 "m_createSelectedContainers"   : True,
                                 "m_useSelected"                : False,
                                 "m_inContainerName_Electrons"  : "Electrons_PreSelected",
                                 "m_inContainerName_Muons"      : "Muons_PreSelected",
                                 "m_inContainerName_Jets"       : "AntiKt4EMTopoJets_Calib",
                                 "m_outContainerName_Muons"     : "MuonsForMet",
                                 "m_outContainerName_Electrons" : "Electrons_OR",
                                 "m_outContainerName_Jets"      : "JetsForMet"                             
                                 }  )


    #
    #  MeT Calibration
    #
    c.setalg("METConstructor", {"m_name"                  : "METBuilding",
                                "m_referenceMETContainer" : "MET_Reference_AntiKt4EMTopo",
                                "m_mapName"               : "METAssoc_AntiKt4EMTopo",
                                "m_coreName"              : "MET_Core_AntiKt4EMTopo",
                                "m_outputContainer"       : "RefFinalEM",
                                "m_inputJets"             : "JetsForMet",
                                "m_inputElectrons"        : "Electrons_OR",
                                "m_inputMuons"            : "MuonsForMet", 
                                "m_doMuonCuts"            : False,
                                "m_doElectronCuts"        : False,
                                "m_doMuonEloss"           : True,
                                "m_doIsolMuonEloss"       : True
                                } )
    c.setalg("MetHistsAlgo", {"m_name":"Met_RefFinalEM/",    "m_inContainerName":"RefFinalEM",
                              "m_detailStr" : "kinematic", } )

    #
    #  Electron Selection
    #
    c.setalg("ElectronSelector", {"m_name"                      : "ElectronSelection",
                                  "m_inContainerName"           : "Electrons_OR",
                                  "m_outContainerName"          : "Electrons_Selected",
                                  "m_createSelectedContainer"   : True,                             
                                  "m_pT_min"                    : 25e3,
                                  "m_eta_max"                   : 2.47,
                                  "m_vetoCrack"                 : False,
                                  "m_doAuthorCut"               : False,
                                  "m_d0sig_max"                 : 5.0,
                                  "m_z0sintheta_max"            : 0.5,
                                  "m_doOQCut"                   : False,
                                  "m_readIDFlagsFromDerivation" : False,
                                  "m_doLHPIDcut"                : True,
                                  "m_LHOperatingPoint"          : "Tight",
                                  "m_MinIsoWPCut"               : "GradientLoose", #no isolation required
                                  "m_IsoWPList"                 : "LooseTrackOnly,Loose,Tight,Gradient,GradientLoose",
                                  }  )
    c.setalg("ElectronHistsAlgo", {"m_name":"Electrons_Selected/",    "m_inContainerName":"Electrons_Selected",  
                                   "m_detailStr" : "kinematic isolation", } )             


    #
    #  Muon Selection
    #
    #
    c.setalg("MuonSelector", { "m_name"                    : "MuonSelection", 
                               "m_inContainerName"         : "MuonsForMet", 
                               "m_outContainerName"        : "Muons_Prompt", 
                               "m_createSelectedContainer" : True,
                               "m_pT_min"                  : 25*1000,
                               "m_eta_max"                 : 2.5,
                               "m_muonQualityStr"          : "Medium", #tight use energy loss information by default 
                               "m_MinIsoWPCut"             : "Medium",
                               } )
    c.setalg("MuonHistsAlgo", {"m_name":"Muons_Prompt/",    "m_inContainerName":"Muons_Prompt",
                               "m_detailStr" : "kinematic quality isolation", } )


    


    #
    # Event Hists
    #
    c.setalg("PlotXhhEvent", { "m_name"        : "XhhCutFlow/", 
                               "m_eventCuts"   : "",
                               "m_inJetName"   : "AntiKt4EMTopoJets_Calib_preSel", 
                               "m_inBJetName"  : "AntiKt4EMTopoJets_Calib_btagged", 
                               #"m_inDiJetName" : "PreDiJets",
                               } )
    

