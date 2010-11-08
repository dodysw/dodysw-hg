"""
Take the number 192 and multiply it by each of 1, 2, and 3:

    192 x 1 = 192
    192 x 2 = 384
    192 x 3 = 576

By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?

"""

def is_pandigital(s):
    if '0' in s:
        return False
    return len(s) == len(dict.fromkeys(list(s)))
    
results = []
#y || y*2 must be less than 987654321, so y must be < 5 digits
for y in xrange(1,10000):
    digits = ''
    for m in xrange(1,10):
        digits += str(y * m)
        if len(digits) == 9 and is_pandigital(digits):
            results.append(digits)
            break
        elif len(digits) > 9:
            break    
            
print results
print max(results)