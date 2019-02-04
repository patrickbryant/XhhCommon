import os
import optparse
parser = optparse.OptionParser()
parser.add_option('-a','--all',       action="store_true",          dest="doAll",          default=False, help="")
parser.add_option('-t','--trig',      action="store_true",          dest="doTrig",         default=False, help="")
parser.add_option('--doMain',         action="store_true",          dest="doMain",         default=False, help="")
parser.add_option('--ttbar',          action="store_true",          dest="doTTBar",        default=False, help="")
parser.add_option('--ddttbar',        action="store_true",          dest="doDDTTBar",      default=False, help="")
parser.add_option('--doSR',           action="store_true",          dest="doSR",           default=False, help="")
parser.add_option('--doCutFlow',      action="store_true",          dest="doCutFlow",      default=False, help="")
parser.add_option('--doSigAcc',       action="store_true",          dest="doSigAcc",       default=False, help="")
parser.add_option('--doSyst',         action="store_true",          dest="doSyst",         default=False, help="")
parser.add_option('--doJER',          action="store_true",          dest="doJER",          default=False, help="")
parser.add_option('--doQCD',          action="store_true",          dest="doQCD",          default=False, help="")
#parser.add_option('--doQCDVars',      action="store_true",          dest="doQCDVars",      default=False, help="")
parser.add_option('--test',           action="store_true",          dest="test",           default=False, help="")
parser.add_option('--iteration',                                    dest="iteration",      default="0", help="")
parser.add_option('--dirName',       dest  ="dirName",            default="Test", help="")
o, a = parser.parse_args()


# Environment Variables
#nTupleVersion  = "TestNewTrig2b00-06-00"
nTupleVersion  = o.dirName+"00-07-00"
#t3data         = "/share/t3data3/johnda/samples/XhhOutput/"+nTupleVersion+"/"
t3data         = "./hists-"+nTupleVersion+"/"
lumi           = "3.23"
#outDir         = "vTestNewTrig2b00_06_00/"
outDir         = "v"+nTupleVersion.replace("-","_")+"/"
#

from helpers import read_mu_qcd_file



#paths that need --base-dir
#m500FileNoBase      = "histsSignal/RSG_c10_M500/hist-tree.root"
#m1000FileNoBase     = "histsSignal/_301495/hist-tree.root"
#m1200FileNoBase     = "histsSignal/_301497/hist-tree.root"
ttbarFileNoBase     = "histsTTbar-0//hist-tree.root" # dont want to reweight the ttbar BKG
dataDirSLCRNoBase   = "histsData-SLCR/hist-tree.root"
ttbarFileSLCRNoBase = "histsTTbar-SLCR/hist-tree.root"

#Full Paths
signalDir      = t3data+"/histsSignal"


dataFile        = t3data+"/histsData-"+str(o.iteration)+"/hist-tree.root"
qcdFile         = t3data+"/histsQCD-"+str(o.iteration)+"/hist-tree.root"
zJetsFile       = t3data+"/histsZJets-0/hist-tree.root"
ttbarFile       = t3data+"/histsTTbar-0/hist-tree.root"
signalShapeFile = t3data+"/makeSignalSysHists.root"

dataFileSLCR   = t3data+"/histsData-SLCR/hist-tree.root"
ttbarFileSLCR  = t3data+"/histsTTbar-SLCR/hist-tree.root"

m500File       = t3data+"/histsSignal/RSG_c10_M500/hist-tree.root"
m800File       = t3data+"/histsSignal/RSG_c10_M800/hist-tree.root"
m1000File      = t3data+"/histsSignal/RSG_c10_M1000/hist-tree.root"
m1200File      = t3data+"/histsSignal/RSG_c10_M1200/hist-tree.root"

m500JERVarFile = t3data+"/histsSignal/XhhMiniNtupleResolved_JET_JER_SINGLE_NP__1up/RSG_c10_M500/hist-tree.root"
m1000JERVarFile = t3data+"/histsSignal/XhhMiniNtupleResolved_JET_JER_SINGLE_NP__1up/RSG_c10_M1000/hist-tree.root"
m1200JERVarFile = t3data+"/histsSignal/XhhMiniNtupleResolved_JET_JER_SINGLE_NP__1up/RSG_c10_M1200/hist-tree.root"

limitInputs    = t3data+"/LimitSettingInputs/resolved_4bSR.root"


muQCDReults    = read_mu_qcd_file(t3data+"/mu_qcd-"+str(o.iteration)+".txt")
mu_qcd         = str(muQCDReults["mu_qcd"])
mu_qcd_err     = str(muQCDReults["mu_qcd_err"])
mu_ttbar       = str(muQCDReults["mu_ttbar"])



if not os.path.isdir(outDir):
    os.mkdir(outDir)

def run(cmd):
    print cmd
    if not o.test:
        os.system(cmd)


if o.doAll or o.doTrig:
    run("python XhhCommon/plotting/plotTrigger.py "+m500File+ "  --out "+outDir+"TrigEffm500")
    run("python XhhCommon/plotting/plotTrigger.py "+m1000File+"  --out "+outDir+"TrigEffm1000")
    run("python XhhCommon/plotting/plotTrigger.py "+ttbarFile+"  --out "+outDir+"TrigEffTTBar")
    run("python XhhCommon/plotting/plotTriggerEmulation.py -s "+signalDir+"  --out "+outDir+"/TrigEmulation")
    
if o.doAll or o.doTTBar:
    run("python XhhCommon/plotting/plotTTBar2TagVs4Tag.py "+ttbarFileNoBase+" --base-dir "+t3data+" --out "+outDir+"TTBar2TagVs4Tag")
    run("python XhhCommon/plotting/plotTTBarVars.py    -t "+ttbarFile+" --m500 "+m500File+" --m1000 "+m1000File+" --out "+outDir+"TTBarPlots")


if o.doAll or o.doDDTTBar:
    run("python XhhCommon/plotting/compTTBarMC.py "+ttbarFile+" "+ttbarFileSLCR+"  --model BasicComp --out "+outDir+"TTBarMC_SLCRvsSR")
    
    run("python XhhCommon/plotting/ttbarCR_MCClosure.py --had "+ttbarFile+" --lep "+ttbarFileSLCR+" --out "+outDir+"ttbarCR_MCClosure.root")
    run("python XhhCommon/plotting/plotMCClosure.py "+outDir+"ttbarCR_MCClosure.root --out "+outDir+"ttbarCR_MCClosure")
    run("python XhhCommon/plotting/plotReversedTTBar.py -d "+dataFile+" --out "+outDir+"reversedTTBarVeto")
    run("python XhhCommon/plotting/plotReversedTTBar.py -d "+ttbarFile+" --max 5 --out "+outDir+"reversedTTBarVetoTTBarMC")
    run("python XhhCommon/plotting/compTTCR_DataMC.py   "+dataDirSLCRNoBase+" "+ttbarFileSLCRNoBase+" --base-dir "+t3data+" --model BasicComp --out "+outDir+"/TTBarCR_DataMC")

    run("python XhhCommon/plotting/ttbarCR_DataVsMC.py  --data "+dataFileSLCR+" --mc "+ttbarFileSLCR+"  --out "+outDir+"/ttbarCR_DataVsMC.root")
    run("python XhhCommon/plotting/plotDataVsMCTTBarCR.py "+outDir+"/ttbarCR_DataVsMC.root --out "+outDir+"/ttbarCR_DataVsMC")

    run("python XhhCommon/plotting/makeFinalTTBarNum.py  --mu_qcd "+mu_qcd+" -d "+dataFile+" -t "+ttbarFile+" --dataFileSLCR "+dataFileSLCR+"  --out "+outDir)
    run("python XhhCommon/plotting/makeFinalTTBarNumZZ.py  --mu_qcd "+mu_qcd+" -d "+dataFile+" -t "+ttbarFile+" --dataFileSLCR "+dataFileSLCR+"  --out "+outDir)

if o.doAll or o.doMain:
    #run("python XhhCommon/plotting/plotResolved.py --plotter interactive -c XhhCommon/plotting/plotIConfig.py --out "+outDir+"resolvedPlots_NoReweight --inputDir "+dataDirNoRW)
    run("python XhhCommon/plotting/plotResolved.py \
                --plotter main \
                -c XhhCommon/plotting/resolvedConfig.py \
                --out "+outDir+"/resolvedPlots \
                --data "+dataFile+" \
                --qcd "+qcdFile+" \
                --ttbar "+ttbarFile+" \
                --signal "+m800File+" \
                --mu_qcd "+mu_qcd+" \
                --mu_ttbar "+mu_ttbar+" \
                --iteration "+str(o.iteration)+" \
                --lumi "+lumi)


if o.doAll or o.doSyst:


    run("python XhhResolved/scripts/makeShapeSysFits.py  -d "+dataFile+" --mu_qcd "+mu_qcd+" -t "+ttbarFile+" --mu_ttbar "+mu_ttbar+" -o "+outDir+"/LimitSettingInputs ")

    run("python XhhCommon/plotting/plotTTBarShapeSys.py "+outDir+"/LimitSettingInputs/shapeSys.root  --out "+outDir+"/LimitSettingInputs" )

    run("python XhhResolved/scripts/makeLimitInputs.py -d "+dataFile+"  --bkgSR "+outDir+"/CutFlows/sampleCompSR.tex -q "+qcdFile+" -t "+ttbarFile+" --shapeFile "+outDir+"/LimitSettingInputs/shapeSys.root --signalFile "+signalShapeFile+"  -o "+outDir+"//LimitSettingInputs")
    run("python XhhResolved/scripts/makeLimitInputsNonResonant.py -d "+dataFile+"  --bkgSR "+outDir+"/CutFlows/sampleCompSR.tex -q "+qcdFile+" -t "+ttbarFile+"  --signalFile "+signalShapeFile+"  -o "+outDir+"//LimitSettingInputs")

    run("python XhhResolved/scripts/makeSystematicsTables.py --in "+outDir+"/LimitSettingInputs/resolvedLimitInputs.root --out "+outDir+"/")

    run("python XhhResolved/scripts/makeSystematicsTablesNonResonant.py --in "+outDir+"//LimitSettingInputs/resolvedLimitInputsNonResonant.root   --out "+outDir+"/")

    run("python XhhCommon/plotting/makePaperPlots.py -d "+dataFile+"  --limits "+outDir+"/LimitSettingInputs/resolvedLimitInputs.root --bkgCR "+outDir+"/CutFlows/sampleComp.tex -q "+qcdFile+" -t "+ttbarFile+" --shapeFile "+outDir+"/LimitSettingInputs/shapeSys.root    -o "+outDir+"//PaperPlots")



if o.doAll or o.doJER:
    run("python XhhCommon/plotting/plotJERVars.py "+m500JERVarFile +" "+m500File+ " --model BasicComp --out "+outDir+"/JERVariationsm500")
    run("python XhhCommon/plotting/plotJERVars.py "+m1000JERVarFile+" "+m1000File+" --model BasicComp --out "+outDir+"/JERVariationsm1000")
    run("python XhhCommon/plotting/plotJERVars.py "+m1200JERVarFile+" "+m1200File+" --model BasicComp --out "+outDir+"/JERVariationsm1200")
    run("python XhhCommon/plotting/plotJESVars.py -i "+t3data+" -o "+outDir+"/JESVariations")

#python XhhResolved/scripts/makeLimitInputs.py -i $t3data/histsQCD-2/hist-tree.root -s $mu_qcd_up   -o $t3data/LimitSettingInputs/resolved_4bSR.root \
#-n qcd_hh_QCDUp
#python XhhResolved/scripts/makeLimitInputs.py -i $t3data/histsQCD-2/hist-tree.root -s $mu_qcd_down -o $t3data/LimitSettingInputs/resolved_4bSR.root \
#-n qcd_hh_QCDDown    

    #run("python XhhCommon/plotting/plotResolved.py \
    #            --plotter systematics \
    #            -c XhhCommon/plotting/resolvedConfig.py \
    #            --out         "+outDir+"/systematics \
    #            --systematics "+outDir+"/LimitSettingInputs/shapeSys_4bSR.root \
    #            --lumi "+lumi)    


if o.doAll or o.doSR:    
    run("python XhhCommon/plotting/plotSRVars.py --sample RSG  --sig "+signalDir+" --out "+outDir+"SRPlots")
    run("python XhhCommon/plotting/plotSRVars.py --sample Hhh  --sig "+signalDir+" --out "+outDir+"SRPlots")
    run("python XhhCommon/plotting/plotSRVars.py --sample  hh  --sig "+signalDir+" --out "+outDir+"SRPlots")

    run("python XhhCommon/plotting/plotMDCVars.py    -d "+dataFile+"  --m500 "+m500File+" --m1000 "+m1000File+" --m1200 "+m1200File+" --out "+outDir+"MDCPlots")    
    run("python XhhCommon/plotting/plotXhhVars.py    -t "+ttbarFile+" --m500 "+m500File+" --m1000 "+m1000File+" --m1200 "+m1200File+" --out "+outDir+"XhhPlots")
    run("python XhhCommon/plotting/plotSidebandCR.py -d "+dataFile+" --out "+outDir+"SidebandCRPlots")
    run("python XhhCommon/plotting/plotImprovedM4j.py "+m500File+" --out "+outDir+"/ImprovedM4j500Plots")
    run("python XhhCommon/plotting/plotImprovedM4j.py "+m1000File+" --out "+outDir+"/ImprovedM4j1000Plots")
    run("python XhhCommon/plotting/plotImprovedM4j.py "+dataFile+" --out "+outDir+"/ImprovedM4jDataPlots")

    run("python XhhCommon/plotting/plotLeadSublMass.py "+m500File+" --out "+outDir+"/LeadSublMass_m500")
    run("python XhhCommon/plotting/plotLeadSublMass.py "+m1000File+" --out "+outDir+"/LeadSublMass_m1000")
    run("python XhhCommon/plotting/plotLeadSublMass.py "+m1200File+" --out "+outDir+"/LeadSublMass_m1200")

if o.doAll or o.doCutFlow:
    run("python XhhCommon/plotting/makeCutFlows.py -d "+dataFile+" -t "+ttbarFile+" --m500 "+m500File+" --m1000 "+m1000File+" --m1200 "+m1200File+" --out "+outDir+"/CutFlows")
    run("python XhhCommon/plotting/makeSampleCompTable.py      -m "+mu_qcd+" -d "+dataFile+"  -t "+ttbarFile+"  --out "+outDir+"/CutFlows")
    run("python XhhCommon/plotting/makeSampleCompTable.py      -m "+mu_qcd+" -d "+dataFile+"  -t "+ttbarFile+"  -z "+zJetsFile+" --out "+outDir+"/CutFlows")
    run("python XhhCommon/plotting/makeSampleCompTableTTBar.py -m "+mu_qcd+" -d "+dataFile+"  -t "+ttbarFile+"  --out "+outDir+"/CutFlows")
    run("python XhhCommon/plotting/makeSampleCompTableQCDVar.py      -m "+mu_qcd+" -d "+dataFile+"  -t "+ttbarFile+" --ttbarSignal "+outDir+"/N_tt_SR.tex  --out "+outDir+"/CutFlows")
    run("python XhhCommon/plotting/makeSampleCompTableQCDVar.py  --zz      -m "+mu_qcd+" -d "+dataFile+"  -t "+ttbarFile+" --ttbarSignal "+outDir+"/N_tt_ZZ.tex  --out "+outDir+"/CutFlows")

    run("python XhhCommon/plotting/makeSampleCompTableSR.py    -m "+mu_qcd+" -d "+dataFile+"  -t "+outDir+"/N_tt_SR.tex  --out "+outDir+"/CutFlows")
    run("python XhhCommon/plotting/makeNumbers.py  --mu_qcd "+mu_qcd+"  --mu_qcd_err "+mu_qcd_err+" -d "+dataFile+" -t "+ttbarFile+" --dataFileSLCR "+dataFileSLCR+"  --out "+outDir)    

if o.doAll or o.doSigAcc:
    run("python XhhCommon/plotting/makeAccPlots.py --sig "+signalDir+" -c 1.0 --out "+outDir+"/SRAcc")
    run("python XhhCommon/plotting/makeAccPlots.py --sig "+signalDir+" -c 2.0  --out "+outDir+"/SRAcc")
    run("python XhhCommon/plotting/makeAccPlots.py --sig "+signalDir+" -c 2HDM  --out "+outDir+"/SRAcc")
    run("python XhhCommon/plotting/makeAccTable.py --sig "+signalDir+" --out "+outDir+"/SRAcc")


if o.doAll or o.doQCD:
    run("python  XhhCommon/plotting/makeWeightPlots.py --in "+t3data+"/weights2bto4b1.root --out "+outDir+"/QCDWeights")


#if o.doQCDVars:
#    outDir = outDir+"QCDVariations"
#    run("python XhhCommon/plotting/plotQCDShapeDiffs.py hists-v6_TightTwoTag00-06-00/histsQCD-1/hist-tree.root  hists-v6_Nominal00-06-00/histsQCD-2/hist-tree.root --model BasicComp --labName "Tight 2-Tag"  --out Test")
    
