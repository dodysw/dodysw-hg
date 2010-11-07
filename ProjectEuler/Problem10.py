i = 2
maxpn = 2000000
pn = 0
allpn = []
while i < maxpn:
    isprime = True
    for t in range(2,int(i**0.5)+1):
        if i % t == 0:
            isprime = False
            break
    if isprime:
        pn += 1
        allpn.append(i)
    i += 1
print sum(allpn)