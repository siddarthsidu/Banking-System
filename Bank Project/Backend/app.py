import sqlite3
from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Serve the index.html file
@app.route('/')
def home():
    return send_from_directory('static', 'Index.html')

# Function to get a database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('bank.db')
    return g.db

# Close the database connection when the app context ends
@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# API endpoint to create a new account
@app.route('/create_account', methods=['POST'])
def create_account():
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()
    cursor.execute('''INSERT INTO accounts (account_number, account_type, customer_name, customer_phone, customer_age, customer_address)
                      VALUES (?, ?, ?, ?, ?, ?)''', 
                   (data['account_number'], data['account_type'], data['customer_name'], data['customer_phone'], data['customer_age'], data['customer_address']))
    cursor.execute('''INSERT INTO balances (account_number, balance) VALUES (?, ?)''', 
                   (data['account_number'], 0))
    db.commit()
    return jsonify({'message': 'Account created successfully'}), 201

# API endpoint to check balance
@app.route('/check_balance/<account_number>', methods=['GET'])
def check_balance(account_number):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT balance FROM balances WHERE account_number = ?', (account_number,))
    balance = cursor.fetchone()
    if balance:
        return jsonify({'balance': balance[0]}), 200
    else:
        return jsonify({'message': 'Account not found'}), 404

# API endpoint to deposit money
@app.route('/deposit', methods=['POST'])
def deposit():
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()
    cursor.execute('SELECT balance FROM balances WHERE account_number = ?', (data['account_number'],))
    balance = cursor.fetchone()
    if balance:
        new_balance = balance[0] + int(data['amount'])
        cursor.execute('UPDATE balances SET balance = ? WHERE account_number = ?', (new_balance, data['account_number']))
        db.commit()
        return jsonify({'message': 'Deposit successful'}), 200
    else:
        return jsonify({'message': 'Account not found'}), 404

# API endpoint to withdraw money
@app.route('/withdraw', methods=['POST'])
def withdraw():
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()
    cursor.execute('SELECT balance FROM balances WHERE account_number = ?', (data['account_number'],))
    balance = cursor.fetchone()
    if balance:
        if balance[0] >= int(data['amount']):
            new_balance = balance[0] - int(data['amount'])
            cursor.execute('UPDATE balances SET balance = ? WHERE account_number = ?', (new_balance, data['account_number']))
            db.commit()
            return jsonify({'message': 'Withdrawal successful'}), 200
        else:
            return jsonify({'message': 'Insufficient funds'}), 400
    else:
        return jsonify({'message': 'Account not found'}), 404

# API endpoint to delete an account
@app.route('/delete_account/<account_number>', methods=['DELETE'])
def delete_account(account_number):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM accounts WHERE account_number = ?', (account_number,))
    cursor.execute('DELETE FROM balances WHERE account_number = ?', (account_number,))
    db.commit()
    return jsonify({'message': 'Account deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)