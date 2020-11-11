from qtpy.QtWidgets import QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QTextBrowser, QApplication, QRadioButton, QCheckBox, QSpinBox, QMessageBox , QVBoxLayout, QPlainTextEdit, QFileDialog
from qtpy import QtCore
from qtpy.QtGui import QIcon, QPixmap, QIntValidator
import sys
import pandas as pd
from os import path



class HilfeFenster(QWidget):
    
    def __init__(self, Dateiname):
        super().__init__()

        vbox = QVBoxLayout()
        HilfBild = QLabel(self)
        HilfBild.setPixmap(QPixmap(Dateiname))
        vbox.addWidget(HilfBild)
        self.setLayout(vbox)
        self.move(200,200)
        
        



class InfoFenster(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initMe()
        
    def initMe(self):
        self.setGeometry(400,400,450,200)
        l = QLabel(self)
        l. move(20,10)
        l.setText("""Bitte öffnen Sie die Datei, anhand welcher die Vorlage erstellt werden soll, auf Excel.

Sie können durch Klicken auf dieses Symbol -->
jederzeit die Hilfe zum aktuellen Arbeitsschritt aufrufen.

Sollten Sie das Program zum ersten Mal verwenden,
wird empfohlen jetzt auf das Hilfesymbol zu drücken.""")
        
        frage = QPushButton(self)
        frage.setIcon(QIcon("bilder_vorlagenersteller\\FrageIcon.png"))
        frage.move(250,27)
        frage.clicked.connect(self.Hilfe)
        
        b = QPushButton('Weiter', self)
        b.move(350,150)
        b.clicked.connect(self.close)
        
        self.show()
        
    def Hilfe(self):
        self.h = HilfeFenster("bilder_vorlagenersteller\\erste_schritte.png")
        self.h.show()
        
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
info = InfoFenster()
info.show()
app.exec_()
        

        
# =============================================================================

# =============================================================================
class ZusatzFensterKerndaten(QWidget):
    
    def __init__(self,nummer,text):
        super().__init__()
        self.initMe(nummer, text) 
        
    def initMe(self,nummer, text):
        self.l1 = QLabel(self)
        self.l1.setText('Inhalt der eingelesenen Zelle')
        self.l1.move(20,5)
        
        self.nummer = nummer
        self.setGeometry(400,300,500,700)
        self.zelle = QPlainTextEdit(self)
        self.zelle.setGeometry(0,40,500,250)
        self.zelle.setPlainText(text)
        self.zelle.setReadOnly(True)
        
        self.l2 = QLabel(self)
        self.l2.setText("""Bitte geben Sie hier den Wert ein nach dem in der Zelle gesucht werden soll.
Bsp. Wollen Sie einen Lastpunkt auslesen, welcher mit 5000 rpm angegeben ist, geben Sie 5000 ein.
Achtung: keine Einheiten mit angeben. Nur Zahlen!""")
        self.l2.move(10,330)
        
        self.eing = QLineEdit(self)
        self.eing.move(10,410)

        p = QPushButton('Prüfen', self)
        p.clicked.connect(self.pruefen)
        p.move(180,409)
        
        self.l3 = QLabel(self)
        self.l3.setText('vorangehende Zeichenkette')
        self.l3.move(10,460)
        
        self.suchstring = QLineEdit(self)
        self.suchstring.move(180,459)
        self.suchstring.setDisabled(True)
        
        
        self.l5 = QLabel(self)
        self.l5.setStyleSheet("background-color: yellow")
        self.l5.setText("Prüfen Sie die vorrangehende Zeichenkette.\nSollte diese nicht stimmen, können Sie selbst eine angeben und erneut prüfen.\nAchtung: Leerzeichen nicht vergessen ")
        self.l5.move(10,490)
        self.l5.setVisible(False)
        
        self.l4 = QLabel(self)
        self.l4.setText('gefundener Eintrag')
        self.l4.move(10, 540)
        
        self.gefundener_string = QLineEdit(self)
        self.gefundener_string.move(180, 539)
        self.gefundener_string.setReadOnly(True)
        
        frage = QPushButton(self)
        frage.setIcon(QIcon("bilder_vorlagenersteller\\FrageIcon.png"))
        frage.move(450, 10)
        frage.clicked.connect(self.Hilfe)
        
        self.weiter = QPushButton('Weiter', self)
        self.weiter.move(420, 650)
        self.weiter.setDisabled(True)
        self.weiter.clicked.connect(self.weiter_gehts)
    
    def suchstring_finden(self):
        startindex = self.zelle.toPlainText().find(self.eing.text())
        if startindex == 0:
            suchstring = '##Anfang###'
            
        elif startindex == -1:
            suchstring = 'ungültige Eingabe'
            
        else:
            suchstring = ''
            for i in range(0,11):
                suchstring = self.zelle.toPlainText()[startindex - i] + suchstring
                if (startindex - i) == 0:
                    break
                
        return suchstring[:-1]
    
    def pruefen(self):
        suchstring = self.suchstring.text()
        
        if suchstring == '':
            suchstring = self.suchstring_finden()
        print(suchstring)    

        self.suchstring.setDisabled(False)
        self.l5.setVisible(True)
        self.weiter.setDisabled(False)
        self.suchstring.setText(suchstring)
        
        startindex = self.zelle.toPlainText().find(suchstring) + len(suchstring)
        ende = startindex + len(self.eing.text()) 
        
        self.gefundener_string.setText(self.zelle.toPlainText()[startindex:ende])
        
    def weiter_gehts(self):
        w.findChild(QLabel, self.nummer).setVisible(True)
        w.findChild(QLineEdit, 'suchstr' + self.nummer).setVisible(True)        
        w.findChild(QLineEdit, 'suchstr' + self.nummer).setText( self.suchstring.text())
        self.close()
        
    def Hilfe(self):
        self.h = HilfeFenster("bilder_vorlagenersteller\\erweitertes_einlesen.png")
        self.h.show()        
        
        
#    def t(self):
#        print(self.nummer)
#app = QtCore.QCoreApplication.instance()
#if app is None:
#    app = QApplication(sys.argv)
#w = ZusatzFensterKerndaten('0')
#w.show()
#app.exec_()

# =============================================================================
# Dropbox: später in Hauptfenster verwendet, ließt Zeilen Spalten, name der Mappe
# und Wert der gedropten daten aus
# =============================================================================

class Dropbox(QLineEdit):
    def __int__(self, title, parent):
        super().__inti__(title,parent)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, e):
        e.accept()
        
    def dropEvent (self,e):
        erkenner = self.objectName()[0]# erkennt ob Dropbox kerndatenfenster oder arbeitsdatenfenster angehört
        
        self.eingabe_pos = (e.mimeData().data('application/x-qt-windows-mime;value="Link"'))# daten einlesen
        
        self.eingabeliste = str(self.eingabe_pos,encoding='utf-8').split('\x00')#schreiben aus string und teilen in Liset

        ind_mappe = int(self.eingabeliste[-4].rfind(']')) # erstellen der Indexe zum Auslesen der Kerndaten
        ind_spalte1 = int(self.eingabeliste[-3].find('S'))
        self.mappe= self.eingabeliste[-4][ind_mappe + 1:]# Beschreiben der kerndaten (hier Mappe)
        self.zeile1= self.eingabeliste[-3][1:ind_spalte1]
#        
        self.ind_dpp = int(self.eingabeliste[-3].find(':'))
        if self.ind_dpp != -1:
#            ind_zeile2 = int(eingabestring[self.ind_dpp:].find('Z')) + self.ind_dpp
            ind_spalte2 = int(self.eingabeliste[-3][self.ind_dpp:].find('S')) +self.ind_dpp
            self.spalte1= self.eingabeliste[-3][ind_spalte1+ 1:self.ind_dpp]
            self.zeile2 = self.eingabeliste[-3][self.ind_dpp + 2 :ind_spalte2]
            self.spalte2= self.eingabeliste[-3][ind_spalte2 + 1: ]
        else:
            self.spalte1= self.eingabeliste[-3][ind_spalte1+ 1:]
            self.spalte2 = self.spalte1
            self.zeile2 = self.zeile1
        self.breite = str(int(self.spalte2) - int(self.spalte1) + 1)
        self.laenge = str(int(self.zeile2) - int(self.zeile1) + 1)
        self.ausgabe = [self.mappe,self.zeile1,self.spalte1,self.laenge,self.breite, self.zeile2, self.spalte2]
        
        if erkenner == 'd':
            self.eingabe_wert = (e.mimeData().text())
            self.setText(self.eingabe_wert)

        
        zeile= self.objectName()[-1]# nummer der Dropbox, zum Auffinden der jew. Dropbox und als Index zum Beschreiben der weiter_gehts_liste 
        if erkenner == 'd':# wird nur für Kerndatenfenster ausgeführt
            for spalte in range(0,3):
                w.findChild(QLineEdit, zeile + str(spalte)).setText(self.ausgabe[spalte])
            w.weiter_gehts[int(zeile)] = True
            if (False in w.weiter_gehts) == False:# gibt weiterknopf frei wenn alle dropboxen eingaben hatten
                w.weiter.setDisabled(False)
                
            w.findChild(QPushButton, zeile).setDisabled(False)
                
        if erkenner == 'A': 
            try:
                for spalte in range(0,5):
                    A.findChild(QPlainTextEdit, zeile + str(spalte)).appendPlainText(self.ausgabe[spalte] )
            except TypeError:
                A.findChild(QPlainTextEdit, zeile + str(spalte)).appendPlainText('-' )
            
            A.weiter_gehts[int(zeile)] = True
            if (False in A.weiter_gehts) == False:
                A.weiter.setDisabled(False)
                
        
# =============================================================================
# Hauptfenster: Daten können über Drag and Drop eingelesen werden
# =============================================================================
        
class KerndatenFenster(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initMe()
        
    def initMe(self):
        
        self.setObjectName('w')       
        
        kd = QLabel(self)
        kd.setText('Einlesen der Kerndaten\n\nMappe\t\t Zeile\t  Spalte')
        kd.move(100,70)
        
        
        dt = QLabel(self)
        dt.setText('Anzahl Zähne\n\n\n\n\n\nAnzahl Slices\n\n\n\n\n\nLastpunkt\n\n\n\n\n\nWinkel Auflösung')
        dt.move(10,133)
        
        frage = QPushButton(self)
        frage.setIcon(QIcon("bilder_vorlagenersteller\\FrageIcon.png"))
        frage.move(370,30)
        frage.clicked.connect(self.Hilfe)

        self.weiter = QPushButton('Weiter', self)
        self.weiter.setDisabled(True)
        self.weiter_gehts = [False, False, False, False]
        self.weiter.move(300,500)
        self.weiter.clicked.connect(self.weiter_funkt)


        name_dbox = ['Dropbox\nZähne', 'Dropbox\nSlices', 'Dropbox\nLastpunkt', 'Dropbox\nWinkel']
        for zeile in range(0,4):
   
            self.drop = Dropbox(self)
            self.drop.setGeometry(300,125 + zeile * 80, 100,70)
            self.drop.setText(name_dbox[zeile])
            self.drop.setObjectName('drop' + str(zeile))
            self.drop.textChanged.connect(self.eingabe_frei)
            
            self.erweiterte_auswertung = QPushButton('erweitertes Einlesen',self)
            self.erweiterte_auswertung.setDisabled(True)
            self.erweiterte_auswertung.move(10,155 + zeile * 80) 
            self.erweiterte_auswertung.setObjectName(str(zeile))
            self.erweiterte_auswertung.clicked.connect(self.zusatz_oeffnen)
            
            self.l1 = QLabel(self)
            self.l1.setText('Wert folgt auf:')
            self.l1.setObjectName(str(zeile))
            self.l1.setVisible(False)
            self.l1.move(120, 160 + zeile * 80)
            
            self.suchstring = QLineEdit(self)
            self.suchstring.setObjectName('suchstr' + str(zeile))
            self.suchstring.setReadOnly(True)
            self.suchstring.setVisible(False)
            self.suchstring.setGeometry(200, 155 + zeile * 80, 85, 25)
            
            for spalte in range (0,3):

                
                self.eing = QLineEdit(self)
                self.eing.setObjectName( str(zeile) + str(spalte))
                if spalte == 0:
                    self.eing.setGeometry(100 + 80 * spalte,125 + zeile * 80, 80,25)
                    self.eing.setReadOnly(True)
                else:
                    self.eing.setGeometry(145 + 50 * spalte,125 + zeile * 80, 40,25)
                self.eing.setReadOnly(True)

        self.show()
        
#    def buchstabe_spalte(self, eingabe):
#        eingabe = eingabe.lower()
#        zahl_komplett = 0
#        for i1 in range(1,len(eingabe) + 1):
#            zahl = ord(eingabe[-i1]) - 96
#            zahl_komplett = zahl_komplett + zahl* 26 ** (i1 -1)
#        return zahl_komplett -1              
        
    def Hilfe(self):
        self.h = HilfeFenster('bilder_vorlagenersteller\\einlesen_kerndaten.png')
        self.h.show()
        
    def weiter_funkt(self):
        self.kern_daten = {}
        datenblock = []
        for zeile in range(0,4):
            datenzeile = []
            for spalte in range(0,3):
                datenzeile.append(self.findChild(QLineEdit, str(zeile)+ str(spalte)).text())
            datenzeile.append(self.findChild(QLineEdit, 'suchstr' + str(zeile)).text())
            datenblock.append(datenzeile)
        self.kern_daten['zaehne'] = datenblock[0]
        self.kern_daten['slices'] = datenblock[1]
        self.kern_daten['Lastpunkt'] = datenblock[2]
        self.kern_daten['Winkel'] = datenblock[3]
        self.close()     
        
    def eingabe_frei(self):
        nummer = self.sender().objectName()[-1]
        self.findChild(QLineEdit, nummer + '1').setReadOnly(False)
        self.findChild(QLineEdit, nummer + '2').setReadOnly(False)
        
    def zusatz_oeffnen(self):
        nummer = self.sender().objectName()
        text =self.findChild(Dropbox, 'drop' + nummer).eingabe_wert        
   
        self.z = ZusatzFensterKerndaten(nummer,text)
        self.z.setWindowTitle('erweitertes Einlesen ')
        self.z.show()




app = QtCore.QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
w = KerndatenFenster()
w.show()
app.exec_()                
# =============================================================================
# Arbeitsdatenfenster
# =============================================================================
       
class ArbeitsdatenFenster(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initMe()
        
    def initMe(self):
        
       
        kd = QLabel(self)
        kd.setText('Einlesen der Arbeitsdaten\n\nMappe\t\t Zeile1      Spalte1      Länge      Breite')
        kd.move(100,80)
        
        
        dt = QLabel(self)
        dt.setText('Gesamtmoment\n\n\n\n\n\n\n\n\nRadialkraft\n\n\n\n\n\n\n\n\nTangentialkraft\n\n\n\n\n\n\n\n\nBiegemoment')
        dt.move(10,133)
        vb = QLabel(self)
        
        vb.move(200,110)
        
        frage = QPushButton(self)
        frage.setIcon(QIcon("bilder_vorlagenersteller\\FrageIcon.png"))
        frage.move(510,30)
        frage.clicked.connect(self.Hilfe)

        self.weiter = QPushButton('Weiter', self)
        self.weiter.setDisabled(True)
        self.weiter_gehts = [False, False, False, False]
        self.weiter.move(480,650)
        self.weiter.clicked.connect(self.weiter_funkt)


        name_dbox = ['Dropbox\nGesamtmoment', 'Dropbox\nRadialkraft', 'Dropbox\nTangentialkraft', 'Dropbox\nBiegemoment']
        for zeile in range(0,4):
   
            self.drop = Dropbox(self)
            self.drop.setGeometry(420,125 + zeile * 120, 140,100)
            self.drop.setText(name_dbox[zeile])
            self.drop.setObjectName('Adrop' + str(zeile))
            

            
            for spalte in range (0,5):
         
                self.eing = QPlainTextEdit(self)

                self.eing.setAcceptDrops(False)
                self.eing.setObjectName( str(zeile) + str(spalte))
                if spalte == 0:
                    self.eing.setGeometry(100 + 80 * spalte,125 + zeile * 120, 80,100)
                elif spalte < 3:
                    self.eing.setGeometry(200 + 45 * (spalte-1),125 + zeile * 120, 40,100)
                else:
                    self.eing.setGeometry(210 + 45 * (spalte-1),125 + zeile * 120, 40,100)


        self.show()

    def weiter_funkt(self):
        self.arbeits_daten = {}
        datenblock = []
        for zeile in range(0,4):
            datenzeile = []
            for spalte in range(0,5):
                eintraege = self.findChild(QPlainTextEdit, str(zeile) + str(spalte)).toPlainText()
                datenzeile.append(eintraege.split('\n'))
            datenblock.append(datenzeile)
        self.arbeits_daten['gesamt_moment'] = datenblock[0]
        self.arbeits_daten['f_rad'] = datenblock[1]
        self.arbeits_daten['f_tan'] = datenblock[2]
        self.arbeits_daten['biege_moment'] = datenblock[3]
        self.close()                      

    def Hilfe(self):
        self.h = HilfeFenster("bilder_vorlagenersteller\\einlesen_arbeitsdaten.png")
        self.h.show()
       
app = QtCore.QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
A = ArbeitsdatenFenster()
A.show()
app.exec_()          


# =============================================================================
# Speicherdialog
# =============================================================================
class SpeicherFenster(QWidget):
    def __init__(self): 
        super().__init__()
                
        self.setGeometry(350,350,700,250)
        self.setWindowTitle('Speicherdialog')
        
        self.textBrowser = QLabel(self)
        self.textBrowser.setGeometry(QtCore.QRect(60, 30, 551, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QTextBrowser(self)
        self.textBrowser.setText('Wo möchten Sie die Dateien speichern?')
        self.textBrowser_2.setGeometry(QtCore.QRect(160, 140, 451, 31))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_2.textChanged.connect(self.weiter)
        self.label = QLabel(self)
        self.label.setText("Speicherort:")
        self.label.setGeometry(QtCore.QRect(60, 140, 101, 31))
        self.label.setObjectName("label")
        self.button = QPushButton(" Fertig" , self)
        self.button.setGeometry(QtCore.QRect(540, 180, 75, 23))
        self.button.setDisabled(True)
        self.button.clicked.connect(self.close)
        button2 = QPushButton('Datei Speichern', self)
        button2.setGeometry(QtCore.QRect(160, 180, 121, 23))

        button2.clicked.connect(self.speichern)#
             
        self.show()
        
    def speichern(self):#schreibt ausgewählten Dateiname - und Pfad in Textfenster und auf die Variable self.ausgabename(zur späteren verwendung)
        pfad = ''
        if path.exists('G:/TS-X1/Studenten/2020_SGuenther_NVH/Umwandler/Vorlagen/') == True:
            pfad = 'G:/TS-X1/Studenten/2020_SGuenther_NVH/Umwandler/Vorlagen/'
        self.ausgabename = QFileDialog.getSaveFileName(self, 'Vorlage speichern', pfad)[0]
        self.textBrowser_2.clear()
        
        if '.' in self.ausgabename[-5:]:# in dieser Verzweigung werden evtl. angefügt Dateiendungen(wie .xlsx) wieder entfernt, da diese später automatisch angehangen werden
            ind = -self.ausgabename.rfind('.')
            self.ausgabename = self.ausgabenamen[:ind - 1]
        self.textBrowser_2.setText(str(self.ausgabename))
        
    def weiter(self):
        self.button.setDisabled(False)

     

app = QtCore.QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
Speicherfenster = SpeicherFenster()
app.exec_()

# =============================================================================
# zuordnung: Namen der Arbeitsmappen -> Position der Arbeitsmappenmappem
# =============================================================================

name = w.findChild(Dropbox, 'drop0').eingabeliste[1]
ende = name.rfind(']')
name = name[:ende].replace("[", "")
if name[-4:] == '.csv':
    Uebersicht_mappen = pd.read_csv( name, delimiter=';' ,  nrows = 1)
    datentyp = '.csv'
else:
    datentyp = 'Excel'
    Uebersicht_mappen = pd.read_excel(name, sheet_name = None , usecols = [1], nrows = 1)
    

mappen_dict= {}
mappen_zahl = 0
if str(type(Uebersicht_mappen)) == "<class 'collections.OrderedDict'>":
    for key in Uebersicht_mappen:
        mappen_dict[key] = mappen_zahl
        mappen_zahl += 1
else:
    mappen_dict[w.findChild(QLineEdit, '00').text()] = 0
    

# =============================================================================
# #    Erstellung der textdatei mit den Daten der Vorlage
# =============================================================================

arbeits_daten = A.arbeits_daten
kern_daten = w.kern_daten


f = open(Speicherfenster.ausgabename + '.txt', 'w')
f.write('Kerndaten\n')
f.write('\nDatentyp:\n' + datentyp + '\n')
for key in kern_daten:
    f.write('\n' +key + '\n')
    f.write('Arbeitsmappe\tstartzeile\tstartspalte\tsuchstring\n')
    for eintrag in range(0,4):
        if eintrag == 0:
            f.write(str(mappen_dict[kern_daten[key][eintrag]]) +'\t')
        else:
            f.write(str(kern_daten[key][eintrag]) +'\t')
    f.write('\n')
    
f.write('\n\n------------------------------------------------------------------------------\n\nArbeitsdaten\n\n')

for key in arbeits_daten:
    anzahl_bloecke = str(len(arbeits_daten[key][0]))
    f.write(key + '\nAnzahl Blöcke: ' + anzahl_bloecke + '\n') 
    f.write('Arbeitsmappe\tstartzeile\tstartspalte\tlänge\tbreite\n')
    for zeile in range(0,int(anzahl_bloecke)):
        for spalte in range(0,5):
            if spalte == 0:
                f.write(str(mappen_dict[arbeits_daten[key][spalte][zeile]]) + '\t')
            else:
                f.write(arbeits_daten[key][spalte][zeile] + '\t')
        f.write('\n')
    f.write('\n')

f.close()