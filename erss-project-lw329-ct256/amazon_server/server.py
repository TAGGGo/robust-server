from django.http import SimpleCookie
from request_handlers import *
from request_handlers import _sendProtoStr
import socket
import threading
import psycopg2
import sys


# WORLD_SIMULATOR = ("vcm-24667.vm.duke.edu", 23456)
WORLD_SIMULATOR = ("vcm-23974.vm.duke.edu", 23456)
# Change it to UPS destination machine
# UPS_SIMULATOR = ("vcm-24667.vm.duke.edu", 34567)
UPS_SIMULATOR = ("vcm-26366.vm.duke.edu", 34567)
WEBAPP_SIMULATOR = ("127.0.0.1", 5555)
TIME_TO_RECONNECT = 5


def connectToDatabase(host="localhost", password="passw0rd123"):
    conn = psycopg2.connect(host=host, database="postgres",
                            user="postgres", password=password, port="5432")
    return conn


def connectToServer(Simulator):
    connSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connSocket.connect(Simulator)
    return connSocket


def connectToServerRepetitivelyUntilSucceed(Simulator):
    global TIME_TO_RECONNECT
    while(1):
        try:
            connSocket = connectToServer(Simulator)
            print("Connected to {}, ready to handle request".format(Simulator))
            return connSocket
        except Exception:
            print("Failed to connect to socket {} retry...".format(Simulator))
            time.sleep(TIME_TO_RECONNECT)
        except KeyboardInterrupt:
            connSocket.close()
            break


def listenToGetSocketAndHandleRequest(Simulator, worldSocket, dbConn):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(Simulator)
        s.listen()
        while(1):
            connSocket, _ = s.accept()
            # Only when handleWebAppRequest fail will it accepts next socket
            print("RECEIVED CONNECTION FROM {}".format(connSocket))
            handleWebAppRequest(worldSocket, connSocket, dbConn)
    except (KeyboardInterrupt, Exception):
        s.close()
        dbConn.close()


def receiveWorldIdFromUps(upsSocket):
    u2aworldid = readProtoRsp(upsSocket, ups.U2AWorldId)
    assert(u2aworldid.HasFeild('worldid'))
    return u2aworldid.worldid


def main():
    global WORLD_SIMULATOR, UPS_SIMULATOR, WEBAPP_SIMULATOR
    # dbConn = connectToDatabase("db", "passw0rd123")
    dbConn = connectToDatabase("vcm-20519.vm.duke.edu", "passw0rd123")
    worldSocket = connectToServerRepetitivelyUntilSucceed(WORLD_SIMULATOR)
    upsSocket = connectToServerRepetitivelyUntilSucceed(UPS_SIMULATOR)
    thread1 = threading.Thread(
        target=handleWorldResponse, args=(worldSocket, upsSocket, dbConn))
    thread2 = threading.Thread(
        target=handleUPSResponse, args=(worldSocket, upsSocket, dbConn))
    thread3 = threading.Thread(target=listenToGetSocketAndHandleRequest, args=(
        WEBAPP_SIMULATOR, worldSocket, dbConn))
    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
    worldSocket.close()
    upsSocket.close()


if __name__ == "__main__":
    main()
