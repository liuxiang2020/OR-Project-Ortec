from Space import Space

def create_residual_space(blockSize, containerSize, spaceStack):
    #space = spaceStack.top()
    space = spaceStack.pop()
    cornerx=[0,0,0]
    cornery=[0,0,0]
    cornerz=[0,0,0]
    sizex=[0,0,0]
    sizey=[0,0,0]
    sizez=[0,0,0]
    w=space.get_size()[0]
    l=space.get_size()[1]
    h=space.get_size()[2]
    deltaw = w-blockSize[0]
    deltal = l-blockSize[1]
    deltah = h-blockSize[2]
    sizez[0] = blockSize[0]
    sizez[1] = blockSize[1]
    sizez[2] = deltah
    x = space.get_corner()[0]
    y = space.get_corner()[1]
    z = space.get_corner()[2]
    cornerx[2]=z
    cornery[2]=z
    cornerz[2]=z+blockSize[2] 
    #Corner Distinction
    corner1=False
    corner2=False
    corner3=False
    #placed at corner nearest to [0,0,0]
    if (x+y <= y+abs(x+w-containerSize[0]) and
        x+y <= x+abs(y+l-containerSize[1]) and
        x+y <= abs(x+w-containerSize[0])+abs(y+l-containerSize[1])):
        cornerx[0] = x + blockSize[0]
        cornerx[1] = y
        cornery[0] = x
        cornery[1] = y + blockSize[1]
        cornerz[0] = x
        cornerz[1] = y
    #placed at corner nearest to [X,0,0]
    elif (y+abs(x+w-containerSize[0]) <= x+abs(y+l-containerSize[1]) and
          y+abs(x+w-containerSize[0]) <= abs(x+w-containerSize[0])+abs(y+l-containerSize[1])):
        cornerx[0] = x
        cornerx[1] = y
        corner1=True
        cornerz[0] = x + deltaw
        cornerz[1] = y
    #placed at corner nearest to [0,Y,0]
    elif x+abs(y+l-containerSize[1]) <= abs(x+w-containerSize[0])+abs(y+l-containerSize[1]):
        cornery[0] = x
        cornery[1] = y
        corner2=True
        cornerz[0] = x
        cornerz[1] = y + deltal
    #placed at corner nearest to [X,Y,0]
    else:
        corner3=True
        cornerz[0] = x + deltaw
        cornerz[1] = y + deltal 
    # resX > resY?   
    if deltaw * l >= w*deltal:
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
        spaceStack.append(Space(cornerz,sizez,'z'))
        spaceStack.append(Space(cornery,sizey,'y'))
        spaceStack.append(Space(cornerx,sizex,'x'))
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
        spaceStack.append(Space(cornerz,sizez,'z'))
        spaceStack.append(Space(cornerx,sizex,'x'))
        spaceStack.append(Space(cornery,sizey,'y'))
    return spaceStack
    