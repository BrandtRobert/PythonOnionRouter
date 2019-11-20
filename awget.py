from typing import List
import networkhelper
import socket
import sys
import argparse

def encode_relay_msg(url, hops: List):
    msg = url + '\n'
    for hop in hops:
        msg = msg + '{} {}\n'.format(hop[0], hop[1])
    return msg


def read_chainfile(txt: str):
    with open(txt, 'r') as f:
        # discard line
        f.readline()
        rest_of_msg = f.read()
    hops = networkhelper.parse_msg_hops(rest_of_msg)
    return hops


def awget(url: str, chainfilename: str):
    hops = read_chainfile(chainfilename)
    ip, port = networkhelper.get_next_hop(hops)
    hops.remove((ip, port))
    print('Forwarding wget to {}:{}'.format(ip, port))
    print('Attempting to connect to {}:{}'.format(ip, port))
    next_step_conn = socket.create_connection((ip, port))
    msg = networkhelper.encode_relay_msg(url, hops)
    networkhelper.send_msg(next_step_conn, req_type='RELAY', msg=msg)
    response: str = networkhelper.receive_msg(next_step_conn)
    print('Received url data from {}:{}'.format(ip, port))
    encoding = response.msg.splitlines()[0]
    content = response.msg[len(encoding):]
    filename = url.split('/')[-1]
    if filename == '' or '/' not in url:
        filename = 'index.html'
    with open(filename, 'w') as f:
        print('Writing content to file...')
        f.write(content)
    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='An anonymous wget program that uses a series of stepping stones to fetch a url')
    parser.add_argument('url', type=str, help='The specified url for awget to fetch')
    parser.add_argument('-c, --chain-file', type=str, default='chaingang.txt',
                        help='Name of the file specifying the onion chain (default is "chaingang.txt").'
                             'In the format:\n<number-entries>\n<ip-first-host> <port-first-host>\n...')
    args = parser.parse_args()
    awget(args.url, 'chainfile.txt')

