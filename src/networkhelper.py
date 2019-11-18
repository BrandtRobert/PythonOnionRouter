import socket
import struct
from types import SimpleNamespace
from typing import List
import random


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
        msg = msg + '{} {}\n'.format(hop[0], hop[1])
    return msg
