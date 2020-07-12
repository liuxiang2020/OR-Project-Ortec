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
from generate_candidate_blocklist import generate_candidate_block_list
from create_residual_space import *
from search_block import search_block
import traceback
from find_solution import find_solution
from transfer_residual_space import transfer_residual_space
from conversion import *


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
    if sys.argv == []:
        print("USAGE: python run.py instance.yaml output_name.yaml")
        exit()
    return sys.argv[1], sys.argv[2]


'''
Parse yaml return itemKinds and containerSize, update available items
'''


def parse_yaml(yamlfile: yaml) -> object:
    with open(yamlfile) as f:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        file = yaml.load(f, Loader=yaml.FullLoader)
        
        itemKinds = file['data']['itemkinds']
        #print(lineno(), "\n", CONTAINER_SIZE, itemKinds)
        for i in range(len(itemKinds)):
            availableItems[itemKinds[i]['id']] = itemKinds[i]['quantity']
            print(itemKinds[i]['quantity'])
        container_size = Size2Pos(file['data']['containerkinds'][0]['loadingspaces'][0]['size'])
        return itemKinds, container_size

def execute_algo():
    import datetime
    import argparse
    begin_time = datetime.datetime.now()
    # get container and boxes file information

    args = None
    parser = argparse.ArgumentParser(description="Visualize loadbuilding solutions")
    parser.add_argument('--instance', '-I',  metavar='INPUT_FILE', required=True, help='The instance file')
    #parser.add_argument('--sol', '-IS',  metavar='INPUT_SOLUTION_FILE', required=True, help='The input solution file')
    parser.add_argument('--solution', '-S',  metavar='SOLUTION_FILE', required=True, help='The solution file')
    parser.add_argument('--runtime', '-R', metavar='MAX_RUNTIME', type = int, required=True, help='Maximum runtime to calculate solution in seconds')

    args = parser.parse_args(args)   
    
    instance = args.instance
    #i_sol_path = args.sol
    solution_path = args.solution    
    #instance = input

    itemKinds, container_size = parse_yaml(instance)
    state, block_dict = find_solution(itemKinds, container_size, args.runtime)
    print(50*'#')
    print(state)
    convert_state_to_solution(instance,state,block_dict,solution_path)
    # print(testvariable)
    # print(transfer_residual_space([]))

    print("Everything passed, Runtime details:")
    print(datetime.datetime.now())
    print(datetime.datetime.now() - begin_time)

if __name__ == "__main__":
    execute_algo()
    
