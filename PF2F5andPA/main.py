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

def PA_Output(rules):
    outputCommands = []
    for item in rules:
        outputCommands.append('set  rulebase security rules <rule name> profile-setting profiles virus default')
        outputCommands.append('set  rulebase security rules <rule name> profile-setting profiles spyware default')
        outputCommands.append('set  rulebase security rules <rule name> profile-setting profiles vulnerability default')
        outputCommands.append('set  rulebase security rules <rule name> profile-setting profiles wildfire-analysis default')
        outputCommands.append('set  rulebase security rules <rule name> to «DEST_ZONE»')
        outputCommands.append('set  rulebase security rules <rule name> from «SRC_ZONE»')
        outputCommands.append('set  rulebase security rules <rule name> source “[+item[0]+]”')
        outputCommands.append('set  rulebase security rules <rule name> destination “[+item[1]+]”')
        outputCommands.append('set  rulebase security rules <rule name> source-user any')
        outputCommands.append('set  rulebase security rules <rule name> category any')
        outputCommands.append('set  rulebase security rules <rule name> application any')
        outputCommands.append('set  rulebase security rules <rule name> service “service”')
        outputCommands.append('set  rulebase security rules <rule name> hip-profiles any')
        outputCommands.append('set  rulebase security rules <rule name> action allow')
        outputCommands.append('set  rulebase security rules <rule name> disabled no')


def writeToTxt(commands,device):
    #write data out to csv file
    with open( device+' commands.txt','w') as out:
        for command in commands:
            out.write(command+'\n')

file = 'ExampleInput.csv'
output = parse_csv(file)
writeToTxt(F5_output(output),'f5')
writeToTxt(PA_Output(output)))
