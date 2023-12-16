import socket 
import threading

nickName=input("Choose your Nick Name: ")

client=socket.socket()
client.connect(('localhost',12345))

def receive():
    while True:

        try:
            msg=client.recv(1024).decode()
            if msg=="NICK NAME:":
                client.send(nickName.encode())
            else:
                print(msg)
        except:

            print("Error occured")
            client.close()

            break

def write():
    while True:
        msg=f"{nickName}: {input()}"
        client.send(msg.encode())


threading.Thread(target=receive).start()
threading.Thread(target=write).start()

