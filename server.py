import threading
import socket

clients = (
    []
)  # tuple with first element as a soc obj and second element is client name ( provided by client )
nick_names = []
Socket = socket.socket()
Socket.bind(
    ("localhost", 12345)
)  # bind socket to ip add- localhost and arbitrary available port no

Socket.listen(5)


def broadcast(msg):
    for client in clients:
        client.send(msg)


# handle msg from clients
def msg_handler(client):
    while True:
        try:
            # broadcast msg
            msg = client.recv(1024)
            broadcast(msg)
        except Exception as e:
            indx = clients.index(client)
            clients.remove(client)
            client.close()

            broadcast(f"{nick_names[indx]} left due to {e}".encode())
            nick_names.remove(nick_names[indx])
            break


def receive():
    while True:
        client, client_ip = Socket.accept()
        print(f"Connected with {client_ip}")
        client.send("NICK NAME:".encode())
        nickName = client.recv(1024).decode()
        clients.append(client)
        nick_names.append(nickName)

        print(f"Nick name is: {nickName}")

        broadcast(f"Nick Name {nickName} joined".encode())

        client.send("Connected to Server!!".encode())
        thread = threading.Thread(target=msg_handler, args=(client,))
        thread.start()


receive()
