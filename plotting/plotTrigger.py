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


rMin = 0.7

trigDir   = "TTVetoFourTag_Signal"
noTrigDir = "TTVetoNoTrigFourTag_Signal"

#trigDir   = "PassTrigFourTag_Inclusive"
#noTrigDir = "FourTag_Inclusive"

plot("leadHCand_Pt",[trigDir,noTrigDir],x_min=200,x_max=400,doratio=1,rMin=rMin,rMax=1.2,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,min=0)
plot("leadHCand_Pt_m",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,x_min=200,x_max=800,min=0)

plot("leadHCand_Mass",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=1,x_min=50,x_max=200,min=0)
plot("leadHCand_leadJet_Pt",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=3,x_min=50,x_max=400,min=0)
plot("leadHCand_leadJet_Pt_m",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,x_min=100,x_max=700,min=0)
#plot("leadHCand_sublJet_Pt",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,x_min=20,x_max=250)
plot("leadHCand_sublJet_Pt",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,x_min=30,x_max=300,min=0)


plot("sublHCand_Pt",[trigDir,noTrigDir],x_min=150,x_max=300,doratio=1,rMin=rMin,rMax=1.2,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,min=0)
plot("sublHCand_Pt_m",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,x_min=150,x_max=700,min=0)

plot("sublHCand_Mass",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=1,x_min=50,x_max=200,min=0)
plot("sublHCand_leadJet_Pt",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=3,x_min=50,x_max=400,min=0)
plot("sublHCand_sublJet_Pt",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,x_min=20,x_max=250,min=0)

plot("m4j",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,x_min=400,x_max=800,min=0)
plot("m4j_l",[trigDir,noTrigDir],doratio=1,rMin=rMin,rMax=1.05,bayesRatio=1,labels=["PassTrigger","No Trigger Cut"],rebin=2,x_min=500,x_max=1500,min=0)

