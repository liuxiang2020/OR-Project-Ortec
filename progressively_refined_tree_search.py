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
    numerator = ((6*7 + 1) * (m + m_root*m_root - m_root)) - m
    denominator = k*m
    return numerator/denominator


def Progressively_Refined_Tree_Search(block, state, block_list, available_boxes, containerSize):
    space = state.get_residualSpaceList().pop()
    state.add_space_residualSpaceList(space)
    state.add_block_occupiedSpaceList(block)
    available_boxes = update_available_boxes(available_boxes, block)
    spacestack = create_residual_space(block.get_size(), containerSize, state.get_residualSpaceList())
    cBlocKList = generate_candidate_block_list(space.get_size(), block_list, available_boxes)
    best_solution = state
    m = 1
    for i in range(STAGE_L-1):
        bkTab = []
        m = m*SCALE
        L = calc_L(K,m)
        bkTab.append(build_m1_tree(cBlocKList, state, m, K, 0, block_list, available_boxes, containerSize, cBlocKList, bkTab))
        for j in range(1, L):
            for d in bkTab[j-1].size()-1:
                nState = bkTab[j-1][d].state
                nBlock = bkTab[j-1][d].block
                bkTab.append(build_m1_tree(nBlock, nState, m, K, j, block_list, available_boxes, containerSize, cBlocKList, bkTab))
        for j in range(1,L):
            if bkTab[j][0].state.get_utilization() > best_solution.get_utilization():
                best_solution = bkTab[j][0]
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