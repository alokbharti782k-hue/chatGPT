const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const messages = document.querySelector('#messages');
const status = document.querySelector('#status');
let conversationId = null;

// Chat is intentionally public. Never expose OPENAI_API_KEY in frontend code.
function authHeaders() {
  return { 'Content-Type': 'application/json' };
}

function addMessage(role, text) {
  const item = document.createElement('div');
  item.className = `message ${role}`;
  item.textContent = text;
  messages.appendChild(item);
  messages.scrollTop = messages.scrollHeight;
}

async function readResponse(response) {
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return await response.json();
  }

  const text = await response.text();
  return { detail: text || `Request failed with HTTP ${response.status}` };
}

async function checkHealth() {
  try {
    const response = await fetch('/health', { cache: 'no-store' });
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
      cache: 'no-store',
      body: JSON.stringify({ message, conversation_id: conversationId })
    });

    const data = await readResponse(response);
    if (!response.ok) {
      throw new Error(data.detail || `Request failed with HTTP ${response.status}`);
    }

    if (!data.response) {
      throw new Error('The server returned no assistant response.');
    }

    conversationId = data.conversation_id || conversationId;
    addMessage('assistant', data.response);
  } catch (error) {
    addMessage('assistant', `Error: ${error.message}`);
  } finally {
    form.querySelector('button').disabled = false;
    input.focus();
  }
});

checkHealth();
