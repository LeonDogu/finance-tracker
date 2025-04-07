import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            type TEXT,
            category TEXT,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_transaction(amount, ttype, category, note):
    try:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()

        # Sicherstellen, dass der Betrag ein float ist
        c.execute('INSERT INTO transactions (amount, type, category, note) VALUES (?, ?, ?, ?)',
                  (float(amount), ttype, category, note))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Fehler beim Hinzufügen der Transaktion in die DB: {e}")


def get_all_transactions():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return transactions

def get_expense_summary():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM transactions WHERE type = 'expense' GROUP BY category")
    data = c.fetchall()
    conn.close()
    return data
