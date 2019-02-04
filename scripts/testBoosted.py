
#
# Ntuples
#
c.setalg("XhhTestBoostedNtuple", { "m_name"                       : "TestNtuples",
                                   "m_boostedHcandName"           : "finalBoostedJets",
                                   "m_debug"                      : False,
                                   "m_trigDetailStr"              : "passTriggers",
                                   "m_inTruthParticleName"        : "TruthParticles",
                                   "m_boostedJetDetailStr"        : "kinematic substructure constituent bosonCount VTags trackJetName_GhostAntiKt2TrackJet",
                                   "m_truthDetailStr"             : "kinematic type bVtx parents children",
                                   "m_evtDetailStr"               : "pileup",
                                   "m_boostedSysName"             : "finalBoostedJets_Algo",
                                   "m_muonContainerName"          : "Muons_Selected", 
                                   "m_muonDetailStr"              : "kinematic quality energyLoss isolation", 
                                   "m_metContainerName"           : "RefFinalEM",
                                   "m_metDetailStr"               : "",
                                   "m_doResolutionStudy"          : False,
                                   } )
