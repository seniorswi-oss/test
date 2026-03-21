from database.postgresql import PostgresDB

db = None

def connect_db():
    global db
    db = PostgresDB()


def insert_order(status):
    global db
    db.insert(
        "INSERT INTO orders (status) VALUES (%s)",
        (status)
    )

def insert_order_item(order_id, item_id, qty, total):
    global db
    db.insert(
        "INSERT INTO orders_items (order_id, item_id, qty, total) VALUES (%s, %s, %s, %s)",
        (order_id, item_id, qty, total)
    )

def fetch_items(order_id=None):
    global db
    if order_id is not None:
        return db.fetch_all(
            "SELECT i.* FROM items i JOIN orders_items oi ON i.item_id = oi.item_id WHERE oi.order_id = %s",
            (order_id,)
        )
    return db.fetch_all("SELECT * FROM items")

def fetch_orders(order_id=None):
    global db
    if order_id is not None:
        return db.fetch_all(
            "SELECT * FROM orders WHERE id = %s",
            (order_id,)
        )
    return db.fetch_all("SELECT * FROM orders")

def update_order_status(order_id, status):
    global db
    db.update(
        "UPDATE orders SET status = %s WHERE id = %s",
        (status, order_id)
    )

def init_db():
    global db
    db.execute("""
        
    DROP TABLE IF EXISTS orders_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS items;
               
    """)