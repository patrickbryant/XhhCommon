import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",        default="", help="")
parser.add_option('-z', '--zJetsFile',          dest="zJetsFileName",        default=None, help="")
parser.add_option(      '--ttbarSignal',        dest="ttbarSignalFileName",  default="", help="")
parser.add_option('-m', '--mu_qcd',             dest="mu_qcd",               default=0, help="")
parser.add_option('--zz',                       action="store_true", dest="doZZ",     default=False, help="")
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

if o.doZZ:
    outFile = open(o.output+"/sampleCompZZ.tex","w")
else:
    outFile = open(o.output+"/sampleCompQCDVar.tex","w")

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

    if o.doZZ:
        signal = inputFile.Get(dir+"_SignalZZ/nbjets")
        values["SignalZZ"]    = scale * signal.Integral()
        values["SignalZZErr"] = scale * pow(signal.Integral(),0.5)
    else:
        signal = inputFile.Get(dir+"_Signal/nbjets")
        values["Signal"]    = scale * signal.Integral()
        values["SignalErr"] = scale * pow(signal.Integral(),0.5)


    for s in values:
        if values[s] < 0: values[s] = 0
    
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

    if o.doZZ:
        values["SignalZZ"]  = lhside["SignalZZ"]  + rhside["SignalZZ"]
        values["SignalZZErr"] = pow(lhside["SignalZZErr"]*lhside["SignalZZErr"]+ rhside["SignalZZErr"]*rhside["SignalZZErr"],0.5)
    else:
        values["Signal"]  = lhside["Signal"]  + rhside["Signal"]
        values["SignalErr"] = pow(lhside["SignalErr"]*lhside["SignalErr"]+ rhside["SignalErr"]*rhside["SignalErr"],0.5)

    return values


def printNum(n,err):
    return str(round(n,2))+" $\pm$ "+str(round(err,2))

def printRow(name,inNum):
    if name == "Data" and not o.doZZ:
        return name+" & "+"Blinded"+" & "+printNum(inNum["Sideband"],inNum["SidebandErr"])+" & "+printNum(inNum["Control"],inNum["ControlErr"])+" & Blinded \\\\"
    else:
        if o.doZZ:
            return name+" & "+printNum(inNum["preSel"],inNum["preSelErr"])+" & "+printNum(inNum["Sideband"],inNum["SidebandErr"])+" & "+printNum(inNum["Control"],inNum["ControlErr"])+" & "+printNum(inNum["SignalZZ"],inNum["SignalZZErr"])+" \\\\"
        else:
            return name+" & "+printNum(inNum["preSel"],inNum["preSelErr"])+" & "+printNum(inNum["Sideband"],inNum["SidebandErr"])+" & "+printNum(inNum["Control"],inNum["ControlErr"])+" & "+printNum(inNum["Signal"],inNum["SignalErr"])+" \\\\"

def printLine(line):
    print line
    outFile.write(line+"\n")

def printTable(inNum):
    
    printLine("\\begin{tabular}{ l | c | c | c | c   }")
    if o.doZZ:
        printLine( "Sample & Preselection & Sideband Region & Control Region & ZZ Region  \\\\")
    else:
        printLine( "Sample & Preselection & Sideband Region & Control Region & hh Region  \\\\")
    printLine( "\hline\hline "                     )
    printLine( "& & & & \\\\")
    printLine(printRow("QCD",sampleNumbers["QCD"]))
    printLine(printRow("\\ttbar",sampleNumbers["ttbar"]))
    if "Z+jets" in sampleNumbers:
        printLine(printRow("Z+jets",sampleNumbers["Z+jets"]))
    printLine( "& & & & \\\\"                       )
    printLine(printRow("Total",sampleNumbers["total"]) )
    printLine( "& & & & \\\\"                       )
    printLine( "\hline\hline"                     )
    printLine( "& & & & \\\\"                       )
    printLine(printRow("Data",sampleNumbers["Data"])   )
    printLine( "& & & & \\\\"                       )
    printLine( "\hline\hline"                     )
    printLine("\end{tabular}")


sampleNumbers = {}
sampleNumbers["QCD" ]   = getValues(dataFile,  "TTVetoTwoTag", float(o.mu_qcd) )
sampleNumbers["ttbar" ] = getValues(ttbarFile, "TTVetoFourTag" )
if zJetsFile:
    sampleNumbers["Z+jets"] = getValues(zJetsFile, "TTVetoFourTag" )


ddttbarFile = open(o.ttbarSignalFileName,"r")
ttbarData = ddttbarFile.readlines()
ttbarDataWords = ttbarData[0].split()
nTTBar        = float(ttbarDataWords[2])
nTTBarErr_QCD = float(ttbarDataWords[4])

nTTBarErr_Eff = float(ttbarDataWords[8])
nTTBarErr     = pow((nTTBarErr_QCD**2 +nTTBarErr_Eff**2),0.5)


if nTTBar < 0: nTTBar = 0

#ttbarValues = {}
#ttbarValues["Signal"] = nTTBar
#ttbarValues["SignalErr"] = nTTBarErr

if o.doZZ:
    sampleNumbers["ttbar"]["SignalZZ"] = nTTBar
    sampleNumbers["ttbar"]["SignalZZErr"] = nTTBarErr
else:
    sampleNumbers["ttbar"]["Signal"] = nTTBar
    sampleNumbers["ttbar"]["SignalErr"] = nTTBarErr


sampleNumbers["total"]  = addValues(sampleNumbers["QCD"], sampleNumbers["ttbar"])
if "Z+jets" in sampleNumbers:
    sampleNumbers["total"]  = addValues(sampleNumbers["total"], sampleNumbers["Z+jets"])
sampleNumbers["Data" ]  = getValues(dataFile,  "TTVetoFourTag" )
printTable(sampleNumbers)    



             
