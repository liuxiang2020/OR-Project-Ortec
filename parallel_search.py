import copy
from progressively_refined_tree_search import Progressively_Refined_Tree_Search
import threading
from conversion import *
from config import *

def f(res,i,currBlock,currState,block_list):
    Sol = Progressively_Refined_Tree_Search(currBlock, currState, block_list)
    res[i] = Sol
    
def search_block_p(packState, candidateBlockList, block_list, available_boxes):
    size = len(candidateBlockList)
    bestIndex = -1
    bestUtilization = -1
    res = []
    threads = []
    for i in range(min(size, MAX_SIZE)):
        res.append(0)
    for i in range(min(size, MAX_SIZE)):
        currState = copy.deepcopy(packState)
        currBlock = candidateBlockList[i]
        t = threading.Thread(target=f,args=(res,i,currBlock,currState,block_list))
        threads.append(t)
        t.start()
    for k in threads:
        k.join()
    #print(res)
    for j in range(len(res)):
        if res[j].get_utilization() > bestUtilization:
            #print("curr sol.get_utilization", i, currBlock, Sol.get_planListBlock())
            bestIndex = j
            bestUtilization = res[j].get_utilization()
    #print(bestIndex)
    print(bestUtilization)
    return candidateBlockList[bestIndex],res[bestIndex]
