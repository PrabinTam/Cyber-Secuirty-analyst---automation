#!/bin/bash

# The purpose of this script is so that once we run this, it will run all the other script which will do one of our
# daily jobs for us.

# if sophos list of computers [devices.csv] not here then gets it by running get_sophos_list.py
while [ ! -f ./devices.csv ]; do
    if test -e ./get_sophos_list.py; then
        echo getting sophos
        ./get_sophos_list.py
        else
            echo get_sophos not here
            exit 1
    fi
    sleep 60
done

# deleting the old vul list
if test -e ./vulns_old.csv; then
    rm vulns_old.csv
fi

# if vulns list is here then renames it to old vuls.
# if old vuln list is here then removes it
if test -e ./vulns.csv; then
    echo renaming vul
    mv vulns.csv vulns_old.csv
    else 
        ./get_vuln_list.py
    fi
ls -l

# getting the new vul list
if test -e ./vulns.csv; then 
    :
    else
        echo gettting new vul list
        ./get_vuln_list.py
        sleep 15
fi

# comparing the vul list
if test -e ./vul_compare.py; then
    echo comparing vul
    ./vul_compare.py
    else
        echo vul_compare not here
        exit 1
    fi

# checks the line of the new vul list
# if line is greater than 1 then runs the daily.py
# if the line is less than 1 then removes the file

if test -e ./current_vul.csv; then
    line=$(wc -l ./current_vul.csv | cut -d' ' -f1)
    if [ $line -le 1 ]; then
        echo There was no new vulnerability
        rm current_vul.csv
        else
        if test -e ./daily_vul.py; then
            echo New vul so running the scan on this new vul.
            ./daily_vul.py
            else
                echo dail_vul not here
                exit 1
                fi

    fi
fi

# remove the old vul list again for the next day
echo removing oldvul list
rm vulns_old.csv

date=$(date '+%y-%m-%d').json
if test -e ./$date; then
    line=$(wc -l ./$date | cut -d' ' -f1)
    if [ $line -le 1 ]; then
        rm $date
    fi
fi
