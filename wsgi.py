from flask import Flask, render_template, url_for
from forms import InputStockForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '33410096fed9b9c3b64e94d4cbef7440'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title = 'Home')

@app.route("/input_stock", methods=['GET', 'POST'])
def input_stock():
    form = InputStockForm()
    return render_template('input_stock.html', title = 'Input Stock', form = form)

if __name__ == '__main__':
    app.run(debug=True)
