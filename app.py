from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(42), unique=True, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    transaction_hash = db.Column(db.String(66), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

db.create_all()

@app.route('/wallet', methods=['POST'])
def add_wallet():
    data = request.json
    wallet_address = data.get('wallet_address')
    if not wallet_address:
        return jsonify({'error': 'Wallet address is required'}), 400
    wallet = Wallet(wallet_address=wallet_address)
    db.session.add(wallet)
    db.session.commit()
    return jsonify({'message': 'Wallet added successfully'}), 201

@app.route('/wallet/<wallet_address>/transaction', methods=['POST'])
def track_transaction(wallet_address):
    wallet = Wallet.query.filter_by(wallet_address=wallet_address).first()
    if wallet is None:
        return jsonify({'error': 'Wallet not found'}), 404
    
    data = request.json
    transaction_hash = data.get('transaction_hash')
    amount = data.get('amount')
    timestamp = data.get('timestamp')
    
    if not all([transaction_hash, amount, timestamp]):
        return jsonify({'error': 'Transaction hash, amount, and timestamp are required'}), 400

    transaction = Transaction(wallet_id=wallet.id, transaction_hash=transaction_hash, amount=amount, timestamp=timestamp)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction added successfully'}), 201

@app.route('/wallet/<wallet_address>/transactions', methods=['GET'])
def get_transactions(wallet_address):
    wallet = Wallet.query.filter_by(wallet_address=wallet_address).first()
    if wallet is None:
        return jsonify({'error': 'Wallet not found'}), 404

    transactions = Transaction.query.filter_by(wallet_id=wallet.id).all()
    transactions_data = [{
        'transaction_hash': transaction.transaction_hash,
        'amount': transaction.amount,
        'timestamp': transaction.timestamp
    } for transaction in transactions]
    return jsonify(transactions_data), 200

@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.json
    message = data.get('message')
    print(f"Notification sent: {message}")
    return jsonify({'message': 'Notification sent successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)