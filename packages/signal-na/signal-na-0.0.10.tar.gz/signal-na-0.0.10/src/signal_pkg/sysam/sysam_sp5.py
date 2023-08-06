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

from signaux.signal_base import SignalBase
from signaux.signal_gbf import GBF
from signaux.signal_fourier import Fourier
from signaux.signal_sysam import Sysam

import base.temps_base
import base.voie_base
import base.utiles_base as utb

import signaux

from sysam.sysam_4_methodes import Sysam4Methodes

__all__ = ["demarrer_sysam"]

 
def demarrer_sysam(*args, **kwargs):
    args = list(args)
    liste_signaux = []
    test_signal = len(args) > 0 and isinstance(args[0], SignalBase)
    if not test_signal:
        print("Quels sont les signaux gérés par sysam?")
        return
    s = args[0]
    while test_signal:
        liste_signaux.append(utb.analyser_args(args, " ", lambda x: isinstance(x, SignalBase), s)[0])
        test_signal = len(args) > 0 and isinstance(args[0], SignalBase)
    affichage = utb.analyser_args_kwargs(args, kwargs, "affichage", lambda x: isinstance(x, bool), True)

    with SysamSP5(liste_signaux, affichage) as sysam:
        pass

# def demarrer_sysam(liste_signaux=None):
#     if __name__ == '__main__':
#         try:
#             sysam = SysamSP5(liste_signaux)
#         except KeyboardInterrupt:
#             print('Interrupted')
#             try:
#                 sys.sys.exit(0)
#             except Systemsys.exit:
#                 os._sys.exit(0)

class SysamSP5(Sysam4Methodes):
    def __init__(self, liste_signaux, affichage):
        Sysam4Methodes.__init__(self, liste_signaux, affichage)

        if "entree" in self.chaine_mode:
            self.sysam.config_entrees(*self.calculer_arguments_config_entrees())
            self.sysam.config_echantillon(*self.calculer_arguments_config_echantillon())

        if "trigger" in self.chaine_mode:
            self.sysam.config_trigger(*self.calculer_arguments_config_trigger())
 
        if "sortie1" in self.chaine_mode and "synchrone" not in self.chaine_mode:
            self.sysam.config_sortie(*self.calculer_arguments_config_sortie(1))

        if "sortie2" in self.chaine_mode and "synchrone" not in self.chaine_mode:
            self.sysam.config_sortie(*self.calculer_arguments_config_sortie(2))


        if "synchrone" in self.chaine_mode:
            self.sysam.acquerir_avec_sorties(*self.calculer_arguments_acquerir_avec_sorties())
            self.mettre_a_jour_entrees()
        elif "entree" in self.chaine_mode and "sortie" in self.chaine_mode:
            tmin, tmax = self.base_de_temps_entrees.calculer_liste_tmin_tmax()
            self.sysam.declencher_sorties(*self.calculer_arguments_declencher_sorties())
            if tmin != 0:
                time.sleep(tmin)
            self.sysam.acquerir()
            self.mettre_a_jour_entrees()
        elif "entree" in self.chaine_mode and "sortie" not in self.chaine_mode:
            tmin, tmax = self.base_de_temps_entrees.calculer_liste_tmin_tmax()
            self.sysam.acquerir()
            self.mettre_a_jour_entrees()            
        elif "sortie" in self.chaine_mode and "entree" not in self.chaine_mode:
            self.sysam.declencher_sorties(*self.calculer_arguments_declencher_sorties())
            test_fin = False
            while not test_fin:
                chaine = input("On arrête les signaux o/N?")
                if chaine == "o" or chaine == "O":
                    test_fin = True

    def mettre_a_jour_entrees(self):
        temps = self.sysam.temps()
        entrees = self.sysam.entrees()
        voies = self.calculer_arguments_config_entrees()[0]
        # print("mettre a jour entrees ", self.chaine_mode)
        if "synchrone" not in self.chaine_mode:
            Nsysam = np.max(base.temps_base.BaseTemps.liste_bases_de_temps_sysam) + 1
            base.temps_base.BaseTemps.liste_bases_de_temps_sysam.append(Nsysam)
        else:
            Nsysam = 0

        for s in self.liste_entrees:
            voie = s.voie.calculer_numero()
            indice = voies.index(voie)
            s.vecteur_signal = np.array(entrees[indice])
            s.base_de_temps = base.temps_base.convertir_vecteur_t_vers_base_de_temps(np.array(temps[indice]))
            s.base_de_temps.Nsysam = Nsysam

if __name__ == "__main__":
    # def faire_une_mesure(f, Ue, tau, n_periodes):
    #     T = 1/f
    #     Te = max(T/100, 2e-7)
    #     s = GBF("cosinus", F = f, liste_tmin_tmax = [0, T], Te = Te)    
    #     s.configurer_voie("SA1", repetition = True)
    #     print("se")
    #     se = Sysam("EA0", liste_tmin_tmax = [tau, tau + n_periodes*T], Te = Te)
    #     print("ss")
    #     ss = Sysam("EA1", liste_tmin_tmax = [tau, tau + n_periodes*T], Te = Te)
    #     se.configurer_trigger(0)
    #     sysam = SysamSP5([s, se, ss])

    #     Vppe = se.mesurer_Vpp()
    #     Vpps = ss.mesurer_Vpp()
    #     G = Vpps / Vppe
    #     phi = ss.mesurer_dephasage_par_rapport_a(se)
    #     Sysam.tracer_signaux([se, ss])
    #     return G, phi

    # def tracer_bode(liste_fmin_fmax, n_points, Ue, tau, n_periodes):
    #     fmin, fmax = liste_fmin_fmax
    #     vecteur_f = np.logspace(np.log10(fmin), np.log10(fmax), n_points)
    #     vecteur_G = np.zeros(n_points)
    #     vecteur_phi = np.zeros(n_points)
        
    #     for i in range(len(vecteur_f)):
    #         f = vecteur_f[i]
    #         G, phi =  faire_une_mesure(f, Ue, tau, n_periodes)
    #         print("f = {0} ; G = {1} ; phi = {2} rad".format(f, G, phi))
    #         vecteur_G[i], vecteur_phi[i] = G, phi
    #     plt.subplot(121)   
    #     plt.semilogx(vecteur_f, 20*np.log10(vecteur_G))
    #     plt.subplot(122)   
    #     plt.semilogx(vecteur_f, vecteur_phi)
    #     plt.show()

    # # tracer_bode([50, 80000], 10, 9, 1e-1, 30)
    # Ts2 = 0.01
    # F = 1/Ts2/2
    # ss = GBF("carre", F = F, liste_tmin_tmax = [0, 1/F], Te = 1e-4)
    # ss.configurer_voie("SA1", repetition = False)
    # sss = Sysam("EA0", liste_tmin_tmax = [0.001, 3*Ts2], Te = 1e-4)
    # ssss = Sysam("EA1", liste_tmin_tmax = [0.001, 3*Ts2], Te = 1e-4)
    # demarrer_sysam([ss, sss, ssss])
    
    # print(ss.base_de_temps.Nsysam)
    # print(sss.base_de_temps.Nsysam)
    # print(ssss.base_de_temps.Nsysam)

    # Sysam.tracer_signaux([sss,ssss], superposition = False)
    T1 = 1e-3
    sortie1 = GBF(F = 1/T1, liste_tmin_tmax = [0, T1], Te = 2e-7)
    sortie1.configurer_voie("SA1", repetition = True)

    entree1 = Sysam("DIFF3", liste_tmin_tmax = [0, 5*T1], Te = 1e-7)
    entree1.configurer_trigger(0)

    T2 = 2.5e-3
    sortie2 = GBF(F = 1/T2, liste_tmin_tmax = [0, T2], Te = 7e-7)
    sortie2.configurer_voie("SA2", repetition = True)

    entree2 = Sysam("EA2", liste_tmin_tmax = [0, 5*T1], Te = 1e-7)
    
    demarrer_sysam(entree1, sortie1, entree2, sortie2, True)
    GBF.tracer_signaux(sortie2, entree1, entree2, titre = "zoo")