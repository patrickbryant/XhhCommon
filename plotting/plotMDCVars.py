import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',           dest="dataFileName",          default="", help="")
parser.add_option('--m300',                     dest="m300FileName",          default="", help="")
parser.add_option('--m500',                     dest="m500FileName",          default="", help="")
parser.add_option('--m1000',                    dest="m1000FileName",         default="", help="")

parser.add_option('-o', '--out',                dest="output",                default="", help="")
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


dataFile  = ROOT.TFile(o.dataFileName,"READ")
m300File  = ROOT.TFile(o.m300FileName,"READ")
m500File  = ROOT.TFile(o.m500FileName, "READ")
m1000File = ROOT.TFile(o.m1000FileName,"READ")


def normHist(hist):
    hist.Scale(1./hist.Integral())
    return hist


def plot1D(dirName, hName, x_min, x_max, y_max, rebin=2):

    can_mW = ROOT.TCanvas(hName+"_can",hName+"_can")
    #dataFile.ls()
    data_hist = dataFile.Get(dirName+"/TwoTag/Inclusive/"+hName)
    data_hist.Sumw2()
    data_hist.Rebin(rebin)
    data_hist = normHist(data_hist)
    data_hist.GetYaxis().SetRangeUser(0,y_max)
    data_hist.GetXaxis().SetRangeUser(x_min,x_max)
    data_hist.Draw("")

    m500_hist = m500File.Get(dirName+"/FourTag/Inclusive/"+hName)
    m500_hist.SetLineColor(ROOT.kRed)
    m500_hist.SetMarkerColor(ROOT.kRed)
    m500_hist.Rebin(rebin)
    m500_hist = normHist(m500_hist)
    m500_hist.Draw("same")
    #data_hist.Draw("same")

    m1000_hist = m1000File.Get(dirName+"/FourTag/Inclusive/"+hName)
    m1000_hist.SetLineColor(ROOT.kBlue)
    m1000_hist.SetMarkerColor(ROOT.kBlue)
    m1000_hist.Rebin(rebin)
    m1000_hist = normHist(m1000_hist)
    m1000_hist.Draw("same")

    m300_hist = m300File.Get(dirName+"/FourTag/Inclusive/"+hName)
    m300_hist.SetLineColor(ROOT.kGreen)
    m300_hist.SetMarkerColor(ROOT.kGreen)
    m300_hist.SetMarkerSize(1)
    m300_hist.Rebin(rebin)
    m300_hist = normHist(m300_hist)
    m300_hist.Draw("same")

    leg = ROOT.TLegend(0.7,0.65,0.9,0.89)
    leg.AddEntry(data_hist, "QCD","PL")
    leg.AddEntry(m300_hist,"m300","PL")
    leg.AddEntry(m500_hist, "m500", "PL")
    leg.AddEntry(m1000_hist,"m1000","PL")


    leg.Draw("same")
    #data_hist.Draw("axis same")    
    outName = dirName.replace("/","_")+"FourTag_Inclusive_"+hName+".pdf"
    print outName
    can_mW.SaveAs(o.output+"/"+outName)



dirName = "Loose/DhhMin"
plot1D(dirName, "leadHCand_Pt_m"  , rebin=2, x_min=0,x_max=1000, y_max = 0.35)
plot1D(dirName, "sublHCand_Pt_m"  , rebin=2, x_min=0,x_max=1000, y_max = 0.35)
plot1D(dirName, "hCandDeta"       , rebin=2, x_min=-3, x_max=3,    y_max = 0.2)
#$plot1D("FourTag_Inclusive","mTop", rebin=4)
#$plot1D("FourTag_Inclusive","Xtt" , rebin=4)

             
