from flask import Flask, render_template, request, jsonify
import requests
from utils.theme_switcher import get_theme

app = Flask(__name__)

# OpenRouter API configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Bot configurations with specialized prompts and templates
bots = {
    'medical': {
        'template': 'chat_medical.html',
        'system_prompt': """You are a medical assistant bot. Provide accurate medical information, symptom analysis, 
        and general health advice. For serious conditions, always recommend consulting a doctor. Be compassionate 
        and clear in your explanations.""",
        'theme': get_theme('medical')
    },
    'finance': {
        'template': 'chat_finance.html',
        'system_prompt': """You are a financial advisor bot. Provide investment advice, budgeting tips, tax information, 
        and financial planning guidance. Always clarify that this is not professional financial advice and recommend 
        consulting a certified financial advisor for major decisions.""",
        'theme': get_theme('finance')
    },
    'agriculture': {
        'template': 'chat_agriculture.html',
        'system_prompt': """You are an agricultural expert bot. Provide farming techniques, crop advice, pest management, 
        and sustainable farming practices. Tailor your advice to different climates and scales of farming operations.""",
        'theme': get_theme('agriculture')
    },
    'shopping': {
        'template': 'chat_shopping.html',
        'system_prompt': """You are a shopping assistant bot. Help users find products, compare options, and make 
        purchasing decisions. Provide objective recommendations based on user needs and preferences.""",
        'theme': get_theme('shopping')
    },
    'education': {
        'template': 'chat_education.html',
        'system_prompt': """You are an educational assistant bot. Help with learning strategies, subject explanations, 
        study techniques, and academic advice. Adapt to different learning styles and education levels.""",
        'theme': get_theme('education')
    },
    'legal': {
        'template': 'chat_legal.html',
        'system_prompt': """You are a legal information bot. Provide general legal information and explain concepts, 
        but always clarify this is not legal advice and recommend consulting an attorney for specific cases.""",
        'theme': get_theme('legal')
    },
    'sustainability': {
        'template': 'chat_sustainability.html',
        'system_prompt': """You are a sustainability expert bot. Provide advice on eco-friendly practices, renewable energy, 
        waste reduction, and sustainable living. Offer practical solutions for individuals and businesses.""",
        'theme': get_theme('sustainability')
    },
    'travel': {
        'template': 'chat_travel.html',
        'system_prompt': """You are a travel assistant bot. Provide destination recommendations, travel tips, 
        itinerary planning, and cultural information. Consider different travel styles and budgets.""",
        'theme': get_theme('travel')
    },
    'hr': {
        'template': 'chat_hr.html',
        'system_prompt': """You are an HR assistant bot. Provide guidance on workplace issues, career development, 
        resume tips, and interview preparation. Focus on best practices and professional development.""",
        'theme': get_theme('hr')
    },
    'mentalhealth': {
        'template': 'chat_mentalhealth.html',
        'system_prompt': """You are a mental health support bot. Offer general wellness advice and coping strategies, 
        but always recommend consulting a mental health professional for serious concerns. Be empathetic and supportive.""",
        'theme': get_theme('mentalhealth')
    }
}

@app.route('/')
def index():
    """Homepage showing all available bots"""
    return render_template('index.html', bots=list(bots.keys()))

# Individual chat routes
@app.route('/medical')
def medical_chat():
    return render_bot_interface('medical')

@app.route('/agriculture')
def agriculture_chat():
    return render_bot_interface('agriculture')

@app.route('/finance')
def finance_chat():
    return render_bot_interface('finance')

@app.route('/shopping')
def shopping_chat():
    return render_bot_interface('shopping')

@app.route('/education')
def education_chat():
    return render_bot_interface('education')

@app.route('/legal')
def legal_chat():
    return render_bot_interface('legal')

@app.route('/sustainability')
def sustainability_chat():
    return render_bot_interface('sustainability')

@app.route('/travel')
def travel_chat():
    return render_bot_interface('travel')

@app.route('/hr')
def hr_chat():
    return render_bot_interface('hr')

@app.route('/mentalhealth')
def mentalhealth_chat():
    return render_bot_interface('mentalhealth')

def render_bot_interface(bot_name):
    """Render the appropriate chat template for the bot"""
    if bot_name not in bots:
        return render_template('error.html', message="Bot not found"), 404
    
    bot_data = bots[bot_name]
    return render_template(
        bot_data['template'],
        bot_name=bot_name,
        theme=bot_data['theme'],
        bot_title=bot_name.capitalize() + " Assistant"
    )

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Handle chat requests through OpenRouter API"""
    data = request.get_json()
    bot_name = data.get('bot')
    user_message = data.get('message')
    conversation_history = data.get('history', [])
    
    if not bot_name or not user_message:
        return jsonify({"error": "Missing parameters"}), 400
    
    if bot_name not in bots:
        return jsonify({"error": "Bot not found"}), 404
    
    # Prepare messages for OpenRouter
    messages = [
        {"role": "system", "content": bots[bot_name]['system_prompt']}
    ]
    
    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        # Call OpenRouter API
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",  # You can change this to other supported models
                "messages": messages,
                "temperature": 0.7
            }
        )
        
        if response.status_code != 200:
            return jsonify({
                "error": "Failed to get response from AI",
                "details": response.text
            }), 500
            
        ai_response = response.json()['choices'][0]['message']['content']
        
        return jsonify({
            "response": ai_response,
            "bot_name": bot_name,
            "theme": bots[bot_name]['theme']
        })
        
    except Exception as e:
        return jsonify({
            "error": "An error occurred",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)