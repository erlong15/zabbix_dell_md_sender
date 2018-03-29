# Python script to send DELL MD counter into zabbix

The script runs SMcli and gets Storage PerformanceStats, parses and sends to Zabbix server
The script is working under pytthon 3.6

# How to run
```bash
pip3.6 install -r requirements.txt

python3.6 get_md_devices.py <StorageName> <HostZabbixName> <stat.log>
```


# Links
[ Russian description ]( https://otus.ru/nest/post/13/ )

