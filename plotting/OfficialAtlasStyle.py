from ROOT import *
import ROOT
try:
    ROOT.gROOT.LoadMacro("/Users/johnda/ROOTHelpers/atlasstyle-00-03-05/AtlasStyle.C")
    SetAtlasStyle()
except:
    try:
        ROOT.gROOT.LoadMacro("/home/johnda/ROOTHelpers/atlasstyle-00-03-05/AtlasStyle.C")
        SetAtlasStyle()
    except:
        print "Passing on AtlasStyle.C"
        pass


#ROOT.gROOT.LoadMacro("AtlasStyle.C") 
#SetAtlasStyle()
