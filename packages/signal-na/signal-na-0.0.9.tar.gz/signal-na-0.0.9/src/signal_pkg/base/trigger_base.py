import numpy as np
import copy

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

class Trigger():
    def __init__(self):
        self.seuil = None
        self.montant = None
        self.pretrigger = None
        self.pretrigger_souple = None
        self.hysteresys = None

    def tester_trigger(self):
        return self.seuil != None

if __name__ == "__main__":
    pass
