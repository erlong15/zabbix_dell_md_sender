#!/usr/bin/env python3
import pandas as pd
import json
from ZabbixSender import ZabbixPacket, ZabbixSender
import os
import sys, subprocess

zabbix_server = ZabbixSender(<zabbix server>, 10051)
storage_host = sys.argv[1]
zabbix_host = sys.argv[2]
file_stat = "/tmp/" + zabbix_host + "-" + storage_host + ".stat"

subprocess.run(['/usr/lib/zabbix/externalscripts/SMcli', storage_host, 
'-S', '-quick', '-c', 'save storageArray performanceStats file="' + file_stat + '";'], 
stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

df = pd.read_csv(file_stat, skiprows=3)
lld_data = {'data': []}
packet = ZabbixPacket()

for index, dev in df[ ~df['Objects'].str.contains('Expansion Enclosure')][2:].iterrows():
    device=dev['Objects']
    lld_data['data'].append({'{#MDDEV}': device})

    map_metrics = {'Current IOs/sec':'dell.md.currios[' + device + ']','Current IO Latency':'dell.md.curriol[' + device + ']',
    'Current MBs/sec':'dell.md.currmbs[' + device + ']','Primary Write Cache Hit %':'dell.md.writecashhit[' + device + ']',
    'Read %':'dell.md.readprc[' + device + ']','Primary Read Cache Hit %':'dell.md.readcashhit[' + device + ']',
    'Total IOs':'dell.md.totalio[' + device + ']'}

    dev=dev=dev.filter([*map_metrics])
    # Delete empty metrics, value is -
    dev=dev[dev!='-']
    dev=dev.rename(map_metrics)
    for metric,value in dev.items():
        packet.add(zabbix_host, metric, value)

packet.add(zabbix_host, 'dell.md.devices', json.dumps(lld_data))
zabbix_server.send(packet)
os.remove(file_stat)
# Print zabbix server status
print(json.dumps(zabbix_server.status, sort_keys=True))
