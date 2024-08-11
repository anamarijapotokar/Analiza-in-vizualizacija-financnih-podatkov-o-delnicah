import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# računanje DNEVNEGA RAZPONA in dodajanje tega v tabele
def dnevni_razpon(podatki_slovar):
    nov_slovar = {}

    for delnica, podatki in podatki_slovar.items():
        podatki['Dnevni razpon'] = podatki['Najvišja cena'].astype(float) - podatki['Najnižja cena'].astype(float)
        nov_slovar[delnica] = podatki
        
    return nov_slovar


# računanje POVPREČJA nekega stolpca 
def izracun_povprecja(podatki_slovar, stolpec):
    povprecja_slovar = {}
    
    for delnica, podatki in podatki_slovar.items():
        povprecje = round(podatki[stolpec].astype(float).mean(), 4) # zaokrožim na 4 decimalke
        povprecja_slovar[delnica] = povprecje
    
    return povprecja_slovar



# ANALIZA TRENDA in dodajanje v tabelo
def preveri_moc_trenda(podatki_slovar):
    nov_slovar = {}
    
    for delnica, podatki in podatki_slovar.items():
        podatki['sprememba_cene'] = podatki['Cena ob koncu trgovalnega dne'].astype(float).diff() # dnevna sprememba cene 
        podatki['sprememba_volumna'] = podatki['Obseg trgovanja'].astype(float).diff() # dnevna sprememba obsega trgovanja
        
        moc_trenda = []
        
        for i in range(1, len(podatki)):
            if (podatki['sprememba_cene'].iloc[i] > 0 and podatki['sprememba_volumna'].iloc[i] > 0) or \
               (podatki['sprememba_cene'].iloc[i] < 0 and podatki['sprememba_volumna'].iloc[i] < 0):
                moc_trenda.append("Močan trend")
            else:
                moc_trenda.append("Manj stabilen trend")
        
        moc_trenda.insert(0, "Ni podatkov za primerjavo")  # na prvi dan nimaš s ničemer za primerjat
        podatki['Moč trenda'] = moc_trenda
        
        nov_slovar[delnica] = podatki
    
    return nov_slovar



# izris grafa za katerokoli delnico in katerokoli ceno (ob začetku, koncu trgovalnega dne, najvišjo ali najnižjo)
def graf_cene(podatki_slovar, stolpec):
    plt.figure(figsize=(14, 10))
    
    for delnica, podatki in podatki_slovar.items():

        # podatki za risanje
        datumi = podatki.index
        cene = podatki[stolpec].astype(float)

        # cene
        plt.plot(datumi, cene, label=f'{delnica} - {stolpec}')

    plt.title(f'{stolpec} za vse delnice')
    plt.xlabel('Datum')
    plt.ylabel('Cena')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



# VOLATILNOST + GRAF
def izracun_volatilnosti(podatki_slovar):
    volatilnosti_slovar = {}
    
    for delnica, podatki in podatki_slovar.items():
        # pogledaš, če stolpec 'Cena ob koncu trgovalnega dne' vsebuje numerične podatke, ker drugač ne bo delal
        if podatki['Cena ob koncu trgovalnega dne'].dtype != 'float64' and podatki['Cena ob koncu trgovalnega dne'].dtype != 'int64':
            podatki['Cena ob koncu trgovalnega dne'] = pd.to_numeric(podatki['Cena ob koncu trgovalnega dne'], errors='coerce')
        
        # dnevni donos = % sprememba zaključne cene delnice med zaporednimi dnevi
        podatki['Donos'] = podatki['Cena ob koncu trgovalnega dne'].pct_change()

        # odstranim NAje
        podatki = podatki.dropna(subset=['Donos'])
        
        volatilnost = podatki['Donos'].std()
        volatilnosti_slovar[delnica] = volatilnost

        # izpis
        print(f'Volatilnost delnice {delnica} za obravnavano obdobje je: {volatilnost:.4f}')


    return volatilnosti_slovar



def graf_histogram_volatilnosti(podatki_slovar):
    plt.figure(figsize=(14, 10))

    for delnica, podatki in podatki_slovar.items():
        podatki['Donos'] = podatki['Cena ob koncu trgovalnega dne'].pct_change()
        volatilnost = podatki['Donos'].std()

        # histogram
        plt.hist(podatki['Donos'].dropna(), bins=30, alpha=0.5, label=f'{delnica} - Volatilnost: {volatilnost:.4f}')

    plt.title('Histogram dnevnih donosov za različne delnice')
    plt.xlabel('Dnevni donos') # v %
    plt.ylabel('Frekvenca') # kok dni v tem enem letu je bil dnevni donos enak ...
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()



# RSI + GRAF
def izracunaj_RSI(podatki_slovar, obdobje=14):
    posodobljen_slovar = {}

    for oznaka, tabela_podatkov in podatki_slovar.items():
        sprememba = tabela_podatkov['Cena ob koncu trgovalnega dne'].diff()  # sprememba cene med zaporednimi dnevi

        poz_spr = sprememba.where(sprememba > 0, 0) # = gains; nadomestiš vrednosti, kjer pogoj sprememba > 0 ni izpolnjen, z vrednostjo 0
        neg_spr = -sprememba.where(sprememba < 0, 0) # = losses; ^ isto sam drgač pogoji

        povp_poz_spr = poz_spr.rolling(window=obdobje).mean() 
        povp_neg_spr = neg_spr.rolling(window=obdobje).mean()

        RS = povp_poz_spr / povp_neg_spr # relativna moč = RS
        RSI = 100 - (100 / (1 + RS)) # formula za RSI

        tabela_podatkov['RSI'] = RSI # RSI v tabelce

        tabela_podatkov['Status'] = np.where(pd.isna(RSI), 'Ni podatkov', # nadomestim NAje z ni podatkov
                                             pd.cut(RSI, bins=[-float('inf'), 30, 70, float('inf')],
                                                    labels=['Podkupljena', 'Nevtralna', 'Prekupljena']))

        
        posodobljen_slovar[oznaka] = tabela_podatkov

    return posodobljen_slovar



def graf_RSI(oznaka, podatki_slovar, obdobje=14):
    podatki_slovar = izracunaj_RSI(podatki_slovar, obdobje)
    tabela_podatkov = podatki_slovar[oznaka]

    plt.figure(figsize=(14, 10))
    plt.plot(tabela_podatkov.index, tabela_podatkov['RSI'], label='RSI', color='blue')
    
    # meje
    plt.axhline(70, color='red', linestyle='--', label='Prekupljeno (70)')
    plt.axhline(30, color='green', linestyle='--', label='Podkupljeno (30)')
    
    # barvanje
    plt.fill_between(tabela_podatkov.index, 0, tabela_podatkov['RSI'], where=(tabela_podatkov['RSI'] < 30), color='lightgreen', alpha=0.5, label='Podkupljeno')
    plt.fill_between(tabela_podatkov.index, 0, tabela_podatkov['RSI'], where=(tabela_podatkov['RSI'] > 70), color='lightcoral', alpha=0.5, label='Prekupljeno')
    plt.fill_between(tabela_podatkov.index, 0, tabela_podatkov['RSI'], where=(tabela_podatkov['RSI'] >= 30) & (tabela_podatkov['RSI'] <= 70), color='lightyellow', alpha=0.5, label='Nevtralno')

    plt.title(f'RSI za delnico {oznaka}')
    plt.xlabel('Datum')
    plt.ylabel('RSI')
    plt.legend()
    plt.grid(True)
    plt.show()



# def. nakup in prodajo delnice; predpostavim, da je kupec racionalen -> vedno kupi največje možno število delnic, ki si ga lahko s svojim stanjem privošči, oz. proda vse delnice, ki jih ima v lasti
def kupi_delnice(stanje, delnice, cena):
    kolicina = int(stanje // cena)
    strosek = cena * kolicina
    if stanje >= strosek:
        delnice += kolicina
        stanje -= strosek
        
        return stanje, delnice, kolicina
    
    return stanje, delnice, 0 # v primeru, ko je stanje < stroška nakupa, je nakup neuspešen, tako da vrnemo 0 = št. kupljenih delnic

def prodaj_delnice(stanje, delnice, cena):
    if delnice > 0:
        stanje += cena * delnice
        prodane_delnice = delnice
        delnice = 0
        
        return stanje, delnice, prodane_delnice
    
    return stanje, delnice, 0 # če prodaja ni bila uspešna, je število prodanih delnic enako 0 ofcourse



def avtomatizirano_trgovanje(oznaka, podatki_slovar, obdobje=14, zacetno_stanje=10000):
    stanje = zacetno_stanje
    delnice = 0

    posodobljen_slovar = izracunaj_RSI(podatki_slovar, obdobje)
    
    tabela_podatkov = posodobljen_slovar[oznaka]

    for indeks, vrstica in tabela_podatkov.iterrows():
        cena = float(vrstica['Cena ob koncu trgovalnega dne'])
        RSI = vrstica['RSI']

        if RSI < 30:  # podkupljena -> kupi
            stanje, delnice, kupljene_delnice = kupi_delnice(stanje, delnice, cena)
            if kupljene_delnice > 0:
                print(f'{indeks.date()}: Kupil {kupljene_delnice} delnic {oznaka} pri ceni {cena:.2f}')
        elif RSI > 70:  # prekupljena -> prodaj
            stanje, delnice, prodane_delnice = prodaj_delnice(stanje, delnice, cena)
            if prodane_delnice > 0:
                print(f'{indeks.date()}: Prodal {prodane_delnice} delnic {oznaka} pri ceni {cena:.2f}')
        else:  # nevtralna -> ne naredi nič
            print(f'{indeks.date()}: Neukrepanje za delnico {oznaka} pri ceni {cena:.2f} z RSI {RSI:.2f}')

    zadnja_cena = float(tabela_podatkov.iloc[-1]['Cena ob koncu trgovalnega dne'])
    vrednost_portfelja = stanje + (delnice * zadnja_cena)

    print(f'Končno stanje portfelja: Stanje: {stanje:.2f}, Delnice: {delnice}, Vrednost portfelja: {vrednost_portfelja:.2f}')

