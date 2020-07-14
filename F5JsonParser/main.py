#is using python2.6 without any extra packages
import pprint
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
    #remove duplicates needs to be done better but works for now
    hostsRequiredNoDuplicates = []
    for i in range(len(hostsRequired)):
        if hostsRequired[i] not in hostsRequired[i + 1:]:
            hostsRequiredNoDuplicates.append(hostsRequired[i])

    return hostsRequiredNoDuplicates


def get_data(hosts):
    #carry out api checks against filtered host
    requestedOutput = []
    outputSelectors = raw_input('Please enter a value that should be recorded on the API')
    #try split using space as delimiter to get two vals for col and val. If split cant be done assumed user entered done or any
    try:
        outputSelectors.split()
    except:
        hostfilterVal = None
    path = raw_input('Please enter the api path:\n/mgmt/tm/')

    for host in hosts:
        url = 'https://'+(host['hostIP'])+'/mgmt/tm/'+path
        auth = HTTPBasicAuth(user,password)
        r = requests.get(url, verify=False, auth=auth)
        data = json.loads(r.text)
        #this is broken and needs fixed
        for item in data['items']:
            outputItem = host['hostname'],host['hostIP']
                for selector in outputSelectors:
                    outputItem + item[selector]
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
myData = get_data(hosts)
pprint.pprint(myData)
write_data_to_csv(myData)