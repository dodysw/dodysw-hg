bank_charge = 0.5
line = raw_input().split()
withdraw, balance = int(line[0]), float(line[1])
if withdraw % 5 == 0 and (withdraw+bank_charge) <= balance:
    balance -= withdraw+bank_charge
print "%0.2f" % balance