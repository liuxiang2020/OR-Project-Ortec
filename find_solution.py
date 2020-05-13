from create_residual_space import create_residual_space
from search_block import search_block
from Functions import update_available_boxes
from transfer_residual_space import transfer_residual_space
from create_blocks import create_general_blocks
from Space import Space
from State import State
from generate_candidate_blocklist_2 import generate_candidate_block_list
from Block import Block
import traceback
from inspect import currentframe, getframeinfo
#from test_algo import *


def lineno():
    frameinfo = getframeinfo(currentframe())
    print("Currently in", frameinfo.filename, "with line number", currentframe().f_back.f_lineno)


#
# available = {(1, 10), (2, 33), (3, 39)}
#
# # [216, 228, 150]
# curr_Space = [220, 230, 155]

"""
itemKinds: yaml
containerSize: [L,W,H]
available: dictionary, key:value  <-> id:quantity
"""

def find_solution(itemKinds, containerSize, available):
    block_list = create_general_blocks(itemKinds, containerSize)
    space = Space([0, 0, 0], containerSize, 'x')
    space_list = [space]
    packState = State(space_list)
    available_boxes = available
    for i in range(len(space_list)):
        considered_space = space_list[i]

        # print("in space", considered_space)
        candidate_list = generate_candidate_block_list(considered_space.get_size(), block_list, available_boxes)

        # print("with space", considered_space, "the candidate_list", candidate_list)
        if candidate_list:
            packed_block = search_block(packState, candidate_list, block_list, available_boxes, containerSize)

            # print("if candidate list is not zero, packed block",packed_block)
            packState.add_block_planListBlock(packed_block)
            packState.add_space_planListSpace(considered_space)
            # TODO: needs check -- checked
            available_boxes = update_available_boxes(available_boxes, packed_block)

            # print("available boxes quantity", available_boxes,"\n",
            #       "with choosen block size", block_size)
            space_list = create_residual_space(packed_block, containerSize, space_list)

            # print("residual space", space_list)
        else:
            if len(space_list) <= 1:
                break
            else:
                space_list = transfer_residual_space(space_list)
    packState.set_residualSpaceList(space_list)
    packState.set_available_items(available_boxes)
    # print("packstate", packState)
    return packState