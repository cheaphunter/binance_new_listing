import json
from binance.client import Client
import keys
import datetime as dt
import smtplib, ssl
import other

### python email tutorial: https://realpython.com/python-send-email/

client = Client(api_key=keys.Pkey, api_secret=keys.Skey)
port = 465  # For SSL
sender = 'ross.c.dev@gmail.com'
receiver = 'ross_coates82@hotmail.com'

def get_pairs(quote):

    info = client.get_exchange_info()
    symbols = info['symbols']
    length = len(quote)
    pairs_list = []

    for item in symbols:
        if item['symbol'][-length:] == quote:
            pairs_list.append(item['symbol'])

    return pairs_list

with open ("pairs.txt", "r") as myfile:
    data = myfile.read()
    old_pairs = json.loads(data)
    # print(f'old pairs: {old_pairs}')

with open("pairs.txt", "w") as myfile:
    usdt_pairs = get_pairs('USDT')
    btc_pairs = get_pairs('BTC')
    bnb_pairs = get_pairs('BNB')

    current_pairs = json.dumps({'usdt': usdt_pairs, 'btc': btc_pairs, 'bnb': bnb_pairs})
    # print(f'current pairs: {current_pairs}')
    myfile.write(current_pairs)

print(f'{len(usdt_pairs)} USDT pairs\n{len(btc_pairs)} BTC pairs\n{len(bnb_pairs)} BNB pairs')

new_listings = []

for i in usdt_pairs:
    if i not in old_pairs.get('usdt'):
        new_listings.append(i)

for j in btc_pairs:
    if j not in old_pairs.get('btc'):
        new_listings.append(i)

for k in bnb_pairs:
    if k not in old_pairs.get('bnb'):
        new_listings.append(i)

if new_listings:
    print(new_listings)
    with open('new_listings.txt', 'a') as n:
        now = dt.now()
        logstring = f'{now.strftime("%X %x")} {new_listings}\n'
        n.write(logstring)

        # Create a secure SSL context
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("ross.c.dev@gmail.com", other.pw)
            server.sendmail(sender, receiver, logstring)
