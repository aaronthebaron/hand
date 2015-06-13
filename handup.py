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
    url_row = query_db('insert into urls set long_url="?", short_code="?", date_added=?', [long_url, short_code, date_added], one=True)
    print(url_row)


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['url']
    if not long_url:
        return '{ "error": "missing url" }'
    if urlparse(long_url).scheme == '':
        return '{ "error": "invalid url" }'

    url_row = query_db('select * from urls where long_url = ?', [long_url], one=True)
    if url_row:
        json_dict = {
            'long_url': url_row['long_url'],
            'short_code': url_row['short_code'],
            'click': url_row['click'],
            'date_added': url_row['date_added']
        }
        #Pass back short url

    json_dict = {
        'long_url': long_url,
        'short_code': ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6)),
        'click': None,
        'date_added': time.time()
    }
    save_short_url()
    return json.dumps(json_dict)

@app.route('/')
def index_page():
    return render_template('index.html') 

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)


