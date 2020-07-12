from create_residual_space import *
from search_block import search_block
from parallel_search import search_block_p
from transfer_residual_space import transfer_residual_space
from create_blocks import create_general_blocks
from Space import Space
from State import State
from generate_candidate_blocklist import generate_candidate_block_list
from inspect import currentframe, getframeinfo
from config import *
from completing_process import completing_process
import copy
import datetime



"""
itemKinds: yaml
CONTAINER_SIZE: [L,W,H]
available: dictionary, key:value  <-> id:quantity
"""

def find_solution(itemKinds, container_size, runtime):
    # create available items
    available_items = {}
    for i in range(len(itemKinds)):
        available_items[itemKinds[i]['id']] = itemKinds[i]['quantity']
    
    
    # create general block list
    time = datetime.datetime.now()
    max_runtime = (datetime.datetime.now().timestamp() + runtime)
    
    block_list, uid_orientation = create_general_blocks(itemKinds, container_size)
    space = Space([0, 0, 0], container_size, 'x')
    space_list = [space]
    packState = State(space_list, container_size)
    packState.set_available_items(available_items)
    best_intermediate = copy.deepcopy(packState)
    print("Setup & Blocklist:")
    print(datetime.datetime.now() - time)
    while (packState.get_residualSpaceList()):
        s = copy.deepcopy(packState)
        considered_space = packState.get_residualSpaceList()[-1]

        candidate_list = generate_candidate_block_list(considered_space.get_size(), block_list, available_items)

        if candidate_list:
            if Parallel:
                packed_block,intermediate = search_block_p(s, candidate_list, block_list, available_items, max_runtime)
            else:
                packed_block,intermediate = search_block(s, candidate_list, block_list, available_items)
            #packed_block = candidate_list[0] <- Use this for (really) fast execution
            packState.add_block_to_space(packed_block, considered_space)
            space_list = create_residual_space(packed_block, space_list)
        else:
            if len(space_list) <= 1:
                break
            else:
                space_list = transfer_residual_space(space_list)
        packState.set_residualSpaceList(space_list)
        print("utilization after search_block in find_solution: ", intermediate.get_utilization())
        if (intermediate.get_utilization() > best_intermediate.get_utilization()):
            best_intermediate = intermediate
        if (max_runtime < datetime.datetime.now().timestamp()):
            break

    if (best_intermediate.get_utilization() > packState.get_utilization()):
        return best_intermediate, block_list, uid_orientation
    else:
        return packState, block_list, uid_orientation
