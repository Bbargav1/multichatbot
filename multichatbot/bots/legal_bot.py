class LegalEaseBot:
    def respond(self, user_input):
        topics = {
            "rent": "Standard rental agreement requires 11-month registration.",
            "divorce": "Mutual consent divorce takes 6-18 months in India."
        }
        user_input = user_input.lower()
        for topic, info in topics.items():
            if topic in user_input:
                return f"⚖️ LegalBot: {info}"
        return "⚖️ LegalBot: Consult a licensed advocate for case-specific advice."