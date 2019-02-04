import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',          dest="dataFileName",         default="", help="")
parser.add_option('-o', '--out',                dest="output",         default="", help="")
parser.add_option(      '--max',                dest="zmax",         default="25", help="")
o, a = parser.parse_args()

import os

#
#
#
import OfficialAtlasStyle
import ROOT
from ROOT import gStyle                                                                                                                             
gStyle.SetPalette(1)
ROOT.gROOT.SetBatch(1)

if not os.path.isdir(o.output):
    os.mkdir(o.output)


dataFile = ROOT.TFile(o.dataFileName,"READ")

def normHist(hist):
    hist.Scale(1./hist.Integral())
    return hist


def plot2D(dir,hName,rootfile):
    was = gStyle.GetPadRightMargin()
    gStyle.SetPadRightMargin(0.15) 
    h_hist = rootfile.Get(dir+"/"+hName)
    print dir+"/"+hName
    canData = ROOT.TCanvas(dir+"_"+hName+"_data",dir+"_"+hName+"_data",700,700)
    #canData.SetLogz(1)
    #h_hist.Rebin2D(2,2)
    h_hist.GetZaxis().SetRangeUser(0,float(o.zmax))
    h_hist.GetXaxis().SetRangeUser(0,300)
    h_hist.GetXaxis().SetTitle("lead di-jet mass [GeV]")
    h_hist.GetYaxis().SetRangeUser(0,300)
    h_hist.GetYaxis().SetTitle("subleading di-jet mass [GeV]")

    #h_hist.GetZaxis().SetRangeUser(0,12)
    h_hist.Draw("colz")
    #h_hist.Sumw2()
    canData.SaveAs(o.output+"/"+dir+"_"+hName+".pdf")
    gStyle.SetPadRightMargin(was)


plot2D("ReverseTTVetoTwoTag_Control", "m12m34",dataFile)
plot2D("ReverseTTVetoTwoTag_Sideband","m12m34",dataFile)

             
