#####segfunc#####
def segfunc(x, y):
    return x+y
#################

#####ide_ele#####
ide_ele = 0
#################

class SegTree:
    """
    init(init_val, ide_ele): 配列init_valで初期化 O(N)
    update(k, x): k番目の値をxに更新 O(logN)
    query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
    """
    def __init__(self, init_val, segfunc, ide_ele):
        """
        init_val: 配列の初期値
        segfunc: 区間にしたい操作
        ide_ele: 単位元
        n: 要素数
        num: n以上の最小の2のべき乗
        tree: セグメント木(1-index)
        """
        self.n = len(init_val)
        self.bitlen = (self.n - 1).bit_length()
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1 << self.bitlen
        self.tree = [ide_ele] * 2 * self.num
        # 配列の値を葉にセット
        for i in range(self.n):
            self.tree[self.num + i] = init_val[i]
        # 構築していく
        for i in range(self.num - 1, 0, -1):
            self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, k, x):
        """
        k番目の値をxに更新
        k: index(0-index)
        x: update value
        """
        k += self.num
        self.tree[k] = x
        while k > 1:
            self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
            k >>= 1

    def query(self, l, r):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
        res = self.ide_ele

        l += self.num
        r += self.num
        while l < r:
            if l & 1:
                res = self.segfunc(res, self.tree[l])
                l += 1
            if r & 1:
                res = self.segfunc(res, self.tree[r - 1])
            l >>= 1
            r >>= 1
        return res

    # (累積がx以上のうち最も小さい値, その時のindex)を得る
    # x以上のものが無ければ None を返す
    def ge(self, x):
        bits = 1
        base = self.ide_ele
        if self.tree[1] < x:
            return (None, None)

        for i in range(self.bitlen):
            bits <<= 1
            ne = self.segfunc(self.tree[bits], base) #左側のノードまでの累積を計算
            if ne < x:
                base = ne # 右側のノードに進むなら左側までの累積を保存
                bits += 1
        ind = bits - self.num
        v = self.tree[bits]
        return ind, v

    # (累積がxを超える値のうち最も小さい値, その時のindex)を得る
    # xを超えるものが無ければ None を返す
    def gt(self, x): return self.ge(x+1)

    # (累積がx以下のうち最も大きい値, その時のindex)を得る
    # x以下のものが無ければ None を返す
    def le(self, x):
        if self.tree[self.num] > x:
            return (None, None)

        if self.tree[1] < x:
            return self.n-1, self.tree[self.num-self.n-1]

        bits = 1
        base = self.ide_ele

        for i in range(self.bitlen):
            bits <<= 1
            ne = self.segfunc(self.tree[bits], base) #左側のノードまでの累積を計算
            if ne < x:
                base = ne # 右側のノードに進むなら左側までの累積を保存
                bits += 1
        ind = bits - self.num
        v = self.tree[bits]

        if self.segfunc(base, v) == x:
            return ind, v

        return ind-1, self.tree[self.num - (ind-1)]  

    def lt(self, x): return self.le(x-1)


from collections import defaultdict

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n
        self.all_groups = n # 現状のグループ数

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
            return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x
        self.all_groups -= 1

    def size(self, x):
        return -self.parents[self.find(x)]

    def same(self, x, y):
        return self.find(x) == self.find(y)

    # 計算量 N 
    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def group_count(self):
        return len(self.roots())

    def all_group_members(self):
        group_members = defaultdict(list)
        for member in range(self.n):
            group_members[self.find(member)].append(member)
        return group_members

    def __str__(self):
        return ''.join(f'{r}: {m}' for r, m in self.all_group_members().items())
# N頂点の木を作成する
import random
def make_tree(N):
    # ノードN個の木を作成
    G =  {i:[] for i in range(N)}
    uf = UnionFind(N)
    use_cost = True
    out_list = []

    # 連結になるまでループ
    while uf.size(0) != N:
        A = random.randint(1, N)
        B = random.randint(1, N)
        if A==B:
            continue

        # 連結でなければ追加
        A,B  =sorted([A,B])
        if not uf.same(A-1, B-1):
            uf.union(A-1,B-1)
            # costはいらない
            G[A-1].append(B-1)
            G[B-1].append(A-1)
            out_list.append((A, B))

    # 1-indexdのリストを作る
    cost = [random.randint(1, 100) for _ in range(N)]
    return out_list, cost

def naive(N, data, cost_list, queries):
    NODE = N
    maps = {i:[] for i in range(NODE)}
    for a,b in data:
        maps[a-1].append(b-1)
        maps[b-1].append(a-1)

    def query(N, start, end, maps, cost_list):
        from collections import deque
        reached = [0] * N ## 1つ前のノードを持たせると微妙に遅くなるのでやめよう
        deq = deque([[start, 0]])

        while deq:

            # node = deq.pop() #DFS
            node, cost = deq.popleft() #BFS
            cost += cost_list[node]

            if node == end:
                return cost
            reached[node] = -1

            for next_node in maps[node]:
                # 訪問済み判定
                if reached[next_node] == -1:
                    continue
                
                reached[next_node] = -1
                deq.append([next_node,cost])

    out = []
    for start, end in queries:
        out.append(query(N, start, end, maps, cost_list))
    return out

def solve(N, data, cost_list, queries):
    maps = {i:[] for i in range(N)}
    for a,b in data:
        maps[a-1].append(b-1)
        maps[b-1].append(a-1)
    hld = HLD(N, maps, cost_list)

    out = []
    for start, end in queries:
        out.append(hld.query(start, end))
    return out



from tqdm import tqdm
import random 

for i in tqdm(range(10000)):
    N = random.randint(10, 20)
    data, cost_list = make_tree(N)
    queries = [(random.randint(0,N-1), random.randint(0,N-1)) for _ in range(5)]
    
    out1 = naive(N, data, cost_list, queries)
    out2 = solve(N, data, cost_list, queries)
    flg = False
    for o1, o2 in zip(out1, out2):
        if o1!=o2:
            flg = True
            print("break")
            break
    if flg:
        break