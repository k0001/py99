import collections
import itertools

################################################################################

def py1(xs):
    return xs[-1]

assert py1([1,2,3]) == 3

################################################################################

def py2(xs):
    return xs[-2]

assert py2([1,2,3]) == 2

################################################################################

def py3(xs, k):
    return xs[k-1]

assert py3([1,2,3], 2) == 2

################################################################################

def py4(xs):
    return len(xs)

assert py4([])    == 0
assert py4([1])   == 1
assert py4([1,2]) == 2

################################################################################

def py5(xs):
    return xs[::-1]

assert list(py5([]))    == []
assert list(py5([1]))   == [1]
assert list(py5([1,2])) == [2,1]

################################################################################

def py6(xs):
    return xs[::-1] == xs

assert py6([])      is True
assert py6([1])     is True
assert py6([1,1])   is True
assert py6([1,1,1]) is True
assert py6([1,2,1]) is True
assert py6([1,2])   is False
assert py6([1,2,3]) is False

################################################################################

def py6a(xs):
    for i in range(len(xs) // 2):
        if xs[i] != xs[-(i+1)]:
            return False
    return True

assert py6a([])      is True
assert py6a([1])     is True
assert py6a([1,1])   is True
assert py6a([1,1,1]) is True
assert py6a([1,2,1]) is True
assert py6a([1,2])   is False
assert py6a([1,2,3]) is False

################################################################################

def py7(xss):
    for xs in xss:
        if isinstance(xs, collections.Iterable):
            for x in py7(xs):
                yield x
        else:
            yield xs

assert list(py7([]))                          == []
assert list(py7([1,2,[3,[4,[[5],6]],7],[8]])) == [1,2,3,4,5,6,7,8]

################################################################################

def py8(xs): # i don't like this highly imperative solution
    it = iter(xs)
    while True:
        x = next(it)
        yield x
        it = itertools.dropwhile(lambda y: y == x, it)

assert list(py8([]))          == []
assert list(py8([1]))         == [1]
assert list(py8([1,1]))       == [1]
assert list(py8([1,1,2]))     == [1,2]
assert list(py8([1,1,2,3]))   == [1,2,3]
assert list(py8([1,1,2,3,3])) == [1,2,3]

################################################################################

def py9(xs): # super ugly
    d = collections.deque()
    for x in xs:
        if len(d) == 0 or d[-1] == x:
            d.append(x)
        else:
            yield list(d)
            d.clear()
            d.append(x)
    if len(d) > 0:
        yield list(d)

assert list(py9([]))        == []
assert list(py9([1]))       == [[1]]
assert list(py9([1,1]))     == [[1,1]]
assert list(py9([1,1,2]))   == [[1,1],[2]]
assert list(py9([1,1,2,2])) == [[1,1],[2,2]]
assert list(py9([1,1,2,2])) == [[1,1],[2,2]]

################################################################################

def py10(xss):
    return map(lambda xs: (len(xs), xs[0]),  py9(xss))

assert py10([4])           == [(1,4)]
assert py10([4,4])         == [(2,4)]
assert py10([4,4,3])       == [(2,4),(1,3)]
assert py10([4,4,3,4,4,4]) == [(2,4),(1,3),(3,4)]

################################################################################

def py11(xss):
    def k(xs):
        if len(xs) == 1: return xs[0]
        else:            return (len(xs), xs[0])
    return map(k, py9(xss))

assert py11([4])           == [4]
assert py11([4,4])         == [(2,4)]
assert py11([4,4,3])       == [(2,4),3]
assert py11([4,4,3,4,4,4]) == [(2,4),3,(3,4)]

################################################################################

# Here, xs = py11(ys). If the original child elements of ys were tuples,
# then py12 doesn't work as expected.
def py12(xs):
    for x in xs:
        if isinstance(x, tuple):
            for _i in xrange(x[0]):
                yield x[1]
        else:
            yield x

assert list(py12([4]))             == [4]
assert list(py12([(2,4)]))         == [4,4]
assert list(py12([(2,4),3]))       == [4,4,3]
assert list(py12([(2,4),3,(3,4)])) == [4,4,3,4,4,4]

################################################################################

def py13(xs):
    it = iter(xs)
    x = it.next()
    count = 1
    for i in it:
        if i == x:       count += 1
        else:
            yield (x if count == 1 else (count,x))
            x = i; count = 1
    yield (x if count == 1 else (count,x))

assert list(py13([4]))           == [4]
assert list(py13([4,4]))         == [(2,4)]
assert list(py13([4,4,3]))       == [(2,4),3]
assert list(py13([4,4,3,4,4,4])) == [(2,4),3,(3,4)]

################################################################################

def py14(xs):
    for x in xs:
        yield x; yield x

assert list(py14([]))    == []
assert list(py14([1]))   == [1,1]
assert list(py14([1,1])) == [1,1,1,1]
assert list(py14([1,2])) == [1,1,2,2]

################################################################################

def py15(xs, n):
    for x in xs:
        for i in xrange(n):
            yield x

assert list(py15([],0))    == []
assert list(py15([],2))    == []
assert list(py15([1],0))   == []
assert list(py15([1],1))   == [1]
assert list(py15([1],2))   == [1,1]
assert list(py15([1,2],0)) == []
assert list(py15([1,2],1)) == [1,2]
assert list(py15([1,2],2)) == [1,1,2,2]

################################################################################

def py16(xs, n):
    i = n
    for x in xs:
        if i == 1:
            i = n
        else:
            yield x
            i -= 1

assert list(py16([], 0))      == []
assert list(py16([], 1))      == []
assert list(py16([1], 0))     == [1]
assert list(py16([1], 1))     == []
assert list(py16([1], 2))     == [1]
assert list(py16([1,2], 0))   == [1,2]
assert list(py16([1,2], 1))   == []
assert list(py16([1,2], 2))   == [1]
assert list(py16([1,2], 3))   == [1,2]
assert list(py16([1,2,3], 2)) == [1,3]

################################################################################

def py17(xs, n):
    return (xs[:n], xs[n:])

assert py17([], 0)    == ([],[])
assert py17([], 1)    == ([],[])
assert py17([1], 0)   == ([],[1])
assert py17([1], 1)   == ([1],[])
assert py17([1,2], 0) == ([],[1,2])
assert py17([1,2], 1) == ([1],[2])
assert py17([1,2], 2) == ([1,2],[])
assert py17([1,2], 3) == ([1,2],[])

################################################################################

def py18(xs, i, k):
    if i < 1 or k < i:
        return []
    return xs[i-1:k]

assert py18([], 0, 0)  == []
assert py18([], 0, 1)  == []
assert py18([], 1, 0)  == []
assert py18([], 1, 1)  == []
assert py18([3], 0, 0) == []
assert py18([3], 0, 1) == []
assert py18([3], 1, 0) == []
assert py18([3], 1, 1) == [3]
assert py18([3], 1, 2) == [3]
assert py18([3,4], 1, 2) == [3,4]
assert py18([3,4], 1, 3) == [3,4]
assert py18([3,4], 0, 0) == []

################################################################################

def py19(xs, n):
    return xs[n:] + xs[:n]

assert py19([],0)       == []
assert py19([],1)       == []
assert py19([1],0)      == [1]
assert py19([1],1)      == [1]
assert py19([1,2],1)    == [2,1]
assert py19([1,2],-1)   == [2,1]
assert py19([1,2,3],1)  == [2,3,1]
assert py19([1,2,3],2)  == [3,1,2]
assert py19([1,2,3],-1) == [3,1,2]
assert py19([1,2,3],-2) == [2,3,1]

################################################################################

def py20(xs, n):
    return (xs[n-1], xs[:n-1] + xs[n:])

assert py20([1], 1)   == (1,[])
assert py20([1,2], 1) == (1,[2])
assert py20([1,2], 2) == (2,[1])

################################################################################

print "All fine!"

