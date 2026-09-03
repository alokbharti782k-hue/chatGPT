const form = document.querySelector('#chat-form');
const input = document.querySelector('#message');
const messages = document.querySelector('#messages');
const status = document.querySelector('#status');
const clearChat = document.querySelector('#clear-chat');
const promptCards = document.querySelectorAll('.prompt-card');
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
  if (contentType.includes('application/json')) return await response.json();
  const text = await response.text();
  return { detail: text || `Request failed with HTTP ${response.status}` };
}

async function checkHealth() {
  try {
    const response = await fetch('/health', { cache: 'no-store' });
    const label = status.querySelector('span');
    if (label) label.textContent = response.ok ? 'Online' : 'Offline';
    status.classList.toggle('offline', !response.ok);
  } catch {
    const label = status.querySelector('span');
    if (label) label.textContent = 'Offline';
    status.classList.add('offline');
  }
}

function resetConversation() {
  conversationId = null;
  messages.innerHTML = '';
  input.value = '';
  input.focus();
}

promptCards.forEach((card) => {
  card.addEventListener('click', () => {
    input.value = card.dataset.prompt || '';
    input.focus();
    input.style.height = 'auto';
    input.style.height = `${Math.min(input.scrollHeight, 180)}px`;
  });
});

clearChat?.addEventListener('click', resetConversation);

input.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = `${Math.min(input.scrollHeight, 180)}px`;
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addMessage('user', message);
  input.value = '';
  input.style.height = 'auto';
  const sendButton = form.querySelector('button[type="submit"]');
  sendButton.disabled = true;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: authHeaders(),
      cache: 'no-store',
      body: JSON.stringify({ message, conversation_id: conversationId })
    });

    const data = await readResponse(response);
    if (!response.ok) throw new Error(data.detail || `Request failed with HTTP ${response.status}`);
    if (!data.response) throw new Error('The server returned no assistant response.');

    conversationId = data.conversation_id || conversationId;
    addMessage('assistant', data.response);
  } catch (error) {
    addMessage('assistant', `Error: ${error.message}`);
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
});

checkHealth();
