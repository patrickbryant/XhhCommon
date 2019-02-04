from helpers import parseOpts, plotterConfig, plot
import os
(opts,a) = parseOpts()

import ROOT, rootlogon
ROOT.gROOT.SetBatch(not opts.interactive)
#ROOT.gROOT.Macro("../post_processing/helpers.C")
#ROOT.gROOT.Macro("../post_processing/cross_sections.C")


#                                                                                                                                               
#  Executing the python                                                                                                                         
#   (configGlobals and configLocals are used to pass vars                                                                                       
#                                                                                                                                               
configGlobals = {}
configLocals  = {"inputDir"   :opts.inputDir,
                 "outputDir"  :opts.outputDir,
                 "data"       :opts.data,
                 "qcd"        :opts.qcd,
                 "ttbar"      :opts.ttbar,
                 "signal"     :opts.signal,
                 "weights"    :opts.weights,
                 "systematics":opts.systematics,
                 "mu_qcd"     :float(opts.mu_qcd),
                 "mu_ttbar"   :float(opts.mu_ttbar),
                 "lumi"       :opts.lumi}

print "Executing", opts.config

execfile(opts.config, configGlobals, configLocals)

#
# Loop on plotters
#
raw_plotters = opts.plotter.split(",")
plotters = {}
for raw_plotter in raw_plotters:
    plotters[raw_plotter] = plotterConfig(configLocals["plot_configs"][raw_plotter])



def chddir(plotter,dirName):
    if not os.path.isdir(dirName):
        os.mkdir(dirName)
    plotters[plotter]["directory"] = dirName

rebins = {}
rebins["m4j_l"] = [400,460,520,580,640,700,800,900,1000,1300,2000]#[100,140,180,220,260,300,340,380,420,460,500,540,600,660,720,800,900,1000,1240,2000] # for bins in 20
#rebins["m4j_l"] = [100, 138, 176, 214, 252, 290, 328, 366, 404, 442, 480, 518, 556, 594, 651, 708, 784, 879, 974, 1069, 1240, 2000]
rebins["m_4j"] = [200,250,300,350,400,450,500,550,600,650,700,800,900,1000,1250,2000,3000]
rebins["leadHCand_Pt_m"] = [180,200,220,240,260,280,300,340,380,420,500,600,700]#[100,200,220,240,260,280,300,320,340,360,380,400,440,500,750,1000]
rebins["sublHCand_Pt_m"] = [140,150,170,190,210,230,250,270,290,310,340,380,420,500,600,700]#[100,150,160,170,180,190,200,220,240,260,280,300,320,340,360,380,400,440,500,750,1000]
rebins["leadHCand_leadJet_Pt"] = [0,30,40,60,80,100,120,140,160,180,200,240,280,320,400,500]#[30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,275,300,325,350,375,400,425,450,475,500]
rebins["sublHCand_leadJet_Pt"] = rebins["leadHCand_leadJet_Pt"]
rebins["leadHCand_sublJet_Pt"] = rebins["leadHCand_leadJet_Pt"]
rebins["sublHCand_sublJet_Pt"] = rebins["leadHCand_leadJet_Pt"]
rebins["otherJets_Pt"] = rebins["leadHCand_leadJet_Pt"]

rebins["leadHCand_leadJet_Pt_m"] = [0,40,60,80,100,120,140,160,180,200,240,280,320,400,500,700]
rebins["leadHCand_sublJet_Pt_m"] = [0,40,60,80,100,120,140,160,180,200,240,280,320,400,500,700]
rebins["sublHCand_leadJet_Pt_m"] = rebins["leadHCand_leadJet_Pt_m"] 
rebins["sublHCand_sublJet_Pt_m"] = rebins["leadHCand_sublJet_Pt_m"] 
rebins["ht_l"] = 2
rebins["hCandDr"] = [2,2.5,2.75,3,3.25,3.5,3.75,4,4.5]
rebins["hCandDeta"] = 4
rebins["leadHCand_dRjj"]        = 4
rebins["sublHCand_dRjj"]        = 4

#
# Reverse ttbar bins
#
reverseTTBins = {}
reverseTTBins["sublHCand_leadJet_Pt"]  = [0,40,60,80,100,120,140,160,180,200,250,300,400,500]
reverseTTBins["leadHCand_leadJet_Pt"]  = reverseTTBins["sublHCand_leadJet_Pt"]
reverseTTBins["leadHCand_sublJet_Pt"]  = [0,40,60,80,100,125,150,175,200,250,300,400,500]
reverseTTBins["sublHCand_sublJet_Pt"]  = reverseTTBins["sublHCand_leadJet_Pt"]
reverseTTBins["leadHCand_Pt_m"]        = [100,150,200,250,300,350,400,500,600,700,800,900,1000]
reverseTTBins["sublHCand_leadJet_Eta"] = 8
reverseTTBins["sublHCand_sublJet_Eta"] = reverseTTBins["sublHCand_leadJet_Eta"] 
reverseTTBins["leadHCand_sublJet_Eta"] = reverseTTBins["sublHCand_leadJet_Eta"] 
reverseTTBins["leadHCand_leadJet_Eta"] = reverseTTBins["sublHCand_leadJet_Eta"] 
reverseTTBins["leadHCand_dRjj"]        = 8
reverseTTBins["leadHCand_Mass"]        = 4
reverseTTBins["sublHCand_Pt_m"]        = reverseTTBins["leadHCand_Pt_m"]
reverseTTBins["sublHCand_dRjj"]        = reverseTTBins["leadHCand_dRjj"]
reverseTTBins["sublHCand_Mass"]        = reverseTTBins["leadHCand_Mass"]



#
# PassTrig Binning
#
passTrigBins = {}
passTrigBins["leadHCand_Pt_m"] = [180,200,220,240,260,280,300,340,380,420,500,600,700]#[100,200,220,240,260,280,300,320,340,360,380,400,440,500,550,600,750,1000]
passTrigBins["sublHCand_Pt_m"] = [140,150,170,190,210,230,250,270,290,310,340,380,420,500,600,700]#[100,150,160,170,180,190,200,220,240,260,280,300,320,340,360,380,400,440,500,600,750,1000]

passTrigBins["leadHCand_leadJet_Pt"] = [20,50,70,90,110,130,150,170,190,210,230,250,275,300,325,350,375,400,425,450,500]
passTrigBins["leadHCand_sublJet_Pt"] = [30,40,60,80,100,120,140,160,180,200,230,250,275,300,325,350,375,400,425,450,500]
passTrigBins["sublHCand_leadJet_Pt"] = passTrigBins["leadHCand_leadJet_Pt"] 
passTrigBins["sublHCand_sublJet_Pt"] = passTrigBins["leadHCand_sublJet_Pt"] 



#
# PassM4j Binning
#
passM4jDep = {}
passM4jDep["leadHCand_Pt_m"] = [180,200,220,240,260,280,300,340,380,420,500,600,700]#[100,200,220,240,260,280,300,320,340,360,380,400,440,500,550,600,750,1000]
passM4jDep["sublHCand_Pt_m"] = [140,150,170,190,210,230,250,270,290,310,340,380,420,500,600,700]#[100,150,170,190,210,230,250,270,290,310,330,350,400,450,500,600,750,1000]
passM4jDep["leadHCand_leadJet_Pt"] = [0,40,60,80,100,120,140,160,180,200,240,280,320,400,500,700]#[20,50,70,90,110,130,150,170,190,210,230,250,275,300,325,350,375,400,425,450,500]
passM4jDep["leadHCand_sublJet_Pt"] = [0,40,60,80,100,120,140,160,180,200,240,280,320,400,500,700]#[30,40,60,80,100,120,140,160,180,200,230,250,275,300,325,350,375,400,425,450,500]
passM4jDep["sublHCand_leadJet_Pt"] = passTrigBins["leadHCand_leadJet_Pt"] 
passM4jDep["sublHCand_sublJet_Pt"] = passTrigBins["leadHCand_sublJet_Pt"] 


selectionRebins = {}
selectionRebins["ReverseTTVeto"] = reverseTTBins
selectionRebins["PassM4jDep"]    = passM4jDep
selectionRebins["PassTrig"]      = passTrigBins



def doRebin(hname, default, selection=""):


    if selection:
        if selection in selectionRebins:
            thisRebins = selectionRebins[selection]
            if hname in thisRebins:
                return thisRebins[hname]

    if hname in rebins:
        return rebins[hname]
    return default

#
#  Make HCandPlots
#
def makeJetPlots(jetName, selection, region, noLog=False):

    doLog = not noLog
    plot(jetName+"_Pt",    selection,region,plotters["main"],logY=doLog,rebin=doRebin(jetName+"_Pt",2,selection), x_min=30, ytitle = "Entries/5 GeV",y_min=0.1)
    plot(jetName+"_Pt_m",    selection,region,plotters["main"],logY=doLog,rebin=doRebin(jetName+"_Pt_m",2,selection), x_min=30, ytitle = "Entries/5 GeV",y_min=0.1)
    plot(jetName+"_MV2c20",selection,region,plotters["main"],logY=doLog,rebin=4)
    plot(jetName+"_Jvt",   selection,region,plotters["main"],logY=doLog,rebin=4)

    plot(jetName+"_Eta",   selection,region,plotters["main"],logY=0,rebin=doRebin(jetName+"_Eta",4,selection))
    plot(jetName+"_Phi",   selection,region,plotters["main"],logY=0,rebin=4)



#
#  Make HCandPlots
#
def makeHCandPlots(hcandName, selection, region, noLog=False):
    doLog = not noLog
    plot(hcandName+"_Pt_m",  selection,region,plotters["main"],logY=doLog ,rebin=doRebin(hcandName+"_Pt_m",2,selection), x_min=100, ytitle = "Entries/10 GeV",y_min=0.1)
    plot(hcandName+"_Eta",   selection,region,plotters["main"],logY=0,rebin=4)
    plot(hcandName+"_Phi",   selection,region,plotters["main"],logY=0,rebin=4)
    plot(hcandName+"_Mass",  selection,region,plotters["main"],logY=0,rebin=doRebin(hcandName+"_Mass",2,selection), x_max=300)
    plot(hcandName+"_dRjj",  selection,region,plotters["main"],logY=0,rebin=doRebin(hcandName+"_dRjj",1,selection), x_max=1.8,x_min=0.2)
    plot(hcandName+"_mW",    selection,region,plotters["main"],logY=0,rebin=4)
    plot(hcandName+"_mTop",  selection,region,plotters["main"],logY=0,rebin=4)
    plot(hcandName+"_Xtt",   selection,region,plotters["main"],logY=0,rebin=4)
    plot(hcandName+"_nTags", selection,region,plotters["main"],logY=0,rebin=1)

    makeJetPlots(hcandName+"_leadJet",selection, region, noLog=noLog) 
    makeJetPlots(hcandName+"_sublJet",selection, region, noLog=noLog) 

def makeCut(region, selection,  noLog = False): 
    chddir("main",opts.outputDir+"/"+region)
    chddir("main",opts.outputDir+"/"+region+"/"+selection)
    chddir("main",opts.outputDir+"/"+region+"/"+selection+"/iter"+opts.iteration)

    makeHCandPlots("leadHCand", selection, region, noLog=noLog)
    makeHCandPlots("sublHCand", selection, region, noLog=noLog)

    makeJetPlots("otherJets", selection, region, noLog=noLog)
    
    plot("NPV",       selection, region, plotters["main"],logY=0,rebin=1)
    plot("mu_ave",    selection, region, plotters["main"],logY=0,rebin=1)
    #plot("mu_act",    selection, region, plotters["main"],logY=0,rebin=1)
    plot("nJetOther", selection, region, plotters["main"],logY=0,rebin=1)

    plot("m4j",       selection, region, plotters["main"],logY=0,rebin=3)
    plot("m4j_l",     selection, region, plotters["main"],logY=0,rebin=doRebin("m4j_l",3,selection), x_min=100, ytitle = "Entries/20 GeV")
    plot("m4j_l",     selection, region, plotters["main"],logY=1,rebin=doRebin("m4j_l",3,selection), x_min=100, ytitle = "Entries/20 GeV")

    plot("m4j_cor",       selection, region, plotters["main"],logY=0,rebin=3)
    plot("m4j_cor_l",     selection, region, plotters["main"],logY=0,rebin=doRebin("m4j_l",3,selection), x_min=100, ytitle = "Entries/20 GeV")
    plot("m4j_cor_l",     selection, region, plotters["main"],logY=1,rebin=doRebin("m4j_l",3,selection), x_min=100, ytitle = "Entries/20 GeV")

    #plot("sumHCandPt",        selection, region, plotters["main"],logY=0,rebin=1)
    #plot("HtOverM4j",         selection, region, plotters["main"],logY=0,rebin=1)
    #plot("sumHCandPtOverM4j", selection, region, plotters["main"],logY=0,rebin=1)
    plot("ht_l",              selection, region, plotters["main"],logY=0,rebin=doRebin("ht_l",2,selection))
    #plot("m4j_l",     selection, region, plotters["main"],logY=0,rebin=3)
    plot("hCandDeta", selection, region, plotters["main"],logY=0,rebin=doRebin("hCandDeta",2,selection))
    plot("hCandDphi", selection, region, plotters["main"],logY=0,rebin=4)
    plot("hCandDr",   selection, region, plotters["main"],logY=0,rebin=doRebin("hCandDr",4,selection),x_min=1)



def makeRegion(region):
    if "Signal" in region: noLog = True
    else: noLog = False
    makeCut(region,  "PassTrig",      noLog)
    makeCut(region,  "TTVeto",        noLog)

    if not region == "SignalZZ":
        makeCut(region,  "PassLeadPt",    noLog)
        makeCut(region,  "PassSublPt",    noLog)
        makeCut(region,  "PassM4jDep",    noLog)
        makeCut(region,  "ReverseTTVeto", noLog)

    #makeCut(region,  "TTVetoM720to900", noLog)
    #makeCut(region, "HLT_2j35_btight_2j35_L13J25")
    #makeCut(region, "HLT_2j45_bmedium_2j45_L13J25")
    #makeCut(region, "HLT_j65_btight_3j65_L13J25")
    #makeCut(region, "HLT_j100_2j55_bmedium")
    #makeCut(region, "HLT_j225_bloose")


def doTrigStudy(region):
    if "Signal" in region: noLog = True
    else: noLog = False
    #trigList = ["HLT_2j35_bt_2j35","HLT_j100_2j55_bm","HLT_j225_bl","HLT_ht850"]
    #trigList = ["HLT_2j35_bt_2j35","HLT_j100_2j55_bm","HLT_j225_bl"]
    trigList = []
    for t in trigList:
        makeCut(region,  t,              noLog)
        #makeCut(region,  "Only_"+t,      noLog)


#chddir(opts.outputDir)
#makeCut("PassTrig")
#makeCut("PassM4jDep")
#makeCut("TTVeto")
#makeCut("HLT_2j35_btight_2j35_L13J25")
#makeCut("HLT_2j45_bmedium_2j45_L13J25")
#makeCut("HLT_j65_btight_3j65_L13J25")
#makeCut("HLT_j100_2j55_bmedium")
#makeCut("HLT_j225_bloose")

if "main" in raw_plotters:
    chddir("main",opts.outputDir)

    
    #makeRegion("SignalZZ")        


    makeRegion("Sideband")
    makeRegion("Control")
    makeRegion("Signal")


    doTrigStudy("Sideband")
    doTrigStudy("Control")

#
# Others plots. Cutflows and mass planes
#

def makeCutFlow(sample,cutflow):
    chddir(sample, opts.outputDir+"/cutflow")

    plot("CutFlow"+cutflow, "", "", plotters[sample],logY=0,rebin=1)

if "cutflow" in raw_plotters:
    makeCutFlow("cutflow","4bRaw")
    makeCutFlow("cutflow","4bWeighted")
    makeCutFlow("cutflow","2bRaw")
    makeCutFlow("cutflow","2bWeighted")

if "cutflowttbar" in raw_plotters:
    makeCutFlow("cutflowttbar","4bRaw")
    makeCutFlow("cutflowttbar","4bWeighted")
    makeCutFlow("cutflowttbar","2bRaw")
    makeCutFlow("cutflowttbar","2bWeighted")

def makeMassPlane(selection,region):
    chddir("2d",opts.outputDir+"/"+region)
    chddir("2d",opts.outputDir+"/"+region+"/"+selection)
    chddir("2d",opts.outputDir+"/"+region+"/"+selection+"/"+"iter"+opts.iteration)

    plot("m12m34",selection,region,plotters["2d"],logY=0,rebin=1,xtitle = "m12 [GeV]",ytitle = "m34 [GeV]", options = "COLZ", canvSize = [800,700],rMargin=0.12)

if "2d" in raw_plotters:
    makeMassPlane("PassTrig","Sideband")
    makeMassPlane("PassTrig","Control")
    makeMassPlane("PassTrig","Signal")

if "weights" in raw_plotters:
    plot("hCandDr",   "", "", plotters["weights"],logY=0,rebin=8,x_min=1.5,x_max=5,y_min=0,y_max=4,function='fit_hCandDr',ytitle='Ratio 4b to 2b')

if "sensitivity" in raw_plotters:
    plot("Sensitivity", "", "", plotters["sensitivity"],logY=0)

if "systematics" in raw_plotters:
    #plot("dataOverQCDinControl", "", "", plotters["systematics"],logY=0,x_min=400,x_max=2000,y_min=0,y_max=4,function=["fit","fitUp","fitDown"],rebin=doRebin("m_4j",3),ytitle="data/QCD")
    plot("dataOverQCDinControl", "", "", plotters["systematics"],logY=0,x_min=400,x_max=2000,y_min=0,y_max=4,function=["fit","fitUp","fitDown"],rebin=doRebin("m4j_l",3),ytitle="data/QCD")

    plotters["QCDShapeUp"] = plotterConfig(configLocals["plot_configs"]["QCDShapeUp"])
    plot(["qcd_hh","qcd_hh_QCDShapeUp"], "", "", plotters["QCDShapeUp"],logY=0,x_min=400,x_max=2000,y_min=0,y_max=15,rebin=doRebin("m_4j",3),ytitle="Events/50 GeV")

    plotters["QCDShapeDown"] = plotterConfig(configLocals["plot_configs"]["QCDShapeDown"])
    plot(["qcd_hh","qcd_hh_QCDShapeDown"], "", "", plotters["QCDShapeDown"],logY=0,x_min=400,x_max=2000,y_min=0,y_max=15,rebin=doRebin("m_4j",3),ytitle="Events/50 GeV")


if "systematics" in raw_plotters:
    #plot("dataOverQCDinControl", "", "", plotters["systematics"],logY=0,x_min=400,x_max=2000,y_min=0,y_max=4,function=["fit","fitUp","fitDown"],rebin=doRebin("m_4j",3),ytitle="data/QCD")
    
    plot("dataOverQCDinControl", "", "", plotters["systematics"],logY=0,x_min=400,x_max=2000,y_min=0,y_max=4,function=["fit","fitUp","fitDown"],rebin=doRebin("m4j_l",3),ytitle="data/QCD")

    plotters["QCDShapeUp"] = plotterConfig(configLocals["plot_configs"]["QCDShapeUp"])
    plot(["qcd_hh","qcd_hh_QCDShapeUp"], "", "", plotters["QCDShapeUp"],logY=0,x_min=400,x_max=2000,y_min=0,y_max=15,rebin=doRebin("m_4j",3),ytitle="Events/50 GeV")

    plotters["QCDShapeDown"] = plotterConfig(configLocals["plot_configs"]["QCDShapeDown"])
    plot(["qcd_hh","qcd_hh_QCDShapeDown"], "", "", plotters["QCDShapeDown"],logY=0,x_min=400,x_max=2000,y_min=0,y_max=15,rebin=doRebin("m_4j",3),ytitle="Events/50 GeV")

