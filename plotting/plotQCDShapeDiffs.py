from iPlot import loadPath
loadPath()
from utils import parseOpts, getPM, setBatch, plot

setBatch()
(o,a) = parseOpts()
pm = getPM(o)

import ROOT

m4j_bins = [400,460,520,580,640,700,800,900,1000,1300,2000]
#m4j_bins = 2

#plot("m4j_l","TTVetoTwoTag_Signal",norm=1,doratio=1,rebin=m4j_bins,rMin=0.5,rMax=1.5,labels=["Nomial",o.labName])
plot("m4j_l","TTVetoTwoTag_Signal",norm=1,doratio=1,rebin=m4j_bins,rMin=0.5,rMax=1.5,labels=[o.labName,"Nomial"])


