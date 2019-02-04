#
# File that stores the config info for all plots. Should probably
# make set it up somehow so that this can be passed into plot.py as an argument
#

plot_configs = {}


#dirName     = "../../DataTestSubl2"
#qcdWeights = 1.22940

#dirName     = "../../DataTestSubl1"
#qcdWeights = 1.03541

#dirName     = "../../DataNoWeight"
#qcdWeights = 0.01399

#dirName     = "../../OutputDataFixOrdering"
#qcdWeights = 0.010219568956796047

#dirName     = "../../OutputData"
#qcdWeights  = 0.007420133592017816

#dirName     = "../../OutputData-v00-04-00"
#qcdWeights  = 0.0075388243343757115

dirName     = inputDir
#qcdWeights  = 0.007488000625631198
#qcdWeights  = 0.007639839014083001
#qcdWeights  = 0.007860764124790816
#qcdWeights  = 0.008715225210083975

# no reweight
#qcdWeights  = 0.008729326341303403


# w/reweight
#qcdWeights  = 1.03634679893

# v00-05-00
#qcdWeights  = 0.008603628161961826

# v00-06-00
#qcdWeights = 0.007601240940842158

# v00-06-00
#qcdWeights = 0.00759726390243
#qcdWeights = (0.0079771270975515/1.05)
#qcdWeights = 0.0079771270975515
#qcdWeights = 0.00810079742223 # iter0
#qcdWeights = 0.00830938802066  # iter1

#qcdWeights = 0.00841745361686 # iter0 test Trig

print 
samples = {}

samples["interactive"] = [ 
#    {
#        'name'      : 'data',
#        'is_data'   : True,
#        'stack'     : False,
#        'overlay'   : True,
#        'path'      : dirName+'/hist-tree.root',
#        'folderReg' : None,
#        'folderCuts': None,
#        'folderTag' : 'FourTag_',
#        'label'     : 'Data',
#        'color'     : 'ROOT.kBlack',
#        'rColor'     : 'ROOT.kRed-3',
#        'weights'   : 1
#        },
#
#
#    {
#        'name'      : 'qcd',
#        'is_data'   : False,
#        'stack'     : True,
#        'overlay'   : False,
#        'path'      : dirName+'/hist-tree.root',
#        'folderReg' : None,
#        'folderCuts': None,
#        'folderTag' : 'TwoTag_',
#        'label'     : "QCD",
#        'color'     : 'ROOT.kYellow',
#        'rColor'     : 'ROOT.kRed-3',
#        'weights'   : mu_qcd
#        },
#
#
#    {
#        'name'       : '4b tt',
#        'is_data'    : False,
#        'stack'      : True,
#        'overlay'    : False,
#        'path'       : dirName+'/ttbar/hist-tree.root',
#        'folderReg'  : None,
#        'folderCuts' : None,
#        'folderTag'  : 'FourTag_',
#        'label'      : "ttbar",
#        'color'      : 'ROOT.kAzure-9',
#        'rColor'     : 'ROOT.kBlue',
#        'weights'    : 1
#        } ,


    {
        'name'      : 'data',
        'is_data'   : True,
        'stack'     : False,
        'overlay'   : True,
        'path'      : dirName+"/hist-tree.root",
        'folderReg' : None,
        'folderCuts': None,
        'folderTag' : 'FourTag_',
        'label'     : 'Data',
        'color'     : 'ROOT.kBlack',
        'rColor'    : 'ROOT.kRed-3',
        'weights'   : 1.0
        },
    {
        'name'      : 'qcd',
        'is_data'   : False,
        'stack'     : True,
        'overlay'   : False,
        'path'      : dirName+'/qcd/hist-tree.root',
        'folderReg' : None,
        'folderCuts': None,
        'folderTag' : 'TwoTag_',
        'label'     : "QCD",
        'color'     : 'ROOT.kYellow',
        'rColor'    : 'ROOT.kRed-3',
        'weights'   : mu_qcd
        },

    {
        'name'       : 'ttbar',
        'is_data'    : False,
        'stack'      : True,
        'overlay'    : False,
        'path'       : dirName+'/ttbar/hist-tree.root',
        'folderReg'  : None,
        'folderCuts' : None,
        'folderTag'  : 'TwoTag_',
        'label'      : "ttbar",
        'color'      : 'ROOT.kAzure-9',
        'rColor'     : 'ROOT.kRed-3',
        'weights'    : mu_ttbar # mu _ttbar
        },

#    {
#        'name'      : 'signal',
#        'is_data'   : False,
#        'stack'     : False,
#        'overlay'   : True,
#        'path'      : signal,
#        'folderReg' : None,
#        'folderCuts': None,
#        'folderTag' : 'FourTag_',
#        'label'     : 'M800',
#        'color'     : 'ROOT.kRed',
#        'rColor'    : 'ROOT.kRed-3',
#        'weights'   : (0.577)**2 #h->bb BR squared
#        },




]


#
# List of plots to make for resolved analysis from the post processing hists
#

plotsList = [ ]

print samples

plot_configs["interactive"] = {
    "directory": dirName+"/plots",
    "output": "test.root",
    "ratio": True,
    "lumi": "3.3 fb^{-1}",
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "samples": samples["interactive"],
    "useTree" : False,
    "plots": plotsList,
    }

