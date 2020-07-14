import copy
from progressively_refined_tree_search import Progressively_Refined_Tree_Search
from config import *
import datetime
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

bestUtilization = 0.9


def search_block(packState, candidateBlockList, block_list, available_boxes, max_runtime):
    size = len(candidateBlockList)
    # if only wants to limited the length of list, just limit the loop times?
    # if size > MAX_SIZE:
    #     size = MAX_SIZE 
    bestIndex = -1
    bestUtilization = -1
    res = 0
    #print(candidateBlockList[0:2])
    for i in range(min(size, MAX_SIZE)):
        if max_runtime > datetime.datetime.now().timestamp():
        # curent packState needed to be considered contains 
        # (residual space) and (used space and corresponding filled block) 
        # and (? List of blocks that still feasible)
            currState = copy.deepcopy(packState)

        # first block from candidateBlockList, which has the highest fitness score
            currBlock = candidateBlockList[i]
        # Sol is a packState, assume it has a total utilization
            Sol = Progressively_Refined_Tree_Search(currBlock, currState, block_list, max_runtime)
            if Sol.get_utilization() > bestUtilization:

                bestIndex = i
                bestUtilization = Sol.get_utilization()
                res = Sol
    # return the suitable block for the residual space
    if bestIndex==-1:
        exit()
    #print(bestUtilization)
    return candidateBlockList[bestIndex],res
