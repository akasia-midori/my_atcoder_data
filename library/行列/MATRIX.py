def prod_func(a,b):
    # 累乗部分がデカすぎてメモリが死んじゃう時など
    # 例えば10^18回移動して到達できる場所はどこ？というときはこれで良い
    if a*b > 0:
        return 1
    return 0
def add_func(a,b):
    return a+b

class MATRIX:
    def __init__(self, prod_func, add_func):
        self.prod_func = prod_func
        self.add_func = add_func
        
    def dot(self, A,B):
        if len(A[0]) != len(B):
            return None
        out = [[0] * len(B[0]) for _ in range(len(A))]
        for ay in range(len(A)):
            for bx in range(len(B[0])):
                sums = 0
                for ax in range(len(A[0])):
                    sums += self.prod_func(A[ay][ax], B[ax][bx])
                out[ay][bx] = sums
        return out

    def sum(self, A,B):
        if not(len(A) == len(B) and len(A[0]) == len(B[0])):
            return None
        out = []
        for ay in range(len(A)):
            temp = []
            for ax in range(len(A[0])):
                temp.append(self.add_func(A[ay][ax], B[ay][ax]))
            out.append(temp)
        return out

    def prod(self, A,B):
        if not(len(A) == len(B) and len(A[0]) == len(B[0])):
            return None
        out = []
        for ay in range(len(A)):
            temp = []
            for ax in range(len(A[0])):
                temp.append(self.prod_func(A[ay][ax], B[ay][ax]))
            out.append(temp)
        return out

    # 正方行列AをN乗する。
    def ruijou(self, A, N):
        out = [[0] * len(A) for _ in range(len(A))]
        for i in range(len(A)):
            out[i][i] = 1

        while N:
            if N%2==1:
                out = self.dot(out, A)
            A = self.dot(A,A)
            N//=2
        return out
