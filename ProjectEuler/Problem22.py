"""
Using names.txt  (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.
For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938 x 53 = 49714.
What is the total of all the name scores in the file?
"""
names = [name.replace('"','') for name in file("names.txt").readlines()[0].split(",")]
names.sort()
total_score = 0
for i,name in enumerate(names):
    score = sum([ord(c)-64 for c in name]) * (i+1)
    #print i, name, score
    total_score += score
print total_score