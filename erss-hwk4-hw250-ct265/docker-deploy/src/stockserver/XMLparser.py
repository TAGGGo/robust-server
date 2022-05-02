import xml.etree.ElementTree as ET
import psycopg2
from dbconn import *
import time

class XMLparser:

    def __init__(self, conn, trans_id):
        self.conn = conn
        self.trans_id = trans_id

    def parse(self, msg):
        try:
            if msg[-4:] == '.xml':
                tree = ET.parse(msg)
                root = tree.getroot()
            else:
                # print(msg)
                root = ET.fromstring(msg)
        except Exception as err:
            print("Cannot parse XML: ", repr(err))
            return

        return_xml = ET.Element("results")

        try:
            if root.tag == 'create':
                self.handle_create(root, return_xml)
            elif root.tag == 'transactions':
                self.handle_transaction(root, return_xml)
            else:
                raise Exception(f"Root tag \"{root.tag}\" unsupported")
        except Exception as err:
            print(repr(err))
            return
        
        # print(ET.tostring(return_xml))
        return ET.tostring(return_xml).decode("UTF-8")


    def handle_create(self, root, return_xml):
        for child in root:
            try:
                if child.tag == 'account':
                    try:
                        account_id = int(child.attrib['id'])
                        balance = float(child.attrib['balance'])
                        if has_account(self.conn, account_id):
                            raise Exception("Account already exists")

                        if balance < 0:
                            raise Exception("Balance cannot be negative")

                        add_account(self.conn, account_id, balance)
                        ET.SubElement(return_xml, 'created', {'id':str(account_id)})
                    except Exception as err:
                        error_msg = ET.SubElement(return_xml, 'error', {'id':str(account_id)})
                        error_msg.text = str(err)

                elif child.tag == 'symbol':
                    sym = child.attrib['sym']

                    for sym_child in child.findall('account'):
                        try:
                            sym_child_id = int(sym_child.attrib['id'])
                            num_shares = float(sym_child.text)

                            if not has_account(self.conn, sym_child_id):
                                raise Exception("Account does not exist")
                            
                            if num_shares < 0:
                                raise Exception("Number of shares cannot be negative")
                            sym_id = get_symbol_id(self.conn, sym)
                            add_position(self.conn, sym_child_id, sym_id, num_shares)
                            ET.SubElement(return_xml, 'created', {'sym':sym, 'id':str(sym_child_id)})
                        except Exception as err:
                            error_msg = ET.SubElement(return_xml, 'error', {'sym':sym, 'id':str(sym_child_id)})
                            error_msg.text = str(err)

                else:
                    raise Exception("Child tag \"{child.tag}\" unsupported")

            except Exception as err:
                error_msg = ET.SubElement(return_xml, 'error')
                error_msg.text = str(err)
        

    def handle_transaction(self, root, return_xml):
        if 'id' not in root.attrib:
            raise Exception("Transaction does not have attribute 'id'")
        
        if len(root) == 0:
            raise Exception("No transactions found")
        
        account_id = root.attrib['id']
        is_valid = has_account(self.conn, account_id)

        for child in root:
            if child.tag == 'order':
                try:
                    if not is_valid:
                        raise Exception("Invalid account id")
                    
                    sym = child.attrib['sym']
                    amount = float(child.attrib['amount'])
                    limit = float(child.attrib['limit'])

                    # check if valid, can reject and raise error
                    if amount == 0:
                        raise Exception("Symbol amount cannot be zero")
                    elif amount > 0 and not has_enough_balance(self.conn, account_id, limit*amount):
                        raise Exception("Buyer does not have enough balance")
                    elif amount < 0 and not has_enough_shares(self.conn, account_id, sym, amount):
                        raise Exception("Seller does not have enough shares")
                    
                    # match orders
                    self.match_orders(account_id, sym, amount, limit)

                    ET.SubElement(return_xml, 'opened', {'sym':sym,'amount':str(amount),'limit':str(limit),'id':str(self.trans_id)})

                    # increase trans_id
                    self.trans_id += 1
                except Exception as err:
                    error_msg = ET.SubElement(return_xml, 'error', {'sym':sym,'amount':str(amount),'limit':str(limit)})
                    error_msg.text = str(err)

            elif child.tag == 'query':
                try:
                    if not is_valid:
                        raise Exception("Invalid account id")

                    trans_id = int(child.attrib['id'])

                    if not check_transid_with_accountid(self.conn, trans_id, account_id):
                        raise Exception("Account does not have trans id")

                    status_xml = ET.SubElement(return_xml, 'status', {'id':str(trans_id)})

                    self.build_order_xml(trans_id, status_xml)
                except Exception as err:
                    ele = return_xml.find('status')
                    if ele is not None:
                        return_xml.remove(ele)
                    error_msg = ET.SubElement(return_xml, 'error', {'id':str(trans_id)})
                    error_msg.text = str(err)

            elif child.tag == 'cancel':
                try:
                    if not is_valid:
                        raise Exception("Invalid account id")

                    trans_id = int(child.attrib['id'])

                    if not check_transid_with_accountid(self.conn, trans_id, account_id):
                        raise Exception("Account does not have trans id")

                    status_xml = ET.SubElement(return_xml, 'canceled', {'id':str(trans_id)})

                    self.cancel_order(trans_id)
                    self.build_order_xml(trans_id, status_xml)
                except Exception as err:
                    ele = return_xml.find('canceled')
                    if ele is not None:
                        return_xml.remove(ele)
                    error_msg = ET.SubElement(return_xml, 'error', {'id':str(trans_id)})
                    error_msg.text = str(err)

            else:
                raise Exception("Child tag \"{child.tag}\" unsupported")


    def match_orders(self, id, sym, amount, limit):
        if amount > 0:
            self.match_buy(id, sym, amount, limit)
        elif amount < 0:
            self.match_sell(id, sym, amount, limit)
        

    def match_buy(self, id, sym, amount, limit):
        cur = self.conn.cursor()
        cur.execute("select * from consumer_order where amount < 0 and symbol_id = {} and status = 'open' and account_id != {} order by limit_price ASC, ts ASC ".format(get_symbol_id(self.conn, sym), id))
        sell_rows = cur.fetchall()
        remain = amount

        # deduct buyer balance
        increase_account_balance(self.conn, id, limit*amount, False)

        if len(sell_rows):
            # search for proper sell orders
            for row in sell_rows:
                sell_order_id = int(row[0])
                sell_account_id = int(row[1])
                sell_trans_id = int(row[2])
                sell_symbol_id = int(row[3])
                sell_amount = -float(row[4])
                sell_limit_price = float(row[5])

                if limit >= sell_limit_price and remain > 0: # matched
                    if remain >= sell_amount:
                        remain -= sell_amount
                        # change sell order
                        change_order_status(self.conn, sell_order_id, "executed")
                        
                        # add buy order
                        add_order(self.conn, id, self.trans_id, sym, sell_amount, sell_limit_price, "executed")

                        # refund seller balance
                        increase_account_balance(self.conn, sell_account_id, sell_limit_price*sell_amount)

                        # refund buyer balance
                        if sell_limit_price < limit:
                            increase_account_balance(self.conn, id, (limit-sell_limit_price)*sell_amount)

                        # increase buyer shares
                        increase_position_amount(self.conn, id, sell_symbol_id, sell_amount)
                        
                    else:
                        # change sell order (part open, part executed)
                        increase_order_amount(self.conn, sell_order_id, remain, add=False)
                        add_order(self.conn, sell_account_id, sell_trans_id, sym, -remain, sell_limit_price, "executed")

                        # add buy order
                        add_order(self.conn, id, self.trans_id, sym, remain, sell_limit_price, "executed")

                        # refund seller balance
                        increase_account_balance(self.conn, sell_account_id, sell_limit_price*remain)

                        #refund buyer balance
                        if sell_limit_price < limit:
                            increase_account_balance(self.conn, id, (limit-sell_limit_price)*remain)

                        # increase buyer shares
                        increase_position_amount(self.conn, id, sell_symbol_id, remain)

                        remain = 0

                else:
                    break

        if remain > 0:
            # add buy order
            add_order(self.conn, id, self.trans_id, sym, remain, limit, "open")


    def match_sell(self, id, sym, amount, limit):
        cur = self.conn.cursor()
        symbol_id = get_symbol_id(self.conn, sym)
        cur.execute("select * from consumer_order where amount > 0 and symbol_id = {} and status = 'open' and account_id != {} order by limit_price DESC, ts ASC ".format(symbol_id, id))
        buy_rows = cur.fetchall()
        remain = -amount

        #deduct seller shares
        increase_position_amount(self.conn, id, symbol_id, remain, False)

        if len(buy_rows):
            # search for proper buy orders
            for row in buy_rows:
                buy_order_id = int(row[0])
                buy_account_id = int(row[1])
                buy_trans_id = int(row[2])
                buy_symbol_id = int(row[3])
                buy_amount = float(row[4])
                buy_limit_price = float(row[5])

                if limit <= buy_limit_price and remain > 0: # matched
                    if remain >= buy_amount:
                        remain -= buy_amount
                        # change buy order
                        change_order_status(self.conn, buy_order_id, "executed")
                        
                        # add sell order
                        add_order(self.conn, id, self.trans_id, sym, -buy_amount, buy_limit_price, "executed")

                        # refund seller balance
                        increase_account_balance(self.conn, id, buy_limit_price*buy_amount)

                        # increase buyer shares
                        increase_position_amount(self.conn, buy_account_id, buy_symbol_id, buy_amount)
                        
                    else:
                        # change buy order (part open, part executed)
                        increase_order_amount(self.conn, buy_order_id, remain, False)
                        add_order(self.conn, buy_account_id, buy_trans_id, sym, remain, buy_limit_price, "executed")

                        # add sell order
                        add_order(self.conn, id, self.trans_id, sym, -remain, buy_limit_price, "executed")

                        # refund seller balance
                        increase_account_balance(self.conn, id, buy_limit_price*remain)

                        # increase buyer shares
                        increase_position_amount(self.conn, buy_account_id, buy_symbol_id, remain)

                        remain = 0

                else:
                    break

        if remain > 0:
            # add sell order
            add_order(self.conn, id, self.trans_id, sym, -remain, limit, "open")



    def build_order_xml(self, trans_id, status_xml):
        rows = get_order_by_trans_id(self.conn, trans_id)

        for row in rows:
            amount = float(row[4])
            price = float(row[5])
            order_status = str(row[6])
            ts = self.toUnixTime(row[7])

            if order_status == 'open':
                ET.SubElement(status_xml, 'open', {'shares':str(amount)})
            elif order_status == 'executed':
                ET.SubElement(status_xml, 'executed', {'shares':str(amount),'price':str(price),'time':str(ts)})
            elif order_status == 'canceled':
                ET.SubElement(status_xml, 'canceled', {'shares':str(amount),'time':str(ts)})
            else:
                raise Exception("Order status unsupported")

        
    def cancel_order(self, trans_id):
        rows = get_order_by_trans_id_and_status(self.conn, trans_id, "open")
        for row in rows:
            order_id = int(row[0])
            account_id = int(row[1])
            symbol_id = int(row[3])
            amount = float(row[4])
            price = float(row[5])

            if amount > 0:
                # refund account balance
                increase_account_balance(self.conn, account_id, amount*price)
            else:
                # increase account shares
                increase_position_amount(self.conn, account_id, symbol_id, -amount)

            # change open orders to canceled
            change_order_status(self.conn, order_id, "canceled")
    

    def toUnixTime(self, dt):
        ts = time.mktime(dt.timetuple())
        return int(ts)



if __name__ == '__main__':
    file_path = 'xml_files/transactions.xml'
    conn = psycopg2.connect(database="stockexchange", user="postgres", password="123456", host="127.0.0.1", port="5432")

    parser = XMLparser(conn, 1000)
    parser.parse(file_path)