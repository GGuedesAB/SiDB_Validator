#############################################################################
#                               UFMG - 2021                                 #
#                            SiDB GateFinder:                               #
#           IP to facilitate edition and testing of SiDB circuits           #
#                                                                           #
# Authors: Arthur Fortini and Gustavo Guedes                                #
# File: wrapper.py                                                          #
# Description: Top level file to address user modifications in a base       #
#              SiDB file and facilitate simulation and anaylis of results.  #
#              Please note that some parts should be edited by user and     #
#              some parts are an automated flow that should not be modified #
#                                                                           #
#############################################################################

# this imports assumes that a pysimanneal directory containing __init__.py,
# simanneal.py, and the compiled simanneal library (_simanneal.so for Linux or
# _simanneal.pyd for Windows) are present.
# also a src directory containing dbMap.py, inputPermuter.py e randomizer.Py
# should be present.

from pysimanneal import simanneal
from dbMap import Design, DBDot
from randomizer import Randomizer

import argparse
import os
import xml.etree.ElementTree as ET
import logger
import copy
import math
from random import seed
from random import randint

seed(1)

def create_logger ():
    build_logger = logger.Logger()
    build_logger.set_error()
    return build_logger

def arg_parser():
    parser = argparse.ArgumentParser(description='Design randomizer script.')
    parser.add_argument('design', help='Design to be randomized', type=str)
    args = parser.parse_args()
    return args

def arg_check():
    if not os.path.isfile(args.design):
        log.error(f"Could not find design file {args.design}")

log = create_logger()
args = arg_parser()
arg_check()

##  PRIMEIRO OS PARAMETROS QUE O USUARIO ENTRA. NOME, MU, QUANTAS ENTRADAS TEM A PORTA.

## AREA PRA ELE MODIFICAR O DESIGN DE ENTRADA COMO ELE QUISER

### AREA NAO EDITAVEL QUE VAI DRIVEAR OQ ELE MUDAR PRAS SIMULACOES QUE VAMOS FAZER E PARA A GERAÇAO DO LOG.


