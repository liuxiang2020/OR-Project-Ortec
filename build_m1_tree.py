from create_residual_space import create_residual_space
from generate_candidate_blocklist import generate_candidate_block_list
from completing_process import completing_process
import copy


def build_m1_tree(block, state, m, k, j, block_list):
    bestTbl = [] #list of k best interim solution saves [state,block and utilization]
    s = copy.deepcopy(state)    
    if state.get_residualSpaceList():
        space = state.get_residualSpaceList()[-1]
    else:
        #there is no space left. So return the last state        
        return bestTbl.append([s, block, state.get_utilization()])
    scomp = completing_process(s, block_list)
    bestTbl.append([scomp, block, scomp.get_utilization()])
    cBlocKList = generate_candidate_block_list(space.get_size(), block_list, state.get_available_items())

    if cBlocKList:
        for i in range(min(len(cBlocKList), m-1)):
            prevState = copy.deepcopy(state)
            # if we use get residual ,then candidate block size need to recalculated since
            # curently the candidate block list is based on previously space we got
            # prevSpace = prevState.get_residualSpaceList()[-1]
            prevSpace = space
            cBlock = cBlocKList[i]
            prevState.add_block_to_space(cBlock, prevSpace)
            prevState.set_residualSpaceList(create_residual_space(cBlock, prevState.get_residualSpaceList()))
            fState = completing_process(prevState, block_list)

            if len(bestTbl) == k:
                for l in range(k-1, 0 , -1):
                    if bestTbl[l][0].get_utilization() < fState.get_utilization():
                        bestTbl[l][0] = fState
                        bestTbl[l][1] = cBlock
                        bestTbl[l][2] = fState.get_utilization()
                        break
            else:
                bestTbl.append([fState, cBlock, fState.get_utilization()])
            
            bestTbl = sorted(bestTbl, key=lambda x: x[2], reverse=True)
    return bestTbl
