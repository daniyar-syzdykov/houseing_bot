import time
import socket
import random
import sys
from threading import Thread
import selectors

def doubler_server(port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.setblocking(False)
        s.listen(5)
        sel = selectors.DefaultSelector()
        sel.register(s, selectors.EVENT_READ)
        while True:
            for key, mask in sel.select():
                if key.fileobj is s:
                    conn, addr = s.accept()
                    print('Connected by: ', addr)
                    conn.setblocking(False)
                    sel.register(conn, selectors.EVENT_READ, ("read", None))
                else:
                    conn = key.fileobj 
                    op, arg = key.data
                    sel.unregister(conn)
                    if op == "read":
                        data = conn.recv(1024)
                        if not data:
                            conn.close()
                        n = int(data.decode())
                        res = f'{n*2}\n'.encode()
                        sel.register(conn, selectors.EVENT_WRITE, ("write", res))
                    elif op == "write":
                        conn.send(arg) 
                        sel.register(conn, selectors.EVENT_READ, ("read", None))
                    else:
                        assert False, op
    


def handle_connection(conn, addr):
    #print("Connected by: ", addr)
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            n = int(data.decode())
            res = f'{n*2}\n'.encode()
            conn.send(res)

def doubler_client(port=8080):
    with socket.create_connection(("127.0.0.1", port)) as s:
        f = s.makefile(mode="rw", buffering=1, newline="\n")
        for _ in range(100):
            n = random.randrange(10)
            f.write(f"{n}\n")
            print(n)
            print(n, f.readline().strip())

def clients():
    threads = [Thread(target=doubler_client) for _ in range(1000)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    if sys.argv[1] == 'server':
        doubler_server()
    elif sys.argv[1] == 'thread_clients':
        clients()
    elif sys.argv[1] == 'client':
        doubler_client()
