import socket
import threading

HOST = '127.0.0.1' 
PORT = 13131

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)
        except:
            print("[ERROR] Disconnected from server.")
            client.close()
            break

def send_messages():
    while True:
        try:
            message = input()
            client.send(message.encode('utf-8'))
        except:
            print("[ERROR] Could not send message.")
            client.close()
            break

threading.Thread(target=receive_messages, daemon=True).start()
threading.Thread(target=send_messages).start()
