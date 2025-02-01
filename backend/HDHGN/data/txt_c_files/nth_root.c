#include <stdio.h>
#include <float.h>

double pow_ (double x, int e) {
    int i;
    double r = 1;
    for (i = 0; i < e; i++) {
        r *= x;
    }
    return r;
}

double root (int n, double x) {
    double d, r = 1;
    if (!x) {
        return 0;
    }
    if (n < 1 || (x < 0 && !(n&1))) {
        return 0.0 / 0.0; /* NaN */
    }
    do {
        d = (x / pow_(r, n - 1) - r) / n;
        r += d;
    }
    while (d >= DBL_EPSILON * 10 || d <= -DBL_EPSILON * 10);
    return r;
}

