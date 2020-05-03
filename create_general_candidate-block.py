# item_usage: store quantity of different types of boxes have been used
# it is a counter of tuple [(id,quantity remain), (id,quantityremain)....]

# check box availability, discard blocks if 
# a block containing a certain number of a type of boxes has already been placed in the 
# container, then another block which requires more boxes of this
# type than the available left-over 

def Check_availabiliy(gb, currentSpace):    
    for i in range(len(gb[0])):
        if item_available[gb[i]] >= gb[1][i]:
            continue;
        else:
            return False
    return True

available = {(1,10),(2,33),(3,39)}

#[216, 228, 150] 
curr_Space = [220,230,155]
def Generate_Candidate_Block_List(currentSpace, generalBlockList, item_available):   
    candidateBlockList = []
    #S = [L,W,H]
    S = currentSpace 
    for gb in generalBlockList:
        #Check block size and space size 
        if (gb.get_size()[0] <= S[0] and gb.get_size()[1] <= S[1] and gb.get_size()[2] <= S[2] ):    
            #Check fitness
            spaceVolume = S[0]*S[1]*S[2]
            gbVolume = gb.get_volume()
            if (spaceVolume <= 2*gbVolume):  
                if Check_availablility(gb,currentSpace) == True:
                    fitness = 2*gbVolume-spaceVolume
                    candidateBlockList.append((gb,fitness))
                    
    candidateBlockList.sort(key=lambda x:x[1],reverse=True)
    print(candidateBlockList)
    return candidateBlockList            

