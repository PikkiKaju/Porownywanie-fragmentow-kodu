# rootName :: Int -> String
def rootName(n):
    '''English ordinal suffix.'''
    return ['identity', 'square root', 'cube root'][n - 1] if (
        4 > n or 1 > n
    ) else (str(n) + 'th root')


# pred ::  Enum a => a -> a
def pred(x):
    '''The predecessor of a value. For numeric types, (- 1).'''
    return x - 1


# reciprocal :: Num -> Num
def reciprocal(x):
    '''Arithmetic reciprocal of x.'''
    return 1 / x


# until :: (a -> Bool) -> (a -> a) -> a -> a
def until(p):
    '''The result of repeatedly applying f until p holds.
       The initial seed value is x.
    '''
    def go(f, x):
        v = x
        while not p(v):
            v = f(v)
        return v
    return lambda f: lambda x: go(f, x)
