# IT-security-automation

Programs used:

    Python3
    Bash

Python Packages used:
    
    Nmap3
    Selenium
    csv
    

    The goal these scripts was to automate one our daily task for Security Analyist - Apprenticeship. 
    The daily task is to go through the daily vulnerabilty found on Tenable, but it only gives IP and hostname of the machine associated with the vulneerabilty with no user. 
    But we need to know the user of the maachine to remediation process. Hence, I go to Sophos concolse to find the the same IP and get the user of the machine to follow up and remediate the vulnerability. 
    However, I thought I could automate this same process of getting the list of the vulnerabilty and getting the user of the machine.

Pr-running the Script what is needed:
    
    We need to run get_tenable_vuln.py only once ever in the machine and that no need to ever.
    Python3 needs to be installed.
    We are using Selenium to crawl the website so need a proper browser driver for it. And for our case, we are using Chrome. 
    

What each script does:

    get_sophos_list.py >> The purpose of this scirpt is to go to the Sophos Console and then to get all the devices in a CSV format.
    
    get_tenable_vuln_list.py >> The purpose of this script is to get the daily vulnerability found on Tenable in a CSV format.
    
    vuln_compare.py >> This script will compaare the previous day's vuln's list with Today's vuln's list and only if there was a new vuln list it will write it out in a file. 
    
    daily_vul.py >> This script go through both file from Tenable and Sophos and if the IP address from Tenable's Vulnerabiliy matches with the Sophos, it will get us the username of the machine. On top of that, regaardless of whether the user was found or not, it will scan that IP with Nmap Scanner and get us more detail about the machine so that we can use it for remediation process.
    
    script.sh >> This Script will take all the above script and runs it all at once instead of you haaving to run every single one, without worrying about which one should be run first or which should I run next.
    
    Chrome_update.sh >> This script will update the driver of Chrome if the current driver is corrupted or if a new version of Chrome is out. But this script is not included with script.sh, which means this needs to be run individually. 
  
