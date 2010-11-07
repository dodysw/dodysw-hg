coins = [200,100,50,20,10,5,2,1]
target = 200
combination = []
stack = []

def calc(lvl=0, prev_total=0):
    if lvl >= len(coins):
        return
    for m in xrange((target/coins[lvl])+1):
        total = prev_total + m*coins[lvl]
        if total < target:
            #print "Under target", lvl, m, total
            stack.append(m)
            calc(lvl+1, total)
            stack.pop()
        elif total == target:
            print "Found", stack + [m]
            combination.append(stack + [m])
        elif total > target:
            #print "Too much", lvl, m, total
            break        

calc()

print len(combination)