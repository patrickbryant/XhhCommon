
import optparse
parser = optparse.OptionParser()
parser.add_option('-d', '--dataFile',           dest="dataFileName",         default="", help="")
parser.add_option('-t', '--ttbarFile',          dest="ttbarFileName",        default="", help="")
parser.add_option('--dataFileSLCR',             type = 'string', default = "", dest = 'inputDataFileSLCR', help = 'input Data File' )
parser.add_option('-m', '--mu_qcd',             dest="mu_qcd",               default=0, help="")
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

#
#  Get CR Counts
#
N_Data_CR  = getValues(dataFile,  "ReverseTTVetoFourTag" )["SignalZZ"]
N_QCD_CR   = getValues(dataFile,  "ReverseTTVetoTwoTag", float(o.mu_qcd) )["SignalZZ"]
N_QCD_CR_ERR = pow(N_Data_CR + (N_QCD_CR*0.06)**2,0.5)

#
#  Get epsilon
#
epsilon_vals = doInclusive("AfterMh", "SignalZZ", "_PassMh", dataFileSLC, dataFileSLC)
eps     = epsilon_vals["eff_c3_Data"]
eps_err_stat = epsilon_vals["eff_c3_Data_Err"]
eps_err_syst = 0.1*eps
eps_err      = pow((eps_err_stat**2 + eps_err_syst**2), 0.5)

print
print
print

print "N_Data_CR:",N_Data_CR
print "N_Data_CR:",N_QCD_CR,"+/-",N_QCD_CR_ERR
print "eps:",eps,"+/-",eps_err




f = eps*eps/(1-eps*eps)

N_tt_CR = (N_Data_CR - N_QCD_CR)
print "N_tt_CR:",N_tt_CR

#N_tt_CR_file = open(o.output+"N_tt_CR.tex","w")
#N_tt_CR_file.write("$N_{t\\bar{t}}^{CR,hh} = "+str(round(N_tt_CR,2))+" \pm "+str(round(N_QCD_CR_ERR,2))+"$\\\\")
#N_tt_CR_file.write("\n")
#N_tt_CR_file.close()

N_tt_SR = f * N_tt_CR

term1 = f * N_QCD_CR_ERR

f_term1 = 2*eps/(1-eps*eps) 
f_term2 = 2*eps*eps*eps/( (1-eps*eps)  * (1-eps*eps) )

print "f",f
print "f_term1: " , f_term1
print "f_term2: " , f_term2
print "f_term1+f_term2: " , f_term1+f_term2
print "f_err: " , (f_term1+f_term2)*eps_err

f_err = (f_term1 + f_term2)*eps_err

term2 = N_tt_CR * f_err

N_tt_CR = pow( (term1 * term1) + (term2 * term2), 0.5)

print 
print  "\tN_tt_SR:", N_tt_SR,"+/-",term1,"+/-",term2

N_tt_SR_file = open(o.output+"N_tt_ZZ.tex","w")
N_tt_SR_file.write("$N_{t\\bar{t}}^{SR,hh} = "+str(round(N_tt_SR,2))+" \pm "+str(round(term1,3))+" \\textrm{(QCD Bkg.)} \pm "+str(round(term2,3))+" \\textrm{ ($t\\bar{t}$-veto efficiency)} $\\\\")
N_tt_SR_file.write("\n")
N_tt_SR_file.close()
