from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 簡單的記憶體內資料儲存（關閉程式後會消失）
data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    date_str = request.form.get("date")
    category = request.form.get("category")
    amount = float(request.form.get("amount"))

    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    month_key = date.strftime("%Y-%m")

    if month_key not in data:
        budget = float(request.form.get("budget"))
        data[month_key] = {"budget": budget, "expenses": {}}

    month_data = data[month_key]
    month_data["expenses"].setdefault(date, []).append({"category": category, "amount": amount})

    return redirect(url_for("summary", month=month_key))

@app.route("/summary")
def summary():
    month = request.args.get("month")
    if month not in data:
        return f"找不到 {month} 的資料"

    month_data = data[month]
    total_spent = sum(e["amount"] for v in month_data["expenses"].values() for e in v)
    remaining = month_data["budget"] - total_spent

    return render_template("summary.html", month=month, data=month_data, total_spent=total_spent, remaining=remaining)

if __name__ == "__main__":
    app.run(debug=True)
