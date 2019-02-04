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

norm = 1
if not o.mcscale == 1.0: norm = 0


rMin = 0.

labelNames=["Mass Correction","No Mass Correction"]

plot(["m4j_cor",  "m4j"  ],"TTVetoFourTag_Signal",labels=labelNames,x_min=300,x_max=1000,xlabel="m_{4j} [GeV]")
plot(["m4j_cor_l","m4j_l"],"TTVetoFourTag_Signal",labels=labelNames,x_min=500,x_max=1500,xlabel="m_{4j} [GeV]")


plot(["m4j_cor",  "m4j"  ],"TTVetoTwoTag_Signal",labels=labelNames,x_min=300,x_max=1000,xlabel="m_{4j} [GeV]",rebin=2,doratio=0)

rebins_m4j_l = [400,460,520,580,640,700,800,900,1000,1300,2000]#[100,140,180,220,260,300,340,380,420,460,500,540,600,660,720,800,900,1000,1240,2000] # for bins in 20
plot(["m4j_cor_l","m4j_l"],"TTVetoTwoTag_Signal",labels=labelNames,xlabel="m_{4j} [GeV]",rebin=rebins_m4j_l,doratio=1)
