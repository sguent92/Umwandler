import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack 
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QScrollArea, QWidget, QButtonGroup, QTextBrowser, QFileDialog, QLineEdit, QComboBox, QRadioButton
from PyQt5.QtGui import QPixmap, QIntValidator, QIcon
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import collections
from os import walk





# =============================================================================
# Hilfefenster 
# =============================================================================
class HilfeFenster(QWidget):
    
    def __init__(self, Dateiname):
        super().__init__()

        vbox = QVBoxLayout()
        HilfBild = QLabel(self)
        HilfBild.setPixmap(QPixmap(Dateiname))
        vbox.addWidget(HilfBild)
        self.setLayout(vbox)
        self.move(200,200)
# =============================================================================
# Fenster zur Auswahl des Simulationsprogrammes für welches die Ausgabe erfolgen soll
# =============================================================================
class AuswahlFenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.setGeometry(400,400,400,200)
        
        l = QLabel(self)
        l.move(20,20)
        l.setText('Bitte wählen Sie für welches Programm die Daten verarbeitet werden sollen')
        
        l1 = QLabel(self)
        l1.move(20,60)
        l1.setText('Simpack:')
        
        self.simpack_button = QRadioButton(self)
        self.simpack_button.move(80,62)
        self.simpack_button.toggled.connect(self.freigabe)
        
        l2 = QLabel(self)
        l2.move(20,100)
        l2.setText('Masta:')
        
        self.masta_button = QRadioButton(self)
        self.masta_button.move(80,102)
        self.masta_button.toggled.connect(self.freigabe)
        
        l3 = QLabel(self)
        l3.move(20,140)
        l3.setText('SinulationX:')

        self.simx_button = QRadioButton(self)
        self.simx_button.move(80,142)
        self.simx_button.toggled.connect(self.freigabe)       
        
        self.weiter = QPushButton('Weiter', self)
        self.weiter.move(300,160)
        self.weiter.setDisabled(True)
        self.weiter.clicked.connect(self.close)
        
        self.show()
        
    def freigabe(self):
        self.weiter.setDisabled(False)
        
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
Auswahl = AuswahlFenster()

app.exec_()



# =============================================================================
# Imm Vorlagenfenster kann die Vorlage ausgwählt werden, die beschreibt in welcher Form die auszulesenden Daten vorliegen
# =============================================================================

class VorlagenFenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.setGeometry(400,400,800,250)
        
        l = QLabel(self)
        l.setText('Wählen Sie eine Vorlage für die auszulesenden Daten.\n\n\n Wenn sich Ihre Vorlage nicht in "G:\\TS-X1\\Studenten\\2020_SGuenther_NVH\\Umwandler\\Vorlagen" befindet können Sie auch manuell danach suchen.')
        l.move (20,10)
        
        l2 = QLabel(self)
        l2.move(40,100)
        l2.setText('aus Liste wählen:')
        
        l3 = QLabel(self)
        l3.move(320,100)
        l3.setText('nach Vorlage suchen:')
        
        l4 = QLabel(self)
        l4.move(40,170)
        l4.setText('Ich möchte eine neue Vorlage erstellen:')
        
        self.r1 = QRadioButton(self)# radiobutton für auswahl aus default Vorlagenordner
        self.r1.move(140,100)
        self.r1.setChecked(True)
        self.r1.clicked.connect(self.freigabe1)      
        
        self.r2 = QRadioButton(self)# radiobutton für manuelle auswahl
        self.r2.move(440,100)
        self.r2.clicked.connect(self.freigabe2)
        
        self.neue_vorlage = False
        self.r3 = QRadioButton(self)
        self.r3.move(250,170)
        self.r3.clicked.connect(self.freigabe3)
        
        self.t= QTextBrowser(self)
        self.t.setGeometry(490,90,280,30)
        self.t.setDisabled(True)
        
        self.b1 = QPushButton('Durchsuchen', self)
        self.b1.move(490,125)
        self.b1.setDisabled(True)
        self.b1.clicked.connect(self.laden)
        
        h = QLabel(self)
        h.setText('Hilfe:')
        h.move(705, 10)
        frage = QPushButton(self)
        frage.setIcon(QIcon("bilder_vorlagenersteller\\FrageIcon.png"))
        frage.move(740, 6)
        frage.clicked.connect(self.Hilfe)        
        
        self.vorlagen = []
        for (Pfad, Ordner, vorlage) in walk('G:/TS-X1/Studenten/2020_SGuenther_NVH/Umwandler/Vorlagen'):
            self.vorlagen.extend(vorlage)# schreibt datein im Vorlageordner auf liste "vorlagen"

        
        self.auswahl = QComboBox(self)# Combobox zur Auswahl der Vorlagen im Vorlagenordner
        self.auswahl.move(170,97)
        for vorlage in self.vorlagen:
            self.auswahl.addItem(vorlage)# gibt die gefundenen Vorlagen an Combobox weiter
        self.auswahl.setCurrentIndex(self.vorlagen.index('JMAG.txt'))# definition des default Wertes/Vorlage

            
        b2 = QPushButton('Weiter', self)
        b2.move(700,210)
        b2.clicked.connect(self.weiter)
        
        self.show()
        
    def freigabe1(self):# freigabe 1 und 2 blenden die zur Verfügung stehenden Eingabemöglichkeiten ein oder aus. Je nach betätigung der Radiobutton
        self.t.setDisabled(True)
        self.b1.setDisabled(True)
        self.auswahl.setDisabled(False)
            
    def freigabe2(self):
        self.t.setDisabled(False)
        self.b1.setDisabled(False)
        self.auswahl.setDisabled(True)
        
    def freigabe3(self):
        self.t.setDisabled(True)
        self.b1.setDisabled(True)
        self.auswahl.setDisabled(True)
        
    def laden(self):# schreibt in manueller auswahl geladenen Name auf Dateiname und in den Textbrowser
        self.dateiname = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Datei öffnen', '.txt')[0])
        self.t.clear()
        self.t.append(self.dateiname)
        
    def weiter(self): #schreibt Name(mit Pfad) der zu lesenden Vorlage auf Variable "vorlagenname". Je nach Auswahl 
        if self.r1.isChecked():
            self.vorlagenname = 'G:/TS-X1/Studenten/2020_SGuenther_NVH/Umwandler/Vorlagen/' + self.vorlagen[self.auswahl.currentIndex()]
        elif self.r2.isChecked():
             self.vorlagenname = self.dateiname
        elif self.r3.isChecked():
            self.neue_vorlage = True
        self.close()
        
    def Hilfe(self):
        self.h = HilfeFenster("bilder_vorlagenersteller\\vorlage_auswählen.png")
        self.h.show()


app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
Vorlage = VorlagenFenster()
    
app.exec_()
    
if Vorlage.neue_vorlage:
    from Vorlagenersteller import * # öffnet Vorlagenersteller wenn gewünscht
        
    app = QtCore.QCoreApplication.instance() # öffnet neues Fenster für Vorlagenauswahl nach Ablauf der "Vorlagenersteller Routine"
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    Vorlage = VorlagenFenster()
    
    app.exec_()
    

# =============================================================================
# Einlesen der Daten aus der Vorlage auf die Dictionarys Kerndaten und Arbeitsdaten
# =============================================================================
    
Kerndaten = collections.OrderedDict()# dict mit Positionen von zahn_zah-, slice_zahl, Lastpunkt und Winkelauflösung in auszulesender Datei
Arbeitsdaten = collections.OrderedDict([])# dict für positionen der Kräfte und Momente 
block_zahl = 0# anzahl der Blöcke der einzelnen Kräfte(falls eine Kraft nicht nur mit einer Startzeil, - spalte , länge und Breite angegeben ist)
start_kerndaten = 5# erste Zeile der Vorlage aus der Kerndaten gelesen werden
start_arbdaten = 26# das selbe für Arbeitsdaten   
f = open(Vorlage.vorlagenname, 'r')# öffnet Vorlage mit oben eingelesenen namen
auslesedaten = f.readlines()# schreibt eingelesene Zeilen der Vorlage auf liste 
for i in range(0,4):
    key_kd = auslesedaten[start_kerndaten].replace('\n', '')# schlüssel des dictionarys für Kerndaten (z.B zaehne oder Lastpunkt)
    werte_kd = auslesedaten[start_kerndaten + 2].split('\t')[:-1]# Positionswerte für jeweiligen Schlüssel (startzeile, -spalte, länge, breite)
    Kerndaten[key_kd] = werte_kd# schreibt werte mit Schlüssel auf dict
    
    block_zahl = int(auslesedaten[start_arbdaten + 1][-2])# prüft anzahl der Blöcke der jeweiligen Arbeitsdaten, wichtig zur bestimmung der auszulesenden Zeile im nächsten Schleifendurchlauf
    key_ad = auslesedaten[start_arbdaten].replace('\n', '')
    werte_ad = auslesedaten[start_arbdaten + 3].split('\t')[:-1]           
    Arbeitsdaten[key_ad] = werte_ad# werte(Positionen der Daten) werden mit entsprechenden Schlüssel auf das dictionary Arbeitsdaten geschrieben
    for zeile in range(1,block_zahl):
        Arbeitsdaten[key_ad] = Arbeitsdaten[key_ad] + auslesedaten[start_arbdaten + 3 + zeile].split('\t')[:-1]# schreibt Werte aus weiteren eingelesenen Block ins dictionary, falls mehr als ein Block vorhanden
        
    start_kerndaten = start_kerndaten + 4# neubestimmung der Startzeile im nächsten durchlauf
    start_arbdaten = start_arbdaten + block_zahl + 4

f.close()
#------------------------------------------------------------------------------
# insofern Verarbeitung für SimulationX gewählt wurde, wird die Routine dafür hier aufgerufen
# und das Programm nach Ablauf der Routine abgebrochen
if Auswahl.simx_button.isChecked():
    from SimX_routine import *#SimX_Gerät import *
    sys.exit(0)    
# =============================================================================
# Fenster zum auslesen des Pfades und namen der zu bearbeitenden Datei
# =============================================================================

class LadeFenster(QWidget):
    def __init__(self): 
        super().__init__()
               
        self.setGeometry(350,350,700,200)
        self.setWindowTitle('Ladedialog')
        
        self.l = QtWidgets.QLabel(self)
        self.l.setGeometry(QtCore.QRect(160, 20, 551, 51))
        self.l.setText('Bitte wählen Sie eine Datei die Sie bearbeiten wollen und drücken Sie anschließend auf "Weiter"')
        self.textBrowser_2 = QtWidgets.QTextBrowser(self)
        self.textBrowser_2.setGeometry(QtCore.QRect(160, 60, 451, 40))
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Ausgewählte Datei:")
        self.label.setGeometry(QtCore.QRect(60, 60, 101, 31))

        button = QtWidgets.QPushButton(" Weiter" , self)
        button.setGeometry(QtCore.QRect(540, 160, 75, 23))
        button.clicked.connect(self.close)
        button2 = QPushButton('Durchsuchen', self)
        button2.setGeometry(QtCore.QRect(160, 100, 121, 23))
        button2.clicked.connect(self.laden)#
                
        self.show()
        
    def laden(self):#
        self.dateiname = str(QtWidgets.QFileDialog.getOpenFileName(self, 'Datei öffnen', 'C:\\')[0])
        self.textBrowser_2.clear()
        self.textBrowser_2.append(self.dateiname)

app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
Lade = LadeFenster()

app.exec_()  


# =============================================================================
# einlesen der Tabellen auf DataFrame und ablage des/ der DataFrame(s) in Ordered Dict
# =============================================================================
dtyp = Lade.dateiname[Lade.dateiname.rfind('.'):]# auslesen Dateiendung(z.B. .csv)

dtyp = Lade.dateiname[Lade.dateiname.rfind('.'):]

if dtyp == '.csv':
    spalten_namen = [i for i in range (0,1200)]# vordefinition der Spaltennamen, wird das nicht getan erhält mann einen Error wenn die Anzahl der elemente in einer Zeile größer ist als in der ersten Zeile
    df =  pd.read_csv(Lade.dateiname, delimiter=';', engine = 'python', nrows=1)# einlesen der ersten Zeile der csv datei
    if len(df.iloc[0][:]) == 1:
        df =  collections.OrderedDict([('1' , pd.read_csv(Lade.dateiname, delimiter=',', engine = 'python',skip_blank_lines = False , names = spalten_namen))])# csv wird eingelesen und auf orderedDict gelegt # liest csv auf dataframe df
    
    else:
        df =  collections.OrderedDict([('1' , pd.read_csv(Lade.dateiname, delimiter=';', engine = 'python',skip_blank_lines = False , names = spalten_namen))])# csv wird eingelesen und auf orderedDict gelegt

else:
    df =  pd.read_excel( Lade.dateiname, sheet_name = None, header = None)

df_keys = [] # liste mit den ausgelesenen Mappennamen, über den Index der Liste kommt das script später an den Namen der Mappen, welche die Schlüssel für das OrderedDict der eingelesenen Daten(df) sind
for i in range(0,len(df)):
    df_keys.append(list(df.items())[i][0])


# =============================================================================
# Fenster mit dem die Kerndaten(Zähne, Slices, Lastpunkt, Winkelauflösung)
#    manuell eingelesen werden können
#    wird aufgerufen wenn: 1. Beim Auslesen der Daten ein Fehkler auftritt
#    2. oder im Datenfenster die Option "manuelle Eingabe" gewählt wird
# =============================================================================
class EinleseFenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.initMe()
            
    def initMe(self):
            
        self.setGeometry(350,350,300,290)
        self.setWindowTitle('Einlesefenster')
        
        validator = QIntValidator(self)
        
        self.TZaehne = QtWidgets.QLineEdit(self)
        self.TZaehne.setGeometry(QtCore.QRect(130, 40, 121, 31))
        self.TZaehne.setValidator(validator)
        
        self.TSlices = QtWidgets.QLineEdit(self)
        self.TSlices.setGeometry(QtCore.QRect(130, 90, 121, 31))
        self.TSlices.setValidator(validator)
        
        self.TWinkel = QtWidgets.QLineEdit(self)
        self.TWinkel.setGeometry(QtCore.QRect(130, 140, 121, 31))
        
        self.TLastpunkt = QtWidgets.QLineEdit(self)
        self.TLastpunkt.setGeometry(QtCore.QRect(130, 190, 121, 31))
        self.TLastpunkt.setValidator(validator)
        
        label = QtWidgets.QLabel(self)
        label.setText("Anzahl der Zähne")
        label.setGeometry(QtCore.QRect(30, 40, 101, 20))

        label_2 = QtWidgets.QLabel(self)
        label_2.setText("Anzahl der Slices")
        label_2.setGeometry(QtCore.QRect(30, 90, 101, 20))

        label_3 = QtWidgets.QLabel(self)
        label_3.setText("Winkelauflösung")
        label_3.setGeometry(QtCore.QRect(30, 140, 80, 20))

        label_4 = QtWidgets.QLabel(self)
        label_4.setText('Lastpunkt')
        label_4.setGeometry(QtCore.QRect(30, 190, 80, 20))

        label_5 = QtWidgets.QLabel(self)
        label_5.setText('°')
        label_5.setGeometry(QtCore.QRect(260, 150, 47, 13))

        label_6 = QtWidgets.QLabel(self)
        label_6.setText('rpm')
        label_6.setGeometry(QtCore.QRect(260, 190, 21, 20))
        label_6.setObjectName("label_6")
        
        button = QtWidgets.QPushButton('Weiter', self)
        button.setGeometry(QtCore.QRect(180, 250, 75, 23))
        button.setObjectName("pushButton")
        button.clicked.connect(self.setze)
       
        self.show()
        
    def komma_weg(self,eingabe):# entfernt komma(falls vorhanden) aus eingabefelden, ersetzt es mit Punkt und gibt eingegebenen Wert im float Format zurück
        if ',' in eingabe:
            eingabe = eingabe.replace(',','.')
        return float(eingabe)      
    
    def setze(self):
        self.zahn_zahl = int(self.TZaehne.text())
        self.slice_zahl = int(self.TSlices.text())
        self.Motordrehzahl = float(self.TLastpunkt.text())
        self.Wink_Aufl = float(self.komma_weg(self.TWinkel.text()))        

        self.close()
        
# =============================================================================
# automatisches Auslesen der Kerndaten
# =============================================================================
def erweitertes_Auslesen(eingabestring, suchstring): # sucht mit in Kerndaten abgelegten suchstring nach den jeweiligen Daten und gibt Sie aus
    if isinstance(eingabestring, str):# prüft ob eingegebener Wert überhaut ein string ist
        if suchstring == '##Anfang##':
            start = 0
            ende = 1
        else:
            start = eingabestring.find(suchstring) + len(suchstring)# startet am ende des strings mit der direkt vor auszulesenden Wert kommt
            ende = start + 1
        while True: #schleife läuft solange, bis index "ende" auf eine stelle im String gesetzt wird, die keine zahl ist oder bis strin zuende ist. 
            try:
                int(eingabestring[ende])
                ende += 1
            except ValueError:
                break
            except IndexError:
                break
        return eingabestring[start:ende]
    else:
        return eingabestring
#-----------------------------------------------------------------------------               
V_Err = False
         
try:
    Motordrehzahl = df[df_keys[int(Kerndaten['Lastpunkt'][0])]].iloc[int(Kerndaten['Lastpunkt'][1]) - 1][int(Kerndaten['Lastpunkt'][2]) - 1]# Die Zellen in dem die Daten sich befinden werden ausgelesen
    zahn_zahl = df[df_keys[int(Kerndaten['zaehne'][0])]].iloc[int(Kerndaten['zaehne'][1]) - 1][int(Kerndaten['zaehne'][2]) - 1]
    slice_zahl = df[df_keys[int(Kerndaten['slices'][0])]].iloc[int(Kerndaten['slices'][1]) - 1][int(Kerndaten['slices'][2]) - 1]
    Wink_Aufl =  float(df[df_keys[int(Kerndaten['Winkel'][0])]].iloc[int(Kerndaten['Winkel'][1]) - 1][int(Kerndaten['Winkel'][2]) - 1])
    
    Motordrehzahl = int(erweitertes_Auslesen(Motordrehzahl, Kerndaten['Lastpunkt'][3])) # mit der Funktion "erweitertes Auslesen" wird innerhalb der Zellen nach den entsprechenden Daten gesucht    
    zahn_zahl = int(erweitertes_Auslesen(zahn_zahl, Kerndaten['zaehne'][3]))
    slice_zahl = int(erweitertes_Auslesen(slice_zahl, Kerndaten['slices'][3]))
    
except ValueError:
    V_Err = True         
 


# =============================================================================
# 
# #fragt ausgelesene Daten ab und gibt Möglichkeit zur manuellen Korrektur
# # erfolgt Value Error bei automatischer Auslese, erfolgt manuelles einlesen automatisch
# =============================================================================
    
class DatenFenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.initMe()
        
    def initMe(self):
        self.setGeometry(350,350,250,250)
        self.setWindowTitle('Datenüberprüfung')
        self. manuell = False
        self.l = QLabel(self)
        self.l.move(20, 20)
        self.l.setObjectName("textBrowser")
        self.l.setText('Bitte prüfen Sie die eingelesenen Daten\n\nAnzahl der Zähne:\t' + str(zahn_zahl) + '\nAnzahl der Slices:\t' + str(slice_zahl) + '\nWinkelauflösung:\t' + str(Wink_Aufl) + ' °' + '\nMotordrehzahl:       \t' + str(Motordrehzahl) + ' rpm\n\n' + 'Sind die eingelesenen Daten korrekt?')
        
        self.manuell = False
        
        button = QtWidgets.QPushButton('Manuelle Eingabe' , self)
        button.move(20,220)
        button.clicked.connect(self.call_manuell)
        button.released.connect(self.close)
        button2 = QPushButton('Daten sind korrekt', self)
        button2.move(130, 220)
        button2.clicked.connect(self.close)#
        self.show()
        
    def call_manuell(self):#
        self.manuell = True




if V_Err == False:# wird nur aufgerufen wenn beim Einlesen der Kerndaten kein Fehler erfolgt, ansonsten wird direkt das Einlesefenster aufgerufen        
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    
    Datenueberpruefung = DatenFenster()
    
    app.exec_()
    
    V_Err = Datenueberpruefung.manuell
# =============================================================================
# Manuell eingelesene Daten werden(wenn vorhanden) auf Variablen geschrieben
# =============================================================================        
if V_Err == True :# öffnet ggf. Einlesefenster und schreibt die eingegebenen Werte auf die entsprechenden Variabeln
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)        
    Manuelle_Einlese = EinleseFenster()       
    app.exec_()
    
    Motordrehzahl = Manuelle_Einlese.Motordrehzahl
    zahn_zahl = Manuelle_Einlese.zahn_zahl
    slice_zahl = Manuelle_Einlese.slice_zahl
    Wink_Aufl =  Manuelle_Einlese.Wink_Aufl
# =============================================================================
#fragt ab mit welchen faktor die jeweiligen Kräfte skaliert werden sollen   
# =============================================================================
class SkalierungsFenster(QWidget):
        
    def __init__(self): 
        super().__init__()
        self.initMe()
        
    def initMe(self):
        self.setGeometry(350,350,330,350)
        self.skalierung = False
        
        Text = QLabel(self)
        Text.setGeometry(20,10, 350 , 85)
        Text.setText('Bitte wählen geben Sie ein mit welchen Faktor Sie die Daten\nskalieren möchten und bestätigen Sie ihre Änderungen.\n\nMöchten Sie ohne Skalierung fortfahren,\ndrücken Sie einfach auf "Weiter"')
        
        self.ges_Moment =QLineEdit(self)
        self.ges_Moment.setText('1')
        self.ges_Moment.setGeometry(QtCore.QRect(160, 100, 121, 31))
        self.ges_Moment.setVisible(Auswahl.masta_button.isChecked())# nur sichtbar wenn Daten für Masta verarbeitet werden sollen

        
        self.Radial = QLineEdit(self)
        self.Radial.setText('1')
        self.Radial.setGeometry(QtCore.QRect(160, 150, 121, 31))
        
        self.Tangential = QLineEdit(self)
        self.Tangential.setText('1')
        self.Tangential.setGeometry(QtCore.QRect(160, 200, 121, 31))
        
        self.Moment = QLineEdit(self)
        self.Moment.setText('1')
        self.Moment.setGeometry(QtCore.QRect(160, 250, 121, 31))
        self.Moment.setVisible(Auswahl.simpack_button.isChecked())# nur sichtbar, wenn Daten für simpack verarbeitet werden sollen
        
        label0 = QLabel(self)
        label0.setText('Faktor Gesamtmoment')
        label0.setGeometry(QtCore.QRect(20, 100, 140, 20))
        label0.setVisible(Auswahl.masta_button.isChecked())
        
        label1 = QtWidgets.QLabel(self)
        label1.setText("Faktor Radialkraft")
        label1.setGeometry(QtCore.QRect(20, 150, 140, 20))
        
        label2 = QtWidgets.QLabel(self)
        label2.setText("Faktor Tangentialkraft")
        label2.setGeometry(QtCore.QRect(20, 200, 140, 20))
        
        label3 = QtWidgets.QLabel(self)
        label3.setText("Faktor Biegemoment")
        label3.setGeometry(QtCore.QRect(20, 250, 140, 20))
        label3.setVisible(Auswahl.simpack_button.isChecked())

        button = QtWidgets.QPushButton('Weiter', self)
        button.setGeometry(QtCore.QRect(210, 310, 75, 23))
        button.clicked.connect(self.uebernehme)
                           
        self.show()
        
    def komma_weg(self,eingabe):# entfernt komma(falls vorhanden) aus eingabefelden, ersetzt es mit Punkt und gibt eingegebenen Wert im float Format zurück
        if ',' in eingabe:
            eingabe = eingabe.replace(',','.')
        return float(eingabe)      
        
    def uebernehme(self):
        self.faktor_mom_ges = self.komma_weg(self.ges_Moment.text())
        self.faktor_rad = self.komma_weg(self.Radial.text())
        self.faktor_tan = self.komma_weg(self.Tangential.text())
        self.faktor_mom_bieg = self.komma_weg(self.Moment.text())

        
        if (self.faktor_rad != 1)  | (self.faktor_tan != 1)  | (self.faktor_mom_bieg != 1) | (self.faktor_mom_ges != 1):
            self.skalierung = True
            
        self.close()
      

app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)

Skalierung = SkalierungsFenster()

app.exec_()
# =============================================================================
# ließt name und Pfad der zu speichernden Datei ein
# =============================================================================
class SpeicherFenster(QWidget):
    def __init__(self): 
        super().__init__()
        eingabename = Lade.dateiname[Lade.dateiname.rfind('/') + 1 : Lade.dateiname.rfind('.')]
        
        if Auswahl.masta_button.isChecked():
            ausgabeordner = 'Ausgabe_Masta/'
        elif Auswahl.simpack_button.isChecked():
            ausgabeordner = 'Ausgabe_Simpack/'
            
        self.default_ausgabe = ausgabeordner + eingabename + '_ausgabe'
        
        self.setGeometry(350,350,700,250)
        self.setWindowTitle('Speicherdialog')
        
        self.textBrowser = QLabel(self)
        self.textBrowser.setGeometry(QtCore.QRect(60, 30, 551, 51))
        self.textBrowser.setText('Wo möchten Sie die Dateien speichern?')
        
        self.textBrowser_2 = QTextBrowser(self)
        self.textBrowser_2.setGeometry(QtCore.QRect(160, 140, 451, 31))
        self.textBrowser_2.setText(self.default_ausgabe)


#        self.textBrowser_2.textChanged.connect(self.weiter)
        
        self.label = QLabel(self)
        self.label.setText("Speicherort:")
        self.label.setGeometry(QtCore.QRect(60, 140, 101, 31))
        
        self.button = QPushButton(" Fertig" , self)
        self.button.setGeometry(QtCore.QRect(540, 180, 75, 23))
#        self.button.setDisabled(True)
        self.button.clicked.connect(self.weiter)
        
        button2 = QPushButton('Datei Speichern', self)
        button2.setGeometry(QtCore.QRect(160, 180, 121, 23))
        button2.clicked.connect(self.speichern)#
             
        self.show()
        
    def speichern(self):#schreibt ausgewählten Dateiname - und Pfad in Textfenster und auf die Variable self.ausgabename(zur späteren verwendung) 
        self.ausgabename = QFileDialog.getSaveFileName(self, 'Datei speichern', self.default_ausgabe )[0]
        self.textBrowser_2.clear()
        
        if '.' in self.ausgabename[-5:]:# in dieser Verzweigung werden evtl. angefügt Dateiendungen(wie .xlsx) wieder entfernt, da diese später automatisch angehangen werden
            ind = -self.ausgabename.rfind('.')
            self.ausgabename = self.ausgabename[:ind - 1]
        self.textBrowser_2.setText(str(self.ausgabename))

        
    def weiter(self):
        self.ausgabename = self.textBrowser_2.toPlainText()
        self.close()

     

app = QtCore.QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
Speicherfenster = SpeicherFenster()
app.exec_()
# =============================================================================
#  Abschnitt 4
# Aufruf der Verarbeitungsroutine für Masta oder Simpack(je nach Auswahl)
# =============================================================================

if Auswahl.masta_button.isChecked():
    from Datenverarbeitung_masta import *

if Auswahl.simpack_button.isChecked():
    from Datenverarbeitung_simpack_neu import *