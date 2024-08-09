import sqlite3

def create_tables():
    conn = sqlite3.connect('zomato.db')
    cur = conn.cursor()

    # Create the restaurants table with all columns from the CSV
    cur.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            restaurant_id INTEGER PRIMARY KEY,
            name TEXT,
            country_code INTEGER,
            city TEXT,
            address TEXT,
            locality TEXT,
            locality_verbose TEXT,
            longitude REAL,
            latitude REAL,
            cuisines TEXT,
            average_cost_for_two INTEGER,
            currency TEXT,
            has_table_booking TEXT,
            has_online_delivery TEXT,
            is_delivering_now TEXT,
            switch_to_order_menu TEXT,
            price_range INTEGER,
            aggregate_rating REAL,
            rating_color TEXT,
            rating_text TEXT,
            votes INTEGER
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
