from flask import Flask, jsonify, request
import sqlite3
from urllib.parse import parse_qs
from datetime import datetime

app = Flask(__name__)

DEFAULT_ORDER_BY = 'ad_id'
DEFAULT_ORDER = 'asc'
ALLOWED_ORDER_BY = ['ad_id', 'price', 'created_at']
ALLOWED_ORDER = ['asc', 'desc']
DB = 'classifieds.db'


def initiate_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        """
            CREATE TABLE IF NOT EXISTS classifieds_ads(
            ad_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            subject TEXT NOT NULL, 
            body TEXT NOT NULL, 
            price NUMERIC, 
            email TEXT NOT NULL, 
            created_at DATE NOT NULL)
        """
    )

    conn.commit()
    return


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def gen_query(query_str):
    parsed_str = parse_qs(query_str, encoding='utf-8')

    order_by = parsed_str.get('sortby', [DEFAULT_ORDER_BY])[0]
    if order_by not in ALLOWED_ORDER_BY:
        order_by = DEFAULT_ORDER_BY

    order = parsed_str.get('sort', [DEFAULT_ORDER])[0]
    if order not in ALLOWED_ORDER:
        order = DEFAULT_ORDER

    return f'SELECT * FROM classifieds_ads ORDER BY {order_by} {order};'


@app.route('/api/v1/classifieds_ads', methods=['GET'])
def list_classifieds():
    conn = sqlite3.connect(DB)
    conn.row_factory = dict_factory
    c = conn.cursor()

    query = gen_query(request.query_string.decode())
    c.execute(query)
    return jsonify(c.fetchall())


@app.route('/api/v1/classifieds_ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    conn = sqlite3.connect(DB)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT * FROM classifieds_ads WHERE ad_id == ?;', (ad_id,))

    result = c.fetchone()
    if result:
        return jsonify(result)
    else:
        return '', 404


@app.route('/api/v1/classifieds_ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM classifieds_ads WHERE ad_id == ?;', (ad_id,))
    conn.commit()
    return ''


@app.route('/api/v1/classifieds_ads', methods=['POST'])
def add_ad():
    ad = request.json
    ad['created_at'] = datetime.now()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""INSERT INTO classifieds_ads(subject, body, price, email, created_at) 
            VALUES (?, ?, ?, ?, ?)""",
                        (ad['subject'], ad['body'], ad['price'], ad['email'], ad['created_at']))
    conn.commit()

    ad['ad_id'] = c.lastrowid
    return jsonify(ad), 201


if __name__ == '__main__':
    initiate_db()

    app.run()
