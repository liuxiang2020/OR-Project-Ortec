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
from conversion import convert_state_to_solution



def parse_yaml(yamlfile: yaml) -> object:
    availableItems = {}
    with open(yamlfile) as f:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        file = yaml.load(f, Loader=yaml.FullLoader)
        
        itemKinds = file['data']['itemkinds']
        for i in range(len(itemKinds)):
            availableItems[itemKinds[i]['id']] = itemKinds[i]['quantity']
            print(itemKinds[i]['quantity'])
        container_size = Size2Pos(file['data']['containerkinds'][0]['loadingspaces'][0]['size'])
        return itemKinds, container_size, availableItems

def execute_algo():
    import datetime
    import argparse
    begin_time = datetime.datetime.now()
    # get container and boxes file information

    args = None
    parser = argparse.ArgumentParser(description="Visualize loadbuilding solutions")
    parser.add_argument('--instance', '-I',  metavar='INPUT_FILE', required=True, help='The instance file')
    parser.add_argument('--solution', '-S',  metavar='SOLUTION_FILE', required=True, help='The solution file')
    parser.add_argument('--runtime', '-R', metavar='MAX_RUNTIME', type = int, required=True, help='Maximum runtime to calculate solution in seconds')

    args = parser.parse_args(args)   
    
    instance = args.instance
    solution_path = args.solution    

    itemKinds, container_size, availableItems = parse_yaml(instance)
    state, block_dict, uid_orientation = find_solution(itemKinds, container_size, args.runtime)
    print(50*'#')
    print(state)
    convert_state_to_solution(instance,state,block_dict,solution_path, uid_orientation)
    
    print("Everything passed, Runtime details:")
    print(datetime.datetime.now())
    print(datetime.datetime.now() - begin_time)

if __name__ == "__main__":
    execute_algo()
    
