from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///evm_wallet_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_record_key=True)
    address = db.Column(db.String(42), unique=True, nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_record_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    hash = db.Column(db.String(66), unique=True, nullable=False)
    value = db.Column(db.Float, nullable=False)
    datetime_recorded = db.Column(db.DateTime, nullable=False)

db.create_all()

@app.route('/wallet', methods=['POST'])
def add_wallet():
    request_data = request.json
    wallet_address = request_data.get('wallet_address')
    if not wallet_address:
        return jsonify({'error': 'Wallet address is required'}), 400
    new_wallet = Wallet(address=wallet_address)
    db.session.add(new_wallet)
    db.session.commit()
    return jsonify({'message': 'Wallet added successfully'}), 201

@app.route('/wallet/<wallet_address>/transaction', methods=['POST'])
def record_transaction(wallet_address):
    existing_wallet = Wallet.query.filter_by(address=wallet_address).first()
    if existing_wallet is None:
        return jsonify({'error': 'Wallet not found'}), 404
    
    transaction_data = request.json
    transaction_hash = transaction_data.get('transaction_hash')
    transaction_amount = transaction_data.get('amount')
    transaction_timestamp = transaction_data.get('timestamp')
    
    if not all([transaction_hash, transaction_amount, transaction_timestamp]):
        return jsonify({'error': 'Transaction hash, amount, and timestamp are required'}), 400

    new_transaction = Transaction(wallet_id=existing_wallet.id, hash=transaction_hash, value=transaction_amount, datetime_recorded=transaction_timestamp)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction recorded successfully'}), 201

@app.route('/wallet/<wallet_address>/transactions', methods=['GET'])
def list_transactions(wallet_address):
    existing_wallet = Wallet.query.filter_by(address=wallet_address).first()
    if existing_wallet is None:
        return jsonify({'error': 'Wallet not found'}), 404

    wallet_transactions = Transaction.query.filter_by(wallet_id=existing_wallet.id).all()
    transactions_response_data = [{
        'transaction_hash': transaction.hash,
        'amount': transaction.value,
        'timestamp': transaction.datetime_recorded
    } for transaction in wallet_transactions]
    return jsonify(transactions_response_parent_object), 200

@app.route('/send-notification', methods=['POST'])
def send_notification():
    request_data = request.json
    notification_message = request_data.get('message')
    print(f"Notification sent: {notification_message}")
    return jsonify({'message': 'Notification sent successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)