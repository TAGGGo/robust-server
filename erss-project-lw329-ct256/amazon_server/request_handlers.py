import world_amazon_pb2 as world
import amazon_ups_pb2 as ups
import amazon_webapp_pb2 as webapp
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint, _VarintBytes
import socket
import threading
import time
import order_status
import traceback
from concurrent.futures import ThreadPoolExecutor

# for generator
sequenceNum = 0
SEQNUM_GENERATOR_LOCK = threading.Lock()

# for resend loop
resendTimeWait = 5

# lock for socket.sendall() with size appended
WRITE_TO_WORLD_LOCK = threading.Lock()
WRITE_TO_UPS_LOCK = threading.Lock()

# world ASK filter: recording status of sending sequence number
WORLD_WAITING_ACKS_QUEUE = set()
WORLD_WAITING_ACKS_QUEUE_LOCK = threading.Lock()

# ups ASK filter
UPS_WAITING_ACKS_QUEUE = set()
UPS_WAITING_ACKS_QUEUE_LOCK = threading.Lock()

# world sequence number filter: recording status of receiving sequence number
WORLD_SEQNUM_RECEIVED_QUEUE = set()
WORLD_SEQNUM_RECEIVED_QUEUE_LOCK = threading.Lock()

# ups sequence number filter
UPS_SEQNUM_RECEIVED_QUEUE = set()
UPS_SEQNUM_RECEIVED_QUEUE_LOCK = threading.Lock()

# orderId purchasemore record dict and set
seqNumberToOrderIdDict = dict()
ORDER_PURCHASED_SET = set()
ORDER_PURCHASED_SET_LOCK = threading.Lock()


def _sendProtoStr(toSocket, command):
    msg = command.SerializeToString()
    _EncodeVarint(toSocket.send, len(msg), None)
    toSocket.send(msg)


def _readProtoDelimitedBySizeWithType(fromSocket, protoType):
    var_int_buff = []
    while True:
        buf = fromSocket.recv(1)
        var_int_buff += buf
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        if new_pos != 0:
            break
    ans = protoType()
    msg = fromSocket.recv(msg_len)
    ans.ParseFromString(msg)
    return ans


def readProtoRsp(fromSocket, protoType, fromWorld=True):
    return _readProtoDelimitedBySizeWithType(fromSocket, protoType)


def _generateSeqNum(queueLock, queue):
    global sequenceNum
    with SEQNUM_GENERATOR_LOCK:
        sequenceNum += 1
        seqNum = sequenceNum
    with queueLock:
        queue.add(sequenceNum)
    return seqNum


def generateSeqNum(toWorld=True):
    global WORLD_WAITING_ACKS_QUEUE_LOCK, WORLD_WAITING_ACKS_QUEUE, UPS_WAITING_ACKS_QUEUE_LOCK, UPS_WAITING_ACKS_QUEUE
    if toWorld:
        return _generateSeqNum(WORLD_WAITING_ACKS_QUEUE_LOCK, WORLD_WAITING_ACKS_QUEUE)
    else:
        return _generateSeqNum(UPS_WAITING_ACKS_QUEUE_LOCK, UPS_WAITING_ACKS_QUEUE)


def _sendProtoStrWithLock(toSocket, command, writeLock):
    with writeLock:
        # print(command)
        _sendProtoStr(toSocket, command)


def _sendProtoStrUntilAckReceived(toSocket, ack, command, writeLock, queueLock, queue):
    while(1):
        time.sleep(resendTimeWait)
        with queueLock:
            if ack in queue:
                # resend
                _sendProtoStrWithLock(toSocket, command, writeLock)
            else:
                # Ack received, exit
                break


'''
    This function is going to block until acks have been received
    Thread-safe, need to specify (lock, queue) pair
'''


def sendProtoStrUntilAckReceived(toSocket, seqNum, command, toWorld=True):
    # WORLD ASK waiting <queue, lock> pair
    global WORLD_WAITING_ACKS_QUEUE_LOCK, WORLD_WAITING_ACKS_QUEUE
    # UPS ASK waiting <queue, lock> pair
    global UPS_WAITING_ACKS_QUEUE_LOCK, UPS_WAITING_ACKS_QUEUE
    # Writing lock for sending msg to socket
    global WRITE_TO_UPS_LOCK, WRITE_TO_WORLD_LOCK
    if toWorld:
        _sendProtoStrUntilAckReceived(toSocket, seqNum, command, WRITE_TO_WORLD_LOCK,
                                      WORLD_WAITING_ACKS_QUEUE_LOCK, WORLD_WAITING_ACKS_QUEUE)
    else:
        _sendProtoStrUntilAckReceived(
            toSocket, seqNum, command, WRITE_TO_UPS_LOCK, UPS_WAITING_ACKS_QUEUE_LOCK, UPS_WAITING_ACKS_QUEUE)


'''
    Thread-safe, send command with wirteLock
'''


def sendProtoStrWithLock(toSocket, command, toWorld=True):
    global WRITE_TO_WORLD_LOCK, WRITE_TO_UPS_LOCK
    writeLock = WRITE_TO_WORLD_LOCK if toWorld else WRITE_TO_UPS_LOCK
    _sendProtoStrWithLock(toSocket, command, writeLock)


def sendAckWithLock(toSocket, seqNum, protoType, toWorld=True):
    command = protoType()
    command.acks.append(seqNum)
    sendProtoStrWithLock(toSocket, command, toWorld)


def updateOrderStatus(dbConn, orderId, status):
    sql = (f"update amazon_order\n"
           f"set status = \'{status}\' \n"
           f"where id = {orderId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    dbConn.commit()


def updateOrderTimeStamp(dbConn, orderId, timeField):
    sql = (f"update amazon_order\n"
           f"set {timeField} = now()\n"
           f"where id = {orderId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    dbConn.commit()


def getOrderIdWithShipId(dbConn, shipId):
    sql = (f"select id from amazon_order\n"
           f"where shipid_or_packageid = {shipId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    return row[0]


def _checkSeqNumHasBeenReceived(seqNum, lock, queue):
    # if seq number has been received before, exit
    with lock:
        if seqNum in queue:
            return True
        else:
            queue.add(seqNum)
    return False


def checkSeqNumHasBeenReceived(seqNum, fromWorld=True):
    global WORLD_SEQNUM_RECEIVED_QUEUE, WORLD_SEQNUM_RECEIVED_QUEUE_LOCK, UPS_SEQNUM_RECEIVED_QUEUE, UPS_SEQNUM_RECEIVED_QUEUE_LOCK
    if fromWorld:
        return _checkSeqNumHasBeenReceived(seqNum, WORLD_SEQNUM_RECEIVED_QUEUE_LOCK, WORLD_SEQNUM_RECEIVED_QUEUE)
    else:
        return _checkSeqNumHasBeenReceived(seqNum, UPS_SEQNUM_RECEIVED_QUEUE_LOCK, UPS_SEQNUM_RECEIVED_QUEUE)


def getOrderStatus(orderId, dbConn):
    sql = (f"select status from amazon_order\n"
           f"where id = {orderId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    return row[0]


def checkIsOrderCancelledByShipId(shipId, dbConn):
    orderId = getOrderIdWithShipId(dbConn, shipId)
    return getOrderStatus(orderId, dbConn) == order_status.cancelled


def getWarehouseInfoWithId(warehouseId, dbConn):
    sql = (f"select * from amazon_warehouse\n"
           f"where id = {warehouseId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    # return id, x, y
    return row[0], row[1], row[2]


def sendConnectToWorld(worldSocket, worldid, dbConn):
    # find all warehouses from database
    sql = (f"select id from amazon_warehouse;")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    command = world.AConnect()
    command.isAmazon = True
    command.worldid = worldid
    for row in rows:
        initWarehouse = command.initwh.add()
        initWarehouse.id, initWarehouse.x, initWarehouse.y = getWarehouseInfoWithId(
            row[0], dbConn)
    # connect to world
    sendProtoStrWithLock(worldSocket, command)


def addProductsToCommand(orderId, command, dbConn):
    sql = (f"select amazon_product.id, amazon_product.description, amazon_orderproduct.count from amazon_orderproduct, amazon_product\n"
           f"where amazon_orderproduct.product_id=amazon_product.id and amazon_orderproduct.order_id = {orderId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        thing = command.things.add()
        thing.id = row[0]
        thing.description = row[1]
        thing.count = row[2]


def startPacking(worldSocket, orderId, dbConn):
    global WRITE_TO_WORLD_LOCK
    print("Packing for orderid {}".format(orderId))
    command = world.ACommands()
    sql = (f"select warehouse_id, shipid_or_packageid from amazon_order\n"
           f"where id = {orderId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()

    APack = command.topack.add()
    APack.whnum = row[0]
    APack.shipid = row[1]
    APack.seqnum = generateSeqNum()

    addProductsToCommand(orderId, APack, dbConn)

    updateOrderStatus(dbConn, orderId, order_status.packing)
    sendProtoStrUntilAckReceived(worldSocket, APack.seqnum, command)
    print(command)


def startLoading(worldSocket, orderId, dbConn):
    global WRITE_TO_WORLD_LOCK
    # send loading to world
    command = world.ACommands()
    sql = (f"select warehouse_id, truck_id, shipid_or_packageid from amazon_order\n"
           f"where id = {orderId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()

    APutOnTruck = command.load.add()
    APutOnTruck.whnum, APutOnTruck.truckid, APutOnTruck.shipid = row
    APutOnTruck.seqnum = generateSeqNum()

    updateOrderStatus(dbConn, orderId, order_status.loading)
    print(command)
    sendProtoStrUntilAckReceived(worldSocket, APutOnTruck.seqnum, command)


def requestTruckFromUPS(upsSocket, orderId, dbConn):
    command = ups.AMsg()
    ATruckReq = command.truckreq.add()
    sql = (f"select warehouse_id, shipid_or_packageid, ups_name from amazon_order\n"
           f"where id = {orderId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    warehouseId = row[0]
    ATruckReq.packageid = row[1]
    if row[2]:
        ATruckReq.upsaccount = row[2]
    ATruckReq.wh.id, ATruckReq.wh.x, ATruckReq.wh.y = getWarehouseInfoWithId(
        warehouseId, dbConn)
    ATruckReq.seqnum = generateSeqNum(toWorld=False)
    addProductsToCommand(orderId, ATruckReq, dbConn)
    sendProtoStrUntilAckReceived(
        upsSocket, ATruckReq.seqnum, command, toWorld=False)


def requestDeliverFromUPS(upsSocket, orderId, dbConn):
    command = ups.AMsg()
    ADeliverReq = command.deliverreq.add()

    sql = (f"select shipid_or_packageid, truck_id, dest_x, dest_y from amazon_order\n"
           f"where id = {orderId};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()

    ADeliverReq.packageid = row[0]
    ADeliverReq.truckid = row[1]
    ADeliverReq.dest_x = row[2]
    ADeliverReq.dest_y = row[3]
    ADeliverReq.seqnum = generateSeqNum(toWorld=False)
    updateOrderStatus(dbConn, orderId, order_status.delivering)
    sendProtoStrUntilAckReceived(
        upsSocket, ADeliverReq.seqnum, command, toWorld=False)


def handlePurchasedMore(worldSocket, upsSocket, purchasedMore, dbConn):
    global ORDER_PURCHASED_SET, ORDER_PURCHASED_SET_LOCK
    sendAckWithLock(worldSocket, purchasedMore.seqnum, world.ACommands)
    if checkSeqNumHasBeenReceived(purchasedMore.seqnum):
        return
    orderPurchaseSet = set()

    with ORDER_PURCHASED_SET_LOCK:
        orderPurchaseSet = ORDER_PURCHASED_SET
        ORDER_PURCHASED_SET = set()

    for orderId in orderPurchaseSet:
        print("Now purchase for orderId = {}".format(orderId))
        startPacking(worldSocket, orderId, dbConn)
        requestTruckFromUPS(upsSocket, orderId, dbConn)


def handlePacked(worldSocket, upsSocket, packed, dbConn):
    sendAckWithLock(worldSocket, packed.seqnum, world.ACommands)
    if checkSeqNumHasBeenReceived(packed.seqnum):
        return
    sql = (f"select id, truck_id from amazon_order\n"
           f"where shipid_or_packageid = {packed.shipid};")

    cursor = dbConn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    orderId = row[0]
    truckId = row[1]
    updateOrderStatus(dbConn, orderId, order_status.packed)
    updateOrderTimeStamp(dbConn, orderId, order_status.packed_at)
    if truckId is not None:
        startLoading(worldSocket, orderId, dbConn)


def handleLoaded(worldSocket, upsSocket, loaded, dbConn):
    sendAckWithLock(worldSocket, loaded.seqnum, world.ACommands)
    if checkSeqNumHasBeenReceived(loaded.seqnum):
        return
    orderId = getOrderIdWithShipId(dbConn, loaded.shipid)
    updateOrderStatus(dbConn, orderId, order_status.loaded)
    updateOrderTimeStamp(dbConn, orderId, order_status.loaded_at)
    requestDeliverFromUPS(upsSocket, orderId, dbConn)


# **Handle World Request**
def handleWorldResponse(worldSocket, upsSocket, dbConn):
    executor = ThreadPoolExecutor(100)
    connected = readProtoRsp(worldSocket, world.AConnected)
    print(connected.result)
    simspeed = world.ACommands()
    simspeed.simspeed = 250
    print(simspeed)
    sendProtoStrWithLock(worldSocket, simspeed)

    while(1):
        global WORLD_WAITING_ACKS_QUEUE, WORLD_WAITING_ACKS_QUEUE_LOCK
        global ORDER_PURCHASED_SET, ORDER_PURCHASED_SET_LOCK
        response = readProtoRsp(worldSocket, world.AResponses)

        print(response)

        for error in response.error:
            print("Error from world: {}".format(error.originseqnum))
            print("ERROR message: {}".format(error.err))
            sendAckWithLock(worldSocket, error.seqnum,
                            world.ACommands, WRITE_TO_WORLD_LOCK)

        for ack in response.acks:
            with WORLD_WAITING_ACKS_QUEUE_LOCK:
                WORLD_WAITING_ACKS_QUEUE.discard(ack)

            with ORDER_PURCHASED_SET_LOCK:
                if seqNumberToOrderIdDict.get(ack):
                    ORDER_PURCHASED_SET.add(seqNumberToOrderIdDict[ack])

        for purchasedMore in response.arrived:
            executor.submit(handlePurchasedMore, worldSocket,
                            upsSocket, purchasedMore, dbConn)

        for packed in response.ready:
            if not checkIsOrderCancelledByShipId(packed.shipid, dbConn):
                executor.submit(handlePacked, worldSocket,
                                upsSocket, packed, dbConn)
            else:
                executor.submit(sendAckWithLock, worldSocket,
                                packed.seqnum, world.ACommands)

        for loaded in response.loaded:
            if not checkIsOrderCancelledByShipId(loaded.shipid, dbConn):
                executor.submit(handleLoaded, worldSocket,
                                upsSocket, loaded, dbConn)
            else:
                executor.submit(sendAckWithLock, worldSocket,
                                loaded.seqnum, world.ACommands)

        if response.HasField("finished"):
            print("WORLD connection ended")
            break


def handleTruckSent(upsSocket, trucksent, dbConn):
    sendAckWithLock(upsSocket, trucksent.seqnum, ups.AMsg, toWorld=False)
    if checkSeqNumHasBeenReceived(trucksent.seqnum, fromWorld=False):
        return
    # update truck_id
    sql = (f"update amazon_order\n"
           f"set truck_id = {trucksent.truckid}\n"
           f"where shipid_or_packageid = {trucksent.packageid};")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    dbConn.commit()


def handleTruckArrived(worldSocket, upsSocket, truckarrived, dbConn):
    sendAckWithLock(upsSocket, truckarrived.seqnum, ups.AMsg, toWorld=False)
    if checkSeqNumHasBeenReceived(truckarrived.seqnum, fromWorld=False):
        return
    orderId = getOrderIdWithShipId(dbConn, truckarrived.packageid)

    status = getOrderStatus(orderId, dbConn)

    if status == order_status.packed:
        startLoading(worldSocket, orderId, dbConn)


def handleDelivered(upsSocket, delivered, dbConn):
    sendAckWithLock(upsSocket, delivered.seqnum, ups.AMsg, toWorld=False)
    if checkSeqNumHasBeenReceived(delivered.seqnum, fromWorld=False):
        return
    orderId = getOrderIdWithShipId(dbConn, delivered.packageid)
    updateOrderStatus(dbConn, orderId, order_status.delivered)
    updateOrderTimeStamp(dbConn, orderId, order_status.delivered_at)


def handleConnectToWorld(worldSocket, upsSocket, worldid, dbConn):
    sendAckWithLock(upsSocket, worldid.seqnum, ups.AMsg, toWorld=False)
    if checkSeqNumHasBeenReceived(worldid.seqnum, fromWorld=False):
        return
    sendConnectToWorld(worldSocket, worldid.worldid, dbConn)



# **Handle UPS Request**
def handleUPSResponse(worldSocket, upsSocket, dbConn):
    executor = ThreadPoolExecutor(100)

    while(1):
        global UPS_WAITING_ACKS_QUEUE, UPS_WAITING_ACKS_QUEUE_LOCK
        response = readProtoRsp(upsSocket, ups.UMsg, fromWorld=False)
        print(response)
        for error in response.error:
            print("Error from ups: {}".format(error.originseqnum))
            print("ERROR message: {}".format(error.err))
            sendAckWithLock(upsSocket, error.seqnum, ups.AMsg, toWorld=False)

        for ack in response.acks:
            with UPS_WAITING_ACKS_QUEUE_LOCK:
                UPS_WAITING_ACKS_QUEUE.discard(ack)

        for trucksent in response.trucksent:
            executor.submit(handleTruckSent, upsSocket, trucksent, dbConn)

        for truckarrived in response.truckarrived:
            if not checkIsOrderCancelledByShipId(truckarrived.packageid, dbConn):
                executor.submit(handleTruckArrived, worldSocket,
                                upsSocket, truckarrived, dbConn)
            else:
                executor.submit(sendAckWithLock, upsSocket,
                                truckarrived.seqnum, ups.AMsg, toWorld=False)

        for delivered in response.delivered:
            executor.submit(handleDelivered, upsSocket, delivered, dbConn)

        for worldid in response.worldid:
            executor.submit(handleConnectToWorld, worldSocket,
                            upsSocket, worldid, dbConn)


def handlePurchaseMore(orderId, worldSocket, dbConn):
    command = world.ACommands()
    APurchaseMore = command.buy.add()
    sql = (f"select * from amazon_warehouse;")
    cursor = dbConn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    # Randomly assign warehouse id
    randomlyAssignedWarehouseId = rows[orderId % len(rows)][0]

    sql = (f"update amazon_order\n"
           f"set warehouse_id = {randomlyAssignedWarehouseId}\n"
           f"where id = {orderId};")

    # Update warehouse number
    cursor.execute(sql)
    dbConn.commit()

    APurchaseMore.whnum = randomlyAssignedWarehouseId
    APurchaseMore.seqnum = generateSeqNum()
    seqNumberToOrderIdDict[APurchaseMore.seqnum] = orderId
    addProductsToCommand(orderId, APurchaseMore, dbConn)
    updateOrderStatus(dbConn, orderId, order_status.purchasing)
    print("send command : {}".format(command))
    sendProtoStrUntilAckReceived(worldSocket, APurchaseMore.seqnum, command)



# **Handle WebApp Request**
def handleWebAppRequest(worldSocket, webAppSocket, dbConn):
    executor = ThreadPoolExecutor(100)
    while(1):
        try:
            response = readProtoRsp(
                webAppSocket, webapp.AWCommands, fromWorld=False)
            print(response)
            if response.HasField("buy"):
                executor.submit(handlePurchaseMore,
                                response.buy.orderid, worldSocket, dbConn)

        except Exception as e:
            print("Exception raised: {}".format(str(e)))
            traceback.print_exc()
            break
