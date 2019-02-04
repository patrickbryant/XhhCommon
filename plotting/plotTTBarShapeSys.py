from iPlot import loadPath
loadPath()
from utils import parseOpts, getPM, setBatch, plot

setBatch()
(o,a) = parseOpts()
pm = getPM(o)

import ROOT


plot(["m4j_l_ttbar_ShapeUp",  "m4j_l_ttbar",],  "",doratio=1,min=0,labels=["Up    ","Nominal"]  ,rMin = 0, rMax =2, max =0.5)
plot(["m4j_l_ttbar_ShapeDown","m4j_l_ttbar",],  "",doratio=1,min=0,labels=["Down  ","Nominal"],rMin = 0, rMax =2, max =0.5)

plot(["m4j_l_qcd_ShapeUp",  "m4j_l_qcd",],  "",doratio=1,min=0,labels=["Up  ","Nominal"]  ,rMin = 0, rMax =2)#, max =10.5)
plot(["m4j_l_qcd_ShapeDown","m4j_l_qcd",],  "",doratio=1,min=0,labels=["Down","Nominal"],rMin = 0, rMax =2)#, max =10.5)

