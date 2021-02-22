import argparse
import os
import xml.etree.ElementTree as ET
import logger

def create_logger ():
    build_logger = logger.Logger()
    build_logger.set_warning()
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
    def __init__(self, dbAttribs) -> None:
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

    def getType(self):
        if self.color == "#ffff0000":
            return "out"
        elif self.color == "#ffc8c8c8":
            return "std"
        elif self.color == "#ff00ff00":
            return "in"

class DesignDBDots ():
    def __init__(self, sqdFile) -> None:
        self.designFilePath = sqdFile
        self.designParseTree = ET.parse(self.designFilePath)

    def parseSqd(self):
        self.dbs = []
        sqdRoot = self.designParseTree.getroot()
        designTag = sqdRoot.find("design")
        for layer in designTag.findall("layer"):
            if layer.attrib["type"] == "DB":
                for db in layer.findall("dbdot"):
                    newDB = DBDot(db)
                    self.dbs.append(newDB)
        return self.dbs

designDbs = DesignDBDots(args.design)
designDbs.parseSqd()
for i, dir in enumerate(designDbs.dbs):
    print (f"DB #{i} is {dir.getType()}")
