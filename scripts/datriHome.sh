#!/bin/bash

if [ ${#} != 2 ]; then
    echo "usage: ${0} LOCALGROUPDISK DS"
    echo " eg: MWT2_UC_LOCALGROUPDISK"
    exit -1
fi

DISK=${1}
DS=${2}

rucio list-dids ${DS}_MiniNTuple.root/
for i in $(rucio list-dids ${DS}_MiniNTuple.root/ --short | sort)
do
    rucio add-rule ${i} 1 ${DISK} --comment fax --activity "User Subscriptions"
done
