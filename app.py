from flask import Flask, request, render_template
from library import wrapper

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/fund_returns", methods=["GET", "POST"])
def get_investor_details():
    fund_ticker = request.form.get("fund_ticker", None)
    data = wrapper.get_fund_returns(fund_ticker)
    return render_template("fund_returns.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    # app.run(host="0.0.0.0")
