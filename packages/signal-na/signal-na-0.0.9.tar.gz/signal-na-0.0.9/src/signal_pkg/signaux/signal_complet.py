#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:43:58 2019

@author: nicolas
"""
import time

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import base.constantes_base as cst

from signaux.signal_base import SignalBase
from base.temps_base import BaseTemps
from base.mesure_base import Mesures
from traitements.signal_arithmetique import SignalArithmetique
from traitements.signal_fft import SignalFFT
from traitements.signal_tns import SignalTNS
from traitements.signal_mesure import SignalMesure
from affichages.signal_plot import SignalPlot, tracer_signaux
from affichages.signal_fft_plot import SignalFFTPlot, tracer_spectres

import numpy as np

import matplotlib.pyplot as plt
 
__all__ = []

class SignalComplet(SignalMesure, SignalTNS, SignalArithmetique, SignalFFTPlot, SignalPlot, SignalFFT, SignalBase):
    pass


if __name__ == "__main__":
    liste_tmin_tmax=[0, 1]
    Te = 1e-3
    F = 2
    
    bdt = BaseTemps(liste_tmin_tmax, Te)
    vecteur_t = bdt.calculer_vecteur_t()
    vecteur_signal = np.cos(2*np.pi*F*vecteur_t)

    s = SignalComplet(bdt, vecteur_signal)
    
    s.tracer_signal()

    print("fin")