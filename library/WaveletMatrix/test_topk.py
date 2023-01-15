from random import randint
from collections import Counter
for _ in range(100):
    N = 10**3
    A = [randint(1,100) for _ in range(N)]
    WM = WaveletMatrix(A)

    for i in range(100):
        l = randint(0,N-1)
        r = randint(l+1,N)
        k = randint(1, r-l)
        C = Counter(A[l:r])
        B = sorted([(v,-1*kk) for kk, v in C.most_common()], reverse=True)
        C = [v[1]*-1 for v in B]
        out = WM.topk(l,r,k)
        oo = [o[0] for o in out]

        flg = False
        for b,o in zip(C[:k], oo):
            if b != o:
                flg = True
                break
        if flg:
            print("Not same")    
            break