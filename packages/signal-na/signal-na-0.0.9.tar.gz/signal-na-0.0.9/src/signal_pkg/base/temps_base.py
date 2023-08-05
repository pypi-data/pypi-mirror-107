import numpy as np
import copy

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import base.constantes_base as cst

def convertir_vecteur_t_vers_base_de_temps(vecteur_t):
    vecteur_Te = vecteur_t[1:] - vecteur_t[:-1]
    bdt = BaseTemps(Te = vecteur_Te.mean())
    bdt.Nmin = bdt.calculer_n(vecteur_t[0])
    bdt.Nmax = bdt.calculer_n(vecteur_t[-1])+1
    bdt.N = bdt.convertir_n_vers_i(bdt.Nmax)
    return bdt


class BaseTemps():
    Panalog = cst.Panalog   
    Ta = cst.Ta

    liste_bases_de_temps_sysam = [0]

    def __init__(self, liste_tmin_tmax = cst.liste_tmin_tmax, Te = cst.Te):
        """
        Initialisation d'une base de temps:
        """
        tmin, tmax = liste_tmin_tmax
        self.NTa = int(np.round(Te / self.Ta))
        self.Te = self.NTa*self.Ta
        self.Nmin, self.Nmax = int(np.ceil(tmin/Te)), int(np.ceil(tmax/Te))
        self.N = self.convertir_n_vers_i(self.Nmax)
        self.Nsysam = 0

    def calculer_n(self, t):
        """
            Détermine l'indice, n, correspondant à t
        """
        return int(np.round(t/self.Te))

    def convertir_n_vers_i(self, n):
        return n-self.Nmin

    def convertir_i_vers_n(self, i):
        return self.Nmin + i

    def calculer_liste_tmin_tmax(self):
        return self.Nmin*self.Te, self.Nmax*self.Te
        
    def calculer_vecteur_n(self, liste_imin_imax = [None, None]):
        """
            Renvoie le vecteur des indices n présents dans la base de temps entre les indices imin et imax
        """
        imin, imax = liste_imin_imax
        
        if imin == None:
            imin = 0
        if imax == None:
            imax = self.convertir_n_vers_i(self.Nmax)
        Nmin, Nmax = self.convertir_i_vers_n(imin), self.convertir_i_vers_n(imax)

        return np.arange(Nmin, Nmax)*self.NTa

    def calculer_vecteur_t(self, liste_imin_imax = [None, None]):
        """
            Renvoie le vecteur des instants présents dans la base de temps
        """
        return self.calculer_vecteur_n(liste_imin_imax)*self.Ta

    def calculer_t(self, n):
        return n*self.Te

    def copier(self):
        return copy.deepcopy(self)

    def __str__(self):
        return str([self.Nmin, self.Nmax, self. NTa, self.Nsysam])

    def __eq__(self, other):
        return self.Nmin == other.Nmin and self.Nmax == other.Nmax and  self.NTa == other.NTa and  self.Nsysam == other.Nsysam 

if __name__ == "__main__":
    Te = 1e-1
    liste_tmin_tmax = 0.09, 2.99
    bdt = BaseTemps(liste_tmin_tmax, Te)

    vecteur_n1 = bdt.calculer_vecteur_n()
    vecteur_n2 = bdt.calculer_vecteur_n([2,5])

    vecteur_t = bdt.calculer_vecteur_t()

    bdt2 = convertir_vecteur_t_vers_base_de_temps(vecteur_t)

    print("NTa", bdt.NTa, bdt2.NTa)
    print("Nmin", bdt.Nmin, bdt2.Nmin)
    print("Nmax", bdt.Nmax, bdt2.Nmax)
    
