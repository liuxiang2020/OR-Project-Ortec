def SkeletonSolution():
    skeleton = """description:
  set: Bischoff & Ratcliff
  name: '1.1'
layout:
  containers:
  - id: 1
    kindid: 1
    loadingspaces:
    - id: 1
      placements:
  unplaced:
  - id: 1
    itemid: 1
    quantity: 0"""
    import yaml
    return yaml.load( skeleton, Loader=yaml.FullLoader )

def search_for_uid (block_dict,uid):
    for i in range(len(block_dict)):
        if block_dict[i].get_unique_id() == uid:
            return block_dict[i]

def break_down_block(cur_block,simple_list,block_dict,cor,pla):
    if cor == pla:
        pos = (cor[0],cor[1],cor[2])
    elif cor[0] < pla[0] and cor[1] == pla[1]:
        pos = (pla[0]-cur_block.get_size()[0],cor[1],cor[2])
    elif cor[0] == pla[0] and cor[1] < pla[1]:
        pos = (cor[0],pla[1]-cur_block.get_size()[1],cor[2])
    elif cor[0] < pla[0] and cor[1] < pla[1]:
        pos = (pla[0]-cur_block.get_size()[0],pla[1]-cur_block.get_size()[1],cor[2])
    if cur_block.get_is_simple():
        simple_list.append((cur_block.get_unique_id(),pos))
        return simple_list
    else:
        (i,j) = cur_block.get_block_uids()
        block_i = search_for_uid(block_dict,i)
        block_j = search_for_uid(block_dict,j)
        dr = cur_block.get_added_direction
        simple_list = break_down_block(block_i,simple_list,block_dict,pos,pos)
        if dr == 0:
            posj = (pos[0]+block_i.get_size()[0],pos[1],pos[2])
        elif dr == 1:
            posj = (pos[0],pos[1]+block_i.get_size()[1],pos[2])
        elif dr == 2:
            posj = (pos[0],pos[1],pos[2]+block_i.get_size()[2])
        simple_list = break_down_block(block_j,simple_list,block_dict,posj,posj)
        return simple_list
# return[(uid,[0,0,0]),...]
def convert_state_to_solution(instancename,state,block_dict):
    unplaced_items =  state.get_available_items()
    blocks = state.get_planListBlock()
    spaces = state.get_planListSpace()
    solution = SkeletonSolution()
    with open(instancename) as f:
        import yaml
        instance = yaml.load( f, Loader=yaml.FullLoader )
    solution['description'] = instance['description']
    simple_list = []
    for i in range(len(blocks)):
        cur_block = blocks[i]
        cur_space = spaces[i]  
        if not cur_block.get_is_simple_block():
            cor = cur_space.get_corner()
            pla = cur_space.get_block_corner()
            simple_list = break_down_block(cur_block,simple_list,cor,pla)
    for si in simple_list:
            simple_block_id = si[0]
            position = si[1]
            simple_block = search_for_uid(block_dict,simple_block_id)
            dr_quantity = simple_block.get_dr_quantity()
            orientation = simple_block.get_orientation()
            item_id = simple_block.get_id()
            boxsize = Size2Pos(itemKinds[item_id-1]['size'], orientation)

            for nx in range(1,dr_quantity[0]):
                if nx > 1:
                    position[0]+=boxsize[0]
                for ny in range(1,dr_quantity[1]):
                    if ny > 1:
                        position[1]+=boxsize[1]
                    for nz in range(1,dr_quantity[2]):
                        placement = MakePlacement(position,id,itemKinds[item_id-1]['id'],orientation)
                        id += 1
                        position[2]+=boxsize[2] 
                        placements = placements + [placement]


    #unplaced blocks
    unplaced = solution['layout']['unplaced']
    import copy
    unplaced = [ copy.deepcopy(unplaced[0]) for i in range(len(itemKinds)) ]
    id = 0
    for itemKind in range(len(itemKinds)):
        unplaced[itemKind]['id'] = id
        unplaced[itemKind]['itemid'] = itemKinds[itemKind]['id']
        unplaced[itemKind]['quantity'] = unplaced_items[itemKind]
        id += 1

    solution['layout']['containers'][0]['loadingspaces'][0]['placements'] = placements
    solution['layout']['unplaced'] = unplaced

    if create_yaml == 1:
        import yaml
            with open('store_file.yaml', 'w') as file:
        documents = yaml.dump(solution, file)

    return