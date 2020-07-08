from create_residual_space import create_residual_space
from generate_candidate_blocklist import generate_candidate_block_list
from build_m1_tree import build_m1_tree
from completing_process import completing_process
import math
import copy
from config import *


def calc_L(m):
    m_root = int(math.sqrt(m))
    numerator = (((6*7 + 1) * (m + ((math.floor(m_root)*math.floor(m_root)) - (math.floor(m_root))))) - m)
    denominator = (K*m)
    return math.floor(numerator/denominator)


def Progressively_Refined_Tree_Search(block, input_state, block_list):
    state = copy.deepcopy(input_state)
    
    space = copy.deepcopy(state.get_residualSpaceList()[-1])
    
    state.add_block_to_space(block, space)
    
    res_space = create_residual_space(block,state.get_residualSpaceList())
    
    state.set_residualSpaceList(res_space)
    
    cBlockList = generate_candidate_block_list(res_space[-1].get_size(), block_list, state.get_available_items())
    
    BestSl = [state, block, state.get_utilization(), state]
    bkTab = []
    
    for i in range(STAGE_L-1):
        m = M_Zero * SCALE
        lm1 = calc_L(m)
        bkTab.append(build_m1_tree(block, state, m, K, 0, block_list))
        for j in range(1,lm1,1):
            j = min (lm1, len(bkTab))
            for d in range(len(bkTab[j-1])):
                nState = copy.deepcopy(bkTab[j-1][d][0])
                nBlock = copy.deepcopy(bkTab[j-1][d][1])
                bkTab.append(build_m1_tree(nBlock, nState, m, K, j, block_list))
        for j in range(min(lm1, len(bkTab)-1)):
            if (len(bkTab[j]) == 0) : continue
            if (bkTab[j][0][2] > BestSl[2]):
                BestSl = bkTab[j][0]
    return completing_process(BestSl, block_list)
                
                
        
