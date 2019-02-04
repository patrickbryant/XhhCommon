import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",        default="", help="")
parser.add_option('--m500',                     dest="m500FileName",         default="", help="")
parser.add_option('--m1000',                    dest="m1000FileName",        default="", help="")
parser.add_option('--m1200',                    dest="m1200FileName",        default="", help="")
parser.add_option('-o', '--out',                dest="output",               default="", help="")
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

outFile = open(o.output+"/cutFlowTable.tex","w")

dataFile  = ROOT.TFile(o.dataFileName,"READ")
ttbarFile = ROOT.TFile(o.ttbarFileName,"READ")
m500File  = ROOT.TFile(o.m500FileName, "READ")
m1000File = ROOT.TFile(o.m1000FileName,"READ")
m1200File = ROOT.TFile(o.m1200FileName,"READ")

cutFlowTitle = {"All"        :  "Pass Skim",
                "AllEvents"  :  "Derivation",
                "PassGRL"    :  "PassGRL",
                #"Pass2DiJetsAny":  "2 HCands",
                "PassBJetSkim": "2 Higgs Cands",
                "NJetsAbove3": "NJets >= 4",
                "NBJetsAbove3": "NBJets >= 4",
                "NBJetsEqual4": "NBJets == 4",
                "PassJetCleaning": "Pass Cleaning",
                "PassJetPt": "jets >= 40 GeV",
                "PassDiJetPt": "HCand $P_T$ cuts",
                "PassTrigRaw": "Trigger Requirement",
                "PassTrig": "Trigger Threshold",
                "PassM4j":"Mass Dep. Cuts",
                "PassTTVeto":"TT Veto",
                "PassTTVetoSignal": "Xhh",
                }

cutFlowOrder = ["AllEvents",
                "All",
                "PassGRL",
                #"PassCleaning",
                "NJetsAbove3",
                "NBJetsAbove3",
                "NBJetsEqual4",
                #"Pass2DiJetsAny",
                "PassBJetSkim",
                "PassJetCleaning",
                "PassJetPt",
                "PassDiJetPt",
                "PassTrigRaw",
                "PassTrig",
                "PassM4j",
                "PassTTVeto",
                "PassTTVetoSignal",
                ]


def getCutFlow(inputFile):
    h_4bWeighted = inputFile.Get("CutFlow4bWeighted")

    thisCutFlow = {}
    for o in cutFlowOrder:
        value = h_4bWeighted.GetBinContent(h_4bWeighted.GetXaxis().FindBin(o))
        thisCutFlow[o] = value
    return thisCutFlow

def printLine(line):
    print line
    outFile.write(line+"\n")


def printTable(inputNumberDic):

    printLine("\\begin{tabular}{ c | c | c | c | c | c }")
    printLine("Cut & Data & $m_{G}$ = 500 GeV  & $m_{G}$ = 1000 GeV & $m_{G}$ = 1200 GeV & \\ttbar\\\\")
    printLine("\hline\hline")

    for o in cutFlowOrder:
        line = ""
        line += cutFlowTitle[o] + " & "
        if o in ["PassTTVetoSignal","PassTTVeto"]:
            line += "Blinded "+" & "
        else:
            line += str(inputNumberDic["data"][o]) + " & "
        line += str(round(inputNumberDic["m500"][o] ,2)) + " & "
        line += str(round(inputNumberDic["m1000"][o],2)) + " & "
        line += str(round(inputNumberDic["m1200"][o],2)) + " & "
        line += str(round(inputNumberDic["ttbar"][o],2)) + "\\\\"
        printLine(line)

    printLine("\hline\hline")
    printLine("%$k/M_{pl} = 1.5$ & - & 63.1 & 3.2 & 0.06 & -\\\\")
    printLine("%$k/M_{pl} = 2.0$ & - & 123.8 & 4.9 & 0.12 & -\\\\")
    printLine("%\hline\hline")
    printLine("\end{tabular}")

cutFlowNumbers = {}
cutFlowNumbers["data" ] = getCutFlow(dataFile )
cutFlowNumbers["m500" ] = getCutFlow(m500File )
cutFlowNumbers["m1000"] = getCutFlow(m1000File)
cutFlowNumbers["m1200"] = getCutFlow(m1200File)
cutFlowNumbers["ttbar"] = getCutFlow(ttbarFile)
printTable(cutFlowNumbers)    

             
