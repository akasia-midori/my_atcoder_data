class LEAF:
    def __init__(self):
        self.l = None
        self.r = None
        self.p = None
        self.value = None
        self.h = 0
class Node:
    def __init__(self, value, p=None):
        self.l = LEAF()
        self.r = LEAF()
        self.p = p # 親
        self.value = value
        self.h = 1

class AVLtree:
    def __init__(self):
        self.tree = Node(float("inf"), Node(float("inf")))
        self.dict = {}
        self.leaf = LEAF()

    def add(self, value, c=1):
        now = self.tree
        if value in self.dict: self.dict[value] += c; return 
        # 値が存在しないときだけノード追加する
        else: self.dict[value] = c
        while True:
            if now.value > value:
                if now.l.h == 0: now.l = Node(value, now); self.__balance__(True, now.l); return
                now = now.l
            else:
                if now.r.h == 0: now.r = Node(value, now); self.__balance__(True, now.r); return
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
                if now.l.h != 0:
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
        now = self.tree.l
        out = None
        while now.h != 0:
            if value < now.value: out = now.value
            
            if now.l.value is None:
                if now.r.value is None: break
                else: now = now.r
            elif now.r.value is None: now = now.l
            else:
                if value < now.l.value:  now = now.l
                else: now = now.r
        return out

    def gt(self, value):
        "Find the smallest element > x, or None if it doesn't exist."
        now = self.tree.l
        out = None
        while now.h != 0:
            if value < now.value: out = now.value
            
            if now.l.value is None:
                if now.r.value is None: break
                else: now = now.r
            elif now.r.value is None: now = now.l
            else:
                if value < now.l.value:  now = now.l
                else: now = now.r
        return out

    def le(self, value):
        "Find the largest element <= x, or None if it doesn't exist."
        if self.find(value): return value
        now = self.tree.l
        out = None
        while now.h != 0:
            if value > now.value: out = now.value
            if now.l.value is None:
                if now.r.value is None: break
                else: now = now.r
            elif now.r.value is None: now = now.l
            else:
                if value < now.l.value: now = now.l
                else: now = now.r
        return out

    def lt(self, value):
        "Find the largest element < x, or None if it doesn't exist."
        now = self.tree.l
        out = None
        while now.h != 0:
            if value > now.value: out = now.value
            if now.l.value is None:
                if now.r.value is None: break
                else: now = now.r
            elif now.r.value is None: now = now.l
            else:
                if value < now.l.value: now = now.l
                else: now = now.r
        return out

    def find(self, value):
        if value in self.dict:
            return True
        return False
        # now = self.tree.l
        # while now.h != 0:
        #     if now.value > value: now = now.l
        #     elif now.value < value: now = now.r
        #     else: return True
        # return False


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

    def __modHeight__(self, u):
        u.h = 1 + max(u.l.h, u.r.h)

    def __rotateR__(self, u):
        v = u.l
        self.__replace__(u, v)
        u.l = v.r
        v.r.p = u
        v.r = u
        u.p = v
        self.__modHeight__(v.r)
        self.__modHeight__(v)
        return v


    def __rotateL__(self, v):
        u = v.r
        self.__replace__(v, u)
        v.r = u.l
        u.l.p = v
        u.l = v
        v.p = u
        self.__modHeight__(u.l)
        self.__modHeight__(u)
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
        while (t.p.value != float("inf")):
            u = t.p
            h = u.h
            if ((u.l == t) == mode):
                if (self.__bias__(u) == 2):
                    if (self.__bias__(u.l) >= 0):
                        u = self.__rotateR__(u)
                    else:
                        u = self.__rotateLR__(u)
                else: self.__modHeight__(u)
            else:
                if (self.__bias__(u) == -2):
                    if (self.__bias__(u.r) <= 0):
                        u = self.__rotateL__(u)
                    else:
                        u = self.__rotateRL__(u)
                else: self.__modHeight__(u)
            if h == u.h:
                break
            t = u
        
    