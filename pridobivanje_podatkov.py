import yfinance as yf
import pandas as pd

def pridobi_podatke(imena_podjetij, zacetek, konec):
    podatki_za_delnice = {}
    
    for oznaka in imena_podjetij:
        df = yf.download(oznaka, start=zacetek, end=konec)
        df = df.drop(columns=['Adj Close']) # ne rabim
        df = df.rename(columns={
            'Open': 'Cena ob začetku trgovalnega dne',
            'High': 'Najvišja cena',
            'Low': 'Najnižja cena',
            'Close': 'Cena ob koncu trgovalnega dne',
            'Volume': 'Obseg trgovanja'
        })
        
        for stolpec in df.columns[:-1]: # vse razen zadnjega hočem zaokrožit na 4 decimalna mesta
            df[stolpec] = df[stolpec].apply(lambda x: f'{x:.4f}')

        podatki_za_delnice[oznaka] = df
    
    return podatki_za_delnice


def shrani_tabele_v_csv(podatki_za_delnice, directory = 'podatki_za_delnice_csv'): # za vsak ključ slovarja želim zdej ustvarit tabelo s podatki o danem ključu (delnici)
    import os

    if not os.path.exists(directory): # če imenik še ne obstaja, ga ustvarim
        os.makedirs(directory)

    for oznaka, podatki in podatki_za_delnice.items():
        ime_dat = os.path.join(directory, f'{oznaka}_podatki.csv') # imena datotek, ustvarjena tako, da združim imenik directort pa ime datoteke glede na oznako delnice
        podatki.to_csv(ime_dat, index = True) # shranim tabelo kot csv dat, index = True pomeni, da je vključen tudi indeksni stolpec = stolpec z datumi


# MOJI PODATKI
# oznake = ['AAPL', 'NVDA', 'GOOGL', 'KO', 'BA'] # seznam oznak delnic, katerih podatke hočem

# zacetek = '2023-08-07'
# konec = '2024-08-07'

# podatki_za_delnice = pridobi_podatke(oznake, zacetek, konec)
# shrani_tabele_v_csv(podatki_za_delnice, directory = 'podatki_za_delnice_csv')
# print(podatki_za_delnice)