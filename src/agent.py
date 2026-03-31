# src/agent.py
from .predict import CropPredictor
from .prolog_bridge import KCropExpertSystem

class AgriculturalAgent:
    """
    A Utility-Based AI Agent for Farm Management.
    Percepts: Soil metrics, weather conditions.
    Actions: Recommends crop, estimates yield, checks logical constraints.
    """
    def __init__(self):
        self.predictor = CropPredictor()
        self.logic_engine = KCropExpertSystem()

    def act(self, environment_state):
        """
        Processes environment percepts and decides on the best action.
        environment_state: dict containing N, P, K, temp, hum, ph, rain, soil_type
        """
        # 1. Use ML to get optimal crop (Probabilistic)
        recommended_crop = self.predictor.recommend_crop(
            environment_state['N'], environment_state['P'], environment_state['K'],
            environment_state['temp'], environment_state['hum'], 
            environment_state['ph'], environment_state['rain']
        )

        # 2. Use Logic Engine to verify environmental safety (Deterministic)
        # Simplify rain logic for the expert system mapping
        rain_level = "high" if environment_state['rain'] > 150 else "moderate"
        safe_crops = self.logic_engine.query(environment_state['soil_type'], rain_level)

        is_logically_safe = recommended_crop.lower().replace(' ', '_') in safe_crops

        return {
            "action": f"Plant {recommended_crop}",
            "ml_confidence": "High",
            "logic_verified": is_logically_safe,
            "logical_alternatives": safe_crops
        }
