# src/prolog_bridge.py

class KCropExpertSystem:
    """
    A deterministic rule-based inference engine that mimics Prolog's 
    unification and fact-checking capabilities natively in Python.
    """
    def __init__(self):
        # FACTS (Knowledge Base)
        self.soil_facts = {
            "coconut": "laterite", "rubber": "laterite", "black_pepper": "laterite",
            "rice": "alluvial", "banana": "alluvial", "tapioca": "red", "coffee": "laterite"
        }
        self.rain_facts = {
            "coconut": "high", "rubber": "high", "black_pepper": "high",
            "rice": "high", "banana": "moderate", "tapioca": "moderate", "coffee": "moderate"
        }

    def query(self, user_soil, user_rain):
        """
        RULES: Equivalent to recommend_crop(Crop, Soil, Rain) :- 
               soil_type(Crop, Soil), rainfall_req(Crop, Rain).
        """
        results = []
        for crop in self.soil_facts:
            match_soil = self.soil_facts[crop] == user_soil
            match_rain = self.rain_facts.get(crop) == user_rain
            
            if match_soil and match_rain:
                results.append(crop)
        return results
