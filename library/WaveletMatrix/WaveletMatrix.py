import bisect
import itertools as it
import heapq
from collections import deque

class WaveletMatrix:

    def __init__(self, A, n=30):
        # matrix構築
        self.bit_length = n
        self.matrix = [[0]*(len(A)+1) for _ in range(self.bit_length)]# 元の並び順での各数値各桁のbit
        self.matrix_zero = [[0]*(len(A)+1) for _ in range(self.bit_length)]# 元の並び順での各数値各桁のbit
        self.zero_count = [len(A)] * self.bit_length # 各bit桁のゼロの数
        self.start_dict = {}
        self.count_dict = {}


        kari = 1<<(self.bit_length-1)
        zero = []
        one = []
        # 各桁ごとにbitが0 or 1で並び替え(0同士、1同士の順序は維持)
        for x, a in enumerate(A, start=1):
            if a&kari:
                one.append((x,a))
                self.zero_count[0]-=1
                self.matrix[0][x]=1
            else:
                self.matrix_zero[0][x]=1
                zero.append((x,a))
            if a in self.count_dict:
                self.count_dict[a] += 1
            else:
                self.count_dict[a] = 1

        kari >>=1
        for y in range(1, self.bit_length):
            temp_zero = []
            temp_one = []
            c=1
            for x, a in zero:
                if a&kari:
                    temp_one.append((x,a))
                    self.zero_count[y]-=1
                    self.matrix[y][c]=1
                else:
                    self.matrix_zero[y][c]=1
                    temp_zero.append((x,a))
                c+=1

            for x, a in one:
                if a&kari:
                    temp_one.append((x,a))
                    self.zero_count[y]-=1
                    self.matrix[y][c]=1
                else:
                    self.matrix_zero[y][c]=1
                    temp_zero.append((x,a))
                c+=1

            zero = temp_zero[:]
            one = temp_one[:]
            kari >>=1

        # 基数ソート後の並び順を取得
        c = 0
        for x,a in zero:
            if a not in self.start_dict:
                self.start_dict[a] = c
            c+=1
        for x,a in one:
            if a not in self.start_dict:
                self.start_dict[a] = c
            c+=1

        # # 累積
        for i in range(self.bit_length):
            self.matrix[i] = list(it.accumulate(self.matrix[i]))
            self.matrix_zero[i] = list(it.accumulate(self.matrix_zero[i]))


    # indexは終端(半開区間)
    # 先頭からindex(開区間)までにvalueが何個あるかを取得
    def rank(self, index, value):
        if value not in self.start_dict: # 最初に与えられたAに存在しないときは0を返す
            return None
        # rank
        kari = 1<<(self.bit_length-1)
        for i in range(self.bit_length):
            if value&kari: # 検索する値の指定のbitが1なら
                index = self.zero_count[i] + (self.matrix[i][index])
            else:
                index = index - self.matrix[i][index]

            kari >>=1
        return (index - self.start_dict[value])
    
    # indexは終端(半開区間)
    # num個目のvalueがどのindexにあったかを取得
    # ナイーブにやるなら値をキーとした配列にindex入れてそれで取る
    def select(self, value, num):
        if value not in self.start_dict: # 最初に与えられたAに存在しないときは0を返す
            return None

        if self.count_dict[value] < num: # 元の配列に存在してる数を超えた場合
            return None

        index = self.start_dict[value] + num # start_dictは0
        kari = 1
        for i in range(self.bit_length-1, -1, -1):
            if value&kari: # 検索する値の指定のbitが1なら
                one_num = index -self.zero_count[i]
                index = bisect.bisect_left(self.matrix[i], one_num)

            else:
                index = bisect.bisect_left(self.matrix_zero[i], index)
            kari <<=1
        return index
        # zeroの数の累積和を持っているがこれを1の累積和の行列で代替したい


    # lからrの中でk番目に小さい値
    def quantile(self, l, r, k):
        out = 0
        if (r-l) < k or k<=0:
            return (None, None)

        # print(zero_num, one_num)
        for i in range(self.bit_length):
            out <<= 1
            # rは開区間, lは閉区間
            zero_num = self.matrix_zero[i][r] - self.matrix_zero[i][l]
            one_num = self.matrix[i][r] - self.matrix[i][l]

            if zero_num < k <= zero_num+one_num: # bitが1なら
                out += 1
                l = self.zero_count[i] + (self.matrix[i][l])
                r = self.zero_count[i] + (self.matrix[i][r])
                k -= zero_num

            else:
                l = l - self.matrix[i][l]
                r = r - self.matrix[i][r]

            # print(out,k)
            # print(f"l:{l}, r:{r}, zero_num:{zero_num}, one_num:{one_num}")

        # out:K番目に小さい値
        # num:何個目のoutか (selectでindexを取ってくる時に使う)
        num = l-self.start_dict[out] + k
        return out, num

    # lからrの中で出現頻度の多い数値を上位k個取り出す、種類が足りない場合は途中で打ち切る
    def topk(self, org_l, org_r, k):
        q1 = [((org_r-org_l), org_l, 0)]

        for i in range(self.bit_length):
            q2 = []
            while q1:
                haba, l, num = q1.pop()
                r = haba + l
                num <<= 1
                # rは開区間, lは閉区間
                zero_num = self.matrix_zero[i][r] - self.matrix_zero[i][l]
                one_num = self.matrix[i][r] - self.matrix[i][l]
                if zero_num != 0:
                    r1 = self.matrix_zero[i][r]
                    l1 = self.matrix_zero[i][l]
                    if i == (self.bit_length-1):
                        heapq.heappush(q2, (-1*(r1-l1), num))
                    else:
                        q2.append((r1-l1, l1, num))

                if one_num != 0:
                    r2 = self.zero_count[i] + self.matrix[i][r]
                    l2 = self.zero_count[i] + self.matrix[i][l]
                    if i == (self.bit_length-1):
                        heapq.heappush(q2, (-1*(r2-l2), num+1))
                    else:
                        q2.append((r2-l2, l2, num+1))
            q1 = q2
        out = []
        c = 0
        
        while q1:
            if k<=0:
                break
            haba, num = heapq.heappop(q1)
            out.append((num, haba*-1))
            k -= 1
        # while q1:
        #     haba, num = heapq.heappop(q1)
        #     out.append((num, min(haba*-1, k)))
        #     if haba*-1 >= k: 
        #         break
        #     else:
        #         k += haba
        return out