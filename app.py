from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

def get_crypto_data(crypto="bitcoin", days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def analyze_data(df):
    avg_price = df['price'].mean()
    max_price = df['price'].max()
    min_price = df['price'].min()
    return avg_price, max_price, min_price

@app.route('/')
def home():
    df = get_crypto_data("bitcoin", days=7)
    avg_price, max_price, min_price = analyze_data(df)
    return render_template('index.html', 
                          avg_price=avg_price, 
                          max_price=max_price, 
                          min_price=min_price, 
                          data=df.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)