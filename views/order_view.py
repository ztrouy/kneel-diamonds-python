import sqlite3
import json

def get_orders():
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                o.id,
                o.metal_id,
                o.size_id,
                o.style_id
            FROM Orders o
        """)
        query_results = db_cursor.fetchall()

        orders = []
        for row in query_results:
            orders.append(dict(row))
        
        serialized_orders = json.dumps(orders)
    
    return serialized_orders

def get_single_order(url):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        order_id = url["pk"]
            
        db_cursor.execute("""
            SELECT
                o.id,
                o.metal_id,
                o.size_id,
                o.style_id
            FROM Orders o
            WHERE o.id = ?
        """, (order_id,))
        query_result = db_cursor.fetchone()

        serialized_order = json.dumps(dict(query_result))

    return serialized_order

def create_order(order_data):
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO `Orders` (metal_id, size_id, style_id)
            VALUES (?, ?, ?);
        """, (order_data["metal_id"], order_data["size_id"], order_data["style_id"]))
        number_of_rows_created = db_cursor.rowcount

        return True if number_of_rows_created > 0 else False