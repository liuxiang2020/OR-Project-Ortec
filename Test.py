import unittest
import os
import numpy as np


def SimpleAlgorithm( instanceFileName, strategy):
    solution = SkeletonSolution()
    instance = None
    with open(instanceFileName) as f:
        import yaml
        instance = yaml.load( f, Loader=yaml.FullLoader )
    if not instance is None:
        solution['description'] = instance['description']
        # note that we only have one container with one loading space
        unplaced = solution['layout']['unplaced']
        containerSize = Size2Pos( instance['data']['containerkinds'][0]['loadingspaces'][0]['size'] )
        itemKinds = instance['data']['itemkinds']
        import copy
        unplaced = [ copy.deepcopy(unplaced[0]) for i in range(len(itemKinds)) ]
        available = [ik['quantity'] for ik in itemKinds]
        id = 0
        for itemKind in range(len(itemKinds)):
            unplaced[itemKind]['id'] = id
            unplaced[itemKind]['itemid'] = itemKinds[itemKind]['id']
            unplaced[itemKind]['quantity'] = available[itemKind]
            id += 1
        referencePos = String2Pos( instance['data']['containerkinds'][0]['loadingspaces'][0]['position'] )
        placements,available = strategy(itemKinds,containerSize,referencePos,id,available)
        for itemKind in range(len(itemKinds)):
         unplaced[itemKind]['quantity'] = available[itemKind]
        solution['layout']['containers'][0]['loadingspaces'][0]['placements'] = placements
        solution['layout']['unplaced'] = unplaced
    return solution


def FullLayerArrangements(itemKinds,containerSize,referencePos,id,available):
    placements = []
    pos = referencePos.copy()
    for itemKind in range(len(itemKinds)):
        color = None
        if 'color' in itemKinds[itemKind]:
            color = itemKinds[itemKind]['color']
        for orientation in itemKinds[itemKind]['orientations'].split(','):
            size = Size2Pos(itemKinds[itemKind]['size'], orientation)
            if pos[2] + size[2] <= containerSize[2]:
                maxInLength = int((containerSize[0] - pos[0]) / size[0])
                maxInWidth = int((containerSize[1] - pos[1]) / size[1])
                maxInHeight = int((containerSize[2] -pos[2]) / size[2])
                maxToPlaceFlat = maxInLength * maxInWidth
                if available[itemKind] >= maxToPlaceFlat:
                    countLayers = 1
                    while available[itemKind] >= maxToPlaceFlat and countLayers <= maxInHeight:
                        countLayers += 1
                        for w in range(maxInWidth):
                            for l in range(maxInLength):
                                placement = MakePlacement(pos,id,itemKinds[itemKind]['id'],orientation,color)
                                placements = placements + [ placement ]
                                id += 1
                                pos[0] += size[0]
                            pos[0] = referencePos[0]
                            pos[1] += size[1]
                        available[itemKind] -= maxToPlaceFlat
                        pos[0] = referencePos[0]
                        pos[1] = referencePos[1]
                        pos[2] += size[2]
                    containerSize[0] = maxInLength * size[0]
                    containerSize[1] = maxInWidth * size[1]
    return placements, available


def String2Pos( string ):
    return np.asarray([int(p) for p in string.split(',')]).astype(int)

def Pos2String( pos ):
    return ','.join([str(p) for p in pos])

def Size2Pos( size, orientation='LWH' ):
    mask = { 'L': 'length', 'W': 'width', 'H': 'height' }
    return np.asarray( [ size[mask[o]] for o in list(orientation) ] ).astype(int)

def MakePlacement(pos,id,itemid,orientation,color=None):
    placement = { 'id': id, 'position': Pos2String(pos), 'itemid': itemid, 'orientation': orientation }
    if not color is None:
        placement['color'] = color
    return placement

def SkeletonSolution():
    skeleton = """description:
  set: Bischoff & Ratcliff
  name: '1.1'
layout:
  containers:
  - id: 1
    kindid: 1
    loadingspaces:
    - id: 1
      placements:
  unplaced:
  - id: 1
    itemid: 1
    quantity: 0"""
    import yaml
    return yaml.load( skeleton, Loader=yaml.FullLoader )


solution = SimpleAlgorithm("br01.001.yaml", FullLayerArrangements)
import yaml
with open(r'C:\Users\dungn\Desktop\OR-Practice\store_file.yaml', 'w') as file:
    documents = yaml.dump(solution, file)