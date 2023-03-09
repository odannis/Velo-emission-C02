import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import seaborn as sns

sns.set_theme(context='talk', style='ticks')

m = 85 # kg masse cycliste + velo
delta_h = 10 # m dénivelé
L = 10000 # m distance parcourue

C_rr = 0.005 # FR = Crr⋅m⋅g  https://fr.wikipedia.org/wiki/R%C3%A9sistance_au_roulement  https://www.velomobil.ch/ch/sites/default/files/images/pages/reifenpruefstand/diagramm_cr_v.jpg
R_t = 0.4 # F = R_T v^2 https://pubmed.ncbi.nlm.nih.gov/468661/ le papier donne 0.2 pour un velo de route. Je prend *2 pour un velo de ville
g = 9.81 # m/s^2
Nombre_d_arret = 4 ## On suppose que le cycliste s'arrete 4 fois et doit donc fournir 4 fois l'enegie cinetique

E_eff = 0.2 # Rendement energétique cycliste https://en.wikipedia.org/wiki/Bicycle_performance or https://pubmed.ncbi.nlm.nih.gov/468661/
food_kgC02_kcal_vegan = 0.6/1000 # https://ourworldindata.org/grapher/ghg-kcal-poore
food_kgC02_kcal_moyen = 1.5/1000 # fig 2 de https://www.connaissancedesenergies.org/sites/default/files/pdf-actualites/etude-cas-impact-carbone-regimes-alimentaires-differencies-2011.pdf
food_kgC02_kcal_boeuf = 3/1000 # fig 2 de https://www.connaissancedesenergies.org/sites/default/files/pdf-actualites/etude-cas-impact-carbone-regimes-alimentaires-differencies-2011.pdf

E_velo_electrique = 0.4 # Rendement vélo 100% électrique à la louche
Electricite_kgC02_jool = 0.1 / (1000 * 60 * 60)  # Electricité francaise kgC02/kwh https://app.electricitymaps.com/zone/FR


def energie_totale(v, verbose = False):
    E_c = 0.5 * m * v**2 * Nombre_d_arret # Energie cinetique
    E_m = m * g * delta_h # Energie mécanique
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

l_v = np.linspace(12, 27) / 3.6
l_kg_C02_bike_human_boeuf, l_kg_C02_bike_human_vegan, l_kg_C02_bike_human_vegan, l_kg_C02_bike_human, l_kg_C02_bike_electrique = [], [], [], [], []
for v in l_v:
    E_tot = energie_totale(v, verbose=True)
    kg_C02_bike_human, _ = C02_from_energie(E_tot, food_kgC02_kcal_boeuf)
    l_kg_C02_bike_human_boeuf.append(kg_C02_bike_human/L * 1000)
    kg_C02_bike_human, _ = C02_from_energie(E_tot, food_kgC02_kcal_vegan)
    l_kg_C02_bike_human_vegan.append(kg_C02_bike_human/L * 1000)
    kg_C02_bike_human, kg_C02_bike_electrique = C02_from_energie(E_tot, food_kgC02_kcal_moyen, verbose=True)
    l_kg_C02_bike_human.append(kg_C02_bike_human/L * 1000)
    l_kg_C02_bike_electrique.append(kg_C02_bike_electrique/L * 1000)

def plot_all(y_scale = "linear"):
    fig, ax = plt.subplots(figsize=(10, 5))
    #plt.plot([l_v[0]*3.6, l_v[-1]*3.6], [0.2, 0.2], label = "Voiture")
    plt.plot([l_v[0]*3.6, l_v[-1]*3.6], [0.08, 0.08], label = "Scooter")
    plt.plot(l_v*3.6, l_kg_C02_bike_human, label = "Cycliste français moyen")
    plt.plot(l_v*3.6, l_kg_C02_bike_human_vegan, label = "Cycliste vegan")
    plt.plot(l_v*3.6, l_kg_C02_bike_human_boeuf, label = "Cycliste carnivore")
    plt.plot(l_v*3.6, l_kg_C02_bike_electrique, label = "Vélo 100% électrique")
    plt.plot([l_v[0]*3.6, l_v[-1]*3.6], [0.003, 0.003], label = "Metro")
    plt.xlabel("Vitesse (km/h)")
    plt.ylabel("kg CO2 / km")
    plt.yscale(y_scale)

    def add_image(path_image, y_top, index_x = -2, zoom = 0.2):
        x_top = l_v[index_x]*3.6*1
        im = plt.imread(path_image)
        imagebox = OffsetImage(im, zoom=zoom)#Annotation box for solar pv logo
        #Container for the imagebox referring to a specific position *xy*.
        ab = AnnotationBbox(imagebox, (x_top, y_top), frameon = False)
        ax.add_artist(ab)

    index_start = -2
    #add_image("images/automobile_1f697.png", 0.2, index_x=index_start)

    add_image("images/motor-scooter_1f6f5.png", 0.08, index_x=index_start)

    add_image("images/metro_1f687.png", 0.003, index_x=index_start, zoom=0.15)

    add_image("images/bicycle_1f6b2.png", l_kg_C02_bike_human[index_start + 1], index_x=index_start)

    add_image("images/bicycle_1f6b2.png", l_kg_C02_bike_human_boeuf[index_start + 1], index_x=index_start)
    add_image("images/cut-of-meat_1f969.png", l_kg_C02_bike_human_boeuf[index_start + 1], zoom=0.15, index_x=index_start + 1)

    add_image("images/bicycle_1f6b2.png", l_kg_C02_bike_human_vegan[index_start + 1], index_x=index_start)
    add_image("images/green-salad_1f957.png", l_kg_C02_bike_human_vegan[index_start + 1], zoom=0.15, index_x=index_start + 1)

    add_image("images/bicycle_1f6b2.png", l_kg_C02_bike_electrique[index_start + 1], index_x=index_start)
    add_image("images/high-voltage_26a1.png", l_kg_C02_bike_electrique[index_start + 1], zoom=0.15, index_x=index_start + 1)

    plt.title("Comparaison des émissions de CO2 par km pour différents moyens de transport", fontsize=14)
    plt.legend(fontsize=12, loc="upper left")
    plt.tight_layout()
    plt.savefig("results/C02_km_%s.png"%y_scale, dpi=300)
    plt.show()

plot_all(y_scale = "linear")
plot_all(y_scale = "log")