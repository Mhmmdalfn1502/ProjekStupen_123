from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os

connection_string = 'mongodb+srv://mhmmdalfn1502:Alfanaja@cluster0.hh8koxv.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp'
client = MongoClient(connection_string)
db = client.Harmony_Resort

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/admin', methods=['GET'])
# def show_Data_admin():
#     articles = list(db.ListKamar.find({}, {'_id':False}))
#     return jsonify({'admin.html': articles})

@app.route('/admin', methods=['GET'])
def show_Data():
    articles = list(db.ListKamar.find({}, {'_id':False}))
    return jsonify({'articles': articles})

# @app.route('/', methods=['GET'])
# def show_data_index():
#     articles = list(db.ListKamar.find({}, {'_id': False}))
#     return render_template('index.html', articles=articles)


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

# Inside your Flask app
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
    
@app.route('/admin-page')
def admin_page():
    return render_template('admin.html')

if __name__== '__main__':
    app.run('0.0.0.0', port=5000, debug=True)