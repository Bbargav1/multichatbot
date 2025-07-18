class GreenTechBot:
    def respond(self, user_input):
        actions = {
            "recycle": "Segregate into wet/dry waste. Contact local municipality.",
            "solar": "5kW system costs ₹2.5L with 25% subsidy in many states."
        }
        user_input = user_input.lower()
        for action, info in actions.items():
            if action in user_input:
                return f"🌿 GreenBot: {info}"
        return "🌿 GreenBot: Calculate your carbon footprint at cag.org.in"