class MediCareBot:
    def respond(self, user_input):
        symptoms = {
            "fever": "Take paracetamol 500mg every 6 hours and rest.",
            "cough": "Try honey-lemon tea. Consult doctor if persistent.",
            "headache": "Hydrate and take rest in a dark room."
        }
        user_input = user_input.lower()
        for symptom, advice in symptoms.items():
            if symptom in user_input:
                return f"🔬 MediCare Bot: {advice}"
        return "🔬 MediCare Bot: If symptoms persist, please consult a doctor immediately."