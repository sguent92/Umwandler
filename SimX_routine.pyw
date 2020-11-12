
if __name__!= '__main__':
    from __main__ import *
  
    

import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5 import QtCore  
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from scipy.fftpack import fft
from scipy import interpolate
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------
# =============================================================================
#Fenster zur Abfrage der Anzahl der Lastpunkte
# =============================================================================
class AuswahlFenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.initMe()
        
    def initMe(self):
               
        self.setGeometry(400,400,400,200)
        
        self.Auswahl = QtWidgets.QSpinBox(self)# Sinbox mit der Anzahl der eingelesenen Datein (Lastpunkt) ausgewält wird
        self.Auswahl.setGeometry(QtCore.QRect(250,70,35,50))
        self.Auswahl.setMinimum(3)
        
        self.Beschreibung =QtWidgets.QLabel(self)
        self.Beschreibung.setGeometry(QtCore.QRect(20,5,400,40))
        self.Beschreibung.setText('Wählen Sie aus wieviele Dokumente bzw. Lastpunkte Sie einlesen möchten.')
        self.l = QtWidgets.QLabel(self)
        self.l.setGeometry(QtCore.QRect(125,80,120,30))
        self.l.setText('Anzahl der Lastpunkte:')
        self.best = QPushButton('Bestätigen', self)
        self.best.setGeometry(QtCore.QRect(300,145,80,30))
        self.best.clicked.connect(self.weiter)
        self.show()
        
    def weiter(self):
        if self.Auswahl.value() != 0:
            self.datei_zahl = self.Auswahl.value()
            self.close()
        
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
    
Auswahl = AuswahlFenster()
app.exec_()

#------------------------------------------------------------------------------
#Fenster ermöglicht einlesen der der Dateinamen(und Pfade)
class MultiLadeFenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.initMe()
        
    def initMe(self):
         
        
        self.setGeometry(350,50,550,200 + Auswahl.datei_zahl * 80)
        self.setWindowTitle('Ladedialog')
        
        self.T1 = QtWidgets.QLabel(self)
        self.T1.setGeometry(QtCore.QRect(50, 5, 510 , 50))
        self.T1.setText('Bitte Laden Sie alle Dokumente, welche die Daten für die jeweiligen Lastpunkte enthalten.')


        self.dateiname = {}# dictionary auf das später die Namen (mit Pfad) aller geladenen Datein geschrieben werden
        
        for i in range(0,Auswahl.datei_zahl ):# in dieser Schleife werden für jeden Lastpunkt ein Button "Durchsuchen ein Label und ein Textbrowser erstellt"
            self.button =QPushButton('Durchsuchen', self)
            self.button.setGeometry(QtCore.QRect(120,112 + i* 80,150,30))
            self.button.setObjectName('Button' + str(i))
            self.findChild(QPushButton, 'Button' + str(i)).clicked.connect(self.laden)
            
            self.label = QtWidgets.QLabel('Lastpunkt ' + str(i+1) + ':', self)
            self.label.setGeometry(QtCore.QRect(55,80 +i* 80,80,30))
            self.label.setObjectName('Label' + str(i))
            
            self.T =QtWidgets.QTextBrowser(self)
            self.T.setGeometry(QtCore.QRect(120,80 + i* 80,360,32))
            self.T.setObjectName('Text' + str(i))        
        # Schleife erstellt Elemente in gewünchter Anzahl    
        
        self.weiter = QPushButton('Weiter', self)
        self.weiter.setGeometry(QtCore.QRect(400, 150 + Auswahl.datei_zahl * 80, 90,30))
        self.weiter.clicked.connect(self.close)
        self.show()
        
    def laden(self):#
        index = self.sender().objectName()[-1]# holt index des gedrückten buttons 
        
        self.dateiname[int(index)] = QtWidgets.QFileDialog.getOpenFileName(self, 'Datei öffnen', 'C:\\')[0]#schreibt Name der geladenen Datei in dictionary
        self.findChild(QtWidgets.QTextBrowser, 'Text' + index).clear() # leert zugehörigen Textbrowser
        self.findChild(QtWidgets.QTextBrowser, 'Text' + index).append(str(self.dateiname[int(index)]))   # schreibt Name der geladenen Datei in Textbrowser
        


        
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
    
Lade = MultiLadeFenster()

app.exec_()


# =============================================================================
# Laden der ausgewählten Dokumente und Sortieren nach Lastpunkt (Drehzahl)
# =============================================================================

def tab_lesen(name): # auslelefunktion für eine csv oder Exceldatei
    dtyp = name[name.rfind('.'):]

    if dtyp == '.csv':
        spalten_namen = [i for i in range (0,1200)]# vordefinition der Spaltennamen, wird das nicht getan erhält mann einen Error wenn die Anzahl der elemente in einer Zeile größer ist als in der ersten Zeile
        df =  pd.read_csv(name, delimiter=';', engine = 'python', nrows=1)
        if len(df.iloc[0][:]) == 1:
            df =  collections.OrderedDict([('1' , pd.read_csv(name, delimiter=',', engine = 'python',skip_blank_lines = False , names = spalten_namen))])# csv wird eingelesen und auf orderedDict gelegt # liest csv auf dataframe df
        
        else:
            df =  collections.OrderedDict([('1' , pd.read_csv(name, delimiter=';', engine = 'python',skip_blank_lines = False , names = spalten_namen))])# csv wird eingelesen und auf orderedDict gelegt
    
    else:
        df =  pd.read_excel(name, sheet_name = None, header = None)
        
    df_neu = {}# die Schlüssel des dictionarys mit den geladenen Daten werden durch Zahlen 0 bis n ersetzt
    new_key = 0
    for key in df:
        df_neu[new_key] = df[key]
        new_key += 1
    return df_neu
#------------------------------------------------------------------------------
        
def erweitertes_Auslesen(eingabestring, suchstring): # sucht mit in Kerndaten abgelegten suchstring nach den jeweiligen Daten und gibt Sie aus
    if (isinstance(eingabestring, str)) & (eingabestring != ''):# prüft ob eingegebener Wert überhaut ein string ist
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
#------------------------------------------------------------------------------
        
df_list_unsortiert=[]
for key in Lade.dateiname: # lädt ausgelesene Daten auf Liste
    df_list_unsortiert.append(tab_lesen(Lade.dateiname[key])) 
    
df_dict = {} # ab hier werden die geladenen Daten nach den Lastpunkten sortiert           
reihenfolge = sorted(df_list_unsortiert, key = (lambda a : int(erweitertes_Auslesen(a[int(Kerndaten['Lastpunkt'][0])].iloc[int(Kerndaten['Lastpunkt'][1]) - 1, int(Kerndaten['Lastpunkt'][2]) - 1], Kerndaten['Lastpunkt'][3]))))  
for i in range(len(reihenfolge)):  
    df_dict[i] = reihenfolge[i]

# =============================================================================
# Die Kerndaten werden von den einzelnen Datein ausgelesen und auf "Kerndatenliste abgelegt"
# =============================================================================

V_Err = False

Kerndatenliste = []         
for key in df_dict:
    lp = {}
    try:
        lp['Motordrehzahl'] = df_dict[key][int(Kerndaten['Lastpunkt'][0])].iloc[int(Kerndaten['Lastpunkt'][1]) - 1, int(Kerndaten['Lastpunkt'][2]) - 1]#df[df_dict[].iloc[int(Kerndaten['Lastpunkt'][1]) - 1][int(Kerndaten['Lastpunkt'][2]) - 1]
        lp['zahn_zahl'] = df_dict[key][int(Kerndaten['zaehne'][0])].iloc[int(Kerndaten['zaehne'][1]) - 1, int(Kerndaten['zaehne'][2]) - 1]
        lp['slice_zahl'] = df_dict[key][int(Kerndaten['slices'][0])].iloc[int(Kerndaten['slices'][1]) - 1, int(Kerndaten['slices'][2]) - 1]
        lp['Wink_Aufl'] =  float(df_dict[key][int(Kerndaten['Winkel'][0])].iloc[int(Kerndaten['Winkel'][1]) - 1, int(Kerndaten['Winkel'][2]) - 1])
            
        lp['Motordrehzahl'] = int(erweitertes_Auslesen(lp['Motordrehzahl'], Kerndaten['Lastpunkt'][3]))     
        lp['zahn_zahl'] = int(erweitertes_Auslesen(lp['zahn_zahl'], Kerndaten['zaehne'][3]))
        lp['slice_zahl'] = int(erweitertes_Auslesen(lp['slice_zahl'], Kerndaten['slices'][3]))
        
        
        
    except ValueError:
        V_Err = True   
    Kerndatenliste.append(lp)

# =============================================================================
# Kerndaten werden untereinander auf übereinstimmung geprüft
# =============================================================================
abweichende_werte = False    
for i in range(0,len(Kerndatenliste)-1):
    if (Kerndatenliste[i]['zahn_zahl'] != Kerndatenliste[i+1]['zahn_zahl']) |(Kerndatenliste[i]['slice_zahl'] != Kerndatenliste[i+1]['slice_zahl']) | (Kerndatenliste[i]['Wink_Aufl'] != Kerndatenliste[i+1]['Wink_Aufl']):
        abweichende_werte = True
zahn_zahl = Kerndatenliste[i]['zahn_zahl']
slice_zahl = Kerndatenliste[i]['slice_zahl']
Wink_Aufl = Kerndatenliste[i]['Wink_Aufl']


Lastpunkt_dict = {}
for i in range(0,len(Kerndatenliste)):
    Lastpunkt_dict[i] = Kerndatenliste[i]['Motordrehzahl']

# =============================================================================
# 
# =============================================================================

laenge = int(360/Wink_Aufl)

Datenbloecke = {}# OrderedDict auf dem DataFrames sämltlicher Blöcke mit den Daten für die Kräfte und Momente abgelegt werden

for Datei in df_dict:
    ad = {}
    for key in Arbeitsdaten:
        einzelblock = pd.DataFrame([])

        for i in range(0,(int(len(Arbeitsdaten[key])/5))):# ein durchlauf pro Block der jeweiligen Kraft/ des Moments (jeder Block hat 5 einträge in "Arbeitsdaten")
            az= int(Arbeitsdaten[key][1 + i * 5]) - 1# az anfangszeile
            ez = az + laenge #int(Arbeitsdaten[key][3 + i * 5])#endzeile
            asp = int(Arbeitsdaten[key][2 + i * 5]) - 1 #anfangsspalte
            esp = asp + int(Arbeitsdaten[key][4 + i * 5])#endspalte
            einzelblock = pd.concat([einzelblock, df_dict[Datei][int(Arbeitsdaten[key][0])].iloc[az : ez , asp : esp ]], axis = 1)# wenn mehr als ein Block vorhanden werden diese verknüpft
        einzelblock = einzelblock.reset_index(drop = True)# index wird auf standart (zahle 0 bis n) zurück gesetzt
        einzelblock.columns = range(einzelblock.shape[1])# spaltenindexe werden zurückgesetzt
        
        try:
            einzelblock = einzelblock.astype(float)# convertiert erste Spalte zu float
        except KeyError:
            pass
        einzelblock = einzelblock.dropna(axis = 1)# entfernt leere Spalten
        ad[key] = einzelblock# einzelne Bloecke werden auf OrderedDict geschrieben, leere Spalten werden entfernt

    Datenbloecke[Datei] = ad

#Auslesen und Prüfen relevanter Daten
#indz = 3
#inds = 5
#indl = 8
#Lastpunkt_dict = {}
##zahnbereich = [i for i in range(16,100)]
##slicebereich = [i for i in range(1,16)]
##Lastbereich = [i for i in range(100-20000)]
#
#zahn_zahl = df_dict[1].iloc[indz][1]
#slice_zahl = df_dict[1].iloc[inds][1]
#Lastpunkt_dict[1]= df_dict[1].iloc[indl][1]
#Wink_Aufl = float(df_dict[1].iloc[20][0]) - float(df_dict[1].iloc[19][0])
#for i in range(2,Auswahl.datei_zahl+1):
#    testz= df_dict[i].iloc[indz][1]         
#    tests = df_dict[i].iloc[inds][1]   
#    testw = float(df_dict[i].iloc[20][0]) - float(df_dict[i].iloc[19][0])
#    
#    Lastpunkt_dict[i]= df_dict[i].iloc[indl][1]
#    if (testz != zahn_zahl) |(tests != slice_zahl) | (testw != Wink_Aufl):
#        abweichende_werte = True

# =============================================================================
# Fenster zeigt ausgelesene Daten und Ergebnisse des Datenabgleiches, gibt Möglichkeit manuelle Dateneinlese zu aktivieren
# =============================================================================
class DatenFenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.initMe()
        
    def initMe(self):      
        
        
        self.setGeometry(350,350,400,400)
        self.setWindowTitle('Datenüberprüfung')
  
            
        self.l2 = QtWidgets.QLabel(self)
        self.l2.setGeometry(QtCore.QRect(45, 5, 310, 40))
        if (abweichende_werte == False) & (V_Err == False):
            self.l2.setText('  -> Anzahl Zähne, Anzahl Slices und Winkelauflösung\n     für alle Dokumente identisch.')
            self.l2.setStyleSheet("background-color: lightgreen")
        elif (abweichende_werte == True) & (V_Err == False):
            self.l2.setText(' !!Ausgelesende Werte weichen voneinander ab!!')
            self.l2.setStyleSheet("background-color: red ; font: bold")
        elif V_Err == True:
            self.l2.setText(' !!Fehler beim Auslesen der Kerndaten!!')
            self.l2.setStyleSheet("background-color: red; font: bold")
            
        try:
            self.l3 = QtWidgets.QLabel(self)
            self.l3.setGeometry(QtCore.QRect(60, -20, 351, 285))
            self.l3.setText('Bitte prüfen Sie die eingelesenen Daten\n\nAnzahl der Zähne:\t' + str(zahn_zahl)
            + '\nAnzahl der Slices:\t' + str(slice_zahl) + '\nWinkelauflösung:\t' + str(Wink_Aufl))
            
        except NameError:
            self.l3 = QtWidgets.QLabel(self)
            self.l3.setGeometry(QtCore.QRect(60, -20, 351, 285))
            self.l3.setText('Bitte prüfen Sie die eingelesenen Daten\n\nAnzahl der Zähne:\t' + ''
            + '\nAnzahl der Slices:\t' + '' + '\nWinkelauflösung:\t' + '')
        
        self.l4 = QtWidgets.QLabel(self)
        self.l4.setGeometry(QtCore.QRect(60, 135, 551, 160))
        text_l4 = ''
        
        doppelt = False
        for i in range(0,Auswahl.datei_zahl):
            text_l4 = text_l4 + '\t' + str(Lastpunkt_dict[i]) + ' rpm\n' + '\t'
            if (i > 0): 
                if (Lastpunkt_dict[i] == Lastpunkt_dict[i-1]):
                    doppelt = True
                    
        self.l4.setText('\nLastpunkte:' + text_l4 + '\n\n' + '\nSind die eingelesenen Daten korrekt?')
        
        self.l1 = QtWidgets.QLabel(self)
        self.l1.setGeometry(QtCore.QRect(45, 40, 310, 30))
        if doppelt == False:
            self.l1.setText("  -> Keine Doppeleinträge gefunden.")
            self.l1.setStyleSheet("background-color: lightgreen")
        else:
            self.l1.setText(' !!Doppeleinträge gefunden. Bitte Lastpunkte prüfen!!')
            self.l1.setStyleSheet("background-color: red; font: bold")
        
        
        button = QtWidgets.QPushButton('Manuelle Eingabe' , self)
        button.setGeometry(QtCore.QRect(192, 330, 120, 23))
        button.setObjectName('1')
        button.clicked.connect(self.weiter_gehts)

        
        button2 = QPushButton('Daten sind korrekt', self)
        button2.setGeometry(QtCore.QRect(55, 330, 120, 23))
        button2.setObjectName('0')
        button2.clicked.connect(self.weiter_gehts)#
        self.show()
        
    def weiter_gehts(self):#
        
        self.manuell = False
        if self.sender().objectName() == '1':
            self.manuell = True
        self.close()

app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
    
Datenüberprüfung = DatenFenster()
    
app.exec_()
#------------------------------------------------------------------------------
# manuelles Einlesen der Daten
Fehler = Datenüberprüfung.manuell

if Fehler == True:
    class EinleseFenster(QWidget):
        def __init__(self): 
            super().__init__()
            self.initMe()
            
        def initMe(self):
            
            
            if Auswahl.datei_zahl > 3:
                faktor = Auswahl.datei_zahl - 3
            else:
                faktor = 0
                
            self.setGeometry(50,50,600 ,270 + faktor * 50)
            self.setWindowTitle('Einlesefenster')
    
            self.TZaehne = QtWidgets.QLineEdit(str(zahn_zahl),self)
            self.TZaehne.setGeometry(QtCore.QRect(130, 40, 121, 31))
            self.TZaehne.setValidator(QIntValidator())
            
            self.TSlices = QtWidgets.QLineEdit(str(slice_zahl),self)
            self.TSlices.setGeometry(QtCore.QRect(130, 90, 121, 31))
            self.TSlices.setValidator(QIntValidator())    
    
            self.TWinkel = QtWidgets.QLineEdit(str(Wink_Aufl), self)
            self.TWinkel.setGeometry(QtCore.QRect(130, 140, 121, 31))    
            
            self.label = QtWidgets.QLabel(self)
            self.label.setText("Anzahl der Zähne")
            self.label.setGeometry(QtCore.QRect(30, 40, 101, 20))
            self.label.setObjectName("label")
            self.label_2 = QtWidgets.QLabel(self)
            self.label_2.setText("Anzahl der Slices")
            self.label_2.setGeometry(QtCore.QRect(30, 90, 101, 20))
            self.label_2.setObjectName("label_2")
    
            self.label_4 = QtWidgets.QLabel(self)
            self.label_4.setText('Winkelauflösung')
            self.label_4.setGeometry(QtCore.QRect(30, 140, 80, 20))
            self.label_4.setObjectName("label_4")
            self.label_5 = QtWidgets.QLabel(self)
    
            self.label_6 = QtWidgets.QLabel(self)
            self.label_6.setText('°')
            self.label_6.setGeometry(QtCore.QRect(260, 142, 21, 20))
            self.label_6.setObjectName("label_6")
            button = QtWidgets.QPushButton('Weiter', self)
            button.setGeometry(QtCore.QRect(480, 230 + faktor * 50, 75, 23))
            button.setObjectName("pushButton")
            button.clicked.connect(self.setze)
    
            
            for i in range (0,Auswahl.datei_zahl):
                self.last = QtWidgets.QLabel('Lastpunkt von Datei ' + str(i), self)
                self.last.setGeometry(QtCore.QRect(310,40 + i * 50,120,30))
    
                self.TLastpunkt = QtWidgets.QLineEdit(self)
                self.TLastpunkt.setGeometry(QtCore.QRect(430, 40+ i * 50, 121, 31)) 
                self.TLastpunkt.setObjectName('Lastpunkt' + str(i))
                self.TLastpunkt.setValidator(QIntValidator())
                
                           
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
            
            self.Lastpunkt_dict = {}
            for i in range(0, Auswahl.datei_zahl):
                self.Lastpunkt_dict[i] = int(self.findChild(QtWidgets.QLineEdit, 'Lastpunkt' + str(i)).text())
            self.close()
            
    #app = QApplication(sys.argv)
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    
    Einlesefenster = EinleseFenster()
    
    app.exec_()
    
    zahn_zahl = Einlesefenster.zahn_zahl
    slice_zahl = Einlesefenster.slice_zahl
    Wink_Aufl = Einlesefenster.Wink_Aufl
    Lastpunkt_dict = Einlesefenster.Lastpunkt_dict
#------------------------------------------------------------------------------
#ließt Name und Pfad der zu speichernden Dateien aus
class Fenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.initMe()
        
    def initMe(self):       
        
        self.setGeometry(50,50,700,250)
        self.setWindowTitle('Speicherdialog')
        
        self.l = QtWidgets.QLabel(self)
        self.l.setGeometry(QtCore.QRect(160, 30, 551, 51))
        self.l.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self)
        self.l.setText('Wo möchten Sie die Dateien speichern?')
        self.textBrowser_2.setGeometry(QtCore.QRect(160, 140, 451, 31))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Speicherort:")
        self.label.setGeometry(QtCore.QRect(60, 140, 101, 31))
        self.label.setObjectName("label")
        button = QtWidgets.QPushButton(" Fertig" , self)
        button.setGeometry(QtCore.QRect(540, 180, 75, 23))
        button.clicked.connect(self.close)
        button2 = QPushButton('Datei Speichern', self)
        button2.setGeometry(QtCore.QRect(160, 180, 121, 23))
        button2.clicked.connect(self.speichern)#
                
        self.show()
        
    def speichern(self):#

        self.ausgabename = QtWidgets.QFileDialog.getSaveFileName(self,'Dateien speichern', 'Ausgabe_SimulationX/')[0]
        
        if '.' in self.ausgabename:
             ind = self.ausgabename.rfind('.')
             self.ausgabename =self.ausgabename[:ind - 1]
             
        self.textBrowser_2.clear()
        self.textBrowser_2.append(self.ausgabename)


        
#app = QApplication(sys.argv)
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
Speicherfenster = Fenster()

app.exec_()

#------------------------------------------------------------------------------
# Erstellt Diagramm Moment über Winkel, einmal pro Lastpunkt

Winkelliste = np.array(([Wink_Aufl * i for i in range(0,laenge)]), dtype = float)
for key in Datenbloecke:
   
    Moment = np.array((Datenbloecke[key]['gesamt_moment']), dtype = float)
    Moment = np.reshape(Moment, len(Moment))
    
    f = open(Speicherfenster.ausgabename + '_Moment_über_Winkel_' + str(Lastpunkt_dict[key]) + 'rpm' + '.txt', "w")
    f.write('x[°]\ty[1][Nm]\n')
    
    for wink, mom in zip(Winkelliste, Moment):
        f.write(str(wink) + '\t' + str(mom) + '\n')
    f.close()

#start_dict = {}
#Moment_Winkel_dict = {}
#Moment_gesamt_dict =  {}
#for i in range(1, len(df_dict) + 1):
#    start_dict[i] = df_dict[i].iloc[:15][0][df_dict[i].iloc[:15][0] == '0'].index[0]
##    df.iloc[:20,0][df.iloc[:20,0] == ind_0].index[0]
#    
#    Winkel = df_dict[i].iloc[start_dict[i]:start_dict[i] + laenge][0]
#    Moment = df_dict[i].iloc[start_dict[i]:start_dict[i] + laenge][1]
#    Moment_Winkel_dict[i] = pd.concat([Winkel,Moment], axis = 1)
#    Moment_gesamt_dict[i]=df_dict[i].iloc[9][1]
#    
#
#    f = open(Speicherfenster.ausgabename + '_Moment_über_Winkel_' + Lastpunkt_dict[i]+ 'rpm' + '.txt', "w")
#    f.write('x[°]\ty[1][Nm]\n')
#    for zelle in zip(Moment_Winkel_dict[i][0], Moment_Winkel_dict[i][1]):
#        f.write(zelle[0] + '\t' + zelle[1] + '\n')
#    f.close()
 #-----------------------------------------------------------------------------
##Erstellt Kurve Moment über Drehzahl (Lastkennlinie versuch1)  
#f = open(ausgabename + '_Lastkennlinie.txt', 'w')
#f.write('x[rpm]\ty[1][Nm]\nrpm\tNm\n')  
#for i in range(0, len(Lastpunkt_dict)+ 1):
#    if i == 0:
#        f.write('0\t' + Moment_gesamt_dict[1] + '\n')
#    else:
#        f.write(Lastpunkt_dict[i] + '\t' + Moment_gesamt_dict[i] + '\n')
#f.close()
#------------------------------------------------------------------------------
# =============================================================================
# Erstellt 2D Kennfeld x= Winkel y=Lastpunkt z= Moment
# =============================================================================

Zeile1 = np.array([i * Wink_Aufl/180 * np.pi for i in range(0,laenge)], dtype = float)
Zeile1 = np.reshape(Zeile1, (-1,len(Zeile1)))
Zelle0 = np.reshape(np.array([0], dtype = float), (1,1))
Zeile1 = np.concatenate ((Zelle0, Zeile1), axis = 1)

Drehzahlen = np.array([Lastpunkt_dict[n]for n in Lastpunkt_dict], dtype = float)
Drehzahlen = np.reshape(Drehzahlen, (len(Drehzahlen),1))
Drehzahlen = np.concatenate((Zelle0, Drehzahlen), axis = 0)

momentenliste = [np.reshape(np.array(Datenbloecke[0]['gesamt_moment']), (1,laenge))]# Daten für ersten Lastpunkt werden doppelt geschreiben(einmal für Lastpunkt selbst und einmal für 0 rpm)
for key in Datenbloecke:
    m = np.array(Datenbloecke[key]['gesamt_moment']) # liest die Momente der jeweiligen Lastpunkte ein
    m = np.reshape(m, (1, len(m)))
    momentenliste.append(m)# schreibt alle moment arrays auf eine Liste
    
Momentenkennfeld = np.concatenate(momentenliste)# verbindet Liste zu einzigem Array
Momentenkennfeld = np.concatenate((Drehzahlen, Momentenkennfeld), axis = 1)# verbindet Momentdaten mit den Lastpunkten/ Drehzahlen
Momentenkennfeld = np.concatenate((Zeile1, Momentenkennfeld), axis = 0)# setzt Zeile 1 (mit den Winkeln in rad) oben drauf

pd.DataFrame(Momentenkennfeld).to_csv(Speicherfenster.ausgabename + '_2D_Diagramm.csv', index = False, header = False)# schreibt array in Csv datei


#Zeile1 =pd.concat([pd.DataFrame(['0']), pd.DataFrame([np.transpose(np.pi/180* np.array( Moment_Winkel_dict[1].iloc[:,0], dtype = float))])], axis = 1, ignore_index = True)
#Block = pd.DataFrame([])
#for i in range(1, len(Lastpunkt_dict) + 1):
#    
#    Zeile = pd.concat([pd.DataFrame([float(Lastpunkt_dict[i])*2*np.pi/60]), pd.DataFrame([np.transpose(np.array(Moment_Winkel_dict[i].iloc[:,1]))])], axis = 1)
#    Block =pd.concat([Block,Zeile], axis =0)
#    if i ==1:
#        Zeile = pd.concat([pd.DataFrame([float(Lastpunkt_dict[i])*2*np.pi/60]), pd.DataFrame([np.transpose(np.array(Moment_Winkel_dict[i].iloc[:,1]))])], axis = 1)
#        Block =pd.concat([Block,Zeile], axis =0)
#
#spalten = np.linspace(0,laenge,laenge+1, dtype = int)
#
#Block.columns = spalten
#
#Block = pd.DataFrame(Block, columns = None)
#Block = pd.concat([Zeile1,Block], axis = 0)
#index = np.linspace(0,len(Block)-1,len(Block), dtype = int)
#Block.index= index
#Block.loc[1][0]='0'
#
#Block.to_csv(Speicherfenster.ausgabename + '_2D_Diagramm.csv', index = False, header = False)

#------------------------------------------------------------------------------
# Erstellung der Lastkennlinie (Versuch 2)
Aufl = 400
#N = int((int(Lastpunkt_dict[len(Lastpunkt_dict)]) - int( Lastpunkt_dict[0]))/ Aufl)
if Vorlage.vorlagenname == 'G:/TS-X1/Studenten/2020_SGuenther_NVH/Umwandler/Vorlagen/JMAG.txt':
    Moment_gesamt_list = [float(df_dict[i][0].iloc[10,1]) for i in range(0, len(df_dict))]
else:
    Moment_gesamt_list = [float(Datenbloecke[i]['gesamt_moment'].mean(axis = 0)) for i in range(0, len(df_dict))]
     
#np.linspace(int(Lastpunkt_dict[1]),int(Lastpunkt_dict[len(Lastpunkt_dict)]) , int(N + 1) )

y = np.array([Moment_gesamt_list]).squeeze()
x = np.array([Lastpunkt_dict[i] for i in range(0, len(Lastpunkt_dict))])

intfunk = interpolate.interp1d(x,y,kind = 'quadratic', fill_value="extrapolate")

xneu = np.arange(int( Lastpunkt_dict[0]), int(Lastpunkt_dict[len(Lastpunkt_dict) - 1]) , Aufl)
xneu = np.array(sorted(np.append(xneu, x)))
xneu = np.unique(xneu)



yneu =np.transpose(intfunk(xneu))
yneu= np.append(yneu[0], yneu)
xneu= np.append(0, xneu)


f = open(Speicherfenster.ausgabename + '_Lastkennlinie.txt', 'w')
f.write('x[rpm]\ty[1][Nm]\nrpm\tNm\n')

for punkt in zip(xneu,yneu):
    f.write(str(punkt[0]) + '\t' + str(punkt[1]) + '\n')
f.close()
#------------------------------------------------------------------------------
def max_loc(A, referenzwert = None , prozent = 100): # ließt 1D array ein und gibt array mit den Positionen der lokalen Maxima aus
    m = []
    for i in range(1, len(A)-1):
        if (A[i] > A[i-1]) & (A[i] > A[i+1]):
            if referenzwert== None:
                 m = m + [i]
            elif (referenzwert != None) & (A[i]> referenzwert * (prozent/100)):
                m = m + [i]
    return m
#------------------------------------------------------------------------------
# erstellt Übersicht der Stärke der auftretenden Moden, sowie png Datei mit graphischer Auswertung der moden
N = laenge
file = open(Speicherfenster.ausgabename + '_torque_ripple_Tabelle.txt', 'w')
fig = plt.figure(figsize = (26, 20))

x = np.array([winkel * Wink_Aufl for winkel in range(0,laenge)], dtype = float)

for i in range(0,len(Lastpunkt_dict)):
    
    y = np.array(Datenbloecke[i]['gesamt_moment'], dtype = float) #np.array(df_dict[1].iloc[1454:1454+laenge,1], dtype = float)
    y_ripple = y - float(Moment_gesamt_list[i])
    
#    t = x/(360 * float(Lastpunkt_dict[i]))# zeit in min

#    t_end_min = 1/float(Lastpunkt_dict[i])
#    Tau = t_end_min/N
    f = np.arange(0,N) 

#    t_ft = np.arange(0,t_end_min, Tau)#np.linspace(0,f/float(Lastpunkt_dict[i])-1,N)
    y_ft = 1/N * np.abs(fft(y_ripple, axis = 0))
    y_ft_prozent = 100 *y_ft/float(Moment_gesamt_list[i])
    moden_pos= max_loc(y_ft,float(Moment_gesamt_list[i]),0.1)
    moden_ausgabestring = ''
    for mode in moden_pos:
        if mode < f[1:N//6][-1]:
            moden_ausgabestring = moden_ausgabestring + ' ' + str(mode) + ','
            
    moden_ausgabestring = moden_ausgabestring[:-1]
    plt.subplot(len(Lastpunkt_dict),3,1 + 3*(i))
    plt.title('Lastpunkt ' + str(i) +  ': ' + str(Lastpunkt_dict[i]) + 'rpm    Moment pro Winkel')
    plt.ylabel('Moment in Nm')
    plt.xlabel('Winkel in °')
    plt.plot(x,y)
    
    plt.subplot(len(Lastpunkt_dict),3,2 + 3*(i))
    plt.title('Lastpunkt ' + str(i) +  ': ' + str(Lastpunkt_dict[i]) + 'rpm    Torque Ripple in %')
    plt.grid()
    plt.ylabel('Anteil der Moden in %')
    plt.xlabel('Modenspektrum  --  relevante Moden bei:' + moden_ausgabestring)
    plt.plot(f[1:N//6],y_ft_prozent[1:N//6], c = 'g')

    
    plt.subplot(len(Lastpunkt_dict),3,3 + 3*(i))
    plt.title('Lastpunkt ' + str(i) +  ': ' + str(Lastpunkt_dict[i]) + 'rpm    Torque Ripple in Nm')
    plt.grid()
    plt.ylabel('Anteil der Moden in Nm')
    plt.xlabel('Modenspektrum  --  relevante Moden bei:' + moden_ausgabestring)
    plt.plot(f[1:N//6],y_ft[1:N//6], c = 'r')   
  
    
    
    #Moden_Amplitude_List = []

    file.write('Lastpunkt:' + str(Lastpunkt_dict[i]) +' rpm\t' + 'Moment gesamt: ' + str(Moment_gesamt_list[i]) + ' Nm\n\n')
    file.write('Mode\tAmplitude in %\t        Amplitude in Nm\n')
    for i2 in moden_pos[:len(moden_pos)//2]:
        
        file.write(str(i2) + '\t' + str(y_ft_prozent[i2].squeeze()) + '\t' + str(y_ft[i2].squeeze()) + '\n')
        #Moden_Amplitude_List.append((i,y_ft_prozent[i]))
    file.write('\n\n')
file.close()
plt.savefig(Speicherfenster.ausgabename + '_torque_ripple_Übersicht.png')
    
# =============================================================================
# Ausgabefenster für Plot
# =============================================================================

class AusgabeFenster(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.scroll = QScrollArea()             
        self.widget = QWidget()            
        self.vbox = QVBoxLayout()            

        Bild = QLabel(self)
        Bild.setPixmap(QPixmap(Speicherfenster.ausgabename + '_torque_ripple_Übersicht.png'))
                
        self.vbox.addWidget(Bild)

        self.widget.setLayout(self.vbox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        self.showMaximized()
        
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
Ausgabe = AusgabeFenster()

app.exec_()
