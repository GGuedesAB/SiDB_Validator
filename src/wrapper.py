#############################################################################
#                               UFMG - 2021                                 #
#                            SiDB GateFinder:                               #
#      Framework to facilitate edition and testing of SiDB circuits         #
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
from inputPermuter import Permuter

import argparse
import os
import xml.etree.ElementTree as ET
import logger
import copy
import math
from random import seed
from random import randint
import re
from datetime import datetime


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

##  EDIT DESIGN BELOW THIS LINE. EXAMPLES OF CLASS METHOD'S USAGE ARE PROVIDED IN src/examples      ##
##      User Parameters  - those should be always provided      ##

design_name = "TEST_3IN_MAJ_GATE"
sim_mu = -0.28
number_of_inputs = 3              # currently gateFinder only support 2 and 3 input gates
ext_potential_vector = None

#   Creation of design, randomizer and inputPermuter is necessary for design edition and sim automation
design = Design(args.design)
randomizer = Randomizer(design)
inputpermuter = Permuter(design)

##      Design Modifications        ##

designDbs = randomizer.design.getDBDots()
print("Inputs: " + str(randomizer.inputs))
print("Outputs: " + str(randomizer.outputs))
print("Std: " + str(randomizer.std))
print("Perturbers: " + str(randomizer.outPerturber))
print("inPertubers: " + str(randomizer.inPerturber))
print("Perturbers: " + str(-1))
# design.removeDBDot(designDbs[0])

# TESTS FOR MODIFYPOSITIONS METHOD
#   OR:
# randomizer.modifyPositions("vertical", 2, "outputPos")
# randomizer.modifyPositions("vertical", 2, "inputPos")
# randomizer.modifyPositions("horizontal", -2, "inputPos")
# randomizer.modifyPositions("horizontal", 2, "outputPos")
#   3-INPUT MAJ GATE:

# TESTS FOR MODIFYANGLE METHOD
#   OR:
# inputPair1 = [randomizer.std[0], randomizer.inputs[0]]
# inputPair2 = [randomizer.std[1], randomizer.inputs[1]]
# randomizer.modifyAngle(inputPair1, 120)
# randomizer.modifyAngle(inputPair2, 120)
# 3-INPUT MAJ GATE:
# inputPair1 = [randomizer.std[0], randomizer.inputs[0]]
# inputPair2 = [randomizer.std[0], randomizer.inPerturber[0]]
# randomizer.modifyAngle(inputPair1, 60)
# randomizer.modifyAngle(inputPair2, 60)
# randomizer.modifyInputAngle(randomizer.std[0], randomizer.inputs[0], randomizer.inPerturber[0], 120)
randomizer.modifyInputAngle(randomizer.std[3], randomizer.inputs[2], randomizer.inPerturber[2], -60)
# randomizer.modifyInputAngle(randomizer.std[0], randomizer.inputs[0], randomizer.inPerturber[0], 60)

#   GENERAL DBPAIRS:
#   top of horizontal line
# inputpair1 = [randomizer.std[0], randomizer.inputs[0]]
# inputpair2 = [randomizer.std[1], randomizer.inputs[1]]
# inputpair3 = [randomizer.std[2], randomizer.inputs[2]]
# inputpair4 = [randomizer.std[3], randomizer.inputs[3]]
# inputpair5 = [randomizer.std[4], randomizer.inputs[4]]
# randomizer.modifyAngle(inputpair1, 120)
# randomizer.modifyAngle(inputpair2, 120)
# randomizer.modifyAngle(inputpair3, 120)
# randomizer.modifyAngle(inputpair4, 120)
# randomizer.modifyAngle(inputpair5, 120)

#   bottom of horizontal line
# inputpair6 = [randomizer.std[5], randomizer.inputs[5]]
# inputpair7 = [randomizer.std[6], randomizer.inputs[6]]
# inputpair8 = [randomizer.std[7], randomizer.inputs[7]]
# inputpair9 = [randomizer.std[8], randomizer.inputs[8]]
# inputpair10 = [randomizer.std[9], randomizer.inputs[9]]
# randomizer.modifyAngle(inputpair6, -120)
# randomizer.modifyAngle(inputpair7, -120)
# randomizer.modifyAngle(inputpair8, -120)
# randomizer.modifyAngle(inputpair9, -120)
# randomizer.modifyAngle(inputpair10, -120)

# TESTS FOR MODIFYSPECIFIC DB METHOD



##      PLEASE DO NOT EDIT BELOW THIS LINE. THIS PIECE OF CODE IS DESTINED TO AUTOMATICALLY     ##
##      HANDLE THE MODIFIED VERSION OF DESIGN AND GENERATE THE CORRECT SIMS AND OUTPUTS         ##

print("------- GateFinder: SiDB Circuits Design Framework -------\n")
print("Universidade Federal de Minas Gerais - Dpto. de Ciência da Computação\n")
print("NanoComp Lab")
print("Developed by Arthur Fortini and Gustavo Guedes")
print("For more info search in the proj README file for contact information")
print("\n")
print("Initializing GateFinder ....\n")

print("Automatic input permutation and simulation started at: " + str(datetime.now()) + "\n")

# Saves modified version of design in cwd #
print("Saving modified version of original design.....\n")
design.overwriteDBDots()
design.save(design_name + ".sqd")
design.save(design_name + "SIM_PROBLEM.xml")
base_dir = os.getcwd()

# Permutes inputs #
print("Permuting inputs.....\n")
if (number_of_inputs == 2):
    inputpermuter.permute2inputs(design_name)
elif (number_of_inputs == 3):
    inputpermuter.permute3inputs(design_name)
else:
    log.error(f"Number of inputs {number_of_inputs} not supported\n")

tt_log = open(design_name + "_truth_table.log", "w")     # creates log for truth table

header = ["-----------------------------------------------------------------------------\n",
          "|                               UFMG - 2021                                 |\n",
          "|                             SiDB GateFinder:                              |\n",
          "|                             Truth Table Log                               |\n",
          "|                                                                           |\n",
          "| Design: " + design_name + "                                                \n",
          "| Description: SimAnneal results for all possible inputs of                 |\n",
          "|              modified design.                                             |\n",
          "| Developed by: Arthur Fortini & Gustavo Guedes                             |\n",
          "-----------------------------------------------------------------------------\n",
          "\n",
          "Report start:\t" + str(datetime.now()) + "\n",
          "\n",
          "-----------------------------------------------------------------------------\n",
          "INPUTS\t\t\t\t\t\t\tOUTPUTS\n",
          "-----------------------------------------------------------------------------\n"]
tt_log.writelines(header)

input_table = []
if (number_of_inputs == 2):
    input_table.append("IN0     IN1\n")
    input_table.append("--------------------\n")
elif (number_of_inputs == 3):
    input_table.append("IN0     IN1     IN2\n")
    input_table.append("--------------------\n")
else:
    log.error(f"Number of inputs {number_of_inputs} not supported\n")

tt_log.writelines(input_table)

# run simulations for each possibility of inputs #

print("Running simulations.....\n")

def run_simAnneal(sim_dir, ext_potential_vector = None):
    directory = "sims"
    path = os.path.join(directory, sim_dir)
    os.chdir(path)
    design = Design(sim_dir + ".xml")
    randomizer = Randomizer(design)
    db_pos = []

    for i, DBDot in enumerate(randomizer.inputs):
        (n, m, l) = DBDot.latcoord
        db_pos.append([int(n), int(m), int(l)])

    for i, DBDot in enumerate(randomizer.std):
        (n, m, l) = DBDot.latcoord
        db_pos.append([int(n), int(m), int(l)])

    for i, DBDot in enumerate(randomizer.inPerturber):
        (n, m, l) = DBDot.latcoord
        db_pos.append([int(n), int(m), int(l)])

    for i, DBDot in enumerate(randomizer.outPerturber):
        (n, m, l) = DBDot.latcoord
        db_pos.append([int(n), int(m), int(l)])

    for i, DBDot in enumerate(randomizer.outputs):
        (n, m, l) = DBDot.latcoord
        db_pos.append([int(n), int(m), int(l)])

    sp = simanneal.SimParams()
    sp.mu = sim_mu
    sp.set_db_locs(db_pos)
    if (ext_potential_vector != None):
        sp.set_v_ext(ext_potential_vector)
        # sp.set_v_ext(np.zeros(len(sp.db_locs)))
    sa = simanneal.SimAnneal(sp)
    sa.invokeSimAnneal()
    results = sa.suggested_gs_results()
    return results

tt_result = []

if (number_of_inputs == 2):
    counter = 0
    simdir = ""
    inputStr = ""

    for i in range(4):
        if (counter == 0):
            simdir = design_name + "_00"
            inputStr = "0\t\t0\t\t"
        elif (counter == 1):
            simdir = design_name + "_01"
            inputStr = "0\t\t1\t\t"
        elif (counter == 2):
            simdir = design_name + "_10"
            inputStr = "1\t\t0\t\t"
        elif (counter == 3):
            simdir = design_name + "_11"
            inputStr = "1\t\t1\t\t"

        if (ext_potential_vector != None):
            result = run_simAnneal(simdir, ext_potential_vector)
        else:
            result = run_simAnneal(simdir)

        print("Simulation result for " + simdir + ".xml : ")
        print(result)
        outputStr = str(result[0])
        find_output_regex = r"[-+\s][0-1](?=])"
        outputRes = re.search(find_output_regex, outputStr).group(0)

        if (outputRes == " 0"):
            tt_log.write(inputStr + "\t\t0\n")
            tt_result.append(inputStr + "\t\t0\n")
        elif (outputRes == "-1"):
            tt_log.write(inputStr + "\t\t1\n")
            tt_result.append(inputStr + "\t\t1\n")
        elif (outputRes == "+1"):
            tt_log.write(inputStr +  "\t\tDEGENERATE \n")
            tt_result.append(inputStr + "\t\tDEGENERATE\n")

        counter = counter+1
        os.chdir(base_dir)

elif (number_of_inputs == 3):
    counter = 0
    simdir = ""
    inputStr = ""

    for i in range(8):
        if (counter == 0):
            simdir = design_name + "_000"
            inputStr = "0\t\t0\t\t0\t\t"
        elif (counter == 1):
            simdir = design_name + "_001"
            inputStr = "0\t\t0\t\t1\t\t"
        elif (counter == 2):
            simdir = design_name + "_010"
            inputStr = "0\t\t1\t\t0\t\t"
        elif (counter == 3):
            simdir = design_name + "_011"
            inputStr = "0\t\t1\t\t1\t\t"
        elif (counter == 4):
            simdir = design_name + "_100"
            inputStr = "1\t\t0\t\t0\t\t"
        elif (counter == 5):
            simdir = design_name + "_101"
            inputStr = "1\t\t0\t\t1\t\t"
        elif (counter == 6):
            simdir = design_name + "_110"
            inputStr = "1\t\t1\t\t0\t\t"
        elif (counter == 7):
            simdir = design_name + "_111"
            inputStr = "1\t\t1\t\t1\t\t"

        if (ext_potential_vector != None):
            result = run_simAnneal(simdir, ext_potential_vector)
        else:
            result = run_simAnneal(simdir)

        print("Simulation result for " + simdir + ".xml : ")
        print(result)
        outputStr = str(result[0])
        find_output_regex = r"[-+\s][0-1](?=])"
        outputRes = re.search(find_output_regex, outputStr).group(0)

        if (outputRes == " 0"):
            tt_log.write(inputStr + "\t\t0\n")
            tt_result.append(inputStr + "\t\t0\n")
        elif (outputRes == "-1"):
            tt_log.write(inputStr + "\t\t1\n")
            tt_result.append(inputStr + "\t\t1\n")
        elif (outputRes == "+1"):
            tt_log.write(inputStr +  "\t\tDEGENERATE \n")
            tt_result.append(inputStr + "\t\tDEGENERATE\n")

        counter = counter+1
        os.chdir(base_dir)

print("Simulation ended at:\t\t" + str(datetime.now()))
print("Simulation final result:\n")

for i, line in enumerate(header):
    print(line)
for i, line in enumerate(input_table):
    print(line)
for i, line in enumerate(tt_result):
    print(line)



