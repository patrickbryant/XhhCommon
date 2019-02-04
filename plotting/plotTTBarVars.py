import optparse
parser = optparse.OptionParser()
parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",         default="", help="")
parser.add_option('--m500',                     dest="m500FileName",         default="", help="")
parser.add_option('--m1000',                    dest="m1000FileName",         default="", help="")
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


ttbarFile = ROOT.TFile(o.ttbarFileName,"READ")
m500File  = ROOT.TFile(o.m500FileName, "READ")
m1000File = ROOT.TFile(o.m1000FileName,"READ")

def normHist(hist):
    hist.Scale(1./hist.Integral())
    return hist


def plot2D(dir,hName,rootfile):
    was = gStyle.GetPadRightMargin()
    gStyle.SetPadRightMargin(0.15) 
    h_hist = rootfile.Get(dir+"/"+hName)
    print dir+"/"+hName
    canData = ROOT.TCanvas(dir+"_"+hName+"_data",dir+"_"+hName+"_data")
    #canData.SetLogz(1)
    #h_hist.Rebin2D(2,2)
    h_hist.GetZaxis().SetRangeUser(0,12)
    h_hist.Draw("colz")
    #h_hist.Sumw2()
    canData.SaveAs(o.output+"/"+dir+"_"+hName+"_data.pdf")
    gStyle.SetPadRightMargin(was)


def plot1D(dir,hName, rebin=2):
    can_mW = ROOT.TCanvas(hName+"_can",hName+"_can")
    tt_hist = ttbarFile.Get(dir+"/allHCand_"+hName)
    tt_hist.SetMinimum(0)
    tt_hist.Rebin(rebin)
    tt_hist = normHist(tt_hist)
    tt_hist.Draw()

    m500_hist = m500File.Get(dir+"/allHCand_"+hName)
    m500_hist.SetLineColor(ROOT.kRed)
    m500_hist.SetMarkerColor(ROOT.kRed)
    m500_hist.Rebin(rebin)
    m500_hist = normHist(m500_hist)
    m500_hist.Draw("same")

    m1000_hist = m1000File.Get(dir+"/allHCand_"+hName)
    m1000_hist.SetLineColor(ROOT.kBlue)
    m1000_hist.SetMarkerColor(ROOT.kBlue)
    m1000_hist.Rebin(rebin)
    m1000_hist = normHist(m1000_hist)
    m1000_hist.Draw("same")

    leg = ROOT.TLegend(0.7,0.7,0.9,0.94)
    leg.AddEntry(tt_hist,   "TTbar","PL")
    leg.AddEntry(m500_hist, "m500", "PL")
    leg.AddEntry(m1000_hist,"m1000","PL")

    leg.Draw("same")
    can_mW.SaveAs(o.output+"/"+dir+"_allHCand_"+hName+".pdf")
    


plot2D("PassTrigFourTag_Inclusive","allHCand_mWmT",ttbarFile)
plot2D("PassTrigTwoTag_Inclusive","allHCand_mWmT", ttbarFile)


plot1D("PassTrigFourTag_Inclusive","mW"  , rebin=4)
plot1D("PassTrigFourTag_Inclusive","mTop", rebin=4)
plot1D("PassTrigFourTag_Inclusive","Xtt" , rebin=4)

             
