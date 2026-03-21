from database import database as db

def place_order(status, session_id, items=[], qtys=[]):
    order_id = db.insert_order(session_id, status)
    if len(items) == 0:
        return order_id
    add_item_to_order(order_id, items, qtys)
    return order_id

def add_item_to_order(order_id, items, qtys):
    items_list = db.fetch_items()
    for i, item in enumerate(items):
        price = items_list[item['name']]['price']
        db.insert_order_item(order_id, item['name'], qtys[i], price * qtys[i])

def order_complete(order_id, status='completed'):
    db.update_order_status(order_id, status)

def get_order_by_id(order_id):
    orders = db.fetch_orders(order_id=order_id)
    if not orders:
        return None
    order = orders[0]
    return order_details(order)

def get_order_by_session(session_id):
    orders = db.fetch_orders(session_id=session_id)
    if not orders:
        return None
    order = orders[0]
    return order_details(order)

def order_details(order):
    items = db.fetch_items(order['id'])
    return {
        "order_id": order['id'],
        "status": order['status'],
        "items": items
    }

def fetch_all_orders():
    return db.fetch_orders()

def fetch_all_items():
    return db.fetch_items()