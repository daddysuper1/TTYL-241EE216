import socket
import threading

HOST = '127.0.0.1'
PORT = 13131

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = {}  

def broadcast(message, sender_socket=None, tag_self=None):
    for client in clients:
        try:
            if client == sender_socket:
                if tag_self:
                    client.send(f"You: {tag_self}".encode('utf-8'))
            else:
                client.send(message)
        except:
            remove_client(client)

def handle_client(client, address):
    try:
        while True:
            client.send(b"[SERVER] Enter a unique username: ")
            username = client.recv(1024).decode('utf-8').strip()

            if username and username not in usernames.values():
                usernames[client] = username
                break
            else:
                client.send(b"[SERVER] Username already taken or invalid. Try again.\n")

        clients.append(client)
        print(f"[+] {username} connected from {address}")
        client.send(f"[SERVER] Welcome, {username}!".encode('utf-8'))

        while True:
            message = client.recv(1024)
            if message:
                decoded = message.decode('utf-8')
                print(f"[{username}] {decoded}")
                broadcast(f"{username}: {decoded}".encode('utf-8'), sender_socket=client, tag_self=decoded)
    except:
        remove_client(client)

def remove_client(client):
    if client in clients:
        username = usernames.get(client, "Unknown")
        print(f"[-] {username} disconnected")
        clients.remove(client)
        del usernames[client]
        client.close()

def receive_connections():
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

if __name__ == "__main__":
    receive_connections()