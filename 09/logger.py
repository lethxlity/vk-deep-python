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
    def __init__(self, logger_name, limit=42):
        self.log = logging.getLogger(logger_name)
        if limit <= 0:
            self.log.error(f"raised creating cache, "
                          f"limit must be > 0,"
                          f" current limit value: {limit}")
            raise ValueError
        self.dict = {}
        self.limit = limit
        self.head = ListNode(0, None)
        self.tail = ListNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

        self.log.debug(f"Cache created, size: {limit}")

    def get(self, key):
        if key in self.dict:
            node = self.dict[key]
            self.remove_from_list(node)
            self.insert_to_head(node)
            self.log.info(f"GET value: {node.val}, key: {key}, SUCCESS")
            return node.val
        self.log.info(f"GET value: {None}, key: {key}, NO KEY")
        return None

    def set(self, key, val):
        if key in self.dict:
            node = self.dict[key]
            self.remove_from_list(node)
            self.insert_to_head(node)
            node.val = val
            self.log.info(f"SET value: {val}, EXISTING key: {key}, SUCCESS")

        else:
            if len(self.dict) >= self.limit:
                self.log.info(f"--------CAPACITY EXCEEDED--------")
                self.remove_from_tail()
            node = ListNode(key, val)
            self.dict[key] = node
            self.insert_to_head(node)
        self.log.info(f"SET value: {val}, NEW key: {key}, SUCCESS")

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

    logger = logging.getLogger('my_logger')
    formatter1 = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    formatter2 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(filename="cache.log",
                                       mode="w",
                                       encoding="utf-8")
    file_handler.setFormatter(formatter1)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(formatter2)

    if filt:
        file_handler.addFilter(CustomFilter())
        stream_handler.addFilter(CustomFilter())
    handlers = [file_handler]
    if sout_logging:
        handlers.append(stream_handler)
    logging.basicConfig(level=logging.DEBUG,
                        handlers=handlers)

    cache = LRUCache('my_logger', 2)
    cache.set("k1", "aaa")
    cache.set("k2", "val2")
    cache.set("k3", "val3")

    cache.get("k1")
    cache.get("k2")
    cache.get("k3")
    try:
        cache2 = LRUCache('my_logger', -1)
    except ValueError:
        pass
