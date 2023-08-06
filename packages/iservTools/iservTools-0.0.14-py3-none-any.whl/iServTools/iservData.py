# coding: utf-8
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


import time, datetime


import os, platform
import os.path 
import shutil
import sqlite3, csv
import re



#import iservTools

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Color



class iservObject:
    """Das Objekt enthält Zugangsdaten für iServ, den Ort der Datenablage und den Namen der Datenbank.
    
       - self.iserv_url: die URL des verwendeten Servers
       
       - self.user_name: Name des verwendeten iServ-Benutzers
       - self.password_user: das entsprechende Passwort für das Login
       - self.password_admin: das Administratorenpasswort für den Benutzer
       - self.database: Name der Datenbank
       - self.user_dir: Benutzerverzeichnis im Dokumentenordner **/user/Documents/iservTool**
       - self.data_dir: Datenverzeichnis, zunächst identisch mit **user_dir**
       - self.mail_domain: Mail domain, z.B. @c-a-g.eu
       - self.schoolyear: gibt den Namen des Schuljahres als Text an, z.B. "2020/21"
       - self.abi_jg_12: Jahr des Abiturs für den Jahrgang 12
       - self.abi_jg_13: Jahr des Abiturs für den Jahrgang 13
       - self.end_of_year: das letzte Kalenderjahr des laufenden Schuljahres, wird verwendet, um ein Verfallsdatum für Gruppen festzulegen.
    """
    def __init__(self):
        
        self.OS = platform.platform()
        self.user_dir  = os.path.expanduser('~') + '/Documents/iservAdminData'
        self.set_default_settings()
        
        self.end_of_year = self.get_schoolyear_end()
        self.schoolyear = str(self.end_of_year-1) + "/" + str(self.end_of_year - 2000)
        self.abi_jg_12 = self.end_of_year + 1
        self.abi_jg_13 = self.end_of_year
        self.message = "Schuljahr " +  self.schoolyear
        print(self.schoolyear)
        
        ### Wenn das Benutzerverzeichnis vorhanden ist ....
        if (os.path.isdir(self.user_dir)): 
            
            ### Wenn die ini-Datei vorliegt ...
            if (os.path.isfile(self.user_dir + "/iservTool.ini")):
                ini_file = open(self.user_dir + "/iservTool.ini", "r")
                self.data_dir = ini_file.read()
                self.data_dir = self.data_dir.strip()
                ini_file.close()
                self.message += "Lade Einstellungen aus " + self.user_dir + "...\n"
                
            ### Wenn die ini-Datei noch fehlt ...
            ### =================================
            else:
                self.message += "Datenverzeichnis neu festgelegt: " + self.data_dir
                self.data_dir = self.user_dir
                self.write_ini_file()
                self.set_default_settings()
            
                
        ### Wenn der Ordner user/Documents/iservTool noch nicht besteht ...
        else:
            self.message += "Datenverzeichnis neu festgelegt: " + self.data_dir
            os.mkdir(self.user_dir)
            self.data_dir = self.user_dir
            self.write_ini_file()
        
            
        self.database = self.data_dir + "/iservDatabase.db"
           
        self.create_table("settings")
        self.create_table("Lehrer")
        self.create_table("Klassen")
        self.create_table("Lehrer_in_Klasse")
        
        if (not os.path.isfile(self.data_dir + "/chromedriver")):
            self.message += "\n\nLade den Chromedriver herunter und lege ihn im Verzeichnis " + self.user_dir + " ab.\n"
            self.message += "https://sites.google.com/a/chromium.org/chromedriver/\n"
        else:
            self.message += "\nChromedriver OK.\n"
        
    
        # Load settings
        # ================
        self.iserv_url = self.get_setting("iserv_url")
        self.iserv_user = self.get_setting("iserv_user")
        self.password_user = self.get_setting("password_user")
        self.password_admin = self.get_setting("password_admin")
        self.export_dir = self.get_setting("export_dir")
        self.Kurswahl_id = self.get_setting("Kurswahl_id")
        self.Kurswahl_Angebote = self.get_setting("Kurswahl_Angebote")
        self.set_students_file = self.get_setting("set_students_file")
        if (self.iserv_url != ""):
            data = self.iserv_url.split("/")
            self.mail_domain =  "@" + data[2]
        else:
            self.mail_domain = ""
            
        if (self.Kurswahl_Angebote == ""):
            self.Kurswahl_Angebote = self.data_dir + "/Projektliste.xlsx"
            
    def get_schoolyear_end(self):
        """Ermittelt das letzte Jahr des laufenden Schuljahres
            
           Geht davon aus, dass das Schuljahr offiziell am 1. August beginnt. Wenn der Monat vor dem August liegt wird das aktuelle Jahr als Endjahr des Schuljahres angenommen, anderenfalls das darauffolgende Jahr.
        """
        d = datetime.datetime.now()
        if (d.month < 8):
            y = d.year
        else:
            y = d.year + 1
        return y
     
        
    def create_table(self, Tabelle):
        """Erstellt eine Tabelle, wenn sie nicht schon besteht: 
        
        - settings
        - Lehrer
        - Klassen
        - Lehrer_in_Klasse
        - Gruppenmitglieder
        
        """
        sql = ""

        if (Tabelle == "Lehrer"):
            sql = "Lehrer (Kurz TEXT, Name TEXT, Vorname TEXT, Id TEXT, eMail TEXT)"
            
        if (Tabelle == "Schueler"):
            sql = "Schueler (Name TEXT, Vorname TEXT, Id TEXT, Klasse TEXT, eMail TEXT)"
            
        if (Tabelle == "Klassen"):
            sql = "Klassen (Klasse TEXT, Kurz TEXT, Jahrgang INT)"
            
        if (Tabelle == "Lehrer_in_Klasse"):
            sql = "Lehrer_in_Klasse (Lehrer_kurz TEXT, Klasse TEXT, Fach TEXT, Jahrgang INT)"
            
        if (Tabelle == "Gruppenmitglieder"):
            sql = "Gruppenmitglieder (Id TEXT, Gruppe TEXT)"
            
        if (Tabelle == "settings"):
            sql = "settings (Variable TEXT, Value TEXT)"
        
        
        if (sql != ""):
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS ' + sql)
            c.execute('CREATE TABLE IF NOT EXISTS table_timestamp (Tabelle TEXT, Datum timestamp)')
            c.close
            conn.close

    def move_data_dir_to(self, new_dir):
        """Bewegt die Daten in einen neuen Ordner.
        
           :param new_dir: (str) Name des neuen Datenverzeichnises
        """
     
        shutil.move(self.data_dir, new_dir)
        self.data_dir = new_dir
        self.write_ini_file()
        
        if os.path.isfile(new_dir + "/chromedriver"):
            shutil.move(new_dir + "/chromedriver", self.user_dir + "/chromedriver")    
        
    ### ================== ###
    ### Settings und Login ###
    ### ================== ###
    
    def write_ini_file(self):
        """Schreibt die ini Datei in den Benutzerordner. Darin wird der Datenordner festgelegt"""
        if not os.path.isdir(self.user_dir):
            os.mkdir(self.user_dir)
        ini_file = open(self.user_dir + "/iservTool.ini", "w")
        ini_file.write(self.data_dir)
        ini_file.close()
        
    def set_default_settings(self):
        """Setzt die Settings auf Standardwerte."""
        self.iserv_url = "https://c-a-g.eu/iserv/"
        self.iserv_user = "admin"
        self.password_user = ""
        self.password_admin = self.password_user
        self.data_dir = self.user_dir
        self.export_dir = self.data_dir
        
        
    def get_setting(self, variable):
        """Liest eine Einstellung aus der Datenbank und gibt ggf. einen Standard-Wert zurück.
        
           :param variable: (str) Name der gesuchten Einstellung:
           
           :return:  Wert der gesuchten Einstellung, ggf. wird ein Standardwert ausgegeben.
        """
        if (variable == "data_dir"):
            setting = self.user_dir
        else:
            conn = sqlite3.connect(self.database)
            c = conn.cursor()
    
            c.execute("SELECT value FROM settings WHERE Variable = ?", (variable,))
            Data = c.fetchall()
        
            if Data:
                setting = Data[0][0]
            else:
                setting = ""
                if (variable == "iserv_user"):
                    setting = "admin"
                if (variable == "iserv_url"):
                    setting = "https://c-a-g.eu/iserv/"
                if (variable == "Kurswahl_Angebote"):
                    setting = self.data_dir + "/Projektliste.xlsx"
                if (variable == "Kurswahl_id"):
                    setting = "1"
                if (variable == "set_students_file"):
                    setting = self.data_dir + "/Festlegungen-SuS.xlsx"
            c.close
            conn.close
        
        return setting
        
    
        
    def save_setting(self, variable, value):
        """Speichert eine Voreinstellung
           
           :param variable: (str) Name des zu speichernden Wertes
           :param value: (str) Wert der zu speichernden Variable
           
           
        """
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute("SELECT * FROM settings WHERE Variable = ?", (variable,))
        Data = c.fetchall()    
        if Data:
            c.execute("UPDATE settings SET Value = ? WHERE Variable = ?", (value, variable))
            conn.commit() 
        else:
            c.execute("INSERT INTO settings (Variable, Value) VALUES (?,?)", (variable, value))
            conn.commit()        
        c.close
        conn.close


    def write_iserv_data(self):
        """Speichert alle Parameter in der Datenbank
        
        - iserv_url
        - iserv_user
        - password_user
        - password_admim
        - data_dir
        - export_dir
        """
        self.save_setting("iserv_url", self.iserv_url)
        self.save_setting("iserv_user", self.iserv_user)
        self.save_setting("password_user", self.password_user)
        self.save_setting("password_admin", self.password_admin)
        self.save_setting("iserv_user", self.iserv_user) 
        self.save_setting("data_dir", self.data_dir)
        self.save_setting("export_dir", self.export_dir)
        
    def write_table_timestamp(self, table_name):
        """
        Hält  in der Tabelle *table_timestamp* fest, wann eine Tabelle zuletzt aktualisert wurde:
        
        - Tabelle
        - Datum
        
        :param table_name: (str) Name der Tabelle
        
        
        """
        jetzt = datetime.datetime.now()
        
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
         
        sql = "SELECT * FROM table_timestamp WHERE Tabelle=?"
        c.execute(sql, (table_name,))
        res = c.fetchall()
        
        if (len(res) >0 ):
            sql = "UPDATE table_timestamp SET Datum =? WHERE Tabelle =?"
            c.execute(sql, (jetzt, table_name))
            conn.commit()
        else:
            c.execute("INSERT INTO table_timestamp (Tabelle, Datum) VALUES (?,?)", (table_name, jetzt))
            conn.commit()  
        
        c.close
        conn.close
        
        
    def get_table_timestamp(self, table_name):
        """
        Gibt das Datum der letzten Aktualisierung einer Tabelle zurück.

        :param table_name: (str) Name der Tabelle
        
        """
        
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
         
        sql = "SELECT Datum FROM table_timestamp WHERE Tabelle=?"
        c.execute(sql, (table_name,))
        res = c.fetchall()
        
        if (len(res) >0 ):
            Datum = 0
        else:
            Datum = res[0][0]
        
        c.close
        conn.close 
        
        return Datum
    
    
    def check_table(self, Tabelle):
        """Überprüft, ob eine Datenbanktabelle exisitiert. 
        
        Wenn die Tabelle nicht existiert wird die Mitteilung "Tabelle 'Tabelle' existiert nicht." zurückgegeben, anderenfalls "Tabelle 'Tabelle' - Stand " + das Datum der letzten Änderung.
        
           param Tabelle: (str) Bezeichnung der Datenbanktabelle    
        """
        
        Tabelle_existiert = "\nTabelle '" + Tabelle + "'\n    - exisitert nicht."
        
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
      
        c.execute("SELECT name FROM sqlite_master WHERE name=?", (Tabelle,))
        
        
        if (bool(c.fetchone())):
            
            sql = "SELECT Datum FROM table_timestamp WHERE Tabelle=?"
            c.execute(sql, (Tabelle,))
            res = c.fetchall()
        
            if (len(res) >0 ):
                Tabelle_existiert = "\nTabelle '" + Tabelle + "'\n    - Stand " + self.timestamp_message(res[0][0])
                     
        c.close
        conn.close
        
        return Tabelle_existiert
    
    def timestamp_message(self, stamp):
        """Gibt eine Meldung zur *timestamp* aus."""
        
        date = datetime.datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.datetime.now()
        age = now - date
        date_str =  stamp
        return date_str[:-10]
    
    def login(self):
        """Login auf der iServ-Seite."""
        self.browser = webdriver.Chrome(self.user_dir + '/chromedriver')
      
        login_URL = self.iserv_url + "login"
        self.browser.maximize_window()
     
        self.browser.get(login_URL)
        #self.browser.execute_script("document.body.style.zoom='60%'")
        time.sleep(2)
                                        
        input = self.browser.find_element_by_name("_username")
        input.send_keys(self.iserv_user)

        input = self.browser.find_element_by_name("_password")
        input.send_keys(self.password_user)

        input.submit()

    def logout(self):
        """Beendet die Sitzung und schließt den Browser"""
        self.browser.get(self.iserv_url)
        time.sleep(2)
        print("ready")
        input = self.browser.find_element_by_id("dropdownProfileMenu")
        input.click()
        time.sleep(1)

        input = self.browser.find_element(By.LINK_TEXT, 'Abmelden')
        input.click()

        self.browser.quit()
        
        
    def admin_login(self):
        """Login im Admin-Bereich
           
           Wenn das Admin-Passwort nicht ausdrücklich gesetzt wurde, nimmt das Programm an, dass dieses mit dem Benutzerpasswort identisch ist. 
        """
        self.browser.get(self.iserv_url + "admin/login")
        if (self.password_admin == ""):
            self.password_admin = self.password_user
            
        time.sleep(2)
        
        input = self.browser.find_element_by_name("form[_password]")
        input.send_keys(self.password_admin)
        input.submit()

