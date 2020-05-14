from create_residual_space import create_residual_space
from generate_candidate_blocklist import generate_candidate_block_list
from completing_process import completing_process
from Functions import update_available_boxes
import copy


def build_m1_tree(block, state, m, k, j, block_list):
    bestTbl = [] #list of k best interim solution saves [state,block and utilization]
    if state.get_residualSpaceList():
        _ = create_residual_space(block, state.get_residualSpaceList())
    else:
        #there is no space left. So return the last state
        return bestTbl.append([state, block, state.get_utilization()])

    space = state.get_residualSpaceList()[-1]
    bestTbl.append([state, block, state.get_utilization()])
    cBlocKList = generate_candidate_block_list(space.get_size(), block_list, state.get_available_items())

    if cBlocKList:
        for i in range(min(len(cBlocKList), m-1)):
            # prevState = copy.deepcopy(state) maybe need copy. But no change in result. Calculating time is higher
            prevState = state
            prevSpace = prevState.get_residualSpaceList()[-1]
            cBlock = cBlocKList[i]
            prevState.add_block_to_space(cBlock, prevSpace)
            fState = completing_process(prevState, block_list)

            if len(bestTbl) == k:
                for l in range(k-1, 0 , -1):
                    if bestTbl[l][0].get_utilization() < fState.get_utilization():
                        bestTbl[l][0] = prevState
                        bestTbl[l][1] = cBlock
                        bestTbl[l][2] = fState.get_utilization()
                        break
            else:
                bestTbl.append([prevState, cBlock, fState.get_utilization()])
            
            bestTbl = sorted(bestTbl, key=lambda x: x[2], reverse=True)
    return bestTbl