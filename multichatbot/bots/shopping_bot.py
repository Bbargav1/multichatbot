class ShopAssistBot:
    def __init__(self):
        self.products = {
            "phone": "Top deals: iPhone 15 (₹79,999), Samsung S23 (₹69,999)",
            "laptop": "Best sellers: MacBook Air (₹92,990), HP Pavilion (₹54,990)"
        }

    def respond(self, user_input):
        user_input = user_input.lower()
        for product, deals in self.products.items():
            if product in user_input:
                return f"🛍️ ShopAssist: {deals}"
        return "🛍️ ShopAssist: Try searching for 'phones', 'laptops', or 'headphones'."