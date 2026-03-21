from database import database as db

def place_order(status, items, qtys):
    order_id = db.insert_order(status)
    if len(items) == 0:
        return order_id
    add_item_to_order(order_id, items, qtys)
    return order_id

def add_item_to_order(order_id, items, qtys):
    items_list = db.fetch_items()
    for i, item in enumerate(items):
        price = items_list[item['name']]['price']
        db.insert_order_item(order_id, item['name'], qtys[i], price * qtys[i])

def order_complete(order_id):
    db.update_order_status(order_id, 'completed')
    return "Order completed successfully"

def get_order_details(order_id):
    order = db.fetch_orders(order_id)[0]
    items = db.fetch_items(order_id)
    return {
        "order_id": order_id,
        "status": order['status'],
        "items": items
    }