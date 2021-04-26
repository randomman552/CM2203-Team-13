from flask import Flask, render_template, url_for
from forms import InputStockForm

from machine_learning.naive_bayes import classify, get_summaries
from machine_learning.api import fetch_stock

app = Flask(__name__)
app.config['SECRET_KEY'] = '2c8553196a4dafa672b8c68d70a24e21eedb937d'

# Train naive bayes, or get previous training
app.config['ML_SUMMARIES'] = get_summaries()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/input_stock", methods=['GET', 'POST'])
def input_stock():
    form = InputStockForm()
    return render_template('input_stock.html', title='Input Stock', form=form)


@app.route("/evaluate/<symbol>")
def evaluate_stock(symbol: str):
    return str(classify(app.config['ML_SUMMARIES'], fetch_stock(symbol)))


if __name__ == '__main__':
    app.run(debug=True)

# For openshift deployment to work, app needs to be called application
application = app
