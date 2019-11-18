from typing import List
import networkhelper
import socket
import sys


def encode_relay_msg(url, hops: List):
    msg = url + '\n'
    for hop in hops:
        msg = msg + '{} {}\n'.format(hop[0], hop[1])
    return msg


def read_chainfile(txt: str):
    with open(txt, 'r') as f:
        # discard line
        f.next()
        rest_of_msg = f.read()
    hops = networkhelper.parse_msg_hops(rest_of_msg)
    return hops


def awget(url: str, chainfilename: str):
    hops = read_chainfile(chainfilename)
    ip, port = networkhelper.get_next_hop(hops)
    hops.remove((ip, port))
    next_step_conn = socket.create_connection((ip, port))
    msg = networkhelper.encode_relay_msg(url, hops)
    networkhelper.send_msg(next_step_conn, req_type='RELAY', msg=msg)
    response: str = networkhelper.receive_msg(next_step_conn)
    encoding = response.splitlines()[0]
    content = response[len(encoding):]
    filename = url.split('/')[-1]
    if filename == '' or '/' not in url:
        filename = 'index.html'
    with open(filename, 'w') as f:
        f.write(content.encode(encoding))


if __name__ == "__main__":
    awget(sys.argv[1], 'chainfile.txt')

