import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",        default="", help="")
parser.add_option('-m', '--mu_qcd',             dest="mu_qcd",               default=0, help="")
parser.add_option('-o', '--out',                dest="output",               default="", help="")
parser.add_option('-b', '--unblinded',          action="store_true",         dest="unblinded",   default=False, help="")
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

if o.unblinded:
    outFile = open(o.output+"/sampleCompSR_unblinded.tex","w")   
else:
    outFile = open(o.output+"/sampleCompSR.tex","w")
   

dataFile  = ROOT.TFile(o.dataFileName,"READ")

def getValues(inputFile,  dir,  scale=1.0, systFraction=None):
    values = {}

    signal = inputFile.Get(dir+"_Signal/nbjets")
    values["Signal"]    = scale * signal.Integral()
    
    if systFraction == None:
        values["SignalErr"] = scale * pow(signal.Integral(),0.5)
    else:
        statError = scale * pow(signal.Integral(),0.5)
        systError = values["Signal"]*systFraction

        values["SignalErr"] = pow(statError*statError + systError*systError  , 0.5)
    
    
    return values


def addValues(lhside,  rhside):
    values = {}

    values["Signal"]    = lhside["Signal"]   + rhside["Signal"]
    values["SignalErr"] = pow(lhside["SignalErr"]*lhside["SignalErr"]+ rhside["SignalErr"]*rhside["SignalErr"],0.5)
    return values


def printNum(n,err,doInt=False):
    if doInt:
        return str(int(n))+" $\pm$ "+str(round(err,2))
    return str(round(n,2))+" $\pm$ "+str(round(err,2))

def printRow(name,inNum):
    if name == "Data" :
        if not o.unblinded:
            return name+" & "+"Blinded"+"\\\\"
        else:
            return name+" & "+printNum(inNum["Signal"],inNum["SignalErr"],doInt=True)+"\\\\"
    else:
        return name+" & "+printNum(inNum["Signal"],inNum["SignalErr"])+"\\\\"

def printLine(line):
    print line
    outFile.write(line+"\n")

def printTable(inNum):
    
    printLine("\\begin{tabular}{ l | c }")
    printLine("Sample & hh Region \\\\")
    printLine("\hline\hline")
    printLine("& \\\\")
    printLine(printRow("QCD",sampleNumbers["QCD"]))
    printLine(printRow("\\ttbar",sampleNumbers["ttbar"]))
    printLine( "& \\\\"                       )
    printLine(printRow("Total",sampleNumbers["total"]) )
    printLine( "& \\\\"                       )
    printLine( "\hline\hline"                     )
    printLine( "& \\\\"                       )
    printLine(printRow("Data",sampleNumbers["Data"])   )
    printLine( "& \\\\"                       )
    printLine( "\hline\hline"                     )
    printLine("\end{tabular}")



sampleNumbers = {}
sampleNumbers["QCD" ]   = getValues(dataFile,  "TTVetoTwoTag", float(o.mu_qcd), systFraction=0.05 )

ddttbarFile = open(o.ttbarFileName,"r")
ttbarData = ddttbarFile.readlines()
ttbarDataWords = ttbarData[0].split()
nTTBar        = float(ttbarDataWords[2])
nTTBarErr_QCD = float(ttbarDataWords[4])

nTTBarErr_Eff = float(ttbarDataWords[8])
nTTBarErr     = pow((nTTBarErr_QCD**2 +nTTBarErr_Eff**2),0.5)

ttbarValues = {}
ttbarValues["Signal"] = nTTBar
ttbarValues["SignalErr"] = nTTBarErr


sampleNumbers["ttbar" ] = ttbarValues
sampleNumbers["total"]  = addValues(sampleNumbers["QCD"], sampleNumbers["ttbar"])

sampleNumbers["Data" ]  = getValues(dataFile,  "TTVetoFourTag" )
printTable(sampleNumbers)    



             
