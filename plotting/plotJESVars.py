import optparse
parser = optparse.OptionParser()
parser.add_option('-o', '--out',                dest="output",               default="", help="")
parser.add_option('-i', '--in',                 dest="inputDir",             default="", help="")
o, a = parser.parse_args()
import ROOT
import OfficialAtlasStyle

ROOT.gROOT.SetBatch(True)

from   ROOTCore.CanvasOptions import CanvasOptions 
from   ROOTCore.Plotting      import plot_hists_wratio, plot_hists
from   ROOTCore.Utils         import make_legend

import os
if not os.path.isdir(o.output):
    os.mkdir(o.output)


def doVar(var, dir, nomFile, sysFiles, sample, rebin=0):

    #
    # Get Hists
    #
    hNom = nomFile.Get(dir+"/"+var)
    if rebin: hNom.Rebin(rebin)
    hSys = []
    for sys in sysFiles:    
        hSys.append(sys.Get(dir+"/"+var))
        if rebin: hSys[-1].Rebin(rebin)

    hUpTotal   = ROOT.TH1F(hNom)
    hUpTotal    .SetName(hNom.GetName()+"_sysUp")
    hUpTotal    .SetLineColor(ROOT.kRed)
    hUpTotal    .SetMarkerColor(ROOT.kRed)
    hDownTotal = ROOT.TH1F(hNom)
    hDownTotal  .SetName(hNom.GetName()+"_sysDown")
    hDownTotal  .SetLineColor(ROOT.kBlue)
    hDownTotal  .SetMarkerColor(ROOT.kBlue)

    for iBin in range(hNom.GetNbinsX()+1):
        upTotal2   = 0
        downTotal2 = 0
        nomValue  = hNom.GetBinContent(iBin)

        for hS in hSys:   
            upDiff  = hS.GetBinContent(iBin) - nomValue
            if upDiff > 0:
                upTotal2    += (upDiff * upDiff)
            else:
                downTotal2  += (upDiff * upDiff)

        hUpTotal  .SetBinContent(iBin, nomValue + pow(upTotal2,  0.5))
        hDownTotal.SetBinContent(iBin, nomValue - pow(downTotal2,0.5))

    can_opts = CanvasOptions()
    thePlot = plot_hists([hUpTotal, hNom,hDownTotal],
                         "Test_stack",
                         canvas_options = can_opts,
                         draw_options  = ["PE","hist","PE"],
                         line_colors   = [ROOT.kBlack, ROOT.kBlack, ROOT.kRed],
                         )

    legend_limits={ 'width' : 0.30, 'height' : 0.05, 'x2' : 1.0, 'y2' : 0.92 }
    thePlot['leg'] = make_legend(hists = [hUpTotal,hNom,hDownTotal],
                                 labels = ["+1 #sigma JES","Nominal","-1 #sigma JES"],
                                 draw_options  = ["PE","hist","PE"],
                                 width = legend_limits['width'], 
                                 height= legend_limits['height'],
                                 x2=legend_limits['x2'],
                                 y2=legend_limits['y2'],
                                 )


    thePlot['leg'].Draw()



    
    thePlot["canvas"].SaveAs(o.output+"/"+sample+"_"+var+".pdf")

    #can = ROOT.TCanvas("test","test")
    #can.cd()
    #hUpTotal.Draw("")
    #hNom.Draw("same")
    #hUpTotal.Draw("same")
    #hDownTotal.Draw("same")
    #can.SaveAs(o.output+"/"+sample+"_"+var+".pdf")
    return
        




def doMassPt(massPt):

    sysVals = [
        "XhhMiniNtupleResolved_JET_GroupedNP_1__1up/"  ,
        "XhhMiniNtupleResolved_JET_GroupedNP_2__1up/"  ,
        "XhhMiniNtupleResolved_JET_GroupedNP_3__1up/"  ,
        "XhhMiniNtupleResolved_JET_GroupedNP_1__1down/",
        "XhhMiniNtupleResolved_JET_GroupedNP_2__1down/",
        "XhhMiniNtupleResolved_JET_GroupedNP_3__1down/",
        ]

    
    #
    #  Get Files
    #
    nominalFile = ROOT.TFile(o.inputDir+"/histsSignal/"+massPt+"/hist-tree.root","READ")
    sysFiles = []
    for sys in sysVals:   sysFiles.append(ROOT.TFile(o.inputDir+"/histsSignal/"+sys+"/"+massPt+"/hist-tree.root","READ"))

    #
    #  Make Plots
    #
    doVar("m4j",           "TTVetoFourTag_Signal",   nominalFile, sysFiles, massPt, rebin=2 )
    doVar("m4j_l",         "TTVetoFourTag_Signal",   nominalFile, sysFiles, massPt, rebin=2 )
    doVar("leadHCand_Mass","TTVetoFourTag_Inclusive",nominalFile, sysFiles, massPt, rebin=2 )
    doVar("sublHCand_Mass","TTVetoFourTag_Inclusive",nominalFile, sysFiles, massPt, rebin=2 )

    #
    #  Close Files
    #
    nominalFile.Close()
    for sysFile in sysFiles: sysFile.Close()

    return 
    




def main():

    signalSubDirs = [
        "RSG_c10_M500","RSG_c10_M1000","RSG_c10_M1200"
        ]
    
    for sig in signalSubDirs:
        doMassPt(sig)


if __name__ == "__main__":
    main()
