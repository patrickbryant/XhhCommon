from iPlot import loadPath
loadPath()
from utils import parseOpts, getPM, setBatch, plot

setBatch()
(o,a) = parseOpts()
pm = getPM(o)

import ROOT

plot(["eff_c3_Data","eff_c3_MC"],"BeforeMh_Eta",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Eta",ylabel="Inferred #epsilon",labels=["Data","MC"])#,plotName="BeforeEtaFromc2")
plot(["eff_c3_Data","eff_c3_MC"],"AfterMh_Eta",doratio=1,rMax=1.5,rMin=0.5, min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Eta",ylabel="Inferred #epsilon",labels=["Data","MC"])#,plotName="AfterEtaFromc2")

plot(["eff_c3_Data","eff_c3_MC"],"BeforeMh_Pt",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,x_min=200,x_max=700,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Pt[GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"])#,plotName="BeforePtFromc2")
plot(["eff_c3_Data","eff_c3_MC"],"AfterMh_Pt",doratio=1,rMax=1.5,rMin=0.5, min=0,max=1.5,x_min=200,x_max=700,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Pt[GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"])#,plotName="AfterPtFromc2")

#plot(["eff_c3_Data","eff_c3_MC"],"BeforeMh_Mass",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Mass[GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"],plotName="BeforePtFromc3")
#plot(["eff_c3_Data","eff_c3_MC"],"AfterMh_Mass",doratio=1,rMax=1.5,rMin=0.5, min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Mass[GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"],plotName="AfterPtFromc3")


plot(["eff_c3_Data","eff_c3_MC"],"BeforeMh_sublJet_Pt_m",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="Subl Jet Pt [GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"],plotName="BeforePtFromc3")
plot(["eff_c3_Data","eff_c3_MC"],"BeforeMh_leadJet_Pt_m",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="Lead Jet Pt [GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"],plotName="BeforePtFromc3")

plot(["eff_c3_Data","eff_c3_MC"],"AfterMh_sublJet_Pt_m",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="Subl Jet Pt [GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"],plotName="BeforePtFromc3")
plot(["eff_c3_Data","eff_c3_MC"],"AfterMh_leadJet_Pt_m",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="Lead Jet Pt [GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"],plotName="BeforePtFromc3")

#plot(["eff_c3_Data","eff_c3_MC"],"BeforeMh_DiJet_CloseJet_Pt_l",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="Close Jet Pt [GeV]",ylabel="Inferred #epsilon",labels=["Data","MC"],plotName="BeforePtFromc3")





