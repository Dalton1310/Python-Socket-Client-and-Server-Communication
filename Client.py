from socket import *

HOST = "127.0.0.1"
PORT = 3321

sockets_Client = socket(AF_INET, SOCK_STREAM)
sockets_Client.connect((HOST, PORT))

while True:
    command = input("Enter command (MSGGET, MSGSTORE, QUIT, SHUTDOWN): ")
    #Client tries to enter the MSGGET command
    if command == "MSGGET":
        sockets_Client.sendall("MSGGET".encode())
        response = sockets_Client.recv(1024).decode()
        print(response)
    #Client tries to enter the MSGSTORE command
    elif command == "MSGSTORE":
        new_msgofday = input("Please enter the new message of the day: ")
        while new_msgofday in ["MSGGET", "MSGSTORE", "QUIT", "SHUTDOWN"]:
            print(f"Error, cannot use a command as a message, please enter a new message of the day:")
            new_msgofday = input("Please enter the new message of the day: ")
        sockets_Client.sendall(f"MSGSTORE {new_msgofday}".encode())
        response = sockets_Client.recv(1024).decode()
        print(response)
    #Client tries to enter the QUIT command    
    elif command == "QUIT":
        sockets_Client.sendall("QUIT".encode())
        response = sockets_Client.recv(1024).decode()
        print(response)
        sockets_Client.close()
        exit()
    #Client tries to enter the SHUTDOWN command
    elif command == "SHUTDOWN":
        sockets_Client.sendall("SHUTDOWN".encode())
        response = sockets_Client.recv(1024).decode()
        print(response)
        password = input("Please enter the password: ")
        sockets_Client.sendall(password.encode())
        response = sockets_Client.recv(1024).decode()
        print(response)
        if "200 OK" in response:
            print("Server successfully shut down. Client exiting.")
            sockets_Client.close()
            exit()
    else:
        print("Invalid command. Please enter any of the following: MSGGET, MSGSTORE, QUIT, or SHUTDOWN.")