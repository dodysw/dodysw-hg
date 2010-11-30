number_of_matches_needed = 5
permute_count = {}
permute_id = {}
n = 1
last_digits_len = 1
while True:
    s = list(str(n*n*n))
    #we need to wait until the digit length has increased to make sure that the permutation is exactly 5
    if len(s) > last_digits_len:
        #get all with 5 count
        matches = sorted([k for k,v in permute_count.items() if v == number_of_matches_needed])
        if matches:
            print "ans:",permute_id[matches[0]]
            break
        else:
            permute_count = {}
            permute_id = {}

    s.sort()
    s = ''.join(s)
    permute_id.setdefault(s, n*n*n)
    permute_count.setdefault(s, 0)
    permute_count[s] += 1
    n += 1
    last_digits_len = len(s)