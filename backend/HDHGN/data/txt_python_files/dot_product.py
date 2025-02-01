
from operator import (mul)

def dotProduct(xs):
    '''Either the dot product of xs and ys,
       or a string reporting unmatched vector sizes.
    '''
    return lambda ys: Left('vector sizes differ') if (
        len(xs) != len(ys)
    ) else Right(sum(map(mul, xs, ys)))

