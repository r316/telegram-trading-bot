from telegram.ext import Updater, MessageHandler, Filters
import yfinance as yf
import ta
import pandas as pd

# 🔑 Paste your Bot Token here:
BOT_TOKEN = '8119549579:AAFcpFtSTnTi-KM66aZht-juzm1bZmDOlUY'

def ai_trading(update, context):
    message = update.message.text.upper().strip()

    if message.startswith("CHECK"):
        try:
            ticker = message.split(" ")[1] + ".NS"
            data = yf.download(ticker, period="5d", interval="15m")

            if data.empty:
                update.message.reply_text(f"No data found for {ticker}")
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
            update.message.reply_text(response)

        except Exception as e:
            update.message.reply_text(f"Error: {str(e)}")
    else:
        update.message.reply_text("❓ Please type: CHECK RELIANCE")

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text, ai_trading))

updater.start_polling()
print("✅ Bot is running... (Ctrl+C to stop)")
updater.idle()
