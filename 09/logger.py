import logging
import sys


class ListNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class CustomFilter(logging.Filter):
    def filter(self, record):
        l = len(record.msg)
        msg = ""
        if l < 80:
            for i in range(80 - l):
                msg += "-"
        record.msg = msg + record.msg
        return True


class LRUCache:
    file_handler = logging.FileHandler(filename="cache.log",
                                       mode="w",
                                       encoding="utf-8")
    stream_handler = logging.StreamHandler(stream=sys.stdout)

    def __init__(self, limit=42, sout_logging=False, filt=False):
        if filt:
            LRUCache.file_handler.addFilter(CustomFilter())
            LRUCache.stream_handler.addFilter(CustomFilter())
        else:
            LRUCache.file_handler.removeFilter(CustomFilter())
            LRUCache.stream_handler.removeFilter(CustomFilter())
        handlers = [LRUCache.file_handler]
        if sout_logging:
            handlers.append(LRUCache.stream_handler)
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s %(levelname)s %(message)s",
                            handlers=handlers)
        if limit <= 0:
            logging.error(f"raised creating cache, "
                          f"limit must be > 0,"
                          f" current limit value: {limit}")
            raise ValueError
        self.dict = {}
        self.limit = limit
        self.head = ListNode(0, None)
        self.tail = ListNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

        logging.debug(f"Cache created, size: {limit}")

    def get(self, key):
        if key in self.dict:
            node = self.dict[key]
            self.remove_from_list(node)
            self.insert_to_head(node)
            logging.info(f"GET value: {node.val}, key: {key}, SUCCESS")
            return node.val
        logging.info(f"GET value: {None}, key: {key}, NO KEY")
        return None

    def set(self, key, val):
        if key in self.dict:
            node = self.dict[key]
            self.remove_from_list(node)
            self.insert_to_head(node)
            node.val = val
            logging.info(f"SET value: {val}, EXISTING key: {key}, SUCCESS")

        else:
            if len(self.dict) >= self.limit:
                logging.info(f"--------CAPACITY EXCEEDED--------")
                self.remove_from_tail()
            node = ListNode(key, val)
            self.dict[key] = node
            self.insert_to_head(node)
        logging.info(f"SET value: {val}, NEW key: {key}, SUCCESS")

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


if __name__ == "__main__":
    opts = sys.argv[1:]
    sout_logging = False
    filt = False
    for opt in opts:
        if opt == "-s":
            sout_logging = True
        elif opt == "-f":
            filt = True
    cache = LRUCache(2, sout_logging, filt)
    cache.set("k1", "aaa")
    cache.set("k2", "val2")
    cache.set("k3", "val3")

    cache.get("k1")
    cache.get("k2")
    cache.get("k3")
    try:
        cache2 = LRUCache(-1)
    except ValueError:
        pass
