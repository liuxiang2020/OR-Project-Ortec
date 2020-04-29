from Functions import *

#Creating Simple Blocks from item boxes
def create_simple_blocks(itemkinds, containerSize):
    simple_block_list = []
    containerlength = containerSize[0]
    containerwidth = containerSize[1]
    containerheight = containerSize[2]
    for itemkind in range(len(itemkinds)):
        quantity_boxes = itemkinds[itemkind]['quantity']
        for orientation in itemkinds[itemkind]['orientations'].split(','):
            boxsize = Size2Pos(itemkinds[itemkind]['size'], orientation) 
            for nx  in range(1, quantity_boxes+1):
                for ny in range(1, quantity_boxes+1):
                    for nz in range(1, quantity_boxes+1):
                        block_length = boxsize[0]*nx
                        block_width = boxsize[1]*ny
                        block_height = boxsize[2]*nz
                        if (block_length < containerlength and block_width < containerwidth and 
                            block_height < containerheight and nx*ny*nz <= quantity_boxes):
                            block_item_id = [itemkinds[itemkind]['id']]
                            block_item_quantity = [nx*ny*nz]
                            block_size = [block_length, block_width, block_height]
                            simple_block_list.append([block_item_id, block_item_quantity, block_size])       
    return simple_block_list

#Creating general blocks from simple blocks
def create_general_blocks(itemkinds, containerSize):
    general_blocks_list =create_simple_blocks(itemkinds, containerSize)
    for Creation_Iterations in range (1, 2):
        for i in range(1, len(general_blocks_list)+1):
            block_i = general_blocks_list[i]
            for j in range (1+1, len(general_blocks_list)+1):
                block_j = general_blocks_list[j]
                orientation = [0,1,2]
                for dr in range(len(orientation)):
                    filling_rate = 0.98
                    g_block_size = [0,0,0]
                    g_block_size[dr] = block_i[2][orientation[dr]] + block_j[2][orientation[dr]]
                    g_block_size[dr-2] = max(block_i[2][orientation[dr]-2], block_j[2][orientation[dr]-2])
                    g_block_size[dr-1] = max(block_i[2][orientation[dr]-1], block_j[2][orientation[dr]-1])
                    if dr < 2:
                        if block_i[2][2] != block_j[2][2]:
                            continue     
                    if (g_block_size[0]<containerSize[0] and 
                        g_block_size[1]<containerSize[1] and 
                        g_block_size[2]<containerSize[2]):
                        if (block_i[2][0]*block_i[2][1]*block_i[2][2] + 
                            block_j[2][0]*block_j[2][1]*block_j[2][2]/
                            (g_block_size[0]*g_block_size[1]*g_block_size[2]))>filling_rate:
                            gen_block_item_id = block_i[0] + block_j[0]
                            gen_block_item_quantity = block_i[1] + block_j[1]
                            general_blocks_list.append([gen_block_item_id, gen_block_item_quantity, g_block_size])
                print(general_blocks_list)           
    return general_blocks_list
