#include "random_testing_units.h"




int main()
{
    float **floatpage;
    int i;
    int j;

    i = 0;
    j = 0;
    floatpage = create_random_float_arrays(10, 10, 10);
    while (floatpage[i])
    {
        j = 0;
        while (j < 10)
        {
            printf("%f ", floatpage[i][j]);
            j++;
        }
        i++;
        printf("\n");
    }
    return (0);
}
