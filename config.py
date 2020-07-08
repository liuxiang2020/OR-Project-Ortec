global K
global M_Zero 
global SCALE 
global STAGE_L 
global MAX_GB
global Parallel
global MAX_SIZE

MAX_GB = 4 # Used in create_blocks.py, sets the number of general block combination iterations
K = 10 # at every stage the k best solutions are used for the next layers treesearch, number of (m,1) trees
M_Zero = 4 # Size of the (m,1) trees, branching factor
SCALE = 3 #...
STAGE_L = 5 #...
MAX_SIZE = 19 # Number of candidate blocks taken as start of the tree search
Parallel = False

#Should be removed from config file
global UID_ORIENTATION
UID_ORIENTATION = {}
