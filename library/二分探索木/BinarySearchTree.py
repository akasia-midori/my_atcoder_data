class Node:
    def __init__(self, value):
        self.l = None
        self.r = None
        self.value = value

class BinarySearchTree:
    def __init__(self):
        self.tree = Node(float("inf"))

    def add(self, value):
        now = self.tree
        while True:
            if now.value > value:
                if now.l is None:
                    now.l = Node(value)
                    break
                now = now.l
            else:
                if now.r is None:
                    now.r = Node(value)
                    break
                now = now.r

    def delete(self, value):
        if self.tree.l is None and self.tree.r is None: return False # ノードが何もない時
        old = self.tree 
        now = self.tree.l
        while True:
            if now.value > value:
                if now.l is None: return False# 削除ノードを見つけられないとき
                old, now = now, now.l
                # now = now.l
            elif now.value < value:
                if now.r is None: return False# 削除ノードを見つけられないとき
                old, now = now, now.r
                # now = now.r
            else:
                # 削除ノードが見つかったとき
                # 葉ノード無し
                if now.l is None and now.r is None:
                    if id(old.r) == id(now): old.r = None # 1つ上のrと今のID値が一致してれば削除
                    else: old.l = None
                    return True
                
                # 子ノード1つだけ
                if (now.l is None and now.r is not None):
                    if id(old.r) == id(now): old.r = now.r # nowの子を自分が元居た場所に付ける
                    else: old.l = now.r
                    return True
                if (now.l is not None and now.r is None):
                    if id(old.r) == id(now): old.r = now.l # nowの子を自分が元居た場所に付ける
                    else: old.l = now.l
                    return True

                # 子ノード2つ
                # 今のノードから1つ右に行き、その後行けるだけ左に行ったノードと今のノードを入れ替える
                change = now.r
                change_old = now
                while change.l:
                    change, change_old = change.l, change

                now.value = change.value # 一番左側のノードと値だけ入れ替える
                if id(change_old.l) == id(change): change_old.l = None
                else: change_old.r = None
                return True

    def find(self, value):
        now = self.tree
        while True:
            if now.value > value:
                if now.l is None: return False
                now = now.l
            elif now.value < value:
                if now.r is None: return False
                now = now.r
            else: return True
            