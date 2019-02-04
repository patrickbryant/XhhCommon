import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",        default="", help="")
parser.add_option('-z', '--zJetsFile',          dest="zJetsFileName",        default=None, help="")
parser.add_option('-m', '--mu_qcd',             dest="mu_qcd",               default=0, help="")
parser.add_option('-o', '--out',                dest="output",               default="", help="")
o, a = parser.parse_args()

if not o.mu_qcd:
    print "ERROR give mu_qcd!!"
    import sys
    sys.exit(-1)


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

outFile = open(o.output+"/sampleComp.tex","w")

dataFile  = ROOT.TFile(o.dataFileName,"READ")
ttbarFile = ROOT.TFile(o.ttbarFileName,"READ")
if not o.zJetsFileName == None:
    zJetsFile = ROOT.TFile(o.zJetsFileName,"READ")    
else:
    zJetsFile = None

def getValues(inputFile,  dir,  scale=1.0):
    values = {}

    preSel = inputFile.Get(dir+"_Inclusive/nbjets")
    values["preSel"]    = scale * preSel.Integral()
    values["preSelErr"] = scale * pow(preSel.Integral(),0.5)

    sideband = inputFile.Get(dir+"_Sideband/nbjets")
    values["Sideband"]    = scale * sideband.Integral()
    values["SidebandErr"] = scale * pow(sideband.Integral(),0.5)

    control = inputFile.Get(dir+"_Control/nbjets")
    values["Control"]    = scale * control.Integral()
    values["ControlErr"] = scale * pow(control.Integral(),0.5)
    
    return values


def addValues(lhside,  rhside):
    values = {}
    values["scale"] = 1.0
    values["preSel"]    = lhside["preSel"]   + rhside["preSel"]
    values["preSelErr"] = pow(lhside["preSelErr"]*lhside["preSelErr"]+ rhside["preSelErr"]*rhside["preSelErr"],0.5)

    values["Sideband"] = lhside["Sideband"] + rhside["Sideband"]
    values["SidebandErr"] = pow(lhside["SidebandErr"]*lhside["SidebandErr"]+ rhside["SidebandErr"]*rhside["SidebandErr"],0.5)

    values["Control"]  = lhside["Control"]  + rhside["Control"]
    values["ControlErr"] = pow(lhside["ControlErr"]*lhside["ControlErr"]+ rhside["ControlErr"]*rhside["ControlErr"],0.5)
    return values


def printNum(n,err):
    return str(round(n,2))+" $\pm$ "+str(round(err,2))

def printRow(name,inNum):
    if name == "Data":
        return name+" & "+"Blinded"+" & "+printNum(inNum["Sideband"],inNum["SidebandErr"])+" & "+printNum(inNum["Control"],inNum["ControlErr"])+"\\\\"
    else:
        return name+" & "+printNum(inNum["preSel"],inNum["preSelErr"])+" & "+printNum(inNum["Sideband"],inNum["SidebandErr"])+" & "+printNum(inNum["Control"],inNum["ControlErr"])+"\\\\"

def printLine(line):
    print line
    outFile.write(line+"\n")

def printTable(inNum):
    
    printLine("\\begin{tabular}{ l | c | c | c  }")
    printLine( "Sample & Preselection & Sideband Region & Control Region  \\\\")
    printLine( "\hline\hline "                     )
    printLine( "& & & \\\\")
    printLine(printRow("QCD",sampleNumbers["QCD"]))
    printLine(printRow("\\ttbar",sampleNumbers["ttbar"]))
    if "Z+jets" in sampleNumbers:
        printLine(printRow("Z+jets",sampleNumbers["Z+jets"]))
    printLine( "& & & \\\\"                       )
    printLine(printRow("Total",sampleNumbers["total"]) )
    printLine( "& & & \\\\"                       )
    printLine( "\hline\hline"                     )
    printLine( "& & & \\\\"                       )
    printLine(printRow("Data",sampleNumbers["Data"])   )
    printLine( "& & & \\\\"                       )
    printLine( "\hline\hline"                     )
    printLine("\end{tabular}")


sampleNumbers = {}
sampleNumbers["QCD" ]   = getValues(dataFile,  "TTVetoTwoTag", float(o.mu_qcd) )
sampleNumbers["ttbar" ] = getValues(ttbarFile, "TTVetoFourTag" )
if zJetsFile:
    sampleNumbers["Z+jets"] = getValues(zJetsFile, "TTVetoFourTag" )
sampleNumbers["total"]  = addValues(sampleNumbers["QCD"], sampleNumbers["ttbar"])
if "Z+jets" in sampleNumbers:
    sampleNumbers["total"]  = addValues(sampleNumbers["total"], sampleNumbers["Z+jets"])
sampleNumbers["Data" ]  = getValues(dataFile,  "TTVetoFourTag" )
printTable(sampleNumbers)    



             
