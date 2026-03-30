from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Database file ka naam
DB_FILE = 'employees.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Nayi table structure with 3 extra columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT,
            mobile TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    # Saare employees ko fetch karna
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    # Form se data nikalna
    emp_id = request.form['emp_id']
    name = request.form['name']
    role = request.form['role']
    email = request.form['email']
    address = request.form['address']
    mobile = request.form['mobile']
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''
        INSERT INTO employees (emp_id, name, role, email, address, mobile) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (emp_id, name, role, email, address, mobile))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    # Port 5000 par run karega
    app.run(debug=True)