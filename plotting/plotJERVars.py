from iPlot import loadPath
loadPath()

from utils import parseOpts, getPM, setBatch, plot

setBatch()
(o,a) = parseOpts()
pm = getPM(o)
import OfficialAtlasStyle

#
#
#
import ROOT
from ROOT import gStyle                                                                                                                             

labels=["JER +1#sigma","Nominal"]

plot("leadHCand_Mass","TTVetoFourTag_Inclusive",doratio=0,rMin=0.5,rMax=1.5,x_max=300,labels=labels,xlabel="lead H-Cand Mass [GeV]")
plot("sublHCand_Mass","TTVetoFourTag_Inclusive",doratio=0,rMin=0.5,rMax=1.5,x_max=300,labels=labels,xlabel="subl H-Cand Mass [GeV]")
plot("m4j",          "TTVetoFourTag_Inclusive", doratio=0,rMin=0.5,rMax=1.5,x_min=300,labels=labels,xlabel="m_{4j} [GeV]",rebin=2)
plot("m4j_l",        "TTVetoFourTag_Inclusive", doratio=0,rMin=0.5,rMax=1.5,x_min=300,labels=labels,xlabel="m_{4j} [GeV]",rebin=2)
