#include "random_testing_units.h"

float       *create_random_float_array(const size_t size, unsigned modulo)
{
    float *arr;
    int i;

    i = 0;
    if (0 == size || 0 == modulo)
        return (NULL);
    arr = malloc(size * sizeof(float));
    if (NULL == arr)
        return (NULL);
    srand(time(0));
    while (i < size)
    {
        arr[i] = (((float)rand() / (float)RAND_MAX)) * 2 * modulo - modulo;
        i++;
    }
    return (arr);
}

char        *create_random_string(const char *charset, const size_t size)
{
    char *random;
    int i;
    size_t circle;

    random = malloc((size + 1) * sizeof(char));
    if (NULL == charset || 0 == size || NULL == random)
        return (NULL);
    circle = strlen(charset) - 1;
    i = 0;
    srand(time(0));
    while (i < size)
    {
        random[i] = charset[rand() % circle];
        i++;
    }
    random[i] = 0;
    return (random);
}

char        *create_random_separated_string(const char *charset, const char *sepcharset, const int size)
{
    char    *random;
    char    *substr;
    size_t  num_of_splits;
    size_t  sublen;
    size_t  len;

    random = malloc((size + 1) * sizeof(char));
    if (NULL == random)
        return (NULL);
    memset(random, 0, (size + 1) * sizeof(char));
    sublen = 0;
    srand(time(0));
    len = size;
    while (len != 0)
    {
        sublen = rand() % size - sublen;
        substr = create_random_string(charset, sublen);
        if (NULL == substr)
           return (NULL);
    }
    return (random);
}


     
