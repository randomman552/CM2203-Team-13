from flask import Flask, render_template, request, session, redirect, url_for, Response, jsonify, abort
from Finance_Pull import *
from forms import InputStockForm
from machine_learning.naive_bayes import classify, get_summaries
from machine_learning.api import fetch_stock

app = Flask(__name__)
app.config['SECRET_KEY'] = '2c8553196a4dafa672b8c68d70a24e21eedb937d'

# Train naive bayes, or get previous training
app.config['ML_SUMMARIES'] = get_summaries()


# Error handling
def generic_error_route(code, exception):
    return render_template("error.html", code=code, text=str(exception))


@app.errorhandler(404)
def error_404_route(e):
    return generic_error_route(404, e)


@app.errorhandler(500)
def error_404_route(e):
    return generic_error_route(500, e)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/")
@app.route("/help")
def help():
    return render_template('help.html', title='Help Page')


# TODO: Link this page to the stock page
@app.route("/input_stock", methods=['GET', 'POST'])
def input_stock():
    form = InputStockForm()
    if request.method == 'POST':
        stock_name = request.form['stock_name']
        session['stock_name'] = stock_name

        return redirect(url_for('input_stock_post', stockTicker=session['stock_name']))
    else:
        return render_template('input_stock.html', title='Input Stock', form=form)


@app.route("/stock/<stockTicker>")
def input_stock_post(stockTicker):
    try:
        stock_evaluation = classify(app.config['ML_SUMMARIES'], fetch_stock(stockTicker))
        stock = stock_page(stockTicker)
    except RuntimeError as e:
        abort(500, description=e.args[0])
    except LookupError as e:
        abort(404, description=e.args[0])
    else:
        return render_template('stock.html', title=stockTicker, stock=stock, stock_evaluation=stock_evaluation)


@app.route("/stock/<stockTicker>.json")
def output_stock_json(stockTicker):
    try:
        stock = stock_page(stockTicker)
        out_dict = \
            {"@context": "https://schema.org",
             "@type": "Corporation",
             "tickerSymbol": stock["Symbol"],
             "Name": stock["Name"],
             "tickerValues": [
                 {
                     '@type': "PriceSpecification",
                     'price': stock['08. previous close']},
                 {
                     '@type': "PriceSpecification",
                     'price': stock['02. open']},
                 {
                     '@type': "AggregateOffer",
                     'lowPrice': stock['04. low'],
                     'highPrice': stock['03. high']},
                 {
                     '@type': "AggregateOffer",
                     'lowPrice': stock["52WeekLow"],
                     'highPrice': stock["52WeekHigh"]},
                 {
                     '@type': "PriceSpecification",
                     'price': stock["50DayMovingAverage"]},
                 {
                     '@type': "PriceSpecification",
                     'price': stock["200DayMovingAverage"]},
                 {
                     "@type": "PropertyValue",
                     "value": stock["MarketCapitalization"]},
                 {
                     '@type': "AggregateOffer",
                     'offerCount': stock['06. volume']},
                 {
                     "@type": "PriceSpecification",
                     "price": stock["EPS"]},
                 {
                     "@type": "PriceSpecification",
                     "price": stock["PERatio"]},
                 {
                     "@type": "Order",
                     "discount": stock['09. change'],
                 }
             ]
             }
    except RuntimeError as e:
        abort(500, description=e.args[0])
    except LookupError as e:
        abort(404, description=e.args[0])
    else:
        return jsonify(out_dict)


@app.route("/evaluate/<symbol>")
def evaluate_stock(symbol: str):
    return str(classify(app.config['ML_SUMMARIES'], fetch_stock(symbol)))


if __name__ == '__main__':
    app.run(debug=True)

# For openshift deployment to work, app needs to be called application
application = app
