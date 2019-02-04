#!/bin/bash 
#Script for submitting production of multiple ntuples on the grid

#################################################
## DEFINE INPUT, TESTAREA AND OUTPUT

filenamelist=/afs/cern.ch/work/l/lazovich/hh/4bAnaCode_devel_r20/run/grid_qcd.txt
yourtestarea=/afs/cern.ch/work/l/lazovich/hh/4bAnaCode_devel_r20 ## replace with here if you don't have a testarea
youroutputarea=/afs/cern.ch/work/l/lazovich/hh/4bAnaCode_devel_r20/grid_output ##your output area
#################################################

#tmpworkdir=$youroutputarea/run_$LSB_JOBID_.$LSB_JOBINDEX
#mkdir $tmpworkdir

#Setup root core
export AtlasSetup=/afs/cern.ch/atlas/software/dist/AtlasSetup
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
cd $yourtestarea
rcSetup -u #unsetup whatever
cd $yourtestarea
source grid_setup.sh
source rcSetup.sh #redo the setup

CONFIG=$yourtestarea/XhhCommon/data/runXhhTestGRID.config ##the data configuration file place
while read -r line
do
    arrIN=(${line//./ })
    suffix="${arrIN[1]}.${arrIN[2]}.minintuple"
    echo $suffix
    cp $CONFIG ./run/runMiniNtuple_$suffix.config
    sed -i "/DQ2Dataset/c DQ2Dataset         ${line}" ./run/runMiniNtuple_$suffix.config ##sent the input file
    sed -i "/SubmitDir/c SubmitDir         submit_${suffix}" ./run/runMiniNtuple_$suffix.config ##sent the input file
    sed -i "/maxEvents/c maxEvents         -1" ./run/runMiniNtuple_$suffix.config
    sed -i "/OutputDir/c OutputDir         user.lazovich.${suffix}" ./run/runMiniNtuple_$suffix.config
    cd $yourtestarea
    echo "current directory" $PWD
    runMiniNtupleGrid ./run/runMiniNtuple_${suffix}.config $youroutputarea/${suffix} &> $youroutputarea/${suffix}.log &
done < "$filenamelist"


# # # # # # # # # # # # # #
#--> Manage your output; check the ouptput from your job

# eos mkdir $eosoutputarea/ESD
# eos mkdir $eosoutputarea/AOD

# xrdcp $OUTESD root://eosatlas/$eosoutputarea/ESD/$OUTESD
# xrdcp $OUTAOD root://eosatlas/$eosoutputarea/AOD/$OUTAOD

#mv xAOD.pool.root $OUTFILE
#xrdcp $OUTFILE root://eosatlas/$eosoutputarea/$OUTFILE


