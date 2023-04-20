class ListNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, limit=42):
        if limit <= 0:
            raise ValueError
        self.dict = {}
        self.limit = limit
        self.head = ListNode(0, None)
        self.tail = ListNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.dict:
            node = self.dict[key]
            self.remove_from_list(node)
            self.insert_to_head(node)
            return node.val
        return None

    def set(self, key, val):
        if key in self.dict:
            node = self.dict[key]
            self.remove_from_list(node)
            self.insert_to_head(node)
            node.val = val
        else:
            if len(self.dict) >= self.limit:
                self.remove_from_tail()
            node = ListNode(key, val)
            self.dict[key] = node
            self.insert_to_head(node)

    def remove_from_list(self, node: ListNode):
        node.prev.next = node.next
        node.next.prev = node.prev

    def insert_to_head(self, node: ListNode):
        temp = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = temp
        temp.prev = node

    def remove_from_tail(self):
        if len(self.dict) == 0:
            return
        tail = self.tail.prev
        self.dict.pop(tail.key)
        self.remove_from_list(tail)
