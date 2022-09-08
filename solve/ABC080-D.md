# ABC080-D Recording 
問題URL:
<a href=https://atcoder.jp/contests/abc080/tasks/abc080_d>
https://atcoder.jp/contests/abc080/tasks/abc080_d
</a>

### 問題文
>joisinoお姉ちゃんは、録画機を用いて N 個のテレビ番組を録画しようとしています。
テレビが受信できるチャンネルは C 個あり、1 から C までの番号がついています。
joisinoお姉ちゃんの録画したいテレビ番組のうち、i 個目のテレビ番組は、時刻 s_iから時刻 t_i
​まで、チャンネル c_iで放送されます。(ただし時刻 s_iを含み、時刻 t_iを除く)

>ただし、同じチャンネルで複数のテレビ番組が同時に放送されることはありません。

>また、録画機は、あるチャンネルの時刻 S から時刻 T までを録画するとき、時刻 S−0.5 から時刻 T までの間、他のチャンネルの録画に使うことができません。(ただし時刻 S−0.5を含み、時刻 T を除く)

>N 個のテレビ番組の全ての放送内容が含まれるように録画するとき、必要な録画機の最小個数を求めてください。

### 制約  
1≦N≦10^5  
1≦C≦30  
1≦s_i<t_i≦10^5   
1≦c_i≦C  
c_i=c_jかつ i≠j ならば t_i≦s_j  か s_i≧t_jが成り立つ  
入力は全て整数

### 考えたこと
<b> 失敗1:区間スケジューリングっぽい？ </b>  
区間スケジューリング: (この問題だと)台数が決められてて何個のチャンネルを録画できますか  
のような問題を解く際の方策。今回は違ったのだが違うことに気付けなかった  

(失敗した方針の供養)  
問題をぱっと見て区間スケジューリングっぽいなぁと思ったのでこれで一旦考えてみることにした。  
終了時間、開始時間の昇順でソート、チャンネルに関しては無視して考えた(今思うとなんで無視したんだろう)  

ソートした後、  
ある番組の終了値 < ある番組の開始値になる箇所を区間として見て、しゃくとり法の要領で各区間の番組数の最大値を取ってくるようにした  
というのも何故か以下のような入力の時、必要な台数が3台だと思ってしまっていたため  
>1 7 1  
1 2 2  
3 5 3  


<b> 成功:累積和 </b>  
上記の入力が2だと思ってから全てを無にして考え直した。  
鮭のホイル焼き美味しい  
ある時間で見た時のチャンネルの種類数がそれぞれの時間で録画に必要な最小の台数であるので  
全ての時間を見てチャンネルの種類数が最大の時の値が答えになる  
(というのに気付くのに1時間かかって泣きそう)

チャンネルが最大30  
終了時間の最大が10^5なので  
全ての時間で各チャンネルを録画する必要があるかを判定すれば良い  
計算量はN×Cで3×10^6. 目安の10^8にはまだ余裕があるので適当に30回以内の計算で判定出来ればよさそう  

<b>判定の方法案</b>  

- 脳死セグ木パンチ:チャンネルの数だけセグ木を作って区間に値を足す  
全部終わったら全ての時間で全てのチャンネルが1以上の数を集計すればそれが録画に必要な台数なはず
計算量も(NlogN)Cぐらいで余裕がありそう
- imos法: 脳死セグ木案を思いついた後に累積和を取るだけならもっと簡単でいいと思ったのでimos法を考えた  
imosの足す側と引く側を別々のリストで管理した

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

N,C = mi()

# imos法での足す側と引く側のリストを別々で管理
plus_lists = [None] * (10**5+3)
minus_lists = [None] * (10**5+3)
for i in range(N):
    s,t,c = mi()
    if plus_lists[s] is None:
        plus_lists[s] = set([c])
    else:
        plus_lists[s].add(c)

    if minus_lists[t+1] is None:
        minus_lists[t+1] = set([c])
    else:
        minus_lists[t+1].add(c)

from collections import defaultdict
maxs = 0
now = defaultdict(int)
for i in range(10**5+2):

    if plus_lists[i] is not None:
        for p in plus_lists[i]:
        	# まだ登録されてないチャンネルなら+1
            now[p] += 1

    if minus_lists[i] is not None:
        for p in minus_lists[i]:
            now[p] -= 1
            # 登録されていらチャンネルから引いて0になるならdelete
            if now[p] == 0:
                del now[p]
    # 各時点で最大値見られているチャンネルの最大数を保存
    maxs = max(len(now), maxs)
print(maxs)
```

<a href=https://atcoder.jp/contests/abc080/submissions/34693937> 提出コード </a>　　
<a href=https://youtu.be/cPahvbMzFVs> 配信 </a>


### 良かった点  
問題を理解できてからの解法を思いつくまでが速かった。成長を感じる

### 反省点
・問題文を途中から読んでないかのようなミスが多く、これが原因で多くの時間を無駄にしてしまった。  
・あいまいな理解の解法に飛びついてしまった。結果的にそれで解ける問題ではなくこれもロスの原因。  
・問題文の理解 → それに合うアルゴリズムを考えるという流れが出来ていなかったので問題文の理解を深められるような再発防止策が望まれる

