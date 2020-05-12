from create_residual_space import create_residual_space
from create_general_candidate_block import *
from search_block import search_block
from Functions import update_available_boxes
from transfer_residual_space import transfer_residual_space
from create_blocks import create_general_blocks
from Space import Space
from State import State
from create_general_candidate_block import *
from Block import Block
import traceback
from test_algo import *


def lineno():
    frameinfo = getframeinfo(currentframe())
    print("Currently in", frameinfo.filename, "with line number", inspect.currentframe().f_back.f_lineno)


def check_availability(gb, item_available):
    for i in range(len(gb.get_id())):
        id = gb.get_id()[i]
        if item_available[id] >= gb.get_item_quantity()[i]:
            continue;
        else:
            return False
    return True


#
# available = {(1, 10), (2, 33), (3, 39)}
#
# # [216, 228, 150]
# curr_Space = [220, 230, 155]


def generate_candidate_block_list(currentSpace, generalBlockList, item_available):
    candidateBlockList = []
    # currSpace = [L,W,H]
    currSpace = currentSpace
    print("curr",currSpace)

    '''DEBUG
    print("start")
    for i in range(len(generalBlockList)):
        print(generalBlockList[i].get_id(), generalBlockList[i].get_item_quantity(),
              generalBlockList[i].get_fitness())
    print("end")

    '''
    for gb in generalBlockList:
        # Check block size and space size
        if (gb.get_size()[0] <= currSpace[0]) and (gb.get_size()[1] <= currSpace[1]) and (
                gb.get_size()[2] <= currSpace[2]):
            # Check fitness
            spaceVolume = currSpace[0] * currSpace[1] * currSpace[2]
            gbVolume = gb.get_volume()
            if (spaceVolume - gbVolume) <= gbVolume:
                if check_availability(gb, item_available):
                    fitness = 2 * gbVolume - spaceVolume
                    gb.set_fitness(fitness)
                    candidateBlockList.append(gb)

    candidateBlockList.sort(key=lambda x: x.get_fitness(), reverse=True)

    '''DEBUG
    for i in range(len(candidateBlockList)):
    print(candidateBlockList[i].get_id(),candidateBlockList[i].get_item_quantity(),candidateBlockList[i].get_fitness(),candidateBlockList[i].get_orientation())
    '''
    return candidateBlockList

"""
itemKinds: yaml
containerSize: [L,W,H]
available: dictionary, key:value  <-> id:quantity
"""

def find_solution(itemKinds, containerSize, available):
    block_list = create_general_blocks(itemKinds, containerSize)
    print("in find solution, create general blocks",block_list)
    space = Space([0, 0, 0], containerSize, 'x')
    space_list = [space]
    start_state = State(space_list,[],[])
    solution_block_list = []
    solution_space_list = []
    available_boxes = available
    for i in range(len(space_list)):
        print(lineno(), "in loop with number" ,i)
        considered_space = space_list[i]
        print("in space", considered_space)
        candidate_list = generate_candidate_block_list(considered_space.get_size(), block_list, available_boxes)
        print("with space", considered_space, "the candidate_list", candidate_list)
        if candidate_list:
            packed_block = search_block(start_state, candidate_list)
            print("if candidate list is not zero, packed block",packed_block)
            solution_block_list.append(packed_block)
            solution_space_list.append(considered_space)

            # TODO: needs check -- checked
            available_boxes = update_available_boxes(available_boxes, packed_block)
            block_size = packed_block.get_size()
            print("available boxes quantity", available_boxes,"\n",
                  "with choosen block size", block_size)
            space_list = create_residual_space(block_size, containerSize, space_list)
            print("residual space", space_list)
        else:
            i = 0
            if len(space_list) <= 1:
                break
            else:
                space_list = transfer_residual_space(space_list)
            i += 1
            if i == 10:
                break

    currState = State(space_list, solution_space_list, solution_block_list)
    currState.set_available_items(available_boxes)
    print("currstate", currState)
    return currState