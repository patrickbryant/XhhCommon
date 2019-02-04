import ROOT
import OfficialAtlasStyle


import optparse
parser = optparse.OptionParser()
parser.add_option('-s', '--signalDir',           dest="signalDir",         default="", help="")
o, a = parser.parse_args()



inFiles = {
    300  :o.signalDir+"/_301488/hist-tree.root",
    500  :o.signalDir+"/_301490/hist-tree.root",
    600  :o.signalDir+"/_301491/hist-tree.root",
    700  :o.signalDir+"/_301492/hist-tree.root",
    800  :o.signalDir+"/_301493/hist-tree.root",
    900  :o.signalDir+"/_301494/hist-tree.root",
    1000 :o.signalDir+"/_301495/hist-tree.root",
    1100 :o.signalDir+"/_301496/hist-tree.root",
    1200 :o.signalDir+"/_301497/hist-tree.root",
}


def getGraph(mass_pts, color, style=ROOT.kSolid):
    gr = ROOT.TGraph(len(mass_pts))
    gr.SetLineWidth(3)
    gr.SetLineColor(color)
    gr.SetMarkerColor(color)
    gr.SetLineStyle(style)
    return gr

def doCut(cutName, mass_pts, region, prefix=""):

    trigs = [
        "HLT_2j35_bt_2j35"  ,
        "HLT_2j45_bm_2j45"  ,
        "HLT_j70_bm_3j70"   ,
        "HLT_j175_bm_j60_bm",
        "HLT_j100_2j55_bm"  ,
        "HLT_ht850"         ,
        "HLT_j225_bl"       ,

        ]
    

    colors = [ROOT.kGray+1, ROOT.kOrange,ROOT.kCyan,ROOT.kGreen,
              ROOT.kPink+10 ,ROOT.kOrange+10,  ROOT.kViolet-1,ROOT.kYellow,ROOT.kRed+2,ROOT.kOrange-8,
              ]    


    gSMTrigFull              = getGraph(mass_pts, ROOT.kBlack)
    gSMTrigs = {}
    for it in range(len(trigs)):
        gSMTrigs[trigs[it]] = getGraph(mass_pts, colors[it])


    g1p0     = getGraph(mass_pts, ROOT.kBlack,ROOT.kDotted)
    g0p95    = getGraph(mass_pts, ROOT.kBlack,ROOT.kDotted)
    g0p90    = getGraph(mass_pts, ROOT.kBlack,ROOT.kDotted)

    binNum = 0

    for i in mass_pts:

        thisFile = ROOT.TFile(inFiles[i],"READ")

        histMC         = thisFile.Get("TriggerMC")

        if region == "Signal":
            PassCuts       = histMC.GetBinContent(histMC    .GetXaxis().FindBin("AllSignal"))
        else:
            PassCuts       = histMC.GetBinContent(histMC    .GetXaxis().FindBin("All"))

        hPassTrig      = thisFile.Get("TTVetoFourTag_"+region+"/hCandDr")
        TrigOR         = hPassTrig.GetEntries()
        effTrigOR      = float(TrigOR)/PassCuts
        gSMTrigFull   .SetPoint(binNum,i,effTrigOR)

        g1p0 .SetPoint(binNum,i,1.0)
        g0p95.SetPoint(binNum,i,0.95)
        g0p90.SetPoint(binNum,i,0.9)


        for t in trigs:

            hPassTrig         = thisFile.Get(prefix+t+"FourTag_"+region+"/hCandDr")
            thisTrigCount     = hPassTrig.GetEntries()
            thisEffTrig       = float(thisTrigCount)/PassCuts
            gSMTrigs[t].SetPoint(binNum, i , thisEffTrig)

        
        thisFile.Close()
        binNum += 1

    leg = ROOT.TLegend(0,0,1.0,1.0)
    leg.SetFillColor(0)
    
    #
    #
    #
    can = ROOT.TCanvas(prefix+cutName+"_"+region,prefix+cutName+"_"+region)
    can.cd()
    gSMTrigFull .Draw("APL")
    if prefix == "Only_":
        gSMTrigFull.GetYaxis().SetRangeUser(0.0,0.05)
    else:
        gSMTrigFull.GetYaxis().SetRangeUser(0.0,1.1)
    gSMTrigFull.GetYaxis().SetTitle("Efficiency")
    gSMTrigFull.GetXaxis().SetTitle("Resonant Mass [GeV]")
    #gSMTrigFull      .Draw("PL")
    #gSMTrigThrsh.Draw("PL")
    #gSMNo2j65.Draw("PL")

    for t in trigs:
        gSMTrigs[t].Draw("PL")
        leg.AddEntry(gSMTrigs[t] , t, "PL")

    #gSMTrig5 .Draw("PL")
    #gSMTrig6 .Draw("PL")
    #gSMTrig7 .Draw("PL")
    g1p0 .Draw("L")
    g0p95.Draw("L")
    g0p90.Draw("L")
    can.Update()
    can.SaveAs(cutName+".pdf")


    canLeg = ROOT.TCanvas(cutName+"Leg",cutName+"Leg")    
    canLeg.cd()
    leg.Draw()
    canLeg.Update()
    canLeg.SaveAs(cutName+"Let.pdf")

    return can, g1p0, g0p90, g0p95, gSMTrigFull, gSMTrigs, leg, canLeg

#AllMassPts     = [300,500,600,700,800,900,1000,1100,1200]
AllMassPts_500 = [500,600,700,800,900,1000,1100,1200]

save = []
save += doCut("TestPassTrig",     AllMassPts_500)
#save += doCut("TestPassTrig",     AllMassPts_500, "Signal")
save += doCut("TestPassTrig",     AllMassPts_500,  "Only_")
#save += doCut("TestPassTrig",     AllMassPts_500, "Signal",      "Only_")
