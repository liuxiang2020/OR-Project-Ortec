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
        self.space_volume = 0
        self.block_volume = 0
    
    def add_block_to_space(self, block, space):
        space_volume_temp = space.get_size()[0] * space.get_size()[1] * space.get_size()[2]
        if block.get_absolute_volume() > space_volume_temp:
            print("Adding block not allowed, space to small.")
        self.add_block_planListBlock(block)
        self.add_space_planListSpace(space,block.get_volume_loss())
        self.update_available_items(block)
        self.update_utilization()


    def add_block_planListBlock(self, block):
        self.planListBlock.append(block)
        self.block_volume += block.get_real_volume()

    def add_space_planListSpace(self, space, block_loss):
        self.planListSpace.append(space)
        self.space_volume += (space.get_size()[0] * space.get_size()[1] * space.get_size()[2])

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

    def set_utilization(self, utilization):
        self.utilization = utilization

    def update_utilization(self):
        if self.space_volume == 0:
            self.utilization = 0
        else:
            self.utilization = self.block_volume/self.space_volume

    def __repr__(self):
        return "{residualSpaceList: %s\n, planListSpace:%s\n, planListBlock: %s\n, utilization: %s\n, avail:%s\n" \
               % (self.residualSpaceList, self.planListSpace, self.planListBlock, self.utilization, self.available) + "}\n"

