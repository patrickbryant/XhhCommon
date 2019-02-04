# Calculate e from different inputs
import ROOT
import array


binDict = {}
binDict["Pt"] = [125,150,175,200,225,250,300,400,700]
binDict["Eta"] = [-2.5,-1.5,-1.0,-0.5,0,0.5,1.0,1.5,2.5]
binDict["leadJet_Pt_m"] = [0,100,125,150,175,200,300,400]
binDict["sublJet_Pt_m"] = [0,40,60,80,100,150,400]


def parseOptions():
    from optparse import OptionParser
    from collections import OrderedDict
    p = OptionParser()
    p.add_option('--data',  type = 'string', default = "", dest = 'inputDataFile', help = 'input Data File' )
    p.add_option('--mc',    type = 'string', default = "", dest = 'inputMCFile',   help = 'input MC   File' )
    p.add_option('--out',   type = 'string', default = "", dest = 'outFileName',   help = 'output File' )
    (o,a) = p.parse_args()
    return (o,a)


def getNum(infile,histName):
    hist = infile.Get(histName)
    return hist.GetEntries()

def getHist(infile,histName):
    hist = infile.Get(histName)

    for v in binDict.keys():
        if histName.find(v) != -1:
            bins = binDict[v] 

            xBins = array.array("d", bins)
            histNew = hist.Rebin(len(bins) - 1,  hist.GetName()+"_rebinned", xBins)
        
            return histNew

    hist.Rebin(4)
    return hist

def printLine(oFile,line):
    print line
    oFile.write(line+"\n")


def pNum(num):
    return str(int(num))

def pFloat(num,rNum):
    return str(round(float(num),rNum))


def makeTables(bNum, aNum):

    outTxtFileC3   = open(o.outFileName.replace(".root","_DataMC_c3.tex"),"w")
    printLine(outTxtFileC3, "\\begin{tabular}{ c | c | c  }")
    printLine(outTxtFileC3, "Observable  & Before $m_h$ & After $m_h$ (100-140 GeV)  \\\\")
    printLine(outTxtFileC3, "\hline")
    printLine(outTxtFileC3, "$N_{P}$ & "+pNum(bNum["Np"])+" & "+pNum(aNum["Np"])+" \\\\")
    printLine(outTxtFileC3, "$N_{F}$ & "+pNum(bNum["Nf"])+" & "+pNum(aNum["Nf"])+" \\\\")
    printLine(outTxtFileC3, "$\epsilon$ from Data & "+pFloat(bNum["eff_c3_Data" ],3)+" $\pm$ "+pFloat(bNum["eff_c3_Data_Err" ],4)+" & "+pFloat(aNum["eff_c3_Data"],3)+" $\pm$ "+pFloat(aNum["eff_c3_Data_Err"],3)+" \\\\")
    printLine(outTxtFileC3, "\hline")
    printLine(outTxtFileC3, "$\epsilon$ from MC & "+pFloat(bNum["eff_c3_MC" ],3)+" $\pm$ "+pFloat(bNum["eff_c3_MC_Err" ],4)+" & "+pFloat(aNum["eff_c3_MC"],3)+" $\pm$ "+pFloat(aNum["eff_c3_MC_Err"],3)+" \\\\")
    printLine(outTxtFileC3, "\end{tabular}")


def doInclusive(regName,hMod,lMod, dataFile, mcFile):
    print
    print
    print "=========================="
    print   regName
    print "=========================="


    Np_MC = getNum(mcFile,"PtLepTop_mub100PassTTVeto"+lMod+"/nbjets")
    Nf_MC = getNum(mcFile,"PtLepTop_mub100FailTTVeto"+lMod+"/nbjets")
    
    NlepTot_MC = Np_MC+Nf_MC
    print "\tNp_MC:",Np_MC
    print "\tNf_MC:",Nf_MC

    c3_MC = Np_MC/(NlepTot_MC)
    eff_c3_MC_Err = pow( (c3_MC * (1-c3_MC)) /NlepTot_MC   ,0.5)
    
    print "\tc3_MC:",c3_MC
    print "\t\teff_MC:",c3_MC,"+/-",eff_c3_MC_Err


    Np_Data = getNum(dataFile,"PtLepTop_mub100PassTTVeto"+lMod+"/nbjets")
    Nf_Data = getNum(dataFile,"PtLepTop_mub100FailTTVeto"+lMod+"/nbjets")

    NlepTot_Data = Np_Data+Nf_Data
    print "\tNp_Data:",Np_Data
    print "\tNf_Data:",Nf_Data

    c3_Data = Np_Data/(NlepTot_Data)
    eff_c3_Data_Err = pow( (c3_Data * (1-c3_Data)) /NlepTot_Data   ,0.5)


    print "\tc3_Data:",c3_Data
    print "\t\teff_Data:",c3_Data,"+/-",eff_c3_Data_Err

    return {"Np":Np_Data, "Nf":Nf_Data,
            "eff_c3_Data":c3_Data, "eff_c3_Data_Err":eff_c3_Data_Err,
            "eff_c3_MC":c3_MC, "eff_c3_MC_Err":eff_c3_MC_Err,
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
    
    
    Np_MC = getHist(inFileMC,"PtLepTop_mub100PassTTVeto"+lMod+"/hCand_"+varName)
    Np_MC.SetName("Np_MC")

    Nf_MC = getHist(inFileMC,"PtLepTop_mub100FailTTVeto"+lMod+"/hCand_"+varName)
    Nf_MC.SetName("Nf")

    NlepTot_MC = ROOT.TH1F(Np_MC)
    NlepTot_MC.Add(Nf_MC)
    NlepTot_MC.SetName("NlepTot_MC")
    
    Np_MC.Write()
    Nf_MC.Write()
    NlepTot_MC.Write()

    c3_MC = ROOT.TH1F(Np_MC)
    c3_MC.Sumw2()
    c3_MC.Divide(NlepTot_MC)
    c3_MC.SetName("c3_MC")
    c3_MC.Write()    

    eff_c3_MC = ROOT.TH1F(c3_MC)
    eff_c3_MC.SetName("eff_c3_MC")
    eff_c3_MC.Write()


    #
    #  Data
    #

    Np_Data = getHist(inFileData,"PtLepTop_mub100PassTTVeto"+lMod+"/hCand_"+varName)
    Np_Data.SetName("Np")

    Nf_Data = getHist(inFileData,"PtLepTop_mub100FailTTVeto"+lMod+"/hCand_"+varName)
    Nf_Data.SetName("Nf")

    NlepTot_Data = ROOT.TH1F(Np_Data)
    NlepTot_Data.Add(Nf_Data)
    NlepTot_Data.SetName("NlepTot_Data")
    
    Np_Data.Write()
    Nf_Data.Write()
    NlepTot_Data.Write()

    c3_Data = ROOT.TH1F(Np_Data)
    c3_Data.Sumw2()
    c3_Data.Divide(NlepTot_Data)
    c3_Data.SetName("c3_Data")
    c3_Data.Write()    

    eff_c3_Data = ROOT.TH1F(c3_Data)
    eff_c3_Data.SetName("eff_c3_Data")
    eff_c3_Data.Write()


    return


def main(inFileData, inFileMC, outFile):

    vars = ["Pt","Eta","mW","mTop","Xtt","dRjj","Mass","leadJet_Pt_m","sublJet_Pt_m"]
    for v in vars:
        doVar("BeforeMh","hCand_",v,"Inclusive","")
        doVar("AfterMh", "hCand_",v,"Signal"   ,"_PassMh")

    BeforeNums = doInclusive("BeforeMh","Inclusive", ""      , inFileData, inFileMC)
    AfterNums  = doInclusive("AfterMh" ,"Signal",   "_PassMh", inFileData, inFileMC)

    makeTables(BeforeNums, AfterNums) 

if __name__ == "__main__":

    o,a = parseOptions()

    inFileData = ROOT.TFile(o.inputDataFile,"READ")
    inFileMC   = ROOT.TFile(o.inputMCFile,  "READ")
    outFile   = ROOT.TFile(o.outFileName,"RECREATE")
    
    main(inFileData, inFileMC, outFile)
