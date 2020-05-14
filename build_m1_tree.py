from create_residual_space import create_residual_space
from generate_candidate_blocklist_2 import generate_candidate_block_list
from completing_process import completing_process
from Functions import update_available_boxes

def build_m1_tree(block, state, m, k, j, block_list, containerSize):
    # TODO I add some ...
    bestTbl = []
    _ = create_residual_space(block, containerSize, state.get_residualSpaceList())

    # do we just want the back or we want to pop it out?
    space = state.get_residualSpaceList()[-1]
    bestTbl.append([state, block, state.get_utilization()])
    cBlocKList = generate_candidate_block_list(space.get_size(), block_list, state.get_available_items())
    # No Blocks??
    print(cBlocKList)
    if cBlocKList:
        for i in range(m-1):
            #think about it which space and block had to be add
            prevState = state
            prevSpace = prevState.get_residualSpaceList()[-1]
            cBlock = cBlocKList[i]
            prevSpace.add_space_planListSpace(space)
            prevSpace.add_block_planListBlock(cBlock)
            fState = completing_process(prevState, block_list, containerSize)
            # TODO bestTbl is a list of list of States?
            if len(bestTbl) < k:
                for l in range(k-1):
                #bestTbl 2dimTable [l]: best k solution
                    if bestTbl[l][2]() < fState.get_Utilisation():
                        bestTbl[l][0] = prevState
                        bestTbl[l][1] = cBlock
                        bestTbl[l][2] = fState.get_Utilisation()
            else:
                bestTbl.append([prevState, cBlock, fState.get_Utilisation()])
            
            #sortbestTbl
    return bestTbl