class HLD:
    def __init__(self, N, maps, vals):
        # 帰りがけ
        self.sz = [0] * N
        self.G = [[] for _ in range(N)]
        self.ET_redict = {}
        reached = [-1] * N
        deq = [(0, -1, True)] # 一番最後のTrue, Falseで
        self.depth = [0] * N # LCA用の深さ

        while deq:
            start, end, preorder = deq.pop()
            # 行き
            if preorder:
                self.sz[start] = 1
                reached[start] = 0
                deq.append((end, start, False))
                maxd = 0
                for end in maps[start]:
                    if maxd < self.depth[end]:
                        maxd = self.depth[end]
                        
                    if reached[end] == 0:
                        continue
                    deq.append((end, start, True))
                self.depth[start] = maxd+1
            # 帰り
            else:
                if start == -1:
                    continue
                # ここで帰りがけに行いたい処理を書く
                self.sz[start] += self.sz[end]

                self.G[start].append(end)
                if len(self.G[start]) == 1:
                    continue

                if self.sz[end] > self.sz[self.G[start][0]]:
                    self.G[start][-1], self.G[start][0] = self.G[start][0], self.G[start][-1]


        # HLDに使用する各種値の取得
        # 帰りがけ
        self.in_list = [0] * N
        # self.out_list = [0] * N 
        self.top = [0] * N # 現在の頂点集合のTOP
        self.next = [-1] * N # 次の頂点集合への入口ノード
        t = 0
        ET_list = []

        deq = [0] # 一番最後のTrue, Falseで
        self.depth[0] = 1
        
        self.ET_redict = {} # 値更新用の辞書
        self.init_val = [0]*N

        while deq:
            v = deq.pop()
            # 行き
            self.in_list[v] = t
            t += 1
            ET_list.append(v)
            self.init_val[len(ET_list)-1] = vals[v]
            self.ET_redict[v] = len(ET_list)-1

            for i in range(len(self.G[v])-1, -1, -1):
                u = self.G[v][i]
                if u == self.G[v][0]:
                    self.top[u] = self.top[v]
                    self.next[u] = self.next[v]
                else:
                    self.top[u] = u
                    self.next[u] = v
                deq.append(u)

        self.tree = SegTree(self.init_val, segfunc, ide_ele)
   
    def LCA(self, start, end):
    # LCAを求める

        while True:
            # 1. startとendが含まれる頂点集合の根を取得する
            top_start = self.top[start]
            top_end = self.top[end]

            # 2. 同じだったらより根に近い方がLCAになっている
            if top_start == top_end:
                # 2
                if self.depth[start] > self.depth[end]:
                    LCA_node = end
                else:
                    LCA_node = start
                return LCA_node
            # 3. 異なっている場合、深い所の頂点集合から次の頂点集合へ移動させる
            else:
                if self.depth[self.top[start]] > self.depth[self.top[end]]:
                    start = self.next[start]

                else:
                    end = self.next[end]

    def part_query(self, LCA_node, end):
        sums = 0
        while self.top[LCA_node] != self.top[end]:
            sums += self.tree.query(self.in_list[self.top[end]], self.in_list[end]+1)
            end = self.next[end]

        sums += self.tree.query(self.in_list[LCA_node], self.in_list[end]+1)

        return sums
    
    def query(self, start, end):
        LCA_node = self.LCA(start, end)
        sums  = self.part_query(LCA_node, start)
        sums += self.part_query(LCA_node, end)
        sums -= self.part_query(LCA_node, LCA_node)
        return sums
    
    def update(self, node, value):
        # node番目のノードをvalueで更新
        self.tree.update(self.ET_redict[node], value)


edge_mode = True
NODE = N
P = [0] * NODE*2 # 辺とか頂点の値を格納
maps = {[] for _ in range(NODE*2)}
data = []
edge_dict = {}
num = N
for _ in range(N-1):
    u,v,c = mi()
    if (u,v) not in edge_dict:
        num+=1
        edge_dict[(u,v)] = num
        edge_dict[(v,c)] = num


    # 両端のノードから疑似ノード(辺)へ辺を張る    
    maps[u-1].append(num-1)
    maps[v-1].append(num-1)

    # 疑似ノード(辺)から両端のノードへ辺を張る
    maps[num-1].append(v-1)
    maps[num-1].append(u-1)

    # 辺の和の時
    if edge_mode:
        P[num-1] = c
    data.append((u,v))

hld = HLD(N*2, maps, P)