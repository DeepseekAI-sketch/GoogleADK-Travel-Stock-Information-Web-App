import datetime
from zoneinfo import ZoneInfo
from flask import Flask, render_template, request, jsonify
import yfinance as yf
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('./.env')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# ------ Travel Info Functions ------

def search_airbnb_listings(city: str) -> dict:
    """Simulates searching for Airbnb listings in a given city with details.

    Args:
        city (str): The city to search for Airbnb listings.

    Returns:
        dict: status and listings or an error message.
    """
    sample_listings = {
        "new york": [
            {
                "title": "Cozy Studio in Manhattan",
                "price_per_night": "$150",
                "location_highlights": "Close to Central Park and subway stations",
            },
            {
                "title": "Modern Loft in Brooklyn",
                "price_per_night": "$120",
                "location_highlights": "Great nightlife and cafes nearby",
            },
        ],
        "san francisco": [
            {
                "title": "Chic Apartment near Golden Gate Park",
                "price_per_night": "$180",
                "location_highlights": "Quiet neighborhood, walkable to park",
            },
            {
                "title": "Sunny Mission District Flat",
                "price_per_night": "$140",
                "location_highlights": "Vibrant area with restaurants and shops",
            },
        ],
    }

    city_key = city.lower()
    if city_key in sample_listings:
        return {"status": "success", "listings": sample_listings[city_key]}
    else:
        return {
            "status": "error",
            "error_message": f"No Airbnb data available for '{city}'.",
        }

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city.

    Returns:
        dict: status and time info or error.
    """
    tz_map = {
        "new york": "America/New_York",
        "san francisco": "America/Los_Angeles",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
    }

    city_key = city.lower()
    if city_key not in tz_map:
        return {
            "status": "error",
            "error_message": f"No timezone data available for '{city}'.",
        }

    tz = ZoneInfo(tz_map[city_key])
    now = datetime.datetime.now(tz)
    return {
        "status": "success",
        "report": f"The current time in {city.title()} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    }

def get_weather(city: str) -> dict:
    """Simulates retrieving the weather for a given city.

    Args:
        city (str): The name of the city.

    Returns:
        dict: status and weather info or error.
    """
    sample_weather = {
        "new york": "Sunny, 25°C (77°F)",
        "san francisco": "Foggy, 18°C (64°F)",
        "london": "Cloudy, 16°C (61°F)",
        "tokyo": "Rainy, 22°C (72°F)",
    }

    city_key = city.lower()
    if city_key not in sample_weather:
        return {
            "status": "error",
            "error_message": f"No weather data available for '{city}'.",
        }

    return {
        "status": "success",
        "report": f"The weather in {city.title()} is {sample_weather[city_key]}."
    }

# ------ Stock Price Functions ------

def get_stock_price(symbol: str):
    """
    Retrieves the current stock price for a given symbol.

    Args:
        symbol (str): The stock symbol (e.g., "AAPL", "GOOG").

    Returns:
        float: The current stock price, or None if an error occurs.
    """
    try:
        stock = yf.Ticker(symbol)
        historical_data = stock.history(period="1d")
        if not historical_data.empty:
            current_price = historical_data['Close'].iloc[-1]
            return {
                "status": "success", 
                "symbol": symbol,
                "price": current_price
            }
        else:
            return {
                "status": "error",
                "error_message": f"No data available for stock symbol '{symbol}'."
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error retrieving stock price for {symbol}: {str(e)}"
        }

# ------ API Routes ------

@app.route('/api/airbnb', methods=['GET'])
def airbnb_api():
    city = request.args.get('city', '')
    if not city:
        return jsonify({"status": "error", "error_message": "City parameter is required"})
    
    return jsonify(search_airbnb_listings(city))

@app.route('/api/time', methods=['GET'])
def time_api():
    city = request.args.get('city', '')
    if not city:
        return jsonify({"status": "error", "error_message": "City parameter is required"})
    
    return jsonify(get_current_time(city))

@app.route('/api/weather', methods=['GET'])
def weather_api():
    city = request.args.get('city', '')
    if not city:
        return jsonify({"status": "error", "error_message": "City parameter is required"})
    
    return jsonify(get_weather(city))

@app.route('/api/stock', methods=['GET'])
def stock_api():
    symbol = request.args.get('symbol', '')
    if not symbol:
        return jsonify({"status": "error", "error_message": "Stock symbol parameter is required"})
    
    return jsonify(get_stock_price(symbol))

# Define the function without decorator
def create_templates():
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    if not os.path.exists('templates/index.html'):
        with open('templates/index.html', 'w') as f:
            f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel & Stock Info</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .card {
            margin-bottom: 20px;
        }
        .results {
            margin-top: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            background-color: #f8f9fa;
            min-height: 100px;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">Travel & Stock Information</h1>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-primary text-white">
                        <h4>Travel Information</h4>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="cityInput" class="form-label">City Name:</label>
                            <input type="text" class="form-control" id="cityInput" placeholder="Enter city name">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Information Type:</label>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="infoType" id="airbnbRadio" value="airbnb" checked>
                                <label class="form-check-label" for="airbnbRadio">
                                    Airbnb Listings
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="infoType" id="weatherRadio" value="weather">
                                <label class="form-check-label" for="weatherRadio">
                                    Weather
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="infoType" id="timeRadio" value="time">
                                <label class="form-check-label" for="timeRadio">
                                    Current Time
                                </label>
                            </div>
                        </div>
                        <button id="getTravelInfo" class="btn btn-primary">Get Travel Information</button>
                        <div id="travelResults" class="results"></div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h4>Stock Information</h4>
                    </div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="stockSymbol" class="form-label">Stock Symbol:</label>
                            <input type="text" class="form-control" id="stockSymbol" placeholder="Enter stock symbol (e.g., AAPL, GOOG)">
                        </div>
                        <button id="getStockInfo" class="btn btn-success">Get Stock Price</button>
                        <div id="stockResults" class="results"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('getTravelInfo').addEventListener('click', async () => {
            const city = document.getElementById('cityInput').value;
            if (!city) {
                alert('Please enter a city name');
                return;
            }
            
            const infoType = document.querySelector('input[name="infoType"]:checked').value;
            const resultsDiv = document.getElementById('travelResults');
            resultsDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><p>Loading...</p></div>';
            
            try {
                const response = await fetch(`/api/${infoType}?city=${encodeURIComponent(city)}`);
                const data = await response.json();
                
                if (data.status === 'error') {
                    resultsDiv.innerHTML = `<div class="alert alert-danger">${data.error_message}</div>`;
                    return;
                }
                
                if (infoType === 'airbnb') {
                    let html = '<h5>Airbnb Listings in ' + city + '</h5><div class="list-group">';
                    data.listings.forEach(listing => {
                        html += `
                            <div class="list-group-item">
                                <h6>${listing.title}</h6>
                                <p><strong>Price:</strong> ${listing.price_per_night}</p>
                                <p><strong>Location:</strong> ${listing.location_highlights}</p>
                            </div>
                        `;
                    });
                    html += '</div>';
                    resultsDiv.innerHTML = html;
                } else {
                    resultsDiv.innerHTML = `<div class="alert alert-info">${data.report}</div>`;
                }
            } catch (error) {
                resultsDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
            }
        });
        
        document.getElementById('getStockInfo').addEventListener('click', async () => {
            const symbol = document.getElementById('stockSymbol').value;
            if (!symbol) {
                alert('Please enter a stock symbol');
                return;
            }
            
            const resultsDiv = document.getElementById('stockResults');
            resultsDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><p>Loading...</p></div>';
            
            try {
                const response = await fetch(`/api/stock?symbol=${encodeURIComponent(symbol)}`);
                const data = await response.json();
                
                if (data.status === 'error') {
                    resultsDiv.innerHTML = `<div class="alert alert-danger">${data.error_message}</div>`;
                    return;
                }
                
                resultsDiv.innerHTML = `
                    <div class="alert alert-success">
                        <h5>${data.symbol}</h5>
                        <p>Current Price: $${data.price.toFixed(2)}</p>
                    </div>
                `;
            } catch (error) {
                resultsDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
            }
        });
    </script>
</body>
</html>
            ''')

# Alternative Methods
# Using the Flask Blueprint Method
# 
# For larger applications, you might consider using Blueprints and implementing the record_once functionality:
# 
# from flask import Flask, Blueprint
# 
# app = Flask(__name__)
# bp = Blueprint('main', __name__)
# 
# @bp.record_once
# def create_templates(state):
#     # Your template creation code here
#     pass
# 
# app.register_blueprint(bp)

if __name__ == '__main__':
    create_templates()  # Call it before app.run
    app.run(debug=True)