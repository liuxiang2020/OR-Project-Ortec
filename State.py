"""
Class State:
residualSpaceList: a list of residual space list. eg. [Space A, Space B]
planListSpace: a list of occupied Space eg. ..
planListSpace: a list of filled Blocks eg [Block A, Block B]
utilization: record current utilization rate
available: record currently available items, it is a dictionary of id: quantity
"""
from Functions import update_available_boxes
from config import *

class State:
    def __init__(self, residualSpaceList, container_size):
        self.residualSpaceList = residualSpaceList
        self.planListSpace = []
        self.planListBlock = []
        self.available = {}
        self.space_volume = 0
        self.real_block_volume = 0
        self.container_size = container_size
    
    def add_block_to_space(self, block, space):
        space_volume_temp = space.get_size()[0] * space.get_size()[1] * space.get_size()[2]
        if block.get_absolute_volume() > space_volume_temp:
            raise Exception("Sorry, volume in State not sufficient!")
        self.add_block_planListBlock(block)
        self.add_space_planListSpace(space,block.get_volume_loss())
        self.update_available_items(block)


    def add_block_planListBlock(self, block):
        self.planListBlock.append(block)
        self.real_block_volume += block.get_real_volume()
             

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
        return (self.real_block_volume / (self.container_size[0]*self.container_size[1]*self.container_size[2]))

    def get_available_items(self):
        return self.available

    def update_available_items(self, block):
        self.available = update_available_boxes(self.available, block)

    def set_available_items(self, available):
        self.available  = available

    def set_residualSpaceList(self, residualSpaceList):
        self.residualSpaceList = residualSpaceList


    def __repr__(self):
        return "{residualSpaceList: %s\n, planListSpace:%s\n, planListBlock: %s\n, utilization: %s\n, avail:%s\n" \
               % (self.residualSpaceList, self.planListSpace, self.planListBlock, self.get_utilization(), self.available) + "}\n"

