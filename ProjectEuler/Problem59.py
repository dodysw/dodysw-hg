cipher = file("cipher1.txt").read()
encoded_cipher = [int(c) for c in cipher.split(',')]
common_words = [" the ", " and "]
highest_scored = [0, None]
for k1 in xrange(97,123):
    for k2 in xrange(97,123):
        for k3 in xrange(97,123):
            key = (k1, k2, k3)
            score = 0
            for w in common_words:
                decoded_cipher = ''.join([chr(encoded_cipher[i] ^ key[i % 3]) for i in xrange(len(encoded_cipher))])
                score += decoded_cipher.count(w)
            if score > highest_scored[0]:
                highest_scored = [score, key]
score, key = highest_scored
print "%c%c%c" % key
print ''.join([chr(encoded_cipher[i] ^ key[i % 3]) for i in xrange(len(encoded_cipher))])
print "Total Ascii:", sum([encoded_cipher[i] ^ key[i % 3] for i in xrange(len(encoded_cipher))])