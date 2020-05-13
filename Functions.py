import numpy as np

def String2Pos( string ):
    return np.asarray([int(p) for p in string.split(',')]).astype(int)

def Pos2String( pos ):
    return ','.join([str(p) for p in pos])

def Size2Pos( size, orientation='LWH' ):
    mask = { 'L': 'length', 'W': 'width', 'H': 'height' }
    return np.asarray( [ size[mask[o]] for o in list(orientation) ] ).astype(int)

def MakePlacement(pos,id,itemid,orientation,color=None):
    placement = { 'id': id, 'position': Pos2String(pos), 'itemid': itemid, 'orientation': orientation }
    if not color is None:
        placement['color'] = color
    return placement

def qsort_candidate_fitness(arr):
    less_than = lambda x, y: x[6] < y[6]
    more_than = lambda x, y: x[6] >= y[6]
    if len(arr) <= 1:
        return arr
    else:
        return qsort_candidate_fitness([x for x in arr[1:] if less_than(x, arr[0])]) + [arr[0]] + qsort_candidate_fitness([x for x in arr[1:] if more_than(x, arr[0])])

"""
available_boxes: dictionary key:value <-> id:quantity
added_block: block
"""

def update_available_boxes(available_boxes, added_block):
    boxes = available_boxes
    block = added_block
    box_id = block.get_id()
    box_quantity = block.get_item_quantity()
    for i in range(len(box_id)):
        boxes[box_id[i]]  = boxes[box_id[i]] - box_quantity[i]
    return boxes


