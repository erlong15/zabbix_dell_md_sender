#!/usr/bin/python3.6
import pandas as pd
import json
from ZabbixSender import ZabbixPacket, ZabbixSender
import os
import sys


storageName = sys.argv[1]
statFile = '/var/log/md3620.stat'

os.system('SMcli -n {} -S -quick -c "save storageArray performanceStats file=\\"{}\\";"'.format(storageName, statFile))

file_stat = '/var/log/md3620.stat'
df = pd.read_csv(file_stat, skiprows=3)
lld_data = {'data': []}
for dev in df[ ~df['Objects'].str.contains('Expansion Enclosure')]['Objects'][2:].tolist():
    lld_data['data'].append({'{#MDDEV}': dev})

packet = ZabbixPacket()
packet.add(storageName, 'dell.md.devices', json.dumps(lld_data))
for ind, dev in df[ ~df['Objects'].str.contains('Expansion Enclosure')][2:].iterrows():
    packet.add(storageName, 'dell.md.currios[{}]'.format(dev['Objects']), dev['Current IOs/sec'])
    packet.add(storageName, 'dell.md.curriol[{}]'.format(dev['Objects']), dev['Current IO Latency'])
    packet.add(storageName, 'dell.md.currmbs[{}]'.format(dev['Objects']), dev['Current MBs/sec'])
    packet.add(storageName, 'dell.md.writecashhit[{}]'.format(dev['Objects']), dev['Primary Write Cache Hit %'])
    packet.add(storageName, 'dell.md.readprc[{}]'.format(dev['Objects']), dev['Read %'])
    packet.add(storageName, 'dell.md.readcashhit[{}]'.format(dev['Objects']), dev['Primary Read Cache Hit %'])
    packet.add(storageName, 'dell.md.totalio[{}]'.format(dev['Objects']), dev['Total IOs'])


result = ZabbixSender().send(packet)
print(result)

