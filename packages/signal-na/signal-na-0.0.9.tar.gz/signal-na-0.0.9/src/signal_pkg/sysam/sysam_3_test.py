import numpy as np
import matplotlib.pyplot as plt

import os, sys, time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

try:
    import pycanum.main as pycan
except:
    # print("Attention: la bibliothèque pycanum n'est pas installée")
    # print(" -> Fonctionnement en mode émulation")
    import acquisition.emulateur_sysam_sp5 as pycan

from sysam.sysam_2_mode import Sysam2Mode

from signaux.signal_gbf import GBF
from signaux.signal_fourier import Fourier
from signaux.signal_sysam import Sysam

import base.voie_base
import base.utiles_base as utb


class Sysam3Test(Sysam2Mode):
    def __init__(self, liste_signaux, affichage):
        Sysam2Mode.__init__(self, liste_signaux, affichage)
        if self.tester_liste_signaux():
            self.test_signaux = True
        else:
            self.test_signaux = False
            sys.exit()


    ##################################################################################################################
    ## tester liste signaux
    ##################################################################################################################
    def tester_liste_signaux(self):
        # Générer Te_entrées_min
        liste_Te = [0.]
        if "entree" in self.chaine_mode:
            liste_Te.append(base.voie_base.Te_direct)
        if "multiplex" in self.chaine_mode:
            liste_Te.append(base.voie_base.Te_multiplex)
        if "synchrone" in self.chaine_mode:
            liste_Te.append(base.voie_base.Te_sortie)
        self.Te_entree_min = np.max(liste_Te)

        # Générer Te_sorties_min
        liste_Te = [0.]
        if "sortie" in self.chaine_mode:
            liste_Te.append(base.voie_base.Te_sortie)
        if "multiplex" in self.chaine_mode and "synchrone" in self.chaine_mode:
            liste_Te.append(base.voie_base.Te_multiplex)
        self.Te_sortie_min = np.max(liste_Te)

        # Générer base de temps entrées
        if self.liste_entrees_simples:
            self.base_de_temps_entrees = self.liste_entrees_simples[0].base_de_temps
        elif self.liste_entrees_diffs:
            self.base_de_temps_entrees = self.liste_entrees_diffs[0].base_de_temps
        else:
            self.base_de_temps_entrees = None

        # tester validite des noms des voies
        liste_signaux_noms_voies_ko = utb.lister_test(self.liste_signaux, 
            lambda s: s.voie.tester_sysam() and (not s.voie.tester_nom()),
            lambda s: s.voie.calculer_numero()
            )
        if liste_signaux_noms_voies_ko:
            print("Problème avec les noms des voies voie suivants:")
            utb.print_liste(liste_signaux_noms_voies_ko, begin = " -> ")
            return False

        # tester compatibilités entre les noms des voies
        liste_paires_signaux_noms_voies_ko = utb.lister_paires_test(self.liste_signaux, 
            lambda s1, s2: s1.voie.tester_sysam() and s2.voie.tester_sysam() and not s1.voie.tester_compatibilite_nom(s2.voie),
            lambda p: p[0].voie.calculer_numero(),
            lambda s: s.voie.calculer_numero()
            )
        if liste_paires_signaux_noms_voies_ko:
            print("Problème de compatibilité entre les noms des paires de voies voie suivants:")
            utb.print_liste_de_listes(liste_paires_signaux_noms_voies_ko, begin1 = " -> ")
            return False

        # tester trigger
        if self.liste_sorties_triggers:
            print("Problèmes des triggers sont affectés sur des sorties:")
            utb.print_liste(self.liste_sorties_triggers, begin = " -> ")
            return False

        if len(self.liste_entrees_triggers) > 1:
            print("Problèmes plusieurs triggers sont affectés sur des entrées:")
            utb.print_liste(self.liste_entrees_triggers, begin = " -> ")
            return False

        # tester entrees echantillonnés trop vite
        liste_entrees_echantillonnees_trop_vite = utb.lister_test(self.liste_entrees, 
            lambda s: s.base_de_temps.Te < self.Te_entree_min,
            lambda s: s.voie.calculer_numero()
            )
        if liste_entrees_echantillonnees_trop_vite:
            print("Les entrees suivantes ne respectent pas Te > {0} s".format(self.Te_entree_min))
            utb.print_liste(liste_entrees_echantillonnees_trop_vite, begin = " -> ")
            return False

        # tester sorties echantillonnées trop vite
        liste_sorties_echantillonnees_trop_vite = utb.lister_test(self.liste_sorties, 
            lambda s: s.base_de_temps.Te < self.Te_sortie_min,
            lambda s: s.voie.calculer_numero()
            )
        if liste_sorties_echantillonnees_trop_vite:
            print("Les sorties suivantes ne respectent pas Te > {0} s".format(self.Te_sortie_min))
            utb.print_liste(liste_sorties_echantillonnees_trop_vite, begin = " -> ")
            return False

        # tester compatibilités entre les bases de temps des entrées
        liste_paires_entrees_bases_de_temps_ko = utb.lister_paires_test(self.liste_entrees, 
            lambda s1, s2: s1.base_de_temps != s2.base_de_temps,
            lambda p: p[0].voie.calculer_numero(),
            lambda s: s.voie.calculer_numero()
            )
        if liste_paires_entrees_bases_de_temps_ko:
            print("Problème de compatibilité entre les bases de temps des paires d'entrées suivantes:")
            utb.print_liste_de_listes(liste_paires_entrees_bases_de_temps_ko, begin1 = " -> ")
            return False

        # tester validite des bases de temps de sortie
        if "synchrone" in self.chaine_mode:
            liste_sorties_echantillonnage_ko = utb.lister_test(self.liste_sorties, 
                lambda s: s.base_de_temps.Te != self.base_de_temps_entrees.Te,
                lambda s: s.voie.calculer_numero()
                )
            if liste_sorties_echantillonnage_ko:
                print("Problème de périodes d'échantillonnage sur les sorties suivantes (ES synchrones):")
                utb.print_liste(liste_sorties_echantillonnage_ko, begin = " -> ")
                return False

        # tester si les sorties commencent à t=0
        liste_sorties_tardives = utb.lister_test(self.liste_sorties, 
            lambda s: s.base_de_temps.Nmin != 0,
            lambda s: s.voie.calculer_numero()
            )
        if liste_sorties_tardives:
            print("Les sorties suivantes ne débutent pas à t=0:")
            utb.print_liste(liste_sorties_tardives, begin = " -> ")
            return False


        # tester espace memoire
        liste_signaux_sysam = utb.lister_test(
            self.liste_signaux, 
            lambda s: s.voie.tester_sysam(),
            lambda s: s.voie.calculer_numero()
            )
        liste_N_ech = [s.base_de_temps.N for s in liste_signaux_sysam]
        if np.sum(liste_N_ech) > base.voie_base.N_ech_max:
            print("Trop d'échantillons stockés en mémoire (max = {0})".format(base.voie_base.N_ech_max))
            for i in range(len(liste_signaux_sysam)):
                N1, N2, N3 = 15, 20, 8
                chaine = " -> {0:" + str(N1) + "} {1} {2:" + str(N3) + "}"
                print(chaine.format(str(liste_signaux_sysam[i]), "."*N2, liste_N_ech[i]))
            print(" "*(N1+N2+5), "-"*N3)
            chaine = " "*(N1+N2+6) + "{0:" +str(N3) + "}"
            print(chaine.format(np.sum(liste_N_ech)))
            return False

        return True

if __name__ == "__main__":

    liste_tmin_tmax = [0, 2e-3]
    Te = 1e-4

    N = 10
    liste_signaux = []
    for i in range(N):
        liste_signaux.append(GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te))

    # # Test noms KO
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA3", repetition = True)
    # liste_signaux[2].configurer_voie("EA12", repetition = True)
    # liste_signaux[3].configurer_voie("DIFF5", repetition = True)
    
    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)


    # # Test paires noms incompatibles 
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA1", repetition = True)
    # liste_signaux[2].configurer_voie("EA5", repetition = True)
    # liste_signaux[3].configurer_voie("EA5", repetition = True)
    # liste_signaux[4].configurer_voie("DIFF1", repetition = True)
    # liste_signaux[5].configurer_voie("EA0", repetition = True)

    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)

    # # tester trigger sortie
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA2", repetition = True)
    # liste_signaux[2].configurer_voie("EA1", repetition = True)
    # liste_signaux[3].configurer_voie("EA5", repetition = True)
    # liste_signaux[4].configurer_voie("DIFF3", repetition = True)

    # liste_signaux[0].configurer_trigger(0.)
    # liste_signaux[1].configurer_trigger(0.)
    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)

    # # tester trigger entrees
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA2", repetition = True)
    # liste_signaux[2].configurer_voie("EA1", repetition = True)
    # liste_signaux[3].configurer_voie("EA5", repetition = True)
    # liste_signaux[4].configurer_voie("DIFF3", repetition = True)

    # liste_signaux[2].configurer_trigger(0.)
    # liste_signaux[3].configurer_trigger(0.)
    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)


    # # tester entrees echantillonnées trop vite
    # Te2 = 1e-7
    # liste_signaux[2] = GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te2)
    # liste_signaux[4] = GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te2)
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA2", repetition = True)
    # liste_signaux[2].configurer_voie("EA1", repetition = True)
    # liste_signaux[3].configurer_voie("EA5", repetition = True)
    # liste_signaux[4].configurer_voie("DIFF3", repetition = True)

    # liste_signaux[3].configurer_trigger(0.)
    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)

    # # tester sorties echantillonnées trop vite
    # Te2 = 1e-7
    # liste_signaux[0] = GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te2)
    # liste_signaux[1] = GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te2)
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA2", repetition = True)
    # liste_signaux[2].configurer_voie("EA1", repetition = True)
    # liste_signaux[3].configurer_voie("EA5", repetition = True)
    # liste_signaux[4].configurer_voie("DIFF3", repetition = True)

    # liste_signaux[3].configurer_trigger(0.)
    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)

    # # tester compatibilité bases de temps des entrées
    # Te2 = 1e-5
    # liste_signaux[2] = GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te2)
    # liste_signaux[4] = GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te2)
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA2", repetition = True)
    # liste_signaux[2].configurer_voie("EA1", repetition = True)
    # liste_signaux[3].configurer_voie("EA5", repetition = True)
    # liste_signaux[4].configurer_voie("DIFF3", repetition = True)

    # liste_signaux[3].configurer_trigger(0.)
    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)

    # # tester compatibilité bases de temps des sorties Te entree = Te sortie si synchrone
    # Te2 = 1e-5
    # liste_signaux[0] = GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te2)
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA2", repetition = True)
    # liste_signaux[2].configurer_voie("EA1", repetition = True)
    # liste_signaux[3].configurer_voie("EA5", repetition = True)
    # liste_signaux[4].configurer_voie("DIFF3", repetition = True)

    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)

    # # tester compatibilité bases de temps des sorties sorties tardives
    # liste_tmin_tmax2 = [1e-2, 8e-2]
    # liste_signaux[0] = GBF(liste_tmin_tmax = liste_tmin_tmax2, Te = Te)
    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA2", repetition = True)
    # liste_signaux[2].configurer_voie("EA1", repetition = True)
    # liste_signaux[3].configurer_voie("EA5", repetition = True)
    # liste_signaux[4].configurer_voie("DIFF3", repetition = True)

    # sysam = Sysam3Test(liste_signaux)
    # del(sysam)

    # tester espace mémoire
    liste_tmin_tmax2 = [0, 27]
    liste_signaux[0] = GBF(liste_tmin_tmax = liste_tmin_tmax2, Te = Te)
    
    liste_signaux[0].configurer_voie("SA1", repetition = True)
    liste_signaux[1].configurer_voie("SA2", repetition = True)
    liste_signaux[2].configurer_voie("EA1", repetition = True)
    liste_signaux[3].configurer_voie("EA5", repetition = True)
    liste_signaux[4].configurer_voie("DIFF3", repetition = True)

    sysam = Sysam3Test(liste_signaux)
    del(sysam)

