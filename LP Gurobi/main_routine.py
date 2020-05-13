from load_instance import load_instance
from model import solve
from construct_solution_new import construct_solution

from ortec.scientific.benchmarks.loadbuilding import SolutionViewer

import argparse

# read arguments
args = None
parser = argparse.ArgumentParser(description="Visualize loadbuilding solutions")
parser.add_argument('--instance', '-I',  metavar='INPUT_FILE', required=True, help='The instance file')
parser.add_argument('--solution', '-S',  metavar='SOLUTION_FILE', required=True, help='The solution file')
args = parser.parse_args(args)

instance_path = args.instance
solution_path = args.solution

# load instance
instance, lbInstance, I, M, p, q, r, o, color, itemid, L, W, H = load_instance(instance_path)

# solve model
model = solve(I, M, p, q, r, o, L, W, H)

# construct solution
construct_solution(solution_path, instance, lbInstance, model, I, color, itemid, L, W, H)

# render solution
SolutionViewer.main()





