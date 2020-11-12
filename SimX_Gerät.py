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
        
        self.Beschreibung =QtWidgets.QLabel(self)
        self.Beschreibung.setGeometry(QtCore.QRect(20,5,400,40))
        self.Beschreibung.setText('Wählen Sie aus wieviele Dokumente bzw. Lastpunkt Sie einlesen möchten.')
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
        
        for i in range(1,Auswahl.datei_zahl + 1):# in dieser Schleife werden für jeden Lastpunkt ein Button "Durchsuchen ein Label und ein Textbrowser erstellt"
            self.button =QPushButton('Durchsuchen', self)
            self.button.setGeometry(QtCore.QRect(120,32 + i* 80,150,30))
            self.button.setObjectName('Button' + str(i))
            self.findChild(QPushButton, 'Button' + str(i)).clicked.connect(self.laden)
            
            self.label = QtWidgets.QLabel('Lastpunkt ' + str(i) + ':', self)
            self.label.setGeometry(QtCore.QRect(55,i* 80,80,30))
            self.label.setObjectName('Label' + str(i))
            
            self.T =QtWidgets.QTextBrowser(self)
            self.T.setGeometry(QtCore.QRect(120,i* 80,360,32))
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
    
Ladefenster = MultiLadeFenster()

app.exec_()

#------------------------------------------------------------------------------
# Laden der ausgewählten Dokumente und Prüfung der Dimensionen der Dateien

df_dict={}# prä allokation für Dictionary die geladenen Datein komplett als DataFrames gelegt werden
abweichende_df = False #gibt an ob die Datein unterschiedlich lang sind

for key in Ladefenster.dateiname:# schlüüsel/key 1 bis n rufen die Namen(mit Pfad) der zu ladenden Datein auf 
    
    df =  pd.read_csv(Ladefenster.dateiname[key], delimiter=';', engine = 'python', nrows=1) #prüft anzahl Einträge in erster Zeile
    if len(df.iloc[0][:]) == 1:
        spalten_namen = [i for i in range (0,1200)] # definiert Spaltennamen 0 bis 1200 für erstellten DataFrame da ".read_csv" sonst Fehler ausgibt wenn die Anzahl der Einträge in unteren Zeilen die der Einträge in der ersten Zeile überschreitet
        df_dict[key] =  pd.read_csv( Ladefenster.dateiname[key],  engine = 'python' , header = None, names = spalten_namen, skip_blank_lines = False) # liest csv auf dataframe df und legt es mit Schlüssel 1 bis n in dictionary df_dict
    else:
        df_dict[key] =  pd.read_csv( Ladefenster.dateiname[key], delimiter = ';', engine = 'python', header = None)
        
for i in range(1,Auswahl.datei_zahl): # vergleicht die länge der eingelesenen DataFrames 
    if (len(df_dict[i]) > len(df_dict[i + 1]) + 10) | (len(df_dict[i]) < len(df_dict[i + 1]) - 10):
        abweichende_df = True
        
        
#------------------------------------------------------------------------------
#
#def search_df(df, suchobj): # Minifunktion die suchen nach Indexen
#    return df[df == suchobj].index[0]
#----------------------------------------------------------------------
#Auslesen und Prüfen relevanter Daten
abweichende_werte = False
indz = 3
inds = 5
indl = 8
Lastpunkt_dict = {}
#zahnbereich = [i for i in range(16,100)]
#slicebereich = [i for i in range(1,16)]
#Lastbereich = [i for i in range(100-20000)]

zahn_zahl = df_dict[1].iloc[indz][1]
slice_zahl = df_dict[1].iloc[inds][1]
Lastpunkt_dict[1]= df_dict[1].iloc[indl][1]
Wink_Aufl = float(df_dict[1].iloc[20][0]) - float(df_dict[1].iloc[19][0])
for i in range(2,Auswahl.datei_zahl+1):
    testz= df_dict[i].iloc[indz][1]         
    tests = df_dict[i].iloc[inds][1]   
    testw = float(df_dict[i].iloc[20][0]) - float(df_dict[i].iloc[19][0])
    
    Lastpunkt_dict[i]= df_dict[i].iloc[indl][1]
    if (testz != zahn_zahl) |(tests != slice_zahl) | (testw != Wink_Aufl):
        abweichende_werte = True
#------------------------------------------------------------------------------
# Fenster zeigt ausgelesene Daten und Ergebnisse des Datenabgleiches, gibt Möglichkeit manuelle Dateneinlese zu aktivieren
class DatenFenster(QWidget):
    def __init__(self): 
        super().__init__()
        self.initMe()
        
    def initMe(self):      
        
        
        self.setGeometry(350,350,400,400)
        self.setWindowTitle('Ladedialog')
        self.l1 = QtWidgets.QLabel(self)
        self.l1.setGeometry(QtCore.QRect(45, 5, 310, 30))
        if abweichende_df == False:
            self.l1.setText("  -> Keine Fehler beim Abgleich der Dokumente.")
            self.l1.setStyleSheet("background-color: lightgreen")
        else:
            self.l1.setText(' !!Dimensionen der Dokumente stimmen nicht überein!!')
            self.l1.setStyleSheet("background-color: red; font: bold")  
            
        self.l2 = QtWidgets.QLabel(self)
        self.l2.setGeometry(QtCore.QRect(45, 35, 310, 40))
        if abweichende_werte == False:
            self.l2.setText('  -> Anzahl Zähne, Anzahl Slices und Winkelauflösung\n     für alle Dokumente identisch.')
            self.l2.setStyleSheet("background-color: lightgreen")
        else:
            self.l2.setText(' !!Ausgelesende Werte weichen voneinander ab!!')
            self.l2.setStyleSheet("background-color: red ; font: bold")
        
        self.l3 = QtWidgets.QLabel(self)
        self.l3.setGeometry(QtCore.QRect(60, -20, 351, 285))
        self.l3.setText('Bitte prüfen Sie die eingelesenen Daten\n\nAnzahl der Zähne:\t' + str(zahn_zahl)
        + '\nAnzahl der Slices:\t' + str(slice_zahl) + '\nWinkelauflösung:\t' + str(Wink_Aufl))
        
        self.l4 = QtWidgets.QLabel(self)
        self.l4.setGeometry(QtCore.QRect(60, 135, 551, 160))
        text_l4 = ''
        for i in range(1,Auswahl.datei_zahl+1):
            text_l4 = text_l4 + '\t' + str(Lastpunkt_dict[i]) + ' rpm\n' + '\t'
        self.l4.setText('\nLastpunkte:' + text_l4 + '\n\n' + '\nSind die eingelesenen Daten korrekt?')
        
        
        button = QtWidgets.QPushButton('Manuelle Eingabe' , self)
        button.setGeometry(QtCore.QRect(192, 330, 120, 23))
        button.clicked.connect(self.call_manuell)
        button.released.connect(self.close)
        button2 = QPushButton('Daten sind korrekt', self)
        button2.setGeometry(QtCore.QRect(55, 330, 120, 23))
        button2.clicked.connect(self.close)#
        global Fehler
        Fehler = False
        self.show()
        
    def call_manuell(self):#
        
        Fehler = True
        
#app = QApplication(sys.argv)
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)

Datenüberprüfung = DatenFenster()

app.exec_()
#------------------------------------------------------------------------------
# manuelles Einlesen der Daten
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
            self.setWindowTitle('Ladedialog')
    
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
    
            
            for i in range (1,Auswahl.datei_zahl+1):
                self.last = QtWidgets.QLabel('Lastpunkt von Datei ' + str(i), self)
                self.last.setGeometry(QtCore.QRect(310,40 + (i - 1) * 50,120,30))
    
                self.TLastpunkt = QtWidgets.QLineEdit(self)
                self.TLastpunkt.setGeometry(QtCore.QRect(430, 40+ (i - 1) * 50, 121, 31)) 
                self.TLastpunkt.setObjectName('Lastpunkt' + str(i))
                self.TLastpunkt.setValidator(QIntValidator())
                
                           
            self.show()
            
        def setze(self):
            zahn_zahl = int(self.TZaehne.text())
            
            slice_zahl = int(self.TSlices.text())
                          
    
            Aufl = self.TWinkel.text()
            if ',' in Aufl:
                Aufl = Aufl.replace(',','.')
            Wink_Aufl = float(Aufl)
            
            for i in range(1, Auswahl.datei_zahl + 1):
                Lastpunkt_dict[i] = int(self.findChild(QtWidgets.QLineEdit, 'Lastpunkt' + str(i)).text())
            
    
            
            self.close()
    #app = QApplication(sys.argv)
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    
    Datenüberprüfung = EinleseFenster()
    
    app.exec_()
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
        global ausgabename
        #ausgabename = QtWidgets.QFileDialog.getOpenFileName(self, 'Ordner wählen', 'C:\\')
        ausgabename = QtWidgets.QFileDialog.getSaveFileName(self)[0]
        self.textBrowser_2.clear()
        self.textBrowser_2.append(ausgabename)
        if '.' in ausgabename[::-1]:
             ind = -ausgabename[::-1].find('.')
             ausgabename =ausgabename[:ind - 1]


        
#app = QApplication(sys.argv)
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QtWidgets.QApplication(sys.argv)
Speicherfenster = Fenster()

app.exec_()

#------------------------------------------------------------------------------
# Erstellt Diagramm Moment über Winkel, einmal pro Lastpunkt
laenge = int(360/Wink_Aufl)
start_dict = {}
Moment_Winkel_dict = {}
Moment_gesamt_dict =  {}
for i in range(1, len(df_dict) + 1):
    start_dict[i] = df_dict[i].iloc[:15][0][df_dict[i].iloc[:15][0] == '0'].index[0]
#    df.iloc[:20,0][df.iloc[:20,0] == ind_0].index[0]
    
    Winkel = df_dict[i].iloc[start_dict[i]:start_dict[i] + laenge][0]
    Moment = df_dict[i].iloc[start_dict[i]:start_dict[i] + laenge][1]
    Moment_Winkel_dict[i] = pd.concat([Winkel,Moment], axis = 1)
    Moment_gesamt_dict[i]=df_dict[i].iloc[9][1]
    

    f = open(ausgabename + '_Moment_über_Winkel_' + Lastpunkt_dict[i]+ 'rpm' + '.txt', "w")
    f.write('x[°]\ty[1][Nm]\n')
    for zelle in zip(Moment_Winkel_dict[i][0], Moment_Winkel_dict[i][1]):
        f.write(zelle[0] + '\t' + zelle[1] + '\n')
    f.close()
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
# Erstellt 2D Kennfeld x= Winkel y=Lastpunkt z= Moment

Zeile1 =pd.concat([pd.DataFrame(['0']), pd.DataFrame([np.transpose(np.pi/180* np.array( Moment_Winkel_dict[1].iloc[:,0], dtype = float))])], axis = 1, ignore_index = True)
Block = pd.DataFrame([])
for i in range(1, len(Lastpunkt_dict) + 1):
    
    Zeile = pd.concat([pd.DataFrame([float(Lastpunkt_dict[i])*2*np.pi/60]), pd.DataFrame([np.transpose(np.array(Moment_Winkel_dict[i].iloc[:,1]))])], axis = 1)
    Block =pd.concat([Block,Zeile], axis =0)
    if i ==1:
        Zeile = pd.concat([pd.DataFrame([float(Lastpunkt_dict[i])*2*np.pi/60]), pd.DataFrame([np.transpose(np.array(Moment_Winkel_dict[i].iloc[:,1]))])], axis = 1)
        Block =pd.concat([Block,Zeile], axis =0)

spalten = np.linspace(0,laenge,laenge+1, dtype = int)

Block.columns = spalten

Block = pd.DataFrame(Block, columns = None)
Block = pd.concat([Zeile1,Block], axis = 0)
index = np.linspace(0,len(Block)-1,len(Block), dtype = int)
Block.index= index
Block.loc[1][0]='0'

Block.to_csv(ausgabename + '_2D_Diagramm.csv', index = False, header = False)

#------------------------------------------------------------------------------
# Erstellung der Lastkennlinie (Versuch 2)
Aufl = 400
N = (int(Lastpunkt_dict[len(Lastpunkt_dict)]) - int( Lastpunkt_dict[1]))/ Aufl
xneu = np.linspace(int(Lastpunkt_dict[1]),int(Lastpunkt_dict[len(Lastpunkt_dict)]) , int(N + 1) )
y = np.array([])
x = np.array([])
for i in range (1,len(Moment_gesamt_dict)+1):
    y = np.append(y, float(Moment_gesamt_dict[i]))
    x = np.append(x, float(Lastpunkt_dict[i]))
intfunk = interpolate.interp1d(x,y,kind = 'quadratic', fill_value="extrapolate")#
yneu =intfunk(xneu)
yneu= np.append(yneu[0], yneu)
xneu= np.append(0, xneu)


f = open(ausgabename + '_Lastkennlinie.txt', 'w')
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
N = len(Moment_Winkel_dict[1])
file = open(ausgabename + '_tourqe_ripple_Tabelle.txt', 'w')
fig = plt.figure(figsize = (30,5* len(Lastpunkt_dict)))

for i in range(1,len(Lastpunkt_dict)+1):
    
    y = np.array(Moment_Winkel_dict[i][1], dtype = float) #np.array(df_dict[1].iloc[1454:1454+laenge,1], dtype = float)
    y_ripple = y - float(Moment_gesamt_dict[i])
    x = np.array(Moment_Winkel_dict[i][0], dtype = float)
    t = x/(360 * float(Lastpunkt_dict[i]))
    t_end_min = 1/float(Lastpunkt_dict[i])
    T = t_end_min/N
    f = 1/T
    t_ft = np.linspace(0,f/float(Lastpunkt_dict[i])-1,N)
    y_ft = 1/N * np.abs(fft(y_ripple))
    y_ft_prozent = 100 *y_ft/float(Moment_gesamt_dict[i])
    moden_pos= max_loc(y_ft,float(Moment_gesamt_dict[i]),0.1)
    moden_ausgabestring = ''
    for mode in moden_pos:
        if mode < t_ft[1:N//6][-1]:
            moden_ausgabestring = moden_ausgabestring + ' ' + str(mode) + ','
            
    moden_ausgabestring = moden_ausgabestring[:-1]
    plt.subplot(len(Lastpunkt_dict),3,1 + 3*(i-1))
    plt.title('Lastpunkt ' + str(i) +  ': ' + Lastpunkt_dict[i] + 'rpm    Moment pro Winkel')
    plt.ylabel('Moment in Nm')
    plt.xlabel('Winkel in °')
    plt.plot(x,y)
    
    plt.subplot(len(Lastpunkt_dict),3,2 + 3*(i-1))
    plt.title('Lastpunkt ' + str(i) +  ': ' + Lastpunkt_dict[i] + 'rpm    Tourque Ripple in %')
    plt.grid()
    plt.ylabel('Anteil der Moden in %')
    plt.xlabel('Modenspektrum  --  relevante Moden bei:' + moden_ausgabestring)
    plt.plot(t_ft[1:N//6],y_ft_prozent[1:N//6], c = 'g')

    
    plt.subplot(len(Lastpunkt_dict),3,3 + 3*(i-1))
    plt.title('Lastpunkt ' + str(i) +  ': ' + Lastpunkt_dict[i] + 'rpm    Tourque Ripple in Nm')
    plt.grid()
    plt.ylabel('Anteil der Moden in Nm')
    plt.xlabel('Modenspektrum  --  relevante Moden bei:' + moden_ausgabestring)
    plt.plot(t_ft[1:N//6],y_ft[1:N//6], c = 'r')   
  
    
    
    #Moden_Amplitude_List = []

    file.write('Lastpunkt:' + Lastpunkt_dict[i] +' rpm\t' + 'Moment gesamt: ' + Moment_gesamt_dict[i] + ' Nm\n\n')
    file.write('Mode\tAmplitude in %\t        Amplitude in Nm\n')
    for i2 in moden_pos[:len(moden_pos)//2]:
        
        file.write(str(i2) + '\t' + str(y_ft_prozent[i2]) + '\t' + str(y_ft[i2]) + '\n')
        #Moden_Amplitude_List.append((i,y_ft_prozent[i]))
    file.write('\n\n')
file.close()
plt.savefig(ausgabename + '_tourqe_ripple_Übersicht.png')
    

