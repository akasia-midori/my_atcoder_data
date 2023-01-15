import random 
from collections import defaultdict
from collections import Counter
A = [random.randint(10, 10**9) for _ in range(2*10**5)]
WM = WaveletMatrix(A)
Co = Counter(A)
dicts = defaultdict(int)
count = 1

for k,v in Co.items():
    for vv in range(1,v+1):
        i = WM.select(value=k, num=vv)
        if A[i-1] != k:
            print("not same")
            break