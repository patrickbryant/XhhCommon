from iPlot import loadPath
loadPath()

from utils import parseOpts, getPM, setBatch, comp

setBatch()
(o,a) = parseOpts()
pm = getPM(o)


def doHCand(candName, HadRegion, LepRegion):
    comp([candName+"_Mass","hCand_Mass"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2,min=0)
    comp([candName+"_Pt_m","hCand_Pt_m"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2)
    comp([candName+"_Eta","hCand_Eta"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2)
    comp([candName+"_dRjj","hCand_dRjj"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=2,doratio=1,rMin=0.,rMax=2,min=0,x_max=2)
    comp([candName+"_mW","hCand_mW"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2,min=0)
    comp([candName+"_mTop","hCand_mTop"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2,min=0)

    comp([candName+"_leadJet_Pt","hCand_leadJet_Pt"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2)
    comp([candName+"_leadJet_Eta","hCand_leadJet_Eta"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2)
    comp([candName+"_sublJet_Pt","hCand_sublJet_Pt"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2)
    comp([candName+"_sublJet_Eta","hCand_sublJet_Eta"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.,rMax=2)




#   # 
#   # Lead HCand
#   #
#   comp(["leadHCand_Mass","DiJet_Mass"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2,min=0)
#   comp(["leadHCand_Pt_m","DiJet_Pt"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   comp(["leadHCand_Eta","DiJet_Eta"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   comp(["leadHCand_dRjj","DiJet_dRjj"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2,min=0)
#   comp(["leadHCand_mW","DiJet_Mcj"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2,min=0)
#   comp(["leadHCand_mTop","DiJet_Mbcj"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2,min=0)
#   
#   comp(["DiJet_LeadJet_Eta","DiJet_LeadJet_Eta"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   comp(["DiJet_LeadJet_Pt_l","DiJet_LeadJet_Pt_l"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   comp(["DiJet_LeadJet_MV1","DiJet_LeadJet_MV1"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   comp(["DiJet_LeadJet_JVF","DiJet_LeadJet_JVF"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=1,doratio=1,rMin=0.5,rMax=2,x_min=-1.1,x_max=1.1,min=0)
#   
#   comp(["DiJet_SublJet_Eta","DiJet_SublJet_Eta"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   comp(["DiJet_SublJet_Pt_l","DiJet_SublJet_Pt_l"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   comp(["DiJet_SublJet_MV1","DiJet_SublJet_MV1"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   comp(["DiJet_SublJet_JVF","DiJet_SublJet_JVF"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=1,doratio=1,rMin=0.5,rMax=2,x_min=-1.1,x_max=1.1,min=0)
#   
#   
#   #
#   #  Close Jets (combined)
#   # 
#   #comp(["DiJet_nCloseJets","DiJet_nCloseJets"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=1,doratio=1,rMin=0.5,rMax=2,min=0)
#   #comp(["DiJet_CloseJet_Pt_l","DiJet_CloseJet_Pt_l"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   #comp(["DiJet_CloseJet_Eta","DiJet_CloseJet_Eta"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   #comp(["DiJet_CloseJet_dR","DiJet_CloseJet_dR"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   #comp(["DiJet_CloseJet_MV1","DiJet_CloseJet_MV1"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=1,doratio=1,rMin=0.5,rMax=2,x_min=-0.1,x_max=1.1,min=0)
#   #comp(["DiJet_CloseJet_JVF","DiJet_CloseJet_JVF"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=1,doratio=1,rMin=0.5,rMax=2,x_min=-1.1,x_max=1.1,min=0)
#   
#   
#   #
#   #  Close Jets (Lead)
#   # 
#   #comp(["LeadDiJet_nCloseJets","LeadDiJet_nCloseJets"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=1,doratio=1,rMin=0.5,rMax=2,min=0)
#   #comp(["LeadDiJet_CloseJet_Pt_l","LeadDiJet_CloseJet_Pt_l"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   #comp(["LeadDiJet_CloseJet_Eta","LeadDiJet_CloseJet_Eta"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   #comp(["LeadDiJet_CloseJet_dR","LeadDiJet_CloseJet_dR"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#   #comp(["LeadDiJet_CloseJet_MV1","LeadDiJet_CloseJet_MV1"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=1,doratio=1,rMin=0.5,rMax=2,x_min=-0.1,x_max=1.1,min=0)
#   #comp(["LeadDiJet_CloseJet_JVF","LeadDiJet_CloseJet_JVF"],[HadRegion,LepRegion],norm=1,labels=["Hadronic tt (Di-Jet+Di-Jet)","Semi-Lep tt (Di-Jet + Lep-Top)"],rebin=1,doratio=1,rMin=0.5,rMax=2,x_min=-1.1,x_max=1.1,min=0)



doHCand("sublHCand","PassTrigFourTag_Inclusive","PtLepTop_mub100")
doHCand("allHCand", "PassTrigFourTag_Inclusive","PtLepTop_mub200")






