import dbMap
class Randomizer ():
    def __init__(self, designFile) -> None:
        self.dbDots = dbMap.DesignDBDots(designFile)
        self.designFile = designFile