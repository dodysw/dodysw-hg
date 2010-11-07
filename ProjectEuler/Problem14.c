/*
n = 999999
maxchain = 0
while n > 0:
    chain_count = 0
    i = n
    while i > 1:
        if i % 2 == 0:
            i /= 2
        else:
            i = 3*i + 1
        chain_count += 1
    if chain_count > maxchain:
        print n, '-', chain_count
        maxchain = chain_count
    n -= 1
*/

#include <stdio.h>

int main() {
    int n = 999999;
    int maxchain = 0;
    while (n > 0) {
        int chain_count = 0;
        long i = n;
        while (i > 1) {
            if (i % 2 == 0) {
                i /= 2;
            }
            else {
                i = 3*i + 1;
            }
            chain_count++;
        }
        if (chain_count > maxchain) {
            printf("%d - %d\n", n, chain_count);
            maxchain = chain_count;
        }
        n--;
    }
}