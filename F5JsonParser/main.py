#is using python2.6 without any extra packages
import sys
import csv
import json
import unicodedata
import requests
from requests.auth import HTTPBasicAuth

def get_hosts(file):
    #convert host file into list of dicts
    hostsRequired = []
    with open(file, 'rt') as hostsFile:
        rows = csv.reader(hostsFile)
        headers = next(rows)
        for row in rows:
            if (1 == 1): #filtering will come later
                d = dict(zip(headers,row))
                hostsRequired.append(d)
    return hostsRequired

def get_data(hosts):
    #carry out operations against relevant host
    requestedOutput = []
    for host in hosts:
        url = 'https://'+(host['hostIP'])+'/mgmt/tm/net/self'
        auth = HTTPBasicAuth('admin','admin')
        r = requests.get(url, verify=False, auth=auth)
        data = json.loads(r.text)
        for item in data['items']:
            outputItem = host['hostname'],host['hostIP'],str(item['name']),str(item['allowService'])
            requestedOutput.append(outputItem)
    return requestedOutput

def write_data_to_csv(output):
    with open('/var/tmp/output.csv','wt') as out:
        write = csv.writer(out)
        write.writerows(output)

hosts = get_hosts('/var/tmp/hostfile.csv')
print(get_data(hosts))
write_data_to_csv(get_data(hosts))
