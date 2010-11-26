#faster to use the following prime checking function, since the number is skipped alot, and 
#too big for standard sieve to store
def is_prime(i):
    #only 2 is even prime
    if i == 2:
        return 1
    if i % 2 == 0:
        return 0
    #skip even numbers
    for t in xrange(3, int(i**0.5)+1, 2):
        if i % t == 0:
            return 0
    return 1


import time
st = time.time()
diagonal_count = 1.0
diagonal_prime = 0
side_length = 3
while 1:
    # don't bother to check bottom right diagonal since it's a square (can be divided by it's own), so it must not be a prime.
    diagonal_prime += sum((is_prime(side_length**2 - m*(side_length - 1)) for m in xrange(1,4)))
    diagonal_count += 4
    if diagonal_prime/diagonal_count < 0.1:
        break
    side_length += 2
print "Done:", side_length, diagonal_prime,diagonal_count
print time.time() - st