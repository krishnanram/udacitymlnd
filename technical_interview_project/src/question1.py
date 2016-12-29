# Question 1
# Given two strings s and t, determine whether some anagram of t is a substring of s.
# For example: if s = "udacity" and t = "ad", then the function returns True.
# Your function definition should look like: question1(s, t) and return a boolean True or False.


from collections import Counter

def is_anagram_best_sol(s, p) :
    res = []
    pCounter = Counter(p)
    sCounter = Counter(s[:len(p) - 1])
    for i in range(len(p) - 1, len(s)):
        sCounter[s[i]] += 1  # include a new char in sliding window
        if sCounter == pCounter:
            return True
        sCounter[s[i - len(p) + 1]] -= 1  # decrease the count of oldest char in the window
        if sCounter[s[i - len(p) + 1]] == 0:
            del sCounter[s[i - len(p) + 1]]  # remove the char from window if count is 0

    return False

def lookup(str,c) :
    pos = 0
    for s in str :
        if c == s :
            return (pos,True)
        pos += 1
    return (pos, False)

def optimized_is_anagram(s1,s2) :

    last_match_pos = 0
    i = 0

    while ( i < len(s2)) :
        rolling_window_str = s1[:last_match_pos]+ s1[last_match_pos:]
        (last_match_pos, match) = lookup(rolling_window_str, s2[i])
        i += 1

        if match == False :
            return False

    return True

def is_anagram(s1, s2):

    counter = Counter()
    for c in s1:
        counter[c] += 1

    for c in s2:
        counter[c] -= 1

    for c in s2 :
        if counter[c] != 0 :
            return False

    return True


if __name__ == '__main__':


    assert( is_anagram_best_sol("udacity", "ic") == True)
    assert( is_anagram_best_sol("udacity", "ty") == True)
    assert( is_anagram_best_sol("udacity", "ic") == True)



'''   Asymptotic Analysis
 = O(s1) + O(s2) + O(s2)
 = O(s1)

'''



