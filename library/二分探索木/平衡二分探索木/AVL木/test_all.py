def solve(query):
    # https://github.com/tatyam-prime/SortedSet/blob/main/SortedMultiset.py
    import math
    from bisect import bisect_left, bisect_right, insort
    from typing import Generic, Iterable, Iterator, TypeVar, Union, List
    T = TypeVar('T')
    
    class SortedMultiset(Generic[T]):
        BUCKET_RATIO = 50
        REBUILD_RATIO = 170
    
        def _build(self, a=None) -> None:
            "Evenly divide `a` into buckets."
            if a is None: a = list(self)
            size = self.size = len(a)
            bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
            self.a = [a[size * i // bucket_size : size * (i + 1) // bucket_size] for i in range(bucket_size)]
        
        def __init__(self, a: Iterable[T] = []) -> None:
            "Make a new SortedMultiset from iterable. / O(N) if sorted / O(N log N)"
            a = list(a)
            if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
                a = sorted(a)
            self._build(a)
    
        def __iter__(self) -> Iterator[T]:
            for i in self.a:
                for j in i: yield j
    
        def __reversed__(self) -> Iterator[T]:
            for i in reversed(self.a):
                for j in reversed(i): yield j
        
        def __len__(self) -> int:
            return self.size
        
        def __repr__(self) -> str:
            return "SortedMultiset" + str(self.a)
        
        def __str__(self) -> str:
            s = str(list(self))
            return "{" + s[1 : len(s) - 1] + "}"
    
        def _find_bucket(self, x: T) -> List[T]:
            "Find the bucket which should contain x. self must not be empty."
            for a in self.a:
                if x <= a[-1]: return a
            return a
    
        def __contains__(self, x: T) -> bool:
            if self.size == 0: return False
            a = self._find_bucket(x)
            i = bisect_left(a, x)
            return i != len(a) and a[i] == x
    
        def count(self, x: T) -> int:
            "Count the number of x."
            return self.index_right(x) - self.index(x)
    
        def add(self, x: T) -> None:
            "Add an element. / O(√N)"
            if self.size == 0:
                self.a = [[x]]
                self.size = 1
                return
            a = self._find_bucket(x)
            insort(a, x)
            self.size += 1
            if len(a) > len(self.a) * self.REBUILD_RATIO:
                self._build()
    
        def discard(self, x: T) -> bool:
            "Remove an element and return True if removed. / O(√N)"
            if self.size == 0: return False
            a = self._find_bucket(x)
            i = bisect_left(a, x)
            if i == len(a) or a[i] != x: return False
            a.pop(i)
            self.size -= 1
            if len(a) == 0: self._build()
            return True
    
        def lt(self, x: T) -> Union[T, None]:
            "Find the largest element < x, or None if it doesn't exist."
            for a in reversed(self.a):
                if a[0] < x:
                    return a[bisect_left(a, x) - 1]
    
        def le(self, x: T) -> Union[T, None]:
            "Find the largest element <= x, or None if it doesn't exist."
            for a in reversed(self.a):
                if a[0] <= x:
                    return a[bisect_right(a, x) - 1]
    
        def gt(self, x: T) -> Union[T, None]:
            "Find the smallest element > x, or None if it doesn't exist."
            for a in self.a:
                if a[-1] > x:
                    return a[bisect_right(a, x)]
    
        def ge(self, x: T) -> Union[T, None]:
            "Find the smallest element >= x, or None if it doesn't exist."
            for a in self.a:
                if a[-1] >= x:
                    return a[bisect_left(a, x)]
        
        def __getitem__(self, x: int) -> T:
            "Return the x-th element, or IndexError if it doesn't exist."
            if x < 0: x += self.size
            if x < 0: raise IndexError
            for a in self.a:
                if x < len(a): return a[x]
                x -= len(a)
            raise IndexError
    
        def index(self, x: T) -> int:
            "Count the number of elements < x."
            ans = 0
            for a in self.a:
                if a[-1] >= x:
                    return ans + bisect_left(a, x)
                ans += len(a)
            return ans
    
        def index_right(self, x: T) -> int:
            "Count the number of elements <= x."
            ans = 0
            for a in self.a:
                if a[-1] > x:
                    return ans + bisect_right(a, x)
                ans += len(a)
            return ans
    sets = SortedMultiset()
    out = []
    for q in query:
        a = float("inf")
        if q[0]==0: # add
            sets.add(q[1])

        elif q[0]==1: # delete
            sets.discard(q[1])

        elif q[0]==2: # lt
            a=sets.lt(q[1])

        elif q[0]==3: # le
            a=sets.le(q[1])

        elif q[0]==4: # ge
            a=sets.ge(q[1])

        elif q[0]==5: # gt
            a=sets.gt(q[1])
        if a is None:
            out.append([q[0], float("inf")])
        else:
            out.append([q[0], a])
    return out

class LEAF:
    def __init__(self):
        self.l = None
        self.r = None
        self.p = None
        self.value = None
        self.h = 0
class Node:
    def __init__(self, value, leaf, p=None):
        self.l = leaf
        self.r = leaf
        self.p = p # 親
        self.value = value
        self.h = 1

class AVLtree:
    def __init__(self):
        self.INF = float("inf")
        self.leaf = LEAF()
        self.tree = Node(self.INF, self.leaf, Node(self.INF, self.leaf))
        self.dict = {}

    def add(self, value, c=1):
        now = self.tree
        if value in self.dict: self.dict[value] += c; return 
        # 値が存在しないときだけノード追加する
        else: self.dict[value] = c
        while True:
            if now.value > value:
                if now.l.h == 0: now.l = Node(value, self.leaf, now); self.__balance__(True, now.l); return
                now = now.l
            else:
                if now.r.h == 0: now.r = Node(value, self.leaf, now); self.__balance__(True, now.r); return
                now = now.r

    def delete(self, value, c=1):
        if value in self.dict: self.dict[value] -= min(self.dict[value], c)  
        else: return False
              
        if self.dict[value] == 0: del self.dict[value]
        else: return False

        now = self.tree.l
        while now.h != 0:
            if now.value > value: now = now.l
            elif now.value < value: now = now.r
            else:
                # 葉に番兵を追加したから葉が1つの時とか考えないで済むよ！やったね妙ちゃん！
                # 削除ノードが見つかったとき
                # 葉ノード無し
                if now.l.h == now.r.h == 0:
                    if now.p.l == now: now.p.l = self.leaf
                    else: now.p.r = self.leaf
                elif now.l.h != 0:
                    # 子ノード2つ
                    # 今のノードから1つ左に行き、その後行けるだけ右に行ったノードと今のノードを入れ替える
                    change = now.l
                    while change.r.h !=0 : change = change.r
                    now.value = change.value # 値を入れ替える

                    self.__replace__(change, change.l)
                    self.__balance__(False, change.l)

                else:
                    self.__replace__(now, now.r)
                    self.__balance__(False, now.r)
                    
                return True

    def ge(self, value):
        "Find the smallest element >= x, or None if it doesn't exist."
        if self.find(value): return value
        return self.gt(value)

    def gt(self, value):
        "Find the smallest element > x, or None if it doesn't exist."
        now = self.tree.l
        out = self.INF
        while now.h != 0:
            if value < now.value <= out: out = now.value
            if now.l.value is None:
                if now.r.value is None: break
                else: now = now.r
            elif now.r.value is None: now = now.l
            else:
                if now.value > value: now = now.l
                else: now = now.r

        if out == self.INF: return None
        return out

    def le(self, value):
        "Find the largest element <= x, or None if it doesn't exist."
        if self.find(value): return value
        return self.lt(value)

    def lt(self, value):
        "Find the largest element < x, or None if it doesn't exist."
        now = self.tree.l
        out = self.INF*-1
        while now.h != 0:
            if value > now.value >= out: out = now.value
            if now.l.value is None:
                if now.r.value is None: break
                else: now = now.r
            elif now.r.value is None: now = now.l
            else:
                if  now.value < value: now = now.r
                else: now = now.l
        if out == self.INF*-1: return None
        return out

    def find(self, value):
        if value in self.dict:
            return True
        return False

    def max(self):
        now = self.tree.l
        out = 0
        while now.h != 0:
            out = now.value
            now = now.r
        return out

    def min(self):
        now = self.tree.l
        out = 0
        while now.h != 0:
            out = now.value
            now = now.l
        return out

    # 参考: http://wwwa.pikara.ne.jp/okojisan/avl-tree/iavl-tree.html
    def __replace__(self, u, v):
        p = u.p
        if (p.l == u): p.l = v
        else: p.r = v
        v.p = p

    def __rotateR__(self, u):
        v = u.l
        self.__replace__(u, v)
        u.l = v.r
        v.r.p = u
        v.r = u
        u.p = v
        v.r.h = 1 + max(v.r.l.h, v.r.r.h)
        v.h = 1 + max(v.l.h, v.r.h)
        return v


    def __rotateL__(self, v):
        u = v.r
        self.__replace__(v, u)
        v.r = u.l
        u.l.p = v
        u.l = v
        v.p = u
        u.l.h = 1 + max(u.l.l.h, u.l.r.h)
        u.h = 1 + max(u.l.h, u.r.h)
        return u

    def __rotateRL__(self, t):
        self.__rotateR__(t.r)
        return self.__rotateL__(t)

    def __rotateLR__(self, t):
        self.__rotateL__(t.l)
        return self.__rotateR__(t)

    def __bias__(self, u):
        return u.l.h - u.r.h

    def __balance__(self, mode, t):
        while (t.p.value != self.INF):
            u = t.p
            h = u.h
            if ((u.l == t) == mode):
                if (self.__bias__(u) == 2):
                    if (self.__bias__(u.l) >= 0):
                        u = self.__rotateR__(u)
                    else:
                        u = self.__rotateLR__(u)
                else: u.h = 1 + max(u.l.h, u.r.h)
            else:
                if (self.__bias__(u) == -2):
                    if (self.__bias__(u.r) <= 0):
                        u = self.__rotateL__(u)
                    else:
                        u = self.__rotateRL__(u)
                else: u.h = 1 + max(u.l.h, u.r.h)
            if h == u.h:
                break
            t = u              


def solve2(query):
    sets = AVLtree()
    out = []
    for q in query:
        a = float("inf")
        if q[0]==0: # add
            sets.add(q[1])

        elif q[0]==1: # delete
            sets.delete(q[1])

        elif q[0]==2: # lt
            a=sets.lt(q[1])

        elif q[0]==3: # le
            a=sets.le(q[1])

        elif q[0]==4: # ge
            a=sets.ge(q[1])

        elif q[0]==5: # gt
            a=sets.gt(q[1])
        if a is None:
            out.append([q[0], float("inf")])
        else:
            out.append([q[0], a])
    return out

import random 

for i in range(10000):
    N = random.randint(2, 30)
    querys = [[random.randint(0, 5),random.randint(-10, 10)] for _ in range(N)]
    no = solve2(querys)
    so = solve(querys)
    flg = False
    for n, s in zip(no, so):
        if n[1]!=s[1]:
            flg = True
            print(N, no, so)
            break
    if flg:
        break