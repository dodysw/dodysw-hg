def isRepeating(needle, haystack):
    block_len = len(needle)
    if block_len > len(haystack)/2:
        return False

    repeating = True
    for pos in xrange(0, len(haystack), block_len):
        comparation = haystack[pos:pos + block_len]
        
        #stop if reach end of numbers
        if len(comparation) != len(candidate):
            break

        #print "C:%s vs %s - bl:%s - fraction:%s" % (candidate, comparation, block_len, haystack)
        if comparation != candidate:
            repeating = False
            break
            
    return repeating

longest_repeat = 0
for i in xrange(1,1000):
    fraction = str(10**10000/i)
    #print "Fraction:", fraction
    
    #repeat detector
    #try 1 char, compare to next value sets, if everything matched, we got a 
    is_repeating = False
    repeating_block = 0
    repeating_numbers = ''
    for pos in xrange(0,len(fraction)):
        is_repeating = False
        for block_len in xrange(1, len(fraction) - pos):
            #print "Pos/Block", pos, block_len
            candidate = fraction[pos:pos+block_len]
            # checking whether this candidate really being repeated all the way
            is_repeating = isRepeating(candidate, fraction[pos + block_len:])
            #print "%s vs %s, result %s" % (candidate, fraction[pos + block_len:], is_repeating)
            
            if is_repeating:
                repeating_block = block_len
                repeating_numbers = str(candidate)
                break
        if is_repeating:
            break
    
    if is_repeating and repeating_numbers != '0':
        print "%s 1/%s Repeat:%s %s (%s)" % (i, i, is_repeating, repeating_numbers, repeating_block)
        if repeating_block > longest_repeat:
            longest_repeat = repeating_block
            happened_at = i
        
print longest_repeat, happened_at