#include <stdio.h>

int generalizedPentagonal(int i) {
    //for n running over positive and negative integers: successively taking n = 1, -1, 2, -2, 3, -3, 4, -4,
    int n = (i+2)/2;
    if ((i % 2) != 0)
        n *= -1;
    //"generalized pentagonal numbers of the form 0.5*n(3n - 1)"
    return 0.5*n*(3*n-1);
}

long pcache[60000] = { 0 };
int pcachelen = 0;

long p(int k) {
    // printf("P called with %d\n", k);
    if (k < 0)
        return 0;

    if (pcachelen > k) {
        return pcache[k];
    }

    long total = 0;
    int sign = 1;
    int gp = 1;
    int i = 0;
    while ((k - gp) > 0) {
        //"The signs in the summation continue to alternate +, +, -, -, +, +, ..."
        sign = (((i+2)/2)  % 2 == 0) ? -1 : 1;
        gp = generalizedPentagonal(i);
        total += sign * (p(k - gp) % 1000000);
        i++;
    }
    pcache[k] = total; pcachelen++;
    return total;
}



int main() {
    //"By convention p(0) = 1, p(n) = 0 for n negative"
    pcache[0] = 1; pcachelen++;
    pcache[1] = 1; pcachelen++;
    int n = 0;
    long counts = 1;
    while (counts % 1000000 != 0) {
        n++;
        counts = p(n);
    }
    printf("ans:%d", n);
}
