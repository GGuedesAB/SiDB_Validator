import argparse
import os
import xml.etree.ElementTree as ET
import logger
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

class DBDot ():
    def __init__(self, dbAttribs, id=0) -> None:
        self.dbAttribs = dbAttribs
        self.id = id
        for attr in self.dbAttribs:
            if attr.tag == "layer_id":
                self.layer_id = attr.text
            elif attr.tag == "latcoord":
                self.latcoord = (attr.attrib["n"], attr.attrib["m"], attr.attrib["l"])
            elif attr.tag == "physloc":
                self.physloc = (attr.attrib["x"], attr.attrib["y"])
            elif attr.tag == "color":
                self.color = (attr.text)
            else:
                log.error(f"Unknown key: {attr.tag}")

    def changeLayerId(self, newLayerId):
        log.debug(f"Changing DB #{self.id} layer_id from {self.layer_id} to {newLayerId}")
        self.layer_id = newLayerId
        for attr in self.dbAttribs:
            if attr.tag == "layer_id":
                attr.text = str(newLayerId)

    def changeLatcoord(self, newLatcoord, m=None, l=None):
        if m is not None and l is not None:
            latcoord = (newLatcoord, m, l)
        else:
            latcoord = newLatcoord
        log.debug(f"Changing DB #{self.id} latcoord from {self.latcoord} to {latcoord}")
        self.latcoord = latcoord
        (n, m, l) = latcoord
        for attr in self.dbAttribs:
            if attr.tag == "latcoord":
                attr.set("n", str(n))
                attr.set("m", str(m))
                attr.set("l", str(l))

    def changePhysloc(self, newPhysloc, y=None):
        if y is not None:
            newPhysloc = (newPhysloc, y)
        log.debug(f"Changing DB #{self.id} physloc from {self.physloc} to {newPhysloc}")
        self.physloc = newPhysloc
        (x,y) = newPhysloc
        for attr in self.dbAttribs:
            if attr.tag == "physloc":
                attr.set("x", str(x))
                attr.set("y", str(y))

    def changeColor(self, newColor):
        log.debug(f"Changing DB #{self.id} color from {self.color} to {newColor}")
        self.color = newColor
        for attr in self.dbAttribs:
            if attr.tag == "color":
                attr.text = str(newColor)

    def getType(self):
        if self.color == "#ffff0000":
            return "out"
        elif self.color == "#ffc8c8c8":
            return "std"
        elif self.color == "#ff00ff00":
            return "in"

class Design ():
    def __init__(self, designFile) -> None:
        self.designFilePath = designFile
        self.designParseTree = ET.parse(self.designFilePath)
        self.dbDots = []

    def getDBDots(self):
        if (len(self.dbDots) > 0):
            return self.dbDots
        sqdRoot = self.designParseTree.getroot()
        designTag = sqdRoot.find("design")
        id = 0
        for layer in designTag.findall("layer"):
            if layer.attrib["type"] == "DB":
                for db in layer.findall("dbdot"):
                    newDB = DBDot(db, id)
                    self.dbDots.append(newDB)
                    id += 1
        return self.dbDots

    def addDBDot(self, layer_id, latcoord, physloc, color):
        newDBDot = DBDot(self.dbDots[0].dbAttribs)
        newDBDot.id = newDBDot.id + 1
        newDBDot.changeLayerId(layer_id)
        newDBDot.changeLatcoord(latcoord)
        newDBDot.changePhysloc(physloc)
        newDBDot.changeColor(color)
        self.dbDots.append(newDBDot)
        sqdRoot = self.designParseTree.getroot()
        designTag = sqdRoot.find("design")
        for layer in designTag.findall("layer"):
            if layer.attrib["type"] == "DB":
                layer.append(newDBDot.dbAttribs)

    def overwriteDBDots(self, DBDotList=None):
        if (DBDotList == None):
            DBDotList = self.dbDots
        sqdRoot = self.designParseTree.getroot()
        designTag = sqdRoot.find("design")
        for layer in designTag.findall("layer"):
            if layer.attrib["type"] == "DB":
                for db in layer.findall("dbdot"):
                    layer.remove(db)
                for db in DBDotList:
                    layer.append(db.dbAttribs)

    def areSameDb(self, db1_attr, db2):
        if isinstance(db1_attr, DBDot):
            db1 = db1_attr
        else:
            db1 = DBDot(db1_attr)

        db1_coord1, db1_coord2, db1_coord3 = db1.latcoord
        db1_physloc1, db1_physloc2 = db1.physloc
        db1_int_latcoord = (int(db1_coord1), int(db1_coord2), int(db1_coord3))
        db1_float_physloc = (float(db1_physloc1), float(db1_physloc2))
        db2_layer_id, db2_latcoord, db2_physloc, db2_color = db2
        equal_id = int(db1.layer_id) == db2_layer_id
        equal_latcoord = db1_int_latcoord == db2_latcoord
        equal_physloc = db1_float_physloc == db2_physloc
        equal_color = db1.color == db2_color
        if equal_id and equal_latcoord and equal_physloc and equal_color:
            return True
        else:
            return False

    def removeDBDot(self, dbattrs, latcoord=None, physloc=None, color=None):
        try:
            if latcoord == None:
                targetDb = dbattrs
            else:
                targetDb = (dbattrs, latcoord, physloc, color)
        except:
            log.error("Please pass db dot information as a tuple (layer_id, latcoord, physloc, color)")
        found = 0
        sqdRoot = self.designParseTree.getroot()
        designTag = sqdRoot.find("design")
        for layer in designTag.findall("layer"):
            if layer.attrib["type"] == "DB":
                for db in layer.findall("dbdot"):
                    if self.areSameDb(db, targetDb):
                        for designDb in self.dbDots:
                            if self.areSameDb(designDb, targetDb):
                                self.dbDots.remove(designDb)
                        layer.remove(db)
                        found+=1
        if (found == 0):
            log.warning(f"Could not find the following db in the design:\n\t({targetDb})")
        elif (found > 1):
            log.error(f"More than one db matched db to be removed:\n\t({targetDb})")

        self.overwriteDBDots()

    def save(self, fileName):
        self.designParseTree.write(fileName)

# def test():
#     design = Design(args.design)
#     designDbs = design.getDBDots()
#     for i, dir in enumerate(designDbs):
#         print("DBDot Type is %s", dir.getType())
#         dir.changeLayerId(i)
#         tu = (8,8,8)
#         dir.changeLatcoord(tu)
#         dir.changePhysloc(1.03, 1.03)
#         dir.changeColor("#ffffffff")
#     design.overwriteDBDots()
#     design.addDBDot(10, (3, 3, 3), (2.22,3.33), "#00000000")
#     design.removeDBDot(3, (3, 3, 3), (2.22,3.33), "#00000000")
#     design.save("test.xml")
#
#
# test()
