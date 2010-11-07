i = 2
maxpn = 10001
pn = 0
while pn < maxpn:
    isprime = True
    for t in range(2,int(i**0.5)+1):
        if i % t == 0:
            isprime = False
            break
    if isprime:
        pn += 1
        print i
    i += 1
#print i