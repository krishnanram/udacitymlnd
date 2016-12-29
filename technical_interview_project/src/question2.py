
#Question 2
#Given a string a, find the longest palindromic substring contained in a.
# Your function definition should look like question2(a), and return a string.
#
from collections import Counter
from permCom import *

def revert(string):
    return string[::-1]

def palindromic(s1):

    res=[]
    counter = Counter()
    oneCounter = Counter()
    twoCounter = Counter()

    for c in s1:
        counter[c] += 1

    minOneCount = 0
    size=0

    for c in counter :
        if counter[c] !=0 :
            lengthV = counter[c]/2
            rem = counter[c]%2
            if rem == 1 :
                oneCounter[c] = 1
                minOneCount = 1

            if lengthV > 0 :
                twoCounter[c] += 1

            size = size + lengthV*2

    size += minOneCount
    inS = ""
    for s in twoCounter :
        inS = inS + str(s)

    permCom = nPrUtil(inS, len(inS),  1)
    s = permCom.next()
    for o in oneCounter :
        res.append(s + o + revert(s))

    return (size, res)


if __name__ == '__main__':

    (maxSize, res) = palindromic("zded")
    print "longest palindromic substring is {:d} and possible permuataions {:d}".format( maxSize, len(res))
    print res
    assert(palindromic("zaabbc") == 3)



