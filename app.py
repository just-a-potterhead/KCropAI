from flask import Flask, request, render_template_string
from src.predict import CropPredictor

# Initialize the Flask application
app = Flask(__name__)

# Initialize our ML backend (This handles joblib automatically!)
predictor = CropPredictor()

# --- MINIMAL HTML FRONTEND ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>KCropAI | Flask</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #1e1e1e; color: #ffffff; padding: 40px; }
        .container { max-width: 500px; margin: auto; background: #2d2d2d; padding: 30px; border-radius: 10px; }
        input[type="number"] { width: 100%; padding: 8px; margin: 10px 0; border-radius: 5px; border: none; }
        input[type="submit"] { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
        input[type="submit"]:hover { background-color: #45a049; }
        .result { background-color: #4CAF50; padding: 15px; margin-top: 20px; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🥥 KCropAI Recommender</h2>
        <p>Enter parameters to get a Machine Learning prediction:</p>
        
        <form action="/predict" method="POST">
            <label>Nitrogen (N):</label>
            <input type="number" name="N" value="50" required>
            
            <label>Phosphorus (P):</label>
            <input type="number" name="P" value="40" required>
            
            <label>Potassium (K):</label>
            <input type="number" name="K" value="60" required>
            
            <label>Temperature (°C):</label>
            <input type="number" step="0.1" name="temp" value="32.5" required>
            
            <label>Humidity (%):</label>
            <input type="number" step="0.1" name="humidity" value="75.0" required>
            
            <label>Soil pH:</label>
            <input type="number" step="0.1" name="ph" value="5.8" required>
            
            <label>Rainfall (mm):</label>
            <input type="number" step="0.1" name="rainfall" value="210.0" required>
            
            <input type="submit" value="🔮 Predict Optimal Crop">
        </form>

        {% if result %}
            <div class="result">
                <h3>🌱 Recommended Crop: <br><b>{{ result }}</b></h3>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

# --- FLASK ROUTES ---

@app.route('/', methods=['GET'])
def home():
    """Renders the default home page with the form."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    """Handles the form submission and runs the ML model."""
    try:
        # 1. Grab the data from the HTML form
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temp = float(request.form['temp'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # 2. Pass it to your modular backend
        recommended_crop = predictor.recommend_crop(N, P, K, temp, humidity, ph, rainfall)

        # 3. Return the page with the result highlighted
        return render_template_string(HTML_TEMPLATE, result=recommended_crop)

    except Exception as e:
        return render_template_string(HTML_TEMPLATE, result=f"Error: {str(e)}")

if __name__ == '__main__':
    # Runs the server on http://127.0.0.1:5000
    app.run(debug=True)
