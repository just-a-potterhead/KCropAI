# KCropAI: Integrated Agricultural Intelligence System

**DEVELOPER :** Ardra Suresh  
**COURSE :** CSA2001 Fundamentals of AI and ML   
**ACADEMIC INSTITUTION :** VIT Bhopal  

KCropAI is a localized, data-driven machine learning pipeline and logical expert system designed to recommend optimal crops based on specific soil metrics and weather conditions. While applicable globally, this project is uniquely contextualized for the agricultural landscape of Kerala (featuring high rainfall and laterite soils).

## Project Overview
KCropAI is an intelligent decision-support system designed to optimize agricultural practices in Kerala. The application integrates multiple Artificial Intelligence paradigms, including Supervised Machine Learning (Classification and Regression) and Deterministic Logic Programming (Expert Systems). By combining these approaches, the system provides both data-driven predictions and rule-based validation to ensure agricultural recommendations are biologically sound and statistically accurate.

The project is architected using a modular Flask web framework, separating the analytical backend from the user interface to ensure scalability and maintainability.

---

## Directory Structure and File Descriptions

### Root Directory
* **app.py**: The primary entry point for the Flask web application. It handles routing, manages session state for form retention, and coordinates data flow between the UI and the source modules.
* **requirements.txt**: A configuration file listing all necessary Python libraries (Flask, Scikit-Learn, Pandas, etc.) required to execute the project.
* **README.md**: Technical documentation providing an overview, installation guide, and architectural details.
* **.gitignore**: Specifies intentionally untracked files that Git should ignore, such as virtual environments, cache files, and sensitive directories.

### data/
* **crop_recommendation.csv**: The primary dataset used for training the Classification model, containing soil nutrients and weather parameters.
* **crop_yield_kerala.csv**: A specialized dataset containing historical yield data specific to Kerala, used for training the Regression model.

### notebooks/
These files contain the experimental phase of the project:
* **01_EDA.ipynb**: Exploratory Data Analysis to understand feature correlations and data distribution.
* **02_Prolog_Demo.ipynb**: Initial testing of logical rules and unification.
* **03_ML_Classification.ipynb**: The training, testing, and evaluation pipeline for the Random Forest Classifier.
* **04_ML_Regression.ipynb**: The training and compression pipeline for the Yield Prediction regressor.

### prolog/
* **crop_knowledge_base.pl**: A traditional Prolog file containing the raw facts and rules regarding crop-soil compatibility. This serves as the logical foundation for the system.

### src/ (Core Analytical Backend)
* **predict.py**: Manages the loading of serialized models and provides methods for real-time inference.
* **prolog_bridge.py**: Translates traditional Prolog logic into a Python-native inference engine, allowing the Expert System to run without external Prolog dependencies.
* **agent.py**: Implements the Intelligent Agent logic, applying the PEAS framework to act as a utility-based agent for farm management.
* **search.py**: Contains the Breadth-First Search (BFS) algorithm used for irrigation pathfinding and state-space search demonstrations.
* **rf_model.pkl / rf_yield_regressor.pkl**: Serialized Random Forest models representing the trained intelligence of the system.
* **label_encoder.pkl / crop_label_encoder.pkl**: Normalization files used to map categorical strings to numerical data and vice versa.

---

## AI Implementation Details

### 1. Classification (Crop Recommendation)
The system uses a Random Forest Classifier to process Nitrogen (N), Phosphorus (P), Potassium (K), Temperature, Humidity, pH, and Rainfall. The model predicts the most suitable crop for the given environment. A logic-based safeguard is integrated to flag "Agronomic Alerts" when inputs fall into biologically impossible ranges (e.g., extreme pH), even if the ML model provides a mathematical prediction.

### 2. Regression (Yield Forecasting)
The Yield Predictor uses a Random Forest Regressor to estimate production volume in tonnes. It accounts for land area, annual rainfall, and chemical inputs (fertilizers/pesticides). This module demonstrates the system's ability to handle continuous numerical output.

### 3. Expert System (Logic Programming)
This module provides deterministic validation. Unlike ML, which works on probability, the Expert System uses strict unification to match crops to soil types (Laterite, Alluvial, Red, Black) and rainfall levels. It ensures that the system remains grounded in fundamental agricultural facts.

---

## Installation and Execution

### 1. Environment Setup
Clone the repository and create a virtual environment to avoid dependency conflicts:
```sh
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Dependency Installation
Install the required packages using the requirements file:
```sh
pip install -r requirements.txt
```

### 3. Running the Application
Launch the Flask development server:
```sh
python app.py
```
Access the interface by navigating to `http://127.0.0.1:5000` in any modern web browser.

---

## Developer Information
* **NAME :** Ardra Suresh
* **REGISTRATION NUMBER+ :** 25BHI10062
* **BRANCH :** B.Tech. CSE (Health Informatics)
* **COURSE :** CSA2001 Fundamentals of AI and ML
