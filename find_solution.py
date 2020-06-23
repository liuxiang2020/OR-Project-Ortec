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
import datetime

def lineno():
    frameinfo = getframeinfo(currentframe())
    #print("Currently in", frameinfo.filename, "with line number", currentframe().f_back.f_lineno)


"""
itemKinds: yaml
CONTAINER_SIZE: [L,W,H]
available: dictionary, key:value  <-> id:quantity
"""

def recombine_residual_spaces(space_list):
    #Idea: If two spaces are nearby, but split up, a big space is available, but 
    #not used by the algorithm

    for space1 in space_list:
        for space2 in space_list:
            possible_space_size = [0,0,0]
            possible_space_corner = [0,0,0]
            #Collect equal corners
            corner_eq = []
            if (space1.corner[0] == space2.corner[0]):
                corner_eq.append(True)
            else:
                corner_eq.append(False)
                
            if (space1.corner[1] == space2.corner[1]):
                corner_eq.append(True)
            else:
                corner_eq.append(False)
                
            if (space1.corner[2] == space2.corner[2]):
                corner_eq.append(True)
            else:
                corner_eq.append(False)
            print(corner_eq)
                
                
            # Length 3 shouldn't occur at all
            if (corner_eq.count(True) == 1):
                print("Starting recombination check")
                for dim in range(3):
                    if (corner_eq[dim] == False):
                        if(space1.corner[dim] < space2.corner[dim]):
                            if(space1.corner[dim]+space1.size[dim] > space2.corner[dim]):
                                possible_space_size[dim] = (space1.corner[dim] + space1.size[dim]) - space2.corner[dim]
                                possible_space_corner[dim] = (space1.corner[dim] + (space1.size[dim] - possible_space_size[dim]))
                        else:
                            if(space2.corner[dim]+space2.size[dim] > space1.corner[dim]):
                                possible_space_size[dim] = (space2.corner[dim] + space2.size[dim]) - space1.corner[dim]
                                possible_space_corner[dim] = (space2.corner[dim] + (space2.size[dim] - possible_space_size[dim]))
                    if (corner_eq[dim] == True):
                        possible_space_size[dim] = min(space1.size[dim], space2.size[dim])
                        possible_space_corner[dim] = space1.corner[dim]
                if ((possible_space_size[0] * possible_space_size[1] * possible_space_size[2]) > 0):
                    # No space transfer on this experimental part
                    print("OH DAMN BOY")
                    exit()
                    space_list.append(possible_space_corner, possible_space_size, 'z')
                
                    
    

def find_solution(itemKinds, container_size):
    # create available items
    available_items = {}
    for i in range(len(itemKinds)):
        available_items[itemKinds[i]['id']] = itemKinds[i]['quantity']
    
    
    # create general block list
    time = datetime.datetime.now()
    block_list = create_general_blocks(itemKinds, container_size)
    space = Space([0, 0, 0], container_size, 'x')
    space_list = [space]
    packState = State(space_list, container_size)
    packState.set_available_items(available_items)
    print("Setup & Blocklist:")
    print(datetime.datetime.now() - time)
    while (packState.get_residualSpaceList()):
        considered_space = packState.get_residualSpaceList()[-1]
        # print("in space", considered_space)
        candidate_list = generate_candidate_block_list(considered_space.get_size(), block_list, available_items)
        # print("with space", considered_space, "the candidate_list", candidate_list)
        if candidate_list:
            if Parallel:
                packed_block = search_block_p(packState, candidate_list, block_list, available_items)
            else:
                packed_block = search_block(packState, candidate_list, block_list, available_items)
            #packed_block = candidate_list[0]
            packState.add_block_to_space(packed_block, considered_space)
            space_list = create_residual_space(packed_block, space_list)
            recombine_residual_spaces(space_list)
            print(space_list)
        else:
            if len(space_list) <= 1:
                break
            else:
                space_list = transfer_residual_space(space_list)
        packState.set_residualSpaceList(space_list)
    # print("packstate", packState)
    return packState, block_list
