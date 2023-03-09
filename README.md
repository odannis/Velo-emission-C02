# Émission CO2 vélo via la nourriture consommée par le cycliste

Dernierement, j'ai été surpris par l'émission de C02 d'un cycliste donnée dans certaines sources (dont un papier Nature) :

 - https://www.nature.com/articles/s41598-020-66170-y
 - https://www.auto-moto.com/actualite/environnement/lautomobile-plus-ecolo-que-le-velo-31204.html
 - https://twitter.com/HugoMe/status/1448047429912342531

La pluplart part de la consommation d'un cycliste mesuré par la science du sport. Un valeur typique, selon l'intensité du cycliste, se situe entre 4 MET et 8 MET. Ou 1 MET (Metabolic equivalent of task) = 1 kcal / (kg * h) correspond à la consommation au repos d'un humain par kilogrammes et heure. [wiki](https://fr.wikipedia.org/wiki/%C3%89quivalent_m%C3%A9tabolique). 

Par exemple, en prenant un MET de 8 pour 30 min de vélo pour quelqu'un de 80 kg, on trouve $E_{depensee} = 8 * 80 / 2 = 320 kcal$. J'ai été très surpris par cette valeur qui correspond à manger 1/3 en plus (ref 1800 kcal) après 30 min de vélo. Donc, j'ai décidé d'essayer de retrouver cette valuer avec une description physique d'un homme sur un vélo.

## Description 

Rapidement, je considère la variation d'énergie cinétique, potentiel de pesanteur, travail des forces de frottement de l'air et de la résistance au roulement. Ce qui donne, en supposant la vitesse constante :

$$E_{tot} = \frac{n_{stop}}{2} m v^2 + m g z + R_t v^2 L + C_{rr} m g L$$

ou $n_{stop}$ est le nombre de fois ou on s'arrete lors du trajet, $L$ la longeur du trajet, $R_t$ un coefficient prenant en compte le frottement de l'air, et $C_{rr}$ le coefficient de réssistance au roulement. Plus de détail sur le choix des valeurs dans le code :

```
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
```
## Comparaison des émissions de CO2 par km pour différents moyens de transport



![plot](./result_linear.png)