res = []
i = 2
while i < 1000000:
    if i == sum([int(c)**5 for c in str(i)]):
        print i
        res.append(i)
    i += 1

print res, sum(res)