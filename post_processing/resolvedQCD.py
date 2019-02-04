"""
qcd.py: a script to convert ntuples into a multijet ntuple.

$ python qcd.py --wp=70
"""
import argparse
import array
import copy
import os
import sys
import ROOT
import glob
import time

treename  = "XhhMiniNtuple"

ROOT.gROOT.SetBatch()
ROOT.gROOT.Macro("helpers.C")

def main():

    ops = options()

    if not ops.wp in ["60", "70", "77", "85"]:
        fatal("Please give a supported --wp like 70 or 77")

    hcand_4vec = ["hcand_resolved_pt[0], hcand_resolved_eta[0], hcand_resolved_phi[0], hcand_resolved_m[0]",
                  "hcand_resolved_pt[1], hcand_resolved_eta[1], hcand_resolved_phi[1], hcand_resolved_m[0]"]

    m4j = "inv_mass("+hcand_4vec[0]+", "+hcand_4vec[1]+")"

    #m4j dependent higgs candidate pt cuts
    CutPtLead    = " || ".join(["(hcand_resolved_pt[0] > 400e3                                    && "+m4j+" > 910e3)",
                                "(hcand_resolved_pt[0] > (0.650*"+m4j+"-190e3) && "+m4j+" > 600e3 && "+m4j+" < 910e3)",
                                "(hcand_resolved_pt[0] > 200e3                 && "+m4j+" < 600e3)"])

    CutPtSubLead = " || ".join(["(hcand_resolved_pt[1] > 260e3                                    && "+m4j+" > 990e3)",
                                "(hcand_resolved_pt[1] > (0.235*"+m4j+"+ 28e3) && "+m4j+" > 520e3 && "+m4j+" < 990e3)",
                                "(hcand_resolved_pt[1] > 150e3                 && "+m4j+" < 520e3)"])

    CutEta       = " || ".join(["abs(hcand_resolved_eta[0] - hcand_resolved_eta[1]) < 1.55e-6*"+m4j+"-0.271 && "+m4j+" > 820e3",
                                "abs(hcand_resolved_eta[0] - hcand_resolved_eta[1]) < 1                     && "+m4j+" < 820e3"])

    preSelection = ["hcand_resolved_n >= 2",
                    "hcand_resolved_pt[0] > 200e3",
                    "hcand_resolved_pt[1] > 150e3"]

    selection = [CutPtLead,
                 CutPtSubLead,
                 CutEta
                 ]

    selection = " && ".join(["(%s)" % sel for sel in selection])

    MV2c20wp = {"60": " 0.4496",
                "70": "-0.0436",
                "77": "-0.4434",
                "85": "-0.7887",
                }
    #need to explicitly cut on mv2 now that we are selecting bjets at 90%
    b00 = "(jet_ak4emtopo_asso_MV2c20[0][0] > "+MV2c20wp[ops.wp]+")"
    b01 = "(jet_ak4emtopo_asso_MV2c20[0][1] > "+MV2c20wp[ops.wp]+")"
    b10 = "(jet_ak4emtopo_asso_MV2c20[1][0] > "+MV2c20wp[ops.wp]+")"
    b11 = "(jet_ak4emtopo_asso_MV2c20[1][1] > "+MV2c20wp[ops.wp]+")"
    
    #all possible ways to get exactly two btags
    # twotag = " || ".join([    b00 + "&&" +     b01 + "&&" + "!"+b10 + "&&" + "!"+b11,
    #                           b00 + "&&" + "!"+b01 + "&&" +     b10 + "&&" + "!"+b11,
    #                           b00 + "&&" + "!"+b01 + "&&" + "!"+b10 + "&&" +     b11,
    #                       "!"+b00 + "&&" +     b01 + "&&" +     b10 + "&&" + "!"+b11,
    #                       "!"+b00 + "&&" +     b01 + "&&" + "!"+b10 + "&&" +     b11,
    #                       "!"+b00 + "&&" + "!"+b01 + "&&" +     b10 + "&&" +     b11])

    #inclusive twotag region for preSelection:
    preSelTwoTag = " || ".join(["(" + b00 + "&&" + b01 + ")",
                                "(" + b10 + "&&" + b11 + ")"])
    preSelection.append(preSelTwoTag)
    preSelection = " && ".join(["(%s)" % sel for sel in preSelection])

    #one or other dijet has 2bjets but not both
    twotag  = " || ".join(["(" +    b00 + "&&" +     b01 + "&&" + "!"+b10 + "&&" + "!"+b11 + ")",
                           "(" +"!"+b00 + "&&" + "!"+b01 + "&&" +     b10 + "&&" +     b11 + ")"])

    fourtag = b00 + "&&" + b01 + "&&" + b10 + "&&" + b11
    
    #sideband = "ResolvedPass_SidebandMass"
    sideband = "((hcand_resolved_m[0]/1000 - 124.0)**2 + (hcand_resolved_m[1]/1000 - 115.0)**2)**0.5 > 58.0"
    
    outputQCD    = "../../skims/qcd_%swp_v00-01-02.root" % (ops.wp)
    output4b     =  "../../skims/4b_%swp_v00-01-02.root" % (ops.wp)

    files = {}
    trees = {}
    skims = {}

    # inputs
    files["data"] = input_data()
    files["mc"]   = input_mc()

    for sample in ["data", "mc"]:

        trees[sample] = ROOT.TChain(treename)
        print trees[sample],treename,sample
        for fi in files[sample]:
            if len(fi) > 120: print fi[:50]+"..."+fi[len(fi)-50:]
            else: print fi
            trees[sample].Add(fi)

        if trees[sample].GetEntries() > 0:
            print time.strftime("%H:%M:%S"),"Copying Tree:",sample
            print "Before preSelection:",trees[sample].GetEntries()
            skims[sample] = trees[sample].CopyTree(preSelection)
            print " After preSelection:",skims[sample].GetEntries()
            skims[sample] = skims[sample].CopyTree(selection)
        else:
            skims[sample] = trees[sample]
            continue

        weight = 1 if sample == "data" else -1
        skims[sample] = add_branches(skims[sample], [("weight_qcd", weight, "I")])

    if skims["data"].GetEntries() == 0:
        fatal("No data entries found. Exiting.")
        
    # merge
    print time.strftime("%H:%M:%S"),"Merging:"
    print "   Data,",skims["data"]
    print "     MC,",skims["mc"]
    skim = merge_trees(skims["data"], skims["mc"])

    #
    # Calculate Weights
    #

    # derive mu_qcd and uncertainty
    print time.strftime("%H:%M:%S"),"Deriving mu_qcd"
    mu_qcd, mu_qcd_stat = get_mu_qcd(skim, twotag=twotag, fourtag=fourtag, topo=sideband, weight="weight_qcd")

    # add branches to tree
    branches = [("Resolved_nbjets",         4,      "I"),
                ("weight_mu_qcd",      mu_qcd,      "F"),
                ("weight_mu_qcd_stat", mu_qcd_stat, "F")]
    
    skim = add_branches(skim, branches)

    # iterate over skimmed tree to calculate kinematic weights for events
    kinematicWeightVars = ["hcand_resolved_pt[0]",
                           "hcand_resolved_dRjj[1]"]

#    for i in range(10):
#        kinematic_reweight(skim, kinematicWeightVars)

   
    #
    # Store trees for Four Tag Region and QCD prediction
    #

    # write 4b
    print time.strftime("%H:%M:%S"),"Copy 4-tag region"
    outfile4b = ROOT.TFile.Open(output4b, "recreate")
    tree4b = skim.CopyTree("1")
    #tree4b.ResetBranchAddresses()
    #print time.strftime("%H:%M:%S"),"Write output4b  file:",output4b,tree4b.GetEntries()
    #outfile4b.cd()
    #tree4b.Print()
    #outfile4b.Write()
    #outfile4b.Close()

    # write QCD
    # print time.strftime("%H:%M:%S"),"Copy 2-tag region"
    # outfileQCD = ROOT.TFile.Open(outputQCD, "recreate")
    # qcd = skim.CopyTree(twotag)
    # qcd.ResetBranchAddresses()
    # print time.strftime("%H:%M:%S"),"Write outputQCD file:",outputQCD,qcd.GetEntries()
    # outfileQCD.cd()
    # qcd.Print()
    # outfileQCD.Write()

    # # summarize
    # template = "%15s | %12s | %12s"
    # print
    # print time.strftime("%H:%M:%S")
    # print " skim summary"
    # print "-"*45
    # print template % ("", "data entries", "mc entries")
    # print "-"*45
    # print template % ("    input trees",   trees["data"].GetEntries(), trees["mc"].GetEntries())
    # print template % ("after selection",   skims["data"].GetEntries(), skims["mc"].GetEntries())
    # print
    # print
    # print " output filesize"
    # print "-"*45
    # print " %.4f MB" % (outfileQCD.GetSize()/pow(1024.0, 2))
    # print

    # # skims["mc"].GetEntries()

    # outfileQCD.Close()
    # skims["mc"].GetEntries()
    # print "closed qcd file"
    # tree4b.Delete()
    # qcd.Delete()
    # skim.Delete()
    # print "deleted skim,tree4b,qcd"
    # trees["data"].Delete()
    # print "deleted data tree"
#    skims["mc"].Delete()
#    print "deleted mc skim"
#    skims["data"].Delete()
#    print "deleted data skim"
    #trees["mc"].Delete()
    #print "deleted mc tree"

    #skims["data"].Delete()
    #print "deleted data skim"


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wp")
    return parser.parse_args()

def fatal(message):
    sys.exit("Error in %s: %s" % (__file__, message))

def merge_trees(skims_data, skims_mc):
    inputs = ROOT.TList()
    inputs.Add(skims_data)
    if skims_mc.GetEntries():
        inputs.Add(skims_mc)
        print "Adding MC to data"
    else:
        print "MC is empty, just using data"
        return skims_data
    dummy = ROOT.TTree(treename, treename)
    #dummy2  = dummy.MergeTrees(inputs)
    #dummy.Delete()
    return dummy.MergeTrees(inputs)

def add_branches(tree, pairs):

    contents = {}
    branches = {}

    for name, value, type in pairs:
        print "adding:",name,value
        contents[name] = array.array(type.lower(), [value])
        branches[name] = tree.Branch(name, contents[name], name+"/"+type)

    for entry in tree:
        for name, value, type in pairs:
            branches[name].Fill()

    return tree

def input_data():
    #return ["/afs/cern.ch/work/p/pbryant/miniNTuple_D3-E3_v00-01-02.root"]
    #return ["/afs/cern.ch/work/p/pbryant/miniNTuple_D3-E3_v00-01-01.root"]
    #return ["/afs/cern.ch/work/p/pbryant/miniNTuple_D3-E3_v00-01-00.root"]

    #test files
    #return glob.glob("/afs/cern.ch/work/p/pbryant/miniNTuples-v00-01-02/group.phys-exotics.data15_13TeV.00279345.physics_Main.hh4b_v00-01-02_MiniNTuple.root/*")
    return ["/afs/cern.ch/work/p/pbryant/miniNTuples-v00-01-02/group.phys-exotics.data15_13TeV.00279345.physics_Main.hh4b_v00-01-02_MiniNTuple.root/group.phys-exotics.6728706._000001.MiniNTuple.root"]

def input_mc():
    return []

def get_mu_qcd(tree, twotag, fourtag, topo, weight):
    """ 
    If we make this topology-dependent, 
    maybe we return an entire histogram? TBD.
    topo is "PassSidebandmass" or controlband mass etc?
    """
    numer = ROOT.TH1F("numer", "numer", 1, 0, 1)
    denom = ROOT.TH1F("denom", "denom", 1, 0, 1)
    for hist in [numer, denom]:
        hist.Sumw2()

    print "Calculating Numerator"
    tree.Draw("0.5 >> numer", "( (%s) && (%s))*(%s)" % (fourtag, topo, weight), "goff")
    print "Calculating Denominator"
    tree.Draw("0.5 >> denom", "( (%s) && (%s))*(%s)" % ( twotag, topo, weight), "goff")

    divide = copy.copy(numer)
    divide.Reset()
    divide.Divide(numer, denom)

    print 
    print " mu_qcd calculation:"
    print "-"*45
    print " %5.1f / %7.1f  =  %7.5f (%7.5f)" % (numer.GetBinContent(1), denom.GetBinContent(1), divide.GetBinContent(1), divide.GetBinError(1))
    print

    return [divide.GetBinContent(1), divide.GetBinError(1)]

# def kinematic_reweight(tree, variables = {}, current_weights = {}):
#     """
#     Reweight events by 1-D kinematic distributions, current_weights
#     start at 1, iterate this function until they converge
#     """
#     if not current_weights: #entering first iteration, initialize branches to store weights
#         for var, bins in variables.iteritems():
#             bins_array = array.array("d", [float(x) for x in bins])
#             current_weights[var] = ROOT.TH1F("weight_"+var, var, len(bins_array)-1, bins_array)

#     for event in tree:
        
        

#     return new_weights

if __name__ == '__main__': 
    main()
