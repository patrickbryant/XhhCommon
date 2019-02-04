
import ROOT
import sys
import os
import optparse
from array import array
import math
parser = optparse.OptionParser()

parser.add_option('-i', '--in',                  dest="inFile", default="Data0/hist-tree.root")
parser.add_option('--bkgCR',      dest="bkgCRFileName",default="")
parser.add_option('--shapeFile',  dest="shapeFileName",default="")
parser.add_option('-o', '--outDir',dest="outDir",default="./")
parser.add_option('-f', '--folder',dest="folder",default="TTVeto")
parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
parser.add_option('-q', '--qcdFile',            dest="qcdFileName",         default="", help="")
parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",        default="", help="")
parser.add_option('-l', '--limitsFile',         dest="limitsFileName",        default="", help="")

o, a = parser.parse_args()


#
#
#
def readBkgFileCR(inFileName):
    inFile = open(inFileName,"r")
    bkgs = {}
    for line in inFile:
        words =  line.split()
        if not len(words): continue

        if words[0] == "QCD": 
            bkgs["QCD"]    = float(words[10])
            bkgs["QCDErr"] = float(words[12].rstrip("\\"))
        if words[0] == "\\ttbar":
            bkgs["ttbar"]    = float(words[10])
            bkgs["ttbarErr"] = float(words[12].rstrip("\\"))
    inFile.close()
    return bkgs


def doBkgHistCR(inFile, histName, norm, name):
    hist =  inFile.Get(histName)
    hist.Sumw2()
    rawIntegral = hist.Integral()
    hist.Scale(norm/rawIntegral)
    hist.SetName(name)
    hist.Write()

def doBkgHistSR(inFile, histName, varNames, name):
    hist =  inFile.Get(histName)
    hist.SetName(name)

    hist_up =  ROOT.TH1F(hist)
    hist_up.SetName(name+"_up")

    hist_down =  ROOT.TH1F(hist)
    hist_down.SetName(name+"_down")

    varHists = []
    for v in varNames:
        varHists.append(inFile.Get(v))

    nBins = hist.GetNbinsX()

    for i in range(nBins):
        nomY        = hist.GetBinContent(i+1)
        nomYErr     = hist.GetBinError  (i+1)

        upTotal2   = (nomYErr*nomYErr)
        downTotal2 = (nomYErr*nomYErr)

        for vHist in varHists:
            thisY = vHist.GetBinContent(i+1)
            thisDiff =  nomY - thisY
            if thisDiff > 0:
                upTotal2   += (thisDiff*thisDiff)
            else:
                downTotal2 += (thisDiff*thisDiff)

        hist_up   .SetBinContent(i+1, nomY + pow(upTotal2,  0.5))
        hist_down .SetBinContent(i+1, nomY - pow(downTotal2,0.5))


    hist     .Write()
    hist_up  .Write()
    hist_down.Write()


def doSignalHist(inFile, histName, name):
    hist =  inFile.Get(histName)
    hist.SetName(name)
    hist.Write()

def doDataHist(inFile, histName, name):
    hist  =  inFile.Get(histName)
    hist.SetBinErrorOption(1)
    #hist.SetName("data_hh_hist")
    #hist.Write()

    nBins = hist.GetNbinsX()

    dataGr = ROOT.TGraphAsymmErrors(nBins)
    dataGr.SetName("data_hh")
    for i in range(nBins):
        thisX        = hist.GetBinCenter(i+1)
        thisY        = hist.GetBinContent(i+1)
        if thisY:
            thisYErrLow  = hist.GetBinErrorLow(i+1)
            thisYErrUp   = hist.GetBinErrorUp(i+1)
        else:
            thisYErrLow = 0
            thisYErrUp  = 0
        #print i, thisX, thisY, thisYErrLow, thisYErrUp
        dataGr.SetPoint(i,thisX, thisY)
        dataGr.SetPointError(i,0, 0, thisYErrLow, thisYErrUp)

    dataGr.Write()



#
#def makeShapeUncertianties(name, inFile, bkg, shapeFile, dir, vars, symmetrize=False):
#
#    canObj = shapeFile.Get("can_"+name)
#    
#    fit = canObj.FindObject(name+"_fit")
#    p1  = fit.GetParameter(1)
#    e1  = fit.GetParError(1)
#    
#    fitUp   = canObj.FindObject(name+"_fitUp")
#    p0Up    = fitUp  .GetParameter(0)
#
#
#    fitDown  = canObj.FindObject(name+"_fitDown")
#    p0Down = fitDown.GetParameter(0)
#
#    for h in ["m4j25_cor"]:#,"m4j50_cor"]:
#
#        
#        hShapeUp = inFile.Get(dir+"/"+h)
#        hShapeUp.Sumw2()
#        hShapeUp.SetName(h+"_"+name+"_hh_"+vars[0])
#
#        hShapeDown  = ROOT.TH1F(hShapeUp)
#        hShapeDown.SetName(h+"_"+name+"_hh_"+vars[1])
#
#        for bin in range(hShapeUp.GetNbinsX()+1):
#            x     = hShapeUp.GetXaxis().GetBinCenter(bin)
#
#            yUp   = ( p0Up   + (p1+e1)*x )*hShapeUp.GetBinContent(bin)
#            if symmetrize:
#                yDown = ( p0Down - (p1+e1)*x )*hShapeUp.GetBinContent(bin)
#            else:
#                yDown = ( p0Down + (p1-e1)*x )*hShapeUp.GetBinContent(bin)
#                
#            if yDown < 0: yDown = 0
#            if yUp   < 0: yUp   = 0
#
#            hShapeUp  .SetBinContent(bin, yUp)
#            hShapeDown.SetBinContent(bin, yDown)
#
#        hShapeUp.Scale(bkg/hShapeUp.Integral())
#        hShapeUp = killNegativeBins(hShapeUp)
#        hShapeUp.Write()
#
#        hShapeDown.Scale(bkg/hShapeDown.Integral())
#        hShapeDown = killNegativeBins(hShapeDown)
#        hShapeDown.Write()
#
#
#    return
#
##
##
##
#
#def makeSignalBTaggingUncertianties(signalFile, samples):
#    
#    btagSFNames = ["FT_EFF_Eigen_B_0__1down","FT_EFF_Eigen_B_0__1up",
#                   "FT_EFF_Eigen_B_1__1down","FT_EFF_Eigen_B_1__1up",
#                   "FT_EFF_Eigen_B_2__1down","FT_EFF_Eigen_B_2__1up",
#                   "FT_EFF_Eigen_B_3__1down","FT_EFF_Eigen_B_3__1up",
#                   "FT_EFF_Eigen_B_4__1down","FT_EFF_Eigen_B_4__1up",
#                   "FT_EFF_Eigen_C_0__1down","FT_EFF_Eigen_C_0__1up",
#                   "FT_EFF_Eigen_C_1__1down","FT_EFF_Eigen_C_1__1up",
#                   "FT_EFF_Eigen_C_2__1down","FT_EFF_Eigen_C_2__1up",
#                   "FT_EFF_Eigen_C_3__1down","FT_EFF_Eigen_C_3__1up",
#                   "FT_EFF_Eigen_Light_0__1down","FT_EFF_Eigen_Light_0__1up",
#                   "FT_EFF_Eigen_Light_1__1down","FT_EFF_Eigen_Light_1__1up",
#                   "FT_EFF_Eigen_Light_10__1down","FT_EFF_Eigen_Light_10__1up",
#                   "FT_EFF_Eigen_Light_11__1down","FT_EFF_Eigen_Light_11__1up",
#                   "FT_EFF_Eigen_Light_12__1down","FT_EFF_Eigen_Light_12__1up",
#                   "FT_EFF_Eigen_Light_13__1down","FT_EFF_Eigen_Light_13__1up",
#                   "FT_EFF_Eigen_Light_2__1down","FT_EFF_Eigen_Light_2__1up",
#                   "FT_EFF_Eigen_Light_3__1down","FT_EFF_Eigen_Light_3__1up",
#                   "FT_EFF_Eigen_Light_4__1down","FT_EFF_Eigen_Light_4__1up",
#                   "FT_EFF_Eigen_Light_5__1down","FT_EFF_Eigen_Light_5__1up",
#                   "FT_EFF_Eigen_Light_6__1down","FT_EFF_Eigen_Light_6__1up",
#                   "FT_EFF_Eigen_Light_7__1down","FT_EFF_Eigen_Light_7__1up",
#                   "FT_EFF_Eigen_Light_8__1down","FT_EFF_Eigen_Light_8__1up",
#                   "FT_EFF_Eigen_Light_9__1down","FT_EFF_Eigen_Light_9__1up",
#                   "FT_EFF_extrapolation__1down","FT_EFF_extrapolation__1up",
#                   "FT_EFF_extrapolation from charm__1down","FT_EFF_extrapolation from charm__1up",
#                   ]
#
#
#    for bSF in btagSFNames:
#        for samp in samples:
#            for h in ["m4j25_cor"]:#,"m4j50_cor"]:
#                sigHist = signalFile.Get(h+"_"+samp+"_"+bSF)
#                sigHist.Write()
#
#    return 
#
#


    


if __name__ == "__main__":

    #
    # Get the input files
    #
    qcdFile    = ROOT.TFile(o.qcdFileName,   "READ")
    ttbarFile  = ROOT.TFile(o.ttbarFileName, "READ")
    shapeFile  = ROOT.TFile(o.shapeFileName, "READ")
    dataFile   = ROOT.TFile(o.dataFileName,  "READ")
    limitsFile = ROOT.TFile(o.limitsFileName,"READ")

    #if os.path.exists(o.outDir+"/resolvedLimitInputs.root"):
    #    out = ROOT.TFile.Open(o.outDir+"/resolvedLimitInputs.root", "UPDATE")
    #else:

    #
    #  Get bkgs and uncertianties
    #
    bkgsCR = readBkgFileCR(o.bkgCRFileName)

    #
    #  Do the Control Region
    #
    outCR = ROOT.TFile.Open(o.outDir+"/resolved_4b_m4j_CR.root", "RECREATE")

    doDataHist(dataFile, "TTVetoFourTag_Control/m4j_l", "data_hh")
    doBkgHistCR(qcdFile,    "TTVetoTwoTag_Control/m4j_l",   bkgsCR["QCD"]  ,    "qcd_hh")
    doBkgHistCR(ttbarFile,  "TTVetoTwoTag_Control/m4j_l",   bkgsCR["ttbar"],    "ttbar_hh")

    shapeFile.Get("can_qcd").FindObject("qcd_fit")    .Write()
    shapeFile.Get("can_qcd").FindObject("qcd_fitUp")  .Write()
    shapeFile.Get("can_qcd").FindObject("qcd_fitDown").Write()
    
    outCR.Write()

    #
    # Do the Signal Region
    #
    outSR = ROOT.TFile.Open(o.outDir+"/resolved_4b_m4j_SR.root", "RECREATE")

    doDataHist(limitsFile, "m4j25_cor_data_hh", "data_hh")



    doBkgHistSR(limitsFile,    "m4j25_cor_qcd_hh",   ["m4j25_cor_qcd_hh_QCDUp", "m4j25_cor_qcd_hh_QCDDown", 
                                                      "m4j25_cor_qcd_hh_QCDShapeUp", "m4j25_cor_qcd_hh_QCDShapeDown"],    
                "qcd_hh")
    

    doBkgHistSR(limitsFile,    "m4j25_cor_ttbar_hh",    ["m4j25_cor_ttbar_hh_TTBarUp","m4j25_cor_ttbar_hh_TTBarDown",
                                                         "m4j25_cor_ttbar_hh_TTBarShapeUp","m4j25_cor_ttbar_hh_TTBarShapeDown",],
                "ttbar_hh")


    doSignalHist(limitsFile, "m4j25_cor_RSG_c10_M800", "signal_hh")

    outSR.Write()



    
#    makeNormUncertianties ("qcd",qcdFile,     bkgs["QCD"],  bkgs["QCDErr"],"TTVetoTwoTag_Signal", ["QCDUp","QCDDown"])
#    makeShapeUncertianties("qcd",qcdFile,     bkgs["QCD"], shapeFile,      "TTVetoTwoTag_Signal", ["QCDShapeUp","QCDShapeDown"])
#
#    #
#    #  Make ttbar inputs
#    #
#    makeNormUncertianties("ttbar", ttbarFile, bkgs["ttbar"], bkgs["ttbarErr"],"TTVetoTwoTag_Signal", ["TTBarUp","TTBarDown"])
#    makeShapeUncertianties("ttbar",ttbarFile, bkgs["ttbar"], shapeFile,       "TTVetoTwoTag_Signal", ["TTBarShapeUp","TTBarShapeDown"])
#
#    #
#    # Make signal JES/JER
#    #
#    
#    samples = ["RSG_c05_M500", "RSG_c05_M1000",
#               "RSG_c10_M400","RSG_c10_M500","RSG_c10_M600","RSG_c10_M700","RSG_c10_M800","RSG_c10_M900","RSG_c10_M1000",
#               "RSG_c10_M1200","RSG_c10_M1300","RSG_c10_M1400","RSG_c10_M1500", "RSG_c10_M1100",
#               "RSG_c20_M400","RSG_c20_M500","RSG_c20_M600","RSG_c20_M700","RSG_c20_M800","RSG_c20_M900","RSG_c20_M1000",
#               "RSG_c20_M1100","RSG_c20_M1200","RSG_c20_M1300","RSG_c20_M1400", "RSG_c20_M1500",
#               "Hhh_M400","Hhh_M500","Hhh_M600","Hhh_M700","Hhh_M800","Hhh_M900","Hhh_M1000","Hhh_M1100","Hhh_M1200","Hhh_M1300","Hhh_M1400"
#               ]
#
#
#
#    #
#    #  Add data distribution
#    #
#    makeObservedData ("data",dataFile,"TTVetoFourTag_Signal")    


