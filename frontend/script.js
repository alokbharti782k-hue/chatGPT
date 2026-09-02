const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const messages = document.querySelector('#messages');
const status = document.querySelector('#status');
let conversationId = null;

function addMessage(role, text) {
  const item = document.createElement('div');
  item.className = `message ${role}`;
  item.textContent = text;
  messages.appendChild(item);
  messages.scrollTop = messages.scrollHeight;
}

async function checkHealth() {
  try {
    const response = await fetch('/health');
    status.textContent = response.ok ? 'Online' : 'Offline';
  } catch {
    status.textContent = 'Offline';
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  addMessage('user', message);
  input.value = '';
  form.querySelector('button').disabled = true;
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, conversation_id: conversationId })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed');
    conversationId = data.conversation_id;
    addMessage('assistant', data.response);
  } catch (error) {
    addMessage('assistant', `Error: ${error.message}`);
  } finally {
    form.querySelector('button').disabled = false;
    input.focus();
  }
});

checkHealth();
