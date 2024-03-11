from random import randint
class node:
    def __init__(self, v, p):
        self.val = v # 値
        self.ch = [None, None] # [左, 右]
        self.pri = p # 優先度
        self.cnt = 1 # 部分木のサイズ
        self.sums = v # 部分木の値の和

def count_node(t):
    if t is None:
        return 0
    return t.cnt

def sum_node(t):
    if t is None:
        return 0
    return t.sums

def update(t):
    t.cnt = count_node(t.ch[0]) + count_node(t.ch[1]) + 1
    t.sums = sum_node(t.ch[0]) + sum_node(t.ch[1]) + t.val
    return t

#参考: https://www.slideshare.net/iwiwi/2-12188757
# 左の木 l , 右の木 r
def merge(l, r):
    # 優先度の高い方の根を新しい根にする
    # 再帰的にmerge  ← 再帰的?! pythonを殺す気か?!
    
    # どちらかがNULLならNULLじゃない方を返す
    if l is None:
        return r
    elif r is None:
        return l
    
    # 左の部分木の根の方が優先度が高い場合
    if l.pri > r.pri:
        l.ch[1] = merge(l.ch[1], r)
        return update(l)
    # 右の部分木の根の方が優先度が高い場合
    else:
        r.ch[0] = merge(l, r.ch[0])
        return update(r)

def split(t, k):
    # splitは優先度のことをを何も考えないで再帰的に切るだけ ← 再帰的?!
    # (部分木内の任意のノードは根より優先度小なので大丈夫)
    if t is None:
        return (None, None)
    
    if k <= count_node(t.ch[0]):
        s = split(t.ch[0], k)
        t.ch[0] = s[1]
        return (s[0], update(t))
    else:
        s = split(t.ch[1], k - count_node(t.ch[0]) -1)
        t.ch[1] = s[0]
        return (update(t), s[1])    

# 木 t, 場所 k, 値 v
def insert(t, k, v):
    # 木tを場所kでsplit
    # 左の部分木、値vのノードだけの木、右の部分木をmerge
    l, r = split(t, k)
    n = node(v, randint(0,10**8))
    
    temp = merge(l,n)
    temp1 = merge(temp, r)
    return temp1

# 木 t, 場所 k
def erase(t, k):
    # 木tを場所kと場所k+1で3つにsplit (split2回やればいい)
    # 一番左と一番右の部分木をmerge
    l1, r1 = split(t, k)
    _, r2 = split(r1, k+1 - count_node(l1))
    return merge(l1, r2)

# 探す木 t, 何番目かを示す k
# k番目に1が立ってる位置を探して返す
def searchK(t, k):
    # 1足ってる数がk以下ならNoneを返す。そんなのないので
    if sum_node(t) < k:
        return None
    # 
    index = 0

    now = t
    while True:
        if now is None:
            break

        #
        part_sums_l = sum_node(now.ch[0])
        sums_l = part_sums_l + now.val # 自分自身を含めた左側の部分木の立ってるbitの数

        # 両方子供がいない。つまり葉であるなら
        if now.ch[0] is None and now.ch[1] is None:  break
        
        # 左が既に超えてたら左のindexへ行く
        if sums_l >= k:
            # 自分のノードを含めないとkに足りない時 
            if part_sums_l < k:
                # 今までの累計のindexと左側の部分木と自分自身を足して返す
                # print(index, count_node(now.ch[0]))
                return index + (count_node(now.ch[0]))

            now = now.ch[0]

        # ここに来るのは左が超えていない状態 
        else: 
            index += (count_node(now.ch[0])+1)
            now = now.ch[1]
            k -= sums_l
        

    return index
