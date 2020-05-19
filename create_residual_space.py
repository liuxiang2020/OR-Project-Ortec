from Space import Space
from config import *

def create_residual_space(block, spaceStack):
    blockSize = block.get_size()
    space = spaceStack.pop()
    
    l = space.get_size()[0]
    w = space.get_size()[1]
    h = space.get_size()[2]
    
    #return spaceStack without last space for wrong block input
    if blockSize[0] > l or blockSize[1] > w or blockSize[2] > h:
        print("Wrong candidate block list!")
        print(block,spaceStack)
        exit()
        
    deltal = l - blockSize[0]
    deltaw = w - blockSize[1]
    deltah = h - blockSize[2]
    
    # Space Z is always the same
    # ! ! ! ! ! For the full suppport constraint, this space should only consist of the minimum 
    spaceZ = [block.get_upper_face()[0], block.get_upper_face()[1], deltah]
    
    #The corner generation should be independent of the space splitting
    corner_of_spaceZ = [space.get_corner()[0], space.get_corner()[1], space.get_corner()[2] + blockSize[2]]
    corner_of_spaceY = [space.get_corner()[0] + blockSize[0], space.get_corner()[1], space.get_corner()[2]]
    corner_of_spaceX = [space.get_corner()[0], space.get_corner()[1] + blockSize[1], space.get_corner()[2]]
    
    # Space X and Y based on Figure 3
    if (deltaw*l >= w*deltal):
        spaceX = [l, deltaw, h]
        spaceY = [deltal, w-deltaw, h]
        spaceStack.append(Space(corner_of_spaceZ, spaceZ, 'z',corner_of_spaceZ))
        spaceStack.append(Space(corner_of_spaceY, spaceY, 'y',corner_of_spaceY))
        spaceStack.append(Space(corner_of_spaceX, spaceX, 'x',corner_of_spaceX))
    else:
        spaceX = [l-deltal, deltaw, h]
        spaceY = [deltal, w, h]
        spaceStack.append(Space(corner_of_spaceZ, spaceZ, 'z',corner_of_spaceZ))
        spaceStack.append(Space(corner_of_spaceX, spaceX, 'x',corner_of_spaceX))
        spaceStack.append(Space(corner_of_spaceY, spaceY, 'y',corner_of_spaceY))
    
    return spaceStack