from flask import Flask, jsonify, request
import sqlite3
from urllib.parse import parse_qs

app = Flask(__name__)

default_order_by = 'ad_id'
default_order = 'asc'


def initiate_db():
    conn = sqlite3.connect('classiffieds.db')
    c = conn.cursor()
    c.execute(
        """
            CREATE TABLE IF NOT EXISTS classiffieds_ads(
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

@app.route('/api/v1/classiffieds_ads', methods=['GET'])
def list_classifieds():
    conn = sqlite3.connect('classiffieds.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query = gen_query(request.query_string.decode())
    print(query)
    cur.execute(query)
    return jsonify(cur.fetchall())


def gen_query(query_str):
    parsed_str = parse_qs(query_str, encoding='utf-8')
    print(parsed_str)

    order_by = parsed_str.get('sortby', [default_order_by])[0]

    if order_by not in ['ad_id', 'price', 'created_at']:
        order_by = default_order_by

    order = parsed_str.get('sort', [default_order])[0]
    if order not in ['asc', 'desc']:
        order = default_order

    return f'SELECT * FROM classiffieds_ads ORDER BY {order_by} {order};'


@app.route('/api/v1/classiffieds_ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    conn = sqlite3.connect('classiffieds.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('SELECT * FROM classiffieds_ads WHERE ad_id == ?;', (ad_id,))
    return jsonify(cur.fetchone())


@app.route('/api/v1/classiffieds_ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    conn = sqlite3.connect('classiffieds.db')
    c = conn.cursor()
    c.execute('DELETE FROM classiffieds_ads WHERE ad_id == ?;', (ad_id,))
    conn.commit()
    return 'OK'


@app.route('/api/v1/classiffieds_ads', methods=['POST'])
def add_classified():
    conn = sqlite3.connect('classiffieds.db')
    c = conn.cursor()
    c.execute("""INSERT INTO classiffieds_ads(subject, body, price, email, created_at) 
            VALUES (?, ?, ?, ?, datetime('now'))""",
                        (request.json['subject'], request.json['body'], request.json['price'], request.json['email']))
    conn.commit()

    return str(c.lastrowid)


if __name__ == '__main__':
    initiate_db()

    app.run()
