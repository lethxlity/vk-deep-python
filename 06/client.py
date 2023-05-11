import socket
import threading
import sys
import queue


class SenderReciever(threading.Thread):

    end = "#END#".encode("utf-8")

    def __init__(self, address):
        threading.Thread.__init__(self)
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address

    def run(self):
        self.client_sock.connect(self.address)
        q_empty = False
        end_of_recv = False
        while not q_empty:
            try:
                self.client_sock.sendall(q.get_nowait().encode("utf8"))
            except Exception:
                q_empty = True
                self.client_sock.sendall(SenderReciever.end)
        while not end_of_recv:
            data = self.client_sock.recv(1024).decode()
            if "#END#" in data:
                end_of_recv = True
                if data != "#END#":
                    print(data.replace("#END#", ''))
            else:
                print(data)


if __name__ == "__main__":
    q = queue.Queue()
    urls = open(sys.argv[2], "r", encoding="utf8")

    for url in urls:
        q.put(url)

    for i in range(int(sys.argv[1])):
        new_sender = SenderReciever(("localhost", 15000))
        new_sender.start()
