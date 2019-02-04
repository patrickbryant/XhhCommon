import ROOT
from optparse import OptionParser
p = OptionParser()
p.add_option('--inFile',  type = 'string', default = "", dest = 'inputFileName', help = '' )
p.add_option('--outDir',  type = 'string', default = "", dest = 'output', help = '' )
(o,a) = p.parse_args()
import OfficialAtlasStyle

ROOT.gStyle.SetOptFit(1111)
inFile = ROOT.TFile(o.inputFileName,"READ")
ROOT.gROOT.SetBatch(True)

import os
if not os.path.isdir(o.output):
    os.mkdir(o.output)


def doVar(varName,min=None,max=None):
    hist = inFile.Get(varName)

    if not min == None:
        hist.GetXaxis().SetRangeUser(min,max)

    hist.GetYaxis().SetTitle("Weights")
    can = ROOT.TCanvas("can"+varName,"can"+varName)
    can.cd()
    hist.Draw()
    can.SaveAs(o.output+"/"+varName+".pdf")

doVar("leadHCand_Pt_m_2b_ratio")
doVar("hCandDr_2b_ratio")
doVar("sublHCand_dRjj_2b_ratio",0.2,1.6)


