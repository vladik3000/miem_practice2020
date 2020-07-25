#include "random_testing_units.h"

static uint32_t    triple32(uint32_t n)
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
    float *arr;
    int i;
    static size_t shift = 1;

    i = 0;
    if (0 == size || 0 == modulo)
        return (NULL);
    arr = malloc(size * sizeof(float));
    if (NULL == arr)
        return (NULL);
    srand(time(0) + shift);
    while (i < size)
    {
        arr[i] = (((float)rand() / (float)RAND_MAX)) * 2 * modulo - modulo;
        i++;
    }
    shift += 111;
    return (arr);
}

float       **create_random_float_arrays(const size_t num_of_arrays, const size_t size_of_each, size_t modulo)
{
    float   **page;
    size_t  i;

    i = 0;
    page = NULL;
    page = malloc(sizeof(float *) * (num_of_arrays + 1)); // page is null-terminated
    if (NULL == page)
        return (NULL);
    while (i < num_of_arrays)
    {
        page[i] = create_random_float_array(size_of_each, modulo);
        if (NULL == page[i])
        {
            if (0 == i)
                return (NULL);
            else
            {
                while (i >= 0)
                {
                    free(page[i]);
                    page[i] = NULL;
                    i--;
                }
                return (NULL);
            }
        }
        i++;
    }
    page[i] = NULL;
    return (page);
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

char        *create_random_separated_string(const char *charset,
            const char *sepcharset, const int size)
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
        sublen = rand() % len - sublen;
        substr = create_random_string(charset, sublen);
        if (NULL == substr)
           return (NULL);
        strncat(random, substr, len - sublen);
        len -= sublen;
    }
    return (random);
}

char        **create_random_strings(size_t num_of_strings, const char *charset, const size_t size)
{
    char **page;
    size_t i;

    i = 0;
    page = NULL;
    page = malloc(sizeof(char *) * (num_of_strings + 1));
    if (NULL == page)
        return (NULL);

    while (i < num_of_strings)
    {
        page[i] = create_random_string(charset, size);
        if (NULL == page[i])
        {
            if (0 == i)
                return (NULL);
            else
            {
                while (i >= 0)
                {
                    free(page[i]);
                    page[i] = NULL;
                    i--;
                }
                return (NULL);
            }
        }
        i++;
    }
    page[i] = NULL;
    return (page);
}

void        delete_page(void **page)
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
     
