from create_residual_space import create_residual_space
from generate_candidate_blocklist import generate_candidate_block_list
from completing_process import completing_process
import copy


def build_m1_tree(block, input_state, m, k, j, block_list):
    state = copy.deepcopy(input_state)
    
    space = copy.deepcopy(state.get_residualSpaceList())
    
    cBlockList = generate_candidate_block_list(state.get_residualSpaceList()[-1].get_size(), block_list, state.get_available_items())
    
    bestkTbl = []
    
    if cBlockList == []:
        return []
    
    for i in range(m-1):
        i = min(i, len(cBlockList)-1)
        prevState = copy.deepcopy(state)
        prevSpace = prevState.get_residualSpaceList()[-1]
        cBlock = cBlockList[i]
        prevState.add_block_to_space(cBlock, prevSpace)
        prevState.set_residualSpaceList(create_residual_space(cBlock,prevState.get_residualSpaceList()))
        fState = completing_process(prevState, block_list)
        for l in range(k-1):
            if (len(bestkTbl) == 0):
                bestkTbl.append([copy.deepcopy(prevState), cBlock, copy.deepcopy(fState.get_utilization()), fState])
                
            else:
                if bestkTbl[-1][2] < fState.get_utilization():
                    bestkTbl.append([copy.deepcopy(prevState), cBlock, copy.deepcopy(fState.get_utilization()), fState])
        bestkTbl = sorted(bestkTbl, key = lambda x: x[2], reverse = True)
    return bestkTbl