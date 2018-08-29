import schedule
import sys
import convert
from xml.dom import minidom
import dboec
import sys 
import pickle
import requests
import merge
import git
import csv
import smtplib
import time
import datetime
import gzip
import os

def update():
    #OEC
    print("Updating OEC database.............\n")
    # do a git pull to update OEC
    try:
        cloned_repo = git.Repo("open_exoplanet_catalogue")
        cloned_repo.git.checkout('master')
        cloned_repo.git.pull()
    except git.exc.GitCommandError:
        print "The repo 'open_exoplanet_catalogue' does not exist for updating."
    root_dir = os.getcwd()
    root_dir = root_dir + "/" + "open_exoplanet_catalogue" + "/" + "systems"
    oec_database = dboec.Database()
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            data_one_system = minidom.parse(root + "/" + name)
            one_system_dict = convert.getOEC(data_one_system)
            oec_database.update_xml(one_system_dict)            
    local_oec = open("local_oec_init", "wb")
    pickle.dump(oec_database, local_oec)
    local_oec.close()     
    
    
    #EU database
    print("Updating .eu database..............\n")
    url_eu = "http://exoplanet.eu/catalog/csv"
    list_eu = []
    with requests.Session() as s:
        download = s.get(url_eu)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            list_eu.append(row)
    eu_data = convert.getEU(list_eu)                
    eu_database = dboec.Database()
    eu_database.update_csv(eu_data, dboec.attr_eu)          
    local_eu = open("local_eu","wb")
    pickle.dump(eu_database, local_eu)
    local_eu.close()
    
    #NASA database
    print("Updating NASA database..............\n")
    url_nasa = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=exoplanets&select=*"
    list_nasa = []
    with requests.Session() as s:
        download = s.get(url_nasa)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            list_nasa.append(row)
    nasa_data = convert.getNASA(list_nasa)
    nasa_database = dboec.Database()
    nasa_database.update_csv(nasa_data, dboec.attr_nasa)
    local_nasa = open("local_nasa","wb")
    pickle.dump(nasa_database, local_nasa)
    local_nasa.close()
    print("Updating finished.")
schedule.every().day.do(update)

while True:
    schedule.run_pending()
    time.sleep(1)
