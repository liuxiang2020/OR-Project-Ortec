from Space import Space
def transfer_residual_space(spaceStack):
    kindcheck = False
    adjacentx = False
    adjacenty = False
    curSpace = spaceStack.pop()
    #can't do space transfer for z spaces
    if curSpace.get_kind() == 'z':
        return spaceStack
    nextSpace = spaceStack.pop()
    #no transfer between two spaces of the same kind or with a z space
    kindcheck = curSpace.get_kind() == nextSpace.get_kind() or nextSpace.get_kind() == 'z' 
    #adjacency checks
    adjacentx = nextSpace.get_corner()[0] + nextSpace.get_size()[0] == curSpace.get_corner()[0] or curSpace.get_corner()[0] + curSpace.get_size()[0] == nextSpace.get_corner()[0]
    adjacenty = nextSpace.get_corner()[1] + nextSpace.get_size()[1] == curSpace.get_corner()[1] or curSpace.get_corner()[1] + curSpace.get_size()[1] == nextSpace.get_corner()[1]
    if kindcheck or (not(adjacentx) and curSpace.get_kind() == 'x') or (not(adjacenty) and curSpace.get_kind() == 'y'):
        spaceStack.append(nextSpace)
        return spaceStack
    newcorner = [0,0,0]
    newsize = [0,0,0]
    #check for corner configuration
    if(curSpace.get_kind()=='x'):
        newsize = nextSpace.get_size()
        newsize[0] += curSpace.get_size()[0]
        if curSpace.get_corner()[1] < nextSpace.get_corner()[1]:
            if curSpace.get_corner()[0] < nextSpace.get_corner()[0]:
                #case1: block was at corner [X,0,0]
                newcorner = nextSpace.get_corner()
                newcorner[1] = curSpace.get_corner()[1]
            elif curSpace.get_corner()[0] > nextSpace.get_corner()[0]:
                #case2: block was at corner [0,0,0]
                newcorner = nextSpace.get_corner()
        elif curSpace.get_corner()[1]==nextSpace.get_corner()[1]:
            if curSpace.get_corner()[0] < nextSpace.get_corner()[0]:
                #case3: block was at corner [X,Y,0]
                newcorner = curSpace.get_corner()
            elif curSpace.get_corner()[0] > nextSpace.get_corner()[0]:
                #case4: block was at corner [0,Y,0]
                newcorner = nextSpace.get_corner()
    if(curSpace.get_kind()=='y'):
        newsize = nextSpace.get_size()
        newsize[1] += curSpace.get_size()[1]
        if curSpace.get_corner()[0] < nextSpace.get_corner()[0]:
            if curSpace.get_corner()[1] < nextSpace.get_corner()[1]:
                #case1: block was at corner [0,Y,0]
                newcorner = nextSpace.get_corner()
                newcorner[0] = curSpace.get_corner()[0]
            elif curSpace.get_corner()[1] > nextSpace.get_corner()[1]:
                #case2: block was at corner [0,0,0]
                newcorner = nextSpace.get_corner()
        elif curSpace.get_corner()[0]==nextSpace.get_corner()[0]:
            if curSpace.get_corner()[1] < nextSpace.get_corner()[1]:
                #case3: block was at corner [X,Y,0]
                newcorner = curSpace.get_corner()
            elif curSpace.get_corner()[1] > nextSpace.get_corner()[1]:
                #case4: block was at corner [X,0,0]
                newcorner = nextSpace.get_corner()

    spaceStack.append(Space(newcorner,newsize,nextSpace.get_kind()))
    return spaceStack
