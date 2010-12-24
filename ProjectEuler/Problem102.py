"""
http://www.ecse.rpi.edu/Homepages/wrf/Research/Short_Notes/pnpoly.html
int pnpoly(int nvert, float *vertx, float *verty, float testx, float testy)
{
  int i, j, c = 0;
  for (i = 0, j = nvert-1; i < nvert; j = i++) {
    if ( ((verty[i]>testy) != (verty[j]>testy)) &&
	 (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
       c = !c;
  }
  return c;
}

Argument	Meaning
nvert 	Number of vertices in the polygon. Whether to repeat the first vertex at the end is discussed below.
vertx, verty 	Arrays containing the x- and y-coordinates of the polygon's vertices.
testx, testy	X- and y-coordinate of the test point. 
"""

triangles = [map(int, line.split(",")) for line in file("triangles.txt").read().split()]

def is_point_in_poly(vertx, verty, testx, testy):
    i = c = 0
    nvert = len(vertx)
    j = nvert - 1
    while i < nvert:
        if ( ((verty[i] > testy) != (verty[j] > testy)) and 
            (testx < (vertx[j] - vertx[i]) * (testy - verty[i]) / float (verty[j]-verty[i]) + vertx[i]) ):
            c = not c
        j = i
        i += 1
    return c

total = 0
for triangle in triangles:
    x1,y1,x2,y2,x3,y3 = triangle
    if is_point_in_poly([x1,x2,x3],[y1,y2,y3],0,0):
        print triangle, "is inside"
        total += 1
    else:
        print triangle, "is not"
        
print "ans:", total
    