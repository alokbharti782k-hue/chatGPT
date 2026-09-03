const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const messages = document.querySelector('#messages');
const status = document.querySelector('#status');
let conversationId = null;

// The chat endpoints are public and do not require authentication, but we
// send the Authorization header anyway so requests remain valid if the
// backend configuration changes. The token can be supplied by the hosting
// page via `window.API_KEY` (e.g. injected at deploy time).
const API_KEY = (typeof window !== 'undefined' && window.API_KEY) || '';

function authHeaders() {
  const headers = { 'Content-Type': 'application/json' };
  if (API_KEY) {
    headers['Authorization'] = `Bearer ${API_KEY}`;
  }
  return headers;
}

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
      headers: authHeaders(),
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
