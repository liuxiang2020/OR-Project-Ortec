global K
global M_Zero 
global SCALE 
global STAGE_L
global Parallel
global MAX_SIZE

K = 9 #At every stage the k best solutions are used for the next layers treesearch, number of (m,1) trees
M_Zero = 1 #Size of the (m,1) trees, branching factor
SCALE = 3 #Multiplier for m
STAGE_L = 6 #Depth of the Tree
MAX_SIZE = 20 #Number of candidate blocks taken as start of the tree search
Parallel = False #Switches parallel execution (multi-threading) on/off
