import time
import json
import random
import string
import sqlite3
from urllib.parse import urlparse
from flask import Flask, render_template, request, g
app = Flask(__name__)

DATABASE = 'database/urls.db'
def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
        return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def save_short_url():
    url_row = query_db('INSERT INTO urls SET long_url="?", short_code="?", date_added=?', [long_url, short_code, date_added], one=True)
    print(url_row)

def record_click(short_code):
    url_row = query_db('UPDATE urls SET click=click + 1 WHER short_code="?"', [short_code])
    print(url_row)


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    if not long_url:
        return '{ "error": "missing url" }'
    if urlparse(long_url).scheme == '':
        return '{ "error": "invalid url" }'

    url_row = query_db('SELECT * FROM urls WHERE long_url = ?', [long_url], one=True)
    if url_row:
        json_dict = {
            'long_url': url_row['long_url'],
            'short_code': url_row['short_code'],
            'click': url_row['click'],
            'date_added': url_row['date_added']
        }
        return json.dumps(json_dict)

    short_code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    date_added = time.time()
    url_row = query_db('SELECT *FROM urls WHERE short_code = ?', [short_code], one=True)
    while url_row:
        short_code = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        url_row = query_db('SELECT * FROM urls WHERE short_code = ?', [], one=True)
        

    json_dict = {
        'long_url': long_url,
        'short_code': short_code,
        'click': None,
        'date_added': date_added
    }
    save_short_url(long_url, short_code, date_added)

    return json.dumps(json_dict)

@app.route('/')
@app.route('/<short_code>')
def index_page(short_code=None):
    if short_code:
        url_row = query_db('SELECT * FROM urls WHERE long_url = ?', [long_url], one=True)
        if url_row:
            long_url = url_row['long_url']
            record_click(short_code=short_code)

            return redirect(long_url, code=302) 

    return render_template('index.html') 

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)


