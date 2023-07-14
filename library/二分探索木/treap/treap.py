class Treap:
    def __init__(self):
        self.INF = float("inf")
        self.leaf = LEAF()
        self.tree = Node(self.INF, self.leaf, random.random(), Node(self.INF, self.leaf, random.random()))
        self.dict = {}


    # 追加したノードを引数にとる
    def __up_heap__(self, node):
        # 最下層から根に向かって値を交換していく
        # 末端ノードから根へ辿っていける
        # count = 1
        while node.p.value != self.INF:
            if node.priority > node.p.priority:
                # print(f"node:{node.value}")
                if (node.p.r is not None) and (node.p.r.value == node.value):
                    # 追加したノードの親を引数にとる
                    node = self.__left_rotate__(node.p)
                    
                elif (node.p.l is not None) and (node.p.l.value == node.value): 
                    # 追加したノードの親を引数にとる
                    node = self.__right_rotate__(node.p)

                else:
                    break

                # print(node.p.value, node.p.l.value, node.p.r.value)
                # print(node.p.priority, node.p.l.priority, node.p.r.priority)
                # print(node.value, node.l.value, node.r.value)
                # print(node.priority, node.l.priority, node.r.priority)
                # print()
                # print()
                # print()
            else:
                break
            # print(count)

    # 追加したノードを引数にとる
    def __up_heap_break__(self, node):
        # 最下層から根に向かって値を交換していく
        # 末端ノードから根へ辿っていける
        # count = 1
        while node.p.value != self.INF:
            if node.priority > node.p.priority:
                if (node.p.r is not None) and (node.p.r.value == node.value):
                    # 追加したノードの親を引数にとる
                    node = self.__left_rotate__(node.p)
                    
                elif (node.p.l is not None) and (node.p.l.value == node.value): 
                    # 追加したノードの親を引数にとる
                    node = self.__right_rotate__(node.p)


                # print(node.p.value, node.p.l.value, node.p.r.value)
                # print(node.p.priority, node.p.l.priority, node.p.r.priority)
                # break

            else:
                break

    def __right_rotate__(self, node): 
        new = node.l
        node.l = new.r
        new.r = node

        # 親側からの√を差し替え
        if node.p.r is not None:
            if node.p.r.priority == node.priority:
                node.p.r = new
            else:
                node.p.l = new

        # 親側からの√を差し替え
        elif node.p.l is not None:
            if node.p.l.priority == node.priority:
                node.p.l = new
            else:
                node.p.r = new

        # 子から親への差し替え
        new.p = node.p
        node.p = new

        # 子から見た親の差し替え
        new.r.l.p = node
        

        return new

    def __left_rotate__(self, node): 
        new = node.r # y:new
        node.r = new.l
        new.l = node
        
        # 親側からの√を差し替え
        if node.p.r is not None:
            if node.p.r.priority == node.priority:
                node.p.r = new
            else:
                node.p.l = new

        # 親側からの√を差し替え
        elif node.p.l is not None:
            if node.p.l.priority == node.priority:
                node.p.l = new
            else:
                node.p.r = new

        # 親差し替え
        new.p, node.p = node.p, new

        # 子から見た親の差し替え
        new.l.r.p = node


        return new

    def add(self, value, priority = None):
        ## 通常の二分探索木の要領で追加 ##
        now = self.tree
        if priority is None:
            priority = random.random()
        if value in self.dict:
            self.dict[value] += 1
            return
        else:
            self.dict[value] = 1
        while True:
            if now.value > value:
                if now.l.value is None: 
                    now.l = Node(value, self.leaf, priority, now)
                    now = now.l
                    break
                now = now.l
            else:
                if now.r.value is None:
                    now.r = Node(value, self.leaf, priority, now)
                    now = now.r
                    break
                now = now.r

        # print(now.p.value, now.p.l.value, now.p.r.value)
        # print(now.p.priority, now.p.l.priority, now.p.r.priority)
        # 木の回転でだいたい平衡にする
        self.__up_heap__(now)

    def delete(self, value):
        if value in self.dict:
            if self.dict[value] == 1:
                node = self.__search_delete_node__(value)
                self.__delete__(node)
                # 削除
                del self.dict[value]
                return True
            else:
                self.dict[value] -= 1
        else:
            return False

    def __search_delete_node__(self, value):
        now = self.tree
        while True:
            if now.value > value:
                now = now.l
            elif now.value < value:
                now = now.r
            else:
                return now

    def __delete__(self, node):
        while True:
        # 葉なら
            if node.l.value is None and node.r.value is None:
                if (node.p.r is not None) and (node.p.r.value == node.value): 
                    node.p.r = self.leaf
                elif (node.p.l is not None) and (node.p.l.value == node.value): 
                    node.p.l = self.leaf
                break            
            # 右のみ子を持つ場合左回転
            elif node.l.value is None and node.r.value is not None:
                node = self.__left_rotate__(node).l
            # 左のみ子を持つ場合右回転
            elif node.l.value is not None and node.r.value is None:
                node = self.__right_rotate__(node).r
            # 両方に子を持つ
            else:
                if node.l.priority > node.r.priority:
                    node = self.__right_rotate__(node).r
                else:
                    node = self.__left_rotate__(node).l


    def find(self, value):
        now = self.tree

        while True:
            if now.value > value:
                if now.l.value is None: 
                    break
                now = now.l
            elif now.value < value:
                if now.r.value is None:
                    break
                now = now.r
            
            # 値が一致
            else:
                return True

        return False
# end    
 