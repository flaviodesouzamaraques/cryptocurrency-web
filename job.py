from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from app import db, CryptocurrencyQuote

sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=30)
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

    new_quote = CryptocurrencyQuote(symbol=symbol, price_currency=price_currency,
                                    price_amount=price_amount, timestamp=timestamp)

    with Session(db.engine) as session:
        try:
            session.add(new_quote)
        except:
            session.rollback()
        else:
            session.commit()
            print(f"quote saved: {str(new_quote)}")


if __name__ == '__main__':
    sched.start()