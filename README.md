# CryptoStock Portfolio Manager

#### Video Demo: [Watch the Video](https://www.youtube.com/watch?v=KQEegzzpwzI)

---

### Table of Contents

1. [Motivation](#motivation)
2. [Description](#description)
3. [Installation](#installation)
4. [Features](#features)
5. [Files Included](#files-included)
6. [Key Functionalities](#key-functionalities)
7. [Design Considerations](#design-considerations)
8. [Future Enhancements](#future-enhancements)
9. [Conclusion](#conclusion)

---
### Motivation
Managing both stocks and cryptocurrencies can be a challenging experience for investors. Most platforms designed for stock trading focus exclusively on stocks, while cryptocurrency platforms like Binance limit users to crypto trades, often offering a restricted range of assets. Even platforms that do offer both stocks and crypto typically provide only a limited selection of cryptocurrencies, leaving investors juggling multiple apps just to keep track of their portfolios.

On top of this, many of these apps are not fully transparent, often obscuring critical information such as the average buy price and total realised PnL (Profit and Loss). By keeping users in the dark about these key metrics, these platforms encourage users to continue buying without fully understanding their financial position, a practice that can feel more like gambling than investing.

**CryptoStock Tracker** was developed to address these gaps. It consolidates stocks and cryptocurrencies in a single platform, giving users a clear, real-time overview of their portfolios. By offering transparent tracking of all relevant data—including average buy prices, realised PnL, and more—this program empowers users to make informed investment decisions, helping them avoid risky behaviour driven by incomplete or hidden information.

---
### Description

**CryptoStock Tracker** is a Python-based portfolio management application designed to help users track both stock and cryptocurrency investments in a single platform. By combining data from **yfinance** and **CoinMarketCap**, the tool provides accurate and up-to-date market information, allowing users to monitor their diverse portfolios with ease.

The application allows users to create multiple portfolios to reflect different investment strategies. Users can track their assets based on real-time fetched prices, manage their portfolios by adding or selling assets, and view the total value of each portfolio. All data is stored locally in a JSON file, ensuring that portfolios persist across multiple sessions.

---
### Installation

Feel free to clone this repository.
A couple of steps are needed to get **CryptoStock Tracker** up and running:

#### Step 1: Clone the repository
You can either clone the repository to your local machine and push it to your own repository in your github account.
An explanation about how to go about that can be found in this Stackoverflow answer: https://stackoverflow.com/a/44076938/14517941

#### Step 2: Navigate to the project directory
Navigate to the project directory after cloning.

#### Step 3: Install the required dependencies
The project uses several external libraries such as yfinance, requests, and python-dotenv.
Use the `pip install -r requirements.txt` command to install all the modules.

#### Step 4: Setup your CoinMarketCap API key:
You need to create a `.env` file in the root directory to store your CoinMarketCap API key.
This file should contain the following: `CMC_API_KEY=your_coinmarketcap_api_key`.

Replace your_coinmarketcap_api_key with your actual API key obtained from the CoinMarketCap website.
You can obtain your own CoinMarketCap API key [here](https://coinmarketcap.com/academy/article/register-for-coinmarketcap-api).

#### Step 5: Run the program:
Once everything is set up, you can run the CryptoStock Tracker by executing: `python project.py`.
When you run the program, you will be presented with an interactive menu where you can:
- Create a new portfolio
- Add stocks and crypotocurrencies to an existing portfolio
- Sell stocks or cryptocurrencies
- View the total value of your portfolio
- Rename an existing portfolio
- Exit the program

---

### Features
- **Unified Portfolio Management**: Manage both stocks and cryptocurrencies in one place.

- **Portfolio Creation**: Create multiple portfolios for different investment strategies.

- **Add and Sell Assets**: Add or sell stocks and cryptocurrencies using ticker symbols and real-time validation.

- **Latest Price Updates**: Fetch the latest stock prices via **yfinance** and cryptocurrency prices via **CoinMarketCap**.

- **Transparent Tracking**: Clear and accessible metrics like average buy price, total realised PnL, and portfolio value.

- **Command-Line Interface**: Simple and intuitive CLI for portfolio management.

- **Data Persistence**: Portfolio data is saved to JSON files, ensuring that your portfolios persist across sessions.

---

### Files Included

- **`project.py`**:
  The main script implementing the program logic, including the `Portfolio` class, helper functions, and user interface.

- **`test_project.py`**:
  Contains unit tests for key functions to ensure the accuracy of the program.

- **`.env`**:
  A file used to securely store your CoinMarketCap API key.

- **`portfolios.json`**:
  A file used to store portfolio data (stocks and crypto), ensuring data persistence across multiple sessions.

---

### Key Functionalities

1. **Create and Manage Portfolios**:
   Users can create multiple portfolios and organize them by different investment strategies.

2. **Add Stocks and Cryptocurrencies**:
   Add both stocks and cryptocurrencies to a portfolio with live validation and pricing.

3. **Sell Stocks and Cryptocurrencies**:
   Sell assets while automatically updating portfolio metrics like realised PnL.

4. **View Portfolio Value**:
   Track the total value of a portfolio with up-to-date prices fetched through APIs.

5. **Rename Portfolios**:
   Rename portfolios for better organization and distinction.

---

### Design Considerations

The design of **CryptoStock Tracker** focuses on flexibility and ease of use. The program stores data in JSON format, allowing for straightforward data persistence between sessions. It integrates **yfinance** for stock prices and **CoinMarketCap** for cryptocurrency prices, ensuring accurate and up-to-date information. The clean separation between logic and user interface makes the code easy to extend and test.

---

### Future Enhancements

- **Historical Data**:
  Add functionality to track and display the historical performance of portfolios over time.

- **Graphical User Interface (GUI)**:
  Implement a GUI to provide a more visual and user-friendly experience.

- **Price Alerts**:
  Enable automated alerts to notify users when asset prices reach certain thresholds.

---

### Conclusion

**CryptoStock Tracker** offers a comprehensive solution for managing both stock and cryptocurrency portfolios in one place. By providing transparent and up-to-date information about key metrics such as average buy price and total realised PnL, this tool helps investors make better-informed decisions. Whether you are managing long-term investments or more frequent trades, **CryptoStock Tracker** ensures you have the clarity and control needed to track your financial position effectively.


---
