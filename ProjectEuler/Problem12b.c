#include <stdio.h>;
#include <math.h>;

int main() {
    int n = 1;
    int i = 1;
    while (1) {
        
        //don't perform test if it's not even (optimization)
        if (i % 2 == 0) {
        
            int divcount = 0;        
            int t;
            int t_limit = sqrt(i);
            for (t = 1; t <= t_limit; t++) {
                if (i % t == 0)
                    divcount += 2;
            }
            if (i == t_limit*t_limit)
                divcount--;
            
            if (divcount > 150) {
                printf("%d - %d\n", i, divcount);
            }
            
            if (divcount > 500) {
                printf("Found: %d - divcount %d\n", i, divcount);
                break;
            }
        }
        
        n++;
        i += n;
        
    }
}