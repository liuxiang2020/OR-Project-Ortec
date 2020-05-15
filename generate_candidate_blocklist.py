import config
def check_availability(gb, item_available):
    for ids,quantity in gb.get_id_quantity().items():
        if item_available[ids] < quantity:
            return False
    return True

def generate_candidate_block_list(currentSpace, generalBlockList, item_available):
    candidateBlockList = []
    # currSpace = [L,W,H]
    currSpace = currentSpace
    print("curr",currSpace)

    '''DEBUG
    print("start")
    for i in range(len(generalBlockList)):
        print(generalBlockList[i].get_id(), generalBlockList[i].get_item_quantity(),
              generalBlockList[i].get_fitness())
    print("end")

    '''
    for gb in generalBlockList:
        # Check block size and space size
        if (gb.get_size()[0] <= currSpace[0]) and (gb.get_size()[1] <= currSpace[1]) and (
                gb.get_size()[2] <= currSpace[2]):
            # Check fitness
            spaceVolume = currSpace[0] * currSpace[1] * currSpace[2]
            gbVolume = gb.get_volume()
            if check_availability(gb, item_available):
                # TODO : check which fitness measure way is best
                fitness = 2*gbVolume- spaceVolume - gb.get_volume_loss()
                gb.set_fitness(fitness)
                candidateBlockList.append(gb)

    candidateBlockList.sort(key=lambda x: x.get_fitness(), reverse=True)
    if candidateBlockList!=[]:
        print(candidateBlockList[0])
    '''DEBUG
    for i in range(len(candidateBlockList)):
    print(candidateBlockList[i].get_id(),candidateBlockList[i].get_item_quantity(),candidateBlockList[i].get_fitness(),candidateBlockList[i].get_orientation())
    '''
    return candidateBlockList