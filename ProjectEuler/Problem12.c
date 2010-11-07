#include <stdio.h>;

int main() {
    int n = 1;
    int i = 1;
    while (1) {
        
        //don't perform test if it's not even (optimization)
        if (i % 2 == 0) {
        
            int divcount = 0;        
            int t;
            int t_limit = i/2;
            for (t = 2; t <= t_limit; t++) {
                if (i % t == 0)
                    divcount++;
            }
            divcount += 2;
            
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