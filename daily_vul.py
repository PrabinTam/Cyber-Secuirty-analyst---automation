#!/usr/bin/env python3

import re
import csv
import json
import nmap
import subprocess as cmd

#The purpose of this script is to compare the vulnerabilites foudn on Tenabe and compare it with sophos list
# And if the IP match on the sophos and tenable then it will tell us who the owner of the PC for remediation process.
# Also, despite if there was a match of sophos or not, the IP found on the vulnerable list will run on Nmap to find open ports
# And hopefully get the hostname and other informaiton regarding that IP.

# fucntion that will open json file and runs the nmap as well!!
def nmaps(ip, outfile, vul_name, computer_name=None, os=None, user=None, location="Tenable"):
    # Initialize the port scanner
    nmScan = nmap.PortScanner()
    # open the file for json
    with open(outfile) as output_file:
        json_format = json.load(output_file)

    # checks if the Ip is already in the file if it is not then add the followinf information.
    ip_in_file = True
    if ip not in json_format['ipaddress']:
        ip_in_file = False
        json_format['ipaddress'].update({ip:[{'location':location}]})
        json_format['ipaddress'][ip][0].update({'ComputerName':computer_name})
        json_format['ipaddress'][ip][0].update({'OS':os})
        json_format['ipaddress'][ip][0].update({'user':user})
        json_format['ipaddress'][ip][0].update({'Vulnerability':{}})
    
    #checks if the vuln is already there for that specific IP. If not then adds.
    vuls = False
    for i in json_format['ipaddress'][ip][0]['Vulnerability']:
        if vul_name ==i:
            vuls = True
            break
    if vuls == False:
        json_format['ipaddress'][ip][0]['Vulnerability'].update({str(len(json_format['ipaddress'][ip][0]['Vulnerability'])+1): vul_name})

    # If the Ip is already on the file then no need to do nmap again. 
    if ip_in_file == False:
        print('runnign syn scan')
        nmScan.scan(ip,'20-500','-Pn -sS --host-timeout 30')
        print('Done syn Scan' + '\n')
        for host in nmScan.all_hosts():
            json_format['ipaddress'][host][0].update({'hostname':nmScan[host].hostname()})
            for proto in nmScan[host].all_protocols():
                json_format['ipaddress'][ip][0].update({proto:{}})
                lport = nmScan[host][proto].keys()
                json_format['ipaddress'][ip][0][proto].update({'port': {}})
                for port in lport:
                    json_format['ipaddress'][ip][0][proto]['port'].update({port:{}})
                    state =  nmScan[host][proto][port]['state']
                    json_format['ipaddress'][ip][0][proto]['port'][port].update({'state':state})

                    service_name = nmScan[host][proto][port]['name']
                    json_format['ipaddress'][ip][0][proto]['port'][port].update({'service':service_name})
                    print("Version Detection started")
                    temp = cmd.run(['nmap','-sV','-Pn', '-p' ,str(port), ip, '--host-timeout', '20'], capture_output=True)
                    print("Version Detection Done")
                    output = str(temp.stdout.decode())
               # string = ''
                    #string = output.replace('\\n', ' ')
                   # string = output.replace('https:','noneed')
               #     ##Trying to get the version name only.
                    version = re.findall(r"open ([\w/ .-]*)", output)
                    if len(version) > 0:
                        version= version[0]
                    else:
                        version=None
               #     #version = string[string.index(index_left)+len(index_left):string.index(index_right)]
               #     #port = int(port)
                    json_format['ipaddress'][ip][0][proto]['port'][port].update({'version':version})
    #write on the file and close it.
    with open(outfile, 'w') as f:
            json.dump(json_format, f, indent=4)
    f.close()



# Goes through the Sophos file and if IP match from vulnerability list to Sophos then 
# returns the OS, COmputerName, and user of that pc. 
def sophos(ip, sophos_file, vul_name = None):
    with open(sophos_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["IPv4 Addresses"] == ip:
                location = "In Sophos"
                return row["Computer Name"], row["Operating System"], row["Last User"], location
            return False 


def main():
    string = '{"ipaddress":{}}'
# getting the current date from the bash shell for the name of the file
    outfile = cmd.run(["date","+%y-%m-%d"], capture_output=True)
    outfile = outfile.stdout.decode().strip()
    outfile = outfile+".json"
# writing the initial string to file to prepare for the json format
    with open(outfile, "w") as f:
        f.write(string)

    sophos_file = "devices.csv"
# Going through the vulnerability file that we got form get_vuln_list.py
    with open("current_vul.csv") as f:
        vul = csv.DictReader(f)
        for row in vul:
            vul_name = row['Plugin Name']
            vul_ip = row['IP Address']
            sophos_values = sophos(vul_ip, sophos_file, vul_name)
#if the ip was not in sophos
            if sophos_values != False:
                nmaps(vul_ip, outfile, vul_name, sophos_values[0], sophos_values[1], sophos_values[2], location)
            else:
                nmaps(vul_ip, outfile, vul_name)

		
if __name__== '__main__':
    main()
