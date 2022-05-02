import os
import socket
from XMLgenerator import *
import time,sys
from multiprocessing import Process

HOST = "127.0.0.1"
PORT = 12345
BUFFERSIZE = 8192
num_of_processes = 20
processes = []
from signal import signal, SIGINT
from sys import exit
def handler(signal_received, frame):
    # Handle any cleanup here
    # svsocket.close()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

def sendStr(sock, xmlmessage):
    # xmlmessage = str(int(len(xmlmessage))) + "\n" + xmlmessage
    # print(xmlmessage)
    sock.sendall(xmlmessage.encode('UTF-8'))

def test_one_piece(test_script):
    # instantiate a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the socket
    sock.connect((socket.gethostname(), PORT))    # Note: if execution gets here before the server starts up, this line will cause a crash
    # print('socket connected')

    sendStr(sock, test_script)
    msg = sock.recv(BUFFERSIZE)
    msg = msg.decode('UTF-8')
    # print(msg)
    sock.close()

# Used for correctness testing
def testcase1():
    testcases = [account_generator(1, 100000, [["AAPL",100],["GOOG",200]]), 
                account_generator(2, 100000, [["AAPL",200],["GOOG",100]]),
                trans_generator(1, [["order","AAPL",-50,100]]),
                trans_generator(2, [["order","AAPL",50,100]]),
                trans_generator(1, [["query",1000]]),
                trans_generator(2, [["query",1001]]),
                trans_generator(1, [["cancel",1000]]),
                trans_generator(2, [["cancel",1001]])]
    for test_script in testcases:
        test_one_piece(test_script)

# Used for connectness testing
def testcase2():
    init_orders = []
    times = 3
    for i in range(times):
        init_orders.append([chr(ord('A')+i), 20])
    buy_orders = []
    sell_orders = []
    querys = []
    cancels = []
    for i in range(times):
        buy_orders.append(["order", chr(ord('A')+i), 10, 100])
        sell_orders.append(["order", chr(ord('A')+i), -15, 90+i])
    for i in range(2*times):
        querys.append(["query", 1000+i])
        cancels.append(["cancel", 1000+i])
    testcases = [account_generator(1, 100000, init_orders),
                account_generator(2, 100000, init_orders),
                account_generator(3, 100000, init_orders),
                trans_generator(3, buy_orders),
                trans_generator(2, buy_orders),
                trans_generator(1, buy_orders),
                trans_generator(2, sell_orders),
                trans_generator(1, querys),
                trans_generator(2, querys)]
    for test_script in testcases:
        test_one_piece(test_script)

def testcase2_2():
    init_orders = []
    times = 1
    for i in range(times):
        init_orders.append([chr(ord('A')+i), 20])
    buy_orders = []
    sell_orders = []
    querys = []
    cancels = []
    for i in range(times):
        buy_orders.append(["order", chr(ord('A')+i), 15, 100])
        sell_orders.append(["order", chr(ord('A')+i), -10, 90+i])
    for i in range(2*times):
        querys.append(["query", 1000+i])
        cancels.append(["cancel", 1000+i])
    testcases = [account_generator(1, 100000, init_orders),
                account_generator(2, 100000, init_orders),
                account_generator(3, 100000, init_orders),
                trans_generator(3, sell_orders),
                trans_generator(2, sell_orders),
                trans_generator(1, sell_orders),
                trans_generator(2, buy_orders),
                trans_generator(1, querys),
                trans_generator(2, querys)]
    for test_script in testcases:
        test_one_piece(test_script)

# Used for time testing
def testcase3(base_id, times):
    for i in range(times):
        test_one_piece(account_generator(base_id + i, 10000, []))

def test_time(base_id, times):
    testcase3(base_id, times)


def main(times = 1000):
    print("testing times for " + str(times*num_of_processes))
    start_time = time.time()
    for i in range(num_of_processes):
        base_id = int(i * times)
        p = Process(target=test_time, args=(base_id, times))
        p.start()
        # print("Client %s starts...", i)
        processes.append(p)

    for p in processes:
        p.join()
    
    stop_time = time.time()
    diff = stop_time - start_time
    print("Time elapsed: " + str(diff))
    print("Speed is {} quries/s".format(1000 * num_of_processes / diff))

if __name__ == '__main__':
    signal(SIGINT, handler)
    if len(sys.argv) == 2:
        num_of_processes = int(sys.argv[1])
    main(7000)