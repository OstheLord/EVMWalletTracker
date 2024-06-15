import os
import requests
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables
load_dotenv()

# Retrieve INFURA_URL and WALLET_ADDRESS from the environment
INFURA_URL = os.getenv("INFURA_URL")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

def connect_to_network(url):
    """Connects to the EVM network."""
    w3 = Web3(Web3.HTTPProvider(url))
    print("Connected to EVM network" if w3.isConnected() else "Failed to connect to EVM network")
    return w3

def monitor_transactions(w3, wallet_address):
    """Monitors and prints transactions involving the specified wallet address."""
    latest_block = w3.eth.get_block('latest')
    print(f"Latest block: {latest_block.number}")
  
    for tx_hash in latest_block.transactions:
        tx = w3.eth.get_transaction(tx_hash)
        if wallet_address.lower() in (tx['to'].lower(), tx['from'].lower()):
            print(f"Transaction found: {tx_hash.hex()}")
            get_transaction_details(w3, tx_hash.hex())

def get_transaction_details(w3, tx_hash):
    """Retrieves and displays details for a given transaction hash."""
    tx = w3.eth.get_transaction(tx_hash)
    details = {
        'Transaction Hash': tx_hash,
        'Block Number': tx['blockNumber'],
        'From': tx['from'],
        'To': tx['to'],
        'Value': w3.fromWei(tx['value'], 'ether'),
        'Gas': tx['gas'],
        'Gas Price': w3.fromWei(tx['gasPrice'], 'gwei'),
        'Nonce': tx['nonce']
    }
    for key, value in details.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    w3 = connect_to_network(INFURA_URL)
    monitor_transactions(w3, WALLET_ADDRESS)