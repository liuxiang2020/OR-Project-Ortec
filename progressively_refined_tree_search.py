from create_residual_space import create_residual_space
from generate_candidate_blocklist_2 import generate_candidate_block_list
from build_m1_tree import build_m1_tree
from Functions import update_available_boxes
from time import sleep
import math

K = 3
M_Zero = 3
SCALE = 3
STAGE_L = 5

def calc_L(k,m):
    m_root =  int(math.sqrt(m))
    #why 6*7+1
    numerator = ((6*7 + 1) * (m + m_root*m_root - m_root)) - m
    denominator = k*m
    return numerator/denominator



#search best solution for Block block and State state
def Progressively_Refined_Tree_Search(block, state, block_list, containerSize):
    space = state.get_residualSpaceList()[-1] # get last item in list
    #put block into the space and update residualSpaceList
    state.add_block_planListBlock(block)
    state.add_space_planListSpace(space)
    available_boxes = update_available_boxes(state.get_available_items(), block)
    state.set_available_items(available_boxes)
    state.set_utilization(0.2) #TODO
    _ = create_residual_space(block, containerSize, state.get_residualSpaceList())

    # Generate Blocklist for new spaces?
    cBlocKList = generate_candidate_block_list(space.get_size(), block_list, state.get_available_items())

    #current best solution is putting just one block in the empty size
    best_solution = state 

    print('Current BestSL')
    print(best_solution)
    
    m = 1
    for _ in range(STAGE_L-1):
        bkTab = [] # packing strategy # maybe need a own datatype..
        m = m*SCALE
        #what is L?
        L = int(calc_L(K,m))
        print(L)
        bkTab.append(build_m1_tree(block, state, m, K, 0, block_list, containerSize))
        for j in range(1, L):
            if(len(bkTab[j-1])-1 > 0):
                for d in len(bkTab[j-1])-1:
                    nState = bkTab[j-1][d][0]
                    nBlock = bkTab[j-1][d][1]
                    bkTab.append(build_m1_tree(nBlock, nState, m, K, j, block_list, containerSize))
        for j in range(1,L):
            if bkTab[j][0][0].get_utilization() > best_solution.get_utilization():
                best_solution = bkTab[j][0][0]
    """
    # test return
    res_space = [Space([0, 0, 0], [1, 1, 1], 'x')]
    occupied_space = [Space([0, 0, 0], [100, 50, 100], 'x')]
    filled_block = [Block(2)]
    filled_block[0].set_size([100, 50, 100])
    filled_block[0].set_item_quantity(4)
    filled_block[0].set_volume(500000)
    filled_block[0].set_orientation(['LHW'])
    filled_block[0].set_volume_loss(1)
    s = State(res_space, occupied_space, filled_block)
    s.set_utilization(0.98)
    return s
    """
    """
    #TODO
    m = 1
    #TODO
    for i in range(STAGE_L-1):
        bkTab = []
        m = m*SCALE
        L = calc_L(K,m)
        bkTab.append(Build_m1_Tree(block, state, m, K, 0))
        for j in range(1, L):
            for d in bkTab[j-1].size()-1:
                nState = bkTab[j-1][d].state
                nBlock = bkTab[j-1][d].block
                bkTab.append(Build_m1_Tree(nBlock, nState, m, K, j))
        for j in range(1,L):
            if bkTab[j][0].state.get_utilization() > best_solution.get_utilization():
                best_solution = bkTab[j][0]
    """
    return best_solution