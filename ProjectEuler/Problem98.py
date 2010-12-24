from time import time

st = time()

words = [i[1:-1] for i in file("words.txt").read().split(",")]
    
from itertools import groupby, combinations
#remove words that can't form anagram
word_charsort = map(sorted, words)
anagramable = filter(lambda w: word_charsort.count(sorted(w)) > 1, words)

print "generating"

#build squares up to max characters, group by its length
squares_len = {}
for sqlen in xrange(1, max(map(len, anagramable)) + 1):
    max_square = int(10**(sqlen/2.0))
    min_square = 10**(sqlen//2)
    squares_len[sqlen] = set([i*i for i in xrange(min_square,max_square+1)])

print "Starting"    

anagram_pair_square = set()

#group by its anagram
stringid = lambda w: sorted(w)
anagramable.sort(key=stringid)
for k,w in groupby(anagramable, stringid):
    #it's possible to have > 1 pair, thus let's create combination of them
    for w1,w2 in combinations(w, 2):
        wordlen = len(w2)
        mapseq = [None] * wordlen
        #generate mapping sequence
        same_letter = None
        for i in xrange(wordlen):
            wcount = w1.count(w2[i])
            assert wcount <= 2
            if wcount == 2:
                #CENTRE->RECENT -> 410523 or 452123
                #record store position for later swapping                
                if same_letter is None:
                    #use the first found letter pos
                    same_letter = i
                    pos = w1.index(w2[i])
                else:
                    #use the second found letter pos
                    pos = w1.index(w2[i], mapseq[same_letter])
                    same_letter = same_letter, i
            else:
                pos = w1.index(w2[i])
            mapseq[i] = pos
        #now try to map square number whose pair is also square
        #note: the problem requires that the square has no same digit, and cannot have leading zeroes
        
        mapseqs = [mapseq]
        if same_letter is not None:
            mapseq2 = mapseq[:]
            mapseq2[same_letter[0]], mapseq2[same_letter[1]] = mapseq2[same_letter[1]], mapseq2[same_letter[0]] 
            mapseqs.append(mapseq2)

        for m in mapseqs:
            #try every squares with the same len
            for sq in squares_len[wordlen]:
                sq_str = str(sq)
                if len(set(sorted(sq_str))) != len(sq_str):
                    continue
                #map sq to mapseq
                ana_str = ''.join([sq_str[i] for i in m])
                if ana_str[0] == "0":
                    continue
                anagram_num = int(ana_str)
                if anagram_num not in squares_len[wordlen]:
                    continue
                    
                print w1, sq, w2, anagram_num
                anagram_pair_square.add(anagram_num)
            
            
print "ans:", max(anagram_pair_square)
#18769
print time() - st