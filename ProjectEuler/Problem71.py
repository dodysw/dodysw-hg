"""
Target: left of 3/7. 3/7 is between 2/5 and 1/2. Based on stern brocot tree, we must go
LEFT, then RIGHT all the way through denomitor is 1000000
"""

#inspired by Pier at http://projecteuler.net/index.php?section=forum&id=73
#modified according to http://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree
def arbol(n1, d1, n2, d2):
    global limit
    while True:
        ad = d1+d2
        an = n1+n2
        if ad + d2 >= limit:
            return an,ad
        #LEFT after 3/7
        if an == 3 and ad == 7:
            n2, d2 = an, ad
        else:
            #then RIGHT all the way
            n1, d1 = an, ad
    return an


def try1():
    global limit
    limit = 1000000
    print arbol(2,5,1,2)
    #print arbol(0,1,1,1)

try1()