# ABC140-D Face Produces Unhappiness
問題URL:
<a href=https://atcoder.jp/contests/abc140/tasks/abc140_d>
https://atcoder.jp/contests/abc140/tasks/abc140_d
</a>

### 問題文
>東西一列に N 人の人が並んでいます。  
各人の状態を表す長さ N の文字列 S が与えられます。   
西から i 番目の人は、文字列 S の i 文字目が L ならば西を、  
R ならば東を向いています。
どの人も、目の前の人が自分と同じ方向を向いていれば幸福です。   
ただし、目の前に人が居ない場合、幸福ではありません。  
あなたは、以下の操作を 0 回以上 K 回以下の好きな回数だけ行います。

>操作: 1 ≤ l ≤ r ≤ N を満たす整数 l,r を選ぶ。  
西から l,l+1,...,r 番目の人の列を 180 度回転する。  
すなわち、i=0,1,...,r−l について、  
西から l+i 番目の人は操作後には西から r−i 番目に移動し、  
元々西を向いていれば東を、東を向いていれば西を向く。

>幸福である人は最大で何人にできるでしょうか。

### 制約  
><section>
<li><var>N</var> は <var>1 ≤ N ≤ 10^5</var> を満たす整数である。</li>
<li><var>K</var> は <var>1 ≤ K ≤ 10^5</var> を満たす整数である。</li>
<li><var>|S| = N</var></li>
<li><var>S</var> の各文字は <code>L</code> または <code>R</code> である。</li>
</ul>
</section>


### 考えたこと
<b>①既に幸福な人を幸福じゃないようにする意味はある？</b>  
LRRLをLRLRにするような反転は必要だろうか  
直観では無いが未証明(十中八九必要ないと思ってここでは考えなかった)  
→ランレングス圧縮で同じ文字をまとめて考えちゃおう(以降同じ文字でまとめた物を区間と呼ぶ)

<b>②ある区間を反転させた時、幸福度が変わるのはどこの人?</b>  
例えば   
*LR2L* Rの人たちの1, 2,3,4を反転させると  
*RL2R* Rとなる  
反転前はR2で幸福度1, L単体で幸福度0だった  
反転後はL2で幸福度1, 右側のRが反転していないRと繋がって幸福度1になる  
このようにある区間をまとめて反転させた時、幸福度が変わるのは両端の部分しかなく  
ランレングス圧縮後では反転させた区間の両端の区間と繋がって幸福度が増える  
また、3つ以上の区間をまとめて反転させたとき、端ではない区間の幸福度は保存される  

両端だけ変わるのなら、3つ以上の区間をまとめて反転させても複雑になるだけ  
 

<b>②' 2つの区間の反転と1つの区間の反転の両方を考えるべきか</b>  
簡単な例でそれぞれの反転のパターンを考えてみた  
1回だけ反転させられる時  
S = LRL  

2つの区間の反転は*LLR*とするのが最適  
幸福度は1  
1つの区間の反転は*LLL*とするのが最適  
幸福度は2  

となる。
考えると②から、反転させて幸福度が上がるのは反転させた区間の両端と繋がった時。  
そうなることが多いのは1つの区間を反転させた時。  
→ 1つの区間の反転だけ考えよう  
(2つの区間を反転させた方がいい例があるかもしれないが、その可能性には目をつぶった)  

1つの区間だけ反転させていくことを考えると以下が見えてきた  
- 端の区間以外はどこの区間を反転させても幸福度が+2される  
- 1つだけ反転させるので、ある区間のRを反転させると1つ隣のLとくっついて1つの区間となり  
次反転させるのはRになる…ということはLとRどちらかだけを反転させていけばOK?  
取れるだけランレングス圧縮後の両端以外を反転させて、その後端を反転させれば良い


#### コード　　
```python
def oi(): return int(input())
def os(): return input()
def mi(): return list(map(int, input().split()))

# import sys
# input = sys.stdin.readline

# 再帰を使うときにコメントアウトはずそう
# import sys
# sys.setrecursionlimit(10**8)
# import pypyjit
# pypyjit.set_param('max_unroll_recursion=-1')
input_count = 0
N,K = mi()
S =os()
import sys
from itertools import groupby

def runLengthEncode(S: str) -> "List[tuple(str, int)]":
    grouped = groupby(S)
    res = []
    for k, v in grouped:
        res.append((k, int(len(list(v)))))
    return res

from heapq import heappop,heappush
pat = runLengthEncode(S)

# LとRそれぞれで反転させたときの幸福度をリストにする
Ls = []
Rs = []
for i, (s,num) in enumerate(pat):
    cost = 2
    # ランレングス圧縮後の両端に属していたら-1する
    # 両端に属している時は反転させても幸福度増えないのでcostは0になる
    cost = cost-1 if i==0 else cost
    cost = cost-1 if len(pat)-1==i else cost

    if s=="L":
        heappush(Ls, -cost)
    else:
        heappush(Rs, -cost)

# 現時点でのスコア計算
now_score = sum([p[1]-1 for p in pat])

# LをRにするパターン
R_score = 0
R_count = 0
while Ls:
    c = heappop(Ls)
    R_count += 1
    if R_count <= K:
        R_score += c
    else:
        break

# RをLにするパターン
L_score = 0
L_count = 0
while Rs:
    c = heappop(Rs)
    L_count += 1
    if L_count <= K:
        L_score += c
    else:
        break
increase_hapiness = -min(L_score, R_score)
print(now_score + increase_hapiness)
```

<a href=https://atcoder.jp/contests/abc140/submissions/34709003> 提出コード </a>　　
<!-- <a href=https://youtu.be/cPahvbMzFVs> 配信 </a> -->


### 良かった点  
・反転させて両端以外は変わらない
・区間1つだけ反転させればいいんじゃない？
と方針をどんどん建てられたのはよかった

### 反省点
改めて文字にすると未証明の部分が多く、今回たまたまうまく行ったから良かった。  
論理的な積み重ねもダメで、仮定に仮定を重ねたような砂上の楼閣のようなものだった

もっとかっちり論理を積み重ねていきたいんだけどどうすればいいんだろう