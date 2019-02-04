

py XhhCommon/plotting/plotTrigger.py OutputSignal-v00-04-00/_301490/hist-tree.root  --out TrigEffm500
py XhhCommon/plotting/plotTrigger.py OutputSignal-v00-04-00/_301495/hist-tree.root  --out TrigEffm1000
py XhhCommon/plotting/plotTrigger.py OutputTTbar-v00-04-01/hist-tree.root  --out TrigEffTTBar


py XhhCommon/plotting/plotTTBarVars.py -t OutputTTbar-v00-04-01/hist-tree.root --m500 OutputSignal-v00-04-00/_301490/hist-tree.root --m100 OutputSignal-v00-04-00/_301495/hist-tree.root --out TTBarPlots

py XhhCommon/plotting/plotMDCVars.py  -d OutputData-v00-04-01/hist-tree.root --m500 OutputSignal-v00-04-00/_301490/hist-tree.root --m1000 OutputSignal-v00-04-00/_301495/hist-tree.root --m120 OutputSignal-v00-04-00/_301497/hist-tree.root --out MDCPlots


py XhhCommon/plotting/plotResolved.py --plotter interactive -c XhhCommon/plotting/plotIConfig.py --out resolvedPlots-NoReweight-v00-04-01/ --inputDir OutputData-v00-04-01/

py XhhCommon/plotting/plotResolved.py --plotter interactive -c XhhCommon/plotting/plotIConfig.py --out resolvedPlots-Reweight-v00-04-01/ --inputDir OutputData-reweight-v00-04-01/

py XhhCommon/plotting/plotSRVars.py --sig OutputSignal-v00-04-00/  --out SRPlots

py XhhCommon/plotting/plotXhhVars.py   -t OutputTTbar-v00-04-01/hist-tree.root --m500 OutputSignal-v00-04-00/_301490/hist-tree.root --m1000 OutputSignal-v00-04-00/_301495/hist-tree.root --m120 OutputSignal-v00-04-00/_301497/hist-tree.root --out XhhPlots

py XhhCommon/plotting/makeCutFlows.py  -d OutputData-v00-04-01/hist-tree.root  -t OutputTTbar-v00-04-01/hist-tree.root --m500 OutputSignal-v00-04-00/_301490/hist-tree.root --m1000 OutputSignal-v00-04-00/_301495/hist-tree.root --m120 OutputSignal-v00-04-00/_301497/hist-tree.root --out CutFlows

py XhhCommon/plotting/plotSidebandCR.py   -d OutputData-v00-04-01/hist-tree.root --out SBCRPlots
py XhhCommon/plotting/plotReversedTTBar.py -d OutputData-reweight-v00-04-01/hist-tree.root --out reversedTTBarVeto

py XhhCommon/plotting/compTTBarMC.py OutputTTbar-v00-04-02/hist-tree.root TestTTBarStudy/hist-MiniNTuple.root --model BasicComp --out TTBarMC_SLCRvsSR

py XhhCommon/plotting/ttbarCR_MCClosure.py --had OutputTTbar-v00-04-02/hist-tree.root  --lep TestTTBarStudy/hist-MiniNTuple.root --out ttbarCR_MCClosure.root

py XhhCommon/plotting/plotMCClosure.py ttbarCR_MCClosure.root --out ttbarCR_MCClosure


py XhhCommon/plotting/plotTTBar2TagVs4Tag.py OutputTTbar-v00-04-02/hist-tree.root  --out TTBar2TagVs4Tag
