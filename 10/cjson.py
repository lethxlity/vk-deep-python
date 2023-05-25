import time
import json
import ujson

import cutils

def main():
    with open('data2.txt', 'r') as file:
        data = file.read().replace('\n', ' ')

        t_1 = time.time()
        json_doc = cutils.loads(data)
        json_str = cutils.dumps(json_doc)
        print("My json module", time.time() - t_1)

        t_1 = time.time()
        json_doc = json.loads(data)
        json_str = json.dumps(json_doc)
        print("Default json module", time.time() - t_1)

        t_1 = time.time()
        json_doc = ujson.loads(data)
        json_str = ujson.dumps(json_doc)
        print("Ultra json module", time.time() - t_1)


if __name__ == "__main__":
    main()
    print("Вывод по анализу времени выполнения - самостоятельно реализованный модуль отвратителен, "
          "проигрывает по времени выполнения в 2-3 раза")
