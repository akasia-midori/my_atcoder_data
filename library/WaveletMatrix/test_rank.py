import random 
from collections import defaultdict
from collections import Counter

A = [random.randint(10, 10**9) for _ in range(2*10**5)]
WM = WaveletMatrix(A)
dicts = defaultdict(int)
for i,a in enumerate(A, start=1):
    dicts[a] += 1
    for k, v in dicts.items():
        if WM.rank(index=i, value=k) != v:
            print(dicts, k, v, WM.rank(index=i, value=k))
            print("not same")