#!/bin/bash
set -e

#Clean and prepare
d="/root/reporting/results"
s="/root/reporting/scripts"
mkdir -p $d
rm -rf $d/*.txt $d/*.csv
rm -rf $d/index.html

#Update ldap informations
/root/ics/reporting/ldap.sh &>/dev/null

#Create files binding users and labs
python $s/01_get_users_labs.py -affectations $d/users_affectations.txt -labos $d/labos_names.txt

#Update users lab in the sql database
python $s/02_update_users_labs_in_database.py -affectations $d/users_affectations.txt

#Compute statistics
py="03_get_mesu_stat.py"
python $s/$py -last total -globals -o $d/0_0total.txt
python $s/$py -last year  -globals -o $d/0_1year.txt
python $s/$py -last month -globals -o $d/0_2month.txt
python $s/$py -last week  -globals -o $d/0_3week.txt
python $s/$py -last day   -globals -o $d/0_4day.txt
cat $d/0_* >> $d/globals.txt
rm $d/0_*
mv $d/globals.txt $d/0_globals.txt
#Total statistics
python $s/$py -last total -labos  -o $d/1_total_labos.txt
python $s/$py -last total -users  -o $d/1_total_users.txt
python $s/$py -last total -queues -o $d/1_total_queues.txt
#Year globals
python $s/$py -last year -labos  -o $d/2_year_labos.txt
python $s/$py -last year -users  -o $d/2_year_users.txt
python $s/$py -last year -queues -o $d/2_year_queues.txt
#Month globals
python $s/$py -last month -labos  -o $d/3_month_labos.txt
python $s/$py -last month -users  -o $d/3_month_users.txt
python $s/$py -last month -queues -o $d/3_month_queues.txt
#Day globals
python $s/$py -last week -labos  -o $d/4_week_labos.txt
python $s/$py -last week -users  -o $d/4_week_users.txt
python $s/$py -last week -queues -o $d/4_week_queues.txt

#Creating the csv files used as processing input
python $s/04_create_csv.py -affectations $d/users_affectations.txt -labos $d/labos_names.txt -i $d/1_total_users.txt -o $d/5_total_users.csv
python $s/04_create_csv.py -affectations $d/users_affectations.txt -labos $d/labos_names.txt -i $d/2_year_users.txt  -o $d/5_year_users.csv
python $s/04_create_csv.py -affectations $d/users_affectations.txt -labos $d/labos_names.txt -i $d/3_month_users.txt -o $d/5_month_users.csv
python $s/04_create_csv.py -affectations $d/users_affectations.txt -labos $d/labos_names.txt -i $d/4_week_users.txt  -o $d/5_week_users.csv

#Creating the html file to link and send to the server
python $s/05_create_html_page.py -directory $d
scp $d/index.html $d/*.txt $d/*.csv root@mesu-smn.dsi.upmc.fr:/srv/www/htdocs/data/