import sqlite3

def verify_data():
    conn = sqlite3.connect('zomato.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM restaurants LIMIT 5')
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()

if __name__ == '__main__':
    verify_data()
