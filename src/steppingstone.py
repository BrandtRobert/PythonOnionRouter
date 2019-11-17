import threading
import socket
import random
import struct
from types import SimpleNamespace
from typing import List
import os


def send_msg(client_con: socket.socket, req_type: str, msg: str):
    """
    Message format
    ----------------------
    msg_length   = 2 bytes
    request_type = 5 bytes
    msg_contents = msg_length - 5 bytes
    """
    length = socket.htons(len(msg))
    client_con.send(struct.pack('>H', length))
    client_con.send(req_type.encode('utf-8'))
    client_con.sendall(msg)


def receive_msg(client_con: socket.socket):
    """
    Message format
    ----------------------
    msg_length   = 2 bytes
    request_type = 5 bytes
    msg_contents = msg_length - 5 bytes
    """
    msg_length = socket.ntohs(int(client_con.recv(2)))
    request_type = client_con.recv(5)
    amount_read = 0
    # Force socket to read the whole msg length
    msg = ''
    while len(msg) < (msg_length - 5):
        msg = msg + client_con.recv(msg_length - 5).decode('utf-8')
    sn = SimpleNamespace()
    sn.request_type = request_type
    sn.msg_length = msg_length
    sn.msg = msg
    return msg


def get_next_hop(hops):
    return hops[random.randint() % len(hops)]


def parse_msg_hops(msg: str):
    hops = []
    for line in msg.splitlines():
        splits = line.split('\\w+')
        ip = splits[0]
        port = int(splits[1])
        hops.append((ip, port))
    return hops


def encode_relay_msg(url, hops: List):
    msg = url + '\n'
    for hop in hops:
        msg = msg + '{} {}'.format(hop[0], hop[1])
    return msg


def relay_msg(url, hops):
    conn_success = False
    while not conn_success:
        try:
            ip, port = get_next_hop(hops)
            hops.remove((ip, port))
            next_hop = socket.create_connection((ip, port))
            conn_success = True
        except:
            print('Failed to connect to {}:{}'.format(ip, port))
    send_msg(next_hop, type='RELAY', msg=encode_relay_msg(url, hops))
    return next_hop


def wget_content(url):
    exit_code = os.system('wget {}'.format(url))
    if exit_code != 0:
        return -1
    filename = url.split('/')[-1]
    with open(filename, 'r') as f:
        content = f.read()
        os.remove('filename')
        return content


def handle_new_connection(client_con: socket.socket):
    msg_contents = receive_msg(client_con)
    if msg_contents.request_type == 'RELAY':
        url = msg_contents.msg.splitlines()[0]
        hops: List = parse_msg_hops(msg_contents.msg[len(url):])
        if len(hops) > 0:
            next_hop_conn = relay_msg(url, hops)
            payload = receive_msg(next_hop_conn).msg
            send_msg(client_con, req_type='RESPN', msg=payload)
        else:
            content = wget_content(url)
            send_msg(client_con, req_type='RESPN', msg=content)
    else:
        client_con.close()


def start_async_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(5)
    connection_threads = []
    while True:
        try:
            new_client = server_socket.accept()
            new_client_thread = threading.Thread(target=handle_new_connection, args=(new_client, ), daemon=True)
            connection_threads.append(new_client_thread)
        except KeyboardInterrupt:
            print('Execution was interrupted, exiting now...')
            for thread in connection_threads:
                thread.join(2)
            exit(0)
