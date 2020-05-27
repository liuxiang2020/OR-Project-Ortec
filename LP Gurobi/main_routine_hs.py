from gurobipy import *


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
def solve(I, M, p, q, r, o, itemid, L, W, H, I_heur, o_heur, pos_heur, color_heur, itemid_heur):
    all_orientations = ["HWL", "HLW", "WHL", "WLH", "LWH", "LHW"]

    # init model
    model = Model(name="SCLP")

    # decision variables
    ## s: equal to 1 if box i is placed in container and 0 otherwise
    s = {}
    for i in I:
        s[i] = model.addVar(vtype=GRB.BINARY, name="s_%i" % (i))
    
    ## x, y, z: coordinates of the front-left-bottom corner of box i
    x = {}
    y = {}
    z = {}
    for i in I:
        x[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=L, name="x_%i" % (i))
        y[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=W, name="y_%i" % (i))
        z[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=H, name="z_%i" % (i))

    ## xr, yr, zr: coordinates of the rear-right corner of box i
    xr = {}
    yr = {}
    zr = {}
    for i in I:
        xr[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=L, name="xr_%i" % (i))
        yr[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=W, name="yr_%i" % (i))
        zr[i] = model.addVar(vtype=GRB.CONTINUOUS, lb=0.0, ub=H, name="zr_%i" % (i))

    #getting the exact indexes of used boxes from heuristic solution
    itemindex = []
    Dummyids = [] 
    Dummyids = itemid.copy()    
    for i in I_heur:
         itemindex.append(Dummyids.index(itemid_heur[i]))
         Dummyids[itemindex[i]] = -1
    
       


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
        lx[i] = model.addVar(vtype=GRB.BINARY, name="lx_%i" % (i))
        ly[i] = model.addVar(vtype=GRB.BINARY, name="ly_%i" % (i))
        lz[i] = model.addVar(vtype=GRB.BINARY, name="lz_%i" % (i))
        wx[i] = model.addVar(vtype=GRB.BINARY, name="wx_%i" % (i))
        wy[i] = model.addVar(vtype=GRB.BINARY, name="wy_%i" % (i))
        wz[i] = model.addVar(vtype=GRB.BINARY, name="wz_%i" % (i))
        hx[i] = model.addVar(vtype=GRB.BINARY, name="hx_%i" % (i))
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
            if i != k:
                a[i, k] = model.addVar(vtype=GRB.BINARY, name="a_%i_%i" % (i, k))
                b[i, k] = model.addVar(vtype=GRB.BINARY, name="b_%i_%i" % (i, k))
                c[i, k] = model.addVar(vtype=GRB.BINARY, name="c_%i_%i" % (i, k))
                #d[i, k] = model.addVar(vtype=GRB.BINARY, name="d_%i_%i" % (i, k))
                #e[i, k] = model.addVar(vtype=GRB.BINARY, name="e_%i_%i" % (i, k))
                #f[i, k] = model.addVar(vtype=GRB.BINARY, name="f_%i_%i" % (i, k))


    #stability variables

    #1 if box i is on the ground
    g = {}
    for i in I:
        g[i] = model.addVar(vtype=GRB.BINARY, name="g_%i" % (i))

    h = {}
    o = {}
    sk = {}
    n1 = {}
    n2 = {}
    n3 = {}
    n4 = {}
    vs = {}
    for i in I:
        for k in I:
            if(i != k):
                #0 if box k has the suitable hight to support box i
                h[i, k] = model.addVar(vtype=GRB.BINARY, name="h_%i_%i" % (i, k))
                #0 if projections on the XY plane of the boxes i and k have a nonempty intersection
                o[i, k] = model.addVar(vtype=GRB.BINARY, name="o_%i_%i" % (i, k))
                #1 if box k support
                sk[i, k] = model.addVar(vtype=GRB.BINARY, name="sk_%i_%i" % (i, k))
                #0 if xk<xi
                n1[i, k] = model.addVar(vtype=GRB.BINARY, name="n1_%i_%i" % (i, k))
                #0 if xk<xi
                n2[i, k] = model.addVar(vtype=GRB.BINARY, name="n2_%i_%i" % (i, k))
                #0 if xk<xi
                n3[i, k] = model.addVar(vtype=GRB.BINARY, name="n3_%i_%i" % (i, k))
                #0 if xk<xi
                n4[i, k] = model.addVar(vtype=GRB.BINARY, name="n4_%i_%i" % (i, k))
                for t in range(0,4):
                    #1 if vertex l of box i supported by box k
                    vs[i, k, t] = model.addVar(vtype=GRB.BINARY)

    #suppport variables
    s1 = {}
    s2 = {}
    for i in I:
        for k in I:
            if(i != k):
                s1[i,k] = model.addVar(vtype=GRB.CONTINUOUS, name="o_%i_%i" % (i, k))
                s2[i,k] = model.addVar(vtype=GRB.BINARY, name="o_%i_%i" % (i, k))

    
    model.update()
    # objective
    model.setObjective(quicksum(p[i] * q[i] * r[i] * s[i] for i in I), GRB.MAXIMIZE)

    # constraints

    ## boxes i and k must not overlap
    for i in I:
        for k in I:
            if i != k:
                model.addConstr(x[k] + p[k] * lx[k] + q[k] * wx[k] + r[k] * hx[k] <= x[i] +  (1- a[i, k]) * L)
                model.addConstr(a[i,k] + a[k,i] <= 1)
                model.addConstr(y[k] + p[k] * ly[k] + q[k] * wy[k] + r[k] * hy[k] <= y[i] +  (1 - b[i, k]) * W)
                model.addConstr(b[i,k] + b[k,i] <= 1)
                model.addConstr(z[k] + p[k] * lz[k] + q[k] * wz[k] + r[k] * hz[k] <= z[i] + (1 - c[i, k]) * H)
                model.addConstr(c[i,k] + c[k,i] <= 1)
                model.addConstr(a[i, k] + b[i, k] + c[i, k] + a[k,i] + b[k,i] + c[k,i] >= s[i] + s[k] - 1)

    ## each box i must be placed completely inside of container
    for i in I:
        model.addConstr(xr[i] <= L * s[i])
        model.addConstr(yr[i] <= W * s[i])
        model.addConstr(zr[i] <= H * s[i])
        #
        #model.addConstr(x[i] + p[i] * lx[i] + q[i] * wx[i] + r[i] * hx[i] <= L + (1 - s[i]) * M)
        #model.addConstr(y[i] + p[i] * ly[i] + q[i] * wy[i] + r[i] * hy[i] <= W + (1 - s[i]) * M)
        #model.addConstr(z[i] + p[i] * lz[i] + q[i] * wz[i] + r[i] * hz[i] <= H + (1 - s[i]) * M)

    ## each dimension of box i must be parallel to one axis
    for i in I:
        model.addConstr(xr[i] - x[i] == lx[i] * p[i] + wx[i] * q[i] + hx[i]*r[i])
        model.addConstr(yr[i] - y[i] == ly[i] * p[i] + wy[i] * q[i] + hy[i]*r[i])
        model.addConstr(zr[i] - z[i] == lz[i] * p[i] + wz[i] * q[i] + hz[i]*r[i])

        model.addConstr(lx[i] + ly[i] + lz[i] == s[i])
        model.addConstr(wx[i] + wy[i] + wz[i] == s[i])
        model.addConstr(hx[i] + hy[i] + hz[i] == s[i])

        model.addConstr(lx[i] + wx[i] + hx[i] == s[i])
        model.addConstr(ly[i] + wy[i] + hy[i] == s[i])
        model.addConstr(lz[i] + wz[i] + hz[i] == s[i])


    '''
    ## allowed orientations:
    for i in I:
        for orientation in o[i].symmetric_difference(all_orientations):
            if orientation == "HWL":
                model.addConstr(hx[i] == 0)
                model.addConstr(wy[i] == 0)
                model.addConstr(lz[i] == 0)
            elif orientation == "HLW":
                model.addConstr(hx[i] == 0)
                model.addConstr(ly[i] == 0)
                model.addConstr(wz[i] == 0)
            elif orientation == "WHL":
                model.addConstr(wx[i] == 0)
                model.addConstr(hy[i] == 0)
                model.addConstr(lz[i] == 0)
            elif orientation == "WLH":
                model.addConstr(wx[i] == 0)
                model.addConstr(ly[i] == 0)
                model.addConstr(hz[i] == 0)
            elif orientation == "LWH":
                model.addConstr(lx[i] == 0)
                model.addConstr(wy[i] == 0)
                model.addConstr(hz[i] == 0)
            elif orientation == "LHW":
                model.addConstr(lx[i] == 0)
                model.addConstr(hy[i] == 0)
                model.addConstr(wz[i] == 0)
    '''


    ## full support (box to box)

    for  i in I:
        #if box i not on the ground, the four corners of the box are supported
        model.addConstr(quicksum(vs[i,k,t] for k in I for t in range(0,4) if i!=k) >= 4 *(1 - g[i]))
        #if g == 1 then box on the ground
        model.addConstr(z[i] <= (1 - g[i]) * H)
        for k in I:
            if( i != k):
                #define values for h: if box k has suitable high for supporting i
                model.addConstr(zr[k] - z[i] <= s1[i,k])
                model.addConstr(z[i] - zr[k] <= s1[i,k])
                model.addConstr(s1[i,k] <= zr[k] - z[i] + 2 * H * (1- s2[i,k]))
                model.addConstr(s1[i,k] <= z[i] - zr[k] + 2 * H * s2[i,k])
                model.addConstr(h[i,k] <= s1[i,k])
                model.addConstr(s1[i,k] <= h[i,k] * H)
                #boxes i and k share a part of their orthogonal projection
                model.addConstr(o[i,k] <= a[i,k] + a[k,i] + b[i,k] + b[k,i])
                model.addConstr(a[i,k] + a[k,i] + b[i,k] + b[k,i] <= 2 * o[i,k])
                #if bottom of i supported by top of k, it implies h + o = 0
                model.addConstr(1 - sk[i,k] <= h[i,k] + o[i,k])
                model.addConstr(h[i,k] + o[i,k] <= 2 * (1 - sk[i,k]))
                for t in range(0,4):
                    #box k supports one vertex of box i iff it is supported by box k (s(i,k) = 1)
                    model.addConstr(vs[i,k,t] <= sk[i,k])
                    #vertex support
                    model.addConstr(n1[i,k] + n2[i,k] <= 2* (1 - vs[i,k,t]))
                    model.addConstr(n2[i,k] + n3[i,k] <= 2* (1 - vs[i,k,t]))
                    model.addConstr(n3[i,k] + n4[i,k] <= 2* (1 - vs[i,k,t]))
                    model.addConstr(n1[i,k] + n4[i,k] <= 2* (1 - vs[i,k,t]))
                #similar to
                model.addConstr(x[k] <= x[i] + n1[i,k] * L)
                model.addConstr(y[k] <= y[i] + n2[i,k] * W)
                model.addConstr(xr[i] <= xr[k] + n3[i,k] * L)
                model.addConstr(yr[i] <= yr[k] + n4[i,k] * W)

    
    #giving the starting solutions
    model.update()
    k = -1
    for i in I:
        if i in itemindex and k <= len(itemindex):
            s[i].start = 1  
            k +=1
            if o_heur[k] == "LWH":
                lx[i].start = 1; ly[i].start = 0; lz[i].start = 0
                wx[i].start = 0; wy[i].start = 1; wz[i].start = 0
                hx[i].start = 0; hy[i].start = 0; hz[i].start = 1
            elif o_heur[k] == "WHL":
                lx[i].start = 0; ly[i].start = 0; lz[i].start = 1
                wx[i].start = 1; wy[i].start = 0; wz[i].start = 0
                hx[i].start = 0; hy[i].start = 1; hz[i].start = 0            
            elif o_heur[k] == "HLW":
                lx[i].start = 0; ly[i].start = 1; lz[i].start = 0
                wx[i].start = 0; wy[i].start = 0; wz[i].start = 1
                hx[i].start = 1; hy[i].start = 0; hz[i].start = 0  
            elif o_heur[k] == "WLH":
                lx[i].start = 0; ly[i].start = 1; lz[i].start = 0
                wx[i].start = 1; wy[i].start = 0; wz[i].start = 0
                hx[i].start = 0; hy[i].start = 0; hz[i].start = 1  
            elif o_heur[k] == "HWL":    
                lx[i].start = 0; ly[i].start = 0; lz[i].start = 1
                wx[i].start = 0; wy[i].start = 1; wz[i].start = 0
                hx[i].start = 1; hy[i].start = 0; hz[i].start = 0
            elif o_heur[k] == "LHW": 
                lx[i].start = 1; ly[i].start = 0; lz[i].start = 0
                wx[i].start = 0; wy[i].start = 0; wz[i].start = 1
                hx[i].start = 0; hy[i].start = 1; hz[i].start = 0

           
            print(lx[i].start)
            #start cannot take souble value, I guess only binary variables can be started 
           
            print(x[i].start)

            model.getVarByName("x_%i" % (i)).start = int(pos_heur[k].split(',')[0])
            model.getVarByName("y_%i" % (i)).start = int(pos_heur[k].split(',')[1])
            model.getVarByName("z_%i" % (i)).start = int(pos_heur[k].split(',')[2])
            
            
            model.getVarByName("xr_%i" % (i)).start = x[i].start + lx[i].start * p[i] + wx[i].start * q[i] + hx[i].start * r[i]
            model.getVarByName("yr_%i" % (i)).start = y[i].start + ly[i].start * p[i] + wy[i].start * q[i] + hy[i].start * r[i]
            model.getVarByName("zr_%i" % (i)).start = z[i].start + lz[i].start * p[i] + wz[i].start * q[i] + hz[i].start * r[i]
            
            if z[i].start == 0:
                g[i].start = 1
                
            else:
                g[i].start = 0


            for k in I:
                if k in itemindex and i!=k:
                    if x[k].start + p[k] * lx[k].start + q[k] * wx[k].start + r[k] * hx[k].start <= x[i].start:
                        a[i, k].start = 1; a[k, i].start = 0
                    else:
                        a[i, k].start = 0; a[k, i].start = 1                    
                    if y[k].start + p[k] * ly[k].start + q[k] * wy[k].start + r[k] * hy[k].start <= y[i].start:
                        b[i, k].start = 1; b[k, i].start = 0
                    else:
                        b[i, k].start = 0; b[k, i].start = 1
                    if z[k].start + p[k] * lz[k].start + q[k] * wz[k].start + r[k] * hz[k].start <= z[i].start:
                        c[i, k].start = 1; c[k, i].start = 0
                    else:
                        c[i, k].start = 0; c[k, i].start = 1


                    if x[i].start <= x[k].start:
                        n1[i, k].start = 1; n1[k, i].start = 0
                    else:
                        n1[i, k].start = 0; n1[k, i].start = 1                    
                    if y[i].start <= y[k].start:
                        n2[i, k].start = 1; n2[k, i].start = 0
                    else:
                        n2[i, k].start = 0; n2[k, i].start = 1
                    if xr[i].start <= xr[k].start:
                        n3[i, k].start = 1; n3[k, i].start = 0
                    else:
                        n3[i, k].start = 0; n3[k, i].start = 1                    
                    if yr[i].start <= yr[k].start:
                        n4[i, k].start = 1; n4[k, i].start = 0
                    else:
                        n4[i, k].start = 0; n4[k, i].start = 1


                    if z[i].start == zr[k].start:
                        h[i,k].start = 0
                    else:
                        h[i,k].start = 1
                    

                    if a[i, k].start + a[k, i].start + b[i, k].start + b[k, i].start >= 1:
                        o[i,k].start = 0
                    else:
                        o[i,k].start = 1


                    if h[i,k].start + o[i,k].start == 0:
                        sk[i,k].start = 1
                    else:
                        sk[i,k].start = 0


                    if (sk[i, k].start == 1) and (n1[i, k].start + n2[i, k].start >= 1):
                        vs[i,k,0].start = 0
                    else:
                        vs[i,k,0].start = 1
                    if (sk[i, k].start == 1) and (n2[i, k].start + n3[i, k].start >= 1):
                        vs[i,k,1].start = 0
                    else:
                        vs[i,k,1].start = 1
                    if (sk[i, k].start == 1) and (n3[i, k].start + n4[i, k].start >= 1):
                        vs[i,k,2].start = 0
                    else:
                        vs[i,k,2].start = 1
                    if (sk[i, k].start == 1) and (n1[i, k].start + n4[i, k].start >= 1):
                        vs[i,k,3].start = 0
                    else:
                        vs[i,k,3].start = 1

                    
                    s1[i,k].start = abs(zr[k].start-z[i].start)


                    if zr[k].start >= z[i].start:
                        s2[i,k].start = 1
                    else:
                        s2[i,k].start = 0    



        else:
            s[i].start = 0   




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
