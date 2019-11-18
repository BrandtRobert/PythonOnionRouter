import threading
import socket
from typing import List
import sys
import requests
from networkhelper import *


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
    if not url.startswith('http://'):
        url = 'http://' + url
    if url[-1] == '/':
        url = url + '/'
    r = requests.get(url, verify=False)
    return r.encoding, r.text


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
            encoding, txt = wget_content(url)
            content = str(encoding) + "\n" + txt
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


if __name__ == "__main__":
    encoding, txt = wget_content(sys.argv[1])
    print(txt)