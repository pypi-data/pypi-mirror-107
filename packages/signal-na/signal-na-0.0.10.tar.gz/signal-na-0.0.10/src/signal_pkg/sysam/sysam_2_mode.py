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


from sysam.sysam_1_base import Sysam1Base
from signaux.signal_gbf import GBF
from signaux.signal_fourier import Fourier
from signaux.signal_sysam import Sysam


import base.utiles_base as utb

class Sysam2Mode(Sysam1Base):
    def __init__(self, liste_signaux, affichage):
        Sysam1Base.__init__(self, liste_signaux, affichage)
        self.generer_chaine_mode()
        if self.affichage:
            print(self.chaine_mode)

    def generer_chaine_mode(self):

        test_multiplex = True if self.liste_paires_signaux_multiplex else False
        test_entree = True if self.liste_entrees else False
        test_sortie = True if self.liste_sorties else False
        test_sortie1 = True if self.liste_sortie1 else False
        test_sortie2 = True if self.liste_sortie2 else False
        test_trigger = True if self.liste_triggers else False

        test_synchrone = False
        if not test_trigger and test_entree and test_sortie:
            if self.liste_entrees_simples: 
                if self.liste_entrees_simples[0].base_de_temps.Nmin == 0:
                    test_synchrone = True
            if self.liste_entrees_diffs: 
                if self.liste_entrees_diffs[0].base_de_temps.Nmin == 0:
                    test_synchrone = True

        chaine_mode = ""
        chaine_mode = chaine_mode + "-entree-" if test_entree else chaine_mode
        chaine_mode = chaine_mode + "-sortie1-" if test_sortie1 else chaine_mode
        chaine_mode = chaine_mode + "-sortie2-" if test_sortie2 else chaine_mode
        chaine_mode = chaine_mode + "-multiplex-" if test_multiplex else chaine_mode
        chaine_mode = chaine_mode + "-synchrone-" if test_synchrone else chaine_mode
        chaine_mode = chaine_mode + "-trigger-" if test_trigger else chaine_mode
        
        self.chaine_mode = chaine_mode


if __name__ == "__main__":

    liste_tmin_tmax = [0, 2e-3]
    Te = 1e-4

    N = 6
    liste_signaux = []
    for i in range(N):
        liste_signaux.append(GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te))

    liste_signaux[0].configurer_voie("SA1", repetition = True)
    liste_signaux[1].configurer_voie("SA2", repetition = True)
    
    sysam = Sysam2Mode(liste_signaux)
    del(sysam)

    liste_signaux[2].configurer_voie("EA1", repetition = True)
    liste_signaux[3].configurer_voie("DIFF2", repetition = True)

    sysam = Sysam2Mode(liste_signaux)
    del(sysam)
    
    liste_signaux[2].configurer_trigger(0.)
    sysam = Sysam2Mode(liste_signaux)
    del(sysam)

    liste_signaux[4].configurer_voie("EA5", repetition = True)
    sysam = Sysam2Mode(liste_signaux)
    del(sysam)


