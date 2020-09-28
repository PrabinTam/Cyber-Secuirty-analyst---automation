#!/usr/bin/env python3
import csv

# opens tenable old vulns and and newly downloaded vulns
with open('vulns.csv', 'r') as f, open('vulns_old.csv','r') as f2:
    file1 = f.readlines()
    file2 = f2.readlines()

# Compares two vulns and if the new vulns were not in the old vulns list then it will write it to a new file
# to be a port scan.
with open('current_vul.csv', 'w') as outfile:
    outfile.write(file1[0])
    for line in file1:
        if line not in file2:
            outfile.write(line)
