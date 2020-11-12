from __main__ import  *
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D

laenge = int(360/Wink_Aufl)#laenge eines Blocks
breite = slice_zahl * zahn_zahl
    
startzeile1 = int(Arbeitsdaten['gesamt_moment'][1]) - 1
startzeile2 = int(Arbeitsdaten['f_rad'][1]) - 1
startzeile3 = int(Arbeitsdaten['f_tan'][1]) - 1
   

df_schrift1 = df['1'].iloc[0 : startzeile1 , 0 : 2]# Kopfstück
if V_Err == True:
    df_schrift1.iloc[5][1] = slice_zahl# überschreibt Slice Zahl in Tabelle mit manuell angegebener
    
df_schrift2 =df['1'].iloc[startzeile1 + laenge : startzeile2 , 0 : 2]# Kopfstück über radialkraftblock
df1 = pd.DataFrame(df['1'].iloc[startzeile1 :startzeile1 + laenge, 0 : 2], dtype = float)# gesamt Moment
df2 = pd.DataFrame(df['1'].iloc[startzeile2 : startzeile2 + laenge, 0 : 1 + breite], dtype = float)# Radialkraft
df_schrift3 = df['1'].iloc[startzeile2 + laenge : startzeile3 , 0 : 2]# Kopfstück über tangentialkraftblock
df3 = pd.DataFrame(df['1'].iloc[startzeile3 : startzeile3 + laenge, 0 : 1 + breite], dtype = float)# Tangentialkraft

if (Skalierung.faktor_rad != 1) | (Skalierung.faktor_tan != 1) | (Skalierung.faktor_mom_ges != 1):# skaliert die entsprechenden Kräfte/ Momente wenn gewünscht
    df1.loc[:,1] = df1.loc[:,1] * Skalierung.faktor_mom_ges
    df2.loc[:,1:] = df2.loc[:,1:] * Skalierung.faktor_rad
    df3.loc[:,1:] = df3.loc[:,1:] * Skalierung.faktor_tan

#df_ausgabe= df['1'].dropna(axis = 1,how = 'all')
#df_ausgabe = df_ausgabe.where(pd.notnull(df_ausgabe), None)
#
#df_ausgabe.to_csv( Speicherfenster.ausgabename + '.csv' , index = None, header = None, na_rep = '')


df_schrift1.to_csv( Speicherfenster.ausgabename + '.csv' , index = None, header = None)
df1.to_csv( Speicherfenster.ausgabename + '.csv' , index = None, header = None , mode = 'a')
df_schrift2.to_csv( Speicherfenster.ausgabename + '.csv' , index = None, header = None , mode = 'a')
df2.to_csv( Speicherfenster.ausgabename + '.csv' , index = None, header = None , mode = 'a')
df_schrift3.to_csv( Speicherfenster.ausgabename + '.csv' , index = None, header = None , mode = 'a')
df3.to_csv( Speicherfenster.ausgabename + '.csv' , index = None, header = None , mode = 'a')

# =============================================================================
# Datenaufarbeitung für Plot
# =============================================================================

def max_loc(A): # ließt array ein und gibt array mit den Positionen der lokalen Maxima aus
    m = []
    for i in range(1, len(A)-1):
        if (A[i] > A[i-1]) & (A[i] > A[i+1]):
            m = m + [i]
    return m
#------------------------------------------------------------------------------

Nr=int(zahn_zahl) # Anzahl messpunkte für räumliche Auswertung
N=laenge # Anzahl Messpunkte eines Zahnes innerhalb einer Rotorumdrehung

Ft2_daten = []
for spalte in range(int(zahn_zahl)):
    Mittelwert_zaehne = np.array(df2.iloc[:, 1 + spalte : int(slice_zahl) * int(zahn_zahl) : int(zahn_zahl)]).mean(axis = 1)
    Ft2_daten.append(Mittelwert_zaehne)# = [Mittelwert_zaehne[0 + i: i + int(slice_zahl) * int(zahn_zahl) + 1 : int(zahn_zahl)] for i in range(int(zahn_zahl))]

Ft2_daten = np.array(Ft2_daten)#np.array(f_rad[0], dtype = float)
#Ft2_daten = np.concatenate((Ft2_daten, np.reshape(Ft2_daten[0,:], (1,N ) )), axis = 0)
#Ft2_daten = np.concatenate((Ft2_daten, np.reshape(Ft2_daten[:,0], (Nr + 1, 1) )), axis = 1)

Ft2_roh = 1/(N)/(Nr) * np.abs(np.fft.fft2(Ft2_daten))
Ft2_zeile0 = np.reshape(Ft2_roh[0,:], (1,N))
Ft2_spektrum = np.flipud(Ft2_roh[1:,:])
Ft2 = (np.concatenate((Ft2_zeile0, Ft2_spektrum)))[:int(Nr//2),:60]

r_end = 1
r_aufl = r_end/Nr
r = np.linspace(0.0, r_end, Nr + 1)
yr = np.array(df2)[0,1: int(zahn_zahl) + 1]#Ft2_daten[:,0] #np.append(raum_ord, raum_ord[0])# raum Ordnung für einen Zahn
#f_raum = 1/Nr * np.abs(scipy.fftpack.fft(yr))[:24]# Amplituden räuml fft
f_raum = Ft2.max(axis = 1)
xf_raum = np.linspace(0, (1/(2*r_aufl)) - 1, Nr//2)# x achse raumordnung
# Variablen festlegung für räumliche fft


t_end_min = 1/ Motordrehzahl # dauer einer Umdrehung in minuten
t_end_sec = 60*t_end_min
Ts = t_end_sec/N # zeitl. Auflösung in sek
Tm = t_end_min/N # zeitl. Auflösung in min
t = np.linspace(0.0 , t_end_sec, N ) # array für Zeitachse
yt = np.array(df2)[:,1]#Ft2_daten[0,:]#np.append(f_rad[0], f_rad[0].iloc[0,0])# für einen Zahn
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
# Plot
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
rad_min = np.abs(df2.iloc[:,1:]).min(axis = 0)
rad_max = np.abs(df2.iloc[:,1:]).max(axis = 0)
rad_mean = np.abs(df2.iloc[:,1:]).mean(axis = 0)
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
tan_min = np.abs(df3.iloc[:,1:]).min(axis = 0)
tan_max = np.abs(df3.iloc[:,1:]).max(axis = 0)
tan_mean = np.abs(df3.iloc[:,1:]).mean(axis = 0)
plt.plot(zahn_x, tan_max, label = 'maximale Tangentialkraft pro Zahn')
plt.plot(zahn_x, tan_min,label = 'minimale Tangentialkraft pro Zahn')
plt.plot(zahn_x, tan_mean, label = 'durchschnittliche Tangentialkraft pro Zahn')
plt.ylim(0, tan_max.max()* 1.33)
plt.title('Datenvalidierung Tangentialkraft')
plt.xlabel('Zähne')
plt.ylabel(' Betrag der Kraft pro Zahn in N')
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
