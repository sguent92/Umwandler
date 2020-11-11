if __name__!= '__main__':
    from __main__ import *

from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D

#------------------------------------------------------------------------------
def schreibe(file,ende): # liest Datei ein und schreibt sie auf Dataframe
    f = open(file,'r')

    data =[]
    for i in range(0,ende):
        data.append(f.readline())
                
    df_neu = pd.DataFrame(data)
    f.close()
    return df_neu
#------------------------------------------------------------------------------
    
writer = pd.ExcelWriter( Speicherfenster.ausgabename + '.xlsx', engine = 'xlsxwriter') # objext auf welchem die erstellten Arbeitmappen vor der tatsächlichen Erstellung der Excel datei gespeichert werden

df_Kopf = schreibe('Kopf_simpac.py',23)# schreibt Kopfstück auf DataFrame
df_wink_end = schreibe('Wink_End.py',4)# Textstelle am Ende der aufgelisteten Winkel
df_ende = schreibe('ende.py',3)# Textstelle am Dokumentende

laenge = int(360/Wink_Aufl)#laenge eines Blocks

Datenbloecke = collections.OrderedDict ()# OrderedDict auf dem DataFrames sämltlicher Blöcke mit den Daten für die Kräfte und Momente abgelegt werden
for key in Arbeitsdaten:
    einzelblock = pd.DataFrame([])
    for i in range(0,(int(len(Arbeitsdaten[key])/5))):# ein durchlauf pro Block der jeweiligen Kraft/ des Moments (jeder Block hat 5 einträge in "Arbeitsdaten")
        az= int(Arbeitsdaten[key][1 + i * 5]) - 1# az anfangszeile
        ez = az + laenge #int(Arbeitsdaten[key][3 + i * 5])#endzeile
        asp = int(Arbeitsdaten[key][2 + i * 5]) - 1 #anfangsspalte
        esp = asp + int(Arbeitsdaten[key][4 + i * 5])#endspalte
        einzelblock = pd.concat([einzelblock, df[df_keys[int(Arbeitsdaten[key][0])]].iloc[az : ez , asp : esp ]], axis = 1)# wenn mehr als ein Block vorhanden werden diese verknüpft
    einzelblock = einzelblock.reset_index(drop = True)# index wird auf standart (zahle 0 bis n) zurück gesetzt
    einzelblock.columns = range(einzelblock.shape[1])# spaltenindexe werden zurückgesetzt
    
    try:
        einzelblock = einzelblock.astype(float)# convertiert erste Spalte zu float
    except KeyError:
        pass
    einzelblock = einzelblock.dropna(axis = 1)# entfernt leere Spalten
    Datenbloecke[key] = einzelblock# einzelne Bloecke werden auf OrderedDict geschrieben, leere Spalten werden entfernt

if Skalierung.skalierung == True:
    Datenbloecke['f_rad'] = Datenbloecke['f_rad'] * Skalierung.faktor_rad
    Datenbloecke['f_tan'] = Datenbloecke['f_tan'] * Skalierung.faktor_tan
    Datenbloecke['biege_moment'] = Datenbloecke['biege_moment'] * Skalierung.faktor_mom_bieg

leere_zelle = pd.DataFrame([float('NaN')])
leere_zellen = pd.concat([leere_zelle for i in range(0,7)], axis = 1)# leere Zellen werden zum anfügen an die Winkel erstellt, wichtig damit Winkel später mit Kräften zusammengefügt werden können

Wink_Aufl_rad= Wink_Aufl/180*np.pi # errechnet Winkel Auflösung in rad

df_Wink = pd.DataFrame([Wink_Aufl_rad * i for i in range(0,laenge)])# erstellt DataFrame mit allen Winkeln in rad
df_Wink[1] = df_Wink[0]
df_Wink[0] = "" # erstellt leerspalte in 1. Spalte
   
leerspalte = [float('NaN') for i in range(0,laenge)]
leerspalten = pd.DataFrame(np.transpose(np.array([leerspalte for i in range(0,6)])))#erstellt Block mit 6 leerspalten. Wird im Abschnitt darunter benötigt


Kopfzeilen_weg = {'f_rad': (10 , 16), 'f_tan' : (11, 18) , 'biege_moment' : (12, 18)}# zuordnung der Zeilen im Kopfstück, die bei evtl fehlenden Daten auskommentiert werden
for key in Datenbloecke:
    if Datenbloecke[key].shape[1] == 0:# prüft ob die ausgelesenen Datenblocke leer sind 
    #(z.B. weil die Daten auf der ausgelesenen Datei nicht vorhanden sind und auf der Vorlage darher eine leere Zelle angegeben wurde) und ersetzt ggf. mit leerspalten
        if key == 'gesamt_moment':
            Datenbloecke[key] =  pd.DataFrame([leerspalte]).transpose()
        else:
            Datenbloecke[key] =  pd.DataFrame([leerspalte for i in range(0,zahn_zahl * slice_zahl)]).transpose()
            
            df_Kopf.iloc[Kopfzeilen_weg[key][0]] = '!' + df_Kopf.iloc[Kopfzeilen_weg[key][0]]# nicht benötigte Kopfzeilen werden mit ! auskommentiert
            df_Kopf.iloc[Kopfzeilen_weg[key][1]]= '!' + df_Kopf.iloc[Kopfzeilen_weg[key][1]]


zahn_winkel = [pd.concat([leere_zelle, pd.DataFrame([2 * np.pi / zahn_zahl * i]), leere_zellen], axis = 1) for i in range(0,zahn_zahl)]

f_rad= [pd.DataFrame(Datenbloecke['f_rad'][i], dtype = float) *  Skalierung.faktor_rad for i in range(0,zahn_zahl * slice_zahl)]#pd.DataFrame([Datenbloecke['f_rad'][durchlauf + slice_nummer * zahn_zahl]], dtype = float).transpose()
f_tan= [pd.DataFrame(Datenbloecke['f_tan'][i], dtype = float) * Skalierung.faktor_tan for i in range(0,zahn_zahl * slice_zahl)]
moment = [pd.DataFrame(Datenbloecke['biege_moment'][i], dtype = float) * Skalierung.faktor_mom_bieg for i in range(0,zahn_zahl * slice_zahl)]


df_kraftdaten = [pd.concat([leerspalten, f_rad[i], f_tan[i], moment[i]], axis = 1) for i in range(0, zahn_zahl * slice_zahl)]


for slice_nummer in range(0,slice_zahl):
    df_kraft_komplett = [pd.DataFrame(np.concatenate([zahn_winkel[i].values, df_kraftdaten[i + slice_nummer * zahn_zahl].values])) for i in range(0, zahn_zahl)]
    df_kraft_komplett = pd.concat(df_kraft_komplett)# for i in range(0,zahn_zahl)]#for i in (zahn_winkel[i], df_kraftdaten[i + slice_nummer * zahn_zahl])]
    df_mappe_komplett = pd.concat([df_Kopf,df_Wink,df_wink_end,df_kraft_komplett, df_ende])
    df_mappe_komplett.to_excel(writer, sheet_name = "Slice " + str(slice_nummer + 1), index = False, header=False)# schreibt komplette Mappen auf writer

writer.save()

raum_ord = np.array(Datenbloecke['f_rad'].iloc[0,:zahn_zahl], dtype = float)# pre Allokation deines arrays auf das Daten geschrieben werden mit dem im Plot später die räumliche Ordnung dargestellt wird


# =============================================================================
# #Daten werden für späteren Plot aufgearbeitet
# =============================================================================

def max_loc(A): # ließt array ein und gibt array mit den Positionen der lokalen Maxima aus
    m = []
    for i in range(1, len(A)-1):
        if (A[i] > A[i-1]) & (A[i] > A[i+1]):
            m = m + [i]
    return m
#------------------------------------------------------------------------------
Nr=int(zahn_zahl) # Anzahl messpunkte für räumliche Auswertung
N=len(df_Wink) # Anzahl Messpunkte eines Zahnes innerhalb einer Rotorumdrehung

#Ft2_daten = np.array(Datenbloecke['f_rad'].iloc[:,:int(zahn_zahl)])#np.array(f_rad[0], dtype = float)
#
#Ft2_daten = np.transpose(Ft2_daten)
#Ft2_roh = 1/N/Nr * np.abs(np.fft.fft2(Ft2_daten, axes = (0,1)))
#Ft2_zeile0 = np.reshape(Ft2_roh[0,:], (1,N))
#Ft2_spektrum = np.flipud(Ft2_roh[1:,:])
#Ft2 = (np.concatenate((Ft2_zeile0, Ft2_spektrum)))[:Nr//2,:60]

Ft2_daten = []
for spalte in range(int(zahn_zahl)):
    Mittelwert_zaehne = np.array(Datenbloecke['f_rad'].iloc[:,  spalte : int(slice_zahl) * int(zahn_zahl) : int(zahn_zahl)]).mean(axis = 1)
    Ft2_daten.append(Mittelwert_zaehne)# = [Mittelwert_zaehne[0 + i: i + int(slice_zahl) * int(zahn_zahl) + 1 : int(zahn_zahl)] for i in range(int(zahn_zahl))]

Ft2_daten = np.array(Ft2_daten)#np.array(f_rad[0], dtype = float)


Ft2_roh = 1/N/Nr * np.abs(np.fft.fft2(Ft2_daten))
Ft2_zeile0 = np.reshape(Ft2_roh[0,:], (1,N))
Ft2_spektrum = np.flipud(Ft2_roh[1:,:])
Ft2 = (np.concatenate((Ft2_zeile0, Ft2_spektrum)))[:Nr//2,:60]


r_end = 1
r_aufl = r_end/Nr
r = np.linspace(0.0, r_end, Nr + 1)
yr = raum_ord#np.append(raum_ord, raum_ord[0])# raum Ordnung für einen Zahn
#f_raum = 1/Nr * np.abs(scipy.fftpack.fft(yr))[:24]# Amplituden räuml fft
f_raum = Ft2.max(axis = 1)
xf_raum = np.linspace(0, (1/(2*r_aufl)) - 1, Nr//2)# x achse raumordnung
# Variablen festlegung für räumliche fft


t_end_min = 1/ Motordrehzahl # dauer einer Umdrehung in minuten
t_end_sec = 60*t_end_min
Ts = t_end_sec/N # zeitl. Auflösung in sek
Tm = t_end_min/N # zeitl. Auflösung in min
t = np.linspace(0.0 , t_end_sec, N ) # array für Zeitachse
yt = f_rad[0]#np.append(f_rad[0], f_rad[0].iloc[0,0])# für einen Zahn
#yt = np.append(Datenbloecke['f_rad'].iloc[:,:zahn_zahl].mean(axis = 1), Datenbloecke['f_rad'].iloc[:,:zahn_zahl].mean(axis = 1)[0])# Mittelwert des gesamten Motors
f = np.linspace(0.0, ((60/(N*Tm))/Motordrehzahl - 1), 60)# array für Frequenzachse
#f_amp1 = 1/N * np.abs(scipy.fftpack.fft(f_rad[0].squeeze()))[:60]# Amplitude des Frequenzbereichs
f_amp = Ft2.max(axis =0)[:60]

# Variablen für zeitl. fft




    
t_mod_pos = max_loc(np.abs(f_amp[:60]))# array mit lokalen maxima der zeitlichen fft
r_mod_pos= max_loc(np.abs(f_raum[:Nr//2]))# array mit lokalen maxima der räumlichen fft
t_mod = []
r_mod = []
t_modstr = ""
r_modstr= ""

for I in t_mod_pos:# Schleifen erstellen String mit den Maxima der jeweiligen ffts, wobei maxima mit zu geringer Amplitude gefiltert werden
    if f_amp[I] > (max(f_amp[1:])/20):
        t_mod = np.append( t_mod, [f[I]])
        if I < 60:
            t_modstr = t_modstr + str(float(round(f[I],5))) + "   "
for I in r_mod_pos:
    if f_raum[I] > (max(f_amp[1:])/20):
        r_mod = np.append( r_mod, [xf_raum[I]])
        if I < (1/(2*r_aufl)):
            r_modstr = r_modstr + str(int(round(xf_raum[I],0))) + "   "

# =============================================================================
# Beginn Plot
# =============================================================================

plt.figure(figsize = (24,22))
plt.subplot(421)
plt.xlabel("Zeit in s")
plt.ylabel('Radialkraft in N')
plt.plot(t,yt)
plt.title('zeitlicher Radialkraftverlauf')
# netzdiagramm räumlicher verteilung der radialkräfte im rotor

plt.subplot(422, polar=True)
angles = np.linspace(0, 2*np.pi, len(yr), endpoint=False)
plt.plot(angles, yr, 'o-', linewidth=2)
plt.fill(angles, yr, alpha=0.25)
plt.ylim(min(yr) * 1.8 , 100)
plt.title("räumliche Verteilung der Radialkraft")
# radialkräfte in abhängikeit der Zeit über die Dauer einer Rotorumdrehung

plt.subplot(423)
plt.plot(f, f_amp[:60], c ='r')
plt.xlabel('zeitliche Moden bei: ' + t_modstr)
plt.grid(which='major')
plt.title('zeitliche Moden')
#räuml. fft

plt.subplot(424)
plt.plot(xf_raum, f_raum[:Nr//2], c='r')
plt.xlabel('räumliche Moden bei: ' + r_modstr)
plt.grid(which='major')
plt.title('räumliche Moden')
#zeitl. fft

ax = plt.subplot(425)   
ax.set_xlabel('zeitliche Ordnung')
ax.set_ylabel('räumliche Ordnung')
ax.set_title('2D fft')
farbschema = 'nipy_spectral'
#farbschema = 'coolwarm' # ist auch nicht schlecht
im = ax.imshow(Ft2, cmap = farbschema, origin = 'lower', vmax = float(Ft2[0,0])/2 )
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar( im,cax=cax, use_gridspec = False)


plt.subplot(426)
rad_min = np.abs(Datenbloecke['f_rad']).min(axis = 0)
rad_max = np.abs(Datenbloecke['f_rad']).max(axis = 0)
rad_mean = np.abs(Datenbloecke['f_rad']).mean(axis = 0)
zahn_x = range(zahn_zahl * slice_zahl)
plt.plot(zahn_x, rad_max, label = 'maximale Radialkraft pro Zahn')
plt.plot(zahn_x, rad_min,label = 'minimale Radialkraft pro Zahn')
plt.plot(zahn_x, rad_mean, label = 'durchschnittliche Radialkraft pro Zahn')
plt.ylim(0, rad_max.max()* 1.33)
plt.title('Datenvalidierung Radialkraft')
plt.xlabel('Zähne')
plt.ylabel(' Betrag der Kraft pro Zahn in N')
plt.legend()

plt.subplot(427)
tan_min = np.abs(Datenbloecke['f_tan']).min(axis = 0)
tan_max = np.abs(Datenbloecke['f_tan']).max(axis = 0)
tan_mean = np.abs(Datenbloecke['f_tan']).mean(axis = 0)
plt.plot(zahn_x, tan_max, label = 'maximale Tangentialkraft pro Zahn')
plt.plot(zahn_x, tan_min,label = 'minimale Tangentialkraft pro Zahn')
plt.plot(zahn_x, tan_mean, label = 'durchschnittliche Tangentialkraft pro Zahn')
plt.ylim(0, tan_max.max()* 1.33)
plt.title('Datenvalidierung Tangentialkraft')
plt.xlabel('Zähne')
plt.ylabel(' Betrag der Kraft pro Zahn in N')
plt.legend()

if Datenbloecke['biege_moment'].dropna().empty == False:
    plt.subplot(428)
    bm_min = np.abs(Datenbloecke['biege_moment']).min(axis = 0)
    bm_max = np.abs(Datenbloecke['biege_moment']).max(axis = 0)
    bm_mean = np.abs(Datenbloecke['biege_moment']).mean(axis = 0)
    rad_x = range(zahn_zahl * slice_zahl)
    plt.plot(zahn_x, bm_max, label = 'maximales Biegemoment pro Zahn')
    plt.plot(zahn_x, bm_min,label = 'minimales Biegemoment pro Zahn')
    plt.plot(zahn_x, bm_mean, label = 'durchschnittliches Biegemoment pro Zahn')
    plt.ylim(0, bm_max.max()* 1.33)
    plt.title('Datenvalidierung Biegemoment')
    plt.xlabel('Zähne')
    plt.ylabel(' Betrag des Moment pro Zahn in Nm')
    plt.legend()


plt.savefig(Speicherfenster.ausgabename + '.png')

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
        Bild.setPixmap(QPixmap(Speicherfenster.ausgabename + '.png'))
        
        
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

# =============================================================================
# 
# =============================================================================
#zeile = Datenbloecke['f_rad'].iloc[0,:].mean()
#zwink = [i * 2 * np.pi /48 for i in range(48)]
#Kraft_complex = [ complex(np.cos(zwink[i]) * Datenbloecke['f_rad'].iloc[0,i], np.sin(zwink[i]) * Datenbloecke['f_rad'].iloc[0,i]) for i in range(48)]
#test = sum(Kraft_complex)
#Kraft_liste = []
#y = []
#z = []
#for ii in range(1440):
#    Kraft_complex = sum([ complex(np.cos(zwink[i]) * Datenbloecke['f_rad'].iloc[ii,i], np.sin(zwink[i]) * Datenbloecke['f_rad'].iloc[ii,i]) for i in range(48)])
#    Kraft_liste.append(Kraft_complex)
#    realteil = sum([np.cos(zwink[i]) * Datenbloecke['f_rad'].iloc[ii,i]for i in range(48)])
#    imaginaerteil = sum([np.sin(zwink[i]) * Datenbloecke['f_rad'].iloc[ii,i]for i in range(48)])
#    
#    y.append(realteil)
#    z.append(imaginaerteil)
#    
#y = np.array([f_rad[0].iloc[0,0] * np.cos(i * 2 *np.pi/1440) for i in range(1440)]) #np.array(y)
#z = np.array([f_rad[0].iloc[0,0] * np.sin(i * 2 *np.pi/1440) for i in range(1440)])#np.array(z)
#
#
#
#zahn = [Datenbloecke['f_rad'].iloc[:,i:i+288:48].mean().mean() for i in range(48)]
#test = np.array([Datenbloecke['f_rad'].iloc[:].mean() for i in range(48)])
#test = test - test.mean()
#test2 = 1/48 * np.abs(np.fft.fft(test))
#
#fig = plt.figure(figsize = (12,12))
#plt.subplot(111, polar=True)
#plt.plot(np.array(zwink), zahn)
#
#
#test3 = []
#
#f_rad_winkel_real = np.array([np.cos(2* np.pi / 48 * i) * Datenbloecke['f_rad'].iloc[:,i:i+288:48].mean(axis = 1) for i in range(48)])
#f_rad_winkel_imag = np.array([np.sin(2* np.pi / 48 * i) * Datenbloecke['f_rad'].iloc[:,i:i+288:48].mean(axis = 1) for i in range(48)])
#
#y = f_rad_winkel_real.sum(axis=0)
#z = f_rad_winkel_imag.sum(axis=0)
#
##for ii in range(1440):
#   
##    f_rad_winkel = np.array([(np.cos(i *2 *np.pi /48) * Datenbloecke['f_rad'].iloc[ii,i:i+288:48].mean(), np.sin(i *2 *np.pi /48) * Datenbloecke['f_rad'].iloc[ii,i:i+288:48].mean() )for i in range(48)])
##    test3.append(f_rad_winkel)
#
#test4 = np.array([test3[i]])
##realteil = np.arry([test3[i][]])
#
#Kraft = np.array(Kraft_liste)    
#fig = plt.figure(figsize = (20,10))
#plt.plot(test3[1][:,1])
#
#Kraftf = np.abs(np.fft.fft(Kraft)) * 1*1440
#f = np.arange(0,1440, 1)
#fig = plt.figure(figsize = (20,10))
#plt.plot(f[:100],Kraftf[:100])
#
#
#from mpl_toolkits import mplot3d
#
#fig = plt.figure(figsize = (28,10))
#ax = plt.axes(projection ="3d")
#
#ax.plot(t,y,z)

