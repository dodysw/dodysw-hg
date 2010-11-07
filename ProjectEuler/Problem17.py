"""
If the numbers 1 to 5 are written out in words: one, two, three, four, five, 
then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?

NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) 
contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. 
The use of "and" when writing out numbers is in compliance with British usage.

"""

ten = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
ten1 = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens = ["", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

def num2words(n):
    n = int(n)
    out = []
    if n >= 1000:
        out.append(ten[int(n / 1000)-1])
        out.append("thousand")
        n -= int(n / 1000) * 1000
    if n >= 100: 
        out.append(ten[int(n / 100)-1])
        out.append("hundred")
        n -= int(n / 100) * 100

    if len(out) > 0 and n > 0:
        out.append("and")

    if n >= 10:
        if n >= 20:
            out.append(tens[int(n / 10)-1])
            n -= int(n / 10) * 10
        else:
            out.append(ten1[(n-10)])
            n = 0    
    if n > 0:
        out.append(ten[n-1])
    if n == 0 and len(out) == 0:
        out.append("zero")
    return " ".join(out)

#for i in xrange(1,1001):
#    print i, num2words(i)
    
print sum([len(num2words(i).replace(" ","")) for i in xrange(1,1001)])
    
    