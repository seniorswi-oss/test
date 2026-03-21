from database.postgresql import PostgresDB

db = None

def connect_db():
    global db
    db = PostgresDB()


def insert_order(session_id, status='pending'):
    global db
    db.insert(
        "INSERT INTO orders (status, session_id) VALUES (%s, %s)",
        (status, session_id)
    )

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
            "SELECT * FROM orders_items oi WHERE oi.order_id = %s",
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
        
    CREATE TABLE IF NOT EXISTS items (
        item_id SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        price NUMERIC(10, 2) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        status TEXT NOT NULL,
        session_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS orders_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER REFERENCES orders(id),
        item_id INTEGER REFERENCES items(item_id),
        qty INTEGER NOT NULL,
        total NUMERIC(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    INSERT INTO items (name, price) VALUES
        ('Pav Bhaji', 6.00), 
        ('Dosa', 5.00), 
        ('Idli', 4.00), 
        ('Chole Bhature', 7.00),
        ('Vada Pav', 3.00),
        ('Pani Puri', 4.50),
        ('Pizza', 8.00),
        ('Burger', 6.50),
        ('Samosa', 2.00),
        ('Jalebi', 3.50),
        ('Chai', 2.00),
        ('Coffee', 3.00),
        ('Lassi', 4.00)
        ON CONFLICT (name) DO NOTHING;
               
    """)

    print(result)