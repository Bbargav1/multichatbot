def get_theme(bot_name):
    """Get the theme CSS file for a specific bot
    
    Args:
        bot_name (str): Name of the bot (e.g., 'medical', 'finance')
        
    Returns:
        str: Filename of the CSS theme
    """
    themes = {
        "medical": "medical_theme.css",
        "agriculture": "agriculture_theme.css",
        "finance": "finance_theme.css",
        "shopping": "shopping_theme.css",
        "education": "education_theme.css",
        "legal": "legal_theme.css",
        "sustainability": "sustainability_theme.css",
        "travel": "travel_theme.css",
        "hr": "hr_theme.css",
        "mentalhealth": "mentalhealth_theme.css"
    }
    return themes.get(bot_name.lower(), "default_theme.css")