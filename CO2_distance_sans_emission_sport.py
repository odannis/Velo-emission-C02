import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import seaborn as sns

sns.set_theme(context='talk', style='ticks')


m = 85 # kg masse cycliste + velo
percent_denivele = 0.01 # delta_h sur 100 m / 100 m  (% dénivelé)
v = 20 / 3.6

C_rr = 0.004 # FR = Crr⋅m⋅g  https://fr.wikipedia.org/wiki/R%C3%A9sistance_au_roulement  https://www.velomobil.ch/ch/sites/default/files/images/pages/reifenpruefstand/diagramm_cr_v.jpg
R_t = 0.4 # F = R_T v^2 https://pubmed.ncbi.nlm.nih.gov/468661/ le papier donne 0.2 pour un velo de route. Je prend *2 pour un velo de ville
g = 9.81 # m/s^2
Nombre_d_arret = 4 ## On suppose que le cycliste s'arrete 4 fois et doit donc fournir 4 fois l'énergie cinetique

E_eff = 0.2 # Rendement energétique cycliste https://en.wikipedia.org/wiki/Bicycle_performance or https://pubmed.ncbi.nlm.nih.gov/468661/
food_kgC02_kcal_vegan = 0.6/1000 # https://ourworldindata.org/grapher/ghg-kcal-poore
food_kgC02_kcal_moyen = 1.5/1000 # fig 2 de https://www.connaissancedesenergies.org/sites/default/files/pdf-actualites/etude-cas-impact-carbone-regimes-alimentaires-differencies-2011.pdf
food_kgC02_kcal_boeuf = 3/1000 # fig 2 de https://www.connaissancedesenergies.org/sites/default/files/pdf-actualites/etude-cas-impact-carbone-regimes-alimentaires-differencies-2011.pdf

E_velo_electrique = 0.4 # Rendement vélo 100% électrique à la louche
Electricite_kgC02_jool = 0.1 / (1000 * 60 * 60)  # Electricité francaise kgC02/kwh https://app.electricitymaps.com/zone/FR

temps_sport_journalier_recommande = 225*60/7 # temps sport recommandé par l'OMS https://www.who.int/news-room/fact-sheets/detail/physical-activity
L_sport_jours = v*temps_sport_journalier_recommande


def energie_totale(L, verbose = False):
    E_c = 0.5 * m * v**2 * Nombre_d_arret # Energie cinetique
    E_m = m * g * percent_denivele * L # Energie mécanique
    E_t = R_t * v**2 * L # Energie frottement air
    E_rr = C_rr * m * g * L # Energie frottement roulement
    E_tot = E_c + E_m + E_t + E_rr # Energie totale
    if verbose:
        print("Vitesse : ", v*3.6, "km/h")
        print("Energie cinétique : ", E_c/4184, "kcal")
        print("Energie mécanique : ", E_m/4184, "kcal")
        print("Energie frottement air : ", E_t/4184, "kcal")
        print("ENergie frottement roulement : ", E_rr/4184, "kcal")
        print(f"Energie totale  : {E_tot/4184:.2f} kcal ")
        print(f"Puissance instant : {E_tot*v/L:.2f} W")
        print()
    return E_tot

def C02_from_energie(E_tot, food_kgC02_kcal, verbose = False):
    kg_C02_bike_human = E_tot/4184 * 1/E_eff * food_kgC02_kcal
    kg_C02_bike_electrique = E_tot/E_velo_electrique * Electricite_kgC02_jool
    if verbose:
        print(f"Energie nourriture  : {E_tot/4184 * 1/E_eff:.2f} kcal = {kg_C02_bike_human:.2f} kg CO2")
        print(f"Trajet en vélo electrique : {E_tot/E_velo_electrique/1000 * 1/(60*60):.2f} kWh")
        print(f"Trajet en vélo electrique : {kg_C02_bike_electrique:.3f} kg CO2")
        print()
        print()
    return kg_C02_bike_human, kg_C02_bike_electrique

l_L = np.linspace(1000, 20000, 70)
l_L_km = l_L / 1000
E_sport_recommande = energie_totale(L_sport_jours, verbose=True)
l_kg_C02_bike_human_boeuf, l_kg_C02_bike_human_vegan, l_kg_C02_bike_human_vegan, l_kg_C02_bike_human, l_kg_C02_bike_electrique = [], [], [], [], []

for L in l_L:
    E_tot = energie_totale(L)
    E_bike = max(0, E_tot - E_sport_recommande)
    kg_C02_bike_human, _ = C02_from_energie(E_bike, food_kgC02_kcal_boeuf)
    l_kg_C02_bike_human_boeuf.append(kg_C02_bike_human)
    kg_C02_bike_human, _ = C02_from_energie(E_bike, food_kgC02_kcal_vegan)
    l_kg_C02_bike_human_vegan.append(kg_C02_bike_human)
    kg_C02_bike_human, _ = C02_from_energie(E_bike, food_kgC02_kcal_moyen)
    l_kg_C02_bike_human.append(kg_C02_bike_human)
    _, kg_C02_bike_electrique = C02_from_energie(E_tot, food_kgC02_kcal_moyen)
    l_kg_C02_bike_electrique.append(kg_C02_bike_electrique)

l_kg_auto = 0.2 * l_L_km
l_kg_moto = 0.08 * l_L_km
l_kg_metro = 0.003 * l_L_km 

def plot_all(y_scale = "linear"):
    fig, ax = plt.subplots(figsize=(10, 5))
    #plt.plot(l_L_km, l_kg_auto , label = "Voiture")
    plt.plot(l_L_km, l_kg_moto, label = "Scooter")
    plt.plot(l_L_km, l_kg_C02_bike_human, label = "Cycliste français moyen")
    plt.plot(l_L_km, l_kg_C02_bike_human_vegan, label = "Cycliste vegan")
    plt.plot(l_L_km, l_kg_C02_bike_human_boeuf, label = "Cycliste carnivore")
    plt.plot(l_L_km, l_kg_C02_bike_electrique, label = "Vélo 100% électrique")
    plt.plot(l_L_km, l_kg_metro, label = "Metro")
    plt.xlabel("Distance (km)")
    plt.ylabel("kg CO2")
    plt.yscale(y_scale)

    def add_image(path_image, y_top, index_x = -2, zoom = 0.2):
        x_top = l_L_km[index_x]
        im = plt.imread(path_image)
        imagebox = OffsetImage(im, zoom=zoom)#Annotation box for solar pv logo
        #Container for the imagebox referring to a specific position *xy*.
        ab = AnnotationBbox(imagebox, (x_top, y_top), frameon = False)
        ax.add_artist(ab)

    index_start = -4
    #add_image("images/automobile_1f697.png", l_kg_auto[index_start], index_x=index_start)

    add_image("images/motor-scooter_1f6f5.png", l_kg_moto[index_start], index_x=index_start)

    add_image("images/metro_1f687.png", l_kg_metro[index_start], index_x=index_start, zoom=0.15)

    add_image("images/bicycle_1f6b2.png", l_kg_C02_bike_human[index_start + 1], index_x=index_start)

    add_image("images/bicycle_1f6b2.png", l_kg_C02_bike_human_boeuf[index_start + 1], index_x=index_start)
    add_image("images/cut-of-meat_1f969.png", l_kg_C02_bike_human_boeuf[index_start + 1], zoom=0.15, index_x=index_start + 2)

    add_image("images/bicycle_1f6b2.png", l_kg_C02_bike_human_vegan[index_start + 1], index_x=index_start)
    add_image("images/green-salad_1f957.png", l_kg_C02_bike_human_vegan[index_start + 1], zoom=0.15, index_x=index_start + 2)

    add_image("images/bicycle_1f6b2.png", l_kg_C02_bike_electrique[index_start + 1], index_x=index_start)
    add_image("images/high-voltage_26a1.png", l_kg_C02_bike_electrique[index_start + 1], zoom=0.15, index_x=index_start + 2)

    plt.legend(fontsize=12, loc="upper left")
    plt.title("Comparaison des émissions de CO2 en retirant les émissions \n liées au temps de sport recommandé par l'OMS sur le vélo")
    plt.tight_layout()
    plt.savefig("results/Emmission_C02_distance_avec_sport_OMS_%s.png"%y_scale, dpi=300)
    plt.show()

plot_all(y_scale = "linear")
plot_all(y_scale = "log")