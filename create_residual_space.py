from Space import Space
from config import *

def create_residual_space(block, spaceStack):
    # space = spaceStack.top()
    blockSize = block.get_size()
    space = spaceStack.pop()
    w = space.get_size()[0]
    l = space.get_size()[1]
    h = space.get_size()[2]
    
    #return spaceStack without last space for wrong block input
    if blockSize[0] > w or blockSize[1] > l or blockSize[2] > h:
        print("Wrong candidate block list!")
        print(block,spaceStack)
        exit()
        #return spaceStack
        
    cornerx = [0, 0, 0]
    cornery = [0, 0, 0]
    cornerz = [0, 0, 0]
    sizex = [0, 0, 0]
    sizey = [0, 0, 0]
    sizez = [0, 0, 0]
    
    
    deltaw = w - blockSize[0]
    deltal = l - blockSize[1]
    deltah = h - blockSize[2]
    sizez[0] = block.get_upper_face()[0]
    sizez[1] = block.get_upper_face()[1]
    sizez[2] = deltah
    x = space.get_corner()[0]
    y = space.get_corner()[1]
    z = space.get_corner()[2]
    cornerx[2] = z
    cornery[2] = z
    cornerz[2] = z + blockSize[2]
    # Corner Distinction
    corner1 = False
    corner2 = False
    corner3 = False
    # placed at corner nearest to [0,0,0]
    if (x + y <= y + abs(x + w - CONTAINER_SIZE[0]) and
            x + y <= x + abs(y + l - CONTAINER_SIZE[1]) and
            x + y <= abs(x + w - CONTAINER_SIZE[0]) + abs(y + l - CONTAINER_SIZE[1])):
        cornerx[0] = x + blockSize[0]
        cornerx[1] = y
        cornery[0] = x
        cornery[1] = y + blockSize[1]
        cornerz[0] = x
        cornerz[1] = y
    # placed at corner nearest to [X,0,0]
    elif (y + abs(x + w - CONTAINER_SIZE[0]) <= x + abs(y + l - CONTAINER_SIZE[1]) and
          y + abs(x + w - CONTAINER_SIZE[0]) <= abs(x + w - CONTAINER_SIZE[0]) + abs(y + l - CONTAINER_SIZE[1])):
        cornerx[0] = x
        cornerx[1] = y
        corner1 = True
        cornerz[0] = x + deltaw
        cornerz[1] = y
    # placed at corner nearest to [0,Y,0]
    elif x + abs(y + l - CONTAINER_SIZE[1]) <= abs(x + w - CONTAINER_SIZE[0]) + abs(y + l - CONTAINER_SIZE[1]):
        cornery[0] = x
        cornery[1] = y
        corner2 = True
        cornerz[0] = x
        cornerz[1] = y + deltal
    # placed at corner nearest to [X,Y,0]
    else:
        corner3 = True
        cornerz[0] = x + deltaw
        cornerz[1] = y + deltal
        # resX > resY?
        
        
        
        
    if deltaw * l >= w * deltal:
        sizex[0] = deltaw
        sizex[1] = l
        sizex[2] = h
        sizey[0] = w - deltaw
        sizey[1] = deltal
        sizey[2] = h
        if corner1:
            cornery[0] = x + deltaw
            cornery[1] = y + blockSize[1]
        elif corner2:
            cornerx[0] = x + blockSize[0]
            cornerx[1] = y
        elif corner3:
            cornerx[0] = x
            cornerx[1] = y
            cornery[0] = x + deltaw
            cornery[1] = y
        spaceStack.append(Space(cornerz, sizez, 'z',calc_corner_for_placement(cornerz,sizez)))
        spaceStack.append(Space(cornery, sizey, 'y',calc_corner_for_placement(cornery,sizey)))
        spaceStack.append(Space(cornerx, sizex, 'x',calc_corner_for_placement(cornerx,sizex)))
    else:
        sizex[0] = deltaw
        sizex[1] = l - deltal
        sizex[2] = h
        sizey[0] = w
        sizey[1] = deltal
        sizey[2] = h
        if corner1:
            cornery[0] = x
            cornery[1] = y + blockSize[1]
        elif corner2:
            cornerx[0] = x + blockSize[0]
            cornerx[1] = y + deltal
        elif corner3:
            cornerx[0] = x
            cornerx[1] = y + deltal
            cornery[0] = x
            cornery[1] = y
        spaceStack.append(Space(cornerz, sizez, 'z',calc_corner_for_placement(cornerz,sizez)))
        spaceStack.append(Space(cornerx, sizex, 'x',calc_corner_for_placement(cornerx,sizex)))
        spaceStack.append(Space(cornery, sizey, 'y',calc_corner_for_placement(cornery,sizey)))
    return spaceStack

def calc_corner_for_placement(corner,size):
    x = corner[0]
    y = corner[1]
    w = size[0]
    l = size[1]
    res_corner = [0,0,0]
    if (x + y <= y + abs(x + w - CONTAINER_SIZE[0]) and
            x + y <= x + abs(y + l - CONTAINER_SIZE[1]) and
            x + y <= abs(x + w - CONTAINER_SIZE[0]) + abs(y + l - CONTAINER_SIZE[1])):
        res_corner = corner
    elif (y + abs(x + w - CONTAINER_SIZE[0]) <= x + abs(y + l - CONTAINER_SIZE[1]) and
          y + abs(x + w - CONTAINER_SIZE[0]) <= abs(x + w - CONTAINER_SIZE[0]) + abs(y + l - CONTAINER_SIZE[1])):
        res_corner[0] = corner[0]
        res_corner[1] = corner[1] + w
        res_corner[2] = corner[2]
    elif x + abs(y + l - CONTAINER_SIZE[1]) <= abs(x + w - CONTAINER_SIZE[0]) + abs(y + l - CONTAINER_SIZE[1]):
        res_corner[0] = corner[0]
        res_corner[1] = corner[1]
        res_corner[2] = corner[2] + l
    else:
        res_corner[0] = corner[0]
        res_corner[1] = corner[1] + w
        res_corner[2] = corner[2] + l
    return res_corner
    
    