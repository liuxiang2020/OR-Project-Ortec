from gurobipy import *
import yaml
import copy

def skeleton_solution():
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
    return yaml.load(skeleton, Loader=yaml.FullLoader)

def construct_solution(path, instance, lbInstance, model, I, color, itemid, L, W, H): 
    solution = skeleton_solution()

    solution["description"] = instance["description"]
    itemKinds = instance['data']['itemkinds']

    # placements/ unplaced
    placements = []
    unplaced = []
    for i in I:
        s = model.getVarByName("s_%i" % (i)).x
        if s == 1:

            placement = {}
            placement["id"] = i
            placement["itemid"] = itemid[i]
            # pos
            x = model.getVarByName("x_%i" % (i)).x
            y = model.getVarByName("y_%i" % (i)).x
            z = model.getVarByName("z_%i" % (i)).x
            placement["position"] = "%i,%i,%i" % (x, y, z)

            # orientation
            lx = model.getVarByName("lx_%i" % (i)).x
            lz = model.getVarByName("lz_%i" % (i)).x
            wy = model.getVarByName("wy_%i" % (i)).x
            hz = model.getVarByName("hz_%i" % (i)).x

            if [lx, lz, wy, hz] == [1, 0, 1, 1]:
                placement["orientation"] = "LWH"
            elif [lx, lz, wy, hz] == [0, 0, 0, 1]:
                placement["orientation"] = "WLH"
            elif [lx, lz, wy, hz] == [0, 1, 1, 0]:
                placement["orientation"] = "HWL"
            elif [lx, lz, wy, hz] == [1, 0, 0, 0]:
                placement["orientation"] = "LHW"
            elif [lx, lz, wy, hz] == [0, 0, 0, 0]:
                placement["orientation"] = "HLW"
            elif [lx, lz, wy, hz] == [0, 1, 0, 0]:
                placement["orientation"] = "WHL"
            else:
                placement["orientation"] = "%s%s%s%s" % (lx, lz, wy, hz)
                print([lx, lz, wy, hz])
            
            # color
            placement["color"] = color[i]

            placements = placements + [placement]
        # TODO: unplaced

    solution['layout']['containers'][0]['loadingspaces'][0]['placements'] = placements

    # write solution
    yaml_file = open(path, "w")
    solution_string = yaml.dump(solution)
    yaml_file.write(solution_string)
    yaml_file.close()
        





















