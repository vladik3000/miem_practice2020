#include <assert.h>
#include <stdio.h>

int     average_between_negatives(int *table, int length);





int     main(void)
{
    int answer;

    int arr[4] = {1, 2, 3, 4};
    answer = average_between_negatives(arr, 4);
    if (answer != -1)
    {
        printf("test1: error:\nexpected:%d\nyours:%d\n:(", -1, answer);
        return (0);
    }
    else
        printf("test1: good :)\n");
    return (0);
}
