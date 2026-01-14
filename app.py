from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Разрешить CORS для всех доменов

def init_db():
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        user TEXT,
        grade TEXT,
        subject TEXT,
        score INTEGER,
        total INTEGER,
        time_spent TEXT,
        time_spent_seconds INTEGER,
        is_custom INTEGER,
        timestamp REAL
    )''')
    conn.commit()
    conn.close()

@app.route('/results', methods=['GET'])
def get_results():
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()
    c.execute('SELECT * FROM results ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            'id': row[0],
            'date': row[1],
            'user': row[2],
            'grade': row[3],
            'subject': row[4],
            'score': row[5],
            'total': row[6],
            'time_spent': row[7],
            'time_spent_seconds': row[8],
            'is_custom': bool(row[9]),
            'timestamp': row[10]
        })
    
    return jsonify(results)

@app.route('/results', methods=['POST'])
def add_result():
    data = request.get_json()
    
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()
    c.execute('''INSERT INTO results 
        (date, user, grade, subject, score, total, time_spent, time_spent_seconds, is_custom, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['date'], data['user'], data['grade'], data['subject'], 
         data['score'], data['total'], data['timeSpent'], data['timeSpentSeconds'], 
         1 if data.get('isCustom') else 0, datetime.now().timestamp()))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)