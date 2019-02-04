import ROOT, rootlogon
import argparse
import array
import copy
import helpers
import os
import sys
import time

#import yaml

# Examples:
#   normal:
#      py  plot.py --plotter trigtrigsideband0  -c plotConfig.py
#   interactive:
#      py  -i plot.py --plotter iter0  -i -c plotIConfig.py
#       then:
#         plot("m4j_l","PassTrig","Control",plotter,logY=0,rebin=2)

from helpers import initHistory, save_history, parseOpts, plotterConfig
initHistory()
import atexit
atexit.register(save_history)

(opts, args) = parseOpts()


ROOT.gROOT.SetBatch(not opts.interactive)
#ROOT.gROOT.Macro("../post_processing/helpers.C")
#ROOT.gROOT.Macro("../post_processing/cross_sections.C")

timestamp = time.strftime("%Y-%m-%d-%Hh%Mm%Ss")


plotter    = {}

#watermarks = None
#legend   = None 
#shared   = None


#
#  Make the actual plot
#
def plot(var, cut, region, plotter_config,  **kw):
    helpers.clear()
    helpers.plot(var, cut, region, plotter_config, **kw)

def main():
    global plotter

    #                                                                                                                                               
    #  Executing the python                                                                                                                         
    #   (configGlobals and configLocals are used to pass vars                                                                                       
    #                                                                                                                                               
    configGlobals = {}
    configLocals  = {"inputDir":opts.inputDir,
                     "mu_qcd"     :float(opts.mu_qcd),
                     "mu_ttbar"   :float(opts.mu_ttbar),}
    print "Executing", opts.config
    execfile(opts.config, configGlobals, configLocals)

    #
    # Loop on plotters
    #
    plotterList = []
    for plotterFile in opts.plotter.split(","): 
        raw_plotter = configLocals["plot_configs"][plotterFile]
        
        #
        #  Config Plotter
        #
        configed_potter = plotterConfig(raw_plotter)
        
        #
        # Add plotter
        #
        plotterList.append(configed_potter)
        
        
    #
    #  Make Plots
    #
    for plotter in plotterList:
        
        # make money
        for iplot in plotter["plots"]:
            helpers.plot(iplot['variable'], plotter["cutName"], plotter["regionName"], plotter, **iplot)

        plotter["output"].Close()


def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

def warn(message):
    print
    print "Warning in %s: %s" % (__file__, message)
    print

def listDirs(plotter):
    plotter["files"][plotter["samples"][0]["name"]].ls()
    return

def example():
    print 'plot("leadHCand_leadJet_Pt","PassTrig","Sideband",plotter,logY=0,rebin=2)'


if __name__ == "__main__":
    main()
        
