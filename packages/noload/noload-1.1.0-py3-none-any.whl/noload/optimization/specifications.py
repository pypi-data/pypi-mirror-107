# SPDX-FileCopyrightText: 2020 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

import autograd.numpy as np
from autograd.builtins import isinstance
from noload.optimization.Tools import *
'''Define optimization specification including objectives and constraints'''
class Spec:
    iNames      = []  #noms des variables d'optimisation
    bounds      = []  #domaine de recherche
    xinit       = []  #valeurs initiales
    xinit_sh    = []
    objectives  = []  #noms des objectifs
    eq_cstr     = []  #noms des contraintes d'équalité
    eq_cstr_val : StructList = None  #valeurs des contraintes d'égalité
    ineq_cstr   = []  #noms des contraintes d'inégalité
    ineq_cstr_bnd : StructList = None  # domaine des contraintes d'inégalité
    freeOutputs = []  # list of outputs to monitor
    nb          = 0
    oNames       = []
    def __init__(self, variables, bounds, objectives, eq_cstr=[], eq_cstr_val=[], ineq_cstr=[], ineq_cstr_bnd=[], freeOutputs=[], xinit=[]):
        x0 = StructList(xinit)
        self.xinit_sh = x0.shape
        if self.xinit_sh != [0] * len(x0.List) and len(self.iNames) != 1:
            bnds = bounds
            bounds = []
            for i in range(len(bnds)):
                if isinstance(bnds[i][0], list):
                    for j in range(len(bnds[i])):
                        bounds.append(bnds[i][j])
                else:
                    bounds.append(bnds[i])
            x0 = StructList(xinit)
            xinit = x0.flatten()
        self.iNames = variables
        if not isinstance(bounds, np.ndarray):
            bounds = np.array(bounds)
        self.bounds = bounds
        if not isinstance(xinit, np.ndarray):
            xinit = np.array(xinit)
        self.xinit = xinit
        self.objectives = objectives
        self.eq_cstr = eq_cstr
        self.eq_cstr_val = StructList(eq_cstr_val)
        self.ineq_cstr = ineq_cstr
        self.ineq_cstr_bnd = StructList(ineq_cstr_bnd)
        self.freeOutputs = freeOutputs
        self.computeAttributes()

    def computeAttributes(self):
        self.oNames = np.concatenate((self.objectives, self.eq_cstr, self.ineq_cstr, self.freeOutputs), axis=0)
        self.nb = len(self.oNames)

    def removeObjective(self, fobj):
        self.objectives.remove(fobj)
        self.computeAttributes()

    def insertObjective(self, position, fobj):
        self.objectives.insert(position, fobj)
        self.computeAttributes()

    def appendConstraint(self, cstr, value):
        self.eq_cstr.append(cstr)
        self.eq_cstr_val.List.append(value)
        self.computeAttributes()

    def removeLastEqConstraint(self):
        self.eq_cstr.pop()
        self.eq_cstr_val.List.pop()
        self.computeAttributes()


