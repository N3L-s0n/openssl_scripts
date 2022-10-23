import socket

def client_program():
    host = socket.gethostname()
    port = 5000
    client_socket = socket.socket()
    #client_socket.connect((host, port))
    client_socket.connect(('172.16.202.21', port))

    request = input("File Name:")
    client_socket.send(request.encode())
    request = input("Private key passphrase:")
    client_socket.send(request.encode())
    request = input("Organization Name:")
    client_socket.send(request.encode())
    request = input("Organization Unit Name:")
    client_socket.send(request.encode())
    request = input("Common Name:")
    client_socket.send(request.encode())
    request = input("Subject Alternative Name Data (separete with ',' if more than one):")
    client_socket.send(request.encode())

    client_socket.close()


if __name__ == '__main__':
    client_program()
