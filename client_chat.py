import socket
import select
import sys

HOST = '127.0.0.1'
PORT = 1337

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Send anytime \"q\" to leave")
print("To send private message, type: \"/private to [username] [message]\"")
username = input("Write username: ")
if username == "q":
    client.close()
    exit("Goodbye!")
client.connect((HOST, PORT))
client.send(bytearray(username, encoding='utf-8'))
status = client.recv(1024)
status = status.decode()
print(status)
while True:
    # message = input("You: ")
    # if message:
    #     client.send(bytearray(username + ": " + message, encoding='utf-8'))
    # response = client.recv(1024)
    # response = response.decode()
    # print(response)

    socket_list = [sys.stdin, client]
    read_sockets, write_socket, error_socket = select.select(socket_list, [], [])
    for sc in read_sockets:
        if sc == client:
            response = client.recv(1024)
            response = response.decode()
            print(response)
        else:
            message = sys.stdin.readline().rstrip()
            if message == "q":
                client.send(bytearray(username + ": " + message, encoding='utf-8'))
                client.close()
                exit("Goodbye!")
            client.send(bytearray(username + ": " + message, encoding='utf-8'))
            sys.stdout.write(f"You: {message}\n")
            sys.stdout.flush()

# client.close()