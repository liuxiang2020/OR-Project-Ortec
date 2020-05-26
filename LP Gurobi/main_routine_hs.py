from load_solution import load_solution
from load_instance import load_instance
from heur_start_model import solve
from construct_solution_new import construct_solution
from run import *

from ortec.scientific.benchmarks.loadbuilding import SolutionViewer




import argparse

# read arguments
args = None
parser = argparse.ArgumentParser(description="Visualize loadbuilding solutions")
parser.add_argument('-I',  metavar='INPUT_FILE', required=True, help='The instance file')
parser.add_argument('-S',  metavar='SOLUTION_FILE', required=True, help='The solution file')
parser.add_argument('-J',  metavar='HEURISTIC_FILE', action="store", required=True, help='The heuristic file')
args = parser.parse_args(args)

instance_path = args.I
solution_path = args.S
heuristic_path = args.J

# load instance
instance, lbInstance, I, M, p, q, r, o, color, itemid, L, W, H = load_instance(instance_path)
heuristic_solution, lbSol, I_heur, o_heur, pos_heur, color_heur, itemid_heur = load_solution(heuristic_path)

# solve model
model = solve(I, M, p, q, r, o, itemid, L, W, H, I_heur, o_heur, pos_heur, color_heur, itemid_heur)

# construct solution
construct_solution(solution_path, instance, lbInstance, model, I, color, itemid, L, W, H)

# render solution
SolutionViewer.main()





