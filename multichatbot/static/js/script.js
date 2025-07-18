// Global variables
let currentBotType = '';
let conversationHistory = [];
const API_BASE_URL = '/api/chat';

// DOM elements
const messageArea = document.getElementById('messageArea');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const chatForm = document.getElementById('chatForm');

// Initialize the chat when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Extract bot type from URL path
    const pathParts = window.location.pathname.split('/');
    currentBotType = pathParts[pathParts.length - 1] || pathParts[pathParts.length - 2];
    
    // Add greeting message
    addBotMessage(getBotGreeting());
    
    // Set focus to input field
    userInput.focus();
    
    // Load any previous conversation from session storage
    loadConversation();
    
    // Set up event listeners
    setupEventListeners();
});

function getBotGreeting() {
    const greetings = {
        'medical': "Hello! I'm your medical assistant. How can I help you with health concerns today?",
        'agriculture': "Hi there! I'm your farming expert. What agricultural questions can I answer?",
        'finance': "Welcome! I'm your financial advisor. How can I assist with money matters?",
        'shopping': "Hello shopper! Ready to find some great deals? What are you looking for?",
        'education': "Greetings student! I'm here to help with your learning journey. What's your question?",
        'legal': "Hello. I provide general legal information. What would you like to know?",
        'sustainability': "Hi eco-warrior! Let's talk about sustainable living. What's on your mind?",
        'travel': "Welcome traveler! Where shall we explore today?",
        'hr': "Hello! I'm your HR assistant. How can I help with workplace matters?",
        'mentalhealth': "Hi there. This is a safe space to talk. How are you feeling today?"
    };
    
    return greetings[currentBotType] || "Hello! How can I help you today?";
}

function setupEventListeners() {
    // Handle form submission
    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            sendMessage();
        });
    }
    
    // Send message on button click
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    // Send message on Enter key (but not Shift+Enter)
    if (userInput) {
        userInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;
    
    // Add user message to chat
    addUserMessage(message);
    userInput.value = '';
    
    // Show typing indicator
    const typingIndicator = addTypingIndicator();
    
    try {
        // Call the API
        const response = await fetch(API_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                bot: currentBotType,
                message: message,
                history: conversationHistory.filter(msg => msg.role).map(msg => ({
                    role: msg.role,
                    content: msg.content
                }))
            })
        });

        // Remove typing indicator
        removeTypingIndicator(typingIndicator);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            addBotMessage("Sorry, I encountered an error. Please try again.");
            console.error("API Error:", data.error);
            return;
        }

        // Add bot response
        if (data.response) {
            addBotMessage(data.response, 'assistant');
        } else {
            addBotMessage("I'm not sure how to respond to that. Could you rephrase?", 'assistant');
        }
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator(typingIndicator);
        addBotMessage("Sorry, I'm having trouble connecting. Please try again later.", 'assistant');
    }
}

function addUserMessage(content) {
    const messageElement = createMessageElement(content, 'user');
    messageArea.appendChild(messageElement);
    conversationHistory.push({
        role: 'user',
        content: content,
        timestamp: new Date().toISOString()
    });
    scrollToBottom();
    saveConversation();
}

function addBotMessage(content, role = 'assistant') {
    const messageElement = createMessageElement(content, 'bot');
    messageArea.appendChild(messageElement);
    conversationHistory.push({
        role: role,
        content: content,
        timestamp: new Date().toISOString()
    });
    scrollToBottom();
    saveConversation();
}

function createMessageElement(content, sender) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}-message`;
    
    const contentElement = document.createElement('div');
    contentElement.className = 'message-content';
    contentElement.textContent = content;
    
    const timeElement = document.createElement('div');
    timeElement.className = 'message-time';
    timeElement.textContent = getCurrentTime();
    
    messageElement.appendChild(contentElement);
    messageElement.appendChild(timeElement);
    
    return messageElement;
}

function addTypingIndicator() {
    const typingElement = document.createElement('div');
    typingElement.className = 'message bot-message typing-indicator';
    typingElement.innerHTML = `
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    messageArea.appendChild(typingElement);
    scrollToBottom();
    return typingElement;
}

function removeTypingIndicator(indicator) {
    if (indicator && indicator.parentNode) {
        indicator.parentNode.removeChild(indicator);
    }
}

function getCurrentTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function scrollToBottom() {
    messageArea.scrollTop = messageArea.scrollHeight;
}

function saveConversation() {
    try {
        sessionStorage.setItem(`chat_${currentBotType}`, JSON.stringify(conversationHistory));
    } catch (e) {
        console.warn("Could not save conversation to sessionStorage:", e);
    }
}

function loadConversation() {
    try {
        const savedConversation = sessionStorage.getItem(`chat_${currentBotType}`);
        if (savedConversation) {
            conversationHistory = JSON.parse(savedConversation);
            
            // Rebuild conversation in UI
            conversationHistory.forEach(msg => {
                if (msg.role === 'user') {
                    addUserMessage(msg.content);
                } else {
                    addBotMessage(msg.content, msg.role);
                }
            });
        }
    } catch (e) {
        console.warn("Could not load conversation from sessionStorage:", e);
    }
}
async function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;
    
    addUserMessage(message);
    userInput.value = '';
    
    const typingIndicator = addTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                bot: currentBotType,
                message: message,
                history: conversationHistory
            })
        });

        const data = await response.json();
        
        if (data.requires_followup) {
            // Handle financial data follow-up
            if (data.ticker) {
                const detailedResponse = await fetchFinancialData(data.ticker);
                addBotMessage(detailedResponse);
            }
        } else {
            addBotMessage(data.response);
        }
    } catch (error) {
        addBotMessage("I'm having trouble accessing financial data. Please try again later.");
    } finally {
        removeTypingIndicator(typingIndicator);
    }
}

// Mock function for financial data (replace with real API call)
async function fetchFinancialData(ticker) {
    // In a real implementation, this would call a financial API
    return `Here's the latest data for ${ticker}:
    - Current Price: $165.32
    - Today's Change: +1.24%
    - 52-Week Range: $120.50 - $178.90
    - P/E Ratio: 24.5`;
}

// Add this CSS to your stylesheet:
/*
.typing-indicator {
    opacity: 0.6;
}
.typing-dots {
    display: inline-flex;
    align-items: center;
    height: 17px;
}
.typing-dots span {
    width: 8px;
    height: 8px;
    margin: 0 2px;
    background-color: #333;
    border-radius: 50%;
    display: inline-block;
    animation: typingAnimation 1.4s infinite both;
}
.typing-dots span:nth-child(2) {
    animation-delay: 0.2s;
}
.typing-dots span:nth-child(3) {
    animation-delay: 0.4s;
}
@keyframes typingAnimation {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}
*/