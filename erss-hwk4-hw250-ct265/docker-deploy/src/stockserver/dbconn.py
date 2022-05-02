import psycopg2

def has_account(conn, id):
    cur = conn.cursor()
    cur.execute("select * from account where account_id = {};".format(id))
    rows = cur.fetchall()
    return len(rows) > 0


def has_symbol(conn, name):
    cur = conn.cursor()
    cur.execute("select * from symbol where name = \'{}\';".format(name))
    rows = cur.fetchall()
    return len(rows) > 0

# insert if not in database, then return symbol id
def get_symbol_id(conn, name):
    cur = conn.cursor()
    # print("insert into symbol (name) values (\'{}\') ON conflict (name) DO NOTHING; commit; select symbol_id from symbol where name='{}';".format(name, name))
    cur.execute("insert into symbol (name) values (\'{}\') ON conflict (name) DO NOTHING; commit; select symbol_id from symbol where name='{}';".format(name, name))
    rows = cur.fetchall()
    # print(rows)
    return int(rows[0][0])


def add_account(conn, account_id, balance):
    if not has_account(conn, account_id):
        cur = conn.cursor()
        # print(f"insert into account (account_id, balance, ts) VALUES (%s, %s, now());"% (str(account_id), str(balance)))
        cur.execute(f"insert into account (account_id, balance, ts) VALUES (%s, %s, now());"% (str(account_id), str(balance)))
        conn.commit()


def get_account_balance(conn, account_id):
    if has_account(conn, account_id):
        cur = conn.cursor()
        cur.execute("select balance from account where account_id = {}".format(account_id))
        rows = cur.fetchall()
        return float(rows[0][0])
    raise Exception("Account not found")


def increase_account_balance(conn, account_id, amount, add=True):
    if has_account(conn, account_id):
        cur = conn.cursor()
        op = '+' if add else '-'
        # print("update account set balance = balance {} {} where account_id = {};".format(op, amount, account_id))
        cur.execute("update account set balance = balance {} {} where account_id = {};".format(op, amount, account_id))
        conn.commit()

# TODO: no position, create position
def increase_position_amount(conn, account_id, symbol_id, amount, add=True):
    # if has_position(conn, account_id, symbol_id):
    cur = conn.cursor()
    op = '+' if add else '-'
    # print("insert into position (account_id, symbol_id, amount) values ({}, {}, {}) ON conflict (account_id, symbol_id) DO update set amount = position.amount {} {};".format(account_id, symbol_id, amount, op, amount))
    cur.execute("insert into position (account_id, symbol_id, amount) values ({}, {}, {}) ON conflict (account_id, symbol_id) DO update set amount = position.amount {} {};".format(account_id, symbol_id, amount, op, amount))
    conn.commit()


def has_position(conn, account_id, symbol_id):
    if has_account(conn, account_id):
        cur = conn.cursor()
        cur.execute("select * from position where account_id = {} and symbol_id = {};".format(account_id, symbol_id))
        rows = cur.fetchall()
        return len(rows) > 0
    else:
        raise Exception("no account detected")


def add_position(conn, account_id, symbol_id, num_shares):
    if has_account(conn, account_id):
        if not has_position(conn, account_id, symbol_id):
            cur = conn.cursor()
            # print(f"insert into position (amount, account_id, symbol_id, ts) VALUES (%s, %s, %s, now());"% (str(num_shares), str(account_id), str(symbol_id)))
            cur.execute(f"insert into position (amount, account_id, symbol_id, ts) VALUES (%s, %s, %s, now());"% (str(num_shares), str(account_id), str(symbol_id)))
            conn.commit()
    else:
        raise Exception("no account detected")


def has_enough_balance(conn, account_id, amount):
    if has_account(conn, account_id):
        cur = conn.cursor()
        # print("select * from account where account_id = {} and balance >= {};".format(account_id, amount))
        cur.execute("select * from account where account_id = {} and balance >= {};".format(account_id, amount))
        rows = cur.fetchall()
        return len(rows) > 0
    else:
        raise Exception("no account detected")


def has_enough_shares(conn, account_id:int, symbol_name:str, amount:float):
    symbol_id = get_symbol_id(conn, symbol_name)
    if has_account(conn, account_id):
        cur = conn.cursor()
        cur.execute("select * from position where account_id = {} and symbol_id = {} and amount >= {};".format(account_id, symbol_id,amount))
        rows = cur.fetchall()
        return len(rows) > 0
    else:
        raise Exception("no account detected")    

def change_order_status(conn, order_id, status):
    cur = conn.cursor()
    # print("update consumer_order set status = \'{}\', ts = now() where order_id = {};".format(status, order_id))
    cur.execute("update consumer_order set status = \'{}\', ts = now() where order_id = {};".format(status, order_id))
    conn.commit()

def add_order(conn, account_id, trans_id, symbol_name, amount, limit_price, status):
    cur = conn.cursor()
    symbol_id = get_symbol_id(conn, symbol_name)
    # print("insert into consumer_order (account_id, trans_id, symbol_id, amount, limit_price, status, ts) values ({}, {}, {}, {}, {}, \'{}\', now());".format(account_id, trans_id, symbol_id, amount, limit_price, status))
    cur.execute("insert into consumer_order (account_id, trans_id, symbol_id, amount, limit_price, status, ts) values ({}, {}, {}, {}, {}, \'{}\', now());".format(account_id, trans_id, symbol_id, amount, limit_price, status))
    conn.commit()

def get_order_by_trans_id(conn, trans_id):
    cur = conn.cursor()
    # print("select * from consumer_order where trans_id = {};".format(trans_id))
    cur.execute("select * from consumer_order where trans_id = {};".format(trans_id))
    return cur.fetchall()

def get_order_by_trans_id_and_status(conn, trans_id, status):
    cur = conn.cursor()
    # print("select * from consumer_order where trans_id = {} and status = \'{}\';".format(trans_id, status))
    cur.execute("select * from consumer_order where trans_id = {} and status = \'{}\';".format(trans_id, status))
    return cur.fetchall()

def increase_order_amount(conn, order_id, amount, add=True):
    cur = conn.cursor()
    op = '+' if add == True else '-'
    # print("update consumer_order set amount = amount {} {} where order_id = {};".format(op, amount, order_id))
    cur.execute("update consumer_order set amount = amount {} {} where order_id = {};".format(op, amount, order_id))
    conn.commit()

def check_transid_with_accountid(conn, trans_id, account_id):
    cur = conn.cursor()
    # "select * from consumer_order where trans_id = {} and account_id = {};".format(trans_id, account_id)
    cur.execute("select * from consumer_order where trans_id = {} and account_id = {};".format(trans_id, account_id))
    rows = cur.fetchall()
    return len(rows) > 0

if __name__ == "__main__":
    #try:
        conn = psycopg2.connect(database="stockexchange", user="postgres", password="123456", host="127.0.0.1", port="5432")
        print("Database Connected....")
        #increase_order_amount(conn, 1, 100)
        print(check_transid_with_accountid(conn, 7000, 3))