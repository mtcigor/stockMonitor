from flask import Flask, render_template, request
import requests
import math

app = Flask(__name__)

def get_time_series_daily(ticker, compact=False):
    if compact:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=compact&apikey=demo'
    else:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=full&apikey=demo'
    r = requests.get(url)
    if r.status_code != 200:
        return
    return r.json()

def get_price(ticker):
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + ticker + '&apikey=demo'
    r = requests.get(url)
    data = r.json()
    return (data["Global Quote"]["05. price"])

def get_close_prices_list(timeSeries):
    # Clean and obtain the close Prices of the time series
    datesList = list()
    closePriceList = list()
    for va in timeSeries["Time Series (Daily)"]:
        datesList.append(va)
    for i in datesList:
        closePriceList.append(float(timeSeries["Time Series (Daily)"][i]["4. close"]))
    return closePriceList

def get_standard_deviation(timeSeries):
    returnList = get_close_prices_list(timeSeries)
    mean = sum(returnList)/len(returnList)
    variance = sum((i - mean) ** 2 for i in returnList) / len(returnList)
    return math.sqrt(variance)

def calculate_historic_volatility(timeSeries, timeSpan):
    stdDeviation = get_standard_deviation(timeSeries)
    return stdDeviation * math.sqrt(timeSpan)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        data = get_time_series_daily('IBM', True)
        return render_template('index.html', price=get_price(ticker), v6=round(calculate_historic_volatility(data, 6), 2), v100=round(calculate_historic_volatility(data, 100), 2))
    else:
        
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)