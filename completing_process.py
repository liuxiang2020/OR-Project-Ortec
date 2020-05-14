from generate_candidate_blocklist import generate_candidate_block_list
from transfer_residual_space import transfer_residual_space
from config import *
from State import State
from Space import Space
from create_residual_space import create_residual_space
"""
completing_process: If the fitness measure considers only the total volume of all boxes in
each block, then the placement is simply placing the block with the biggest volume into each space.
"""
def completing_process(prevState, block_list):
    curState = prevState
    # loop through residual space list backwards (largest space first，index range [length, 0))
    for i in range(len(curState.get_residualSpaceList()), 0 , -1):
        space = curState.get_residualSpaceList()[-1]
        cBlocKList = generate_candidate_block_list(space.get_size(), block_list, curState.get_available_items())
        if cBlocKList:
            #add best fitting block to space
            bestBlock = cBlocKList[0]
            curState.add_space_planListSpace(space)
            curState.add_block_planListBlock(bestBlock)
            curState.update_utilization()
            _ = create_residual_space(bestBlock, curState.get_residualSpaceList())
            # available_boxes = update_available_boxes(curState.get_available_items(), bestBlock)
            curState.update_available_items(bestBlock)
            # curState.set_available_items(available_boxes)

        else:
            _ = transfer_residual_space(curState.get_residualSpaceList()[i-1])


        #                                           curState.add_block_planListBlock(bestBlock) so that utilization is set immediantly
        # curState.update_utilization()
    return curState
