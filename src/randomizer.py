from dbMap import Design, DBDot
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


class Randomizer ():
    def __init__(self, designObj) -> None:
        self.design = designObj
        # self.design = dbMap.Design(designFile)
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

    def changeXcoord(self, dbDot, distance, n, m, l):
        (x, y) = dbDot.physloc
        if n >= 0:
            newN = distance + n
            dbDot.changeLatcoord(newN, m, l)
            newX = newN * 3.84
            dbDot.changePhysloc(newX, float(y))
        if n < 0:
            newN = n + distance
            dbDot.changeLatcoord(newN, m, l)
            newX = newN * 3.84
            dbDot.changePhysloc(newX, float(y))

    def changeYcoord(self, dbDot, distance, n, m, l):
        (x, y) = dbDot.physloc
        if m >= 0:
            newM = distance + m
            dbDot.changeLatcoord(n, newM, l)
            newY = newM * 7.68 + l * 2.25
            dbDot.changePhysloc(float(x), newY)
        if m < 0:
            newM = m + distance
            dbDot.changeLatcoord(n, newM, l)
            newY = newM * 3.84 + l * 2.25
            dbDot.changePhysloc(float(x), newY)

    def changecoord(self, dbDot, n, m, l):
        newX = n*3.84
        newY = m*7.68 + l*2.25
        dbDot.changeLatcoord(n, m, l)
        dbDot.changePhysloc(newX, newY)

    def modifySpecificDBbyID(self, dbId, distance, axis):
        DBDotList = self.design.getDBDots()
        for i, DBDot in enumerate(DBDotList):
            if DBDot.id == dbId:
                if axis == "x":
                    (n, m, l) = DBDot.latcoord
                    self.changeXcoord(DBDot, distance, int(n), int(m), int(l))
                if axis == "y":
                    (n, m, l) = DBDot.latcoord
                    self.changeYcoord(DBDot, distance, int(n), int(m), int(l))
            else:
                log.error(f" modifySpecificDB: id of DB not found\n")

    def modifySpecificDB(self, DBDot, distance, axis):
        if axis == "x":
            (n, m, l) = DBDot.latcoord
            self.changeXcoord(DBDot, distance, int(n), int(m), int(l))
        if axis == "y":
            (n, m, l) = DBDot.latcoord
            self.changeYcoord(DBDot, distance, int(n), int(m), int(l))

    # Below method only works for 2 input gates. Work on solution for 3 input gates.
    def modifyPositions(self, axis, distance, type=None):
        if type == "outputPos":
            if axis == "horizontal":
                # move outputs
                for i, dir in enumerate(self.outputs):
                    (n, m, l) = dir.latcoord
                    self.changeXcoord(dir, distance, int(n), int(m), int(l))
                # move perturber along with outputs.
                for i, dir in enumerate(self.outPerturber):
                    (n, m, l) = dir.latcoord
                    self.changeXcoord(dir, distance, int(n), int(m), int(l))
            if axis == "vertical":
                # move outputs
                for i, dir in enumerate(self.outputs):
                    (n, m, l) = dir.latcoord
                    self.changeYcoord(dir, distance, int(n), int(m), int(l))
                # move perturber along with outputs.
                for i, dir in enumerate(self.outPerturber):
                    (n, m, l) = dir.latcoord
                    self.changeYcoord(dir, distance, int(n), int(m), int(l))
        elif type == "inputPos":
            if axis == "horizontal":
                for i, dir in enumerate(self.inputs):
                    (n, m, l) = dir.latcoord
                    self.changeXcoord(dir, distance, int(n), int(m), int(l))
            if axis == "vertical":
                for i, dir in enumerate(self.inputs):
                    (n, m, l) = dir.latcoord
                    self.changeYcoord(dir, distance, int(n), int(m), int(l))
        elif type == None:
            log.error(f"modifyPositions method called without specifying TYPE of position modification\n")
        else:
            log.error(f"modifyPositions method called with invalid TYPE of position modification\n")

    def modifyAngle(self, dbPair, angle):
        dbRoot = dbPair[0]
        dbLeaf = dbPair[1]
        (n1, m1, l1) = dbRoot.latcoord
        nR = int(n1)
        mR = int(m1)
        lR = int(l1)
        (n2, m2, l2) = dbLeaf.latcoord
        nL = int(n2)
        mL = int(m2)
        lL = int(l2)

        #if lR == 0:      # checks if dbRoot db is un upper or lower stream of grid horizontal line
        if angle == 0:
            if (mR == mL):
                newnL = nR + abs(nR - nL)
                self.changecoord(dbLeaf, newnL, mR, lR)
            elif(nR > nL):
                newnL = nR + abs(nR - nL) + 1
                self.changecoord(dbLeaf, newnL, mR, lR)
            elif(nR < nL):
                self.changecoord(dbLeaf, nL+1, mR, lR)
            else:
                newnL = nR + abs(mL - mR) + 1
                self.changecoord(dbLeaf, newnL, mR, lR)
        elif angle == 60:
            if(nR == nL):
                newnL = nR + abs(mR - mL)
                newmL = mL - abs(nR - nL)
                self.changecoord(dbLeaf, newnL, newmL, lL)
            elif (mR == mL):
                if (nR > nL):
                    newnL = nR + abs(nR - nL)
                    newmL = mL - abs(nR - nL) + 1
                    self.changecoord(dbLeaf, newnL, newmL, 1)
                else:
                    newmL = mL - abs(nR - nL) + 1
                    self.changecoord(dbLeaf, nL, newmL, 1)
            elif(nR > nL):
                newnL = nR + abs(nR - nL)
                self.changecoord(dbLeaf, newnL, mL, lL)
        elif angle == 90:
            if (mR == mL):
                newmL = mR - abs(nL - nR)+1
                self.changecoord(dbLeaf, nR, newmL, lL)
            else:
                self.changecoord(dbLeaf, nR, mL, lL)
        elif angle == 120:
            if (nR == nL):
                newnL = nR - abs(mR - mL)
                newmL = mL - abs(nR - nL)
                self.changecoord(dbLeaf, newnL, newmL, lL)
            elif (mR == mL):
                if (nR < nL):
                    newnL = nR - abs(nR - nL)
                    newmL = mL - abs(nR - nL) +1
                    self.changecoord(dbLeaf, newnL, newmL, 1)
                else:
                    newmL = mL - abs(nR - nL) +1
                    self.changecoord(dbLeaf, nL, newmL, 1)
            elif (nR < nL):
                newnL = nR - abs(nR - nL)
                self.changecoord(dbLeaf, newnL, mL, lL)
        elif angle == 180:
            if (mR == mL):
                newnL = nR - abs(nR - nL)
                self.changecoord(dbLeaf, newnL, mR, lR)
            elif(nL > nR):
                newnL = nR - abs(nL - nR) -1
                self.changecoord(dbLeaf, newnL, mR, lR)
            elif(nL < nR):
                self.changecoord(dbLeaf, nL-1, mR, lR)
            else:
                newnL = nR - abs(mL - mR) -1
                self.changecoord(dbLeaf, newnL, mR, lR)
        # else:
        #     log.error(f" modifyAngle: angle argument invalid!\n")

        #elif lR == 1:
            # if angle == 0:
            #     if (mR == mL):
            #         newnL = nR + abs(nR - nL)
            #         self.changecoord(dbLeaf, newnL, mR, lR)
            #     elif(nR > nL):
            #         newnL = nR + abs(nR - nL) + 1
            #         self.changecoord(dbLeaf, newnL, mR, lR)
            #     elif(nR < nL):
            #         self.changecoord(dbLeaf, nL+1, mR, lR)
            #     else:
            #         newnL = nR + abs(mL - mR) + 1
            #         self.changecoord(dbLeaf, newnL, mR, lR)
        elif angle == -60:
            if(nR == nL):
                newnL = nR + abs(mR - mL)
                newmL = mL + abs(nR - nL)
                self.changecoord(dbLeaf, newnL, newmL, lL)
            elif (mR == mL):
                if (nR > nL):
                    newnL = nR + abs(nR - nL)
                    newmL = mL + abs(nR - nL) - 1
                    self.changecoord(dbLeaf, newnL, newmL, 0)
                else:
                    newmL = mL + abs(nR - nL) - 1
                    self.changecoord(dbLeaf, nL, newmL, 0)
            elif(nR > nL):
                newnL = nR + abs(nR - nL)
                self.changecoord(dbLeaf, newnL, mL, lL)
        elif angle == -90:
            if (mR == mL):
                newmL = mR + abs(nL - nR) -1
                self.changecoord(dbLeaf, nR, newmL, lL)
            else:
                self.changecoord(dbLeaf, nR, mL, lL)
        elif angle == -120:
            if (nR == nL):
                newnL = nR - abs(mR - mL)
                newmL = mL + abs(nR - nL)
                self.changecoord(dbLeaf, newnL, newmL, lL)
            elif (mR == mL):
                if (nR < nL):
                    newnL = nR - abs(nR - nL)
                    newmL = mL + abs(nR - nL) -1
                    self.changecoord(dbLeaf, newnL, newmL, 0)
                else:
                    newmL = mL + abs(nR - nL) -1
                    self.changecoord(dbLeaf, nL, newmL, 0)
            elif (nR < nL):
                newnL = nR - abs(nR - nL)
                self.changecoord(dbLeaf, newnL, mL, lL)
        elif angle == -180:
            if (mR == mL):
                newnL = nR - abs(nR - nL)
                self.changecoord(dbLeaf, newnL, mR, lR)
            elif(nL > nR):
                newnL = nR - abs(nL - nR) -1
                self.changecoord(dbLeaf, newnL, mR, lR)
            elif(nL < nR):
                self.changecoord(dbLeaf, nL-1, mR, lR)
            else:
                newnL = nR - abs(mL - mR) -1
                self.changecoord(dbLeaf, newnL, mR, lR)
        else:
            log.error(f" modifyAngle: angle argument invalid!\n")
    # else:
    #     log.error(f"modifyAngle: position of root db in pair inconsistent. l can only be 0 or 1\n")

    def modifyInputAngle(self, DBRoot, DBin, DBper, angle):
        inputPair1 = [DBRoot, DBin]
        inputPair2 = [DBRoot, DBper]
        self.modifyAngle(inputPair1, angle)
        self.modifyAngle(inputPair2, angle)

# def test():
#     design = Design(args.design)
#     randomizer = Randomizer(design)
#
#     #randomizer.modifySpecificDBbyID(0, 2, "x")
#     randomizer.modifySpecificDB(randomizer.inPerturber[0], -5, "x")
#     randomizer.modifySpecificDB(randomizer.inPerturber[0], -6, "y")
#
#
#
#     design.overwriteDBDots()
#     design.save("test.sqd")
#     design.save("test.xml")
#
#
#
# test()