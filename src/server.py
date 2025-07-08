import socket
import threading

HOST = '127.0.0.1'
PORT = 13131

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                remove_client(client)

def handle_client(client, address):
    while True:
        try:
            message = client.recv(1024)
            if message:
                print(f"[{address}] {message.decode('utf-8')}")
                broadcast(message, sender_socket=client)
        except:
            remove_client(client)
            break

def remove_client(client):
    if client in clients:
        clients.remove(client)
        client.close()

def receive_connections():
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

if __name__ == "__main__":
    receive_connections()