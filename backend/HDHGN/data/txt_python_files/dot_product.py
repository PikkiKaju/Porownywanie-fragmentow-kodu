'''Dot product'''

from operator import (mul)


# dotProduct :: Num a => [a] -> [a] -> Either String a
def dotProduct(xs):
    '''Either the dot product of xs and ys,
       or a string reporting unmatched vector sizes.
    '''
    return lambda ys: Left('vector sizes differ') if (
        len(xs) != len(ys)
    ) else Right(sum(map(mul, xs, ys)))


# TEST ----------------------------------------------------
# main :: IO ()
def main():
    '''Dot product of other vectors with [1, 3, -5]'''

    print(
        fTable(main.__doc__ + ':\n')(str)(str)(
            compose(
                either(append('Undefined :: '))(str)
            )(dotProduct([1, 3, -5]))
        )([[4, -2, -1, 8], [4, -2], [4, 2, -1], [4, -2, -1]])
    )