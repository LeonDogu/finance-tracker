from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_transaction, get_all_transactions, get_expense_summary

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    transactions = get_all_transactions()
    summary = get_expense_summary()
    
    labels = [row[0] for row in summary]
    values = [abs(row[1]) for row in summary]

    return render_template("index.html", transactions=transactions, labels=labels, values=values)

@app.route('/add', methods=['POST'])
def add_transaction_route():
    amount = float(request.form['amount'])
    ttype = request.form['type']
    category = request.form['category']
    note = request.form['note']

    add_transaction(amount, ttype, category, note)

    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Starte Flask-App...")
    app.run(debug=True)
