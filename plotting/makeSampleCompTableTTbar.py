
import os

#
#
#
import OfficialAtlasStyle
import ROOT
from ROOT import gStyle                                                                                                                             
gStyle.SetPalette(1)
ROOT.gROOT.SetBatch(1)


def parseOptions():
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
    parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",        default="", help="")
    parser.add_option('-m', '--mu_qcd',             dest="mu_qcd",               default=0, help="")
    parser.add_option('-o', '--out',                dest="output",               default="", help="")
    o, a = parser.parse_args()
    
    if not o.mu_qcd:
        print "ERROR give mu_qcd!!"
        import sys
        sys.exit(-1)
    return o,a


def getValues(inputFile,  dir,  scale=1.0):
    values = {}

    sideband = inputFile.Get(dir+"_Sideband/nbjets")
    values["Sideband"]    = scale * sideband.Integral()
    values["SidebandErr"] = scale * pow(sideband.Integral(),0.5)

    control = inputFile.Get(dir+"_Control/nbjets")
    values["Control"]    = scale * control.Integral()
    values["ControlErr"] = scale * pow(control.Integral(),0.5)

    signal = inputFile.Get(dir+"_Signal/nbjets")
    values["Signal"]    = scale * signal.Integral()
    values["SignalErr"] = scale * pow(signal.Integral(),0.5)

    signalzz = inputFile.Get(dir+"_SignalZZ/nbjets")
    values["SignalZZ"]    = scale * signalzz.Integral()
    values["SignalZZErr"] = scale * pow(signalzz.Integral(),0.5)
    
    return values


def addValues(lhside,  rhside):
    values = {}

    values["Sideband"] = lhside["Sideband"] + rhside["Sideband"]
    values["SidebandErr"] = pow(lhside["SidebandErr"]*lhside["SidebandErr"]+ rhside["SidebandErr"]*rhside["SidebandErr"],0.5)

    values["Control"]  = lhside["Control"]  + rhside["Control"]
    values["ControlErr"] = pow(lhside["ControlErr"]*lhside["ControlErr"]+ rhside["ControlErr"]*rhside["ControlErr"],0.5)

    values["Signal"]    = lhside["Signal"]   + rhside["Signal"]
    values["SignalErr"] = pow(lhside["SignalErr"]*lhside["SignalErr"]+ rhside["SignalErr"]*rhside["SignalErr"],0.5)

    return values


def printNum(n,err,noErrors):
    if noErrors: return str(int(n))
    return str(round(n,2))+" $\pm$ "+str(round(err,2))

def printRow(name,inNum, noErrors=False):
    return name+" & "+printNum(inNum["Sideband"],inNum["SidebandErr"],noErrors)+" & "+printNum(inNum["Control"],inNum["ControlErr"],noErrors)+" & "+printNum(inNum["Signal"],inNum["SignalErr"],noErrors)+"\\\\"


def printLine(line):
    print line
    outFile.write(line+"\n")

def printTable(inNum):
    
    printLine("\\begin{tabular}{ l | c | c | c  }")
    printLine( "Sample & TTSideband Region & TTControl Region & TThh Region  \\\\")
    printLine( "\hline\hline "                     )
    printLine( "& & & \\\\")
    printLine(printRow("QCD",    inNum["QCD"]   ))
    printLine(printRow("\\ttbar",inNum["ttbar"] ))
    printLine( "& & & \\\\"                       )
    printLine(printRow("Total",  inNum["total"] ))
    printLine( "& & & \\\\"                       )
    printLine( "\hline\hline"                     )
    printLine( "& & & \\\\"                       )
    printLine(printRow("Data",   inNum["Data"], noErrors=False ))
    printLine( "& & & \\\\"                       )
    printLine( "\hline\hline"                     )
    printLine("\end{tabular}")


def main(dataFile, ttbarFile, mu_qcd):

    sampleNumbers = {}
    sampleNumbers["QCD" ]   = getValues(dataFile,  "ReverseTTVetoTwoTag", float(mu_qcd) )
    sampleNumbers["ttbar" ] = getValues(ttbarFile, "ReverseTTVetoFourTag" )
    sampleNumbers["total"]  = addValues(sampleNumbers["QCD"], sampleNumbers["ttbar"])
    sampleNumbers["Data" ]  = getValues(dataFile,  "ReverseTTVetoFourTag" )
    printTable(sampleNumbers)    


if __name__ == "__main__":

    o,a = parseOptions()
    if not os.path.isdir(o.output):
        os.mkdir(o.output)


    outFile = open(o.output+"/sampleCompTTbar.tex","w")
    dataFile  = ROOT.TFile(o.dataFileName,"READ")
    ttbarFile = ROOT.TFile(o.ttbarFileName,"READ")
    main(dataFile, ttbarFile, o.mu_qcd)

             
