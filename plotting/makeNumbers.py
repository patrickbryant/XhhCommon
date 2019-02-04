
import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",        default="", help="")
parser.add_option('--dataFileSLCR',             type = 'string', default = "", dest = 'inputDataFileSLCR', help = 'input Data File' )
parser.add_option('-m', '--mu_qcd',             dest="mu_qcd",               default=0, help="")
parser.add_option('--mu_qcd_err',               dest="mu_qcd_err",           default=0, help="")
parser.add_option('-o', '--out',                dest="output",               default="", help="")
o, a = parser.parse_args()

if not o.mu_qcd:
    print "ERROR give mu_qcd!!"
    import sys
    sys.exit(-1)


from makeSampleCompTableTTbar import getValues
from ttbarCR_DataVsMC         import doInclusive

import ROOT

dataFile  = ROOT.TFile(o.dataFileName,"READ")
ttbarFile = ROOT.TFile(o.ttbarFileName,"READ")
dataFileSLC = ROOT.TFile(o.inputDataFileSLCR,"READ")


nJet2Tag = dataFile.Get("PassTrigTwoTag_Inclusive/nJetOther")
n2TagEvents = nJet2Tag.Integral()

nJet2Tag_ttbar = ttbarFile.Get("PassTrigTwoTag_Inclusive/nJetOther")
n2TagEvents_ttbar = nJet2Tag_ttbar.Integral()


N_2Tag_file = open(o.output+"N_2tag.tex","w")
N_2Tag_file.write(str(int(n2TagEvents)))
N_2Tag_file.close()


#
#  2 Tag TTbar Fraction
#
ttbarFrac = round(float(n2TagEvents_ttbar)/n2TagEvents*100,1)
N_2Tag_ttbarFrac_file = open(o.output+"N_2tag_ttbarFrac.tex","w")
N_2Tag_ttbarFrac_file.write(str(ttbarFrac)+"\%")
N_2Tag_ttbarFrac_file.close()

#
#  2 Tag TTbar Fraction (Sideband)
#
nJet2Tag_sideband = dataFile.Get("PassTrigTwoTag_Sideband/nJetOther")
n2TagEvents_sideband = nJet2Tag_sideband.Integral()

nJet2Tag_ttbar_sideband = ttbarFile.Get("PassTrigTwoTag_Sideband/nJetOther")
n2TagEvents_ttbar_sideband = nJet2Tag_ttbar_sideband.Integral()
ttbarFrac_sideband = round(float(n2TagEvents_ttbar_sideband)/n2TagEvents_sideband*100,1)
N_2Tag_ttbarFrac_sideband_file = open(o.output+"N_2tag_ttbarFrac_sideband.tex","w")
N_2Tag_ttbarFrac_sideband_file.write(str(ttbarFrac_sideband)+"\%")
N_2Tag_ttbarFrac_sideband_file.close()

#
#  4 Tag TTbar Fraction (Sideband)
#
nJet4Tag_sideband = dataFile.Get("PassTrigFourTag_Sideband/nJetOther")
n4TagEvents_sideband = nJet4Tag_sideband.Integral()

nJet4Tag_ttbar_sideband     = ttbarFile.Get("PassTrigFourTag_Sideband/nJetOther")
n4TagEvents_ttbar_sideband = nJet4Tag_ttbar_sideband.Integral()
ttbar4TagFrac_sideband     = round(float(n4TagEvents_ttbar_sideband)/n4TagEvents_sideband*100,1)
N_4Tag_ttbarFrac_sideband_file = open(o.output+"N_4tag_ttbarFrac_sideband.tex","w")
N_4Tag_ttbarFrac_sideband_file.write(str(ttbar4TagFrac_sideband)+"\%")
N_4Tag_ttbarFrac_sideband_file.close()


#
#  2 Tag TTbar Fraction in ReverseTTVeto Control)
#
nJet2Tag_TTCR    = dataFile.Get("ReverseTTVetoTwoTag_Control/nJetOther")
n2TagEvents_TTCR = nJet2Tag_TTCR.Integral()

nJet2Tag_ttbar_TTCR        = ttbarFile.Get("ReverseTTVetoTwoTag_Control/nJetOther")
n2TagEvents_ttbar_TTCR     = nJet2Tag_ttbar_TTCR.Integral()

ttbarFrac_TTCR             = round(float(n2TagEvents_ttbar_TTCR)/n2TagEvents_TTCR*100,1)
N_2Tag_ttbarFrac_TTCR_file = open(o.output+"N_2tag_ttbarFrac_TTCR.tex","w")
N_2Tag_ttbarFrac_TTCR_file.write(str(ttbarFrac_TTCR)+"\%")
N_2Tag_ttbarFrac_TTCR_file.close()



nJet4Tag_ttbar   = ttbarFile.Get("TTVetoFourTag_Signal/nJetOther")
n_ttbar_bkg_error = ROOT.Double ()
n_ttbar_bkg = nJet4Tag_ttbar.IntegralAndError(0,nJet4Tag_ttbar.GetNbinsX(),n_ttbar_bkg_error)
#print n_ttbar_bkg, n_ttbar_bkg_error

#print n_ttbar_bkg, nJet4Tag_ttbar.GetEntries()

N_MC_ttbar_bkg_file = open(o.output+"N_MC_ttbar_bkg.tex","w")
N_MC_ttbar_bkg_file.write("$"+str(round(n_ttbar_bkg,2))+" \pm "+str(round(n_ttbar_bkg_error,2))+"$\n")
N_MC_ttbar_bkg_file.close()

mu_qcd_file = open(o.output+"mu_qcd.tex","w")
mu_qcd     = float(o.mu_qcd)
mu_qcd_err = float(o.mu_qcd_err)

mu_qcd_file.write("$ \\mu_{\\rm{QCD}} = "+str.format('{0:.5f}', mu_qcd)+" \pm "+str.format('{0:.5f}', mu_qcd_err)+"$ (stat.)\n")
mu_qcd_file.close()


nJetDataFourTag_inclusive = dataFile.Get("TTVetoFourTag_Inclusive/nJetOther")
print nJetDataFourTag_inclusive.Integral()

nJetDataTwoTag_inclusive = dataFile.Get("TTVetoTwoTag_Inclusive/nJetOther")
nJetTTbarTwoTag_inclusive = ttbarFile.Get("TTVetoTwoTag_Inclusive/nJetOther")
print nJetDataTwoTag_inclusive.Integral()
print nJetTTbarTwoTag_inclusive.Integral()

def getQCDBkg(cut, region):
    hist_data2tag   = dataFile.Get(cut+"TwoTag_"+region+"/nJetOther")
    n2TagData       = hist_data2tag.Integral()

    hist_ttbar2tag = ttbarFile.Get(cut+"TwoTag_"+region+"/nJetOther")
    n2TagTTbar     = hist_ttbar2tag.Integral()

    nQCD           = (n2TagData - n2TagTTbar) * float(o.mu_qcd)
    return nQCD

def getTTbarBkg(cut, region):

    hist_ttbar4tag = ttbarFile.Get(cut+"FourTag_"+region+"/nJetOther")
    n4TagTTbar     = hist_ttbar4tag.Integral()
    return n4TagTTbar

def getTotalBkg(cut,region):

    nQCD       = getQCDBkg  (cut, region)
    n4TagTTbar = getTTbarBkg(cut, region)

    nTotal = nQCD + n4TagTTbar
    return nTotal
    
def printBreakDown(cut, region):
    nQCD   = getQCDBkg  (cut,region)
    nTTBar = getTTbarBkg(cut,region)
    nTotal = getTotalBkg(cut,region)    
    print "\tQCD",  nQCD  ,"(",nQCD/nTotal,")"
    print "\tttbar",nTTBar,"(",nTTBar/nTotal,")"
    print "Total",  nTotal


#printBreakDown("PassM4jDep","Signal")
#print 
#printBreakDown("TTVeto","Signal")

