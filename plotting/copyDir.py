import os

import optparse
parser = optparse.OptionParser()
parser.add_option('-a','--all',       action="store_true",          dest="doAll",          default=False, help="")
parser.add_option('--signal',         action="store_true",          dest="doSignal",       default=False, help="")
parser.add_option('--JERVars',        action="store_true",          dest="doJERVars",      default=False, help="")
parser.add_option('--data',           action="store_true",          dest="doData",         default=False, help="")
parser.add_option('--ttbar',          action="store_true",          dest="doTTBar",        default=False, help="")
parser.add_option('--zjets',          action="store_true",          dest="doZJets",        default=False, help="")
parser.add_option('--slcr',           action="store_true",          dest="doSLCR",         default=False, help="")
parser.add_option('--limits',         action="store_true",          dest="doLimits",       default=False, help="")
parser.add_option('--test',           action="store_true",          dest="doTest",         default=False, help="")
parser.add_option('--inputDir',                                     dest="inputDir",       default=False, help="")
parser.add_option('--iteration',                                    dest="iteration",      default="0", help="")
o, a = parser.parse_args()


inputTag = o.inputDir #"TestNewTrig2b00-06-00"

t3dir = "/share/t3data3/johnda/samples/XhhOutput/"+inputTag
localDir = "hists-"+inputTag



if not os.path.isdir(localDir):
    os.system("mkdir "+localDir)


#
#  Mu QCD
#
if o.doAll or o.doData:
    muQCDFiles = ["mu_qcd-"+str(o.iteration)+".txt","weights2bto4b"+str(int(o.iteration)+1)+".root"]
    for m in muQCDFiles:
        cmd = "scp uct3.uchicago.edu:"+t3dir+"/"+m+" "+localDir
        print cmd
        if not o.doTest: os.system(cmd)

#
# Get Data and Backgrounds
#
if o.doAll or o.doData or o.doTTBar or o.doSLCR or o.doZJets:
    getHistTree = []
    if o.doAll or o.doData:
        getHistTree += ["histsData-"+str(o.iteration),"histsQCD-"+str(o.iteration)]
    if o.doAll or o.doTTBar:
        getHistTree += ["histsTTbar-"+str(o.iteration)]
    if o.doAll or o.doZJets:
        getHistTree += ["histsZJets-"+str(o.iteration)]
    if o.doAll or o.doSLCR:
        getHistTree += ["histsData-SLCR","histsTTbar-SLCR"]

    for d in getHistTree:
        thisLocalDir = localDir + "/"+d
        if not os.path.isdir(thisLocalDir):
            cmd = "mkdir "+thisLocalDir
            print cmd
            if not o.doTest: os.system(cmd)
        cmd = "scp uct3.uchicago.edu:"+t3dir+"/"+d+"/hist-tree.root "+thisLocalDir
        print cmd
        if not o.doTest: os.system(cmd)



#
# Get signal
#
if o.doAll or o.doSignal:
    localSignalDir = localDir+"/histsSignal"
    if not os.path.isdir(localSignalDir):
        if not o.doTest: os.system("mkdir "+localSignalDir)    


    signalSubDirs = [
        "hh_4b",
        "RSG_c05_M500","RSG_c05_M1000",
        "RSG_c10_M300","RSG_c10_M400","RSG_c10_M500","RSG_c10_M600","RSG_c10_M700","RSG_c10_M800","RSG_c10_M900","RSG_c10_M1000","RSG_c10_M1100","RSG_c10_M1200","RSG_c10_M1300","RSG_c10_M1400","RSG_c10_M1500",
        "RSG_c20_M300","RSG_c20_M400","RSG_c20_M500","RSG_c20_M600","RSG_c20_M700","RSG_c20_M800","RSG_c20_M900","RSG_c20_M1000","RSG_c20_M1100","RSG_c20_M1200","RSG_c20_M1300","RSG_c20_M1400","RSG_c20_M1500",
        "Hhh_M300","Hhh_M400","Hhh_M500","Hhh_M600","Hhh_M700","Hhh_M800","Hhh_M900","Hhh_M1000","Hhh_M1100","Hhh_M1200","Hhh_M1300","Hhh_M1400","Hhh_M1500",
        ]
    # signalSubDirs  = ["_301486", "_301487","_301488",
    #                   "_301489", "_301490","_301491","_301492","_301493","_301494","_301495","_301496","_301497","_301498","_301500",
    #                   "_301509", "_301510","_301511","_301512","_301513","_301514","_301515","_301516","_301517","_301518","_301519","_301520",]

    for s in signalSubDirs:
        thisLocalDir =  localSignalDir + "/"+s
        if not os.path.isdir(thisLocalDir):
            if not o.doTest: os.system("mkdir "+thisLocalDir)
        cmd = "scp uct3.uchicago.edu:"+t3dir+"/"+s+"_XhhMiniNtuple-0/hist-tree.root "+thisLocalDir
        print cmd
        if not o.doTest: os.system(cmd)


#
# Get JER Var
#
if o.doAll or o.doJERVars:
    
    sysVars = [
        "XhhMiniNtupleResolved_JET_GroupedNP_1__1down/",
        "XhhMiniNtupleResolved_JET_GroupedNP_1__1up/"  ,
        "XhhMiniNtupleResolved_JET_GroupedNP_2__1down/",
        "XhhMiniNtupleResolved_JET_GroupedNP_2__1up/"  ,
        "XhhMiniNtupleResolved_JET_GroupedNP_3__1down/",
        "XhhMiniNtupleResolved_JET_GroupedNP_3__1up/"  ,
        "XhhMiniNtupleResolved_JET_JER_SINGLE_NP__1up/",
        ]

    signalSubDirs = [
        "RSG_c10_M500","RSG_c10_M1000","RSG_c10_M1200"
        ]

    
    for sys in sysVars:
        localSignalDir = localDir+"/histsSignal/"+sys
        if not os.path.isdir(localSignalDir):
            if not o.doTest: os.system("mkdir "+localSignalDir)    

        for sig in signalSubDirs:
            thisLocalDir =  localSignalDir + "/"+sig
            if not os.path.isdir(thisLocalDir):
                if not o.doTest: os.system("mkdir "+thisLocalDir)
            cmd = "scp uct3.uchicago.edu:"+t3dir+"/"+sys+"/"+sig+"_XhhMiniNtuple-0/hist-tree.root "+thisLocalDir
            print cmd
            if not o.doTest: os.system(cmd)


#
# LimitSetting
#
if o.doAll or o.doLimits:
    localLimitSetting = localDir+"/LimitSettingInputs/"
    if not os.path.isdir(localLimitSetting):
        if not o.doTest: os.system("mkdir "+localLimitSetting)    
    
    if not o.doTest: os.system("scp uct3.uchicago.edu:"+t3dir+"/LimitSettingInputs/resolved_4bSR.root "+localLimitSetting)    



