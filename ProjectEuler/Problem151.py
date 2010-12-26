from random import randint, seed

def cut(anum):
    global A
    if A[anum] == 0:
        cut(anum-1)
    A[anum] -= 1
    A[anum+1] += 2

def pick(anum):
    global A
    if A[anum] == 0:
        cut(anum-1)
    A[anum] -= 1

def try1():
    """Random method
    """
    #initialize
    A = [0,1,0,0,0,0]    
    # after firstjob
    A = [0,0,1,1,1,1]
    #using random method
    seed()
    trial_count = 1500000
    single_sheet = 0
    for trial in xrange(trial_count):
        A = [0,0,1,1,1,1]
        for i in xrange(14):
            envelope = []
            for n in xrange(6):
                if A[n] == 0:
                    continue
                envelope += [n]*A[n]
            paper_count = len(envelope)
            if paper_count == 1:
                single_sheet += 1
                random_paper = 0
            else:    
                #random pick
                random_paper = randint(0,paper_count-1)
            if envelope[random_paper] != 5:
                for u in xrange(envelope[random_paper],5):
                    cut(u)
    #         pick(5)
            if A[5] == 0:
                cut(4)
            A[5] -= 1

    print "ans:%0.6f" % (single_sheet/float(trial_count))
    
total_singles = 0
total_trial = 0

def try2():
    """search tree method
    """
    single_sheet = 0
    
    def cut_paper(A, anum):
        if A[anum] == 0:
            cut_paper(A, anum-1)
        A[anum] -= 1
        A[anum+1] += 2

    def recur(A, level=14, single_sheet=0, mult=1):
        global total_singles, total_trial
        indent = " "*(15-level)
        print indent,"L", level, A, "Single!" if level > 0 and sum(A) == 1 else "", "Mult", mult    
        if level == 0:
            print indent,"Picked single %d times (Mult %d)" % (single_sheet, mult)
            total_singles += mult*single_sheet
            total_trial += mult

            return single_sheet

        if sum(A) == 1:
            single_sheet += 1

        #try picking each paper, and tally its single sheet count
        for papersize in xrange(0, 6):
            if A[papersize] == 0: continue
            print indent,"Picking A%d" % papersize
            m = A[papersize] # if given papersize has >1, then the number of singles found should be multiplied by this
#             if papersize == 5:
#                 m -= 1
            Atry = A[:]
            if papersize != 5:
                for u in xrange(papersize,5):
                    cut_paper(Atry, u)
            if Atry[5] == 0:
                cut_paper(Atry, 4)
            Atry[5] -= 1
            recur(Atry, level-1, single_sheet, m*mult)
    
    A = [0,0,1,1,1,1]
#     A = [0,0,0,1,1,1]
    recur(A,14)
    print "ans:%0.6f" % (total_singles/float(total_trial))
    print total_singles, total_trial
    
try2()