from flask import Flask, request, jsonify, session, send_from_directory
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

app.config["MONGO_URI"] = "mongodb://localhost:27017/finance-tracker"
mongo = PyMongo(app)

# User registration
@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    if users.find_one({"$or": [{"email": email}, {"username": username}]}):
        return jsonify({"error": "Email or username already exists"}), 409

    hash_pass = generate_password_hash(password)
    user_id = users.insert_one({'email': email, 'username': username, 'password': hash_pass}).inserted_id
    new_user = users.find_one({'_id': user_id})

    return jsonify({'email': new_user['email'], 'username': new_user['username']}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.json['email']
    password = request.json['password']
    user = users.find_one({'$or': [{'email': email}, {'username': email}]})

    if user and check_password_hash(user['password'], password):
        session['user_id'] = str(user['_id'])
        return jsonify({'email': user['email'], 'username': user['username']}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

# Fetch transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    transactions = list(mongo.db.transactions.find({'user_id': ObjectId(session['user_id'])}))
    for transaction in transactions:
        transaction['_id'] = str(transaction['_id'])
    return jsonify({'transactions': transactions}), 200

# Add transaction
@app.route('/transactions', methods=['POST'])
def add_transaction():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    transaction = {
        'user_id': ObjectId(session['user_id']),
        'description': request.json['description'],
        'amount': request.json['amount'],
        'date': request.json['date']
    }
    transaction_id = mongo.db.transactions.insert_one(transaction).inserted_id
    transaction['_id'] = str(transaction_id)
    return jsonify({'transaction': transaction}), 201

# Fetch expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    expenses = list(mongo.db.expenses.find({'user_id': ObjectId(session['user_id'])}))
    for expense in expenses:
        expense['_id'] = str(expense['_id'])
    return jsonify({'expenses': expenses}), 200

# Add expense
@app.route('/expenses', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    expense = {
        'user_id': ObjectId(session['user_id']),
        'description': request.json['description'],
        'amount': request.json['amount'],
        'date': request.json['date']
    }
    expense_id = mongo.db.expenses.insert_one(expense).inserted_id
    expense['_id'] = str(expense_id)
    return jsonify({'expense': expense}), 201

# Fetch revenues
@app.route('/revenues', methods=['GET'])
def get_revenues():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    revenues = list(mongo.db.revenues.find({'user_id': ObjectId(session['user_id'])}))
    for revenue in revenues:
        revenue['_id'] = str(revenue['_id'])
    return jsonify({'revenues': revenues}), 200

# Add revenue
@app.route('/revenues', methods=['POST'])
def add_revenue():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    revenue = {
        'user_id': ObjectId(session['user_id']),
        'description': request.json['description'],
        'amount': request.json['amount'],
        'date': request.json['date']
    }
    revenue_id = mongo.db.revenues.insert_one(revenue).inserted_id
    revenue['_id'] = str(revenue_id)
    return jsonify({'revenue': revenue}), 201

# Fetch profile
@app.route('/profile', methods=['GET'])
def get_profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify({'user': user}), 200
    return jsonify({"error": "User not found"}), 404

# Update profile
@app.route('/profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.form
    user_id = ObjectId(session['user_id'])

    update_data = {
        'name': data.get('name'),
        'id': data.get('id'),
        'address': data.get('address'),
        'occupation': data.get('occupation')
    }

    # Handle profile picture upload
    if 'profilePicture' in request.files:
        profile_picture = request.files['profilePicture']
        profile_picture_path = os.path.join('profile_pictures', str(user_id))
        profile_picture.save(profile_picture_path)
        update_data['profilePicture'] = profile_picture_path

    mongo.db.users.update_one({'_id': user_id}, {'$set': update_data})
    user = mongo.db.users.find_one({'_id': user_id})
    user['_id'] = str(user['_id'])
    return jsonify({'user': user}), 200

# Serve profile pictures
@app.route('/profile_pictures/<filename>')
def get_profile_picture(filename):
    return send_from_directory('profile_pictures', filename)

if __name__ == '__main__':
    app.run(debug=True)
