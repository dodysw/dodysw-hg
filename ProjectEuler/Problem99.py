nums = []
for i,line in enumerate(file("base_exp.txt").read().split()):
    base, expon = map(int, line.split(","))
    expon /= 100000.0
    nums.append(base**expon)
    
print "ans:", nums.index(max(nums))+1