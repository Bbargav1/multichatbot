import logging
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from utils.theme_switcher import get_theme

load_dotenv()

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # Keep chat payloads bounded.

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_API_URL = os.getenv(
    "OPENROUTER_API_URL",
    "https://openrouter.ai/api/v1/chat/completions",
).strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo").strip()
REQUEST_TIMEOUT_SECONDS = float(os.getenv("AI_REQUEST_TIMEOUT", "30"))

bots = {
    "medical": {
        "template": "chat_medical.html",
        "system_prompt": "You are a medical information assistant. Give general information, avoid definitive diagnoses, and recommend a qualified clinician for personal medical concerns. For emergencies, advise contacting local emergency services.",
        "theme": get_theme("medical"),
    },
    "finance": {
        "template": "chat_finance.html",
        "system_prompt": "You provide general financial education, budgeting guidance, and risk-aware explanations. Do not promise returns or present information as individualized professional financial advice.",
        "theme": get_theme("finance"),
    },
    "agriculture": {
        "template": "chat_agriculture.html",
        "system_prompt": "You are an agricultural assistant. Give practical farming, crop-care, pest-management, and sustainability information. Ask for location and crop details when needed.",
        "theme": get_theme("agriculture"),
    },
    "shopping": {
        "template": "chat_shopping.html",
        "system_prompt": "You are a shopping assistant. Compare options objectively based on the user's needs, budget, and preferences.",
        "theme": get_theme("shopping"),
    },
    "education": {
        "template": "chat_education.html",
        "system_prompt": "You are an educational assistant. Explain concepts clearly, adapt to the learner's level, and encourage understanding.",
        "theme": get_theme("education"),
    },
    "legal": {
        "template": "chat_legal.html",
        "system_prompt": "You provide general legal information, not legal advice. Explain that laws vary by jurisdiction and recommend a qualified lawyer for specific cases.",
        "theme": get_theme("legal"),
    },
    "sustainability": {
        "template": "chat_sustainability.html",
        "system_prompt": "You are a sustainability assistant. Offer practical advice about waste reduction, energy, conservation, and sustainable living.",
        "theme": get_theme("sustainability"),
    },
    "travel": {
        "template": "chat_travel.html",
        "system_prompt": "You are a travel assistant. Help with destination ideas, itineraries, culture, logistics, and budgets. Flag details that should be verified before travel.",
        "theme": get_theme("travel"),
    },
    "hr": {
        "template": "chat_hr.html",
        "system_prompt": "You are an HR and career assistant. Help with workplace communication, resumes, interviews, and professional development.",
        "theme": get_theme("hr"),
    },
    "mentalhealth": {
        "template": "chat_mentalhealth.html",
        "system_prompt": "You provide empathetic general emotional-wellness support, not diagnosis or therapy. Encourage professional help for serious concerns. If a user may be in immediate danger, encourage contacting local emergency services or a trusted person now.",
        "theme": get_theme("mentalhealth"),
    },
}


@app.route("/")
def index():
    """Show the available domain assistants."""
    return render_template("index.html", bots=list(bots.keys()))


@app.route("/medical")
def medical_chat():
    return render_bot_interface("medical")


@app.route("/agriculture")
def agriculture_chat():
    return render_bot_interface("agriculture")


@app.route("/finance")
def finance_chat():
    return render_bot_interface("finance")


@app.route("/shopping")
def shopping_chat():
    return render_bot_interface("shopping")


@app.route("/education")
def education_chat():
    return render_bot_interface("education")


@app.route("/legal")
def legal_chat():
    return render_bot_interface("legal")


@app.route("/sustainability")
def sustainability_chat():
    return render_bot_interface("sustainability")


@app.route("/travel")
def travel_chat():
    return render_bot_interface("travel")


@app.route("/hr")
def hr_chat():
    return render_bot_interface("hr")


@app.route("/mentalhealth")
def mentalhealth_chat():
    return render_bot_interface("mentalhealth")


def render_bot_interface(bot_name):
    """Render the selected assistant's chat page."""
    bot_data = bots.get(bot_name)
    if bot_data is None:
        return render_template("error.html", message="Bot not found"), 404

    return render_template(
        bot_data["template"],
        bot_name=bot_name,
        theme=bot_data["theme"],
        bot_title=f"{bot_name.capitalize()} Assistant",
    )


def _normalise_history(history, current_message):
    """Accept only safe, well-formed chat history and avoid duplicate last turns."""
    if not isinstance(history, list):
        return []

    cleaned = []
    for item in history[-20:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        # Never allow a client to inject system/developer instructions.
        if role not in ("user", "assistant") or not isinstance(content, str):
            continue
        content = content.strip()
        if content:
            cleaned.append({"role": role, "content": content[:8000]})

    # Several existing chat pages include the current user turn in history.
    # The endpoint appends it below, so remove it here if it is already present.
    if cleaned and cleaned[-1]["role"] == "user" and cleaned[-1]["content"] == current_message:
        cleaned.pop()
    return cleaned


@app.route("/api/chat", methods=["POST"])
def chat_api():
    """Send a validated chat request to OpenRouter."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    bot_name = data.get("bot")
    user_message = data.get("message")
    if not isinstance(bot_name, str) or bot_name not in bots:
        return jsonify({"error": "Unknown assistant."}), 400
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "Please enter a message."}), 400

    user_message = user_message.strip()
    if len(user_message) > 8000:
        return jsonify({"error": "Message is too long (maximum 8000 characters)."}), 400

    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY is not configured.")
        return jsonify({
            "error": "AI service is not configured. Add OPENROUTER_API_KEY to your environment."
        }), 503

    messages = [{"role": "system", "content": bots[bot_name]["system_prompt"]}]
    messages.extend(_normalise_history(data.get("history", []), user_message))
    messages.append({"role": "user", "content": user_message})

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv("APP_URL", "http://localhost:5000"),
                "X-Title": os.getenv("APP_NAME", "MultiChatbot"),
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": messages,
                "temperature": 0.7,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
        ai_response = payload["choices"][0]["message"]["content"]
        if not isinstance(ai_response, str) or not ai_response.strip():
            raise ValueError("The AI provider returned an empty response.")

        return jsonify({
            "response": ai_response.strip(),
            "bot_name": bot_name,
            "theme": bots[bot_name]["theme"],
        })
    except requests.Timeout:
        logger.warning("OpenRouter request timed out.")
        return jsonify({"error": "The AI service took too long to respond. Please try again."}), 504
    except requests.RequestException as exc:
        status_code = getattr(getattr(exc, "response", None), "status_code", None)
        logger.error("OpenRouter request failed (status=%s): %s", status_code, exc)
        return jsonify({"error": "The AI service is temporarily unavailable. Please try again later."}), 502
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        logger.error("Unexpected OpenRouter response: %s", exc)
        return jsonify({"error": "The AI service returned an invalid response. Please try again."}), 502


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
