"""
Class State:
residualSpaceList: a list of residual space list. eg. [Space A, Space B]
planListSpace: a list of occupied Space eg. ..
planListSpace: a list of filled Blocks eg [Block A, Block B]
utilization: record current utilization rate
available: record currently available items, it is a dictionary of id: quantity
"""
from Functions import update_available_boxes

class State:
    def __init__(self, residualSpaceList):
        self.residualSpaceList = residualSpaceList
        self.planListSpace = []
        self.planListBlock = []
        self.utilization = 0
        self.available = {}

    # TODO rest of the three methods maybe has the similar function?
    def add_block_planListBlock(self, block):
        self.planListBlock.append(block)

    def add_space_planListSpace(self, space):
        self.planListSpace.append(space)

    def get_residualSpaceList(self):
        return self.residualSpaceList
    
    def get_planListSpace(self):
        return self.planListSpace

    def get_planListBlock(self):
        return self.planListBlock

    def get_utilization(self):
        return self.utilization

    def get_available_items(self):
        return self.available

    def update_available_items(self, block):
        self.available = update_available_boxes(self.available, block)

    def set_available_items(self, available):
        self.available  = available

    def set_residualSpaceList(self, residualSpaceList):
        self.residualSpaceList = residualSpaceList

    def set_utilization(self,utilization):
        self.utilization = utilization

    def __repr__(self):
        return "{res: %s\n, occu:%s\n, fill: %s\n, ut: %s\n, avail:%s\n" \
               % (self.residualSpaceList, self.planListSpace, self.planListBlock, self.utilization, self.available) + "}\n"

