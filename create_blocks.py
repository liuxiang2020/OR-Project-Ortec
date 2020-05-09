import numpy as np
from Block import Block


def Size2Pos(size, orientation='LWH'):
    mask = {'L': 'length', 'W': 'width', 'H': 'height'}
    return np.asarray([size[mask[o]] for o in list(orientation)]).astype(int)


# Creating Simple Blocks from item boxes
def create_simple_blocks(itemkinds, containerSize):
    simple_block_list = []
    containerlength = containerSize[0]
    containerwidth = containerSize[1]
    containerheight = containerSize[2]
    for itemkind in range(len(itemkinds)):
        quantity_boxes = itemkinds[itemkind]['quantity']
        for orientation in itemkinds[itemkind]['orientations'].split(','):
            boxsize = Size2Pos(itemkinds[itemkind]['size'], orientation)
            for nx in range(1, quantity_boxes):
                for ny in range(1, quantity_boxes):
                    for nz in range(1, quantity_boxes):
                        block_length = boxsize[0] * nx
                        block_width = boxsize[1] * ny
                        block_height = boxsize[2] * nz
                        if (block_length < containerlength and block_width < containerwidth and
                                block_height < containerheight and nx * ny * nz <= quantity_boxes):
                            block = Block(itemkinds[itemkind]['id'])
                            block.set_item_quantity(nx * ny * nz)
                            block.set_size([block_length, block_width, block_height])
                            block.set_orientation([orientation])
                            volume = block_height * block_length * block_width
                            block.set_volume(volume)
                            block.set_volume_loss(0)
                            simple_block_list.append(block)
    return simple_block_list


# Creating general blocks from simple blocks
def create_general_blocks(itemkinds, containerSize):
    general_blocks_list = create_simple_blocks(itemkinds, containerSize)
    for _ in range(1, 2):
        a = len(general_blocks_list)
        for i in range(0, a):
            block_i = general_blocks_list[i]
            for j in range(i + 1, a):
                block_j = general_blocks_list[j]
                orientation = [0, 1, 2]
                for dr in range(len(orientation)):
                    filling_rate = 0.98
                    g_block_size = [0, 0, 0]
                    g_block_size[dr] = block_i.get_size()[orientation[dr]] + block_j.get_size()[orientation[dr]]
                    g_block_size[dr - 2] = max(block_i.get_size()[orientation[dr] - 2],
                                               block_j.get_size()[orientation[dr] - 2])
                    g_block_size[dr - 1] = max(block_i.get_size()[orientation[dr] - 1],
                                               block_j.get_size()[orientation[dr] - 1])
                    if dr < 2:
                        if block_i.get_size()[2] != block_j.get_size()[2]:
                            continue
                    if (g_block_size[0] < containerSize[0] and
                            g_block_size[1] < containerSize[1] and
                            g_block_size[2] < containerSize[2]):
                        gen_block_volume = g_block_size[0] * g_block_size[1] * g_block_size[2]
                        if ((block_i.get_volume() + block_j.get_volume()) / gen_block_volume) > filling_rate:
                            if (block_i.get_id() == block_j.get_id() and
                                    block_i.get_orientation() == block_j.get_orientation()):
                                gen_block = Block(block_i.get_id())
                                # TODO: add set_volume
                                gen_block.set_volume(gen_block_volume)
                                gen_block.set_item_quantity(0)
                                gen_block.set_orientation(block_i.get_orientation())
                                gen_block_item_quantity = []
                                for i in range(0, len(block_i.get_orientation())):
                                    gen_block_item_quantity.append(
                                        # TODO set quantity?
                                        block_i.get_orientation()[i] + block_j.get_orientation()[i])
                                gen_block.set_item_quantity(gen_block_item_quantity)
                            else:
                                gen_block = Block(block_i.get_id() + block_j.get_id())
                                # TODO: add set_volume
                                gen_block.set_volume(gen_block_volume)
                                gen_block_item_quantity = block_i.get_item_quantity() + block_j.get_item_quantity()
                                block_orientations = block_i.get_orientation() + block_j.get_orientation()
                                gen_block.set_orientation(block_orientations)

                            block_volume_loss = gen_block_volume - (block_i.get_volume() + block_j.get_volume())
                            gen_block.set_volume_loss(block_volume_loss)
                            general_blocks_list.append(gen_block)
    return general_blocks_list
