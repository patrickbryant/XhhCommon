from iPlot import loadPath
loadPath()

from utils import parseOpts, getPM, setBatch, comp

setBatch()
(o,a) = parseOpts()
pm = getPM(o)


# 
# Lep-Top
#
ttSLCRDir = "PtLepTop_mub100"

norm = 0

comp("lepTop_Pt_m",          ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0,x_min=0,x_max=800)
comp("lepTop_Eta",           ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0)
                             
                             
# Jet                        
comp("lepTop_jet_Pt",        ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0)
comp("lepTop_jet_MV2c20",    ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0,x_min=-0.1 ,x_max=1.1)
comp("lepTop_jet_Jvt",       ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=1,doratio=1,rMin=0.,rMax=2,min=0,x_min=0.5,  x_max=1.1)

# Muon 
comp("lepTop_muon_Pt_l",     ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=4,doratio=1,rMin=0.,rMax=2,min=0)
comp("lepTop_muon_ptcone20", ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=2,doratio=1,rMin=0.,rMax=2,min=1e-1,logy=1)

# Met
comp("lepTop_mT",            ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0)
comp("lepTop_meT_l",         ttSLCRDir, norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0)


# 
# Di-Jet Side
#

comp("hCand_Mass",           ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0)
comp("hCand_Pt_m",           ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2)
comp("hCand_Eta",            ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2)
comp("hCand_dRjj",           ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=2,doratio=1,rMin=0.,rMax=2,min=0, x_max=2)
comp("hCand_mW",             ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0)
comp("hCand_mTop",           ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0)
comp("hCand_Xtt",            ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,min=0)

comp("hCand_leadJet_Eta",    ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2)
comp("hCand_leadJet_Pt",     ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2)
comp("hCand_leadJet_MV2c20", ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2)
comp("hCand_leadJet_Jvt",    ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,x_min=-0.1,x_max=1.1,min=0)

comp("hCand_sublJet_Eta",    ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2)
comp("hCand_sublJet_Pt",     ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2)
comp("hCand_sublJet_MV2c20", ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2)
comp("hCand_sublJet_Jvt",    ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=3,doratio=1,rMin=0.,rMax=2,x_min=-0.1,x_max=1.1,min=0)


comp("nJetOther",            ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=1,doratio=1,rMin=0.5,rMax=2,min=0)

#
#  Close Jets (combined)
# 
#comp(["DiJet_nCloseJets",   "DiJet_nCloseJets"],ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=1,doratio=1,rMin=0.5,rMax=2,min=0)
#comp(["DiJet_CloseJet_Pt_l","DiJet_CloseJet_Pt_l"],ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#comp(["DiJet_CloseJet_Eta", "DiJet_CloseJet_Eta"],ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#comp(["DiJet_CloseJet_dR",  "DiJet_CloseJet_dR"],ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=4,doratio=1,rMin=0.5,rMax=2)
#comp(["DiJet_CloseJet_MV1", "DiJet_CloseJet_MV1"],ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=1,doratio=1,rMin=0.5,rMax=2,x_min=-0.1,x_max=1.1,min=0)
#comp(["DiJet_CloseJet_JVF", "DiJet_CloseJet_JVF"],ttSLCRDir,norm=norm,labels=["Data (TT-CR)","MC (TT-CR)"],rebin=1,doratio=1,rMin=0.5,rMax=2,x_min=-1.1,x_max=1.1,min=0)











