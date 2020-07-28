#include <assert.h>
#include <stdio.h>
#include "../../random_testing_units/random_testing_units.h"
#define MAX_TESTS 10

int		average_between_negatives(int *table, int length);

int		abn(int *table, int length)
{
	int i;
	int j;
	int n;
	int sum;

	i = 0;
	j = length - 1;
	sum = 0;
	n = 0;
	if (length <= 2 || NULL == table)
		return (-1);
	while (i < length)
	{
		if (table[i] < 0)
		{
			i++;
			break;
		}
		i++;
	}
	while (j > 0)
	{
		if (table[j] < 0)
		{
			j--;
			break;
		}
		j--;
	}
	if (i == j)
		return (table[i]);
	if (0 == j || length - 1 == i || i > j)
		return (-1);
	while (i <= j)
	{
		sum += table[i];
		i++;
		n++;
	}
	return (sum / n);
}

int     main(void)
{
	int n;
	int **arr;
	int i;
	int j;
	int expected;
	int yours;
	int errors;

	errors = 0;
	j = 0;
	i = 0;
	n = 1;
	while (n <= MAX_TESTS)
	{
		i = 0;
		arr = create_random_int_arrays(100, n, n * n);
		
		while (NULL != arr[i] || 0 == n)
		{
			expected = abn(arr[i], n);
			yours = average_between_negatives(arr[i], n);
			if (yours != expected)
			{
				errors += 1;
				j = 0;
				printf("test%d failed:(\n", n);
				printf("input array:");
				while (j < n)
				{
					printf("%d ", arr[i][j]);
					j++;
				}
				printf("\n");
				printf("expected:%d\nyours:%d\n", expected, yours);
			}
			i++;
		}
		delete_page((void **)arr);
		n++;
	}
	printf("total errors:%d\n", errors);
    return (errors);
}
