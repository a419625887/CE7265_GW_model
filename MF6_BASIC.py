# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 10:23:31 2021

@author: syang
"""


# A module for wirting MODFLOW6 basic packages
import numpy as np
import csv

#
class MF6_basic():
    def __init__(self, modelpath, modelname, nrow, ncol, dx, dy, top, bot):
        self.modelpath = modelpath
        self.modelname = modelname
        self.nrow = nrow
        self.ncol = ncol
        self.dx = dx
        self.dy = dy
        self.top = top
        self.bot = bot
    #
    def write_dis(self):
        with open(self.modelpath + self.modelname + '.dis', 'w', newline = '') as output:
            writer = csv.writer(output, delimiter = ' ')
            writer.writerow(['BEGIN', 'OPTIONS'])
            writer.writerow(['LENGTH_UNITS', 'METERS'])
            writer.writerow(['END', 'OPTIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'DIMENSIONS'])
            writer.writerow(['NLAY', 1])
            writer.writerow(['NROW', self.nrow])
            writer.writerow(['NCOL', self.ncol])
            writer.writerow(['END', 'DIMENSIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'GRIDDATA'])
            writer.writerow(['DELR'])
            writer.writerow(['CONSTANT', self.dx])
            writer.writerow(['DELC'])
            writer.writerow(['CONSTANT', self.dy])
            writer.writerow(['TOP', 'LAYERED'])
            writer.writerow(['CONSTANT', self.top])
            writer.writerow(['BOTM', 'LAYERED'])
            writer.writerow(['CONSTANT', self.bot])
            writer.writerow(['IDOMAIN'])
            writer.writerow(['CONSTANT', 1])
            writer.writerow(['END', 'GRIDDATA'])
           #
        return 1
    #
    def write_chd(self, chd_list):
        with open(self.modelpath + self.modelname + '.chd', 'w', newline = '') as output:
            writer = csv.writer(output, delimiter = ' ')
            writer.writerow(['BEGIN', 'OPTIONS'])
            writer.writerow(['END', 'OPTIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'DIMENSIONS'])
            writer.writerow(['MAXBOUND', len(chd_list)])
            writer.writerow(['END', 'DIMENSIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'PERIOD', '1'])
            for p in chd_list:
                writer.writerow([int(p[0]), int(p[1]), int(p[2]), p[3]])
            writer.writerow(['END', 'PERIOD'])
        #
        return 1
    #
    def write_wel(self, wel_list, transient = 'False', nperiod = None):
        with open(self.modelpath + self.modelname + '.wel', 'w', newline = '') as output:
            writer = csv.writer(output, delimiter = ' ')
            writer.writerow(['BEGIN', 'OPTIONS'])
            writer.writerow(['END', 'OPTIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'DIMENSIONS'])
            writer.writerow(['MAXBOUND', len(wel_list)])
            writer.writerow(['END', 'DIMENSIONS'])
            writer.writerow([])
            #
            if transient == 'False':
                writer.writerow(['BEGIN', 'PERIOD', '1'])
                for p in wel_list:
                    writer.writerow([int(p[0]), int(p[1]), int(p[2]), p[3]])
                writer.writerow(['END', 'PERIOD'])
            else:
                writer.writerow(['BEGIN', 'PERIOD', '2'])
                for p in wel_list:
                    writer.writerow([int(p[0]), int(p[1]), int(p[2]), p[3]])
                writer.writerow(['END', 'PERIOD'])
            #
        #
        return 1
    #
    def write_npf(self, K):
        with open(self.modelpath + self.modelname + '.npf', 'w', newline = '') as output:
            writer = csv.writer(output, delimiter = ' ')
            writer.writerow(['BEGIN', 'OPTIONS'])
            writer.writerow(['SAVE_FLOWS'])
            writer.writerow(['END', 'OPTIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'GRIDDATA'])
            writer.writerow(['ICELLTYPE'])
            writer.writerow(['CONSTANT', 0])
            writer.writerow(['K', 'LAYERED'])
            writer.writerow(['CONSTANT', K])
            writer.writerow(['END', 'GRIDDATA'])
            writer.writerow([])
        #
        return 1
    #
    def write_ic(self, initial_head):
        with open(self.modelpath + self.modelname + '.ic', 'w', newline = '') as output:
            writer = csv.writer(output, delimiter = ' ')
            writer.writerow(['BEGIN', 'GRIDDATA'])
            writer.writerow(['STRT', 'LAYERED'])
            writer.writerow(['CONSTANT', initial_head])
            writer.writerow(['END', 'GRIDDATA'])
            writer.writerow([])
        #
        return 1
    #
    def write_oc(self):
        with open(self.modelpath + self.modelname + '.oc', 'w', newline = '') as output:
            writer = csv.writer(output, delimiter = ' ')
            writer.writerow(['BEGIN', 'OPTIONS'])
            writer.writerow(['BUDGET', 'FILEOUT', self.modelname + '.ccf'])
            writer.writerow(['HEAD', 'FILEOUT', self.modelname + '.hed'])
            writer.writerow(['END', 'OPTIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'PERIOD', 1])
            writer.writerow(['SAVE', 'HEAD', 'ALL'])
            writer.writerow(['SAVE', 'BUDGET', 'ALL'])
            writer.writerow(['END', 'PERIOD'])
            writer.writerow([])
        #
        return 1
    #
    def write_tdis(self, transient = 'False', periodlist = None):
        if transient == 'False':
            nperiod = 1
            periodlist = [[1.0, 1, 1.0]]
        else:
            nperiod = len(periodlist)
        #
        with open(self.modelpath + self.modelname + '.tdis', 'w', newline = '') as output:
            writer = csv.writer(output, delimiter = ' ')
            writer.writerow(['BEGIN', 'OPTIONS'])
            writer.writerow(['TIME_UNITS', 'DAYS'])
            writer.writerow(['END', 'OPTIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'DIMENSIONS'])
            writer.writerow(['NPER', nperiod])
            writer.writerow(['END', 'DIMENSIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'PERIODDATA'])
            writer.writerows(periodlist)
            writer.writerow(['END', 'PERIODDATA'])
            writer.writerow([])
        #
        return 1
    #
    def write_sto(self, ss):
        with open(self.modelpath + self.modelname + '.sto', 'w', newline = '') as output:
            writer = csv.writer(output, delimiter = ' ')
            writer.writerow(['BEGIN', 'OPTIONS'])
            writer.writerow(['SAVE_FLOWS'])
            writer.writerow(['END', 'OPTIONS'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'GRIDDATA'])
            writer.writerow(['ICONVERT'])
            writer.writerow(['CONSTANT', 0])
            writer.writerow(['SS', 'LAYERED'])
            writer.writerow(['CONSTANT', ss])
            writer.writerow(['END', 'GRIDDATA'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'PERIOD', 1])
            writer.writerow(['STEADY-STATE'])
            writer.writerow(['END', 'PERIOD'])
            writer.writerow([])
            #
            writer.writerow(['BEGIN', 'PERIOD', 2])
            writer.writerow(['TRANSIENT'])
            writer.writerow(['END', 'PERIOD'])
            writer.writerow([])
        #
        return 1
    #

