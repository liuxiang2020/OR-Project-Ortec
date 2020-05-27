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
def solve(I, M, p, q, r, orientations, L, W, H, starting_solution):
    all_orientations = ["HWL", "HLW", "WHL", "WLH", "LWH", "LHW"]
    #print(starting_solution[0])
    #print("x", starting_solution[1])
    #print("y", starting_solution[2])
    #print("z", starting_solution[3])
    #print("xr", starting_solution[4])
    #print("yr", starting_solution[5])
    #print("zr", starting_solution[6])
    #print("a", starting_solution[16])
    #print("g", starting_solution[19])
    #print("h", starting_solution[20])
    #print("o", starting_solution[21])
    #print("sk", starting_solution[22])
    #print("vs", starting_solution[27])
    #print("s1", starting_solution[28])
    # init model
    model = Model(name="SCLP")

    # model parameters
    '''
    model.Params.OptimalityTol = .00001 # Tolerance
    model.Params.FeasibilityTol = .00001 # Tolerance
    model.Params.MIPFocus = 1 # focus on finding feasible solutions quickly
    model.Params.VarBranch = 3 # strong branching
    model.Params.TimeLimit = 600 # seconds
    model.Params.NodeLimit = 10000
    model.Params.SolutionLimit = 3 # stop after 3rd feasible solution
    model.Params.MIPGap = 0.1 # stop when within 10% optimum
    '''

    # decision variables
    ## s: equal to 1 if box i is placed in container and 0 otherwise
    s = {}
    for i in I:
        s[i] = model.addVar(vtype=GRB.BINARY, name="s_%i" % (i)) # (21)
    
    ## x, y, z: coordinates of the front-left-bottom corner of box i
    x = {}; y = {}; z = {}
    for i in I:
        x[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=L, name="x_%i" % (i)) # (20)
        y[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=W, name="y_%i" % (i))
        z[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=H, name="z_%i" % (i))

    ## xr, yr, zr: coordinates of the rear-right corner of box i
    xr = {}; yr = {}; zr = {}
    for i in I:
        xr[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=L, name="xr_%i" % (i))
        yr[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=W, name="yr_%i" % (i))
        zr[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=H, name="zr_%i" % (i))
    
    ## lx, ly, lz, wx, wy, wz, hx, hy, hz: equal to 1 if the l-/w-/h-dimension of box i is parallel to to the x-/y-/z-axis
    lx = {}; ly = {}; lz = {}
    wx = {}; wy = {}; wz = {}
    hx = {}; hy = {}; hz = {}
    for i in I:
        lx[i] = model.addVar(vtype=GRB.BINARY, name="lx_%i" % (i))
        ly[i] = model.addVar(vtype=GRB.BINARY, name="ly_%i" % (i))
        lz[i] = model.addVar(vtype=GRB.BINARY, name="lz_%i" % (i))
        wx[i] = model.addVar(vtype=GRB.BINARY, name="wx_%i" % (i))
        wy[i] = model.addVar(vtype=GRB.BINARY, name="wy_%i" % (i))
        wz[i] = model.addVar(vtype=GRB.BINARY, name="wz_%i" % (i))
        hx[i] = model.addVar(vtype=GRB.BINARY, name="hx_%i" % (i))
        hy[i] = model.addVar(vtype=GRB.BINARY, name="hy_%i" % (i))
        hz[i] = model.addVar(vtype=GRB.BINARY, name="hz_%i" % (i))

    ## a, b, c: equal to 1 if box i is right/behind/above of box k and 0 otherwise
    a = {}; b = {}; c = {}
    for i in I:
        for k in I:
            if i != k:
                a[i, k] = model.addVar(vtype=GRB.BINARY, name="a_%i_%i" % (i, k))
                b[i, k] = model.addVar(vtype=GRB.BINARY, name="b_%i_%i" % (i, k))
                c[i, k] = model.addVar(vtype=GRB.BINARY, name="c_%i_%i" % (i, k))
    
    ## g: equal to 1 if box i is on the ground and 0 otherwise
    g = {}
    for i in I:
        g[i] = model.addVar(vtype=GRB.BINARY, name="g_%i" % (i))

    h = {} ## h: 0 if box k has the suitable hight to support box i
    o = {} ## o: 0 if projections on the XY plane of the boxes i and k have a nonempty intersection
    sk = {} ## sk: equal to 1 if box k supports box i
    n1 = {} ## n1: equal to 1 if xk <= xi
    n2 = {} ## n2: equal to 1 if yk <= yi
    n3 = {} ## n3: equal to 1 if xk' <= xi'
    n4 = {} ## n4: equal to 1 if yk' <= yi'
    vs = {} ## vs: equal to 1 if vertex t of box i is supported by box k
    for i in I:
        for k in I:
            if(i != k):
                h[i, k] = model.addVar(vtype=GRB.BINARY, name="h_%i_%i" % (i, k))
                o[i, k] = model.addVar(vtype=GRB.BINARY, name="o_%i_%i" % (i, k))
                sk[i, k] = model.addVar(vtype=GRB.BINARY, name="sk_%i_%i" % (i, k))
                n1[i, k] = model.addVar(vtype=GRB.BINARY, name="n1_%i_%i" % (i, k))
                n2[i, k] = model.addVar(vtype=GRB.BINARY, name="n2_%i_%i" % (i, k))
                n3[i, k] = model.addVar(vtype=GRB.BINARY, name="n3_%i_%i" % (i, k))
                n4[i, k] = model.addVar(vtype=GRB.BINARY, name="n4_%i_%i" % (i, k))
                for t in range(0,4):
                    vs[i, k, t] = model.addVar(vtype=GRB.BINARY, name="vs_%i_%i_%i" % (i, k, t))
    
    s1 = {} ## absolute value of zr[k] - z[i]
    s2 = {} ## equal to 1 if zr[k] > z[i] and 0 otherwise
    for i in I:
        for k in I:
            if(i != k):
                s1[i, k] = model.addVar(vtype=GRB.CONTINUOUS, name="s1_%i_%i" % (i, k))
                s2[i, k] = model.addVar(vtype=GRB.BINARY, name="s2_%i_%i" % (i, k))
    

    # objective
    model.setObjective(quicksum(p[i] * q[i] * r[i] * s[i] for i in I), GRB.MAXIMIZE)

    # constraints
    ## boxes dont overlap the container
    for i in I:
        '''
        model.addConstr(xr[i] <= L + (1 - s[i]) * L, name="5_%i" % (i)) # (5)
        model.addConstr(yr[i] <= W + (1 - s[i]) * W, name="6_%i" % (i)) # (6)
        model.addConstr(zr[i] <= H + (1 - s[i]) * H, name="7_%i" % (i)) # (7)
        '''
        model.addConstr(xr[i] <= L * s[i], name="5_%i" % (i)) # (5)
        model.addConstr(yr[i] <= W * s[i], name="6_%i" % (i)) # (6)
        model.addConstr(zr[i] <= H * s[i], name="7_%i" % (i)) # (7)
        
    
    ## connect position variables
    for i in I:
        model.addConstr(xr[i] == x[i] + lx[i] * p[i] + wx[i] * q[i] + hx[i] * r[i], name="8_%i" % (i)) # (8)
        model.addConstr(yr[i] == y[i] + ly[i] * p[i] + wy[i] * q[i] + hy[i] * r[i], name="9_%i" % (i)) # (9)
        model.addConstr(zr[i] == z[i] + lz[i] * p[i] + wz[i] * q[i] + hz[i] * r[i], name="10_%i" % (i)) # (10)
        
    ## each dimension must be parallel to one axis
    for i in I:
        model.addConstr(lx[i] + ly[i] + lz[i] == 1, name="11.1_%i" % (i)) # (11)
        model.addConstr(wx[i] + wy[i] + wz[i] == 1, name="11.2_%i" % (i))
        model.addConstr(hx[i] + hy[i] + hz[i] == 1, name="11.3_%i" % (i))

        model.addConstr(lx[i] + wx[i] + hx[i] == 1, name="12.1_%i" % (i)) # (12)
        model.addConstr(ly[i] + wy[i] + hy[i] == 1, name="12.2_%i" % (i))
        model.addConstr(lz[i] + wz[i] + hz[i] == 1, name="12.3_%i" % (i))
    
    ## boxes dont overlap each other
    for i in I:
        for k in I:
            if i != k:
                model.addConstr(a[i, k] + a[k, i] + b[i, k] + b[k, i] + c[i, k] + c[k, i] >= s[i] + s[k] - 1, name="13_%i_%i" % (i, k)) # (13)

                model.addConstr(xr[k] <= x[i] + (1 - a[i, k]) * L, name="14_%i_%i" % (i, k)) # (14)
                model.addConstr(x[i] + 1 <= xr[k] + a[i, k] * L, name="15_%i_%i" % (i, k)) # (15)
                
                model.addConstr(yr[k] <= y[i] + (1 - b[i, k]) * W, name="16_%i_%i" % (i, k)) # (16)
                model.addConstr(y[i] + 1 <= yr[k] + b[i, k] * W, name="17_%i_%i" % (i, k)) # (17)
                
                model.addConstr(zr[k] <= z[i] + (1 - c[i, k]) * H, name="18_%i_%i" % (i, k)) # (18)
    
    ## allowed orientations
    for i in I:
        # x axis (19)
        string = ""
        for st in orientations[i]:
            string = string + st[0]
        if "L" not in string:
            model.addConstr(lx[i] == 0, name="19.L_%i" % (i))
        if "W" not in string:
            model.addConstr(wx[i] == 0, name="19.W_%i" % (i))
        if "H" not in string:
            model.addConstr(hx[i] == 0, name="19.H_%i" % (i)) 
        if i == 8:
            print("8:", orientations[i])
        # y axis (20)
        string = ""
        for st in orientations[i]:
            string = string + st[1]
        if "L" not in string:
            model.addConstr(ly[i] == 0, name="20.L_%i" % (i))
        if "W" not in string:
            model.addConstr(wy[i] == 0, name="20.W_%i" % (i))
        if "H" not in string:
            model.addConstr(hy[i] == 0, name="20.H_%i" % (i)) 
        # z axis (21)
        string = ""
        for st in orientations[i]:
            string = string + st[2]
        if "L" not in string:
            model.addConstr(lz[i] == 0, name="21.L_%i" % (i))
        if "W" not in string:
            model.addConstr(wz[i] == 0, name="21.W_%i" % (i))
        if "H" not in string:
            model.addConstr(hz[i] == 0, name="21.H_%i" % (i))
    
    ## each vertex supported by other box or ground
    for i in I:
        # replaced >= by ==
        model.addConstr(quicksum(vs[i, k, t] for k in I for t in range(0, 4) if i != k) >= 4 * (1 - g[i]), name="26_%i" % (i)) # (26)
        model.addConstr(z[i] <= (1 - g[i]) * H, name="27_%i" % (i)) # (27)
    
    for i in I:
        for k in I:
            if i != k:
                ## suitible height for support
                model.addConstr(zr[k] - z[i] <= s1[i, k], name="28_%i_%i" % (i, k)) # (28)
                model.addConstr(z[i] - zr[k] <= s1[i, k], name="29_%i_%i" % (i, k)) # (29)

                model.addConstr(s1[i, k] <= zr[k] - z[i] + 2 * H * (1 - s2[i, k]), name="30_%i_%i" % (i, k)) # (30)
                model.addConstr(s1[i, k] <= z[i] - zr[k] + 2 * H * s2[i, k], name="31_%i_%i" % (i, k)) # (31)

                model.addConstr(h[i, k] <= s1[i, k], name="32_%i_%i" % (i, k)) # (32)
                model.addConstr(s1[i, k] <= h[i, k] * H, name="33_%i_%i" % (i, k)) # (33)

                # boxes i and k share a part of their orthogonal projection
                model.addConstr(o[i, k] <= a[i, k] + a[k, i] + b[i, k] + b[k, i], name="34.1_%i_%i" % (i, k)) # 34
                model.addConstr(a[i, k] + a[k, i] + b[i, k] + b[k, i] <= 2 * o[i, k], name="34.2_%i_%i" % (i, k))

                # if bottom of i supported by top of k, it implies h + o = 0
                model.addConstr(1 - sk[i, k] <= h[i, k] + o[i, k], name="35.1_%i_%i" % (i, k)) # 35
                model.addConstr(h[i, k] + o[i, k] <= 2 * (1 - sk[i, k]), name="35.1_%i_%i" % (i, k))

                ## support
                model.addConstr(s[i] - s[k] <= 1 - sk[i, k], name="36_%i_%i" % (i, k)) # (36)
                model.addConstr(s[k] - s[i] <= 1 - sk[i, k], name="37_%i_%i" % (i, k)) # (37)

                for t in range(0, 4):
                    model.addConstr(vs[i, k, t] <= sk[i, k], name="38_%i_%i_%i" % (i, k, t)) # (38)
                    
                model.addConstr(n1[i, k] + n2[i, k] <= 2 * (1 - vs[i, k, 0]), name="39_%i_%i" % (i, k)) # (39)
                model.addConstr(n2[i, k] + n3[i, k] <= 2 * (1 - vs[i, k, 1]), name="40_%i_%i" % (i, k)) # (40)
                model.addConstr(n3[i, k] + n4[i, k] <= 2 * (1 - vs[i, k, 2]), name="41_%i_%i" % (i, k)) # (41)
                model.addConstr(n1[i, k] + n4[i, k] <= 2 * (1 - vs[i, k, 3]), name="42_%i_%i" % (i, k)) # (42)
                                    
                ## orthogonal projection overlapping
                model.addConstr(x[k] <= x[i] + n1[i, k] * L, name="43_%i_%i" % (i, k)) # (43)
                model.addConstr(y[k] <= y[i] + n2[i, k] * W, name="44_%i_%i" % (i, k)) # (44)
                model.addConstr(xr[i] <= xr[k] + n3[i, k] * L, name="45_%i_%i" % (i, k)) # (45)
                model.addConstr(yr[i] <= yr[k] + n4[i, k] * W, name="46_%i_%i" % (i, k)) # (46)

    model.update()

    '''
    # starting solution
    #[s_, x_, y_, z_, xr_, yr_, zr_, lx_, ly_, lz_, wx_, wy_, wz_, hx_, hy_, hz_, a_, b_, c_, g_, h_, o_, sk_, n1_, n2_, n3_, n4_, vs_, s1_, s2_]
    for i in I:
        model.getVarByName("s_%i" % (i)).start = starting_solution[0][i]
        
        model.getVarByName("x_%i" % (i)).start = starting_solution[1][i]
        model.getVarByName("y_%i" % (i)).start = starting_solution[2][i]
        model.getVarByName("z_%i" % (i)).start = starting_solution[3][i]

        model.getVarByName("xr_%i" % (i)).start = starting_solution[4][i]
        model.getVarByName("yr_%i" % (i)).start = starting_solution[5][i]
        model.getVarByName("zr_%i" % (i)).start = starting_solution[6][i]

        model.getVarByName("lx_%i" % (i)).start = starting_solution[7][i]
        model.getVarByName("ly_%i" % (i)).start = starting_solution[8][i]
        model.getVarByName("lz_%i" % (i)).start = starting_solution[9][i]

        model.getVarByName("wx_%i" % (i)).start = starting_solution[10][i]
        model.getVarByName("wy_%i" % (i)).start = starting_solution[11][i]
        model.getVarByName("wz_%i" % (i)).start = starting_solution[12][i]

        model.getVarByName("hx_%i" % (i)).start = starting_solution[13][i]
        model.getVarByName("hy_%i" % (i)).start = starting_solution[14][i]
        model.getVarByName("hz_%i" % (i)).start = starting_solution[15][i]

        model.getVarByName("g_%i" % (i)).start = starting_solution[19][i]

        for k in I:
            if i != k:
                model.getVarByName("a_%i_%i" % (i, k)).start = starting_solution[16][i, k]
                model.getVarByName("b_%i_%i" % (i, k)).start = starting_solution[17][i, k]
                model.getVarByName("c_%i_%i" % (i, k)).start = starting_solution[18][i, k]

                model.getVarByName("h_%i_%i" % (i, k)).start = starting_solution[20][i, k]
                model.getVarByName("o_%i_%i" % (i, k)).start = starting_solution[21][i, k]
                model.getVarByName("sk_%i_%i" % (i, k)).start = starting_solution[22][i, k]

                model.getVarByName("n1_%i_%i" % (i, k)).start = starting_solution[23][i, k]
                model.getVarByName("n2_%i_%i" % (i, k)).start = starting_solution[24][i, k]
                model.getVarByName("n3_%i_%i" % (i, k)).start = starting_solution[25][i, k]
                model.getVarByName("n4_%i_%i" % (i, k)).start = starting_solution[26][i, k]

                model.getVarByName("s1_%i_%i" % (i, k)).start = starting_solution[28][i, k]
                model.getVarByName("s2_%i_%i" % (i, k)).start = starting_solution[29][i, k]

                for t in range(0, 4):
                    model.getVarByName("vs_%i_%i_%i" % (i, k, t)).start = starting_solution[27][i, k, t]
    '''

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



