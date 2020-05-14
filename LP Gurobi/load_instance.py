from ortec.scientific.benchmarks.loadbuilding.instance.read.YAMLtoThreeDinstance import YAMLtoThreeDinstance
import yaml

def load_instance(path):

    # load instance
    yamlToLB = YAMLtoThreeDinstance(path)
    lbInstance = yamlToLB.CreateThreeDinstance()

    # load yaml file (for reading color only)
    with open(path) as f:
        instance = yaml.load(f, Loader=yaml.FullLoader)

    # validate
    checkResult = lbInstance.AllChecks()
    if checkResult[0] and (not instance is None):
        print("Instance loaded successfully. \n")
    elif not checkResult[0]:
        print("Instance validation failed: " + checkResult[1])
    else:
        print("Instance validation failed: YAML-Loader error")

    # sets
    I = [] # set of boxes
    M = 0 # an arbitrary large number

    p = [] # length of box i
    q = [] # width of box i
    r = [] # height of box i
    o = [] # orientations of box i
    color = [] # color of box i
    itemid = [] # itemid of box i

    L = 0 # length of container 
    W = 0 # width of container 
    H = 0 # height of container

    itemKinds = instance['data']['itemkinds']

    # boxes
    for counter, item in enumerate(lbInstance.itemkinds):
        for i in range(item.quantity):
            p.append(item.boundingBox[0])
            q.append(item.boundingBox[1])
            r.append(item.boundingBox[2])
            o.append(item.orientations)
            color.append(instance["data"]["itemkinds"][counter]["color"])
            itemid.append(item.id)
    
    I = range(len(p))

    # container
    L = lbInstance.containerkinds[0].loadingspaces[0].boundingBox[0]
    W = lbInstance.containerkinds[0].loadingspaces[0].boundingBox[1]
    H = lbInstance.containerkinds[0].loadingspaces[0].boundingBox[2]

    # big M
    M = max([L, W, H])*1.05

    return instance, lbInstance, I, M, p, q, r, o, color, itemid, L, W, H