from flask import Flask, request, render_template
from library import wrapper

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/plot_trend", methods=["GET", "POST"])
def get_investor_details():
    stock_code = request.form.get("stock_code", None)
    start_date = request.form.get("start_date", None)
    end_date = request.form.get("end_date", None)

    data = wrapper.get_investor_details(stock_code=stock_code, start_date=start_date, end_date=end_date)
    return render_template("plotter.html", data=data)


@app.route("/find_transactions", methods=["GET", "POST"])
def find_transactions():
    stock_code = request.form.get("stock_code", None)
    start_date = request.form.get("start_date", None)
    end_date = request.form.get("end_date", None)
    threshold = request.form.get("threshold", None)

    data = wrapper.find_transactions(stock_code=stock_code, start_date=start_date, end_date=end_date,
                                     threshold=threshold)
    return render_template("transactions.html", data=data)


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8080)
    app.run(host="0.0.0.0")
