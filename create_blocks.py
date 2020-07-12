import numpy as np
from Block import Block
from config import *

def Size2Pos(size, orientation='LWH'):
    mask = {'L': 'length', 'W': 'width', 'H': 'height'}
    return np.asarray([size[mask[o]] for o in list(orientation)]).astype(int)


# Creating Simple Blocks from item boxes
def create_simple_blocks(itemkinds,container_size):
    simple_block_list = []
    uid_orientation = {}
    unique_ids = 0
    containerlength = container_size[0]
    containerwidth = container_size[1]
    containerheight = container_size[2]
    for itemkind in range(len(itemkinds)):
        quantity_boxes = itemkinds[itemkind]['quantity']
        for orientation in itemkinds[itemkind]['orientations'].split(','):
            boxsize = Size2Pos(itemkinds[itemkind]['size'], orientation)
            for nx in range(1, quantity_boxes + 1):
                for ny in range(1, quantity_boxes + 1):
                    for nz in range(1, quantity_boxes + 1):
                        block_length = boxsize[0] * nx
                        block_width = boxsize[1] * ny
                        block_height = boxsize[2] * nz
                        if (block_length <= containerlength and block_width <= containerwidth and
                                block_height <= containerheight and nx * ny * nz <= quantity_boxes):
                            block = Block({itemkinds[itemkind]['id']:nx * ny * nz}, True)
                            block.set_size([block_length, block_width, block_height])
                            volume = block_height * block_length * block_width
                            #For simple blocks, the real_volume equals the absolute volume
                            block.set_real_volume(volume)
                            block.set_absolute_volume(volume)
                            block.set_added_direction(0)
                            block.set_dr_quantity((nx, ny, nz))
                            block.set_upper_face((block_length,block_width))
                            #Set block orientation for solution mapping
                            uid_orientation.update({unique_ids:orientation})
                            block.set_unique_id(unique_ids)
                            unique_ids += 1
                            simple_block_list.append(block)
    simple_block_list = filter_redundant_blocks(simple_block_list)                       
    return simple_block_list, unique_ids, uid_orientation


# Creating general blocks from simple blocks
def create_general_blocks(itemkinds, container_size):
    general_blocks_list, unique_ids, uid_orientation = create_simple_blocks(itemkinds, container_size)
    for _ in range(1, 2):
        a = len(general_blocks_list)
        for i in range(0, a):
            block_i = general_blocks_list[i]
            for j in range(i + 1, a):
                block_j = general_blocks_list[j]
                orientation = [0, 1, 2]
                for dr in range(len(orientation)):
                    filling_rate = 0.98
                    gen_block_candidate_size = [0, 0, 0]
                    
                    #Combine block in the direction given by 'dr'
                    gen_block_candidate_size[dr] = block_i.get_size()[orientation[dr]] + block_j.get_size()[orientation[dr]]
                    gen_block_candidate_size[dr - 2] = max(block_i.get_size()[orientation[dr] - 2],
                                               block_j.get_size()[orientation[dr] - 2])
                    gen_block_candidate_size[dr - 1] = max(block_i.get_size()[orientation[dr] - 1],
                                               block_j.get_size()[orientation[dr] - 1])
                    
                    #Only for conversion.py
                    #If the combination is done on the z axis (on block ontop of the other)
                    #then the upper_face is the smaller block
                    if dr == 2:
                        if (block_i.get_size()[orientation[0]] <= block_j.get_size()[orientation[0]] and
                            block_i.get_size()[orientation[1]] <= block_j.get_size()[orientation[1]]):
                            upper_face = (block_i.get_size()[orientation[0]],block_i.get_size()[orientation[1]])
                            triangle = block_i
                            block_i = block_j
                            block_j = triangle
                        elif (block_i.get_size()[orientation[0]] >= block_j.get_size()[orientation[0]] and
                            block_i.get_size()[orientation[1]] >= block_j.get_size()[orientation[1]]):
                            upper_face = (block_j.get_size()[orientation[0]],block_j.get_size()[orientation[1]])
                        else:
                            continue

                    #If the combination is done on the x or y axis, check if they have the same height.
                    #Then calulate the upper_face
                    if dr < 2:
                        if block_i.get_size()[2] != block_j.get_size()[2]:
                            continue
                        if dr == 0:
                            upper_face = (block_i.get_size()[0]+block_j.get_size()[0],min(block_i.get_size()[1],block_j.get_size()[1]))
                        if dr == 1:
                            upper_face = (min(block_i.get_size()[0],block_j.get_size()[0]), block_i.get_size()[1]+block_j.get_size()[1])    
                    
                    
                    #Check if the new block fits in the given container
                    if (gen_block_candidate_size[0] <= container_size[0] and
                            gen_block_candidate_size[1] <= container_size[1] and
                            gen_block_candidate_size[2] <= container_size[2]):
                        new_gb_absolute_volume = gen_block_candidate_size[0] * gen_block_candidate_size[1] * gen_block_candidate_size[2]
                        if ((block_i.get_absolute_volume() + block_j.get_absolute_volume()) / new_gb_absolute_volume) > filling_rate:
                            merged_id_quantities = {x: block_i.get_id_quantity().get(x,0) + block_j.get_id_quantity().get(x,0) for x in set(block_i.get_id_quantity()).union(block_j.get_id_quantity())}
                            
                            new_gb = Block(merged_id_quantities)
                            new_gb.set_absolute_volume(new_gb_absolute_volume)
                            new_gb.set_real_volume(block_i.get_real_volume() + block_j.get_real_volume())
                            
                            new_gb.set_size([gen_block_candidate_size[0], gen_block_candidate_size[1], gen_block_candidate_size[2]])
                            
                            too_many_items = False
                            for ids,quantity in new_gb.get_id_quantity().items():
                                availableItems=itemkinds[ids-1]['quantity']
                                if availableItems < quantity:
                                    too_many_items = True
                                    
                            if not too_many_items:
                                new_gb.set_unique_id(unique_ids)
                                unique_ids += 1
                                new_gb.set_block_uids((block_i.get_unique_id(), block_j.get_unique_id()))
                                new_gb.set_upper_face(upper_face)
                                new_gb.set_added_direction((dr))
                                general_blocks_list.append(new_gb)
        general_blocks_list = filter_redundant_blocks(general_blocks_list)                                              
    return general_blocks_list, uid_orientation

def filter_redundant_blocks(blocklist):
    a = len(blocklist)
    redundant_blocks = []
    for i in range(0, a):
        block_i = blocklist[i]
        for j in range(i + 1, a):
            block_j = blocklist[j]
            if (block_i.get_id_quantity() == block_j.get_id_quantity() and
                block_i.get_size() == block_j.get_size()):
                redundant_blocks.append(j)
    redundant_blocks = list(set(redundant_blocks))
    redundant_blocks = sorted(redundant_blocks)
    x = 0
    for i in redundant_blocks:
      blocklist.pop(i-x)
      x += 1
    return blocklist
