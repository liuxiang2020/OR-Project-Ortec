from generate_candidate_blocklist import generate_candidate_block_list
from transfer_residual_space import transfer_residual_space
from config import *
from State import State
from Space import Space
from create_residual_space import *
import copy
"""
completing_process: If the fitness measure considers only the total volume of all boxes in
each block, then the placement is simply placing the block with the biggest volume into each space.
"""
def completing_process(prevState, block_list):
    curState = prevState
    # loop through residual space list backwards (largest space first，index range [length, 0))
    while curState.get_residualSpaceList() != []:
        space = curState.get_residualSpaceList()[-1]
        cBlocKList = generate_candidate_block_list(space.get_size(), block_list, curState.get_available_items())
        if cBlocKList:
            #add best fitting block to space
            bestBlock = cBlocKList[0]
            curState.add_block_to_space(bestBlock, space)

            curState.set_residualSpaceList = create_residual_space(bestBlock, curState.get_residualSpaceList())


        else:
            curState.set_residualSpaceList = transfer_residual_space(curState.get_residualSpaceList())

    return curState
