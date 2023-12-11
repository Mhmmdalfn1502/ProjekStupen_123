from flask import Flask, render_template, jsonify, request, url_for, session, redirect, flash, abort
from pymongo import MongoClient
from pymongo import DESCENDING
from datetime import datetime
import os

connection_string = 'mongodb+srv://mhmmdalfn1502:Alfanaja@cluster0.hh8koxv.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'
client = MongoClient(connection_string)
db = client.Harmony_Resort

app = Flask(__name__)
app.secret_key = "secret_key"

users = [{"email": "user1", "password": "password1"}]

@app.route('/')
def home():
    articles = list(db.ListKamar.find({}, {'_id': False}))
    contacts = list(db.contacts.find().sort('date_created', DESCENDING).limit(4))  # Menggunakan metode limit(4) untuk membatasi jumlah data
    return render_template('index.html', articles=articles, contacts=contacts, email=session.get('email'))


# @app.route('/')
# def home():
#     articles = list(db.ListKamar.find({}, {'_id': False}))
#     return render_template('index.html', articles=articles, email=session.get('email'))

# @app.route('/get_data', methods=['GET'])
# def get_data():
#     contacts = list(db.contacts.find())
#     return render_template('index.html', contacts=contacts)

@app.route('/admin/roomnames', methods=['GET'])
def get_room_names():
    room_names = list(db.ListKamar.find({}, {'Name': 1, '_id': False}))
    return jsonify({'room_names': room_names})

# CRUD

# @app.route('/admin', methods=['GET'])
# def show_Data_admin():
#     articles = list(db.ListKamar.find({}, {'_id':False}))
#     return jsonify({'admin.html': articles})

@app.route('/admin', methods=['GET'])
def show_Data():
    articles = list(db.ListKamar.find({}, {'_id':False}))
    return jsonify({'articles': articles})

@app.route('/admin', methods=['POST'])
def save_Data():
    Name_receive = request.form.get('Name_give')
    Price_receive = request.form.get('Price_give')

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d %H-%M-%S')

    file = request.files['file_give']
    file_extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{file_extension}'
    file.save(filename)

    doc = {
        'file': filename,
        'Name': Name_receive,
        'Price': Price_receive,
    }
    db.ListKamar.insert_one(doc)
    return jsonify({'message': 'data was saved!!!'})

@app.route('/edit/<Name>', methods=['GET', 'POST'])
def edit_item(Name):
    if request.method == 'GET':
        data = db.ListKamar.find_one({'Name': Name}, {'_id': False})
        return render_template('Edit.html', data=data)
    
    elif request.method == 'POST':
        new_Name = request.form.get('edit-Name')
        new_Price = request.form.get('edit-Price')

        update_data = {'$set': {'Name': new_Name, 'Price': new_Price}}
        db.ListKamar.update_one({'Name': Name}, update_data)

        return jsonify({'success': True, 'message': 'Changes saved successfully'})

@app.route('/delete/<Name>', methods=['DELETE'])
def delete_data(Name):
    try:
        db.ListKamar.delete_one({'Name': Name})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
def check_admin_role():
    if 'email' in session and session['role'] == 'admin':
        return True
    return False

@app.route('/admin-page')
def admin_page():
    return render_template('admin.html')
    
# SignUp and SignIn

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validasi password dan konfirmasi password
        if password != confirm_password:
            flash({'Password and Confirm Password do not match'})
            return render_template('signup.html')
        
        # Mengecek apakah alamat email sudah terdaftar
        existing_user = db.dataregis.find_one({'email': email})
        if existing_user:
            flash('Email is already registered. Please use a different email.', 'danger')
            return render_template('signup.html')

        # Simpan informasi pengguna ke database (gunakan MongoDB atau penyimpanan lainnya)
        db.dataregis.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "role": "user"  # Menambahkan peran pengguna
        })

        # Otentikasi pengguna (contoh sederhana)
        session['email'] = email

        # Jika Anda ingin menentukan peran admin secara langsung di sini,
        # sesuaikan logika berikut sesuai kebutuhan aplikasi Anda
        if email == "admin@HarmonyResort.com":
            session['role'] = "admin"

        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Mengecek keberadaan pengguna di database MongoDB
        user = db.dataregis.find_one({"email": email, "password": password})

        if user:
            session['email'] = email
            session['first_name'] = user.get('first_name', '')  # Menyimpan first_name dalam sesi
            session['last_name'] = user.get('last_name', '')  # Menyimpan last_name dalam sesi
            session['role'] = user.get('role', 'user')  # Ambil peran pengguna atau beri nilai default 'user'

            flash(f'Welcome, {session["first_name"]} {session["last_name"]}!', 'success')

            if session['role'] == 'admin':
                return redirect(url_for('admin_page'))  # Jika peran adalah 'admin', arahkan ke halaman admin

            return redirect(url_for('home'))  # Jika peran adalah 'user', arahkan ke halaman home
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('signin.html')

@app.route('/admin/checkemail/<email>', methods=['GET'])
def check_email(email):
    existing_email = db.dataregis.find_one({'email': email})
    if existing_email:
        abort(400, 'Email has already been registered.')
    return jsonify({'message': 'Email is available'})

@app.route('/signup')
def signin_page():
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    return redirect(url_for('home'))

# contact

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contacts_collection = db.contacts
        contacts_collection.insert_one({'name': name, 'email': email, 'message': message})
        return render_template('contact.html', success=True)
    else:
        return render_template('contact.html', email=session.get('email'))
    


@app.route('/about')
def about_us():
    return render_template('about.html', email=session.get('email'))

@app.route('/gallery')
def gallery():
    return render_template('gallery.html', email=session.get('email'))

@app.route('/book')
def order():
    if 'email' not in session:
        return redirect(url_for('signin'))
    else:
        return render_template('book.html')

if __name__== '__main__':
    app.run('0.0.0.0', port=5000, debug=True)