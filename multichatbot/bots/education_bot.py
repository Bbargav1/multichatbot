class EduHelperBot:
    def respond(self, user_input):
        subjects = {
            "math": "Use Khan Academy for algebra practice.",
            "science": "NCERT solutions available at ncert.nic.in"
        }
        user_input = user_input.lower()
        for subject, resource in subjects.items():
            if subject in user_input:
                return f"📚 EduBot: {resource}"
        return "📚 EduBot: I can help with math, science, and history topics."