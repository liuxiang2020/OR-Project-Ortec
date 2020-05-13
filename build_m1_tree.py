from create_residual_space import create_residual_space
from generate_candidate_blocklist_2 import generate_candidate_block_list
from completing_process import completing_process
from Functions import update_available_boxes

def build_m1_tree(block, state, m, k, j, block_list, available_boxes, containerSize, bestTbl):
    # TODO I add some ...
    space_list = create_residual_space(block.get_size(), containerSize, state.get_residualSpaceList())

    # do we just want the back or we want to pop it out?
    space = state.get_residualSpaceList().pop()
    #added
    cBlocKList = generate_candidate_block_list(space, block_list,state.get_available_items())
    state.add_space_planListSpace(space)
    state.add_block_planListBlock(block)

    for i in range(m-1):
        prevState = state
        prevSpace = prevState.get_residualSpaceList().pop()
        print(cBlocKList)
        cBlock = cBlocKList[i]
        prevSpace.add_space_planListSpace(space)
        prevSpace.add_block_planListBlock(cBlock)
        fState = completing_process(prevState, block_list, available_boxes)
        # TODO bestTbl is a list of list of States?
        for l in range(k-1):
            if bestTbl:
                if bestTbl[l].get_Utilisation() < fState.get_Utilisation():
                    bestTbl[l].state = prevState
                    bestTbl[l].block = cBlock
                    bestTbl[l].Utilisation = fState.get_Utilisation()
            else:
                bestTbl[l].state = prevState
                bestTbl[l].block = cBlock
                bestTbl[l].Utilisation = fState.get_Utilisation()
        
        #sortbestTbl
    return bestTbl