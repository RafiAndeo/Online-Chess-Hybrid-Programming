# server.py adalah file execute server untuk menjalankan server dari game

# import library socket untuk membuat socket
# import library pickle untuk mengirimkan objek melalui socket
# import library time untuk mengatur waktu
# import library threading untuk membuat thread
# import library board untuk mengimport class board

import socket
import pickle
import time
from threading import Thread
from board import Board

# mendefinisikan host dan port yang digunakan berdasarkan ip address dan port yang telah ditentukan dari Radmin VPN

host = "26.122.184.85"
port = 10000
address = (host, port)

# mendefinisikan socket server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
server.listen()

boards = []
sockets = []
list_names = []
client_connection = 0

# membuat function client thread untuk menerima command dari client dan mengirimkannya ke client lainnya


def client_thread(client: socket.socket, board: Board, connection: int):
    global client_connection

    if connection % 2 == 0:
        number_clients = connection + 1
        while number_clients >= len(sockets):
            continue
    else:
        number_clients = connection - 1

    user = client.recv(1024).decode("utf-8")
    list_names.append(user)
    board.set_name(user)
    time.sleep(1)

    client.send(pickle.dumps(board))

    while True:
        try:
            command = client.recv(4096)
            board.command(pickle.loads(command))
            sockets[number_clients].send(command)
        except (ConnectionResetError, ConnectionAbortedError, EOFError):
            client.close()
            sockets[number_clients].close()
            print("Client disconnected")
            client_connection = client_connection - 1
            if client_connection == 0:
                print("All Clients are disconnected")
            return

# membuat function main untuk menjalankan server


if __name__ == "__main__":
    print("Server is running...")

    while True:
        client, addr = server.accept()
        sockets.append(client)
        client_connection = client_connection + 1

        if (len(sockets) - 1) // 2 >= len(boards):
            boards.append(Board())

        thread = Thread(target=client_thread, args=(
            client, boards[-1], len(sockets) - 1))
        thread.start()
