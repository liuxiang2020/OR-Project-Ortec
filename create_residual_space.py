#space: at pos (0,1,0), size (55,34,34)
#spaceStack[[0,1,0][55,34,34]]

def create_residual_space(blockSize, containerSize, spaceStack):
    #space = spaceStack.top()
    space = spaceStack.pop()
    resX =[[0,0,0],[0,0,0]]
    resY =[[0,0,0],[0,0,0]]
    resZ =[[0,0,0],[0,0,0]]
    w=space[1][0]
    l=space[1][1]
    h=space[1][2]
    deltaw = w-blockSize[0]
    deltal = l-blockSize[1]
    deltah = h-blockSize[2]
    resZ[1][0] = blockSize[0]
    resZ[1][1] = blockSize[1]
    resZ[1][2] = deltah
    x = space[0][0]
    y = space[0][1]
    z = space[0][2]
    resX[0][2]=z
    resY[0][2]=z
    resZ[0][2]=z+blockSize[2] 
    #Corner Distinction
    corner1=False
    corner2=False
    corner3=False
    #placed at corner nearest to [0,0,0]
    if (x+y <= y+abs(x+w-containerSize[0]) and
        x+y <= x+abs(y+l-containerSize[1]) and
        x+y <= abs(x+w-containerSize[0])+abs(y+l-containerSize[1])):
        resX[0][0] = x + blockSize[0]
        resX[0][1] = y
        resY[0][0] = x
        resY[0][1] = y + blockSize[1]
        resZ[0][0] = x
        resZ[0][1] = y
    #placed at corner nearest to [X,0,0]
    elif (y+abs(x+w-containerSize[0]) <= x+abs(y+l-containerSize[1]) and
          y+abs(x+w-containerSize[0]) <= abs(x+w-containerSize[0])+abs(y+l-containerSize[1])):
        resX[0][0] = x
        resX[0][1] = y
        corner1=True
        resZ[0][0] = x + deltaw
        resZ[0][1] = y
    #placed at corner nearest to [0,Y,0]
    elif x+abs(y+l-containerSize[1]) <= abs(x+w-containerSize[0])+abs(y+l-containerSize[1]):
        resY[0][0] = x
        resY[0][1] = y
        corner2=True
        resZ[0][0] = x
        resZ[0][1] = y + deltal
    #placed at corner nearest to [X,Y,0]
    else:
        corner3=True
        resZ[0][0] = x + deltaw
        resZ[0][1] = y + deltal 
    # resX > resY?   
    if deltaw * l >= w*deltal:
        resX[1][0] = deltaw
        resX[1][1] = l
        resX[1][2] = h
        resY[1][0] = w - deltaw
        resY[1][1] = deltal
        resY[1][2] = h
        if corner1:
            resY[0][0] = x + deltaw
            resY[0][1] = y + blockSize[1]
        elif corner2:
            resX[0][0] = x + blockSize[0]
            resX[0][1] = y 
        elif corner3:
            resX[0][0] = x
            resX[0][1] = y 
            resY[0][0] = x + deltaw
            resY[0][1] = y 
        spaceStack.append(resZ)
        spaceStack.append(resY)
        spaceStack.append(resX)
    else:
        resX[1][0] = deltaw
        resX[1][1] = l - deltal
        resX[1][2] = h
        resY[1][0] = w
        resY[1][1] = deltal
        resY[1][2] = h
        if corner1:
            resY[0][0] = x
            resY[0][1] = y + blockSize[1]
        elif corner2:
            resX[0][0] = x + blockSize[0]
            resX[0][1] = y + deltal
        elif corner3:
            resX[0][0] = x
            resX[0][1] = y + deltal
            resY[0][0] = x
            resY[0][1] = y
        spaceStack.append(resZ)
        spaceStack.append(resX)
        spaceStack.append(resY)
    return spaceStack
    