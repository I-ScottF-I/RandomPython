#is using python2.6 without any extra packages
import sys
import csv
import json
import requests
from requests.auth import HTTPBasicAuth

def get_hosts(file):
    #convert host file into list of dicts
    hostsRequired = []
    hostFilterCol = None

    #open hosts file and read headers
    with open(file, 'rt') as hostsFile:
        rows = csv.reader(hostsFile)
        headers = next(rows)

        #loop for new hostfile filters until user enters command 'done'
        while not hostFilterCol == 'done':
            hostFilterCol = raw_input('Please enter a filter column and a value to filter that column with:\n- If filtering is done enter done\n- If no filtering is required then enter any\n')

            #try split using space as delimiter to get two vals for col and val. If split cant be done assumed user entered done or any
            try:
                hostFilterCol,hostFilterVal=hostFilterCol.split()
            except:
                hostfilterVal = None
            if hostFilterCol == 'done':
                print('time to get data')
            elif hostFilterCol == 'any':
                for row in rows:
                    d = dict(zip(headers,row))
                    hostsRequired.append(d)
            else:
                for row in rows:
                    d = dict(zip(headers,row))
                    if hostFilterVal in (d[hostFilterCol]):
                        hostsRequired.append(d)
    #remove duplicates needs to be done
    return hostsRequired

def get_data(hosts):
    #carry out api checks against filtered host
    requestedOutput = []
    for host in hosts:
        url = 'https://'+(host['hostIP'])+'/mgmt/tm/net/self'
        auth = HTTPBasicAuth(user,password)
        r = requests.get(url, verify=False, auth=auth)
        data = json.loads(r.text)
        for item in data['items']:
            outputItem = host['hostname'],host['hostIP'],str(item['name']),str(item['allowService'])
            requestedOutput.append(outputItem)
    return requestedOutput

def write_data_to_csv(output):
    #write data out to csv file
    with open('/var/tmp/output.csv','wt') as out:
        write = csv.writer(out)
        write.writerows(output)

user = raw_input('Enter Username: ')
password = raw_input('Enter Password: ')
hosts = get_hosts('/var/tmp/hostfile.csv')
print(get_data(hosts))
write_data_to_csv(get_data(hosts))
