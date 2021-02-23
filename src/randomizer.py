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
        #self.design = dbMap.Design(designFile)
        self.inputs = []
        self.outputs = []
        self.std = []
        self.outPerturber = []
        self.mapPorts()

    def mapPorts(self):
        DBDotList = self.design.getDBDots()
        #if (DBDotList == None):
        #    DBDotList = self.DBDots
        for i, DBDot in enumerate(DBDotList):
            portType = DBDot.getType()
            if (portType == "in"):
                self.inputs.append(DBDot)
            elif (portType == "out"):
                self.outputs.append(DBDot)
            elif (portType == "std"):
                self.std.append(DBDot)
            else:
            #elif (portType == "perturber"):
                self.outPerturber.append(DBDot)

    def modifyPositions(self, type=None, symmetry, distance):
        ##COMO DETERMINAR UMA POSIÇÃO VÁLIDA PRO DB? TIPO, COMO EU SEI A COORDENADA ONDE EXISTE UM PONTO?
        ##COMO DETERMINAR AS COORDENADAS CORRETAS DA LATITUDE?
        ## to do:        ter um parametro de entrada que diz se a porta eh vertical ou horizontal

        n, m, l = 0
        x, y = 0
        newN = 0

        if type == "outputSymmetry":
            if symmetry == "vertical":
                for i, dir in enumerate(self.outputs):
                    (n, m, l) = dir.latcoord           ## to do: CRIAR UM METODO PRA RETORNAR AS COORDENADAS DO PONTO. E depois modificar.
                    (x, y) = dir.physloc
                    if n >= "0":
                        newN = distance*n
                        dir.changeLatcoord(newN, m, l)
                    if n < "0":
                        newN = n + (7.68*distance)
                        dir.changeLatcoord(newN, m , l)



                for i, dir in enumerate(self.outPerturber):
                    (n, m, l) = dir.latcoord
                    (x, y) = dir.physloc
                    if n >= "0":
                        newN = distance * n
                        dir.changeLatcoord(newN, m, l)




            #if symmetry == "horizontal":

        # elif type == "inputSymmetry":
        #
        #
        # elif type == None:
        #     log.error(f"modifyPositions method called without specifying TYPE of position modification\n")






    # def modifyAngles(self, type):
    #     ##COMO CALCULAR OU DETERMINAR OS ANGULOS
    #     if type == "InputAngles":
    #
    #     elif type == "OutputAngles":
    #
    #     elif type == None:
    #         log.error(f"modifyAngles method called without specifying TYPE of angle modification\n")
    #
    #
    #
    # def modifySimParams(self, mi, fermi):
    #     ##TO DO: PARSEAR A PARTE DE ARGUMENTOS DE SIMULAÇÃO TBM, NAO APENAS SOBRE OS DBS EM SI, PRA DAR PRA MEXER NISSO AQ.




def test():
    design = Design(args.design)
    randomizer = Randomizer(design)
    designDbs = randomizer.design.getDBDots()
    print("Inputs: " + str(randomizer.inputs))
    print("Outputs: " + str(randomizer.outputs))
    print("Std: " + str(randomizer.std))
    print("Perturbers: " + str(randomizer.outPerturber))
    for i, dir in enumerate(designDbs):
        print("DBDot Type is " + str(dir.getType()))
        dir.changeLayerId(5)
        tu = (8, 8, 8)
        dir.changeLatcoord(tu)
        dir.changePhysloc(1.03, 1.03)
        dir.changeColor("#ffffffff")
    design.overwriteDBDots()
    design.addDBDot(10, (3, 3, 3), (2.22, 3.33), "#00000000")
    design.save("test.xml")

test()