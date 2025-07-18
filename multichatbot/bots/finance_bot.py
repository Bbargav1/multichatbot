class FinanceAnalystBot:
    def respond(self, user_input):
        keywords = {
            "investment": "Diversify across stocks (60%), bonds (30%), gold (10%)",
            "loan": "Compare rates: SBI (8.5%), HDFC (9.2%), ICICI (9%)"
        }
        user_input = user_input.lower()
        for term, advice in keywords.items():
            if term in user_input:
                return f"💰 FinanceBot: {advice}"
        return "💰 FinanceBot: Always check CIBIL score before applying for loans."