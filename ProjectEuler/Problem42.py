"""
The n^(th) term of the sequence of triangle numbers is given by, t_(n) = 0.5*n(n+1); so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t_(10). If the word value is a triangle number then we shall call the word a triangle word.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?
"""


def wordValue(w):
    return sum([ord(c)-64 for c in w])

#build around 100 triangle numbers
triangles = [0.5*n*(n+1) for n in xrange(1,101)]

triangle_word_count = 0
for word in file("words.txt").read().split(","):
    word = word.strip('"')
    if wordValue(word) in triangles:
        triangle_word_count += 1
print triangle_word_count