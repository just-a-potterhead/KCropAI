# src/predict.py
import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CropPredictor:
    def __init__(self):
        self.clf_model, self.clf_encoder = self._load_model('rf_model.pkl', 'label_encoder.pkl')
        self.reg_model, self.reg_encoder = self._load_model('rf_yield_regressor.pkl', 'crop_label_encoder.pkl')

    def _load_model(self, model_name, encoder_name):
        try:
            m_path = os.path.join(BASE_DIR, model_name)
            e_path = os.path.join(BASE_DIR, encoder_name)
            return joblib.load(m_path), joblib.load(e_path)
        except Exception as e:
            print(f"Warning: Could not load {model_name}. Ensure notebooks have been run.")
            return None, None

    def recommend_crop(self, N, P, K, temp, humidity, ph, rainfall):
        """Classification: Predicts the best crop."""
        if not self.clf_model or not self.clf_encoder:
            return "Error: Model not loaded"
        
        input_data = np.array([[N, P, K, temp, humidity, ph, rainfall]])
        pred_encoded = self.clf_model.predict(input_data)[0]
        return self.clf_encoder.inverse_transform([pred_encoded])[0].replace('_', ' ').title()

    def predict_yield(self, crop_name, area, rainfall, fertilizer, pesticide):
        """Regression: Predicts the expected yield."""
        if not self.reg_model or not self.reg_encoder:
            return 0.0
            
        try:
            crop_encoded = self.reg_encoder.transform([crop_name.lower().replace(' ', '_')])[0]
            input_data = np.array([[area, rainfall, fertilizer, pesticide, crop_encoded]])
            return self.reg_model.predict(input_data)[0]
        except ValueError:
            return 0.0 # Crop not in training data
