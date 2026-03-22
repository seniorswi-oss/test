from database import database as db

def place_order(status, session_id, items=[], qtys=[]):
    order_id = db.insert_order(session_id, status)
    if len(items) == 0:
        return order_id
    add_item_to_order(order_id, items, qtys)
    return order_id

def add_item_to_order(order_id, items, qtys):
    items_map = {i['name'].lower(): i for i in db.fetch_items()}

    for name, qty in zip(items, qtys):
        item = items_map.get(name.lower())
        if not item:
            continue

        cart = db.fetch_cart_item(order_id, item['item_id'])
        new_qty = cart['qty'] + qty if cart else qty
        total = float(item['price']) * float(new_qty)

        (db.update_order_item if cart else db.insert_order_item)(
            order_id, item['item_id'], new_qty if cart else qty, total
        )

def remove_item_from_order(order_id, items, qtys):
    items_map = {i['name'].lower(): i for i in db.fetch_items()}

    for name, qty in zip(items, qtys):
        item = items_map.get(name.lower())
        if not item:
            continue

        (db.update_order_item if qty > 0 else db.remove_order_item)(
            order_id,
            item['item_id'],
            qty,
            float(item['price']) * float(qty)
        ) if qty > 0 else db.remove_order_item(order_id, item['item_id'])

def order_complete(order_id, status='completed'):
    db.update_order_status(order_id, status)

def get_order_by_id(order_id):
    orders = db.fetch_orders(order_id=order_id)
    if not orders:
        return "Order not found"
    order = orders[0]
    return order_details(order)

def get_order_by_session(session_id):
    orders = db.fetch_orders(session_id=session_id)
    if not orders:
        place_order('pending', session_id)
        orders = db.fetch_orders(session_id=session_id)

    order = orders[0]
    return order_details(order)

def order_details(order):
    items = db.fetch_items(order['id'])
    return {
        "order_id": order['id'],
        'session_id': order['session_id'],
        "status": order['status'],
        "items": items
    }

def fetch_all_orders():
    return db.fetch_orders()

def fetch_all_items():
    return db.fetch_items()