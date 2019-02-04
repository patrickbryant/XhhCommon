##!/bin/bash
#python xAODAnaHelpers/scripts/checkoutASGtags.py $1
##the baseline rc is 2.4.31 now!


# fix bug 
svn co svn+ssh://svn.cern.ch/reps/atlasoff/PhysicsAnalysis/AnalysisCommon/AssociationUtils/tags/AssociationUtils-01-01-50 AssociationUtils

# The default version for JetUncertainties in 2.4.25 is 00-09-55. We still check it out for patching below
#svn co svn+ssh://svn.cern.ch/reps/atlasoff/Reconstruction/Jet/JetUncertainties/tags/JetUncertainties-00-09-63 JetUncertainties

# Check out teh BJet Trigger Emulation Tool (Will be added to the realease soon) 
git clone https://:@gitlab.cern.ch:8443/cvarni/TrigBtagEmulationTool.git
cd TrigBtagEmulationTool
git checkout TrigBtagEmulationTool-00-01-09
cd -

# Check out the hh reweighting tool
git clone https://:@gitlab.cern.ch:8443/johnda/hhTruthWeightTools.git 
cd hhTruthWeightTools
git checkout hhTruthWeightTools-00-00-00
cd -

# copying the CDI file is no longer needed. (Use the path resolver.)

# KL Fitter
#svn co svn+ssh://svn.cern.ch/reps/atlasoff/PhysicsAnalysis/TopPhys/KLFitter/tags/KLFitter-00-07-05 KLFitter 
#svn co svn+ssh://svn.cern.ch/reps/atlasoff/AsgExternal/Asg_BAT/tags/Asg_BAT-00-09-04-01 Asg_BAT

#apply a fix for jet uncertainties
#derived from 00-09-51, but also confirmed to be compatible with 00-09-55
#patch -d JetUncertainties -p0 < XhhCommon/patch.patch


#new JSS tagging tool; or user@gitlab.cern.ch
#
#  SHOULD NOT USE HEAD OF PACKAGE HERE!
#    - 1) unstable and often causes complilation errors
#    - 2) makes it hard/impossible to know which code was used after the fact/by different users
# git clone "https://"$USER$"@gitlab.cern.ch/JSSTools/BoostedJetTaggers.git"
#git clone "https://"$USER$"@gitlab.cern.ch/JSSTools/BoostedJetTaggers.git"
#
#cd BoostedJetTaggers
#git checkout 7d5d12812766b2ab4be56d0392d54800d2129b46
#cd ..
