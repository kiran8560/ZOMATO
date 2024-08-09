from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('zomato.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/restaurant/<int:id>', methods=['GET'])
def get_restaurant_details(id):
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM restaurants WHERE restaurant_id = ?', (id,)).fetchone()
    conn.close()
    if restaurant is None:
        return "Restaurant not found", 404
    #return render_template('restaurant_detail.html', restaurant=restaurant)
    return jsonify(dict(restaurant)) 

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    conn = get_db_connection()

    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page

    # Filtering parameters
    country = request.args.get('country')
    min_average_cost = request.args.get('min_average_cost')
    max_average_cost = request.args.get('max_average_cost')
    cuisines = request.args.get('cuisines')
    search = request.args.get('search')

    # Base query
    query = 'SELECT * FROM restaurants WHERE 1=1'
    params = []

    # Add filters to the query
    if country:
        query += ' AND country_code = ?'
        params.append(country)
    if min_average_cost:
        query += ' AND average_cost_for_two >= ?'
        params.append(min_average_cost)
    if max_average_cost:
        query += ' AND average_cost_for_two <= ?'
        params.append(max_average_cost)
    if cuisines:
        query += ' AND cuisines LIKE ?'
        params.append(f'%{cuisines}%')
    if search:
        query += ' AND (name LIKE ? OR address LIKE ?)'
        params.append(f'%{search}%')
        params.append(f'%{search}%')

    # Add pagination to the query
    query += ' LIMIT ? OFFSET ?'
    params.append(per_page)
    params.append(offset)

    # Fetch restaurants with filters and pagination
    restaurants = conn.execute(query, params).fetchall()
    total_restaurants = conn.execute('SELECT COUNT(*) FROM restaurants WHERE 1=1').fetchone()[0]

    conn.close()

    return render_template('restaurant_list.html', restaurants=restaurants, page=page, per_page=per_page, total_restaurants=total_restaurants)

@app.route('/api/restaurant/<int:id>', methods=['GET'])
def api_get_restaurant_by_id(id):
    conn = get_db_connection()
    restaurant = conn.execute('SELECT * FROM restaurants WHERE restaurant_id = ?', (id,)).fetchone()
    conn.close()
    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404
    return jsonify(dict(restaurant))

@app.route('/api/restaurants', methods=['GET'])
def api_get_restaurants():
    conn = get_db_connection()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    offset = (page - 1) * per_page

    country = request.args.get('country')
    min_average_cost = request.args.get('min_average_cost')
    max_average_cost = request.args.get('max_average_cost')
    cuisines = request.args.get('cuisines')
    search = request.args.get('search')

    query = 'SELECT * FROM restaurants WHERE 1=1'
    params = []

    if country:
        query += ' AND country_code = ?'
        params.append(country)
    if min_average_cost:
        query += ' AND average_cost_for_two >= ?'
        params.append(min_average_cost)
    if max_average_cost:
        query += ' AND average_cost_for_two <= ?'
        params.append(max_average_cost)
    if cuisines:
        query += ' AND cuisines LIKE ?'
        params.append(f'%{cuisines}%')
    if search:
        query += ' AND (name LIKE ? OR address LIKE ?)'
        params.append(f'%{search}%')
        params.append(f'%{search}%')

    query += ' LIMIT ? OFFSET ?'
    params.append(per_page)
    params.append(offset)

    restaurants = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(restaurant) for restaurant in restaurants])

if __name__ == '__main__':
    app.run(debug=True)
