import sqlite3
import json

def get_metals(url):
    pass

def get_single_metals(url):
    pass

def create_metal(metal_data):
    pass

def update_metal(id, metal_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE Metals
                SET price = ?
            WHERE id = ?
        """, (metal_data["price"], id))
        rows_affected = db_cursor.rowcount

    return True if rows_affected > 0 else False

def delete_metal(pk):
    pass