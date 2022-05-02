from multiprocessing import Process
import psycopg2
import os
import socket
from XMLparser import XMLparser

num_of_processes = 8
processes = []
PORT = 12345

def receiveStr(sfile):
    num = sfile.readline()
    if num != "":
        return sfile.read(int(num))
    raise Exception("received nothing")

def handle_request(fd, client_address, parser):
    #print("received connection from "+ str(client_address))
    sfile = fd.makefile("rw")
    msg = receiveStr(sfile)
    #print(msg)
    return_msg = parser.parse(msg)
    sfile.write(return_msg)
    return

def accept_requests(serversocket, trans_id):
    conn = psycopg2.connect(database="stockexchange", user="postgres", password="123456", host="db", port="5432")
    parser = XMLparser(conn, trans_id)
    while True:
        fd, client_address = serversocket.accept()
        handle_request(fd, client_address, parser)

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), PORT))
    serversocket.listen(5)

    for i in range(num_of_processes):
        tmp = int((i+1) * 1e3)
        p = Process(target=accept_requests, args=(serversocket, tmp))
        p.deamon = True
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()

