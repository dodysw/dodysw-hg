#include <stdio.h>

long limit = 100000;
long arbolcount = 0;

//inspired by Pier at http://projecteuler.net/index.php?section=forum&id=73
//modified according to http://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree
void arbol(long n1, long d1, long n2, long d2) {
    long ad = d1+d2;
    if (ad > limit)
        return;
    long an = n1+n2;
    //go through tree (left side) until denominator is 12k
    arbol(n1, d1, an, ad);
    //go through tree (right side) until denominator is 12k
    arbol(an, ad, n2, d2);
    arbolcount++;
}


int main() {
    arbol(0,1,1,1);
    printf("ans:%ld\n", arbolcount);
    
}
