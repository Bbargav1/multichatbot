class TravelGuardBot:
    def respond(self, user_input):
        destinations = {
            "goa": "Best Nov-Feb. Required: ID proof for beaches",
            "kerala": "Monsoon (Jun-Sep) offers lowest hotel rates."
        }
        user_input = user_input.lower()
        for place, tips in destinations.items():
            if place in user_input:
                return f"✈️ TravelBot: {tips}"
        return "✈️ TravelBot: Check visa requirements at indianvisaonline.gov.in"