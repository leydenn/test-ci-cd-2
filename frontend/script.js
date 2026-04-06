const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'http://ваш-сервер:8000';

async function loadMessages() {
    try {
        const response = await fetch(`${API_URL}/messages`);
        const messages = await response.json();
        
        const container = document.getElementById('messages');
        if (messages.length === 0) {
            container.innerHTML = '<div class="loading">No messages yet. Be the first! 🎉</div>';
            return;
        }
        
        container.innerHTML = messages.map(msg => `
            <div class="message-card">
                <div class="message-header">
                    <span>👤 ${escapeHtml(msg.username)}</span>
                    <span class="message-time">${new Date(msg.created_at).toLocaleString()}</span>
                </div>
                <div class="message-content">${escapeHtml(msg.content)}</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading messages:', error);
        document.getElementById('messages').innerHTML = '<div class="loading">❌ Failed to load messages</div>';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function sendMessage() {
    const username = document.getElementById('username').value.trim();
    const content = document.getElementById('content').value.trim();
    
    if (!username || !content) {
        alert('Please fill both fields');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, content })
        });
        
        if (response.ok) {
            document.getElementById('username').value = '';
            document.getElementById('content').value = '';
            loadMessages();
        }
    } catch (error) {
        console.error('Error sending message:', error);
        alert('Failed to send message');
    }
}

document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('content').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

loadMessages();
// Refresh every 5 seconds
setInterval(loadMessages, 5000);