import optparse
parser = optparse.OptionParser()
parser.add_option('-i', '--input',           dest="inFileName",         default="", help="Input file name")
parser.add_option('-p', '--disPos',          dest="disPos",             default=1, help="Input file name")
o, a = parser.parse_args()

inFile = open(o.inFileName, "r")

dsidsDict = {}

for rawline in inFile: 
    ds = rawline.rstrip()
    words = ds.split(".")
    dsid = words[int(o.disPos)]

    if int(dsid) in dsidsDict:
        print "Have Duplicate",dsid
    dsidsDict[int(dsid)] = ds


keys = dsidsDict.keys()
keys.sort()

for k in keys:
    print dsidsDict[k]
