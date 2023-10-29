import requests
from flask import Flask, jsonify, request
from flask_cors import CORS


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/cources', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    response_object['data'] = dict()
    post_data = request.get_json()
    data = get_data(post_data.get('symbol'), post_data.get('interval'))
    response_object['data'] = data
    return jsonify(response_object)


def get_data(symbol, interval):
    try:
        r = requests.get(f'https://api.binance.com/api/v3/klines?symbol={symbol.replace("/", "")}&interval={interval}')
    except:
        return False
    return [i[:5] for i in r.json()[:40]]


@app.route('/pairs', methods=['GET'])
def get_all_pairs():
    r = requests.get('https://api.binance.com/api/v1/exchangeInfo')
    data = r.json()
    symbols = [i['symbol'].replace('USDT', r'/USDT') for i in data['symbols'] if i['symbol'].endswith('USDT') and not (i['symbol'].endswith('UPUSDT') or i['symbol'].endswith('DOWNUSDT'))]
    return jsonify([i for i in symbols if r'/USDT' in i])


@app.route('/price_change', methods=['GET'])
def get_price_change():
    currency = request.args.get('currency')
    r = requests.get(f'https://api.binance.com/api/v1/ticker/24hr?symbol={currency}')
    persent = float(r.json()['priceChangePercent'])
    persent = f'+{persent}%' if persent > 0 else f'{persent}%'
    volume = int(float(r.json()['volume']))
    if volume > 10000:
        volume = f'${int(volume/1000)}K'
    volume = f'Volume {volume}'
    return jsonify({'persent': persent, 'volume': volume})


if __name__ == '__main__':
    app.run()
