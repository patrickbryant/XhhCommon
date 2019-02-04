# Calculate e from different inputs
import ROOT

from optparse import OptionParser
from collections import OrderedDict
import array
p = OptionParser()
p.add_option('--had',  type = 'string', default = "", dest = 'inputHadFile', help = 'intput HadHad File' )
p.add_option('--lep',  type = 'string', default = "", dest = 'inputLepFile', help = 'intput LepHad File' )
p.add_option('--out',  type = 'string', default = "", dest = 'outFileName',  help = 'output File' )
(o,a) = p.parse_args()


inFileHad = ROOT.TFile(o.inputHadFile,"READ")
inFileLep = ROOT.TFile(o.inputLepFile,"READ")

outFile      = ROOT.TFile(o.outFileName,"RECREATE")

binDict = {}
binDict["Pt"] = [125,150,175,200,225,250,300,400,700]
binDict["Eta"] = [-2.5,-1.5,-1.0,-0.5,0,0.5,1.0,1.5,2.5]
binDict["leadJet_Pt_m"] = [0,100,125,150,175,200,300,400]
binDict["sublJet_Pt_m"] = [0,40,60,80,100,150,400]


def getNum(infile,histName):
    hist = infile.Get(histName)
    return hist.GetEntries()

def printLine(oFile,line):
    print line
    oFile.write(line+"\n")


def pNum(num):
    return str(int(num))

def pFloat(num,rNum):
    return str(round(float(num),rNum))

def divideCorrelated(numHist, denHist):
    rHist = ROOT.TH1F(numHist)
    for i in range(numHist.GetNbinsX()):
        #print i+1
        #print "\t Npp:",round(Npp.GetBinContent(i+1),3),"+/-",round(Npp.GetBinError(i+1),3),
        #print "\t NhadTot:",round(NhadTot.GetBinContent(i+1),3),"+/-",round(NhadTot.GetBinError(i+1),3),
        #print "\t c1:",round(c1.GetBinContent(i+1),3),"+/-",round(c1.GetBinError(i+1),3),
        thisNum  = numHist.GetBinContent(i+1)
        thisDen = denHist.GetBinContent(i+1)
        if thisDen:
            r = thisNum/thisDen
            rErr = pow(r*(1-r) / thisDen, 0.5)
            rHist.SetBinContent(i+1, r)
            rHist.SetBinError(i+1, rErr)
        else:
            rHist.SetBinContent(i+1, 0)
            rHist.SetBinError(i+1, 0)
            #print "\t mine:",round(myc1,3),"+/-",round(myc1Err,3),
        #print 
    return rHist



def makeTables(bNum, aNum):

    outTxtFileC1C2   = open(o.outFileName.replace(".root","_c1c2.tex"),"w")

    printLine(outTxtFileC1C2, "\\begin{tabular}{ c | c | c  }")
    printLine(outTxtFileC1C2, "Observable  & Before $m_h$ cut & After $m_h$  \\\\")
    printLine(outTxtFileC1C2, "\hline")
    printLine(outTxtFileC1C2, "$N_{PP}$ & "+pNum(bNum["Npp"])+" & "+pNum(aNum["Npp"])+" \\\\")
    printLine(outTxtFileC1C2, "$N_{PF}$ & "+pNum(bNum["Npf"])+" & "+pNum(aNum["Npf"])+" \\\\")
    printLine(outTxtFileC1C2, "$N_{FF}$ & "+pNum(bNum["Nff"])+" & "+pNum(aNum["Nff"])+" \\\\")
    printLine(outTxtFileC1C2, "$c1    $ & "+pFloat(bNum["c1" ],3)+" $\pm$ "+pFloat(bNum["c1Err" ],4)+" & "+pFloat(aNum["c1"],3)+" $\pm$ "+pFloat(aNum["c1Err"],3)+" \\\\")
    printLine(outTxtFileC1C2, "$c2    $ & "+pFloat(bNum["c2" ],3)+" $\pm$ "+pFloat(bNum["c2Err" ],4)+" & "+pFloat(aNum["c2"],3)+" $\pm$ "+pFloat(aNum["c2Err"],3)+" \\\\")
    printLine(outTxtFileC1C2, "\hline")
    printLine(outTxtFileC1C2, "$\epsilon$ from $c1$ & "+pFloat(bNum["eff_c1" ],3)+" $\pm$ "+pFloat(bNum["eff_c1_err" ],4)+" & "+pFloat(aNum["eff_c1"],3)+" $\pm$ "+pFloat(aNum["eff_c1_err"],3)+" \\\\")
    printLine(outTxtFileC1C2, "$\epsilon$ from $c2$ & "+pFloat(bNum["eff_c2" ],3)+" $\pm$ "+pFloat(bNum["eff_c2_err" ],4)+" & "+pFloat(aNum["eff_c2"],3)+" $\pm$ "+pFloat(aNum["eff_c2_err"],3)+" \\\\")
    printLine(outTxtFileC1C2, "\end{tabular}    ")

    outTxtFileC1C2C3 = open(o.outFileName.replace(".root","_c1c2c3.tex"),"w")

    printLine(outTxtFileC1C2C3, "\\begin{tabular}{ c | c | c  }")
    printLine(outTxtFileC1C2C3, "Observable  & Before $m_h$ & After $m_h$  \\\\")
    printLine(outTxtFileC1C2C3, "\hline")
    printLine(outTxtFileC1C2C3, "$N_{P}$ & "+pNum(bNum["Np"])+" & "+pNum(aNum["Np"])+" \\\\")
    printLine(outTxtFileC1C2C3, "$N_{F}$ & "+pNum(bNum["Nf"])+" & "+pNum(aNum["Nf"])+" \\\\")
    printLine(outTxtFileC1C2C3, "$\epsilon$ from $c3$ & "+pFloat(bNum["c3" ],3)+" $\pm$ "+pFloat(bNum["c3Err" ],4)+" & "+pFloat(aNum["c3"],3)+" $\pm$ "+pFloat(aNum["c3Err"],3)+" \\\\")
    printLine(outTxtFileC1C2C3, "\hline")
    printLine(outTxtFileC1C2C3, "$\epsilon$ from $c1$ & "+pFloat(bNum["eff_c1" ],3)+" $\pm$ "+pFloat(bNum["eff_c1_err" ],4)+" & "+pFloat(aNum["eff_c1"],3)+" $\pm$ "+pFloat(aNum["eff_c1_err"],3)+" \\\\")
    printLine(outTxtFileC1C2C3, "$\epsilon$ from $c2$ & "+pFloat(bNum["eff_c2" ],3)+" $\pm$ "+pFloat(bNum["eff_c2_err" ],4)+" & "+pFloat(aNum["eff_c2"],3)+" $\pm$ "+pFloat(aNum["eff_c2_err"],3)+" \\\\")
    printLine(outTxtFileC1C2C3, "\end{tabular}")


def getHist(infile,histName):
    hist = infile.Get(histName)
    for v in binDict.keys():
        if histName.split("/")[-1].find(v) != -1:
            bins = binDict[v]
            #print "Found",v,histName
            xBins = array.array("d", bins)
            histNew = hist.Rebin(len(bins) - 1,  hist.GetName()+"_rebinned", xBins)

            return histNew

    hist.Rebin(4)
    return hist

def getErrEffC1(c1, c1Err):
    den = 2*pow(c1,0.5)
    if den:
        err = c1Err / den
    else:
        err = 0 
    return err


def getErrEffC2(c2, c2Err):

    if (4 - 8*c2)<0:
        c2 = (c2 - c2Err)
        if (4 - 8*c2)<0:
            return 0
    discrim = pow(4 - 8*c2,0.5)

    if discrim:
        err = c2Err / discrim
    else:
        err = 0 
    return err


def effFromC2(c2):

    denom = 4.0
    if (4-8*c2) < 0:
        print "ERROR c2:",c2
        c2 = 0.5
        #return 0

    discrim = pow(4 - 8*c2,0.5)
    num   = 2 + discrim
    
    e = num/denom
    return e


def effFromC1Hist(c1Hist):

    eff = ROOT.TH1F(c1Hist)
    eff.SetName("eff_c1")
    
    nBins = c1Hist.GetNbinsX()
    for i in range(nBins):
        c1    = c1Hist.GetBinContent(i+1)
        c1Err = c1Hist.GetBinError  (i+1)
        
        eff_c1 = pow(c1,0.5)
        eff_c1_err = getErrEffC1(c1,c1Err)
        
        if eff_c1_err:
            eff.SetBinContent(i+1, eff_c1)
            eff.SetBinError  (i+1, eff_c1_err)
        else:
            eff.SetBinContent(i+1, 0)
            eff.SetBinError  (i+1, 0)
    
    return eff


def effFromC2Hist(c2Hist):

    eff = ROOT.TH1F(c2Hist)
    eff.SetName("eff_c2")
    
    nBins = c2Hist.GetNbinsX()
    for i in range(nBins):
        c2    = c2Hist.GetBinContent(i+1)
        c2Err = c2Hist.GetBinError  (i+1)
        
        eff_c2     = effFromC2(c2)
        eff_c2_err = getErrEffC2(c2,c2Err)


        if eff_c2_err:
            eff.SetBinContent(i+1, eff_c2)
            eff.SetBinError  (i+1, eff_c2_err)
        else:
            eff.SetBinContent(i+1, 0)
            eff.SetBinError  (i+1, 0)

    
    return eff





def doInclusive(regName,hMod,lMod):
    print
    print
    print "=========================="
    print   regName
    print "=========================="

    Npp = getNum(inFileHad,"0FailTTVetoFourTag_"+hMod+"/nbjets")
    Npf = getNum(inFileHad,"1FailTTVetoFourTag_"+hMod+"/nbjets")
    Nff = getNum(inFileHad,"2FailTTVetoFourTag_"+hMod+"/nbjets")
    NhadTot = Npp+Npf+Nff

    print "\tNpp:",Npp
    print "\tNpf:",Npf
    print "\tNff:",Nff
    
    c1 = Npp/NhadTot
    print c1
    c1Err = pow(c1*(1-c1)/NhadTot,0.5)
    eff_c1 = pow(c1,0.5)
    eff_c1_err = getErrEffC1(c1, c1Err)
    print "\tc1:",c1,"+/-",c1Err
    print "\t\teff:",eff_c1,"+/-",eff_c1_err
    

    c2 = Npf/NhadTot
    c2Err = pow(c2*(1-c2)/NhadTot,0.5)
    eff_c2 = effFromC2(c2)
    eff_c2_err = getErrEffC2(c2,c2Err)
    print "\tc2:",c2
    print "\t\teff:",eff_c2,"+/-",eff_c2_err
    
    Np = getNum(inFileLep,"PtLepTop_mub100PassTTVeto"+lMod+"/nbjets")
    Nf = getNum(inFileLep,"PtLepTop_mub100FailTTVeto"+lMod+"/nbjets")
    NlepTot = Np+Nf
    print "\tNp:",Np
    print "\tNf:",Nf

    c3 = Np/(NlepTot)
    c3Err = pow(c3*(1-c3)/NlepTot,0.5)    
    print "\tc3:",c3
    print "\t\teff:",c3,"+/-",c3Err

    return {"Npp":Npp, "Npf":Npf, "Nff":Nff, 
            "Np":Np,  "Nf":Nf,
            "c1":c1, "c1Err":c1Err, 
            "c2":c2, "c2Err":c2Err, 
            "c3":c3, "c3Err":c3Err, 
            "eff_c1":eff_c1, "eff_c1_err":eff_c1_err,
            "eff_c2":eff_c2, "eff_c2_err":eff_c2_err,
            }


def doVar(name,hCandName,varName,hMod,lMod):
    print
    print
    print "=========================="
    print   varName
    print "=========================="
    outFile.cd()
    thisDir = outFile.mkdir(name+"_"+varName)
    thisDir.cd()

    Npp = getHist(inFileHad,"0FailTTVetoFourTag_"+hMod+"/"+hCandName+varName)
    Npp.SetName("Npp")
    
    Npf = getHist(inFileHad,"1FailTTVetoFourTag_"+hMod+"/"+hCandName+varName)
    Npf.SetName("Npf")
    
    Nff = getHist(inFileHad,"2FailTTVetoFourTag_"+hMod+"/"+hCandName+varName)
    Nff.SetName("Nff")
    
    NhadTot = ROOT.TH1F(Npp)
    NhadTot.Add(Npf)
    NhadTot.Add(Nff)
    NhadTot.SetName("NhadTot")

    Npp.Write()
    Npf.Write()
    Nff.Write()
    NhadTot.Write()
    

    
    # 
    # Need to set error bars by hand
    # 
    #c1 = ROOT.TH1F(Npp)
    #c1.Divide(NhadTot)
    #c1.SetName("c1")

    c1 = divideCorrelated(Npp, NhadTot)
    c1.SetName("c1")
    
    c1.Write()

    eff_c1 = effFromC1Hist(c1)
    eff_c1.Write()

    #print "\t\teff:",pow(c1,0.5)
    
    c2 = ROOT.TH1F(Npf)
    c2.Divide(NhadTot)
    c2.SetName("c2")
    c2.Write()


    eff_c2 = effFromC2Hist(c2)
    eff_c2.Write()
    
    Np = getHist(inFileLep,"PtLepTop_mub100PassTTVeto"+lMod+"/hCand_"+varName)
    Np.SetName("Np")

    Nf = getHist(inFileLep,"PtLepTop_mub100FailTTVeto"+lMod+"/hCand_"+varName)
    Nf.SetName("Nf")

    NlepTot = ROOT.TH1F(Np)
    NlepTot.Add(Nf)
    NlepTot.SetName("NlepTot")
    
    Np.Write()
    Nf.Write()
    NlepTot.Write()

    #c3 = ROOT.TH1F(Np)
    #c3.Divide(NlepTot)
    c3 = divideCorrelated(Np, NlepTot)
    c3.SetName("c3")
    c3.Write()    

    eff_c3 = ROOT.TH1F(c3)
    eff_c3.SetName("eff_c3")
    eff_c3.Write()

    return


vars = ["Pt","Eta","mW","mTop","Xtt","dRjj","Mass","leadJet_Pt_m","sublJet_Pt_m"]
#vars = ["Eta"]
for v in vars:

    #
    # Before Mh
    #
    doVar("BeforeMh","sublHCand_",v,"Inclusive","")


    #
    # After Mh
    #
    doVar("AfterMh","sublHCand_",v,"Signal","_PassMh")



#
BeforeNums = doInclusive("BeforeMh","Inclusive","")
AfterNums  = doInclusive("AfterMh" ,"Signal","_PassMh")
makeTables(BeforeNums, AfterNums) 
