class State:
    def __init__(self, residualSpaceList, occupiedSpaceList, filledBlocks, utilization):
        self.residualSpaceList = residualSpaceList
        self.occupiedSpaceList = occupiedSpaceList
        self.filledBlocks = filledBlocks
        self.utilization = utilization
       
    
    def get_residualSpaceList(self):
        return self.residualSpaceList
    
    def get_occupiedSpaceList(self):
        return self.occupiedSpaceList

    def get_filledBlocks(self):
        return self.filledBlocks

    def get_utilization(self):
        return self.utilization
    
     def set_residualSpaceList(self, residualSpaceList):
        return self.residualSpaceList = residualSpaceList
    
    def set_occupiedSpaceList(self,occupiedSpaceList):
        return self.occupiedSpaceList = occupiedSpaceList

    def set_filledBlocks(self, filledBlocks):
        return self.filledBlocks = filledBlocks

    def set_utilization(self,utilization):
        return self.utilization = utilization
   