import hashlib
import socket
import threading
from os import cpu_count

HOST = '10.100.102.7'
PORT = 8080


def checker(start, end, encode):
    for i in range(start, end):
        test = hashlib.md5(str(i).encode())
        if test.hexdigest() == encode.lower():
            return send_protocol(str(i), '0', 'encrypt', encode)
    return send_protocol('0', '0', "decrypt", encode)


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


def client_thread(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        while True:
            response = receive_protocol(client)
            if len(response) != 0:
                if response[2] == 'encrypt':
                    client.send(send_protocol(response[0], '0', 'encrypt', response[-1]))
                    break
                else:
                    result = checker(int(response[0]), int(response[1]), response[-1])
                    client.send(result)

    except:
        print("Client disconnected.")
    finally:
        client.close()


if __name__ == "__main__":
    threads = []

    for i in range(cpu_count()):
        thread = threading.Thread(target=client_thread, args=(HOST, PORT))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
