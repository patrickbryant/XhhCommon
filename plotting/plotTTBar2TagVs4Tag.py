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

labelNames=["TTbar 4-Tag","TTbar 2-Tag"]

def doRegion(regNames):
    

    #plot("leadHCand_Pt",regNames,x_min=200,x_max=800,doratio=1,rMin=rMin,rMax=1.2,labels=labelNames,rebin=2,norm=1)
    plot("leadHCand_Pt_m",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=[150,200,220,240,260,280,300,340,380,420,500,600,700],norm=1)
    plot("sublHCand_Pt_m",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=[100,140,160,180,200,220,240,260,280,300,340,380,420,500,600,700],norm=1)

    plot("leadHCand_dRjj",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,norm=1,x_max=2,x_min=0)
    plot("sublHCand_dRjj",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,norm=1,x_max=2,x_min=0)


    plot("leadHCand_Mass",        regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,x_min=0,x_max=300,norm=1)
    plot("leadHCand_leadJet_Pt",  regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=3,x_min=50,x_max=400,norm=1)
    plot("leadHCand_leadJet_Pt_m",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,x_min=100,x_max=700,norm=1)
    #plot("leadHCand_sublJet_Pt",  regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,x_min=20,x_max=250,norm=1)
    plot("leadHCand_sublJet_Pt",  regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,x_min=30,x_max=300,norm=1)
    
    
    #plot("sublHCand_Pt",regNames,x_min=150,x_max=300,doratio=1,rMin=rMin,rMax=1.2,labels=labelNames,,norm=1)

    
    plot("sublHCand_Mass",      regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,x_min=0,x_max=300,norm=1)
    plot("sublHCand_leadJet_Pt",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=3,x_min=50,x_max=400,norm=1)
    plot("sublHCand_sublJet_Pt",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,x_min=20,x_max=250,norm=1)
    
    #plot("m4j",  regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=2,x_min=400,x_max=2000,norm=1)
    plot("m4j_l",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=[400,500,600,700,800,900,1100,1500,2000],x_min=400,x_max=2000,norm=1,plotPreFix="coarse")
    plot("m4j_l",regNames,doratio=1,rMin=rMin,rMax=2,labels=labelNames,rebin=8,x_min=400,x_max=2000,norm=1,logy=1)
    


doRegion(["PassTrigFourTag_Inclusive","PassTrigTwoTag_Inclusive"])
doRegion(["TTVetoFourTag_Signal",     "TTVetoTwoTag_Signal"])
