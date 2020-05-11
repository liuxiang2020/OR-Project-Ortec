import numpy as np
import inspect
import sys
import yaml
from Functions import *
from Block import Block
from Space import Space
from State import State
from create_blocks import *
from inspect import currentframe, getframeinfo
from venv import *
from create_general_candidate_block import *
from create_residual_space import *
from search_block import *
import traceback
from find_solution import find_solution

"""
Global Variables
"""
# store residual space
residualSpace = []
# a dictionary of available items and its quantity
availableItems = {}
stateList = []
occupiedSpace = []
filledblocks = []
"""
Returns the current line number in our program.
"""


def lineno():
    frameinfo = getframeinfo(currentframe())
    print("Currently in", frameinfo.filename, "with line number", inspect.currentframe().f_back.f_lineno)


'''
parse_args: accept a commend and parse the arguments
eg. python testfile.py instance.yaml 
'''


def parse_args():
    if sys.argv == [] or (len(sys.argv) != 2):
        print("USAGE: python -testfile.py -instance.yaml")
        exit()
    return sys.argv[1]


'''
Parse yaml return itemKinds and containerSize, update available items
'''


def parse_yaml(yamlfile: yaml) -> object:
    with open(yamlfile) as f:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        file = yaml.load(f, Loader=yaml.FullLoader)
        containerSize = Size2Pos(file['data']['containerkinds'][0]['loadingspaces'][0]['size'])
        itemKinds = file['data']['itemkinds']
        print(lineno(), "\n", containerSize, itemKinds)
        for i in range(len(itemKinds)):
            availableItems[itemKinds[i]['id']] = itemKinds[i]['quantity']
            print(itemKinds[i]['quantity'])
        return containerSize, itemKinds



if __name__ == "__main__":
    # get container and boxes file information
    instance = parse_args()

    # parse_instance files and update available items
    containerSize, itemKinds = parse_yaml(instance)

    # test find_solution
    state = find_solution(itemKinds,containerSize,availableItems)

    # Global variables
    # print(availableItems)
    #
    # # check simple blocks
    # simple_lst = create_simple_blocks(itemKinds, containerSize)
    #
    # # check general blocks
    # general_lst = create_general_blocks(itemKinds, containerSize)
    # #print(general_lst)
    #
    # # Build new space, start with empty container
    # s = Space([0,0,0],containerSize,'x')
    # residualSpace.append(s)
    # # check candidate block
    # candidate_block_lst = generate_candidate_block_list(residualSpace[0].get_size(), general_lst, availableItems)
    # # create residual space
    # state = State(residualSpace, occupiedSpace, filledblocks, 0)
    # best_block = search_block(state, candidate_block_lst)
    # residualSpace = create_residual_space(best_block, containerSize, residualSpace)
    # state.set_filledBlocks(filledblocks.append(best_block))
    # state.set_residualSpaceList(residualSpace)
    # # state.set_occupiedSpaceList(state.get_r)
    # print(residualSpace)

    print("Everything passed")
