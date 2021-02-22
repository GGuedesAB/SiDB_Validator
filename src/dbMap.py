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
        for attr in dbAttribs:
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
        log.warning(f"Changing DB #{self.id} layer_id from {self.layer_id} to {newLayerId}")
        self.layer_id = newLayerId
        for attr in self.dbAttribs:
            if attr.tag == "layer_id":
                attr.set("layer_id", str(newLayerId))

    def changeLatcoord(self, newLatcoord, m=None, l=None):
        if m is not None and l is not None:
            latcoord = (newLatcoord, m, l)
        else:
            latcoord = newLatcoord
        log.warning(f"Changing DB #{self.id} latcoord from {self.latcoord} to {latcoord}")
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
        log.warning(f"Changing DB #{self.id} physloc from {self.physloc} to {newPhysloc}")
        self.physloc = newPhysloc
        (x,y) = newPhysloc
        for attr in self.dbAttribs:
            if attr.tag == "physloc":
                attr.set("x", str(x))
                attr.set("y", str(y))

    def changeColor(self, newColor):
        log.warning(f"Changing DB #{self.id} color from {self.color} to {newColor}")
        self.color = newColor
        for attr in self.dbAttribs:
            if attr.tag == "color":
                attr.set("color", str(newColor))

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

    def save(self, fileName):
        self.designParseTree.write(fileName)

def test():
    design = Design(args.design)
    designDbs = design.getDBDots()
    for i, dir in enumerate(designDbs):
        dir.changeLayerId(5)
        tu = (8,8,8)
        dir.changeLatcoord(tu)
        dir.changePhysloc(1.03, 1.03)
        dir.changeColor("#ffffffff")
    design.overwriteDBDots()
    design.save("test.xml")

test()
