#include <stdio.h>

void insertion_sort(int*, const size_t); 

void insertion_sort(int *a, const size_t n) {
	for(size_t i = 1; i < n; ++i) {
		int key = a[i];
		size_t j = i;
		while( (j > 0) && (key < a[j - 1]) ) {
			a[j] = a[j - 1];
			--j;
		}
		a[j] = key;
	}
}
