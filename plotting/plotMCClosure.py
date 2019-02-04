from iPlot import loadPath
loadPath()
from utils import parseOpts, getPM, setBatch, plot

setBatch()
(o,a) = parseOpts()
pm = getPM(o)

import ROOT

plot(["eff_c1","eff_c2"],"BeforeMh_Eta",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Eta",ylabel="Inferred #epsilon",labels=["from c1","from c2"],plotName="BeforeEtaFromc2")
plot(["eff_c1","eff_c2"],"AfterMh_Eta",doratio=1,rMax=1.5,rMin=0.5, min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Eta",ylabel="Inferred #epsilon",labels=["from c1","from c2"],plotName="AfterEtaFromc2")

plot(["eff_c1","eff_c2"],"BeforeMh_Pt",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,x_max=700,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Pt[GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c2"],plotName="BeforePtFromc2")
plot(["eff_c1","eff_c2"],"AfterMh_Pt",doratio=1,rMax=1.5,rMin=0.5, min=0,max=1.5,x_max=700,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Pt[GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c2"],plotName="AfterPtFromc2")


plot(["eff_c1","eff_c3"],"BeforeMh_Eta",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Eta",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="BeforeEtaFromc3")
plot(["eff_c1","eff_c3"],"AfterMh_Eta",doratio=1,rMax=1.5,rMin=0.5, min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Eta",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="AfterEtaFromc3")

plot(["eff_c1","eff_c3"],"BeforeMh_Pt",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,x_max=700,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Pt[GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="BeforePtFromc3")
plot(["eff_c1","eff_c3"],"AfterMh_Pt",doratio=1,rMax=1.5,rMin=0.5, min=0,max=1.5,x_max=700,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Pt[GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="AfterPtFromc3")


plot(["eff_c1","eff_c3"],"BeforeMh_Mass",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Mass[GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="BeforePtFromc3")
plot(["eff_c1","eff_c3"],"AfterMh_Mass",doratio=1,rMax=1.5,rMin=0.5, min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="DiJet Mass[GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="AfterPtFromc3")


plot(["eff_c1","eff_c3"],"BeforeMh_sublJet_Pt_m",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="Subl Jet Pt [GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="BeforePtFromc3")
plot(["eff_c1","eff_c3"],"BeforeMh_leadJet_Pt_m",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="Lead Jet Pt [GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="BeforePtFromc3")
#plot(["eff_c1","eff_c3"],"BeforeMh_DiJet_CloseJet_Pt_l",doratio=1,rMax=1.5,rMin=0.5,min=0,max=1.5,draw_options=["LPE","E2"],line_colors=[1,ROOT.kYellow],xlabel="Close Jet Pt [GeV]",ylabel="Inferred #epsilon",labels=["from c1","from c3"],plotName="BeforePtFromc3")





