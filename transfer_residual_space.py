#spaceStack = [[[0,10,0],[10,15,30]], [[10,0,0], [50,25,30]]]

def create_residual_space(spaceStack):
    curSpace = spaceStack.pop()
    nextSpace = spaceStack.pop()
    interSec_x = nextSpace[0][0] + nextSpace[1][0]
    interSec_y = nextSpace[0][1] + nextSpace[1][1]
    if curSpace[0][0] == interSec_x:
        nextSpace[1][0] += curSpace[1][0]
    elif curSpace[0][1] == interSec_y:
        nextSpace[1][1] += curSpace[1][1]
    spaceStack.append(nextSpace)
    return spaceStack

#print(create_residual_space(spaceStack))
