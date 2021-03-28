from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import sqlite3
from datetime import datetime

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=1)
def timed_job():
    res = requests.get(
        'https://api.cryptonator.com/api/full/btc-brl',
        headers={
            'Accept': 'application/json',
            'Host': 'api.cryptonator.com',
            'User-Agent': 'cryptocurrency-web',
        },
    )

    json = res.json()
    ticker = json["ticker"]

    symbol = ticker["base"]
    price_currency = ticker["target"]
    price_amount = ticker["price"]
    timestamp = datetime.fromtimestamp(json["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

    print(timestamp)
    conn = sqlite3.connect('local.db')
    print(f"INSERT INTO cryptocurrency_quotes (symbol, price_currency, price_amount, timestamp) VALUES ('{symbol}', '{price_currency}', {price_amount}, '{timestamp}')")
    conn.execute(f"INSERT INTO cryptocurrency_quotes (symbol, price_currency, price_amount, timestamp) VALUES ('{symbol}', '{price_currency}', {price_amount}, '{timestamp}')")
    print(ticker["base"], ' ', ticker["target"], ticker["price"], ' ', ticker["price"], ' ', timestamp)
    conn.commit()
    conn.close()

sched.start()