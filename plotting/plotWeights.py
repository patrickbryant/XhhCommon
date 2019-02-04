import ROOT
import OfficialAtlasStyle
ROOT.gROOT.SetBatch(True)

import optparse
parser = optparse.OptionParser()
parser.add_option('-i', '--inputDir',           dest="inputDir",         default="", help="")
parser.add_option('-o', '--outputDir',           dest="outputDir",         default=".", help="")
o, a = parser.parse_args()

import os
if not os.path.isdir(o.outputDir):
    os.mkdir(o.outputDir)



infile = ROOT.TFile(o.inputDir,"READ")
infile.ls()

#atlasstyle.SetOptFit(111)
ROOT.gStyle.SetOptFit(111)



def plotFit(name):
    hist = infile.Get(name)
    can = ROOT.TCanvas(name,name)
    hist.Draw()
    can.SaveAs(o.outputDir+"/"+name+".pdf")

plotFit("hCandDr_2b_ratio")
plotFit("leadHCand_Pt_m_2b_ratio")
plotFit("sublHCand_dRjj_2b_ratio")
plotFit("leadHCand_sublJet_Pt_2b_ratio")
