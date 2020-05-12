import numpy as np
from Block import Block
from Space import Space
from State import State

# from OR-Project-ORTEC import *
"""
NOTE:  Space.py add information of filled blocks and utilization rate
"""
"""
packState: A partial packing plan and a dynamically
changing list of (List of (type)Spaces) residual spaces. 
- residual spaces list
- plan: occupied spaces list and filled blockList) ??maybe space utilization(seperate or total)) 

candidateBlockList: a (type)List wil candiate (type)Blocks
"""
MAX_SIZE = 10


def Progressively_Refined_Tree_Search(block, state):
    # test return
    res_space = [Space([0, 0, 0], [1, 1, 1], 'x')]
    occupied_space = [Space([0, 0, 0], [100, 50, 100], 'x')]
    filled_block = [Block(2)]
    filled_block[0].set_size([100, 50, 100])
    filled_block[0].set_item_quantity(4)
    filled_block[0].set_volume(500000)
    filled_block[0].set_orientation(['LHW'])
    filled_block[0].set_volume_loss(1)
    s = State(res_space, occupied_space, filled_block)
    s.set_utilization(0.98)
    return s


bestUtilization = 0.9


def search_block(packState, candidateBlockList):
    size = len(candidateBlockList) - 1
    # if only wants to limited the length of list, just limit the loop times?
    # if size > MAX_SIZE:
    #     size = MAX_SIZE 
    bestIndex = -1
    bestUtilization = -1
    for i in range(min(size, MAX_SIZE)):
        # curent packState needed to be considered contains 
        # (residual space) and (used space and corresponding filled block) 
        # and (? List of blocks that still feasible)
        currState = packState
        # first block from candidateBlockList, which has the highest fitness score
        currBlock = candidateBlockList[i]
        # Sol is a packState, assume it has a total utilization
        print("curr in search blokc before progress", currState, currBlock)
        Sol = Progressively_Refined_Tree_Search(currBlock, currState);
        print("Sol returned in searchblock", Sol)
        if Sol.get_utilization() > bestUtilization:
            print("curr sol.get_utilization", i, currBlock, Sol.get_filledBlocks)

            bestIndex = i
            bestUtilization = Sol.get_utilization()
            print("bestUtilization", bestUtilization)
    # return the suitable block for the residual space
    return candidateBlockList[bestIndex]
