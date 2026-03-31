from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client

app = Flask(__name__)

# Supabase Credentials (Wahi jo migrate.py mein use kiye the)
SUPABASE_URL = "https://jhhxjthrpdngwxpuodgq.supabase.co"
SUPABASE_KEY = "sb_secret_rbT1M125PxwbOwPyauRGhQ_wCvRRSZM"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    # Cloud se data fetch karna
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
    # Cloud (Supabase) mein insert karna
    supabase.table("employees").insert(data).execute()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)