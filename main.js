import axios from 'axios';
import dotenv from 'dotenv';
dotenv.config();

document.addEventListener('DOMContentLoaded', function() {
  const walletAddressInput = document.getElementById('walletAddr');
  const telegramBotTokenInput = document.getElementById('telegramBotToken');
  const telegramChatIdInput = document.getElementById('telegramChatID');
  const updateConfigurationButton = document.getElementById('updateConfigBtn');
  const fetchTransactionsButton = document.getElementById('fetchTransactionsBtn');
  const transactionsDisplayElement = document.getElementById('transactionsDisplay');

  async function fetchWalletTransactions(walletAddress) {
    try {
      const response = await axios.get(`${process.env.BACKEND_URL}/transactions/${walletAddress}`);
      transactionsDisplayElement.innerHTML = JSON.stringify(response.data, null, 2);
    } catch (error) {
      console.error('Error fetching wallet transactions', error);
      transactionsDisplayElement.innerHTML = 'Failed to load transactions';
    }
  }

  async function updateWalletConfiguration(walletAddress, telegramBotToken, telegramChatID) {
    try {
      const response = await axios.post(`${process.env.BACKEND_URL}/updateConfig`, {
        walletAddress,
        telegramBotToken,
        telegramChatID
      });
      console.log('Wallet configuration updated successfully', response.data);
    } catch (error) {
      console.error('Error updating wallet configuration', error);
    }
  }

  fetchTransactionsButton.addEventListener('click', function() {
    fetchWalletTransactions(walletAddressInput.value);
  });

  updateConfigurationButton.addEventListener('click', function() {
    updateWalletConfiguration(walletAddressInput.value, telegramBotTokenInput.value, telegramChatIdInput.value);
  });
});