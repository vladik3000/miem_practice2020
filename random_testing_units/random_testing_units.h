#ifndef RANDOM_TESTING_UNITS_H

#define RANDOM_TESTING_UNITS_H

#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <stdio.h>

float       *create_random_float_array(const size_t size, size_t modulo);
float       **create_random_float_arrays(const size_t num_of_arrays,
            const size_t size_of_each, size_t modulo);
char        *create_random_string(const char *charset, const size_t size);
char        *create_random_separated_string(const char *charset,
            const char *sepcharset, const int size);
char        **create_random_strings(size_t num_of_strings, const char *charset,
            const size_t size);
int         *create_random_int_array(size_t length, size_t modulo);
int         **create_random_int_arrays(size_t n, size_t size_of_each, size_t modulo);
void        delete_page(void **page);

#endif
