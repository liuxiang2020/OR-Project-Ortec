from generate_candidate_blocklist_2 import generate_candidate_block_list
from transfer_residual_space import transfer_residual_space

def completing_process(prevState, block_list, available_boxes):
    curState = prevState
    for i in range(len(curState.get_space_residualSpaceList().pop() - 1), 0 , -1):
        space = curState.get_residualSpaceList()[i]
        cBlocKList = generate_candidate_block_list(space.get_size(), block_list, available_boxes)
        if cBlocKList:
            bestBK = cBlocKList[0]
            curState.add_space_planListSpace(space)
            curState.add_block_planListBlock(bestBK)
        else:
            space_list = transfer_residual_space(curState.get_residualSpaceList()[i])
    curState.set_utilization()
    return curState