from Space import Space
import config
def transfer_residual_space(spaceStack):
    #The spacestack should consist of x, y and z.
    cur_space = spaceStack.pop()

    #This should never happen (when transferring residual space, there should be x and y in the spacestack)
    if not spaceStack: return spaceStack
    
    next_space = spaceStack[-1]
    
    if (cur_space.get_kind()=='x'):
        if (next_space.get_kind()=='y'):
            next_space.update_size_y(next_space.get_size()[1] + cur_space.get_size()[1])
    elif (cur_space.get_kind()=='y'):
        if (next_space.get_kind()=='x'):
            next_space.update_size_x(next_space.get_size()[0] + cur_space.get_size()[0])
    return spaceStack