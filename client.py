import socket

# Function to connect to the server
def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.0.195', 2444))
    return client

# Function to send commands to the server
def send_command(client, command):
    client.send(command.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(response)

# Main client code
def start_client():
    client = connect_to_server()

    while True:
        command = input("Enter command (or 'exit' to quit): ")
        if command.lower() == 'exit':
            break

        send_command(client, command)

    client.close()

# Start the client
start_client()

