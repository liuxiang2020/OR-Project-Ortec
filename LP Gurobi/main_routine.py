from load_instance import load_instance
from load_instance_packed import load_instance_packed
from load_solution import load_solution
from fs_model import solve
from main_routine_hs import solve_packed
from construct_solution_new import construct_solution

from ortec.scientific.benchmarks.loadbuilding import SolutionViewer

import argparse

# read arguments
args = None
parser = argparse.ArgumentParser(description="Visualize loadbuilding solutions")
parser.add_argument('--instance', '-I',  metavar='INPUT_FILE', required=True, help='The instance file')
#parser.add_argument('--sol', '-IS',  metavar='INPUT_SOLUTION_FILE', required=True, help='The input solution file')
parser.add_argument('--solution', '-S',  metavar='SOLUTION_FILE', required=True, help='The solution file')
args = parser.parse_args(args)

instance_path = args.instance
#i_sol_path = args.sol
solution_path = args.solution

# load instance with placed items
instance, lbInstance, I, M, p, q, r, o, color, itemid, L, W, H, placed, given_orientation, positions = load_instance_packed(instance_path)

#load instance
#instance, lbInstance, I, M, p, q, r, o, color, itemid, L, W, H = load_instance(instance_path)

#load solution
#heuristic_solution, lbSol, I_heur, o_heur, pos_heur, color_heur, itemid_heur = load_solution(i_sol_path)

# solve model
model = solve(I, M, p, q, r, o, L, W, H, placed, given_orientation, positions)

#solve model with solution
#model = solve_packed(I, M, p, q, r, o, itemid, L, W, H, I_heur, o_heur, pos_heur, color_heur, itemid_heur)

# construct solution
construct_solution(solution_path, instance, lbInstance, model, I, color, itemid, L, W, H)

# render solution
SolutionViewer.main()
