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

        # 1st inputperturber data
        input1_id = self.inPerturber[0].layer_id
        input1_latcoord = self.inPerturber[0].latcoord
        input1_physloc = self.inPerturber[0].physloc
        input1_color = self.inPerturber[0].color

        # 2nd inputperturber data
        input2_id = self.inPerturber[1].layer_id
        input2_latcoord = self.inPerturber[1].latcoord
        input2_physloc = self.inPerturber[1].physloc
        input2_color = self.inPerturber[1].color

        for i in range(4):
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
                self.design.removeDBDot(self.inPerturber[0].dbAttribs)
                self.design.removeDBDot(self.inPerturber[1].dbAttribs)
            elif (counter == 2):
                self.design.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
            elif (counter == 3):
                self.design.removeDBDot(self.inPerturber[1].dbAttribs)
                self.design.addDBDot(input1_id, input1_latcoord, input1_physloc, input1_color)

            self.design.overwriteDBDots()
            self.design.save(per_dir + ".sqd")
            self.design.save(per_dir + ".xml")
            counter = counter + 1

    def permute3inputs(self, designName):
        directory = "sims"
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        counter = 0
        per_dir = ""

        # 1st inputperturber data
        input1_id = self.inPerturber[0].layer_id
        input1_latcoord = self.inPerturber[0].latcoord
        input1_physloc = self.inPerturber[0].physloc
        input1_color = self.inPerturber[0].color

        # 2nd inputperturber data
        input2_id = self.inPerturber[1].layer_id
        input2_latcoord = self.inPerturber[1].latcoord
        input2_physloc = self.inPerturber[1].physloc
        input2_color = self.inPerturber[1].color

        # 3rd inputperturber data
        input3_id = self.inPerturber[2].layer_id
        input3_latcoord = self.inPerturber[2].latcoord
        input3_physloc = self.inPerturber[2].physloc
        input3_color = self.inPerturber[2].color

        for i in range(8):
            if (counter == 0):
                per_dir = designName + "_111"
            elif (counter == 1):
                per_dir = designName + "_000"
            elif (counter == 2):
                per_dir = designName + "_001"
            elif (counter == 3):
                per_dir = designName + "_011"
            elif (counter == 4):
                per_dir = designName + "_010"
            elif (counter == 5):
                per_dir = designName + "_110"
            elif (counter == 6):
                per_dir = designName + "_100"
            elif (counter == 7):
                per_dir = designName + "_101"

            per_path = os.path.join(path, per_dir)
            os.mkdir(per_path)
            os.chdir(per_path)

            if (counter == 1):
                self.design.removeDBDot(self.inPerturber[0].dbAttribs)
                self.design.removeDBDot(self.inPerturber[1].dbAttribs)
                self.design.removeDBDot(self.inPerturber[2].dbAttribs)
            elif (counter == 2):
                self.design.addDBDot(input3_id, input3_latcoord, input3_physloc, input3_color)
            elif (counter == 3):
                self.design.addDBDot(input2_id, input2_latcoord, input2_physloc, input2_color)
            elif (counter == 4):
                self.design.removeDBDot(self.inPerturber[2].dbAttribs)
            elif (counter == 5):
                self.design.addDBDot(input1_id, input1_latcoord, input1_physloc, input1_color)
            elif (counter == 6):
                self.design.removeDBDot(self.inPerturber[1].dbAttribs)
            elif (counter == 7):
                self.design.addDBDot(input3_id, input3_latcoord, input3_physloc, input3_color)

            self.design.overwriteDBDots()
            self.design.save(per_dir + ".sqd")
            self.design.save(per_dir + ".xml")
            counter = counter + 1

def test():
    design = Design(args.design)
    randomizer = Randomizer(design)
    inputpermuter = Permuter(design)
    designDbs = randomizer.design.getDBDots()
    print("Inputs: " + str(randomizer.inputs))
    print("Outputs: " + str(randomizer.outputs))
    print("Std: " + str(randomizer.std))
    print("Perturbers: " + str(randomizer.outPerturber))
    print("inPertubers: " + str(randomizer.inPerturber))
    print("Perturbers: " + str(-1))
    #design.removeDBDot(designDbs[0])

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
    #inputPair1 = [randomizer.std[0], randomizer.inputs[0]]
    #inputPair2 = [randomizer.std[0], randomizer.inPerturber[0]]
    #randomizer.modifyAngle(inputPair1, 60)
    #randomizer.modifyAngle(inputPair2, 60)
    randomizer.modifyInputAngle(randomizer.std[0], randomizer.inputs[0], randomizer.inPerturber[0], 180)

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

    design.overwriteDBDots()
    design.save("test.sqd")
    design.save("test.xml")

    inputpermuter.permute2inputs("TEST_OR_GATE")

test()