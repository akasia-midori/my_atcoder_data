#テストコード
from random import randint
N = 10**3
A = [randint(1,100) for _ in range(N)]
WM = WaveletMatrix(A)

for i in range(100):
    l = randint(0,N-1)
    r = randint(l+1,N)
    k = randint(1, r-l)
    B = sorted(A[l:r])
    if B[k-1] != WM.quantile(l,r,k)[0]:
        print("not same")
        break