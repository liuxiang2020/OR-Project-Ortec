import numpy as np
import Block.py
import Space.py
import State.py
#from OR-Project-ORTEC import *
"""
NOTE: Space.py add information of filled blocks and utilization rate
"""
"""
packState: A partial packing plan and a dynamically
changing list of (List of (type)Spaces) residual spaces. 
- residual spaces list
- plan: occupied spaces list and filled blockList) ??maybe space utilization(seperate or total)) 

candidateBlockList: a (type)List wil candiate (type)Blocks
"""
MAX_SIZE = 10
def search_block(packState, candidateBlockList):
    size = len(candidateBlockList) -1
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
        #first block from candidateBlockList, which has the highest fitness score
        currBlock = candidateBlockList[i]
        #Sol is a packState, assume it has a total utilization
        Sol = Progressively_Refined_Tree_Search(currBlock, currState);
        if Sol.get_utilization() > bestUtilisation:
            bestIndex = i
            bestUtilization = Sol.get_utilization()
    #return the suitable block for the residual space 
    return candidateBlockList[bestIndex]

    