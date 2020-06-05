from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

classiffieds_ads = []


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

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/classiffieds_ads', methods=['GET'])
def list_classifieds():
    conn = sqlite3.connect('classiffieds.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('SELECT * FROM classiffieds_ads;')
    return jsonify(cur.fetchall())


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/classiffieds_ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    conn = sqlite3.connect('classiffieds.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('SELECT * FROM classiffieds_ads WHERE ad_id == ?;', (ad_id,))
    return jsonify(cur.fetchone())


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/classiffieds_ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    conn = sqlite3.connect('classiffieds.db')
    c = conn.cursor()
    c.execute('DELETE FROM classiffieds_ads WHERE ad_id == ?;', (ad_id,))
    conn.commit()
    return 'OK'


# A route to return all of the available entries in our catalog.
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
