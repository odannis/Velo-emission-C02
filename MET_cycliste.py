import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import seaborn as sns

sns.set_theme(context='talk', style='ticks')

m_cycliste = 70 # kg
m = 85 # kg masse cycliste + velo
delta_h = 10 # m dénivelé
L = 10000 # m distance parcourue

C_rr = 0.005 # FR = Crr⋅m⋅g  https://fr.wikipedia.org/wiki/R%C3%A9sistance_au_roulement  https://www.velomobil.ch/ch/sites/default/files/images/pages/reifenpruefstand/diagramm_cr_v.jpg
R_t = 0.4 # F = R_T v^2 https://pubmed.ncbi.nlm.nih.gov/468661/ le papier donne 0.2 pour un velo de route. Je prend *2 pour un velo de ville
g = 9.81 # m/s^2
Nombre_d_arret = 4 ## On suppose que le cycliste s'arrete 4 fois et doit donc fournir 4 fois l'enegie cinetique

E_eff = 0.2 # Rendement energétique cycliste https://en.wikipedia.org/wiki/Bicycle_performance or https://pubmed.ncbi.nlm.nih.gov/468661/

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

l_v = np.linspace(12, 27) / 3.6
l_MET = []
for v in l_v:
    E_tot = energie_totale(v, verbose=True) / 4184 # kcal
    E_nourriture = E_tot / E_eff # Perte lors de la conversion
    MET = 1 + E_nourriture / (m_cycliste * L/v) * (3600)   # kcal/kg/h (Metabolisme + energie dépensée)
    l_MET.append(MET)

def plot_all(y_scale = "linear"):
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.plot(l_v*3.6, l_MET, label="Energie totale")
    plt.plot([16], [4], marker='o', markersize=5, color="red", label="Donnée wikipedia : Vélo de plaisance, <16 km/h = 4 MET")
    plt.xlabel("Vitesse (km/h)")
    plt.ylabel("MET (kcal/kg/h)")
    plt.yscale(y_scale)

    plt.title(f"MET pour un cycliste sur plat ({delta_h/L * 100:.2f} % de pente) selon sa vitesse ", fontsize=14)
    plt.legend(fontsize=12, loc="upper left")
    plt.tight_layout()
    plt.savefig("results/MET_%s.png"%y_scale, dpi=500)
    plt.show()

plot_all(y_scale = "linear")