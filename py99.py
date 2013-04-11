import collections
import itertools


def py1(xs):
    return xs[-1]

assert py1([1,2,3]) == 3



def py2(xs):
    return xs[-2]

assert py2([1,2,3]) == 2



def py3(xs, k):
    return xs[k-1]

assert py3([1,2,3], 2) == 2



def py4(xs):
    return len(xs)

assert py4([])    == 0
assert py4([1])   == 1
assert py4([1,2]) == 2



def py5(xs):
    return xs[::-1]

assert tuple(py5([]))    == tuple([])
assert tuple(py5([1]))   == tuple([1])
assert tuple(py5([1,2])) == tuple([2,1])



def py6(xs):
    return xs[::-1] == xs

assert py6([])      is True
assert py6([1])     is True
assert py6([1,1])   is True
assert py6([1,1,1]) is True
assert py6([1,2,1]) is True
assert py6([1,2])   is False
assert py6([1,2,3]) is False



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



def py7(xss):
    for xs in xss:
        if isinstance(xs, collections.Iterable):
            for x in py7(xs):
                yield x
        else:
            yield xs

assert list(py7([]))                          == []
assert list(py7([1,2,[3,[4,[[5],6]],7],[8]])) == [1,2,3,4,5,6,7,8]



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



def py10(xss):
    return map(lambda xs: (len(xs), xs[0]),  py9(xss))


assert py10([4])           == [(1,4)]
assert py10([4,4])         == [(2,4)]
assert py10([4,4,3])       == [(2,4),(1,3)]
assert py10([4,4,3,4,4,4]) == [(2,4),(1,3),(3,4)]


print "All fine!"
