from telegram.ext import Updater, MessageHandler, Filters
import yfinance as yf
import ta
import pandas as pd
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')  # Secure way to handle token

def ai_trading(update, context):
    message = update.message.text.upper().strip()
    chat_id = update.message.chat.id

    if message.startswith("CHECK"):
        try:
            ticker = message.split(" ")[1] + ".NS"
            data = yf.download(ticker, period="5d", interval="15m")

            if data.empty:
                context.bot.send_message(chat_id=chat_id, text=f"No data found for {ticker}")
                return

            close_prices = data['Close'].values.flatten()
            rsi_indicator = ta.momentum.RSIIndicator(pd.Series(close_prices), window=14)
            data['RSI'] = rsi_indicator.rsi().values

            latest_price = float(data['Close'].iloc[-1])
            latest_rsi = float(data['RSI'].iloc[-1])

            if latest_rsi < 30:
                signal = "BUY ✅"
            elif latest_rsi > 70:
                signal = "SELL ❌"
            else:
                signal = "WAIT ⏳"

            response = f"{ticker}\nPrice: ₹{latest_price:.2f}\nRSI: {latest_rsi:.2f}\nDecision: {signal}"
            context.bot.send_message(chat_id=chat_id, text=response)

        except Exception as e:
            context.bot.send_message(chat_id=chat_id, text=f"Error: {str(e)}")
    else:
        context.bot.send_message(chat_id=chat_id, text="❓ Please type: CHECK RELIANCE")

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), ai_trading))

updater.start_polling()
updater.idle()
