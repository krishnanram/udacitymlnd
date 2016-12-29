import math

def permutations(string,length):
    yield ''
    for i, d in enumerate(string):
        for perm in permutations(string[:i] + string[i+1:], length):
            yield d + perm


def combinations(string,length):
    yield ''
    for i, d in enumerate(string):
        for comb in combinations(string[i + 1:],length):
            yield d + comb


def stirling(n):
    # http://en.wikipedia.org/wiki/Stirling%27s_approximation
    return math.sqrt(2 * math.pi * n) * (n / math.e) ** n


def nPr(n, r):
    return (stirling(n) / stirling(n - r) if n > 20 else
            math.factorial(n) / math.factorial(n - r))


def ncr(n, r):
    return (stirling(n) / stirling(r) / stirling(n - r) if n > 20 else
            math.factorial(n) / math.factorial(r) / math.factorial(n - r))

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def nPrUtil(n,r, flag) :
    permL = [perm for perm in permutations(n, r)]
    for perm in permL:
        if flag == 1 :
            if len(perm) == r:
                yield perm
        else :
            if len(perm) <= r:
                yield perm


def nCrUtil(n,r, flag) :
    combL = [comb for comb in combinations(n, r)]
    for comb in combL:

        if flag == 1:
            if len(comb) == r:
             yield comb
        else :
            if len(comb) <= r:
                yield comb


if __name__ == '__main__':

    inputS = "1234"
    r=3
    flag = 1

    print "********* Testing Permuations ***************"
    permL = [perm for perm in nPrUtil(inputS, r, flag)]
    print "total:", len(permL), "nPr:", nPr(len(inputS), r)
    print permL


    print "********* Testing Combinations ***************"
    combL = [comb for comb in nCrUtil(inputS, r, flag)]
    print "total:", len(combL), "nCr:",nCr( len(inputS), r)
    print combL