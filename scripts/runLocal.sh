# xAH_run.py  --files /share/t3data3/johnda/samples/mc15_13TeV.301497.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1200.merge.DAOD_EXOT8.e3820_s2608_s2183_r6869_r6282_p2454/DAOD_EXOT8.07033790._000001.pool.root.1  --config XhhCommon/scripts/combinedMaster.py  --submitDir NewTestM1200 -f --nevents 300  --isMC direct

#inDS=mc15_13TeV.301495.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1000.merge.DAOD_EXOT8.e3820_s2608_s2183_r7772_r7676_p2669
#inDS=mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.merge.DAOD_EXOT8.e4135_s2608_s2183_r7725_r7676_p2719
#inDS=mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.merge.DAOD_EXOT8.e3698_s2608_s2183_r7725_r7676_p2719
#inDS=mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.merge.DAOD_EXOT8.e3698_s2608_s2183_r7725_r7676_p2839
#inDS=mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.merge.DAOD_EXOT8.e4135_s2608_s2183_r7725_r7676_p2839
#inDS=mc15_13TeV.301490.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M500.merge.DAOD_EXOT8.e3820_s2608_s2183_r7772_r7676_p2952
inDS=mc15_13TeV.301488.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M300.merge.DAOD_EXOT8.e3820_s2608_s2183_r7772_r7676_p2952
#inDS=mc15_13TeV.342619.aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_hh_4b.merge.DAOD_EXOT8.e4419_s2608_r7772_r7676_p2952
echo xAH_run.py  --files $inDS   --config XhhCommon/scripts/combinedMaster.py  --submitDir NewTestHH -f --nevents -1 --inputRucio  --isMC direct


