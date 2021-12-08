import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

# SERVER = "192.168.1.203"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = {}

def broadcast(message):
    for name in clients.keys():
        clients[name].send(message)

def handle_client(conn, addr):
    print(f"New client connected. Address: {addr} ")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length is not None:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == "!DISCONNECT":
                connected = False
            print(f"{addr}: {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()

def receive():
    while True:
        conn, addr = server.accept()
        print(f"Connected with {str(addr)}")

        conn.send("NICK".encode(FORMAT))
        nickname = conn.recv(1024)

        clients[nickname] = conn

        print(f"Nickname: {nickname}")
        broadcast(f"{nickname} entered the chat room")

        conn.send("Connected to the chat room".encode(FORMAT))


def start():
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"Number of active connections: {threading.active_count() - 1}")


print("Starting the server...")
start()