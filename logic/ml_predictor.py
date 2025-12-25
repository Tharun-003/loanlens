import joblib
import pandas as pd

from utils.encoders import encode_user_profile


class MLPredictor:
    """
    Wrapper around the trained ML eligibility model.
    Used ONLY to refine borderline eligibility cases.
    """

    def __init__(self, model_path: str = "model/eligibility_model.pkl"):
        try:
            self.model = joblib.load(model_path)
            self.model_loaded = True
        except Exception:
            self.model = None
            self.model_loaded = False

    def is_available(self) -> bool:
        """Check if ML model is available"""
        return self.model_loaded

    def predict_probability(self, user_profile: dict) -> float:
        """
        Returns probability of eligibility (0.0 – 1.0)
        """
        if not self.model_loaded:
            return 0.0

        encoded = encode_user_profile(user_profile)
        df = pd.DataFrame([encoded])

        # Predict probability for class 'Eligible' (1)
        prob = self.model.predict_proba(df)[0][1]
        return float(prob)

    def final_decision(
        self,
        rule_decision: str,
        user_profile: dict,
        threshold: float = 0.6
    ) -> str:
        """
        Combine rule-based decision with ML probability.
        """

        # Rules always win
        if rule_decision in ["Eligible", "Not Eligible"]:
            return rule_decision

        # Borderline → ML decides
        prob = self.predict_probability(user_profile)

        if prob >= threshold:
            return "Eligible"
        else:
            return "Not Eligible"
