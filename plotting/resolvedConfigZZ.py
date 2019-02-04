#
# File that stores the config info for all plots. Should probably
# make set it up somehow so that this can be passed into plot.py as an argument
#

plot_configs = {}

# before switching to only QCD hcand container
#  (1139.0 -  28.0) / (131628.0 -  1821.4)  =  0.00856 (0.00026) #iter0
# #iter1
# After swtiching to only QCD hcand container
#  (894.0 -  13.8) / (131628.0 -  1771.5)  =  0.00678 (0.00023) #iter0
#  0.00697 #iter1
# After sorting dijets by MV2 
# (1188.0 -  29.2) / (155265.0 -  2448.8)  =  0.00758 (0.00023) and after reweight (N_4b - N_tt4b)/(N_2b - N_tt2b) = 1158.8 / 147384.1  =  0.00786

lumi        = lumi+" fb^{-1}"

samples = {}

samples["main"] = [ 
    {
        'name'      : 'data',
        'is_data'   : True,
        'stack'     : False,
        'overlay'   : True,
        'path'      : data,
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
        'path'      : qcd,
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
        'path'       : ttbar,
        'folderReg'  : None,
        'folderCuts' : None,
        'folderTag'  : 'TwoTag_',
        'label'      : "ttbar",
        'color'      : 'ROOT.kAzure-9',
        'rColor'     : 'ROOT.kRed-3',
        'weights'    : mu_ttbar
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
#        }
]



samples["cutflow"] = [ {
        'name'       : 'data',
        'is_data'    : True,
        'stack'      : False,
        'overlay'    : False,
        'path'       : data,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "",
        'color'      : 'ROOT.kBlack',
        'weights'    : 1
}]
samples["cutflowttbar"] = [ {
        'name'       : 'ttbar',
        'is_data'    : True,
        'stack'      : False,
        'overlay'    : False,
        'path'       : ttbar,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "",
        'color'      : 'ROOT.kBlack',
        'weights'    : 1
}] 

samples["2d"] = [ {
        'name'       : 'dijetMassPlane',
        'is_data'    : True,
        'stack'      : False,
        'overlay'    : False,
        'path'       : data,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : 'TwoTag_',
        'label'      : "",
        'color'      : 'ROOT.kAzure-9',
        'rColor'     : 'ROOT.kRed-3',
        'weights'    : 1
        } ] 

samples["weights"] = [ {
        'name'       : '4b/2b',
        'is_data'    : True,
        'stack'      : False,
        'overlay'    : False,
        'path'       : weights,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "",
        'color'      : 'ROOT.kBlack',
        'weights'    : 0.125
}] 

samples["systematics"] = [ {
        'name'       : 'systematics',
        'is_data'    : True,
        'stack'      : False,
        'overlay'    : False,
        'path'       : systematics,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "",
        'color'      : 'ROOT.kBlack',
        'weights'    : 1
}] 

samples["QCDShapeUp"] = [ {
        'name'       : 'Shape Up',
        'is_data'    : True,
        'stack'      : False,
        'overlay'    : True,
        'path'       : systematics,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "Plus Shape",
        'color'      : 'ROOT.kBlack',
        'weights'    : 1
},{
        'name'       : 'Nominal',
        'is_data'    : False,
        'stack'      : True,
        'overlay'    : False,
        'path'       : systematics,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "Nominal",
        'color'      : 'ROOT.kYellow',
        'weights'    : 1
}] 

samples["QCDShapeDown"] = [ {
        'name'       : 'Shape Down',
        'is_data'    : True,
        'stack'      : False,
        'overlay'    : True,
        'path'       : systematics,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "Minus Shape",
        'color'      : 'ROOT.kBlack',
        'weights'    : 1
},{
        'name'       : 'Nominal',
        'is_data'    : False,
        'stack'      : True,
        'overlay'    : False,
        'path'       : systematics,
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "Nominal",
        'color'      : 'ROOT.kYellow',
        'weights'    : 1
}] 

samples["sensitivity"] = [ {
        'name'       : 'Highest MV2',
        'is_data'    : True,
        'stack'      : False,
        'overlay'    : True,
        'path'       : 'sensitivityHighestMV2.root',
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "Highest MV2",
        'color'      : 'ROOT.kBlack',
        'rColor'     : 'ROOT.kRed-3',
        'weights'    : 1
},{
        'name'       : 'Highest Mass',
        'is_data'    : False,
        'stack'      : True,
        'overlay'    : False,
        'path'       : 'sensitivityBiasFix.root',
        'folderReg'  : "",
        'folderCuts' : "",
        'folderTag'  : "",
        'label'      : "Highest Mass",
        'color'      : 'ROOT.kAzure-9',
        'rColor'     : 'ROOT.kRed-3',
        'weights'    : 1
}] 


#
# List of plots to make for resolved analysis from the post processing hists
#

plotsList = [ ]

plot_configs["main"] = {
    "directory": outputDir,
    "output": "test.root",
    "ratio": True,
    "ks": False,
    "chi2": True,
    "lumi": lumi,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "samples": samples["main"],
    "useTree" : False,
    "plots": plotsList,
    }


plot_configs["cutflow"] = {
    "directory": outputDir,
    "output": "test.root",
    "ratio": False,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "lumi": lumi,
    "samples": samples["cutflow"],
    "useTree": False,
    "plots": plotsList
    }

plot_configs["cutflowttbar"] = {
    "directory": outputDir,
    "output": "test.root",
    "ratio": False,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "lumi": lumi,
    "samples": samples["cutflowttbar"],
    "useTree": False,
    "plots": plotsList
    }

plot_configs["2d"] = {
    "directory": outputDir,
    "output": "test.root",
    "ratio": False,
    "lumi": lumi,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "samples": samples["2d"],
    "useTree": False,
    "plots": plotsList
    }

plot_configs["weights"] = {
    "directory": outputDir,
    "output": "test.root",
    "ratio": False,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "lumi": lumi,
    "samples": samples["weights"],
    "useTree": False,
    "plots": plotsList
    }

plot_configs["systematics"] = {
    "directory": outputDir,
    "output": "test.root",
    "ratio": False,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "lumi": lumi,
    "samples": samples["systematics"],
    "useTree": False,
    "plots": plotsList
    }

plot_configs["QCDShapeUp"] = {
    "directory": outputDir,
    "output": "test.root",
    "ratio": True,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "lumi": lumi,
    "samples": samples["QCDShapeUp"],
    "useTree": False,
    "plots": plotsList
    }

plot_configs["QCDShapeDown"] = {
    "directory": outputDir,
    "output": "test.root",
    "ratio": True,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "lumi": lumi,
    "samples": samples["QCDShapeDown"],
    "useTree": False,
    "plots": plotsList
    }

plot_configs["sensitivity"] = {
    "directory": "sensitivityFiles",
    "output": "test.root",
    "ratio": True,
    "ks": False,
    "lumi": lumi,
    "autoRatio": False,
    "systematics": False,
    "data": False, #FIXME
    "samples": samples["sensitivity"],
    "useTree" : False,
    "plots": plotsList,
    }
