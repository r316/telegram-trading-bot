from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yfinance as yf
import ta
import pandas as pd

BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Replace this with your token

async def ai_trading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.upper().strip()

    if message.startswith("CHECK"):
        try:
            ticker = message.split(" ")[1] + ".NS"
            data = yf.download(ticker, period="5d", interval="15m")

            if data.empty:
                await update.message.reply_text(f"No data found for {ticker}")
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
            await update.message.reply_text(response)

        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    else:
        await update.message.reply_text("❓ Please type: CHECK RELIANCE")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ai_trading))
app.run_polling()
