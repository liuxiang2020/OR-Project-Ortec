from create_residual_space import create_residual_space
from generate_candidate_blocklist import generate_candidate_block_list
from build_m1_tree import build_m1_tree
from completing_process import completing_process
import math
import copy
from config import *
import datetime

def calc_L(k,m):
    m_root =  int(math.sqrt(m))

    numerator = ((6*7 + 1) * (m + m_root*m_root - m_root)) - m
    denominator = k*m
    return numerator/denominator



#search best solution for Block block and State state
def Progressively_Refined_Tree_Search(block, state, block_list, max_runtime):
    space = state.get_residualSpaceList()[-1] # get last item in list
    #put block into the space and update residualSpaceList
    state.add_block_to_space(block, space)
    state.set_residualSpaceList(create_residual_space(block, state.get_residualSpaceList()))
    space = state.get_residualSpaceList()[-1]
    # Generate Blocklist for new spaces
    cBlocKList = generate_candidate_block_list(space.get_size(), block_list, state.get_available_items())
    #block = cBlocKList[0]
    #current best solution is putting just one block in the empty size
    best_solution = copy.deepcopy(state) 

    if cBlocKList:
        m = M_Zero
        bkTab = []
        for _ in range(STAGE_L -1):
            m = m*SCALE

            L = int(calc_L(K,m))
            tree = build_m1_tree(block, state, m, K, 0, block_list)
            if type(tree) != type(None):
                bkTab.append(tree)
            for j in range(1, min(L , len(bkTab))):

                if type(bkTab[j-1]) == type(None):
                    pass
                else:
                    for d in range(len(bkTab[j-1])):
                        nState = copy.deepcopy(bkTab[j-1][d][0])
                        nBlock = bkTab[j-1][d][1]
                        tree = build_m1_tree(nBlock, nState, m, K, j, block_list)
                        if type(tree) != type(None):
                            bkTab.append(tree)
            for j in range(min(L, len(bkTab))):

                if type(bkTab[j]) == type(None):
                    pass
                elif bkTab[j][0][2] > best_solution.get_utilization():
                    best_solution = bkTab[j][0][0]
    else:
        return completing_process(best_solution, block_list)
    return best_solution