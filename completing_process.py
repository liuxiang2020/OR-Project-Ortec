from generate_candidate_blocklist_2 import generate_candidate_block_list
from transfer_residual_space import transfer_residual_space
from create_residual_space import create_residual_space
from Functions import update_available_boxes

def completing_process(prevState, block_list, containerSize):
    curState = prevState
    for i in range(len(curState.get_space_residualSpaceList() - 1), 0 , -1):
        space = curState.get_residualSpaceList()[-1]
        cBlocKList = generate_candidate_block_list(space.get_size(), block_list, curState.get_available_items())
        if cBlocKList:
            #add best fitting block to space
            bestBlock = cBlocKList[0]
            curState.add_space_planListSpace(space)
            curState.add_block_planListBlock(bestBlock)
            _ = create_residual_space(bestBlock, containerSize, space)
            available_boxes = update_available_boxes(curState.get_available_items(), bestBlock)
            curState.set_available_items(available_boxes)

        else:
            _ = transfer_residual_space(curState.get_residualSpaceList()[i])
    curState.set_utilization()
    return curState