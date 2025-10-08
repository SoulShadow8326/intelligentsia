import sqlite3
import json
import time
from pathlib import Path

DB_PATH = Path(__file__).parent / 'data.db'

def _conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def _ensure():
    conn = _conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        created_at INTEGER,
        updated_at INTEGER
    )''')
    conn.commit()
    conn.close()

def Create(payload):
    _ensure()
    now = int(time.time())
    data = json.dumps(payload)
    conn = _conn()
    cur = conn.cursor()
    cur.execute('INSERT INTO items (data, created_at, updated_at) VALUES (?, ?, ?)', (data, now, now))
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid

def Get(item_id=None):
    _ensure()
    conn = _conn()
    cur = conn.cursor()
    if item_id is None:
        cur.execute('SELECT * FROM items ORDER BY id DESC')
        rows = cur.fetchall()
        result = []
        for r in rows:
            try:
                payload = json.loads(r['data'])
            except Exception:
                payload = r['data']
            result.append({'id': r['id'], 'data': payload, 'created_at': r['created_at'], 'updated_at': r['updated_at']})
        conn.close()
        return result
    else:
        cur.execute('SELECT * FROM items WHERE id = ?', (item_id,))
        r = cur.fetchone()
        conn.close()
        if not r:
            return None
        try:
            payload = json.loads(r['data'])
        except Exception:
            payload = r['data']
        return {'id': r['id'], 'data': payload, 'created_at': r['created_at'], 'updated_at': r['updated_at']}

def Update(item_id, payload):
    _ensure()
    now = int(time.time())
    data = json.dumps(payload)
    conn = _conn()
    cur = conn.cursor()
    cur.execute('UPDATE items SET data = ?, updated_at = ? WHERE id = ?', (data, now, item_id))
    conn.commit()
    updated = cur.rowcount
    conn.close()
    return bool(updated)

def Delete(item_id):
    _ensure()
    conn = _conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    deleted = cur.rowcount
    conn.close()
    return bool(deleted)

if __name__ == '__main__':
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    _ensure()
    i = Create({'hello':'world'})
    print('created', i)
    print('all', Get())
    print('one', Get(i))
    print('update', Update(i, {'hello':'universe'}))
    print('one', Get(i))
    print('delete', Delete(i))
    print('all', Get())
