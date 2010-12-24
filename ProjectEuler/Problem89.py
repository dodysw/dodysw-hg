"""
I = 1
V = 5
X = 10
L = 50
C = 100
D = 500
M = 1000
MMMMDCLXXII

Hahaha, working on google nexus s competition....
50 50 47,4 21 17 = Grasmarkt 120, Brussel, Belgium (BE)
60 10 11,24 56 17 = Simkonkato 2, Helsinki, Finland (FI)
12 6 17,15 2 40 = Rue du Cherif, N'Djamena, Chad (TD)
*
52 13 47,21 0 44 = Rondo Romana Dmowskiego, Warszawa Poland (PL)
3 8 20,101 41 13 = Jalan Damansara, Kuala Lumpur, Malaysia (MY)
/
30 3 45,31 14 50 = Ramsis Sq. Egypt (EG)
35 41 22,139 41 30 = Tokyo Shinjuku, Japan (JP)
-18 8 30,178 25 27 = Marchartur St, Suva, Fiji (FJ)
-35 16 55,149 7 43 = Versnon Cir, Canberra, Australia (AU)
-10 25 18,105 40 41 = Chrismas island (CX)
-34 52 60,-56 10 = Comando, Montevideo, Uruguay (UY)
bit.ly/ejjucy

Rules:
    Numerals must be arranged in descending order of size.
   1. Only I, X, and C can be used as the leading numeral in part of a subtractive pair.
   2. I can only be placed before V and X.
   3. X can only be placed before L and C.
   4. C can only be placed before D and M.
MCCCCCCVI -> MDCVI
XIIIIII -> XVI
DCCCCXXXVIIII -> 
"""

from time import time
st = time()

romvals = dict(I=1, V=5, X=10, L=50, C=100, D=500, M=1000)
def roman2dec(long_roman):
    lr_len = len(long_roman)
    total = i = 0
    while i < lr_len:
        char = long_roman[i]
        charval = romvals[char]
        if char in "IXC" and i+1 < lr_len:
            #look ahead for any larger chars
            for j in xrange(i+1,lr_len+1):        
                is_ending = (j == lr_len)
                if is_ending or (long_roman[j] != char):
                    sign = -1 if not is_ending and romvals[long_roman[j]] > charval else 1
                    total += sign*(j-i)*charval
                    i = j
                    break
        else:
            total += charval
            i += 1
    return total

short_conv = dict(
    C=["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"],
    X=["","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"],
    I=["","I","II","III","IV","V","VI","VII","VIII","IX"]
    )

def dec2roman(n):
    out = ""
    M,n = divmod(n, 1000)
    out += "M"*M
    C,n = divmod(n, 100)
    out += short_conv["C"][C]
    X,I = divmod(n, 10)
    out += short_conv["X"][X]
    out += short_conv["I"][I]
    return out

# print dec2roman(1606)
# 1/0

romans = file("roman.txt").read().split()
saving = 0
for long_roman in romans:
    diff = len(long_roman) - len(dec2roman(roman2dec(long_roman)))
    saving += diff
    
print "ans:", saving
#743
print time() - st