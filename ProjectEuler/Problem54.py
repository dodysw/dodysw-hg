"""
try1: convert hand into list of 3 element that express their rank.
1st element correspond to 10 major rule map a number between 1 and 10
2nd element correspond to a list of numbers that express rank within the same major rule. 
Python will correctly use this list to perform rank comparation.
"""
import math

def rankValue2(cards):
    #cards is string of 5 x 2 chars card code like 5H 6S 7S KD AC (6)
    is_flush = [suite for suite in "CDHS" if cards.count(suite) == 5]
    
    #test Royal Flush: Ten, Jack, Queen, King, Ace, in same suit. value 10.
    if is_flush and sum([1 for val in "TJQKA" if val+is_flush[0] in cards]) == 5:
        return [10,[]]

    #prepare variables that will be used multiple times in subsequent test
    vals = [cards[i] for i in xrange(0,12+1,3)]
    valsnum = []
    for val in vals:
        #   replace T,J,Q,K,A with 10,11,12,13,14
        for i,j in dict(T=10,J=11,Q=12,K=13,A=14).iteritems():
            if val == i:
                val = j
                break
        valsnum.append(int(val))
    valsnum.sort(reverse=True)
    #   setup list of unique values, with its number. e.g. [[4,10],[1,6]] for four 10 over 6.
    unique_values = [[valsnum.count(val),val] for val in dict.fromkeys(valsnum)]
    unique_values.sort(reverse=True)

    #test straight (5)
    max_straight = max(valsnum)
    is_straight = (reduce(lambda x,y:x*y, valsnum) == math.factorial(max_straight)/math.factorial(max_straight-5))
    # if ace and 2 exist, ace can be considered as "1" and form a straight. So I will check this directly.
    if not is_straight and valsnum == [14,5,4,3,2]:
        is_straight = True
        max_straight = 5
    
    #test straight flush (9)
    if is_straight and is_flush:
        return [9, unique_values]

    #test four of a kind (8)
    if len(unique_values) == 2 and unique_values[0][0] == 4:
        return [8, unique_values]

    #test full house (7)
    if len(unique_values) == 2 and unique_values[0][0] == 3:
        return [7, unique_values]

    #test flush (6)
    if is_flush:
        return [6, unique_values]

    #test straight (5)
    if is_straight:
        return [5, unique_values]

    #test three of a kind (4)
    if len(unique_values) == 3 and unique_values[0][0] == 3:
        return [4, unique_values]

    #test two pairs (3)
    if len(unique_values) == 3 and unique_values[0][0] == 2:
        return [3, unique_values]

    #test pair (2)
    if len(unique_values) == 4:
        return [2, unique_values]

    #high card
    return [1, unique_values]
 
player1win = 0
for line in file("poker.txt"):
    cards = line.split()
    player1win += 1 if rankValue2(' '.join(cards[0:5])) > rankValue2(' '.join(cards[5:10])) else 0

print player1win