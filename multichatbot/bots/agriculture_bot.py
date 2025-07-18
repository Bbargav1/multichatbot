class AgriGuruBot:
    def respond(self, user_input):
        crops = {
            "rice": "Requires 150-300cm rainfall. Ideal pH: 5-6.5",
            "wheat": "Grows best in 75-100cm rain. Temperature: 15-20°C"
        }
        user_input = user_input.lower()
        for crop, info in crops.items():
            if crop in user_input:
                return f"🌱 AgriGuru: {info}"
        return "🌱 AgriGuru: Contact your local Krishi Vigyan Kendra for detailed advice."