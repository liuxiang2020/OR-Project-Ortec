Sets
i box number / 1*3 /

Alias (i, k )
;
set arc(i,k) / 1.2, 1.3, 2.3 /;

Parameters
L /587 /
W /233 /
H /220 /

p(i) length of box i
/
1  108
2  110
3  92
/
q(i) width  of box i
/
1  76
2  43
3  81
/
r(i) height of box i
/
1  30
2  25
3  55
/
;


Binary Variables
s(i) Whether box i is packed or not

lx(i) Whether the length of box i is parallel to the X axis
ly(i) Whether the length of box i is parallel to the Y axis
lz(i) Whether the length of box i is parallel to the Z axis
wx(i) Whether the width of box i is parallel to the X axis
wy(i) Whether the width of box i is parallel to the Y axis
wz(i) Whether the width of box i is parallel to the Z axis
hx(i) Whether the height of box i is parallel to the X axis
hy(i) Whether the height of box i is parallel to the Y axis
hz(i) Whether the height of box i is parallel to the Z axis

a(i,k) Box i is on the left of box k
b(i,k) Box i is on the right of box k
c(i,k) Box i is on the behind of box k
d(i,k) Box i is on the front of box k
e(i,k) Box i is on the below of box k
f(i,k) Box i is on the above of box k
;
Positive Variables x(i), y(i), z(i) continuous variables indicating the x y and z coordinates of the front-left-bottom corner of box i
;
Variables zet objective function
;


Equations
Objective             Our objective is maximizing the volume of boxes packed
Nonoverlapleft(i,k)   Const 2
Nonoverlapright(i,k)  Const 3
Nonoverlapbehind(i,k) Const 4
Nonoverlapfront(i,k)  Const 5
Nonoverlapbelow(i,k)  Const 6
Nonoverlapabove(i,k)  Const 7
Orientation(i,k)      Const 8 i should be on one orientation of
Boxfitslength(i)      Const 29
Boxfitswidth(i)       Const 30
Boxfitsheight(i)      Const 31
LenghtParallel(i)     Const 14
WidthParallel(i)      Const 15
HeightParallel(i)     Const 16
xParallel(i)          Const 17
yParallel(i)          Const 18
zParallel(i)          Const 19
trial
;

Objective..                 zet =e= L*W*H - sum(i,p(i)*q(i)*r(i)*s(i)) ;
Nonoverlapleft(i,k)..       x(i)+p(i)*lx(i)+q(i)*wx(i)+r(i)*hx(i) =l= x(k)+(1 - a(i, k)) * 999;
Nonoverlapright(i,k)..      x(k)+p(k)*lx(k)+q(k)*wx(k)+r(k)*hx(k) =l= x(i)+(1 - b(i, k)) * 999;
Nonoverlapbehind(i,k)..     y(i)+p(i)*ly(i)+q(i)*wy(i)+r(i)*hy(i) =l= y(k)+(1 - c(i, k)) * 999;
Nonoverlapfront(i,k)..      y(k)+p(k)*ly(k)+q(k)*wy(k)+r(k)*hy(k) =l= y(i)+(1 - d(i, k)) * 999;
Nonoverlapbelow(i,k)..      z(i)+p(i)*lz(i)+q(i)*wz(i)+r(i)*hz(i) =l= z(k)+(1 - e(i, k)) * 999;
Nonoverlapabove(i,k)..      z(k)+p(k)*lz(k)+q(k)*wz(k)+r(k)*hz(k) =l= z(i)+(1 - f(i, k)) * 999;
Orientation(i,k)..          a(i, k) + b(i, k) + c(i, k) + d(i, k) + e(i, k) + f(i, k) =g= s(i) + s(k) - 1;
Boxfitslength(i)..          x(i)+p(i)*lx(i)+q(i)*wx(i)+r(i)*hx(i) =l= L+(1 - s(i)) * 999;
Boxfitswidth(i)..           y(i)+p(i)*ly(i)+q(i)*wy(i)+r(i)*hy(i) =l= W+(1 - s(i)) * 999;
Boxfitsheight(i)..          z(i)+p(i)*lz(i)+q(i)*wz(i)+r(i)*hz(i) =l= H+(1 - s(i)) * 999;

LenghtParallel(i)..         lx(i) + ly(i) + lz(i) =e= 1;
WidthParallel(i)..          wx(i) + wy(i) + wz(i) =e= 1;
HeightParallel(i)..         hx(i) + hy(i) + hz(i) =e= 1;
xParallel(i)..              lx(i) + wx(i) + hx(i) =e= 1;
yParallel(i)..              ly(i) + wy(i) + hy(i) =e= 1;
zParallel(i)..              lz(i) + wz(i) + hz(i) =e= 1;
trial..                          s('1') =e= 1;

model Untitled_1 /all/ ;
Untitled_1.optfile=1;
$onecho >cplex.opt
rhsrng all
objrng all
$offecho
option optca=0;
option optcr=0;
solve Untitled_1 using MIP minimizing zet;
