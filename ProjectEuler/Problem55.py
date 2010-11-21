def is_palindromic(n):
    if n < 10:
        return True
    s = str(n)
    return s == s[::-1]

def sum_with_its_reverse(n):
    return n + int(str(n)[::-1])

lycrel_count = 0
for n in xrange(10000):
    for trial in xrange(50):
        n = sum_with_its_reverse(n)
        if is_palindromic(n):
            break
    else:
        lycrel_count += 1

print lycrel_count