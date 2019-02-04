import optparse
import sys, os, subprocess
parser = optparse.OptionParser()
parser.add_option('-t',      '--tag',            dest="tag",            default="",                             help="DS Tag JZXW or Data")
parser.add_option('-r',      '--reference',      dest="refFileName",    default="EXOT8_data_EventCounts.txt",   help="DS Tag JZXW or Data")
o, a = parser.parse_args()

import ROOT

expectedCountDict = {}
expectedCountFileName = os.path.expandvars(o.refFileName)
expectedCountFile     = open(expectedCountFileName, "r")

for line in expectedCountFile:
    words = line.split()
    events =  int(words[1])
    daodName = words[0]

    year      =  daodName.split(".")[0]
    runNumber =  daodName.split(".")[1]
    expectedCountDict[year+"."+runNumber]  = events

expectedCountFile.close()


if not o.tag:
  print "ERROR: give a tag"
  sys.exit(-1) 



#
#  Getting expected event counts
#
def getExpectedCounts(runNumber):
    #print expectedCountDict
    if runNumber in expectedCountDict:
        return expectedCountDict[runNumber]

    return -1

#
#  Getting expected event counts
#
def getNProcessed(runNumber, fileName):
    thisFile = ROOT.TFile(fileName,"READ")
    procEvents = -1
    keys = thisFile.GetListOfKeys()
    for k in keys:
        name = k.GetName()
        if name.count("cutflow") and not name.count("weighted"):
            procEvents  = int((k.ReadObj()).GetBinContent(1))
    thisFile.Close()
    return procEvents


#
#  Executing the python
#   (configGlobals and configLocals are used to pass vars
#
configGlobals = {}
configLocals  = {}
execfile(os.path.expandvars("$ROOTCOREBIN/user_scripts/XhhResolved/dataSetDB.py"), configGlobals, configLocals)

dsList = configLocals["dsDB"][o.tag]


cmd = ""
for ds in dsList:
    
    print ds

    #
    #  Get Expected Event Counts
    #
    expected_counts = getExpectedCounts(ds)

    if expected_counts < 0:
        print "\tNo expected counts for ",ds
        continue

    #
    #  Get number of processed events
    #
    procDirs = True
    if procDirs:
        processed_events = 0
        files = os.popen("ls "+dsList[ds]+"/*root*").readlines()
        for f in files:
            fileName = f.rstrip()
            processed_events += getNProcessed(ds, fileName)
    else:
        processed_events = getNProcessed(ds, dsList[ds])

    if processed_events < 0:
        print "\tNo processed event counts for ",ds
        continue

    if not expected_counts == processed_events:
        print "\tCount mis match:",expected_counts,"expected",processed_events,"processed"
    else: 
        print "\tall good."
