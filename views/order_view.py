import sqlite3
import json

def get_orders():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                o.id,
                o.metal_id,
                o.size_id,
                o.style_id,
                m.metal,
                m.price AS metal_price,
                s.carat,
                s.price AS size_price,
                st.style,
                st.price AS style_price
            FROM Orders o
            JOIN Metals m ON m.id = o.metal_id
            JOIN Sizes s ON s.id = o.size_id
            JOIN Styles st ON st.id = o.style_id
        """)
        query_results = db_cursor.fetchall()

        orders = []
        for row in query_results:
            order = {
                "id": row["id"],
                "metal_id": row["metal_id"],
                "size_id": row["size_id"],
                "style_id": row["style_id"]
            }
            metal = {
                "id": row["metal_id"],
                "metal": row["metal"],
                "price": row["metal_price"]
            }
            size = {
                "id": row["size_id"],
                "carat": row["carat"],
                "price": row["size_price"]
            }
            style = {
                "id": row["style_id"],
                "style": row["style"],
                "price": row["style_price"]
            }

            order["metal"] = metal
            order["size"] = size
            order["style"] = style

            orders.append(order)

        serialized_orders = json.dumps(orders)

    return serialized_orders

def get_single_order(url):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        order_id = url["pk"]

        db_cursor.execute("""
            SELECT
                o.id,
                o.metal_id,
                o.size_id,
                o.style_id,
                m.metal,
                m.price AS metal_price,
                s.carat,
                s.price AS size_price,
                st.style,
                st.price AS style_price
            FROM Orders o
            JOIN Metals m ON m.id = o.metal_id
            JOIN Sizes s ON s.id = o.size_id
            JOIN Styles st ON st.id = o.style_id
            WHERE o.id = ?
        """, (order_id,))
        query_result = db_cursor.fetchone()

        order = {}
        if query_result:
            order = {
                "id": query_result["id"],
                "metal_id": query_result["metal_id"],
                "size_id": query_result["size_id"],
                "style_id": query_result["style_id"]
            }
            metal = {
                "id": query_result["metal_id"],
                "metal": query_result["metal"],
                "price": query_result["metal_price"]
            }
            size = {
                "id": query_result["size_id"],
                "carat": query_result["carat"],
                "price": query_result["size_price"]
            }
            style = {
                "id": query_result["style_id"],
                "style": query_result["style"],
                "price": query_result["style_price"]
            }

            order["metal"] = metal
            order["size"] = size
            order["style"] = style

        else:
            order = None

        serialized_order = json.dumps(order)

    return serialized_order

def create_order(order_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO `Orders` (metal_id, size_id, style_id)
            VALUES (?, ?, ?);
        """, (order_data["metal_id"], order_data["size_id"], order_data["style_id"]))
        number_of_rows_created = db_cursor.rowcount

    return True if number_of_rows_created > 0 else False

def delete_order(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM Orders WHERE id = ?
        """, (pk,))
        number_of_rows_deleted = db_cursor.rowcount

        return True if number_of_rows_deleted > 0 else False
