import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
parser.add_option('-o', '--out',                dest="output",         default="", help="")
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
    canData = ROOT.TCanvas(dir+"_"+hName,dir+"_"+hName, 700,700)
    
    h_hist.GetXaxis().SetRangeUser(0,300)
    h_hist.GetXaxis().SetTitle("lead di-jet mass [GeV]")
    h_hist.GetYaxis().SetRangeUser(0,300)
    h_hist.GetYaxis().SetTitle("subleading di-jet mass [GeV]")

    h_hist.Draw("colz")
    #h_hist.Sumw2()
    canData.SaveAs(o.output+"/"+dir+"_"+hName+".pdf")
    gStyle.SetPadRightMargin(was)

    


plot2D("PassTrigTwoTag_Sideband","m12m34",dataFile)
plot2D("PassTrigTwoTag_Control","m12m34" ,dataFile)

             
