from socket import *

HOST = "127.0.0.1"
PORT = 3321
flag = 0
msgofday = "Yet another message of the day!"
passcode = "123"
socketsServer = socket(AF_INET, SOCK_STREAM)
socketsServer.bind((HOST, PORT))
socketsServer.listen()
print(f"Server is listening to port {PORT}")

while True:
    connThread, address = socketsServer.accept()
    with connThread:
        print(f"Connected by {address}")
        while True:
            data = connThread.recv(1024).decode()
            print(f"Data Received: {data}")
            #Client enters the message "MSGGET"
            if data == "MSGGET":
                connThread.sendall(f"200 OK\n{msgofday}\n".encode())
            #Client enters the message "MSGSTORE"
            elif data.startswith("MSGSTORE"):
                new_msgofday = data[9:]
                msgofday = new_msgofday.strip()
                connThread.sendall("200 OK\n".encode())
            #Client enters the message "QUIT"
            elif data == "QUIT":
                connThread.sendall(b"200 OK\n")
                connThread.close()
                print("Connection with " + str(address) + " closed.")
                break
            #Client enters the message "SHUTDOWN"
            elif data == "SHUTDOWN":
                connThread.sendall(b"300 PASSWORD REQUIRED\n")
                password_attempt = connThread.recv(1024).decode()
                if password_attempt == passcode:
                    connThread.sendall(b"200 OK\n")
                    socketsServer.close()
                    print("Server shutdown initiated.")
                    exit()
                else:
                    #Error for if the password is wrong
                    connThread.sendall(b"301 WRONG PASSWORD\n")
            else:
                #Error for any failed request
                connThread.sendall(b"400 BAD REQUEST\n")