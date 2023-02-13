# AVL木のページ

## 概要
ノードの左右の部分木の高さの絶対差が1以内であるようにする。  
絶対差が2以上発生するようなケース(二分探索木の最悪ケース)の場合は<b>木の回転</b>で対応する。  
実装上の工夫であるが、各ノードにはデフォルトで高さが0の番兵を追加し、左右に子ノードが無くても部分木の高さの絶対差を計算できるようにしている。  
各ノードの高さは左右の部分木の高さの最大値+1とする。  



|  処理  |  計算量  |
| ---- | ---- |
|  追加  | O(logN)  |
|  削除  | O(logN)  |
|  検索  | O(logN)、この実装では辞書に入れてるのでO(1)  |
|  二分探索  | O(logN) |

<br></br>

## 用途
データが逐次追加されるような状況で二分探索が必要な時。  
値が制限されるとき、SortedSetと同じぐらい速かったよ。

<br></br>

## 処理概要

### 追加 
根のノードから以下を行う。
追加したい値をVとする。  

1. 自分のノードに含まれる値 <= Vなら左のノードへ遷移する。もし、遷移先が無ければそこに新しいノードを追加する。  
2. そうでなければ右のノードへ遷移する。もし、遷移先が無ければそこに新しいノードを追加する。  

追加のロジックは普通の二分木と同じ。  
追加したノードを含む木の高さを反映させ、バランスが崩れていないかを判定する。崩れていた場合、木の回転を行いバランス調整を行う。


<br></br>

### 削除 
根のノードから以下を行う。
削除したい値をVとする。  

削除したい値が見つかるまで以下を行う.もし見つからなかったら終わり。アルゴリズムからの要望はないので好きな処理にしてね。
1. 自分のノードに含まれる値 <= Vなら左のノードへ遷移する。もし、遷移先が無ければそこで終わり。  
2. そうでなければ右のノードへ遷移する。もし、遷移先が無ければそこで終わり。  
3. 削除したい場所に辿り着いたら以下の分岐に入る。　 


#### 削除パターン
AVL木で番兵を追加しているので、「子ノードがない時」は存在せず、全て子ノードが2つある状態になっていることに注意。あと回転が実装されているため、削除前のタイミングで左右の部分木の高さの絶対差が2以上になってもいない。

削除ノードから1つ右遷移(削除パターンの条件から必ずある)し、その後、左側に行けるだけ行く。
辿り着いたノードと削除ノードを取り替える。  
※1つ左に遷移した後辿れるだけ右に遷移したものと取り替えても別に問題ない。  
念のため、削除パターンを画像で列挙する
![delete_pattern](./image/delete_pattern.png)


削除後、削除したノードを含む木のバランスが崩れる可能性があるため、チェックし崩れていたら回転でバランスを整える

参考サイト:(というか番兵とか回転とかまんま真似しました)
・http://wwwa.pikara.ne.jp/okojisan/avl-tree/iavl-tree.html


<br></br>

#### 実験memo
下記コードにて生のpythonとpypyで実行時間の比較を行った
python  
シーケンシャルアクセス:0.9374985694885254  
ランダムアクセス:4.039090156555176  
木ノードを参照:1.673384428024292  
  
<br></br>
pypy(atcoder環境 7.3.0)  
シーケンシャルアクセス:0.021963834762573242  
ランダムアクセス:0.05605173110961914  
木ノードを参照:0.1224982738494873
  
  
pypy環境では木ノードを再帰的に参照するよりランダムアクセスの方が速いらしい.
ノードの作り方を工夫したら定数倍速くなるのでは？  
「部分木のインデックスを持たせたリスト」と「ノードに持つ値を格納したリスト」を持つみたいな実装をしたら地獄みたいに遅くなった(pypyで木を辿る時の3倍)
pythonだとランダムアクセスと同じぐらい  
なんでこんなことがおこるんだろう…whileで回すしてるので毎回if文が回ってるから？

```python
class LEAF:
    def __init__(self):
        self.l = None
        self.r = None
        self.p = None
        self.value = None
        self.h = 0
        
class Node:
    def __init__(self, value, leaf, p=None):
        self.l = LEAF()
        self.r = LEAF()
        self.p = p # 親
        self.value = value
        self.h = 1
N = 10**6
ls = LEAF()
tree = Node(0, ls)
now = tree
for i in range(1, N):
    now.r = Node(i, ls)
    now = now.r

from time import time
lists = [i for i in range(N)]

start = time()
for _ in range(10):
    sums = 0
    for i in range(N):
        sums += lists[i]
print(time()-start)
import random 
seni = [i for i in range(N)]
random.shuffle(seni)

start = time()
for _ in range(10):
    sums = 0
    
    for i in seni:
        sums += lists[i]
print(time()-start)
import random 
seni = [i for i in range(N)]
random.shuffle(seni)

start = time()
for _ in range(10):
    sums = 0
    now = tree
    while now.value is not None:
        sums += now.value
        now = now.r
print(time()-start)

import random 
seni = [i for i in range(N)]
random.shuffle(seni)

lists = seni[:]
dicts = {}
ind = [i for i in range(N)]

for r,d in zip(lists, ind):
    dicts[r] = d

INF = 10**9
inds = []
for i in lists:
    if i+1 == N:
        inds.append(INF)
    else:
        inds.append(dicts[i+1])


start_ind = lists.index(0)
start = time()
for _ in range(10):
    sums = 0
    ind = start_ind
    while ind != INF:
        sums += lists[ind]
        ind = inds[ind]
print(time()-start)
```