class HRHelperBot:
    def respond(self, user_input):
        queries = {
            "resume": "Keep it 1-page with quantifiable achievements.",
            "interview": "STAR method: Situation, Task, Action, Result"
        }
        user_input = user_input.lower()
        for query, tip in queries.items():
            if query in user_input:
                return f"💼 HRBot: {tip}"
        return "💼 HRBot: EPF withdrawal forms available at epfindia.gov.in"