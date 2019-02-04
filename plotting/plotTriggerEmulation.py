import ROOT
import OfficialAtlasStyle


import optparse
parser = optparse.OptionParser()
parser.add_option('-s', '--signalDir',           dest="signalDir",         default="", help="")
parser.add_option('-o', '--outputDir',           dest="outputDir",         default=".", help="")
parser.add_option('--add_j175',        action="store_true",          dest="add_j175",          default=False, help="")
parser.add_option('--add_j70',         action="store_true",          dest="add_j70",           default=False, help="")
parser.add_option('--add_2j45',        action="store_true",          dest="add_2j45",           default=False, help="")
o, a = parser.parse_args()

ROOT.gROOT.SetBatch(True)

import os
if not os.path.isdir(o.outputDir):
    os.mkdir(o.outputDir)


inFiles = {
#    300  :o.signalDir+"/_301488/hist-tree.root",
#    500  :o.signalDir+"/_301490/hist-tree.root",
#    600  :o.signalDir+"/_301491/hist-tree.root",
#    700  :o.signalDir+"/_301492/hist-tree.root",
#    800  :o.signalDir+"/_301493/hist-tree.root",
#    900  :o.signalDir+"/_301494/hist-tree.root",
#    1000 :o.signalDir+"/_301495/hist-tree.root",
#    1100 :o.signalDir+"/_301496/hist-tree.root",
#    1200 :o.signalDir+"/_301497/hist-tree.root",

    300  :o.signalDir+"/RSG_c10_M300/hist-tree.root",
    400  :o.signalDir+"/RSG_c10_M400/hist-tree.root",
    500  :o.signalDir+"/RSG_c10_M500/hist-tree.root",
    600  :o.signalDir+"/RSG_c10_M600/hist-tree.root",
    700  :o.signalDir+"/RSG_c10_M700/hist-tree.root",
    800  :o.signalDir+"/RSG_c10_M800/hist-tree.root",
    900  :o.signalDir+"/RSG_c10_M900/hist-tree.root",
    1000 :o.signalDir+"/RSG_c10_M1000/hist-tree.root",
    1100 :o.signalDir+"/RSG_c10_M1100/hist-tree.root",
    1200 :o.signalDir+"/RSG_c10_M1200/hist-tree.root",

}


def getGraph(mass_pts, color, style=ROOT.kSolid):
    gr = ROOT.TGraph(len(mass_pts))
    gr.SetLineWidth(3)
    gr.SetLineColor(color)
    gr.SetMarkerColor(color)
    gr.SetLineStyle(style)
    return gr

def doCut(cutName, mass_pts, prefix=""):

    trigs = [
        "HLT_2j35_btight_2j35_L13J25_0ETA23",
        "HLT_j100_2j55_bmedium",
        #"HLT_ht850",
        "HLT_j225_bloose",
        ]

    if o.add_2j45:
        trigs += ["HLT_2j45_bmedium_2j45_L13J25_0ETA23"]


    if o.add_j70:
        trigs += ["HLT_2j45_bmedium_2j45_L13J25_0ETA23",
                  "HLT_j70_bmedium_3j70_L13J25_0ETA23",]       

    if o.add_j175:
        trigs += ["HLT_2j45_bmedium_2j45_L13J25_0ETA23",
                  "HLT_j70_bmedium_3j70_L13J25_0ETA23",
                  "HLT_j175_bmedium_j60_bmedium",]
                  

    

    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray+1, 
              ROOT.kPink+10 ,ROOT.kCyan, ROOT.kViolet-1,ROOT.kYellow,ROOT.kRed+2,ROOT.kOrange-8,
              ]    


    gSMTrigFull              = getGraph(mass_pts, ROOT.kBlack)
    gSMTrigFullMCEMulation   = getGraph(mass_pts, ROOT.kBlack)
    gSMTrigFullDataEMulation = getGraph(mass_pts, ROOT.kBlack)

    gSMTrigs = {}
    for it in range(len(trigs)):
        gSMTrigs[trigs[it]] = getGraph(mass_pts, colors[it])

    gSMTrigsMCEMulation = {}
    for it in range(len(trigs)):
        gSMTrigsMCEMulation[trigs[it]] = getGraph(mass_pts, colors[it])

    gSMTrigsNonClosure = {}
    for it in range(len(trigs)):
        gSMTrigsNonClosure[trigs[it]] = getGraph(mass_pts, colors[it])

    gSMTrigsDataEMulation = {}
    for it in range(len(trigs)):
        gSMTrigsDataEMulation[trigs[it]] = getGraph(mass_pts, colors[it])


    g1p0     = getGraph(mass_pts, ROOT.kBlack,ROOT.kDotted)
    g0p95    = getGraph(mass_pts, ROOT.kBlack,ROOT.kDotted)
    g0p90    = getGraph(mass_pts, ROOT.kBlack,ROOT.kDotted)

    binNum = 0

    for i in mass_pts:

        thisFile = ROOT.TFile(inFiles[i],"READ")

        histMC         = thisFile.Get("TriggerMC")
        histMCEm       = thisFile.Get("TriggerMCEmulation")
        histDataEm     = thisFile.Get("TriggerDataEmulation")

        if prefix == "Only_":
            PassCuts       = histMC.GetBinContent(histMC    .GetXaxis().FindBin("All"))
            PassCutsMCEM   = histMC.GetBinContent(histMCEm  .GetXaxis().FindBin("All"))
            PassCutsDataEM = histMC.GetBinContent(histDataEm.GetXaxis().FindBin("All"))
        else:
            PassCuts       = histMC.GetBinContent(histMC    .GetXaxis().FindBin("All"))
            PassCutsMCEM   = histMC.GetBinContent(histMCEm  .GetXaxis().FindBin("All"))
            PassCutsDataEM = histMC.GetBinContent(histDataEm.GetXaxis().FindBin("All"))

        TrigOR         = histMC    .GetBinContent(histMC    .GetXaxis().FindBin("TriggerOR"))
        TrigORMCEM     = histMCEm  .GetBinContent(histMCEm  .GetXaxis().FindBin("TriggerOR"))
        TrigORDataEM   = histDataEm.GetBinContent(histDataEm.GetXaxis().FindBin("TriggerOR"))

        for t in trigs:
            thisTrigCount = histMC.GetBinContent(histMC.GetXaxis().FindBin(prefix+t))
            thisEffTrig   = float(thisTrigCount)/PassCuts
            gSMTrigs[t].SetPoint(binNum, i , thisEffTrig)

            thisTrigCountMCEm = histMCEm.GetBinContent(histMCEm.GetXaxis().FindBin(prefix+t))
            thisEffTrigMCEm   = float(thisTrigCountMCEm)/PassCutsMCEM
            gSMTrigsMCEMulation[t].SetPoint(binNum, i , thisEffTrigMCEm)

            if thisEffTrig:
                gSMTrigsNonClosure[t].SetPoint(binNum, i, (thisEffTrigMCEm-thisEffTrig)/thisEffTrig)
            else:
                gSMTrigsNonClosure[t].SetPoint(binNum, i, 1.0)
            thisTrigCountDataEm = histDataEm.GetBinContent(histDataEm.GetXaxis().FindBin(prefix+t))
            thisEffTrigDataEm   = float(thisTrigCountDataEm)/PassCutsDataEM
            gSMTrigsDataEMulation[t].SetPoint(binNum, i , thisEffTrigDataEm)


        effTrigOR         = float(TrigOR)/PassCuts
        gSMTrigFull   .SetPoint(binNum,i,effTrigOR)

        effTrigORMCEm     = float(TrigORMCEM)/PassCutsMCEM
        gSMTrigFullMCEMulation   .SetPoint(binNum,i,effTrigORMCEm)

        effTrigORDataEm   = float(TrigORDataEM)/PassCutsDataEM
        gSMTrigFullDataEMulation   .SetPoint(binNum,i,effTrigORDataEm)

        g1p0 .SetPoint(binNum,i,1.0)
        g0p95.SetPoint(binNum,i,0.95)
        g0p90.SetPoint(binNum,i,0.9)
        
        thisFile.Close()
        binNum += 1
    
    can = ROOT.TCanvas(prefix+cutName,prefix+cutName)
    can.cd()
    gSMTrigFull .Draw("APL")
    if prefix == "Only_":
        gSMTrigFull.GetYaxis().SetRangeUser(0.0,0.15)
    else:
        gSMTrigFull.GetYaxis().SetRangeUser(0.0,1.1)
    gSMTrigFull.GetYaxis().SetTitle("Efficiency")
    gSMTrigFull.GetXaxis().SetTitle("Resonant Mass [GeV]")
    #gSMTrigFull      .Draw("PL")
    #gSMTrigThrsh.Draw("PL")
    #gSMNo2j65.Draw("PL")


    for t in trigs:
        gSMTrigs[t].Draw("PL")


    #gSMTrig5 .Draw("PL")
    #gSMTrig6 .Draw("PL")
    #gSMTrig7 .Draw("PL")
    g1p0 .Draw("L")
    g0p95.Draw("L")
    g0p90.Draw("L")
    can.Update()
    can.SaveAs(o.outputDir+"/"+prefix+cutName+".pdf")


    leg = ROOT.TLegend(0,0,1.0,1.0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    #
    #  MC EM
    #
    canMCEM = ROOT.TCanvas(prefix+cutName+"MCEMulation",prefix+cutName+"MCEMulation")
    canMCEM.cd()
    gSMTrigFullMCEMulation .Draw("APL")
    if prefix == "Only_":
        gSMTrigFullMCEMulation.GetYaxis().SetRangeUser(0.0,0.15)
    else:
        gSMTrigFullMCEMulation.GetYaxis().SetRangeUser(0.0,1.1)
    gSMTrigFullMCEMulation.GetYaxis().SetTitle("Efficiency")
    gSMTrigFullMCEMulation.GetXaxis().SetTitle("Resonant Mass [GeV]")

    leg.AddEntry(gSMTrigFullMCEMulation , "Combined OR", "PL")

    for t in trigs:
        gSMTrigsMCEMulation[t].Draw("PL")
        leg.AddEntry(gSMTrigsMCEMulation[t] , t, "PL")


    g1p0 .Draw("L")
    g0p95.Draw("L")
    g0p90.Draw("L")
    canMCEM.Update()
    canMCEM.SaveAs(o.outputDir+"/"+prefix+cutName+"MCEmulation.pdf")


    #
    #  MC Non-closure
    #
    canMCNonClosure = ROOT.TCanvas(prefix+cutName+"MCNonClosure",prefix+cutName+"MCNonClosure")
    canMCNonClosure.cd()

    didFirst = False
    for t in trigs:
        if not didFirst:
            didFirst = True
            gSMTrigsNonClosure[t] .Draw("APL")
            gSMTrigsNonClosure[t].GetYaxis().SetRangeUser(-0.5,0.5)
            gSMTrigsNonClosure[t].GetYaxis().SetTitle("MC Non-Closure")
            gSMTrigsNonClosure[t].GetXaxis().SetTitle("Resonant Mass [GeV]")
        else:
            gSMTrigsNonClosure[t].Draw("PL")

    canMCNonClosure.Update()
    canMCNonClosure.SaveAs(o.outputDir+"/"+prefix+cutName+"MCNonClosure.pdf")


    #
    #  Data EM
    #
    canDataEM = ROOT.TCanvas(prefix+cutName+"DataEMulation",prefix+cutName+"DataEMulation")
    canDataEM.cd()
    gSMTrigFullDataEMulation .Draw("APL")
    if prefix == "Only_":
        gSMTrigFullDataEMulation.GetYaxis().SetRangeUser(0.0,0.15)
    else:
        gSMTrigFullDataEMulation.GetYaxis().SetRangeUser(0.0,1.1)
    gSMTrigFullDataEMulation.GetYaxis().SetTitle("Efficiency")
    gSMTrigFullDataEMulation.GetXaxis().SetTitle("Resonant Mass [GeV]")

    for t in trigs:
        gSMTrigsDataEMulation[t].Draw("PL")
    gSMTrigFullDataEMulation .Draw("PL")
    g1p0 .Draw("L")
    g0p95.Draw("L")
    g0p90.Draw("L")
    canDataEM.Update()
    canDataEM.SaveAs(o.outputDir+"/"+prefix+cutName+"DataEmulation.pdf")



    canLeg = ROOT.TCanvas(cutName+"Leg",cutName+"Leg")    
    canLeg.cd()
    leg.Draw()
    canLeg.Update()
    canLeg.SaveAs(o.outputDir+"/"+cutName+"Let.pdf")

    return can, g1p0, g0p90, g0p95, gSMTrigFull, gSMTrigs, gSMTrigsMCEMulation, gSMTrigFullMCEMulation, gSMTrigsDataEMulation, gSMTrigFullDataEMulation, leg, canLeg, canMCNonClosure, gSMTrigsNonClosure

#AllMassPts_500     = [300,500,600,700,800,900,1000,1100,1200]
AllMassPts_500 = [500,600,700,800,900,1000,1100,1200]

save = []
save += doCut("PassTrig",     AllMassPts_500)
save += doCut("PassTrig",     AllMassPts_500, "Only_")
