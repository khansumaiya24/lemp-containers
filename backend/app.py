from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme')
DB_NAME = os.getenv('DB_NAME', 'appdb')

@app.get('/api/health')
def health():
    return {'status': 'ok'}

@app.get('/api')
def index():
    """Demo endpoint: verifies DB connectivity."""
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from MySQL via Flask!'")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message=row[0])

@app.get('/api/time')
def server_time():
    """Returns server time from MySQL using SELECT NOW()."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        cur = conn.cursor()
        cur.execute("SELECT NOW() AS server_time, @@global.time_zone AS tz")
        row = cur.fetchone()
        cur.close(); conn.close()
        # row[0] is server_time, row[1] is time_zone
        return jsonify(ok=True, time=row[0], mysql_time_zone=row[1])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
