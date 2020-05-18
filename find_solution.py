from create_residual_space import create_residual_space
from search_block import search_block
from Functions import update_available_boxes
from transfer_residual_space import transfer_residual_space
from create_blocks import create_general_blocks
from Space import Space
from State import State
from generate_candidate_blocklist import generate_candidate_block_list
from completing_process import completing_process
from Block import Block
import traceback
from inspect import currentframe, getframeinfo
from config import *

def lineno():
    frameinfo = getframeinfo(currentframe())
    #print("Currently in", frameinfo.filename, "with line number", currentframe().f_back.f_lineno)


"""
itemKinds: yaml
CONTAINER_SIZE: [L,W,H]
available: dictionary, key:value  <-> id:quantity
"""

def find_solution(itemKinds):
    # create available items
    available_items = {}
    for i in range(len(itemKinds)):
        available_items[itemKinds[i]['id']] = itemKinds[i]['quantity']
    
    # create general block list
    block_list = create_general_blocks(itemKinds)
    space = Space([0, 0, 0], CONTAINER_SIZE, 'x', [0,0,0])
    space_list = [space]
    packState = State(space_list)
    packState.set_available_items(available_items)
    while (packState.get_residualSpaceList()):
        considered_space = packState.get_residualSpaceList()[-1]
        # print("in space", considered_space)
        candidate_list = generate_candidate_block_list(considered_space.get_size(), block_list, available_items)
        # print("with space", considered_space, "the candidate_list", candidate_list)
        if candidate_list:
            #packed_block = search_block(packState, candidate_list, block_list, available_items)
            packed_block = candidate_list[0]
            packState.add_block_to_space(packed_block, considered_space)

            space_list = create_residual_space(packed_block, space_list)
        else:
            if len(space_list) <= 1:
                break
            else:
                space_list = transfer_residual_space(space_list)
    packState.set_residualSpaceList(space_list)
    # print("packstate", packState)
    return packState, block_list