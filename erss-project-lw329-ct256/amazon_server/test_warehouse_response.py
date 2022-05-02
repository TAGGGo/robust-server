from email.message import Message
from sqlite3 import connect
from world_ups_pb2 import UConnect
from world_amazon_pb2 import *
from world_ups_pb2 import *
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import socket

def sendProtoStr(toSocket, protoClass):
    msg = protoClass.SerializeToString()
    _EncodeVarint(toSocket.send, len(msg), None)
    toSocket.send(protoClass.SerializeToString())

def readProtoStr(fromSocket):
    var_int_buff = []
    while True:
        buf = fromSocket.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    return fromSocket.recv(msg_len)


if __name__ == "__main__":
    WORLD_WAREHOUSE_SIMULATOR = (socket.gethostname(), 23456)
    WORLD_TRUCK_SIMULATOR = (socket.gethostname(), 12345)

    worldWareHouseSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worldWareHouseSocket.connect(WORLD_WAREHOUSE_SIMULATOR)
    worldTruckSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worldTruckSocket.connect(WORLD_TRUCK_SIMULATOR)

    connectReq = UConnect()
    connectReq.isAmazon = False
    sendProtoStr(worldTruckSocket, connectReq)
    msg = readProtoStr(worldTruckSocket)
    connected = UConnected()
    connected.ParseFromString(msg)
    print(connected)

# connectReq = world_amazon_pb2.AConnect()
# connectReq.isAmazon = True
 
# worldWareHouseSocket.send(connectReq.SerializeToString())

# res = worldWareHouseSocket.recv(1024)
# print(res.decode())
# connectedRsp = world_amazon_pb2.AConnected()
# connectedRsp.ParseFromString(res)
# print(connectedRsp)
 
# Acommand = world_amazon_pb2.ACommands()
# APurchase = world_amazon_pb2.APurchaseMore()

# APurchase.whnum = 1
# thing = APurchase.AProduct.add()
# thing.id = 1
# thing.description = "apple watch"
# thing.count = 3

# APurchase.seqnum = 1

