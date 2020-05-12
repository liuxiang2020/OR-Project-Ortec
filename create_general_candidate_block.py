# item_usage: store quantity of different types of boxes have been used
# it is a counter of tuple [(id,quantity remain), (id,quantityremain)....]

# check box availability, discard blocks if 
# a block containing a certain number of a type of boxes has already been placed in the 
# container, then another block which requires more boxes of this
# type than the available left-over 
from Block import Block
from test_algo import *

def check_availability (gb, item_available):
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

    '''DEBUG
    print("start")
    for i in range(len(generalBlockList)):
        print(generalBlockList[i].get_id(), generalBlockList[i].get_item_quantity(),
              generalBlockList[i].get_fitness())
    print("end")
    
    '''
    for gb in generalBlockList:
        # Check block size and space size
        if (gb.get_size()[0] <= currSpace[0]) and (gb.get_size()[1] <= currSpace[1]) and (gb.get_size()[2] <= currSpace[2]):
            # Check fitness
            spaceVolume = currSpace[0] * currSpace[1] * currSpace[2]
            gbVolume = gb.get_volume()
            if (spaceVolume-gbVolume) <= gbVolume:
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
