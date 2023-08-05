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

from signaux.signal_gbf import GBF
from signaux.signal_fourier import Fourier
from signaux.signal_sysam import Sysam

import base.utiles_base as utb

class Sysam1Base():
    def __init__(self, liste_signaux, affichage):
        self.sysam = pycan.Sysam("SP5")
        self.affichage = affichage

        if isinstance(liste_signaux, list) and len(liste_signaux)> 0:
            self.liste_signaux = liste_signaux
        else:
            print("Pas de signaux")
            sys.exit()
        if affichage:  
            utb.print_liste(self.liste_signaux)

        self.liste_entrees_simples = utb.lister_test(self.liste_signaux, 
            lambda s: s.voie.tester_entree_simple(),
            lambda s: s.voie.calculer_numero()
            )
        self.liste_entrees_diffs = utb.lister_test(self.liste_signaux, 
            lambda s: s.voie.tester_entree_diff(),
            lambda s: s.voie.calculer_numero()
            )
        self.liste_entrees = utb.lister_test(self.liste_signaux, 
            lambda s: s.voie.tester_entree(),
            lambda s: s.voie.calculer_numero()
            )
        self.liste_sorties = utb.lister_test(self.liste_signaux, 
            lambda s: s.voie.tester_sortie(),
            lambda s: s.voie.calculer_numero()
            )
        self.liste_sortie1 = utb.lister_test(self.liste_sorties, 
            lambda s: s.voie.nom == "SA1",
            lambda s: s.voie.calculer_numero()
            )
        self.liste_sortie2 = utb.lister_test(self.liste_sorties, 
            lambda s: s.voie.nom == "SA2",
            lambda s: s.voie.calculer_numero()
            )
        self.liste_triggers = utb.lister_test(self.liste_signaux, 
            lambda s: s.trigger.tester_trigger(),
            lambda s: s.voie.calculer_numero()
            )
        self.liste_entrees_triggers = utb.lister_test(self.liste_entrees, 
            lambda s: s.trigger.tester_trigger(),
            lambda s: s.voie.calculer_numero()
            )
        self.liste_sorties_triggers = utb.lister_test(self.liste_sorties, 
            lambda s: s.trigger.tester_trigger(),
            lambda s: s.voie.calculer_numero()
            )
        self.liste_paires_signaux_multiplex = utb.lister_paires_test(self.liste_signaux, 
            lambda s1, s2: s1.voie.tester_necessite_multiplexage(s2.voie),
            lambda p: p[0].voie.calculer_numero(),
            lambda s: s.voie.calculer_numero()
            )
        
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        # self.voie.close()
        pass

    def __del__(self):
        self.sysam.stopper_sorties(1, 1)
        self.sysam.fermer()
    
if __name__ == "__main__":

    # liste_tmin_tmax = [0, 2e-3]
    # Te = 1e-4

    # N = 6
    # liste_signaux = []
    # for i in range(N):
    #     liste_signaux.append(GBF(liste_tmin_tmax = liste_tmin_tmax, Te = Te))

    # liste_signaux[0].configurer_voie("SA1", repetition = True)
    # liste_signaux[1].configurer_voie("SA2", repetition = True)
    
    # # s1.configurer_trigger(0.)
    # sysam = Sysam1Base(liste_signaux)
    # del(sysam)

    # liste_signaux[2].configurer_voie("EA1", repetition = True)
    # liste_signaux[3].configurer_voie("DIFF2", repetition = True)

    # sysam = Sysam1Base(liste_signaux)
    # del(sysam)
    
    # liste_signaux[2].configurer_trigger(0.)
    # sysam = Sysam1Base(liste_signaux)
    # del(sysam)

    sysam = pycan.Sysam("SP5")
    sysam.fermer()
