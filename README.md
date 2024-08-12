# Opis

Avtorica: Anamarija Potokar

Pri svoji projektni nalogi pri Uvodu v programiranje sem uvozila, shranila in analizirala podatke o delnicah izbranih petih podjetij za obdobje enega leta med določenima datumoma. S spletne strani [Yahoo Finance](https://finance.yahoo.com) sem uvozila in izluščila podatke, ki so me zanimali za nadaljnjo analizo: cene ob začetku in koncu trgovalnega dne, najnižje in najvišje cene ter volumen oziroma obseg trgovanja. Podatke za posamezno delnico sem shranila tudi v CSV datoteko s tabelo vrednosti za večjo preglednost. 

# Navodila za uporabo

V datoteki pridobivanje_podatkov.py se nahaja koda za uvoz in shrambo podatkov v CSV datoteko, kjer si lahko uporabnik sam izbere podjetja, katerih delnice ga zanimajo, ter preučevano časovno obdobje. Pri tem mora paziti, da začetni in končni datum zapiše v pravilnem formatu oblike leto-dan-mesec ter pravilne oznake za delnice podjetij, o katerih se lahko prepriča na [Yahoo Finance](https://finance.yahoo.com).
V datoteki analiza_podatkov.py se nahaja koda za izračun raznih vrednosti in kazalnikov, ki pripomorejo k boljšemu poznavanju lastnosti in obnašanja posamezne delnice ter pomagajo pri investicijskih odločitvah s preprosto simulacijo avtomatiziranega trgovanja.
V datoteki predstavitev.ipynb pa si lahko uporabnik pogleda rezultate opravljenih analiz.
