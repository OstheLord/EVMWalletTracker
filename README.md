# EVMWalletTracker

This project tracks transactions on an EVM wallet and sends notifications to Telegram using Python for the backend and HTML/CSS/JavaScript for the frontend.

## Structure

- **HTML/CSS/JavaScript**: Handles the frontend interface.
- **Python**: Manages backend processing, database interactions, and transaction tracking.
- **Telegram**: Sends notifications via Telegram bot.

## Setup

### HTML/CSS/JavaScript
1. Open the `index.html` file in a web browser to view the frontend interface.

### Python
1. Install Python if it is not already installed.
2. Navigate to the project directory and create a virtual environment:
    ```
    python -m venv venv
    ```
3. Activate the virtual environment:
    - On Windows:
        ```
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```
        source venv/bin/activate
        ```
4. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Set up the environment variables by creating a `.env` file in the `config` directory with the following content:
    ```
    FLASK_APP=app.py
    DATABASE_URL=sqlite:///tracker.db
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    ```
6. Initialize the database:
    ```
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```
7. Run the Python application:
    ```
    flask run
    ```

## Overview

1. HTML/CSS/JavaScript provides a user interface for connecting a wallet, viewing recent transactions, and configuring Telegram notifications.
2. Python processes the transaction data, interacts with the database, and sends notifications.
3. Telegram bot sends notifications to the user's Telegram account for every transaction.
