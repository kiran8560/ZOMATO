import sqlite3
import csv

def load_data():
    conn = sqlite3.connect('zomato.db')
    cur = conn.cursor()

    with open('zomato.csv', 'r', encoding='latin1') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            cur.execute('''
                INSERT OR IGNORE INTO restaurants (restaurant_id, name, country_code, city, address, locality, locality_verbose, longitude, latitude, cuisines, average_cost_for_two, currency, has_table_booking, has_online_delivery, is_delivering_now, switch_to_order_menu, price_range, aggregate_rating, rating_color, rating_text, votes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    load_data()
