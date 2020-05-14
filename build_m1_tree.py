from create_residual_space import create_residual_space
from generate_candidate_blocklist import generate_candidate_block_list
from completing_process import completing_process
from Functions import update_available_boxes


def build_m1_tree(block, state, m, k, j, block_list):
    # TODO I add some ...
    bestTbl = []
    _ = create_residual_space(block, state.get_residualSpaceList())

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
            prevState.add_space_planListSpace(space)
            prevState.add_block_planListBlock(cBlock)
            fState = completing_process(prevState, block_list)
            # TODO bestTbl is a list of list of States?
            print(bestTbl,"nnnnn")
            if len(bestTbl) < k:
                for l in range(k-1):
                #bestTbl 2dimTable [l]: best k solution
                    # if bestTbl[j][l].get_utilization() < fState.get_utilization():
                    #     bestTbl[j][l][0] = prevState
                    #     bestTbl[j][l][1] = cBlock
                    #     bestTbl[j][l].set_utilization(fState.get_utilization())
                    print(50*"#")
                    print(bestTbl)
                    print(50 * "#" , j, l)
                    if bestTbl[l][0].get_utilization() < fState.get_utilization():
                        bestTbl[l][0] = prevState
                        bestTbl[l][1] = cBlock
                        bestTbl[l][2] = fState.get_utilization()
            else:
                bestTbl.append([prevState, cBlock, fState.get_utilization()])
            
            #sortbestTbl
    return bestTbl