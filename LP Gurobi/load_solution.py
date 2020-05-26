from ortec.scientific.benchmarks.loadbuilding.instance.read.YAMLtoThreeDinstance import YAMLtoThreeDinstance
import yaml

def load_solution(path):

    # load instance
    yamlToLB = YAMLtoThreeDinstance(path)
    lbSol = yamlToLB.CreateThreeDinstance()

    # load yaml file (for reading color only)
    with open(path) as f:
        heuristic_solution = yaml.load(f, Loader=yaml.FullLoader)

    # validate
    checkResult = lbSol.AllChecks()
    if checkResult[0] and (not heuristic_solution is None):
        print("Heuristic solution loaded successfully. \n")
    elif not checkResult[0]:
        print("Heuristic solution validation failed: " + checkResult[1])
    else:
        print("Heuristic solution validation failed: YAML-Loader error")

    # sets
    I_heur = [] # set of boxes
    o_heur = [] # orientations of box i
    pos_heur = [] # position of box i
    color_heur = [] # color of box i
    itemid_heur = [] # itemid of box i

    itemKinds = heuristic_solution['layout']['containers'][0]['loadingspaces'][0]['placements']
    
    

    # boxes
    for counter in range(len(itemKinds)):  
         
        pos_heur.append(itemKinds[counter]['position'])
        o_heur.append(itemKinds[counter]['orientation'])
        color_heur.append(itemKinds[counter]['color'])       
        itemid_heur.append(itemKinds[counter]['itemid'])
        
    
    I_heur = range(len(o_heur))

    return heuristic_solution, lbSol, I_heur, o_heur, pos_heur, color_heur, itemid_heur