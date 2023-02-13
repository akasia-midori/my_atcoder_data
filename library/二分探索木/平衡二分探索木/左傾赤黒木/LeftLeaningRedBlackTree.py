RED = True
BLACK = False
# class LEAF:
#     def __init__(self):
#         self.left = None
#         self.right = None
#         self.prt = None
#         self.value = None
#         self.color = BLACK # 黒   Trueを赤, Falseを黒とする

class Node:
    def __init__(self, value, p=None):
        self.left = None #leaf
        self.right = None #leaf
        self.prt = p # 親
        self.color = RED # 赤   Trueを赤, Falseを黒とする
        self.value = value

class LeftLeaningRedBlackTree:
    def __init__(self):
        self.root = None
        # self.LEAF = LEAF()
        self.dicts = {}

    def rotate_left(self,h):
        x = h.right 
        m = x.left
        p = h.prt

        # 元々hに繋がってた親ノードをxに繋ぎ変える
        x.prt = p 
        if p is not None:
            if(p.left == h): # hが繋がってた場所にxを入れる
                p.left = x
            else: 
                p.right = x

        # 真ん中のmをhの右側に繋ぎ変える
        h.right = m
        if m is not None:
            m.prt = h

        # xとhの親子関係を反転させる
        x.left = h
        h.prt = x

        x.color = h.color
        h.color = RED
        return x

    def rotate_right(self, h):
        x = h.left 
        m = x.right
        p = h.prt

        # 元々hに繋がってた親ノードをxに繋ぎ変える
        x.prt = p
        if p is not None:
            if(p.left == h): # hが繋がってた場所にxを入れる
                p.left = x
            else: 
                p.right = x

        # 真ん中のmをhの左側に繋ぎ変える
        h.left = m
        if m is not None:
            m.prt = h

        # xとhの親子関係を反転させる
        x.right = h
        h.prt = x

        x.color = h.color
        h.color = RED
        return x

    def flip_color(self, h):
        h.color = not h.color
        if h.left is not None:
            h.left.color = not h.left.color
        if h.right is not None:
            h.right.color = not h.right.color

    def is_red(self,node):
        if node is not None and node.color == RED and node.value is not None:
            return True
        return False

    def is_black(self,node):
        if node is None or node.color == BLACK:
            return True
        return False

    def move_red_left(self, node):
        self.flip_color(node)

        right = node.right
        if(self.is_red(right.left)):
            right = self.rotate_right(right)
            node = self.rotate_left(node)
            self.flip_color(node)
            if node.prt is None:
                self.root = node
        return node

    def move_red_right(self, node):
        self.flip_color(node)

        left = node.left
        if self.is_red(left.left):
            node = self.rotate_right(node)
            self.flip_color(node)
            if(node.prt is None):
                self.root = node
        return node


    def fixup(self, node):
        if(self.is_red(node.right) and self.is_black(node.left)):
            node = self.rotate_left(node)
            if(node.prt is None):
                self.root = node

        if(self.is_red(node.left) and self.is_red(node.left.left)):
            node = self.rotate_right(node)
            if(node.prt is None):
                self.root = node

        if(self.is_red(node.left) and self.is_red(node.right)):
            self.flip_color(node)
        return node


    def find_node(self, node, x):
        if(node == None): return node
        while (node.value != x):
            if(x < node.value):
                if(node.left is None): break
                node = node.left
            else:
                if(node.right is None): break
                node = node.right
        return node

    def insert(self, x):
        if x in self.dicts:
            self.dicts[x] += 1
            return True
        else:
            self.dicts[x] = 1
        if(self.root is None):
            new_node = Node(x)
            self.root = new_node
            new_node.color = BLACK
            return True

        node = self.find_node(self.root, x)# 挿入するノードまで探索
        if node.value == x:
            return False

        new_node = Node(x)
        if(x < node.value):
            node.left = new_node
        else:
            node.right = new_node
        new_node.prt = node

        while(node):
            # ++node->size
            # show(node)
            node = self.fixup(node).prt
        self.root.color = BLACK
        return True

    ############# delete ################
    def move_red_left(self, node):
        self.flip_color(node)

        right = node.right
        if self.is_red(right.left):
            self.rotate_right(right)
            node = self.rotate_left(node)
            self.flip_color(node)
            if node.prt is None:
                self.root = node
        return node

    def move_red_right(self, node):
        self.flip_color(node)

        left = node.left
        if self.is_red(left.left):
            node = self.rotate_right(node)
            self.flip_color(node)
            if node.prt is None:
                self.root = node
        return node

    def delete(self, x):
        if x in self.dicts:
            self.dicts[x] -= 1
            if self.dicts[x] == 0:
                del self.dicts[x]
            else:
                return False
        else:
            return False

        node = self.root
        deleted = False
        while node:
            if node is not None and  x < node.value:
                if node.left is None: break

                if self.is_black(node.left) and self.is_black(node.left.left):
                    node = self.move_red_left(node)
                node = node.left
                continue
        
            if self.is_red(node.left):
                node = self.rotate_right(node)
                if node.prt is None: self.root = node
            if node.right is None:
                if node.value == x: deleted = True
                break
                
            if self.is_black(node.right) and self.is_black(node.right.left):
                node = self.move_red_left(node)
            if node.value == x:
                c_node = node.right
                while c_node.left:
                    if self.is_black(c_node.left) and  self.is_black(c_node.left.left):
                        c_node = self.move_red_left(c_node)
                    c_node = c_node.left
                node.value = c_node.value
                node = c_node
                deleted = True
                break
            node = node.right

        # show(node)
        if deleted:
            prt = node.prt
            if prt:
                if prt.left == node:
                    prt.left = None# self.LEAF
                else:
                    prt.right = None# self.LEAF
            else:
                self.root = None
            node = prt

        if node:
            while node:
                # if deleted: node.size -= 1
                node = self.fixup(node).prt
            self.root.color = BLACK
        return True





tree = LeftLeaningRedBlackTree()
tree.insert(1)
tree.insert(2)
tree.insert(3)
tree.insert(4)
tree.insert(5)
tree.insert(6)

tree.delete(1)
tree.delete(2)
tree.delete(4)
# 1~4まで消したタイミングで右の子だけが残る なぜ？左に行ってほしい