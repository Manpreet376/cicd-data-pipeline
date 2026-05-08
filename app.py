# app.py
from flask import Flask, render_template, request, send_file, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'csvcleanerpro2024'

UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fake users database (for now)
users = {}

# ===== HOME =====
@app.route('/')
def home():
    return render_template('index.html')

# ===== SIGNUP =====
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users:
            return render_template('signup.html', error='Email already exists!')
        users[email] = {'name': name, 'password': password}
        session['user'] = name
        return redirect(url_for('home'))
    return render_template('signup.html')

# ===== LOGIN =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users and users[email]['password'] == password:
            session['user'] = users[email]['name']
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid email or password!')
    return render_template('login.html')

# ===== LOGOUT =====
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ===== UPLOAD & CLEAN =====
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error='No file selected!')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No file selected!')

    if not file.filename.endswith('.csv'):
        return render_template('index.html', error='Please upload a CSV file only!')

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, 'uploaded.csv')
    file.save(filepath)

    try:
        result = clean_data(filepath)
        return render_template('result.html', 
                             original=result['original'],
                             cleaned=result['cleaned'],
                             stats=result['stats'])
    except Exception as e:
        return render_template('index.html', error=f'Error: {str(e)}')

# ===== CLEAN FUNCTION =====
def clean_data(filepath):
    df = pd.read_csv(filepath)
    original_rows = len(df)
    original_preview = df.head(5).to_html(classes='preview-table', index=False)

    # Cleaning steps
    df = df.drop_duplicates()
    df = df.dropna()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()

    cleaned_rows = len(df)
    cleaned_path = os.path.join(UPLOAD_FOLDER, 'cleaned.csv')
    df.to_csv(cleaned_path, index=False)
    cleaned_preview = df.head(5).to_html(classes='preview-table', index=False)

    return {
        'original': original_preview,
        'cleaned': cleaned_preview,
        'stats': {
            'original_rows': original_rows,
            'cleaned_rows': cleaned_rows,
            'removed_rows': original_rows - cleaned_rows,
            'columns': len(df.columns),
            'column_names': list(df.columns)
        }
    }

# ===== DOWNLOAD =====
@app.route('/download')
def download():
    path = os.path.join(UPLOAD_FOLDER, 'cleaned.csv')
    return send_file(path, as_attachment=True, download_name='cleaned_data.csv')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)