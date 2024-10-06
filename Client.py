"""
Author: Ido Shema
Date: 05/10/2024
Description: A simple client using threads to crack MD5
"""

import hashlib
import socket
import threading
from os import cpu_count
from Protocol import send_protocol, receive_protocol

HOST = '10.101.112.7'
PORT = 8080


def checker(start, end, encode):
    """
        checks if the MD5 of a range of numbers matches the MD5 encryption we are looking for
        :param start: the start of the range of numbers
        :param end: the end of the range of numbers
        :param encode: the encryption we want to match with
        :return: the results using protocol
    """
    for i_ in range(start, end):
        test = hashlib.md5(str(i_).encode())
        if test.hexdigest() == encode.lower():
            return send_protocol(str(i_), '0', 'encrypt', encode)
    return send_protocol('0', '0', "decrypt", encode)


def client_thread(host, port):
    """
        the thread of the client
        :param host: host ip
        :param port: port of the program
        :return: None
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        while True:
            response = receive_protocol(client)
            if len(response) != 0:
                if response[2] == 'encrypt':
                    break
                else:
                    result = checker(int(response[0]), int(response[1]), response[-1])
                    client.send(result)
                    if 'encrypt' in result.decode():
                        break

    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        print("client disconnected")
        client.close()


def main():
    threads = []

    for i in range(cpu_count()):
        thread = threading.Thread(target=client_thread, args=(HOST, PORT))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
