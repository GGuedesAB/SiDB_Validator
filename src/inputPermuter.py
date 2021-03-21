from dbMap import Design, DBDot
from randomizer import Randomizer
import argparse
import os
import xml.etree.ElementTree as ET
import logger
from random import seed
from random import randint

seed(1)

def create_logger():
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

class Permuter ():
    def __init__(self, designObj) -> None:
        self.design = designObj
        self.inputs = []
        self.outputs = []
        self.std = []
        self.inPerturber = []
        self.outPerturber = []
        self.mapPorts()

    def mapPorts(self):
        DBDotList = self.design.getDBDots()
        # if (DBDotList == None):
        #    DBDotList = self.DBDots
        for i, DBDot in enumerate(DBDotList):
            portType = DBDot.getType()
            if (portType == "in"):
                self.inputs.append(DBDot)
            elif (portType == "out"):
                self.outputs.append(DBDot)
            elif (portType == "std"):
                self.std.append(DBDot)
            elif (portType == "inPerturber"):
                self.inPerturber.append(DBDot)
            else:
            # elif (portType == "perturber"):
                self.outPerturber.append(DBDot)

    # creates a directory for each permutation of inputs, where will be stored also the results from simulations invoked through cmd
    def permute2inputs(self, designName):
        directory = "sims"
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        counter = 0
        per_dir = ""

        for i in range(3):
            if (counter == 0):
                per_dir = designName + "_11"
            elif (counter == 1):
                per_dir = designName + "_00"
            elif (counter == 2):
                per_dir = designName + "_01"
            elif (counter == 3):
                per_dir = designName + "_10"

            per_path = os.path.join(path, per_dir)
            os.mkdir(per_path)
            os.chdir(per_path)

            if (counter == 1):
                self.design.removeDBDot()
                self.design.removeDBDot()
            elif (counter == 2):
                self.design.addDBDot()
            elif (counter == 3):
                self.design.removeDBDot()
                self.design.addDBDot()

            self.design.overwriteDBDots()
            self.design.save(per_dir + ".sqd")
            self.design.save(per_dir + ".xml")

    def permute3inputs(self, designName):
        directory = "sims"
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        counter = 0
        per_dir = ""

        for i in range(7):
            if (counter == 0):
                per_dir = designName + "_111"
            elif (counter == 1):
                per_dir = designName + "_000"
            elif (counter == 2):
                per_dir = designName + "_001"
            elif (counter == 3):
                per_dir = designName + "_010"
            elif (counter == 4):
                per_dir = designName + "_011"
            elif (counter == 5):
                per_dir = designName + "_100"
            elif (counter == 6):
                per_dir = designName + "_101"
            elif (counter == 7):
                per_dir = designName + "_110"

            per_path = os.path.join(path, per_dir)
            os.mkdir(per_path)
            os.chdir(per_path)

            if (counter == 1):
                self.design.removeDBDot()
                self.design.removeDBDot()
                self.design.removeDBDot()
            elif (counter == 2):
                design.addDBDot()
            elif (counter == 3):
                design.removeDBDot()
                design.addDBDot()
            elif (counter == 4):
                design.removeDBDot()
                design.addDBDot()
            elif (counter == 5):
                design.removeDBDot()
                design.addDBDot()
            elif (counter == 6):
                design.removeDBDot()
                design.addDBDot()
            elif (counter == 7):
                design.removeDBDot()
                design.addDBDot()



            design.overwriteDBDots()
            design.save(per_dir + ".sqd")
            design.save(per_dir + ".xml")