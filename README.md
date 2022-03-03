# Binance Bollinger Band Notification Bot
Querying Binance Future API and get Close/Last price and Calculating Bollinger Band(BB).
Sending message if some conditions met.
It loops Binance querying and sending with interval.(Chart is every 10Min, Message is 1Min)

# Requirement
* Python 3 (With dependency)

# How to install
## 1. Make virtual running environment
* Run `setup.sh`(Linux) or `setup.bat`(Window)

## 2. Create or inject `.env` file using `config.env`
* `TELEGRAM_TOKEN` is bot id created by Telegram's bot father (https://t.me/botfather)
* `TELEGRAM_DEFAULT_CHAT_ID` is default Chat ID if you have known chat id from created bot
* `BINANCE_API_KEY` is API key issued from Binance
* `BINANCE_API_SECRET_KEY` is SECRET API key issued from Binance
* `BINANCE_TRACE_SYMBOL` is ticker symbol to calculate Bollinger Band (e.g. `BTCUSDT`)
* `BINANCE_TRACE_INTERVAL` is calculate interval (e.g. `15m`)

# How to Run
## Run like daemon
`python main.py`

# Caveat
Use own discretion. It does not guarantee the secure information

# Credit
This project has the modified code of Yogesh K which is released under unidentified copyright
(Maybe Fair dealing for research or study) Go to https://blog.finxter.com/bollinger-bands-algorithm-python-binance-api-for-crypto-trading/
for original code
