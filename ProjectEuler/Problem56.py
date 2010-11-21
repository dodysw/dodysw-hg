max_digital_sum = 0
for a in xrange(100):
    for b in xrange(100):
        max_digital_sum = max(sum([int(n) for n in str(pow(a,b))]), max_digital_sum)
print max_digital_sum