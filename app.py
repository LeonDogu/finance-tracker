from flask import Flask, render_template, request, redirect, url_for
from database import (
    init_db,
    add_transaction,
    get_all_transactions,
    get_expense_summary,
    get_income_summary,
    get_balance,
    get_transactions_by_date,
    delete_transaction_by_id
)

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    transactions = get_all_transactions()
    expense_summary = get_expense_summary()
    income_summary = get_income_summary()
    balance = get_balance()
    daily_data = get_transactions_by_date()

    expense_labels = [row[0] for row in expense_summary]
    expense_values = [abs(row[1]) for row in expense_summary]

    income_labels = [row[0] for row in income_summary]
    income_values = [row[1] for row in income_summary]

    dates = [row[0] for row in daily_data]
    daily_amounts = [round(row[1], 2) for row in daily_data]

    # DEBUG
    print("EXPENSE LABELS:", expense_labels)
    print("INCOME LABELS:", income_labels)
    print("DATES:", dates)

    return render_template(
        "index.html",
        transactions=transactions,
        balance=balance,
        expense_labels=expense_labels,
        expense_values=expense_values,
        income_labels=income_labels,
        income_values=income_values,
        dates=dates,
        daily_amounts=daily_amounts
    )



@app.route('/add', methods=['POST'])
def add_transaction_route():
    amount = float(request.form['amount'])
    ttype = request.form['type']
    category = request.form['category']
    note = request.form['note']

    if ttype == 'expense' and amount > 0:
        amount *= -1

    add_transaction(amount, ttype, category, note)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_transaction(id):
    delete_transaction_by_id(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("Starte Flask-App...")
    app.run(debug=True)
