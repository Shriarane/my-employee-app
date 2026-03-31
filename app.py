import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client
from dotenv import load_dotenv

# Environment variables load ho rahe hain
load_dotenv()

app = Flask(__name__)

# Supabase Connection
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

@app.route('/')
def index():
    # Cloud (Supabase) se saara data fetch karna
    response = supabase.table("employees").select("*").execute()
    employees = response.data
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    # Form se data lena
    data = {
        "emp_id": request.form['emp_id'],
        "name": request.form['name'],
        "role": request.form['role'],
        "email": request.form['email'],
        "address": request.form['address'],
        "mobile": request.form['mobile']
    }
    
    # Cloud Database mein insert karna
    try:
        supabase.table("employees").insert(data).execute()
    except Exception as e:
        print(f"Error adding employee: {e}")
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Local testing ke liye port 5000
    app.run(debug=True)