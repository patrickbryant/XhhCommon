import optparse
parser = optparse.OptionParser()
parser.add_option('--signalDir',                dest="signalDir",             default="", help="")
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

order = ["hh","2HDM","RSG"]
dirMap = {
    "RSG"  : "RSG_c10_M500",
    "2HDM" : "Hhh_M500",
    "hh"   : "hh_4b",
    }

signalFiles = {}
for d in dirMap: 
    signalFiles[d] = ROOT.TFile(o.signalDir+"/"+dirMap[d]+"/hist-tree.root", "READ")

total = {}

outFile = open(o.output+"/sigAccTable.tex","w")
def w(line):
    outFile.write(line+"\n")

class cutValue:
    
    def __init__(self, name, legName="", color=ROOT.kBlack, style=0):
        self.name = name
        self.sampleYeilds = {}
        self.color = color
        self.style = style
        self.legName = legName

    def eff(self,sample):
        #print "eff: ", sample
        #print float(self.sampleYeilds[sample]),self.norm.sampleYeilds[sample]
        
        return str(round(float(self.sampleYeilds[sample])/self.norm.sampleYeilds[sample],4))

    def rel(self,sample):
        thisEff =  float(self.sampleYeilds[sample])/self.prev.sampleYeilds[sample]
        #lastEff =  float(self.prev.sampleYeilds[sample])/self.norm.sampleYeilds[sample]
        return str(round(thisEff,4))
    
    def printRow(self,norm,previous=None):
        self.norm = norm
        self.prev = previous
        if previous == None:
            line  = self.legName     + "   &   " 
            line += self.eff("hh")   + "   &   "  + " - " + "   &   "
            line += self.eff("2HDM") + "   &   "  + " - " + "   &   " 
            line += self.eff("RSG")  + "   &   "  + " - " +"\\\\"
        else:
            line  = self.legName     + "   &   " 
            line += self.eff("hh")   + "   &   "  + self.rel("hh")   + "   &   "
            line += self.eff("2HDM") + "   &   "  + self.rel("2HDM") + "   &   " 
            line += self.eff("RSG")  + "   &   "  + self.rel("RSG")  +"\\\\"

        w(line)

    def makeGraph(self, massPts, norm):
        self.graph = ROOT.TGraph(len(massPts))
        self.graph.SetLineWidth(2)
        self.graph.SetLineColor  (self.color)
        self.graph.SetMarkerColor(self.color)
        
        if self.style:
            self.graph.SetMarkerStyle(self.style)
        
        pointCount = 0
        for m in massPts:
            
            if not norm.massYeilds[m]: continue
            eff = float(self.sampleYeilds[m])/norm.sampleYeilds[m]
            
            self.graph.SetPoint(pointCount, float(m), eff)
            pointCount += 1
                                
    

totals = cutValue("AllEvents")


cutList = []
#cutList.append( cutValue("NJetsAbove3"     ) )
cutList.append( cutValue("NBJetsEqual4"    ,  "4 b-jets",      ROOT.kBlue,    25) )
cutList.append( cutValue("PassBJetSkim"    ,  "2 dijets",      ROOT.kBlue,    22) )
#cutList.append( cutValue("PassTrig"        ,  "Trigger",       ROOT.kBlack,    22) )
cutList.append( cutValue("PassM4j"         ,  "MDC",           ROOT.kBlue-5,  23) )
cutList.append( cutValue("PassTTVeto"      ,  "tt Cut",        ROOT.kBlue-5,  24) )
cutList.append( cutValue("PassTTVetoSignal",  "Signal Region", ROOT.kRed,     28) )

for m in order:
    cutFlowHists = signalFiles[m].Get("CutFlow4bRaw")

    totals.sampleYeilds[m] = cutFlowHists.GetBinContent(cutFlowHists.GetXaxis().FindBin(totals.name))             
    
    for c in cutList:
        if c.name == "PassTTVetoSignal":
            print m, cutFlowHists.GetBinContent(cutFlowHists.GetXaxis().FindBin(c.name))             
        
        c.sampleYeilds[m] = cutFlowHists.GetBinContent(cutFlowHists.GetXaxis().FindBin(c.name))             




w("\\begin{tabular}{ lcccccc }")
w("\hline")
w(" & \multicolumn{2}{c}{SM HH} & \multicolumn{2}{c}{2HDM, $m_{H}=500$\,GeV} & \multicolumn{2}{c}{RSG c=1.0, $m_{G*}=500$\,GeV} \\\\")
w(" Requirement & Abs. $\\varepsilon$ & Rel. $\\varepsilon$&  Abs. $\\varepsilon$ & Rel. $\\varepsilon$ &  Abs. $\\varepsilon$ & Rel. $\\varepsilon$\\\\")
w(" \hline")
cutList[0].printRow(totals)
cutList[1].printRow(totals,cutList[0])
cutList[2].printRow(totals,cutList[1])
cutList[3].printRow(totals,cutList[2])
cutList[4].printRow(totals,cutList[3])
w("\hline")
w("\end{tabular}")

