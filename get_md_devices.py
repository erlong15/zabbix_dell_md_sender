#!/usr/bin/python3.6
import pandas as pd
import json
from ZabbixSender import ZabbixPacket, ZabbixSender
import os
import sys

storageName = sys.argv[1]
zbxName = sys.argv[2]
mdName = sys.argv[3]

os.system('SMcli -n {} -S -quick -c "save storageArray performanceStats file=\\"/var/log/{}.stat\\";"'.format(storageName, mdName))

file_stat = '/var/log/{}.stat'.format(mdName)
df = pd.read_csv(file_stat, skiprows=3)
lld_data = {'data': []}
for dev in df[ ~df['Objects'].str.contains('Expansion Enclosure')]['Objects'][2:].tolist():
    lld_data['data'].append({'{#MDDEV}': dev})

packet = ZabbixPacket()
packet.add(zbxName, 'dell.md.devices', json.dumps(lld_data))
for ind, dev in df[ ~df['Objects'].str.contains('Expansion Enclosure')][2:].iterrows():
    packet.add(zbxName, 'dell.md.currios[{}]'.format(dev['Objects']), dev['Current IOs/sec'])
    packet.add(zbxName, 'dell.md.curriol[{}]'.format(dev['Objects']), dev['Current IO Latency'])
    packet.add(zbxName, 'dell.md.currmbs[{}]'.format(dev['Objects']), dev['Current MBs/sec'])
    packet.add(zbxName, 'dell.md.writecashhit[{}]'.format(dev['Objects']), dev['Primary Write Cache Hit %'])
    packet.add(zbxName, 'dell.md.readprc[{}]'.format(dev['Objects']), dev['Read %'])
    packet.add(zbxName, 'dell.md.readcashhit[{}]'.format(dev['Objects']), dev['Primary Read Cache Hit %'])
    packet.add(zbxName, 'dell.md.totalio[{}]'.format(dev['Objects']), dev['Total IOs'])


result = ZabbixSender().send(packet)
print(result)

