#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:43:58 2019

@author: nicolas
"""
import time

import os, sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import base.constantes_base as cst
import base.utiles_base as utb
from base.temps_base import BaseTemps
from signaux.signal_complet import SignalComplet



import matplotlib.pyplot as plt
 
__all__ = ["Fourier"]




class Fourier(SignalComplet):
    def __init__(self, F, liste_an, liste_bn, liste_tmin_tmax = cst.liste_tmin_tmax, Te = cst.Te, nom = ""):
        base_de_temps_periode = BaseTemps([0, 1/F], Te)
        base_de_temps = BaseTemps(liste_tmin_tmax, Te)

        Nperiode = base_de_temps_periode.convertir_n_vers_i(base_de_temps_periode.Nmax)
        Nsignal = base_de_temps.convertir_n_vers_i(base_de_temps.Nmax)

        vecteur_t_periode = base_de_temps_periode.calculer_vecteur_t()
        
        a0 = 0
        if len(liste_an)>0:
            a0 = liste_an[0]

        vecteur_signal_periode = a0*np.ones(Nperiode)

        for i in range(1, len(liste_an)):
            fi = i * F
            vecteur_signal_periode = vecteur_signal_periode + liste_an[i]*np.cos(2*np.pi*fi*vecteur_t_periode)
        for i in range(1, len(liste_bn)):
            fi = i * F
            vecteur_signal_periode = vecteur_signal_periode + liste_bn[i]*np.sin(2*np.pi*fi*vecteur_t_periode)


        SignalComplet.__init__(self, base_de_temps, utb.periodiser(Nsignal, vecteur_signal_periode), nom)
        self.mesures.T_th = 1/F


if __name__ == "__main__":

    s1 = Fourier(1e3, [1,1], [], nom="$s_1$")

    s1.tracer_signal()


    print("fin")