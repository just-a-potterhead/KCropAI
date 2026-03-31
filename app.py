from flask import Flask, request, render_template_string

import os



# --- IMPORT MODULAR BACKEND ---

from src.predict import CropPredictor

from src.prolog_bridge import KCropExpertSystem



# Initialize Flask

app = Flask(__name__)



# Initialize ML Backend

predictor = CropPredictor()

expert_system = KCropExpertSystem()



# --- UNIFIED HTML TEMPLATE (Bootstrap 5) ---

HTML_TEMPLATE = """

<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>KCropAI | Flask Architecture</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>

        body { background-color: #121212; color: #ffffff; padding-bottom: 50px; }

        .card { background-color: #1e1e1e; border: 1px solid #333; }

        .form-control, .form-select { background-color: #2d2d2d; color: #fff; border: 1px solid #444; }

        .form-control:focus, .form-select:focus { background-color: #3d3d3d; color: #fff; border-color: #198754; box-shadow: none; }

        .nav-tabs .nav-link { color: #aaa; cursor: pointer; border: none; }

        .nav-tabs .nav-link.active { background-color: #1e1e1e; color: #198754; border-bottom: 3px solid #198754; font-weight: bold; }

        .nav-tabs { border-bottom: 1px solid #333; }

        .result-box { background-color: #198754; color: white; padding: 15px; border-radius: 5px; margin-top: 20px; }

        .error-box { background-color: #6c4a4a; color: white; padding: 15px; border-radius: 5px; margin-top: 20px; border-left: 5px solid #dc3545; }

        .badge-caption { background-color: #198754; color: white; font-size: 0.7em; vertical-align: middle; margin-left: 10px; padding: 5px 10px; border-radius: 4px; }

    </style>

</head>

<body>

<div class="container py-5">

    <h1 class="mb-2">KCropAI System <span class="badge-caption">Intelligence Meets Soil</span></h1>

    <p class="text-secondary mb-4">Developed by Ardra Suresh | CSA2001 Fundamentals in AI & ML</p>



    <ul class="nav nav-tabs mb-4">

      <li class="nav-item"><a class="nav-link {% if active_tab == 'tab1' %}active{% endif %}" href="/">1. Crop Recommender</a></li>

      <li class="nav-item"><a class="nav-link {% if active_tab == 'tab2' %}active{% endif %}" href="/tab/yield">2. Yield Predictor</a></li>

      <li class="nav-item"><a class="nav-link {% if active_tab == 'tab3' %}active{% endif %}" href="/tab/logic">3. Expert System</a></li>

    </ul>



    <div class="tab-content card p-4">

      

      {% if active_tab == 'tab1' %}

        <h3>Crop Recommendation Engine</h3>

        <p class="text-secondary">Utilizes a Random Forest Classifier to determine optimal crop types.</p>

        <form action="/predict_crop" method="POST">

            <div class="row mb-3">

                <div class="col-md-4"><label>Nitrogen (N):</label><input type="number" class="form-control" name="N" value="{{ form_data.get('N', '50') }}" required></div>

                <div class="col-md-4"><label>Phosphorus (P):</label><input type="number" class="form-control" name="P" value="{{ form_data.get('P', '40') }}" required></div>

                <div class="col-md-4"><label>Potassium (K):</label><input type="number" class="form-control" name="K" value="{{ form_data.get('K', '60') }}" required></div>

            </div>

            <div class="row mb-3">

                <div class="col-md-4"><label>Temperature (°C):</label><input type="number" step="0.01" class="form-control" name="temp" value="{{ form_data.get('temp', '32.50') }}" required></div>

                <div class="col-md-4"><label>Humidity (%):</label><input type="number" step="0.01" class="form-control" name="humidity" value="{{ form_data.get('humidity', '75.00') }}" required></div>

                <div class="col-md-4"><label>Rainfall (mm):</label><input type="number" step="0.01" class="form-control" name="rainfall" value="{{ form_data.get('rainfall', '210.00') }}" required></div>

            </div>

            <div class="row mb-4">

                <div class="col-md-4"><label>Soil pH:</label><input type="number" step="0.01" class="form-control" name="ph" value="{{ form_data.get('ph', '5.80') }}" required></div>

            </div>

            <button type="submit" class="btn btn-success w-100 py-2">Predict Optimal Crop</button>

        </form>

      {% endif %}



      {% if active_tab == 'tab2' %}

        <h3>Crop Yield Predictor</h3>

        <p class="text-secondary">Utilizes a Random Forest Regressor to forecast production volume.</p>

        <form action="/predict_yield" method="POST">

            <div class="row mb-3">

                <div class="col-md-12">

                    <label>Select Crop:</label>

                    <select class="form-select" name="crop_choice">

                        {% for crop in crops %}

                        <option value="{{ crop }}" {% if form_data.get('crop_choice') == crop %}selected{% endif %}>{{ crop.title() }}</option>

                        {% endfor %}

                    </select>

                </div>

            </div>

            <div class="row mb-3">

                <div class="col-md-6"><label>Land Area (Hectares):</label><input type="number" step="0.01" class="form-control" name="area" value="{{ form_data.get('area', '5.00') }}" required></div>

                <div class="col-md-6"><label>Annual Rainfall (mm):</label><input type="number" step="0.01" class="form-control" name="rain" value="{{ form_data.get('rain', '2000.00') }}" required></div>

            </div>

            <div class="row mb-4">

                <div class="col-md-6"><label>Fertilizer Used (kg):</label><input type="number" step="0.01" class="form-control" name="fert" value="{{ form_data.get('fert', '150.00') }}" required></div>

                <div class="col-md-6"><label>Pesticide Used (kg):</label><input type="number" step="0.01" class="form-control" name="pest" value="{{ form_data.get('pest', '5.00') }}" required></div>

            </div>

            <button type="submit" class="btn btn-success w-100 py-2">Predict Yield</button>

        </form>

      {% endif %}



      {% if active_tab == 'tab3' %}

        <h3>Deterministic Logic Engine</h3>

        <p class="text-secondary">Uses strict Unification Logic to validate agronomic conditions.</p>

        <form action="/predict_logic" method="POST">

            <div class="row mb-4">

                <div class="col-md-6">

                    <label>Select Soil Type:</label>

                    <select class="form-select" name="soil_type">

                        <option value="laterite" {% if form_data.get('soil_type') == 'laterite' %}selected{% endif %}>Laterite</option>

                        <option value="alluvial" {% if form_data.get('soil_type') == 'alluvial' %}selected{% endif %}>Alluvial</option>

                        <option value="red" {% if form_data.get('soil_type') == 'red' %}selected{% endif %}>Red</option>

                        <option value="black" {% if form_data.get('soil_type') == 'black' %}selected{% endif %}>Black</option>

                    </select>

                </div>

                <div class="col-md-6">

                    <label>Select Rainfall Level:</label>

                    <select class="form-select" name="rain_level">

                        <option value="high" {% if form_data.get('rain_level') == 'high' %}selected{% endif %}>High</option>

                        <option value="moderate" {% if form_data.get('rain_level') == 'moderate' %}selected{% endif %}>Moderate</option>

                        <option value="low" {% if form_data.get('rain_level') == 'low' %}selected{% endif %}>Low</option>

                    </select>

                </div>

            </div>

            <button type="submit" class="btn btn-success w-100 py-2">Query Knowledge Base</button>

        </form>

      {% endif %}



      {% if result %}

        <div class="{% if 'Alert' in result or 'Error' in result or 'No match' in result %}error-box{% else %}result-box{% endif %}">

            <h4 class="mb-0">{{ result | safe }}</h4>

        </div>

      {% endif %}



    </div>

</div>

</body>

</html>

"""



# --- FLASK ROUTING LOGIC ---



def get_crops():

    """Helper to safely get crop list for dropdowns from the model metadata."""

    if hasattr(predictor, 'get_yield_crops'):

        return predictor.get_yield_crops()

    return ['coconut', 'rice', 'banana', 'rubber', 'tapioca']



@app.route('/')

def home():

    return render_template_string(HTML_TEMPLATE, active_tab='tab1', result=None, form_data={})



@app.route('/tab/<tab_name>')

def switch_tab(tab_name):

    tab_map = {'yield': 'tab2', 'logic': 'tab3'}

    target_tab = tab_map.get(tab_name, 'tab1')

    return render_template_string(HTML_TEMPLATE, active_tab=target_tab, result=None, crops=get_crops(), form_data={})



@app.route('/predict_crop', methods=['POST'])

def predict_crop():

    # Capture data

    N, P, K = float(request.form['N']), float(request.form['P']), float(request.form['K'])

    temp, humidity = float(request.form['temp']), float(request.form['humidity'])

    ph, rainfall = float(request.form['ph']), float(request.form['rainfall'])



    # Get Prediction

    result = predictor.recommend_crop(N, P, K, temp, humidity, ph, rainfall)

    

    # Logic Guardrails

    if ph > 8.5 or ph < 4.5 or (N == 0 and P == 0 and K == 0):

        final_result = f"Agronomic Alert: Extreme conditions detected!<br>Machine Learning Guess: <b>{result}</b>"

    elif "Error" in result:

        final_result = result

    else:

        final_result = f"Recommended Crop: <b>{result}</b>"



    return render_template_string(HTML_TEMPLATE, active_tab='tab1', result=final_result, form_data=request.form)



@app.route('/predict_yield', methods=['POST'])

def predict_yield():

    crop = request.form['crop_choice']

    area, rain = float(request.form['area']), float(request.form['rain'])

    fert, pest = float(request.form['fert']), float(request.form['pest'])



    result = predictor.predict_yield(crop, area, rain, fert, pest)

    

    if isinstance(result, str):

        final_result = f"Error: {result}"

    else:

        final_result = f"Estimated Yield: <b>{result:.2f} Tonnes / Units</b>"



    return render_template_string(HTML_TEMPLATE, active_tab='tab2', result=final_result, crops=get_crops(), form_data=request.form)



@app.route('/predict_logic', methods=['POST'])

def predict_logic():

    soil, rain = request.form['soil_type'], request.form['rain_level']

    matches = expert_system.query(soil, rain)

    

    if matches:

        final_result = f"Logical Matches Found: <b>{', '.join([m.title() for m in matches])}</b>"

    else:

        final_result = "No matching crops found for these exact logical conditions."



    return render_template_string(HTML_TEMPLATE, active_tab='tab3', result=final_result, form_data=request.form)



if __name__ == '__main__':

    app.run(debug=True, port=5000)
