import sys
import convert
from xml.dom import minidom
import dboec
import sys
import pickle
import requests
import merge
import push_to_git
import csv
import smtplib
import time
import get_xml
import gzip
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header
from subprocess import Popen


if len(sys.argv) == 1:
    g = push_to_git.configuration()
    push_to_git.clone_repo(g)
    print("Initiating OEC database, Please wait.............\n")
    root_dir1 = os.getcwd()
    root_dir = root_dir1 + "/" + g.name + "/" + "systems"
    oec_database = dboec.Database()
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            data_one_system = minidom.parse(root + "/" + name)
            one_system_dict = convert.getOEC(data_one_system)
            oec_database.update_xml(one_system_dict)
    local_oec = open("local_oec_init", "wb")
    pickle.dump(oec_database, local_oec)
    local_oec.close()
    print("Initialize finished.")
    print("Welcome! Here you find a software to update open_exoplanet_catalogue.\n")
    print("For more information type '\help' to start!\n")
    while 1:
        user_input = sys.stdin.readline()
        if (user_input == r"\help" + "\n"):
            print("********************** User Guide ************************")
            print("\n")
            print("\help ---------------------- Open the User Guide.")
            print("\n")
            print(r'\update' + " -------------------- Update the databases.")
            print("\n")
            print("\merge ------------------- Merge all databases.")
            print("\n")
            print("\push ---------------------- Commit and push the change \
to Git repository, requires user's information.")
            print("\n")
            print(r"\autostart ---------------------- Turn on auto update.")
            print("\n")
            print(r"\autostop ---------------------- Turn off auto update.")
            print("\n")
            print("\send ---------------------- Send email notification.")
            print("\n")
            print("\exit ---------------------- Shut down our programme.")
            print("\n")
            print("**********************************************************")

        elif (user_input == r"\update" + "\n"):
            # OEC database
            print("Updating OEC database.............\n")
            push_to_git.pull_repo(g)
            root_dir1 = os.getcwd()
            root_dir = root_dir1 + "/" + g.name + "/" + "systems"
            oec_database2 = dboec.Database()
            for root, dirs, files in os.walk(root_dir):
                for name in files:
                    data_one_system = minidom.parse(root + "/" + name)
                    one_system_dict = convert.getOEC(data_one_system)
                    oec_database2.update_xml(one_system_dict)
            local_oec = open("local_oec_init", "wb")
            pickle.dump(oec_database2, local_oec)
            local_oec.close()

            # EU database
            print("Updating EU database.............\n")
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
            local_eu = open("local_eu", "wb")
            pickle.dump(eu_database, local_eu)
            local_eu.close()

            # NASA database
            print("Updating NASA database.............\n")
            url_nasa1 = "http://exoplanetarchive.ipac.caltech.edu/cgi-bin/"
            url_nasa2 = "nstedAPI/nph-nstedAPI?table=exoplanets&select=*"
            url_nasa = url_nasa1 + url_nasa2
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
            local_nasa = open("local_nasa", "wb")
            pickle.dump(nasa_database, local_nasa)
            local_nasa.close()

            print("Update finished.")

        elif (user_input == r"\merge" + "\n"):  # merge 3 databases
            local_nasa = open("local_nasa", "rb")
            local_eu = open("local_eu", "rb")
            local_oec = open("local_oec_init", "rb")

            nasa_database = pickle.load(local_nasa)
            eu_database = pickle.load(local_eu)
            oec_database = pickle.load(local_oec)

            local_nasa.close()
            local_eu.close()
            local_oec.close()

            print("Merging EU to OEC...............\n")

            database_merge1 = merge.merge(eu_database, oec_database)

            print("Merging NASA to OEC...............\n")

            database_merge2 = merge.merge(nasa_database, database_merge1)

            local_new = open("local_new", "wb")
            pickle.dump(database_merge2, local_new)
            local_new.close()

            print("Merging finished.")

        elif (user_input == r"\push" + "\n"):  # push xmls to git
            local_oec = open("local_oec_init", "rb")
            origin_db = pickle.load(local_oec)
            local_oec.close()
            local_new = open("local_new", "rb")
            merged_db = pickle.load(local_new)
            local_new.close()
            push_to_git.push_to_git(g, origin_db, merged_db)

        elif (user_input == r"\send" + "\n"):  # send email notification
            print("Please enter your email:")
            target = sys.stdin.readline()
            resource1 = r"http://exoplanet.eu/catalog/"
            resource2 = r"http://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=planets"
            update_msg = "There are new updates on open_exoplanet_catalogue, please go and check the pull request.\n"
            content = update_msg + "resources:\n" + resource1 + "\n" + resource2
            msg = MIMEText(content, "plain", "utf-8")
            msg["Subject"] = Header("Pull requests notifiction")
            msg["From"] = Header("tmntcscc01@gmail.com")
            msg["To"] = Header(target)

            mailhost = "smtp.gmail.com"
            usermail = "tmntcscc01@gmail.com"
            password = "Ilovecscc01"

            try:
                server = smtplib.SMTP("smtp.gmail.com:587", timeout=30)
                server.ehlo()
                server.starttls()
                server.login(usermail, password)
                server.sendmail(usermail, [target],
                                msg.as_string())
                server.quit()
                print("Email successfully sent!")
            except Exception as e:
                print(str(e))

        elif (user_input == r"\add" + "\n"):  # add planet feature
            print("Please type in full file path that you want to add:")
            file_path = sys.stdin.readline()  # sgl for single xml file
            file_path = file_path.strip("\n")
            data_sgl = minidom.parse(file_path)
            sgl_dict = convert.getOEC(data_sgl)
            sgl_database = dboec.Database()
            sgl_database.update_xml(sgl_dict)
            local_new = open("local_new", "rb")
            database_merge2 = pickle.load(local_new)
            local_new.close()
            database_merge3 = merge.merge(sgl_database, database_merge2)
            local_new = open("local_new", "wb")
            pickle.dump(database_merge3, local_new)
            local_new.close()
            print("Adding finished.")

        elif (user_input == r"\autostart" + "\n"):
            sub = Popen([sys.executable, "update.py"])
            print("Auto update started.")
            
        elif (user_input == r"\autostop" + "\n"):
            sub.kill()
            print("Auto update stopped")

        elif (user_input == r"\exit" + "\n"):
            sys.exit()

        else:
            print("Sorry, we cannot recognize your command. Please try again.")
