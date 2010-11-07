def is_plaindromic_slow(s):
    s_len = len(s)
    if s_len < 2:
        return True
    for i in xrange(len(s)/2):
        if s[i] != s[-1-i]:
            return False
    return True

total_plaindromics = 0
for i in xrange(1000000):
    if is_plaindromic(str(i)) and is_plaindromic(bin(i)[2:]):
        print i, bin(i)[2:]
        total_plaindromics += i
        
print "Total", total_plaindromics
#872187