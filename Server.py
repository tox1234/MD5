"""
Author: Ido Shema
Date: 05/10/2024
Description: A simple server using threads to crack MD5
"""
import socket
from threading import Thread, Lock
from Protocol import send_protocol, receive_protocol

ENCODE = "EC9C0F7EDCC18A98B1F31853B1813301"
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080

found = ('0', '0', "decrypt", ENCODE)
start = 0
end = 1000000
lock = Lock()
clients = []
printed = False


def handle_connection(client_socket, client_address):
    """
        handle a connection
        :param client_socket: the connection socket
        :param client_address: the remote address
        :return: None
    """
    global found
    global start
    global end
    global printed
    try:
        print('New connection received from ' + client_address[0] + ':' + str(client_address[1]))
        while True:
            if found[2] == "decrypt":
                with lock:
                    client_start = start
                    client_end = end
                    start = end
                    end += 1000000
                client_socket.send(send_protocol(str(client_start), str(client_end), 'decrypt', ENCODE))
                found = receive_protocol(client_socket)
            else:
                if not printed:
                    printed = True
                    print("the decoded number is: " + found[0])
                for client in clients:
                    try:
                        if client != client_socket:
                            client.send(send_protocol(found[0], '0', 'encrypt', ENCODE))
                    except socket.error:
                        pass
                break

    except IndexError or socket.error:
        pass
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)

        while True:
            client_socket, client_address = server_socket.accept()
            thread = Thread(target=handle_connection,
                            args=(client_socket, client_address))
            clients.append(client_socket)
            thread.start()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
