import queue
import socket
import sys
import getopt
import threading
import re
import itertools
import requests
import json
from bs4 import BeautifulSoup


def parseurl(url, n_words):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.get_text()

    words = re.split(r"[ ,\n.()-/]+", text)
    dct = {}
    for word in words:
        if word.lower() not in dct:
            dct[word.lower()] = 0
        dct[word.lower()] += 1
    dct.pop("")
    sorted_tuples = sorted(dct.items(), key=lambda item: item[1], reverse=True)
    dct = {k: v for k, v in sorted_tuples}
    if len(dct) > n_words:
        return dict(itertools.islice(dct.items(), n_words))
    else:
        return dct


class ClientHandler(threading.Thread):

    total = 0

    end = "#END#".encode("utf-8")

    def __init__(self, socket, address):
        threading.Thread.__init__(self, name=f"{address} handler")
        self.client_socket = socket
        self.client_address = address

    def run(self):
        url_counter = 0
        end_of_recv = False
        buffer = ""
        while not end_of_recv:
            data = self.client_socket.recv(1024).decode()
            if "#END#" in data:
                end_of_recv = True
            buffer += data
        buffer = buffer.split('\n')
        buffer.remove("#END#")
        for url in buffer:
            q_in.put((self.client_address, url))
            url_counter += 1
        while url_counter:
            try:
                response = q_out[self.client_address].get()
                self.client_socket.sendall(json.dumps(response).encode(('utf-8')))
                url_counter -= 1
                ClientHandler.total += 1
                print(f"Urls processed: {ClientHandler.total}")
            except Exception:
                pass
        self.client_socket.sendall(ClientHandler.end)
        q_out.pop(self.client_address)


class Worker(threading.Thread):

    def __init__(self, worker_id):
        threading.Thread.__init__(self, name=f"Worker{worker_id}")

    def run(self):
        while True:
            try:
                address, url = q_in.get_nowait()
                result = parseurl(url, n_words)
                q_out[address].put(url + ": " + str(result))
            except Exception:
                pass


class Master(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name=Master)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.bind(("localhost", 15000))

    def run(self):
        print("Server started")
        print("Waiting for client request..")
        while True:
            self.server_sock.listen()
            client_sock, client_addr = self.server_sock.accept()
            new_client_handler = ClientHandler(client_sock, client_addr)
            if client_addr not in q_out:
                q_out[client_addr] = queue.Queue()
            new_client_handler.start()


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "w:k:")
    for opt, arg in opts:
        if opt == "-w":
            print("Number of workers:", arg)
            n_workers = int(arg)

        elif opt == "-k":
            print("Number of top rep. words:", arg)
            n_words = int(arg)
    q_in = queue.Queue()
    q_out = {}

    for i in range(n_workers):
        worker = Worker(i)
        worker.daemon = True
        worker.start()

    master = Master()
    master.start()
