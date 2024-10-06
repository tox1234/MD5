import socket
from threading import Thread, Lock

ENCODE = "e04f7532963346f9edb86ef54125eea5"
QUEUE_SIZE = 10
IP = '0.0.0.0'
PORT = 8080

found = ('0', '0', "decrypt", ENCODE)
start = 0
end = 1000000
lock = Lock()
clients = []
printed = False


def send_protocol(start, end, cmd, encode):
    start_len = len(start)
    end_len = len(end)
    cmd_len = len(cmd)
    encode_len = len(encode)
    total_message = str(start_len) + '!' + start + str(end_len) + '!' + end + str(cmd_len) + '!' + cmd + str(
        encode_len) + "!" + encode
    total_message = total_message.encode()
    return total_message


def receive_protocol(client_socket):
    special_character = ''
    start_len = ''
    end_len = ''
    cmd_len = ''
    encode_len = ''
    try:
        while special_character != '!':
            special_character = client_socket.recv(1).decode()
            start_len += special_character
        start_len = start_len[:-1]

        start = client_socket.recv(int(start_len)).decode()

        special_character = ''

        while special_character != '!':
            special_character = client_socket.recv(1).decode()
            end_len += special_character
        end_len = end_len[:-1]

        end = client_socket.recv(int(end_len)).decode()

        special_character = ''

        while special_character != '!':
            special_character = client_socket.recv(1).decode()
            cmd_len += special_character
        cmd_len = cmd_len[:-1]

        cmd = client_socket.recv(int(cmd_len)).decode()

        special_character = ''

        while special_character != '!':
            special_character = client_socket.recv(1).decode()
            encode_len += special_character
        encode_len = encode_len[:-1]

        encode = client_socket.recv(int(encode_len)).decode()

        final_message = (start, end, cmd, encode)
    except socket.error:
        final_message = ('There was an error', '')
    return final_message


def handle_connection(client_socket, client_address):
    global found
    global start
    global end
    global printed
    """
    handle a connection
    :param client_socket: the connection socket
    :param client_address: the remote address
    :return: None
    """
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
                            clients.remove(client)
                    except socket.error:
                        pass
                break

    except Exception as e:
        print(e)
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
