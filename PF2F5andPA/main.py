import csv
import pprint

def parse_csv(file):
    #parse CSV into understandable components
    rules = []

    #open hosts file and read headers
    with open(file, 'rt') as file:
        rows = csv.reader(file)
        headers = next(rows)
        for row in rows:
            rules.append(row)
    return rules

def F5_output(rules):
    outputCommands = []
    outputCommands.append('create security firewall rule-list <rule-list> <rule-list>')
    outputCommands.append('modify security firewall policy <Policy> rules add { <rule-list> { rule-list <rule-list> place-after last } <rule-list> { rule-list <rule-list> place-after last } }')
    for item in rules: 
        outputCommands.append('modify security firewall rule-list <rule-list> rules add { <rule name> { action accept-decisively ip-protocol '+item[2]+' description \'CHANGE NUMBER\' log yes source { addresses add { '+item[0]+'} VLANs add { <VLAN> } } destination { addresses add { '+item[1]+' } ports add { '+item[3]+' } } place-after last } }')
    return outputCommands

#def PA_Output(input):
#    for item in input:

def writeToTxt(commands,device):
    #write data out to csv file
    with open( device+' commands.txt','w') as out:
        for command in commands:
            out.write(command+'\n')

file = 'ExampleInput.csv'
output = parse_csv(file)
writeToTxt(F5_output(output),'f5')
#writeToTxt(PA_Output(output)))