import socket
import threading

# Configuración del servidor
host = '127.0.0.1'
port = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado con {str(address)}!")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname del cliente es {nickname}!")
        broadcast(f"{nickname} se ha unido al chat!".encode('utf-8'), client)
        client.send("Conectado al servidor!".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
