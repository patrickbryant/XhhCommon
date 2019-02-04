import optparse
parser = optparse.OptionParser()
parser.add_option('--signalDir',                dest="signalDir",             default="", help="")
parser.add_option('-o', '--out',                dest="output",                default="", help="")
parser.add_option('-s', '--sample',             dest="sample",                default="RSG", help="")
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

order = [
    "m300" ,
    "m400" ,
    "m500" ,
    "m600" ,
    "m700" ,
    "m800" ,
    "m900" ,
    "m1000",
    "m1100",
    "m1200",
    ]

if o.sample == "RSG":
    dirMap = {
        "m300" :"RSG300_2015_hists",  
        "m400" :"RSG400_2015_hists",  
        "m500" :"RSG500_2015_hists",  
        "m600" :"RSG600_2015_hists",  
        "m700" :"RSG700_2015_hists",  
        "m800" :"RSG800_2015_hists",  
        "m900" :"RSG900_2015_hists",  
        "m1000":"RSG1000_2015_hists",  
        "m1100":"RSG1100_2015_hists",  
        "m1200":"RSG1200_2015_hists",
        }
elif o.sample == "Hhh":
    dirMap = {
        "m300" :"RSG300_2015_hists",  
        "m400" :"Hhh_M400",  
        "m500" :"Hhh_M500",  
        "m600" :"Hhh_M600",  
        "m700" :"Hhh_M700",  
        "m800" :"Hhh_M800",  
        "m900" :"Hhh_M900",  
        "m1000":"Hhh_M1000",  
        "m1100":"Hhh_M1100",  
        "m1200":"Hhh_M1200",
        }
else:
    order = ["SM hh"]
    dirMap = {
        "SM hh" :"nonResonant_2015_hists",  
        }    

colors = {
    "SM hh" :ROOT.kBlack,
    "m300" :ROOT.kRed,
    "m400" :ROOT.kBlue,
    "m500" :ROOT.kGreen,
    "m600" :ROOT.kOrange,  
    "m700" :ROOT.kAzure+10,  
    "m800" :ROOT.kViolet,  
    "m900" :ROOT.kCyan+3,  
    "m1000":ROOT.kRed+2,  
    "m1100":ROOT.kBlue+2,  
    "m1200":ROOT.kGreen+2,
    }


signalFiles = {}

for d in order: 
    signalFiles[d] = ROOT.TFile(o.signalDir+"/"+dirMap[d]+"/hists.root", "READ")

def normHist(hist):
    hist.Scale(1./hist.Integral())
    return hist


def plot1D(dirName, hName, x_min, x_max, y_max, rebin=2):

    can_mW = ROOT.TCanvas(hName+"_can",hName+"_can")
    #can_mW.SetLogy(1)
    signal_hists = {}
    isFirst=True
    leg = ROOT.TLegend(0.7,0.55,0.9,0.89)

    for d in order:

        signal_hists[d] = signalFiles[d].Get(dirName+"/FourTag/Inclusive/"+hName)

        signal_hists[d].Rebin(rebin)
        signal_hists[d] = normHist(signal_hists[d])
        signal_hists[d].SetLineColor  (colors[d])
        signal_hists[d].SetMarkerColor(colors[d])

        leg.AddEntry(signal_hists[d], d, "PL")

        if isFirst:
            signal_hists[d].GetYaxis().SetRangeUser(1e-3,y_max)
            signal_hists[d].GetXaxis().SetRangeUser(x_min,x_max)
            signal_hists[d].Draw("")
        else:
            signal_hists[d].Draw("same")            
            signal_hists[d].Draw("same axis")            

        isFirst = False

    leg.Draw("same")
    can_mW.SaveAs(o.output+"/"+o.sample+"_"+dirName.replace("/","_")+"FourTag_Inclusive_"+hName+".pdf")



#dirName = "TTVeto"
dirName = "Loose/DhhMin"
rebin = 1
y_max = 0.15
if o.sample in ["Hhh"]:
    y_max = 0.3
if o.sample in ["hh"]:
    y_max = 0.1
    rebin = 2

plot1D(dirName, "m4j_l"  , rebin=rebin, x_min=0,x_max=1600, y_max = y_max)
#plot1D(dirName, "sublHCand_Pt_m"  , rebin=2, x_min=150,x_max=1000, y_max = 0.35)
#plot1D(dirName, "hCandDeta"       , rebin=2, x_min=-5, x_max=5,    y_max = 0.2)
##$plot1D("FourTag_Inclusive","mTop", rebin=4)
##$plot1D("FourTag_Inclusive","Xtt" , rebin=4)

             
