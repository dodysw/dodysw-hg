import time

def try1():
    #look for pattern of repeating number, starting from 1 digit, 2 digit, etc, found:
    #a digit: repeat each 4 n
    #2 digit: repeat each 20 n
    #3 digit: repeat each 100 n
    #4 digit each 500n
    #then uses wolfram alpha to come up with Possible closed form:
    # a_n = 4 x 5^(n-1) (for all terms given)
    #http://www.wolframalpha.com/input/?i=4%2C20%2C100%2C500
    #then it's easy to predict the last 10 digit of 2^n:
    last_digits = 10
    repeating_each = 4*5**(last_digits-1)
    
    #2**7830457's 10 last digit is...
    last_ten_equal_to = 2**(7830457 % repeating_each)
    
    #finally
    print str(28433*last_ten_equal_to+1)[-10:]
    
    #however, getting the first pattern of numbers is no easy feat, is there other way?

def try2():
    #Wohooo!
    print (28433*2**(7830457 % (4*5**9))+1) % 10**10

def from_forum():
    #from people in projecteuler forum, first post by lassevk,  agggh they always found simpler way!
    #but my algorithm is faster!
    print (28433 * 2**7830457 + 1) % 10000000000 

st = time.time()
print try2()
print time.time() - st