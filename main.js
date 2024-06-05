import axios from 'axios';
import dotenv from 'dotenv';
dotenv.config();
document.addEventListener('DOMContentLoaded', function() {
  const walletInput = document.getElementById('walletAddr');
  const telegramBotTokenInput = document.getElementById('telegramBotToken');
  const telegramChatIdInput = document.getElementById('telegramChatID');
  const updateConfigBtn = document.getElementById('updateConfigBtn');
  const fetchTransactionsBtn = document.getElementById('fetchTransactionsBtn');
  const transactionsDisplay = document.getElementById('transactionsDisplay');
  async function fetchTransactions(walletAddress) {
    try {
      const response = await axios.get(`${process.env.BACKEND_URL}/transactions/${walletAddress}`);
      transactionsDisplay.innerHTML = JSON.stringify(response.data, null, 2);
    } catch (error) {
      console.error('Error fetching transactions', error);
      transactionsDisplay.innerHTML = 'Failed to load transactions';
    }
  }
  async function updateConfiguration(walletAddress, telegramBotToken, telegramChatID) {
    try {
      const response = await axios.post(`${process.env.BACKEND_URL}/updateConfig`, {
        walletAddress,
        telegramBotToken,
        telegramChatID
      });
      console.log('Configuration updated successfully', response.data);
    } catch (error) {
      console.error('Error updating configuration', error);
    }
  }
  fetchTransactionsBtn.addEventListener('click', function() {
    fetchTransactions(walletInput.value);
  });
  updateConfigExampleBtn.addEventListener('click', function() {
    updateConfiguration(walletInput.value, telegramBotTokenInput.value, telegramChatIdInput.value);
  });
});