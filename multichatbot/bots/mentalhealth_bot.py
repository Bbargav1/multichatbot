class MentalHealthBot:
    def respond(self, user_input):
        feelings = {
            "anxious": "Try 4-7-8 breathing: Inhale 4s, Hold 7s, Exhale 8s",
            "depressed": "Contact Vandrevala Foundation: +91 9999 666 555"
        }
        user_input = user_input.lower()
        for feeling, advice in feelings.items():
            if feeling in user_input:
                return f"🧠 MindBot: {advice}"
        return "🧠 MindBot: You're not alone. NIMHANS helpline: 080-4611 0007"