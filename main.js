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
      if (response.status === 200) {
        transactionsDisplayElement.innerHTML = JSON.stringify(response.data, null, 2);
      } else {
        console.error(`Error fetching wallet transactions: ${response.status}`);
        transactionsDisplayElement.innerHTML = `Error: Unable to fetch transactions for address ${walletAddress}`;
      }
    } catch (error) {
      console.error('Error fetching wallet transactions', error);
      transactionsDisplayElement.innerHTML = `Failed to load transactions due to an error: ${error.message}`;
    }
  }

  async function updateWalletConfiguration(walletAddress, telegramBotToken, telegramChatID) {
    try {
      const response = await axios.post(`${process.env.BACKEND_URL}/updateConfig`, {
        walletAddress,
        telegramBotToken,
        telegramChatID
      });

      if (response.status === 200) {
        console.log('Wallet configuration updated successfully', response.data);
      } else {
        console.error(`Error updating wallet configuration: ${response.status}`);
        alert(`Configuration update failed: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error updating wallet configuration', error);
      alert(`Configuration update failed due to an error: ${error.message}`);
    }
  }

  fetchTransactionsButton.addEventListener('click', function() {
    if (walletAddressInput.value === '') {
      alert('Please enter a wallet address.');
      return;
    }
    fetchWalletNotifications(walletAddressInput.value);
  });

  updateConfigurationButton.addEventListener('click', function() {
    if (walletAddressInput.value === '' || telegramBotTokenInput.value === '' || telegramChatIdInput.value === '') {
      alert('Please ensure all fields are filled out.');
      return;
    }
    updateWalletConfiguration(walletAddressInput.value, telegramBotTokenInput.value, telegramChatIdInput.value);
  });
});