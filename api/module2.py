import sqlite3

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class FinancialData(Resource):
    def get(self):
        # Retrieve query parameters
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        symbol = request.args.get("symbol")
        limit = int(request.args.get("limit", 5))
        page = int(request.args.get("page", 1))
        
        # Connect to database and retrieve requested data
        conn = sqlite3.connect("financial_stock.db")
        c = conn.cursor()
        
        query = "SELECT COUNT(*) FROM financial_data"
        if start_date:
            query += f" WHERE date >= '{start_date}'"
        if end_date:
            query += f" AND date <= '{end_date}'"
        if symbol:
            query += f" AND symbol = '{symbol}'"
        
        c.execute(query)
        total_count = c.fetchone()[0]
        
        query = "SELECT * FROM financial_data"
        if start_date:
            query += f" WHERE date >= '{start_date}'"
        if end_date:
            query += f" AND date <= '{end_date}'"
        if symbol:
            query += f" AND symbol = '{symbol}'"
        query += f" LIMIT {limit}"
        print(query)
        c.execute(query)
        results = c.fetchall()
        
        # Calculate pagination metadata
        total_pages = (total_count + limit - 1) // limit
        pagination = {
            "count": total_count,
            "page": page,
            "limit": limit,
            "pages": total_pages
        }
        
        # Format results as list of dicts
        data = []
        for row in results:
            data.append({
                "symbol": row[0],
                "date": row[1],
                "open_price": row[2],
                "close_price": row[3],
                "volume": row[4],
                "page": row[5]
            })
        
        # Close database connection
        conn.close()
        
        # Return response
        response = {
            "data": data,
            "pagination": pagination,
            "info": {}
        }
        return jsonify(response)

api.add_resource(FinancialData, "/financial-data")



# Define the route for the statistics endpoint
@app.route('/statistics')
def statistics():
    # Parse the query parameters from the request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    symbols = request.args.get('symbols').split(',')
    
    # Connect to the database
    conn = sqlite3.connect('financial_stock.db')
    cursor = conn.cursor()
    
    try:
        # Query the database for the specified date range and symbols
        data = []
        for symbol in symbols:
            cursor.execute('SELECT * FROM financial_data WHERE symbol = ? AND date BETWEEN ? AND ?', (symbol, start_date, end_date))
            rows = cursor.fetchall()
            
            # Calculate the average daily open price, closing price, and volume
            open_prices = [row[2] for row in rows]
            avg_open_price = sum(open_prices) / len(open_prices)
            
            close_prices = [row[3] for row in rows]
            avg_close_price = sum(close_prices) / len(close_prices)
            
            volumes = [row[4] for row in rows]
            avg_volume = sum(volumes) / len(volumes)
            
            # Add the statistics to the data array
            data.append({
                'symbol': symbol,
                'avg_open_price': avg_open_price,
                'avg_close_price': avg_close_price,
                'avg_volume': avg_volume
            })
        
        # Return the JSON response with the calculated statistics
        response = {
            'data': data,
            'info': {
                'status': 'success'
            }
        }
        
    except Exception as e:
        # Return an error response if an exception occurs
        response = {
            'data': [],
            'info': {
                'status': 'error',
                'message': str(e)
            }
        }
        
    finally:
        # Close the database connection
        conn.close()
        
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
