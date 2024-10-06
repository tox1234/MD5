"""
Author: Ido Shema
Date: 05/10/2024
Description: a simple protocol
"""

import socket


def send_protocol(start, end, cmd, encode):
    """
        sends the message as the protocol blueprint
        :param start: the start of the range of numbers
        :param end: the end of the range of numbers
        :param cmd: which cmd we want to do(encrypt,decrypt)
        :param encode: the encryption we want to match with
        :return: the message as the protocol blueprint
    """
    start_len = len(start)
    end_len = len(end)
    cmd_len = len(cmd)
    encode_len = len(encode)
    total_message = str(start_len) + '!' + start + str(end_len) + '!' + end + str(cmd_len) + '!' + cmd + str(
        encode_len) + "!" + encode
    total_message = total_message.encode()
    return total_message


def receive_protocol(client_socket):
    """
        receives the message and transfers it to tuple
        :param client_socket: the client socket
        :return: a tuple including the start end cmd and encode of the message
    """
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
