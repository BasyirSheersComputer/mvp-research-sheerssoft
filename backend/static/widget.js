(function () {
    // Configuration
    const API_URL = document.currentScript.getAttribute('data-api-url') || 'http://localhost:8000';
    const PROPERTY_ID = document.currentScript.getAttribute('data-property-id');
    const THEME_COLOR = document.currentScript.getAttribute('data-color') || '#0F172A'; // Slate-900 default

    if (!PROPERTY_ID) {
        console.error('SheersSoft AI Widget: data-property-id is required');
        return;
    }

    // Creating styles
    const style = document.createElement('style');
    style.innerHTML = `
        #sheerssoft-widget-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        #sheerssoft-launcher {
            width: 60px;
            height: 60px;
            background-color: ${THEME_COLOR};
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
        }

        #sheerssoft-launcher:hover {
            transform: scale(1.05);
        }

        #sheerssoft-launcher svg {
            width: 32px;
            height: 32px;
            fill: white;
        }

        #sheerssoft-chat-window {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 380px;
            height: 600px;
            max-height: calc(100vh - 100px);
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
            display: none;
            flex-direction: column;
            overflow: hidden;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.3s, transform 0.3s;
        }

        #sheerssoft-chat-window.open {
            display: flex;
            opacity: 1;
            transform: translateY(0);
        }

        .sheerssoft-header {
            background-color: ${THEME_COLOR};
            color: white;
            padding: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .sheerssoft-header h3 {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
        }

        .sheerssoft-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            background: #f8fafc;
        }

        .sheerssoft-message {
            max-width: 80%;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.5;
            position: relative;
        }

        .sheerssoft-message.guest {
            align-self: flex-end;
            background-color: ${THEME_COLOR};
            color: white;
            border-bottom-right-radius: 2px;
        }

        .sheerssoft-message.ai {
            align-self: flex-start;
            background-color: white;
            color: #1e293b;
            border-bottom-left-radius: 2px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .sheerssoft-input-area {
            padding: 16px;
            background: white;
            border-top: 1px solid #e2e8f0;
            display: flex;
            gap: 8px;
        }

        .sheerssoft-input-area input {
            flex: 1;
            padding: 10px 14px;
            border: 1px solid #e2e8f0;
            border-radius: 24px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }

        .sheerssoft-input-area input:focus {
            border-color: ${THEME_COLOR};
        }

        .sheerssoft-send-btn {
            background: none;
            border: none;
            cursor: pointer;
            color: ${THEME_COLOR};
            padding: 4px;
        }

        .sheerssoft-typing {
            font-size: 12px;
            color: #64748b;
            margin-left: 12px;
            display: none;
        }
    `;
    document.head.appendChild(style);

    // Creating DOM elements
    const container = document.createElement('div');
    container.id = 'sheerssoft-widget-container';

    const launcher = document.createElement('div');
    launcher.id = 'sheerssoft-launcher';
    launcher.innerHTML = `
        <svg viewBox="0 0 24 24">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
        </svg>
    `;

    const chatWindow = document.createElement('div');
    chatWindow.id = 'sheerssoft-chat-window';
    chatWindow.innerHTML = `
        <div class="sheerssoft-header">
            <h3>Concierge</h3>
            <span style="cursor:pointer; font-size: 20px;">×</span>
        </div>
        <div class="sheerssoft-messages" id="sheerssoft-messages"></div>
        <div class="sheerssoft-typing" id="sheerssoft-typing">Concierge is typing...</div>
        <div class="sheerssoft-input-area">
            <input type="text" id="sheerssoft-input" placeholder="Ask about rooms, rates, facilities..." />
            <button class="sheerssoft-send-btn">➤</button>
        </div>
    `;

    container.appendChild(chatWindow);
    container.appendChild(launcher);
    document.body.appendChild(container);

    // Logic
    let isOpen = false;
    let sessionId = localStorage.getItem('sheerssoft_session_id') || crypto.randomUUID();
    localStorage.setItem('sheerssoft_session_id', sessionId);

    function toggleChat() {
        isOpen = !isOpen;
        chatWindow.classList.toggle('open', isOpen);
        if (isOpen) {
            document.getElementById('sheerssoft-input').focus();
            if (document.getElementById('sheerssoft-messages').children.length === 0) {
                appendMessage('ai', 'Hi! 👋 Welcome to our hotel. How can I help you today?');
            }
        }
    }

    launcher.addEventListener('click', toggleChat);
    chatWindow.querySelector('.sheerssoft-header span').addEventListener('click', toggleChat);

    function appendMessage(role, text) {
        const msgs = document.getElementById('sheerssoft-messages');
        const div = document.createElement('div');
        div.className = `sheerssoft-message ${role}`;
        div.innerText = text;
        msgs.appendChild(div);
        msgs.scrollTop = msgs.scrollHeight;
    }

    async function sendMessage() {
        const input = document.getElementById('sheerssoft-input');
        const text = input.value.trim();
        if (!text) return;

        appendMessage('guest', text);
        input.value = '';

        document.getElementById('sheerssoft-typing').style.display = 'block';

        try {
            const response = await fetch(`${API_URL}/api/v1/conversations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    property_id: PROPERTY_ID,
                    message: text,
                    session_id: sessionId
                }),
            });
            const data = await response.json();
            document.getElementById('sheerssoft-typing').style.display = 'none';
            appendMessage('ai', data.response);
        } catch (error) {
            console.error('SheersSoft AI Error:', error);
            document.getElementById('sheerssoft-typing').style.display = 'none';
            appendMessage('ai', 'Sorry, I am having trouble connecting to the concierge. Please try again.');
        }
    }

    document.getElementById('sheerssoft-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    chatWindow.querySelector('.sheerssoft-send-btn').addEventListener('click', sendMessage);

})();
