class State:
    def __init__(self, residualSpaceList, planListSpace,planListBlock):
        self.residualSpaceList = residualSpaceList
        self.planListSpace = planListSpace
        self.planListBlock = planListBlock
        self.utilization = 0
        self.available = {}

    # TODO rest of the three methods maybe has the similar function?
    def add_block_planListBlock(self, block):
        self.planListBlock.append(block)

    def add_space_planListSpace(self, space):
        self.planListSpace.append(space)

    def get_residualSpaceList(self):
        return self.residualSpaceList
    
    def get_planListSpace(self):
        return self.planListSpace

    def get_planListBlock(self):
        return self.planListBlock

    def get_utilization(self):
        return self.utilization

    def get_available_items(self):
        return self.available

    def set_available_items(self, available):
        self.available  = available
        return self.available

    def set_filledBlocks(self, filledBlocks):
        self.filledBlocks = filledBlocks
        return self.filledBlocks

    def set_utilization(self,utilization):
        self.utilization = utilization
        return self.utilization

    def __repr__(self):
        return "{res: %s\n, occu:%s\n, fill: %s\n, ut: %s\n, avail:%s\n" \
               % (self.residualSpaceList, self.occupiedSpaceList, self.filledBlocks, self.utilization, self.available) + "}\n"


    # def add_block_occupiedSpaceList(self, block):
    #     self.occupiedSpaceList.append(block)
    # # TODO do i need it since we are updating inside the create residul space and we just totally create a new list
    # def add_space_residualSpaceList(self, space):
    #     self.SpaceList.append(space)

    # Added
    # def add_block_filledbockList(self, block):
    #     self.filledBlocks.append(block)

    # def set_residualSpaceList(self, residualSpaceList):
    #     self.residualSpaceList = residualSpaceList
    #     return self.residualSpaceList
    # def set_occupiedSpaceList(self,occupiedSpaceList):
    #     self.occupiedSpaceList = occupiedSpaceList
    #     return self.occupiedSpaceList