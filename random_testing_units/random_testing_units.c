#include "random_testing_units.h"

void     delete_page(void **page) // free 2d array
{
    size_t i;

    i = 0;
    while (page[i] != NULL)
    {
        free(page[i]);
        page[i] = NULL;
        i++;
    }
    free(page);
    page = NULL;
}

static uint32_t    triple32(uint32_t n) /*might use it later for better randomiztion*/
{
    n ^= n >> 0x11;
    n *= 0xed5ad4bbu;
    n ^= n >> 0x0b;
    n *= 0xac4c1b51u;
    n ^= n >> 0x0f;
    n *= 0x31848babu;
    n ^= n >> 0x0e;
    return (n);
}


float       *create_random_float_array(const size_t size, size_t modulo)
{
    float           *arr;
    size_t          i;
    static size_t   shift = 0; /* shift for setting the seed randomly between calls */

    i = 0;
    if (0 == size || 0 == modulo)
        return (NULL);
    arr = malloc(size * sizeof(float));
    if (NULL == arr)
        return (NULL);
    srand(time(0) & shift);
    while (i < size)
    {
        arr[i] = (((float)rand() / (float)RAND_MAX)) * 2 * modulo - modulo;
        i++;
    }
    shift += rand(); /* randomly shifting the seed */
    return (arr);
}

float       **create_random_float_arrays(const size_t num_of_arrays, const size_t size_of_each, size_t modulo)
{
    float   **page;
    size_t  i;

    i = 0;
    page = NULL;
    page = malloc(sizeof(float *) * (num_of_arrays + 1)); /* page is null-terminated */
    if (NULL == page)
        return (NULL);
    while (i < num_of_arrays)
    {
        page[i] = create_random_float_array(size_of_each, modulo);
        if (NULL == page[i])
        {
            delete_page((void **)page);
            return (NULL);
        }
        i++;
    }
    page[i] = NULL;
    return (page);
}

char        *create_random_string(const char *charset, const size_t size)
{
    char            *random;
    size_t          i;
    size_t          circle;
    static size_t   shift = 12; /* shift for setting the seed randomly between calls */

    random = malloc((size + 1) * sizeof(char));
    if (NULL == charset || 0 == size || NULL == random)
        return (NULL);
    circle = strlen(charset) - 1;
    i = 0;
    srand(time(0) & shift);
    while (i < size)
    {
        random[i] = charset[rand() % circle];
        i++;
    }
    random[i] = 0;
    shift += rand(); /* randomly shifting the seed */
    return (random);
}

char        **create_random_strings(size_t num_of_strings, const char *charset, const size_t size)
{
    char    **page;
    size_t  i;

    i = 0;
    page = NULL;
    page = malloc(sizeof(char *) * (num_of_strings + 1)); /*page is null-terminated*/
    if (NULL == page)
        return (NULL);
    while (i < num_of_strings)
    {
        page[i] = create_random_string(charset, size);
        if (NULL == page[i])
        {
            delete_page((void **)page);
            return (NULL);
        }
        i++;
    }
    page[i] = NULL;
    return (page);
}

int         *create_random_int_array(size_t length, size_t modulo)
{
    int             *arr;
    size_t          i;
    static size_t   shift = 1; 

    i = 0;
    if (length == 0)
        return (NULL);
    arr = malloc(sizeof(int) * length);
    if (NULL == arr)
        return (NULL);
    srand(time(0) * shift);
    while (i < length)
    {
        arr[i] = (int)(((float)rand() / (float)RAND_MAX) * 2 * modulo - modulo);
        i++;
    }
    shift += rand();
    return (arr);
}

int         **create_random_int_arrays(size_t n, size_t size_of_each, size_t modulo)
{
    int     **page;
    size_t  i;

    i = 0;
    page = malloc(sizeof(int *) * (n + 1)); /*page is null-terminated*/
    if (NULL == page)
        return (NULL);
    while (i < n)
    {
        page[i] = create_random_int_array(size_of_each, modulo);
        if (NULL == page[i])
        {
            delete_page((void **)page);
            return (NULL);
        }
        i++;
    }
    page[i] = NULL;
    return (page);
}

