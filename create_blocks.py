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
            for nx  in range(1, quantity_boxes):
                for ny in range(1, quantity_boxes):
                    for nz in range(1, quantity_boxes):
                        block_length = boxsize[0]*nx
                        block_width = boxsize[1]*ny
                        block_height = boxsize[2]*nz
                        if (block_length < containerlength and block_width < containerwidth and 
                            block_height < containerheight and nx*ny*nz <= quantity_boxes):
                            block_item_id = [itemkinds[itemkind]['id']]
                            block_item_quantity = [nx*ny*nz]
                            block_size = [block_length, block_width, block_height]
                            block_orientation = [orientation]
                            block_volume = block_length*block_width*block_height
                            volume_loss = 0
                            
                            simple_block_list.append([block_item_id, block_item_quantity, block_size, block_orientation, block_volume, volume_loss])       
    return simple_block_list

#Creating general blocks from simple blocks
def create_general_blocks(itemkinds, containerSize):
    general_blocks_list =create_simple_blocks(itemkinds, containerSize)
    for Creation_Iterations in range (1, 2):
        a = len(general_blocks_list)
        for i in range(0, a):
            block_i = general_blocks_list[i]
            for j in range (i+1, a):
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
                        gen_block_volume = g_block_size[0]*g_block_size[1]*g_block_size[2]
                        if ((block_i[4] + block_j[4])/gen_block_volume)>filling_rate:
                            if block_i[0]==block_j[0] and block_i[3] == block_j[3]:
                                gen_block_item_id = block_i[0]
                                gen_block_item_quantity = []
                                block_orientations = block_i[3]
                                for i in range(0, len(block_i[1])): 
                                    gen_block_item_quantity.append(block_i[1][i] + block_j[1][i]) 

                            else:
                                gen_block_item_id = block_i[0] + block_j[0]
                                gen_block_item_quantity = block_i[1] + block_j[1]
                                block_orientations = block_i[3] + block_j[3]
                            
                            block_volume_loss = gen_block_volume - (block_i[4] + block_j[4])
                            general_blocks_list.append([gen_block_item_id, gen_block_item_quantity, g_block_size, block_orientations, gen_block_volume, block_volume_loss])
    return general_blocks_list
