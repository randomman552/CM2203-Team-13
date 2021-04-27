from flask import Flask, render_template, request

from Finance_Pull import *
from forms import InputStockForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '2c8553196a4dafa672b8c68d70a24e21eedb937d'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


# TODO: Link this page to the stock page
@app.route("/input_stock", methods=['GET', 'POST'])
def input_stock():
    form = InputStockForm()
    return render_template('input_stock.html', title='Input Stock', form=form)


@app.route("/stock/<stockTicker>")
def input_stock_post(stockTicker):
    stock = stock_page(stockTicker)
    return render_template('stock.html', title=stockTicker, stock=stock)


if __name__ == '__main__':
    app.run(debug=True)

# For openshift deployment to work, app needs to be called application
application = app
