# coding: utf-8
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


import time, datetime
import os, platform
import sqlite3, csv
import re
#import iservTools

import iservData

from iservGroups import groupsObject
from iservToolBox import toolboxObject

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Color

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class importObject:
    """ importObject

        Managt die Erstellung von csv-Dateien für das iServ Import-Modul

    """
    
    def __init__(self, iserv):
        self.iserv = iserv
        self.tools = toolboxObject(iserv)
        self.groups = groupsObject(iserv)
        self.iserv.message = ""
           
    def update_teacher_list(self, teacher_file):
        """Aktualisiert die Liste der Lehrer in der Datenbank auf Basis einer CSV-Datei.
        
        :param teacher_file: (string) Name der CSV-Datei mit den Lehrerdaten
        
        Die CSV-Datei mit den Lehrerdaten sollte enthalten:
              
        - Kürzel
        - Personalnummer 
        - Vorname
        - Name
               
        Schreibt die Daten in die Datenbank **self.iserv.database** in die Tabelle Lehrer
    
        """
        conn = sqlite3.connect(self.iserv.database)
        c = conn.cursor()

        with open(teacher_file, 'rt', encoding="iso-8859-1") as csvfile:

            teacherData = csv.reader(csvfile, delimiter=",")
            self.iserv.write_table_timestamp("Lehrer")

            c.execute("DROP TABLE IF EXISTS Lehrer")
            self.iserv.create_table("Lehrer")

            counter = 0
            for row in teacherData:
                if (counter == 0):
                    if ("KÜRZEL" in row):
                        iKurz    = row.index("KÜRZEL")
                    else:
                        iKurz = -1
                 
                    if "PERSONALNR" in row:
                        iId = row.index("PERSONALNR")
                    else:
                        iId = -1
                        print("NUMMER fehlt!")
                        
                    if "NAME, VORNAME" in row:
                        iName    = row.index("NAME, VORNAME")
                        iVorname = row.index("NAME, VORNAME")
                    else:
                        iName    = row.index("NAME")
                        iVorname = row.index("VORNAME")

                counter = counter + 1

                if (iName == iVorname):
                    name = row[iName].split(", ")
                    mNachname = name[0]
                    mVorname = name[1]
                else:
                    mNachname = row[iName]
                    mVorname = row[iVorname]
                    
                mName = mNachname + ", " + mVorname
                
                if (iKurz < 0):
                    mKurz = ""
                else:
                    mKurz = row[iKurz]
                    
                mId = row[iId]

                if counter > 1:

                   c.execute("INSERT INTO Lehrer (Kurz, Name, Vorname, Id) VALUES (?,?,?,?)",
                             (mKurz, mNachname, mVorname, mId))
                   conn.commit()
                   
            c.close
            conn.close   
    
    
    
    def update_student_list(self, student_file):
        """Aktualisiert die Liste der Schüler in der Datenbank auf Basis einer CSV-Datei.
        
        :param student_file: (string) Name der CSV-Datei mit den Lehrerdaten
            - erfordert Vorname, Name, Id, Klasse
     
        Schreibt die Daten in die Datenbank **self.iserv.database** in die Tabelle Schueler
    
        """
        conn = sqlite3.connect(self.iserv.database)
        c = conn.cursor()
        self.message = "Öffne Datei " + student_file
        
        with open(student_file, 'rt', encoding="iso-8859-1") as csvfile:
        #with open(self.data_dir + "/" + student_file, 'rt', encoding="iso-8859-1") as csvfile:

            #iservTools.DateiInfo(studentFile)
            myLine = csv.reader(csvfile, delimiter=",")
            aKlassenliste = []
            counter = 0

            self.iserv.write_table_timestamp("Schueler")
            c.execute("DROP TABLE IF EXISTS Schueler")
            self.iserv.create_table("Schueler")

            c.execute("DROP TABLE IF EXISTS Gruppenmitglieder")
            c.execute('CREATE TABLE Gruppenmitglieder (Id TEXT, Gruppe TEXT)')

            for row in myLine:
                if (counter == 0):
                    iKlasse = row.index("KLASSE")
                    iId = row.index("IDENTNUMMER")
                    iVorname = -1
                    if ("NAME, RUFNAME" in row):
                        iNameVorname = row.index("NAME, RUFNAME")
                    else:
                        iVorname = row.index("RUFNAME")
                        iName = row.index("FAMILIENNAME")
                  
                else:
                    vKlasse = row[iKlasse]
                    vId = row[iId]
                    
                    if (iVorname <0):
                        vName = row[iNameVorname]
                        vName.replace("(","")
                        vName.replace(")","")
                        aName = vName.split(", ")
                        vName = aName[0]
                        vVorname = aName[1]
                    else:
                        vName = row[iName]
                        vVorname = row[iVorname]
                        vVorname.replace(")", "")
                        vVorname.replace("(", "")

                    c.execute("INSERT INTO Schueler (Name, Vorname, Id, Klasse) VALUES (?,?,?,?)",
                              (vName, vVorname, vId, vKlasse))
                    conn.commit()

                counter = counter + 1

        c.close
        conn.close    

    
    def import_tutor_list(self):
        """
        Importiert eine Liste der Klassenlehrer aus **Klassenlehrer.txt**
        
        """
        self.iserv.message = "Datei 'Klassenlehrer.txt' nicht gefunden."
        
        with open(self.iserv.data_dir + "/Klassenlehrer.txt", 'rt', encoding="utf-8") as csvfile:
            conn = sqlite3.connect(self.iserv.database)
            c = conn.cursor()
            
            self.iserv.write_table_timestamp("Klassen")
            self.iserv.message = "Importiere Datei 'Klassenlehrer.txt'."
            
            c.execute("DROP TABLE IF EXISTS Klassen")
            c.execute('CREATE TABLE Klassen (Klasse TEXT, Kurz TEXT, Jahrgang INT)')
            
            Data = csv.reader(csvfile, delimiter=" ")
            for row in Data:
                Klasse = row[0]
                Tutor = row[1]
                Jahrgang = int(self.tools.get_year_by_class(Klasse))
                c.execute("INSERT INTO Klassen (Klasse, Kurz, Jahrgang) VALUES (?,?,?)",
                              (Klasse, Tutor, Jahrgang))
                conn.commit()

            c.close
            conn.close
        
    
    def add_teacher_accounts_to_db(self):
        """Ergänzt die Lehreraccounts in der Lehrer-Tabelle der Datenbank"""
        TabellenDatum = self.iserv.check_table("Lehrer")
        self.iserv.message = TabellenDatum
        if ("nicht" in TabellenDatum):
            self.iserv.message += " Die Daten können nicht ergänzt werden."
        else:
            self.iserv.login()
            self.iserv.admin_login()
            
            url = self.iserv.iserv_url + "admin/user?filter[status]=&filter[roles][]=ROLE_TEACHER&filter[search]="
            self.iserv.browser.get(url)
            time.sleep(4)

            xpath_table = '//*[@id="crud-table"]'      
            Zeilen = self.iserv.browser.find_elements_by_xpath(xpath_table + "/tbody[1]/tr")
            
            conn = sqlite3.connect(self.iserv.database)
            c = conn.cursor()
            
            i = 0
            for row in Zeilen:
                Zeile = row.find_elements_by_tag_name("td")
       
                if (len(Zeile) > 1):
                    i = i + 1
                    Account = Zeile[1].text
                    Vorname = Zeile[2].text
                    Nachname = Zeile[3].text
                    
                    c.execute("UPDATE Lehrer SET eMail = ? WHERE Vorname = ? AND Name = ?",
                               (Account, Vorname, Nachname))
                    conn.commit()
                  
            self.iserv.logout()
            self.iserv.message += "\n  Daten ergänzt."
            
        

        
    
            
    def export_teacher_account_list_html(self):
        """Exportiert eine Liste der Lehrer-Accounts als HTML-Tabelle."""
        self.iserv.message = "\nExportiere Kürzelliste als HTML\n"
        conn = sqlite3.connect(self.iserv.database)
        c = conn.cursor()
        
        c.execute("SELECT eMail, Kurz, Vorname, Name FROM Lehrer ORDER BY Kurz")
        Liste = c.fetchall()    
        
        if (Liste[0][0] == ""):
            self.iserv.message += "Die Accounts sind noch nicht eingetragen. Export nicht möglich."
        else:
            
            f= open(self.iserv.data_dir + "/TeacherAccounts.html","w+")
            f.write("<table>\n<tr bgcolor=orange><td>Kürzel &nbsp; </td><td>Name</td><td><span style='font-family: courier new, courier;'>E-Mail</span></td></tr>")
            i=0
            for row in Liste:
                i = i + 1
                Kurz = row[1]
                Vorname = row[2]
                Name = row[3]
                Account = str(row[0])
                
                if (i % 2 == 1):
                    bgColor = "white"
                else:
                    bgColor = "lightyellow"
                    
                f.write("\n\n<tr bgcolor=" + bgColor + "><td width='100'>" + Kurz + "</td><td>  &nbsp; " + Vorname + " " + Name + " &nbsp; </td><td><span style='font-family: courier new, courier;'>" + Account + "</span></td></tr>")
            f.write("\n\n</table>")
            f.close
        
        
        
        c.close
        conn.close
   
    
    def import_highschool_courses(self, OberstufenFile):
        """Aktualisiert die Teilnehmer der Oberstufenkurse aufgrund eines Exports aus IndiWare.
        
           :param OberstufenFile: (string) Excel-Datei mit den Oberstufenkursen mit Dateipfad
        """
        if ("/" not in OberstufenFile):
            OberstufenFile = self.data_dir + "/" + OberstufenFile
        
        if (os.path.isfile(OberstufenFile)):
            
            conn = sqlite3.connect(self.iserv.database)
            c = conn.cursor()
            
            with open(OberstufenFile, 'rt', encoding="utf-8") as csvfile: 
                self.iserv.write_table_timestamp("Oberstufe") 
                Data = csv.reader(csvfile, delimiter=";")
                
                c.execute("DROP TABLE IF EXISTS Oberstufe")
                c.execute('CREATE TABLE Oberstufe (Kurs TEXT, Name TEXT)')

                vKursname = ""
                vKursleiter = ""

                for row in Data:
                    if (row[0] == "Kursliste"):
                        if (row[7] != ""):
                            vKursname = row[7]
                        else:
                            vKursname = row[10]

                        vKursname = vKursname.split(" - ")
                        vKursname = vKursname[0]

                    if (re.search("\d+", row[3]) or re.search("\d+", row[2]) or re.search("\d+", row[1])):
                        if row[4] != "":
                            vName = row[4]
                        else:
                            vName = row[7]

                        vId = self.get_student_id(vName)

                        c.execute("INSERT INTO Oberstufe (Name, Kurs) VALUES (?,?)",
                              (vName, vKursname))
                        c.execute("INSERT INTO Gruppenmitglieder (Id, Gruppe) VALUES (?,?)",
                              (vId, vKursname))

                        conn.commit()
                    
                c.close
                conn.close
    
    def import_highschool_courses_csv(self, OberstufenFile):
        """Aktualisiert die Teilnehmer der Oberstufenkurse aufgrund eines Exports aus IndiWare.
        
           :param OberstufenFile: (string) Excel-Datei mit den Oberstufenkursen mit Dateipfad
        """
        if ("/" not in OberstufenFile):
            OberstufenFile = self.iserv.data_dir + "/" + OberstufenFile
        
        if (os.path.isfile(OberstufenFile)):
            
            conn = sqlite3.connect(self.iserv.database)
            c = conn.cursor()
            
            with open(OberstufenFile, 'rt', encoding="utf-8") as csvfile: 
                self.iserv.write_table_timestamp("Oberstufe") 
                Data = csv.reader(csvfile, delimiter=";")
                
                c.execute("DROP TABLE IF EXISTS Oberstufe")
                c.execute("DROP TABLE IF EXISTS Kurse")
                c.execute('CREATE TABLE Oberstufe (Kurs TEXT, Name TEXT, Gruppe TEXT, Jahrgang INT)')
                c.execute('CREATE TABLE Kurse (Kurs TEXT, Kursleitung TEXT, Gruppe TEXT, Jahrgang INT)')
                
                
                vKursname = ""
                vKursleiter = ""
                AbiJahrgang = ""

                for row in Data:
                    if (row[0] == "Kursliste"):
                        if (row[11] != ""):
                            vKursname = row[11]
                        else:
                            vKursname = row[10]
                         
                        vKursname = vKursname.split(" - ")
                        vKursname = vKursname[0]
                        
                        
                    if (AbiJahrgang == "" and "Abiturjahrgang" in row[0]):
                        d = row[0].split(", ")
                        AbiJahrgang = d[0][-4:]
                        if (AbiJahrgang == self.iserv.abi_jg_12):
                            Jahrgang = 12
                        else:
                            Jahrgang = 13
                        
                         
                        vKursname = vKursname.split(" - ")
                        vKursname = vKursname[0]
                    if (row[0] == "Kursleiter:"):
                        vKursleiter = row[11]
                        vKursleiter = vKursleiter.replace("Herr ", "")
                        vKursleiter = vKursleiter.replace("Frau ", "")
                        vKursleiter = vKursleiter.replace("Dr. ", "")
                        Gruppe = self.tools.get_highschool_groupname(vKursname) + "-" + AbiJahrgang
                        c.execute("SELECT Vorname FROM Lehrer WHERE Name = ?",(vKursleiter,))
                        res = c.fetchall()
                        if (len(res) > 0):
                            vKursleiter = res[0][0] + " " + vKursleiter
                            c.execute("INSERT INTO Kurse (Kurs, Kursleitung, Jahrgang, Gruppe) VALUES (?,?,?,?)",
                              (vKursname, vKursleiter, Jahrgang, Gruppe))

                        else:
                            
                            vKursleiter = ""
                            
                        
                            
                 
                        
                    if (re.search("\d+", row[3]) or re.search("\d+", row[2]) or re.search("\d+", row[1])):
                        if row[4] != "":
                            vName = row[4]
                        else:
                            vName = row[7]
                        
                        vId = self.tools.get_student_id_by_name(vName)
                        

                        c.execute("INSERT INTO Oberstufe (Name, Kurs, Jahrgang, Gruppe) VALUES (?,?,?,?)",
                              (vName, vKursname, Jahrgang, Gruppe))
                        conn.commit()
                        
                        if (vId != ""):
                            c.execute("INSERT INTO Gruppenmitglieder (Id, Gruppe) VALUES (?,?)",
                              (vId, vKursname))
                            conn.commit()
                        #else:
                            #print(vName)
                       
                    
                        
                    
                c.close
                conn.close
    
    def update_class_teachers(self):
        """
        Liest die Lehrer einer Klasse aus der Untis-Datei GPU002.TXT aus. 
        """
        if (os.path.isfile(self.data_dir + "/GPU002.TXT")):

            conn = sqlite3.connect(databaseFile)
            c = conn.cursor()

            with open("./data/GPU003.TXT", 'rt', encoding="iso-8859-1") as csvfile:
                 Data = csv.reader(csvfile, delimiter=",")
                 for row in Data:
                      vKlasse = row[0]
                      vLehrer = row[29]

                      if (vLehrer != ""):
                          vLehrerId = iservTools.LehrerId(vLehrer)
                          c.execute("UPDATE Klassen SET Klassenlehrer=? WHERE Klasse = ?",
                               (vLehrerId, vKlasse))
                          conn.commit()
                #print (vKlasse + "  " + iservTools.get_teacher_name_by_id(vLehrerId))

            c.close
            conn.close
    
    
    def export_iserv_list_teachers(self, list_S, list_L):
        """Exportiert die Liste der Lehrer für den Import in iServ.
        
    
        - Liest die Informationen aus der Datenbank iserv.database aus und speichert sie im passenden Format für das Import-Modul von iServ.
        
        - Lehrer werden hier auch den Klassengruppen, in denen sie aktuell unterrichten zugeordnet, wenn der Stundenplan bereits importiert wurde. 
        
        - Grundsätzlich ist hier auch eine Zuordnung in den Oberstufenkursen möglich, wenn eine entsprechende Datei aus IndieWare importiert wurde.
        
        - Die Zuordnung erfolgt über die Tabelle **Gruppenmitglieder**.
        
        :param list_S: (int) Wenn der Wert 1 ist, wird für Klassen eine Klassenlehrerliste mit den Schülern angelegt. In diesem Fall werden der Klassenlehrer z.B. zur Klassenliste 10a-S hinzugefügt. Voraussetzung ist, dass eine Liste der Klassenlehrer eingelesen wurde.
        
        :param list_L: (int) Wenn der Wert 1 ist, wird eine Lehrerliste für die Klasse angelegt, bei 0 erfolgt das nicht. Vorausetzung ist, dass der Stundenplan eingelesen wurde.
    
           
        """
        TabellenDatum = self.iserv.check_table("Lehrer")
        if ("nicht" in TabellenDatum):
            self.iserv.message = "Die Tabelle mit den Lehrerdaten ist leer. Export NICHT möglich."
        else:
            self.iserv.message = "Tabelle 'Lehrer' (" + str(TabellenDatum) + ") ausgelesen."
            conn = sqlite3.connect(self.iserv.database)
            c = conn.cursor()
            i = 0
            c.execute("SELECT Name, Vorname, Kurz, Id FROM Lehrer ASCENDING") # (Name, Vorname, Id, Klasse)
            Data = c.fetchall()

            iservFile  = open(self.iserv.data_dir + '/iserv-Lehrer-Gruppen.csv', "w")
            iservWriter = csv.writer(iservFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL) 
            
           
            
            for row in Data:
                i = i + 1
                vName     = row[0]
                vVorname  = row[1]
                vKurz     = row[2]
                vId = row[3]
                vGruppen  = ""    
                
                ###
                ### Lehrer in der Klasse 
                ###               
                
                c.execute("SELECT Klasse FROM Lehrer_in_Klasse WHERE Lehrer_kurz= ? ", (vKurz,)) 
                aKlassen = c.fetchall()

                if aKlassen:
                    for row in aKlassen:
                        Klasse = row[0]
                        Gruppe = self.tools.get_class_groupname(Klasse)
                        print(Gruppe)
                        if (Gruppe not in vGruppen):
                            vGruppen += Gruppe + ","
                        if (list_L == 1 and Gruppe + "-L," not in vGruppen):
                            vGruppen += Gruppe + "-L,"  
            
                ###
                ### Klassenlehrer
                ###
                
                c.execute("SELECT Klasse FROM Klassen WHERE Kurz = ?",(vKurz,))
                res = c.fetchall()
                
                if (res):
                    Klasse = res[0][0]
                    Gruppe = self.tools.get_class_groupname(Klasse)
                    if (list_S == 1 and Gruppe + "-S," not in vGruppen):
                        vGruppen += Gruppe + "-S," 

                iservWriter.writerow([vVorname, vName, vId, vGruppen])

            iservFile.close() 

            c.close
            conn.close

    
        
    def export_iserv_list_students(self, list_S):
        """Exportiert die Liste der Schüler (*iserv-Schueler.csv*) für den Import in iServ.
        
        - Wenn der Oberstufenplan importiert wurde, werden Gruppen für Kurse angelegt und die Schüler diesen zugeordnet.
        
        - Es können Klassengruppen mit Klassenlehrer und Schülern (z.B. Klasse-10a-S) automatisch angelegt und zugewiesen werden. 
        
           :param list_S: (int) Wenn der Wert 1 ist, wird eine Klassengruppe (zu der auch der Klassenlehrer gehört) angelegt. Wird der Wert 0 übergeben, wird die zusätzliche List nicht angelegt.
        """

        TabellenDatum = self.iserv.check_table("Schueler")
        if ("nicht" in TabellenDatum):
            self.iserv.message = "Die Tabelle mit den Schülerdaten ist leer."
        else:
            self.iserv.message = "Die Tabelle 'Schueler' ("+ TabellenDatum +") wird ausgelesen."
            conn = sqlite3.connect(self.iserv.database)
            c = conn.cursor()
            i = 0
            c.execute("SELECT * FROM Schueler ASCENDING") # (Name, Vorname, Id, Klasse)
            Data = c.fetchall()
            self.iserv.message = "Schreibe Daten in " + self.iserv.data_dir + "/iserv-Schueler.csv"
            print(self.iserv.message)
            iservFile  = open(self.iserv.data_dir + "/iserv-Schueler.csv", "w")
            iservWriter = csv.writer(iservFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)

            GruppenTabelle = self.iserv.check_table("Gruppenmitglieder")
            
            if ("nicht" in GruppenTabelle):
                self.iserv.message += "\n\nEs werden keine besonderen Gruppenmitgliedschaften eingelesen, weil die entsprechende Tabelle nicht existiert."
            else:
                self.iserv.message += "\n\nGruppenmitlgiedschaften werden ausgelesen."
                    
            for row in Data:
                i = i + 1
                vName     = row[0]
                vVorname  = row[1]
                vId       = row[2]
                vKlasse   = row[3]
                vJahrgang = self.tools.get_year_by_class(vKlasse)
                
                if (list_S == 1 and vJahrgang < 12):
                    vGruppen = "Schüler-innen,Klasse-" + vKlasse + "-" + str(self.iserv.end_of_year) + "-S,Klasse-" + vKlasse + "-" + str(self.iserv.end_of_year)
                else:
                    vGruppen = "Schüler-innen,Klasse-" + vKlasse + "-" + str(self.iserv.end_of_year)
                
                if ("nicht" not in GruppenTabelle):
                
                    c.execute("SELECT * FROM Gruppenmitglieder WHERE Id = ? ", (vId,)) 
                    aGruppen = c.fetchall()
                    
                    if aGruppen:

                       for line in aGruppen:
                           vNeueGruppe = iservTools.OberstufengruppenName(line[1])
                           vGruppen = vGruppen + "," + vNeueGruppe
                           vGruppen = vGruppen[1:]

                iservWriter.writerow([vName, vVorname, vId, vKlasse, vGruppen])
                
            iservFile.close() 

            c.close
            conn.close
            print("... " +str(i) + " Schüler exportiert")
        


    def set_passwords_for_new_users(self):
        """Setze Passwörter für neue Benutzer und generiere Infoblätter.
        """
        self.iserv.login()
        self.iserv.admin_login()
        url = self.iserv.iserv_url + "admin/user?filter%5Broles%5D%5B0%5D=ROLE_STUDENT&filter%5Bdefault_pwd%5D=default_pwd&sort%5Bby%5D=username&sort%5Bdir%5D=ASC"
        self.iserv.browser.get(url)
        time.sleep(4)
        
        xpath_table = '//*[@id="crud-table"]'      
        Zeilen = self.iserv.browser.find_elements_by_xpath(xpath_table + "/tbody[1]/tr")
        
        conn = sqlite3.connect(self.iserv.database)
        c = conn.cursor()
        
        c.execute("DROP TABLE IF EXISTS neue_Schueler")
        c.execute('CREATE TABLE neue_Schueler (Name TEXT, Vorname TEXT, Account TEXT, erstellt TEXT)')
        for row in Zeilen:
            Zeile = row.find_elements_by_tag_name("td")
       
            if (len(Zeile) > 1):
                    
                Account = Zeile[1].text
                Vorname = Zeile[2].text
                Nachname = Zeile[3].text
                erstellt = Zeile[5].text
                
                c.execute("INSERT INTO neue_Schueler (Name, Vorname, Account, erstellt) VALUES (?,?,?,?)",
                             (Nachname, Vorname, Account, erstellt))
                conn.commit()
                   
        
        c.execute("SELECT Name, Vorname, Account, erstellt FROM neue_Schueler")
        alle = c.fetchall()
        if (alle):
            doc = Document()
            for row in alle:
                Vorname   = row[1]
                Nachname  = row[0]
                Account   = row[2]
                Klasse    = self.tools.get_class_of_student(Vorname, Nachname)
                Passwort  = self.groups.generate_user_password()
                
                self.groups.set_user_password(Account, Passwort)
                self.groups.print_info_page(Vorname, Nachname, Account, Passwort, Klasse, "", "", doc)
               
            
            doc.save(self.iserv.data_dir + "/iserv-Logins-neu.docx")
        c.close
        conn.close
        self.iserv.logout()
        


###########################



if __name__ == '__main__':

    print("\n\nIMPORT\n")

    iServ = iservData.iservObject()
    Import = importObject(iServ)


    #Import.import_highschool_courses_csv("AbiKursliste12.csv")
    Import.set_passwords_for_new_users()
    print(Import.iserv.message)

    print("\n")

