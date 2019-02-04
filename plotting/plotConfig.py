#
# File that stores the config info for all plots. Should probably
# make set it up somehow so that this can be passed into plot.py as an argument
#

plot_configs = {}


#this is for different kinematic reweighting locations
qcdWeights = {"trig"     :{0 : 0.00898, 1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 3.64534},
              "m4j"      :{0 : 0.00943, 1 : 1.30179, 2 : 1.79096, 3 : 2.44450, 4 : 3.34117, 5 : 4.56565}, #need update
              "ttbar"    :{0 : 0.00954, 1 : 1.34975, 2 : 1.91893, 3 : 2.70474, 4 : 3.81413, 5 : 5.37688}, #need update
              "b65_3j65" :{0 : 0.01193, 1 : 1.39675, 2 : 1.95945, 3 : 2.75475, 4 : 3.87146, 5 : 5.44100},
              "run1or"   :{0 : 0.06041, 1 : 1.18372, 2 : 1.28595, 3 : 1.40193, 4 : 1.52942, 5 : 1.66878},
              }

paths = {
         "m4j"     :{0:'reWeightData0', 1:'reWeightDataM4jKine1', 2:'reWeightDataM4jKine2', 3:'reWeightDataM4jKine3', 4:'reWeightDataM4jKine4', 5:'reWeightDataM4jKine5'},
         "trig"    :{0:'reWeightData0', 1:'reWeightDataTrigKine1', 2:'reWeightDataTrigKine2', 3:'reWeightDataTrigKine3', 4:'reWeightDataTrigKine4', 5:'reWeightDataTrigKine5'},
         "ttbar"   :{0:'reWeightData0', 1:'reWeightDataTTVetoKine1', 2:'reWeightDataTTVetoKine2', 3:'reWeightDataTTVetoKine3', 4:'reWeightDataTTVetoKine4', 5:'reWeightDataTTVetoKine5'},
         "b65_3j65":{0:'reWeightData0', 1:'reWeightDatab65_3j65_only1', 2:'reWeightDatab65_3j65_only2', 3:'reWeightDatab65_3j65_only3', 4:'reWeightDatab65_3j65_only4', 5:'reWeightDatab65_3j65_only5'},
         "run1or"  :{0:'reWeightData0', 1:'reWeightDatarun1or1', 2:'reWeightDatarun1or2', 3:'reWeightDatarun1or3', 4:'reWeightDatarun1or4', 5:'reWeightDatarun1or5'}
         }

lumi = "2.08/fb"

samples = {}
reWeightStages = ["trig","m4j","ttbar","b65_3j65","run1or"]
cuts = {"btag":"", "trig":"PassTrig", "m4j":"PassM4jDep", "ttbar":"TTVeto", "b65_3j65": "HLT_j65_btight_3j65_L13J25", "run1or": "Run1_OR"} 
massRegions = {"sideband":"Sideband", "control":"Control", "Signal":"signal"}
for reWeightStage in reWeightStages:
    for mass in massRegions:
        for cut in cuts.keys(): 
            for i in range(0,6):
                samples[reWeightStage+cut+mass+str(i)] = [ {
                                    'name'      : 'data',
                                    'is_data'   : True,
                                    'stack'     : False,
                                    'overlay'   : True,
                                    'path'      : '../../'+paths[reWeightStage][i]+'/hist-pbryant.root',
                                    'folderReg' : massRegions[mass],
                                    'folderCuts': cuts[cut],
                                    'folderTag' : 'FourTag_',
                                    'label'     : '4b',
                                    'color'     : 'ROOT.kBlack',
                                    'rColor'    : 'ROOT.kRed-3',
                                    'weights'   : 1
                                   },
                                   {
                                    'name'       : 'qcd',
                                    'is_data'    : False,
                                    'stack'      : True,
                                    'overlay'    : False,
                                    'path'       : '../../'+paths[reWeightStage][i]+'/hist-pbryant.root',
                                    'folderReg'  : massRegions[mass],
                                    'folderCuts' : cuts[cut],
                                    'folderTag'  : 'TwoTag_',
                                    'label'      : "2b",
                                    'color'      : 'ROOT.kAzure-9',
                                    'rColor'     : 'ROOT.kRed-3',
                                    'weights'    : qcdWeights[reWeightStage][i]
                                   },
                                   {
                                    'name'       : 'ttbar',
                                    'is_data'    : False,
                                    'stack'      : False,
                                    'overlay'    : True,
                                    'path'       : '../../MC0/hist-data-MiniNTuple.root',
                                    'folderReg'  : massRegions[mass],
                                    'folderCuts' : cuts[cut],
                                    'folderTag'  : 'TwoTag_',
                                    'label'      : "ttbar",
                                    'color'      : 'ROOT.kBlue',
                                    'rColor'     : 'ROOT.kRed',
                                    'weights'    : 1
                                   } ] 

#
# List of plots to make for resolved analysis from the post processing hists
#

plotsList = [ 
  {#Event Level Plots
      'name'     : 'm4j',
      'variable' : 'm4j_l',
      'xtitle'   : "M_{4j} [GeV]",
      'ytitle'   : 'Number of events',
      'rebin'    : 3,
      'x_min'    : 300.0,
      'x_max'    : 1800.0,
      'logY'     : False
},{
      'name'     : 'nljets',
      'variable' : 'nJetOther',
      'xtitle'   : "# of extra jets",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
      'x_min'    : -0.5,
      'x_max'    : 7.5
},{
      'name'     : 'nbjets',
      'variable' : 'nbjets',
      'xtitle'   : "# of bjets in dijets",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
      'x_min'    : -0.5,
      'x_max'    : 4.5

},{#Two HCands Plots
      'name'     : 'hcands_dR',
      'variable' : 'hCandDr',
      'xtitle'   : "Higgs Candidate dR",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 3,
      'x_min'    : 0.3,
      'x_max'    : 5.5
},{
      'name'     : 'hcands_dPhi',
      'variable' : 'hCandDphi',
      'xtitle'   : "Higgs Candidate dPhi",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 3
},{
      'name'     : 'hcands_dEta',
      'variable' : 'hCandDeta',
      'xtitle'   : "Higgs Candidate dEta",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4

},{#Single HCand Plots
      'name'     : 'leadHCand_Mass',
      'variable' : 'leadHCand_Mass',
      'xtitle'   : "lead dijet mass",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 4,
      'x_min'    : 25.0,
      'x_max'    : 450.0
},{
      'name'     : 'sublHCand_Mass',
      'variable' : 'sublHCand_Mass',
      'xtitle'   : "sublead dijet mass",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 4,
      'x_min'    : 25.0,
      'x_max'    : 400.0
},{
      'name'     : 'leadHCand_Pt',
      'variable' : 'leadHCand_Pt_m',
      'xtitle'   : "Lead Higgs Candidate Pt",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 3,
      'x_min'    : 150.0,
      'x_max'    : 800.0
},{
      'name'     : 'sublHCand_Pt',
      'variable' : 'sublHCand_Pt_m',
      'xtitle'   : "Sublead Higgs Candidate Pt",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 3,
      'x_min'    : 100.0,
      'x_max'    : 800.0
},{
      'name'     : 'leadHCand_Eta',
      'variable' : 'leadHCand_Eta',
      'xtitle'   : "leadHCand_Eta",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 4
},{
      'name'     : 'sublHCand_Eta',
      'variable' : 'sublHCand_Eta',
      'xtitle'   : "sublHCand_Eta",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 4
},{
      'name'     : 'leadHCand_Phi',
      'variable' : 'leadHCand_Phi',
      'xtitle'   : "leadHCand_Phi",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 4
},{
      'name'     : 'sublHCand_Phi',
      'variable' : 'sublHCand_Phi',
      'xtitle'   : "sublHCand_Phi",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 4
},{
      'name'     : 'leadHCand_dRjj',
      'variable' : 'leadHCand_dRjj',
      'xtitle'   : "dR in leading DiJet system",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 2,
      'x_min'    : 0.4,
      'x_max'    : 1.6
},{
      'name'     : 'sublHCand_dRjj',
      'variable' : 'sublHCand_dRjj',
      'xtitle'   : "dR in subleading DiJet system",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 2,
      'x_min'    : 0.4,
      'x_max'    : 1.6
},{
      'name'     : 'leadHCand_mW',
      'variable' : 'leadHCand_mW',
      'xtitle'   : "leadHCand_mW",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 10
},{
      'name'     : 'sublHCand_mW',
      'variable' : 'sublHCand_mW',
      'xtitle'   : "sublHCand_mW",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 10
},{
      'name'     : 'leadHCand_mTop',
      'variable' : 'leadHCand_mTop',
      'xtitle'   : "leadHCand_mTop",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 10
},{
      'name'     : 'sublHCand_mTop',
      'variable' : 'sublHCand_mTop',
      'xtitle'   : "sublHCand_mTop",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 10
},{
      'name'     : 'leadHCand_Xtt',
      'variable' : 'leadHCand_Xtt',
      'xtitle'   : "leadHCand_Xtt",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 10
},{
      'name'     : 'sublHCand_Xtt',
      'variable' : 'sublHCand_Xtt',
      'xtitle'   : "sublHCand_Xtt",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 10

},{#HCand Constituents Plots
      'name'     : 'leadHCand_leadJet_Pt',
      'variable' : 'leadHCand_leadJet_Pt_m',
      'xtitle'   : "lead dijet lead jet pt",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 2,
      'x_min'    : 100.0,
      'x_max'    : 700.0
},{
      'name'     : 'leadHCand_sublJet_Pt',
      'variable' : 'leadHCand_sublJet_Pt',
      'xtitle'   : "lead dijet sublead jet pt",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 2,
      'x_min'    : 20.0,
      'x_max'    : 350.0
},{
      'name'     : 'sublHCand_leadJet_Pt',
      'variable' : 'sublHCand_leadJet_Pt_m',
      'xtitle'   : "sublead dijet lead jet pt",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 2,
      'x_min'    : 40.0,
      'x_max'    : 600.0
},{
      'name'     : 'sublHCand_sublJet_Pt',
      'variable' : 'sublHCand_sublJet_Pt',
      'xtitle'   : "sublead dijet sublead jet pt",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 2,
      'x_min'    : 20.0,
      'x_max'    : 350.0
},{
      'name'     : 'leadHCand_leadJet_Eta',
      'variable' : 'leadHCand_leadJet_Eta',
      'xtitle'   : "lead dijet lead jet eta",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'leadHCand_sublJet_Eta',
      'variable' : 'leadHCand_sublJet_Eta',
      'xtitle'   : "lead dijet sublead jet eta",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'sublHCand_leadJet_Eta',
      'variable' : 'sublHCand_leadJet_Eta',
      'xtitle'   : "sublead dijet lead jet eta",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'sublHCand_sublJet_Eta',
      'variable' : 'sublHCand_sublJet_Eta',
      'xtitle'   : "sublead dijet sublead jet eta",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'leadHCand_leadJet_Phi',
      'variable' : 'leadHCand_leadJet_Phi',
      'xtitle'   : "lead dijet lead jet phi",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'leadHCand_sublJet_Phi',
      'variable' : 'leadHCand_sublJet_Phi',
      'xtitle'   : "lead dijet sublead jet phi",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'sublHCand_leadJet_Phi',
      'variable' : 'sublHCand_leadJet_Phi',
      'xtitle'   : "sublead dijet lead jet phi",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'sublHCand_sublJet_Phi',
      'variable' : 'sublHCand_sublJet_Phi',
      'xtitle'   : "sublead dijet sublead jet phi",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'leadHCand_leadJet_MV2c20',
      'variable' : 'leadHCand_leadJet_MV2c20',
      'xtitle'   : "lead dijet lead jet MV2c20",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'leadHCand_sublJet_MV2c20',
      'variable' : 'leadHCand_sublJet_MV2c20',
      'xtitle'   : "lead dijet sublead jet MV2c20",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'sublHCand_leadJet_MV2c20',
      'variable' : 'sublHCand_leadJet_MV2c20',
      'xtitle'   : "sublead dijet lead jet MV2c20",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,
},{
      'name'     : 'sublHCand_sublJet_MV2c20',
      'variable' : 'sublHCand_sublJet_MV2c20',
      'xtitle'   : "sublead dijet sublead jet MV2c20",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 4,

},{#Untagged HCand plots
      'name'     : 'untaggedHCand_Mass',
      'variable' : 'untaggedHCand_Mass',
      'xtitle'   : "untagged dijet mass",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
      'x_min'    : 25.0,
      'x_max'    : 450.0
},{
      'name'     : 'untaggedHCand_Pt',
      'variable' : 'untaggedHCand_Pt_l',
      'xtitle'   : "Untagged Higgs Candidate Pt",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
      'x_min'    : 100.0,
      'x_max'    : 800.0
},{
      'name'     : 'untaggedHCand_Eta',
      'variable' : 'untaggedHCand_Eta',
      'xtitle'   : "untaggedHCand_Eta",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 1
},{
      'name'     : 'untaggedHCand_Phi',
      'variable' : 'untaggedHCand_Phi',
      'xtitle'   : "untaggedHCand_Phi",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 1
},{
      'name'     : 'untaggedHCand_dRjj',
      'variable' : 'untaggedHCand_dRjj',
      'xtitle'   : "dR in untagged DiJet system",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
      'x_min'    : 0.4,
      'x_max'    : 1.6
},{
      'name'     : 'untaggedHCand_mW',
      'variable' : 'untaggedHCand_mW',
      'xtitle'   : "untaggedHCand_mW",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 2
},{
      'name'     : 'untaggedHCand_mTop',
      'variable' : 'untaggedHCand_mTop',
      'xtitle'   : "untaggedHCand_mTop",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 2
},{
      'name'     : 'untaggedHCand_Xtt',
      'variable' : 'untaggedHCand_Xtt',
      'xtitle'   : "untaggedHCand_Xtt",
      'ytitle'   : 'events',
      'logY'     : False,
      'rebin'    : 2

},{#Untagged HCand Constituents Plots
      'name'     : 'untaggedHCand_leadJet_Pt',
      'variable' : 'untaggedHCand_leadJet_Pt_m',
      'xtitle'   : "untagged dijet lead jet pt",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
      'x_min'    : 20.0,
      'x_max'    : 700.0
},{
      'name'     : 'untaggedHCand_sublJet_Pt',
      'variable' : 'untaggedHCand_sublJet_Pt',
      'xtitle'   : "untagged dijet sublead jet pt",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
      'x_min'    : 20.0,
      'x_max'    : 350.0
},{
      'name'     : 'untaggedHCand_leadJet_Eta',
      'variable' : 'untaggedHCand_leadJet_Eta',
      'xtitle'   : "untagged dijet lead jet eta",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
},{
      'name'     : 'untaggedHCand_sublJet_Eta',
      'variable' : 'untaggedHCand_sublJet_Eta',
      'xtitle'   : "untagged dijet sublead jet eta",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
},{
      'name'     : 'untaggedHCand_leadJet_Phi',
      'variable' : 'untaggedHCand_leadJet_Phi',
      'xtitle'   : "untagged dijet lead jet phi",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
},{
      'name'     : 'untaggedHCand_sublJet_Phi',
      'variable' : 'untaggedHCand_sublJet_Phi',
      'xtitle'   : "untagged dijet sublead jet phi",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
},{
      'name'     : 'untaggedHCand_leadJet_MV2c20',
      'variable' : 'untaggedHCand_leadJet_MV2c20',
      'xtitle'   : "untagged dijet lead jet MV2c20",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,
},{
      'name'     : 'untaggedHCand_sublJet_MV2c20',
      'variable' : 'untaggedHCand_sublJet_MV2c20',
      'xtitle'   : "untagged dijet sublead jet MV2c20",
      'ytitle'   : 'Events',
      'logY'     : False,
      'rebin'    : 1,

},{#Plots of other jets
      'name'     : 'otherJets_Phi',
      'variable' : 'otherJets_Phi',
      'xtitle'   : "otherJets_Phi",
      'ytitle'   : 'Jets',
      'logY'     : False,
      'rebin'    : 4
},{
      'name'     : 'otherJets_Eta',
      'variable' : 'otherJets_Eta',
      'xtitle'   : "otherJets_Eta",
      'ytitle'   : 'Jets',
      'logY'     : False,
      'rebin'    : 4
},{
      'name'     : 'otherJets_Pt',
      'variable' : 'otherJets_Pt',
      'xtitle'   : "otherJets_Pt",
      'ytitle'   : 'Jets',
      'logY'     : True,
      'rebin'    : 4
},{
      'name'     : 'otherJets_Jvt',
      'variable' : 'otherJets_Jvt',
      'xtitle'   : "otherJets_Jvt",
      'ytitle'   : 'Jets',
      'logY'     : True,
      'rebin'    : 4
}
]


for reWeightStage in reWeightStages:
    for mass in massRegions.keys():
        for cut in cuts:
            for i in range(0,6):
                plot_configs[reWeightStage+cut+mass+str(i)] = {
                    "directory": "../../plots/resolved/reweightAfter"+reWeightStage+"/"+mass+"_00-01-04/"+cut+"/iter"+str(i)+"/",
                    "output": "test.root",
                    "ratio": True,
                    "lumi": lumi,
                    "autoRatio": False,
                    "systematics": False,
                    "data": False, #FIXME
                    "samples": samples[reWeightStage+cut+mass+str(i)],
                    "useTree": False,
                    "plots": plotsList
                    }

#
# 2D Plots
#

for reWeightStage in reWeightStages:
    for mass in massRegions:
        for cut in cuts.keys(): 
            for i in range(0,6):
                samples["2d"+reWeightStage+cut+mass+str(i)] = [ {
                                    'name'       : 'qcd',
                                    'is_data'    : True,
                                    'stack'      : False,
                                    'overlay'    : False,
                                    'path'       : '../../'+paths[reWeightStage][i]+'/hist-pbryant.root',
                                    'folderReg'  : massRegions[mass],
                                    'folderCuts' : cuts[cut],
                                    'folderTag'  : 'TwoTag_',
                                    'label'      : "QCD",
                                    'color'      : 'ROOT.kAzure-9',
                                    'rColor'     : 'ROOT.kRed-3',
                                    'weights'    : 1
                                   } ] 

plotsList2d = [ 
  {#Event Level Plots
      'name'     : 'm12m34',
      'variable' : 'm12m34',
      'xtitle'   : "m12 [GeV]",
      'ytitle'   : 'm34 [GeV]',
      'rebin'    : 1,
      'options'  : "COLZ",
      'canvSize' : [800,700],
      'rMargin'  : 0.12,
      'logY'     : False
}]

for reWeightStage in reWeightStages:
    for mass in massRegions.keys():
        for cut in cuts:
            for i in range(0,6):
                plot_configs["2d"+reWeightStage+cut+mass+str(i)] = {
                    "directory": "../../plots/resolved/reweightAfter"+reWeightStage+"/"+mass+"_00-01-04/"+cut+"/iter"+str(i)+"/",
                    "output": "test.root",
                    "ratio": False,
                    "lumi": lumi,
                    "autoRatio": False,
                    "systematics": False,
                    "data": False, #FIXME
                    "samples": samples["2d"+reWeightStage+cut+mass+str(i)],
                    "useTree": False,
                    "plots": plotsList2d
                    }


#
# CutFlow plots
#
samples["cutflow"] = [ {
                        'name'       : 'data',
                        'is_data'    : True,
                        'stack'      : False,
                        'overlay'    : False,
                        'path'       : '../../reWeightData0/hist-pbryant.root',
                        'folderReg'  : "",
                        'folderCuts' : "",
                        'folderTag'  : '',
                        'label'      : "",
                        'color'      : 'ROOT.kBlack',
                        'weights'    : 1
                     } ] 

cutflow = [ 
{
      'name'     : '4bRaw',
      'variable' : 'CutFlow4bRaw',
      'xtitle'   : "Cuts",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 1
},{
      'name'     : '4bWeighted',
      'variable' : 'CutFlow4bWeighted',
      'xtitle'   : "Cuts",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 1
},{
      'name'     : '2bRaw',
      'variable' : 'CutFlow2bRaw',
      'xtitle'   : "Cuts",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 1
},{
      'name'     : '2bWeighted',
      'variable' : 'CutFlow2bWeighted',
      'xtitle'   : "Cuts",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 1
},{
      'name'     : 'TriggersFailTrig',
      'variable' : 'TriggersFailTrig',
      'xtitle'   : "Triggers that fired when HLT_OR did not",
      'ytitle'   : 'Events',
      'logY'     : True,
      'rebin'    : 1
}
]


plot_configs["cutflow"] = {
                    "directory": "../../plots/resolved/cutflow/",
                    "output": "test.root",
                    "ratio": False,
                    "autoRatio": False,
                    "systematics": False,
                    "data": False, #FIXME
                    "lumi": lumi,
                    "samples": samples["cutflow"],
                    "useTree": False,
                    "plots": cutflow
                    }
