# src/predict.py
import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CropPredictor:
    def __init__(self):
        self.clf_error = ""
        self.reg_error = ""
        self.clf_model, self.clf_encoder = self._load_model('rf_model.pkl', 'label_encoder.pkl', 'clf')
        self.reg_model, self.reg_encoder = self._load_model('rf_yield_regressor.pkl', 'crop_label_encoder.pkl', 'reg')

    def _load_model(self, model_name, encoder_name, model_type):
        try:
            m_path = os.path.join(BASE_DIR, model_name)
            e_path = os.path.join(BASE_DIR, encoder_name)
            
            # Check if files physically exist first
            if not os.path.exists(m_path):
                raise FileNotFoundError(f"Missing {m_path}")
            if not os.path.exists(e_path):
                raise FileNotFoundError(f"Missing {e_path}")
                
            return joblib.load(m_path), joblib.load(e_path)
        except Exception as e:
            # Capture the exact error
            if model_type == 'clf':
                self.clf_error = str(e)
            else:
                self.reg_error = str(e)
            return None, None

    def recommend_crop(self, N, P, K, temp, humidity, ph, rainfall):
        """Classification: Predicts the best crop."""
        if not self.clf_model or not self.clf_encoder:
            return f"Error loading Classification Models: {self.clf_error}"
        
        try:
            input_data = np.array([[N, P, K, temp, humidity, ph, rainfall]])
            pred_encoded = self.clf_model.predict(input_data)[0]
            return self.clf_encoder.inverse_transform([pred_encoded])[0].replace('_', ' ').title()
        except Exception as e:
            return f"Prediction Error: {str(e)}"

    def get_yield_crops(self):
        """Returns the exact crop names the regression model was trained on."""
        if self.reg_encoder:
            # This pulls the exact strings from the encoder's memory!
            return self.reg_encoder.classes_.tolist()
        return ["Error loading crops"]

    def predict_yield(self, crop_name, area, rainfall, fertilizer, pesticide):
        """Regression: Predicts the expected yield."""
        if not self.reg_model or not self.reg_encoder:
            return "Error: Model files not found."

        try:
            # We don't need to format the text anymore, because we are passing
            # the exact string from the encoder's own list.
            crop_encoded = self.reg_encoder.transform([crop_name])[0]

            input_data = np.array([[area, rainfall, fertilizer, pesticide, crop_encoded]])
            return float(self.reg_model.predict(input_data)[0])
        except Exception as e:
            return f"Math/Format Error: {str(e)}"
