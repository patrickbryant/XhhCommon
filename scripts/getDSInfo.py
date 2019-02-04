import optparse
parser = optparse.OptionParser()
parser.add_option('-i', '--inFile',   dest="inFileName",         default="", help="Input txt file with DS")
o, a = parser.parse_args()

try:
    import pyAMI.client
except:
    print "Failed to load pyAMI.client, setting up local PyAMI"
    print " > localSetupPyAMI "
    #import os
    #os.system("localSetupPyAMI")
    #import pyAMI.client

import pyAMI.atlas.api as AtlasAPI

client = pyAMI.client.Client('atlas')
AtlasAPI.init()



inputDS = []
#"XhhCommon/scripts/grid_samples_EXOT8_test.txt"
inputFile = open(o.inFileName,"r")

for line in inputFile:
    if line.startswith("#"): continue
    words = line.split()
    if not len(words): continue
    
    dsName = words[0].rstrip("/")
    dsID = dsName.split(".")[1]
    print dsName

    dsProv = AtlasAPI.get_dataset_prov(client,dataset=dsName)
    for prov in dsProv["node"]:
        if prov['dataType'] == "EVNT":
            thisProvDSName = prov['logicalDatasetName']
            thisProvDSID   = thisProvDSName.split(".")[1]
            if thisProvDSID == dsID:
                print "\tUsing ",thisProvDSName
                inputDS.append(thisProvDSName)

def getUnitSF(unit):
    if unit == "nano barn":
        return 1000
    print "Unknown unit..."
    return 1.0


for ds in inputDS:
    dsList = AtlasAPI.get_dataset_info(client,dataset=ds)
    dsInfo = dsList[0]
    #print dsInfo['logicalDatasetName']
    #print "\tcross section",dsInfo["crossSection_mean"]
    #print "\tfilter Eff.",dsInfo["GenFiltEff_mean"]
    unit = dsInfo['crossSection_unit']
    getSF = getUnitSF(unit)
    #print dsInfo
    print dsInfo['datasetNumber']," ",dsInfo['physicsShort']," ",float(dsInfo["crossSection_mean"])*getSF," 1.  ",float(dsInfo["GenFiltEff_mean"])," 1."#,dsInfo['totalEvents']


