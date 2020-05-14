from gurobipy import *

from load_instance import load_instance

# I: set of boxes
# M: an arbitrary large number
# p: length of box i
# q: width of box i
# r: height of box i
# o: orientations of box i
# color: color of box i
# L: length of container
# W: width of container
# H: height of container
def solve(I, M, p, q, r, o, L, W, H):
    all_orientations = ["HWL", "HLW", "WHL", "WLH", "LWH", "LHW"]

    # init model
    model = Model(name="SCLP")

    # decision variables
    ## s: equal to 1 if box i is placed in container and 0 otherwise
    s = {}
    for i in I:
        s[i] = model.addVar(vtype=GRB.BINARY, name="s_%i" % (i)) # (21)
    
    ## x, y, z: coordinates of the front-left-bottom corner of box i
    x = {}
    y = {}
    z = {}
    for i in I:
        x[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=L, name="x_%i" % (i)) # (20)
        y[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=W, name="y_%i" % (i))
        z[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=H, name="z_%i" % (i))
    
    ## lx, ly, lz, wx, wy, wz, hx, hy, hz: equal to 1 if the l-/w-/h-dimension of box i is parallel to to the x-/y-/z-axis
    lx = {}
    ly = {}
    lz = {}
    wx = {}
    wy = {}
    wz = {}
    hx = {}
    hy = {}
    hz = {}
    for i in I:
        lx[i] = model.addVar(vtype=GRB.BINARY, name="lx_%i" % (i)) # (23)
        ly[i] = model.addVar(vtype=GRB.BINARY, name="ly_%i" % (i))
        lz[i] = model.addVar(vtype=GRB.BINARY, name="lz_%i" % (i))
        wx[i] = model.addVar(vtype=GRB.BINARY, name="wx_%i" % (i)) # (24)
        wy[i] = model.addVar(vtype=GRB.BINARY, name="wy_%i" % (i))
        wz[i] = model.addVar(vtype=GRB.BINARY, name="wz_%i" % (i))
        hx[i] = model.addVar(vtype=GRB.BINARY, name="hx_%i" % (i)) # (25)
        hy[i] = model.addVar(vtype=GRB.BINARY, name="hy_%i" % (i))
        hz[i] = model.addVar(vtype=GRB.BINARY, name="hz_%i" % (i))

    ## a, b, c, d, e, f: equal to 1 if box i is left/right/behind/in front/below/above box k and 0 otherwise
    a = {}
    b = {}
    c = {}
    d = {}
    e = {}
    f = {}
    for i in I:
        for k in I:
            if i < k:
                a[i, k] = model.addVar(vtype=GRB.BINARY, name="a_%i_%i" % (i, k)) # (26)
                b[i, k] = model.addVar(vtype=GRB.BINARY, name="b_%i_%i" % (i, k))
                c[i, k] = model.addVar(vtype=GRB.BINARY, name="c_%i_%i" % (i, k))
                d[i, k] = model.addVar(vtype=GRB.BINARY, name="d_%i_%i" % (i, k))
                e[i, k] = model.addVar(vtype=GRB.BINARY, name="e_%i_%i" % (i, k))
                f[i, k] = model.addVar(vtype=GRB.BINARY, name="f_%i_%i" % (i, k))
    
    # objective (1) --> (27)
    model.setObjective(quicksum(p[i] * q[i] * r[i] * s[i] for i in I), GRB.MAXIMIZE)

    # constraints
    ## boxes i and k must not overlap
    for i in I:
        for k in I:
            if i < k:
                model.addConstr(x[i] + p[i] * lx[i] + q[i] * wx[i] + r[i] * hx[i] <= x[k] + (1 - a[i, k]) * M) # (2)
                model.addConstr(x[k] + p[k] * lx[k] + q[k] * wx[k] + r[k] * hx[k] <= x[i] + (1 - b[i, k]) * M) # (3)

                model.addConstr(y[i] + p[i] * ly[i] + q[i] * wy[i] + r[i] * hy[i] <= y[k] + (1 - c[i, k]) * M) # (4)
                model.addConstr(y[k] + p[k] * ly[k] + q[k] * wy[k] + r[k] * hy[k] <= y[i] + (1 - d[i, k]) * M) # (5)

                model.addConstr(z[i] + p[i] * lz[i] + q[i] * wz[i] + r[i] * hz[i] <= z[k] + (1 - e[i, k]) * M) # (6)
                model.addConstr(z[k] + p[k] * lz[k] + q[k] * wz[k] + r[k] * hz[k] <= z[i] + (1 - f[i, k]) * M) # (7)
                
                model.addConstr(a[i, k] + b[i, k] + c[i, k] + d[i, k] + e[i, k] + f[i, k] >= s[i] + s[k] - 1) # (8) --> (28)
    
    ## each box i must be assigned to one container (9), containers used (10) --> not necessary in one container case

    ## each box i must be placed completely inside of container
    for i in I:
        model.addConstr(x[i] + p[i] * lx[i] + q[i] * wx[i] + r[i] * hx[i] <= L + (1 - s[i]) * M) # (11) --> (29)
        model.addConstr(y[i] + p[i] * ly[i] + q[i] * wy[i] + r[i] * hy[i] <= W + (1 - s[i]) * M) # (12) --> (30)
        model.addConstr(z[i] + p[i] * lz[i] + q[i] * wz[i] + r[i] * hz[i] <= H + (1 - s[i]) * M) # (13) --> (31)
    
    ## each dimension of box i must be parallel to one axis
    for i in I:
        
        model.addConstr(lx[i] + ly[i] + lz[i] == 1) # (14)
        model.addConstr(wx[i] + wy[i] + wz[i] == 1) # (15)
        model.addConstr(hx[i] + hy[i] + hz[i] == 1) # (16)

        model.addConstr(lx[i] + wx[i] + hx[i] == 1) # (17)
        model.addConstr(ly[i] + wy[i] + hy[i] == 1) # (18)
        model.addConstr(lz[i] + wz[i] + hz[i] == 1) # (19)

    ## allowed orientations:
    for i in I:
        # x axis
        string = ""
        for st in o[i]:
            string = string + st[0]
        if "L" not in string:
            model.addConstr(lx[i] == 0)
        if "W" not in string:
            model.addConstr(wx[i] == 0)
        if "H" not in string:
            model.addConstr(hx[i] == 0)  
        # y axis
        string = ""
        for st in o[i]:
            string = string + st[1]
        if "L" not in string:
            model.addConstr(ly[i] == 0)
        if "W" not in string:
            model.addConstr(wy[i] == 0)
        if "H" not in string:
            model.addConstr(hy[i] == 0) 
        # y axis
        string = ""
        for st in o[i]:
            string = string + st[2]
        if "L" not in string:
            model.addConstr(lz[i] == 0)
        if "W" not in string:
            model.addConstr(wz[i] == 0)
        if "H" not in string:
            model.addConstr(hz[i] == 0)     
    
    ## full support (box to box)
    for i in I:
        for k in I:
            if i < k:
                # dont overlap in x
                model.addConstr(x[i] + p[i] * lx[i] + q[i] * wx[i] + r[i] * hx[i] >= x[k] + p[k] * lx[k] + q[k] * wx[k] + r[k] * hx[k] - (1 - f[i, k]) * M)
                model.addConstr(x[k] + p[k] * lx[k] + q[k] * wx[k] + r[k] * hx[k] >= x[i] + p[k] * lx[k] + q[k] * wx[k] + r[k] * hx[k] - (1 - f[i, k]) * M)
                model.addConstr(x[i] <= x[k] + (1 - f[i, k]) * M)
                model.addConstr(x[k] <= x[i] + (1 - f[i, k]) * M)

                # dont overlap in y
                model.addConstr(y[i] + p[i] * ly[i] + q[i] * wy[i] + r[i] * hy[i] >= y[k] + p[k] * ly[k] + q[k] * wy[k] + r[k] * hy[k] - (1 - f[i, k]) * M)
                model.addConstr(y[k] + p[k] * ly[k] + q[k] * wy[k] + r[k] * hy[k] >= y[i] + p[k] * ly[k] + q[k] * wy[k] + r[k] * hy[k] - (1 - f[i, k]) * M)
                model.addConstr(y[i] <= y[k] + (1 - f[i, k]) * M)
                model.addConstr(y[k] <= y[i] + (1 - f[i, k]) * M)
    
    ## full support (box to ground)
    for i in I:
        model.addConstr(z[i] <= quicksum(f[i, k] for k in I if i < k) * M) # place box to ground if no box is below it
    
    model.optimize()

    if model.status == GRB.OPTIMAL:
        print("Model solved successfully")
        space_utilization = model.ObjVal / L / W / H
        print("Space utilization: %s" % (space_utilization))
        for i in I:
            if s[i].x == 1:
                print("Pack box %i to position (%i | %i | %i)" % (i, x[i].x, y[i].x, z[i].x))
            else:
                print("Don't pack box", i)
    elif model.status == GRB.INFEASIBLE:
        print("No success: Infeasible")
    else:
        print("No success:", model.status)
    
    return model



