from database.postgresql import PostgresDB

db = None

def connect_db():
    global db
    db = PostgresDB()


def insert_order(session_id, status='pending'):
    global db
    result = db.execute(
        "SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'orders';",
            fetch=True
    )
    print("test")
    print(result)
    # db.insert(
    #     "INSERT INTO orders (status, session_id) VALUES (%s, %s)",
    #     (status, session_id)
    # )

def insert_order_item(order_id, item_id, qty, total):
    global db
    db.insert(
        "INSERT INTO orders_items (order_id, item_id, qty, total) VALUES (%s, %s, %s, %s)",
        (order_id, item_id, qty, total)
    )

def remove_order_item(order_id, item_id):
    global db
    db.delete(
        "DELETE FROM orders_items WHERE order_id = %s AND item_id = %s",
        (order_id, item_id)
    )

def fetch_items(order_id=None):
    global db
    if order_id is not None:
        return db.fetch_all(
            "SELECT i.* FROM items i JOIN orders_items oi ON i.item_id = oi.item_id WHERE oi.order_id = %s",
            (order_id,)
        )
    return db.fetch_all("SELECT * FROM items")

def fetch_orders(session_id=None, order_id=None):
    global db
    if session_id is not None:
        return db.fetch_all(
            "SELECT * FROM orders WHERE session_id = %s",
            (session_id,)
        )
    if order_id is not None:
        return db.fetch_all(
            "SELECT * FROM orders WHERE id = %s",
            (order_id,)
        )
    return db.fetch_all("SELECT * FROM orders")

def update_order_item(order_id, item_id, qty, total):
    global db
    db.update(
        "UPDATE orders_items SET qty = %s, total = %s WHERE order_id = %s AND item_id = %s",
        (qty, total, order_id, item_id)
    )

def update_order_status(order_id, status):
    global db
    db.update(
        "UPDATE orders SET status = %s WHERE id = %s",
        (status, order_id)
    )

def init_db():
    global db
    result = db.execute("""
        
  DROP TABLE IF EXISTS orders_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS items;
               
    """)
    print(result)