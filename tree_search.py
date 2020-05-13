from create_residual_space import create_residual_space
from create_general_candidate_block import Generate_Candidate_Block_List
from Build_m1_Tree import Build_m1_Tree
import math
K = 3
M_Zero = 3
SCALE = 3
STAGE_L = 5

def calc_L(k,m):
    m_root =  int(math.sqrt(m))
    numerator = (6*7 + 1) * (m + m_root^2 - m_root) - m
    denominator = k*m
    return numerator/denominator

def progressively_refined_tree_search(block, state):
    space=state.get_residualSpaceList.pop()
    state.plan.spaceList.append(space)
    state.plan.blockList.append(block)
    #TODO
    create_residual_space(state.Spacelist, containerSize, spaceStack)
    #TODO
    cBlocKList = Generate_Candidate_Block_List(space, block, item_available)
    best_solution = state
    #TODO
    m = 1
    #TODO
    for i in range(STAGE_L-1):
        bkTab = []
        m = m*SCALE
        L = calc_L(K,m)
        bkTab.append(Build_m1_Tree(block, state, m, K, 0))
        for j in range(1, L):
            for d in bkTab[j-1].size()-1:
                nState = bkTab[j-1][d].state
                nBlock = bkTab[j-1][d].block
                bkTab.append(Build_m1_Tree(nBlock, nState, m, K, j))
        for j in range(1,L):
            if bkTab[j][0].state.get_utilization() > best_solution.get_utilization():
                best_solution = bkTab[j][0]
    
    return best_solution