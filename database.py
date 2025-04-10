import sqlite3

DB_PATH = "data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            type TEXT,
            category TEXT,
            note TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(amount, ttype, category, note):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO transactions (amount, type, category, note)
        VALUES (?, ?, ?, ?)
    ''', (amount, ttype, category, note))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM transactions ORDER BY date DESC')
    result = c.fetchall()
    conn.close()
    return result

def get_expense_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT category, SUM(amount) FROM transactions
        WHERE type = 'expense'
        GROUP BY category
    """)
    data = c.fetchall()
    conn.close()
    return data

def get_income_summary():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
        SELECT category, SUM(amount) FROM transactions
        WHERE type = 'income'
        GROUP BY category
    """)
    data = c.fetchall()
    conn.close()
    return data


def get_balance():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM transactions")
    balance = c.fetchone()[0] or 0
    conn.close()
    return round(balance, 2)

def get_transactions_by_date():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT DATE(date), SUM(amount) FROM transactions
        GROUP BY DATE(date)
        ORDER BY DATE(date)
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def delete_transaction_by_id(transaction_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()
