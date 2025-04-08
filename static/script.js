const messageForm = getElementById('message-form');
const messageInput = getElementById('message-input');
const chatLog = getElementById('chat-log');
const clearButton = getElementById('clear-button');
const regenerateButton = getElementById('regenerate-button');
const chatIdSelect = getElementById('chat-id-select');

regenerateButton.addEventListener('click', regenerateChatId);
chatIdSelect.addEventListener('change', updateChatId);
messageForm.addEventListener('submit', event => {
  event.preventDefault();
  const message = messageInput.value;
  messageInput.value = '';
  addMessage({ sender: 'user', message });
  chatLog.classList.add('loading');
  messageInput.disabled = true;
  // messageInput.classList.add('blur');
  const body = `message=${encodeURIComponent(message)}&chat_id=${localStorage.getItem('selectedChatId')}`;
  fetch('/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: body
  })
  .then(response => response.json())
  .then(data => {
    addMessage({ sender: 'bot', message: data.response });
    // messageInput.classList.remove('blur');
    chatLog.classList.remove('loading');
    window.scrollTo(0, document.body.scrollHeight);
     messageInput.disabled = false;
  });
});

function getElementById(id) {
  return document.getElementById(id);
}

function addMessage({ sender, message }) {
  const messageElem = document.createElement('div');
  messageElem.classList.add('message', `${sender}-message`);

  const regex = /```([\s\S]*?)```/g;
  const formattedMessage = message.replace(regex, (match, code) => {
    const escapedCode = code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return `<div class="codeblock-container"><pre class="codeblock"><code>${escapedCode}</code></pre><button class="copy-button">copy</button></div>`;
  });

  messageElem.innerHTML = formattedMessage;
  chatLog.appendChild(messageElem);

  messageElem.querySelectorAll('.copy-button').forEach(button => {
    button.addEventListener('click', () => {
      const codeElem = button.previousElementSibling.firstElementChild;
      const range = document.createRange();
      range.selectNodeContents(codeElem);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      try {
        const successful = document.execCommand('copy');
        if (successful) {
          button.textContent = 'Copy OK';
          setTimeout(() => {
            button.textContent = 'Copy';
          }, 1000); // ÔÚ1000ºÁÃë£¨1Ãë£©ºó»Ö¸´Ô­Ê¼ÎÄ±¾
        } else {
          throw new Error('¸´ÖÆÊ§°Ü');
        }
      } catch (err) {
        console.error('¸´ÖÆÊ§°Ü', err);
        alert('¸´ÖÆÊ§°Ü£¬ÇëÊÖ¶¯¸´ÖÆ');
      }
      selection.removeAllRanges();
    });
  });
}


function clearChatId() {
  localStorage.removeItem('chatId');
  localStorage.removeItem('chatIds');
  localStorage.removeItem('selectedChatId');
  alert('Chat ID history cleared successfully!');
  location.reload();
}

function regenerateChatId() {
  const newChatId = Math.random().toString(36).substring(2, 15);
  localStorage.setItem('chatId', newChatId);
  const chatIds = localStorage.getItem('chatIds') ? JSON.parse(localStorage.getItem('chatIds')) : [];
  chatIds.push(newChatId);
  localStorage.setItem('chatIds', JSON.stringify(chatIds));
  const option = document.createElement('option');
  option.value = newChatId;
  option.textContent = newChatId;
  chatIdSelect.appendChild(option);
  localStorage.setItem('selectedChatId', newChatId)
  fetch('/new', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body:`chat_id=${localStorage.getItem('selectedChatId')}`
  })
  .then(response => response.json())
  .then(data => {
    alert('new chat gpt already');
  });

}

function updateChatId() {
  localStorage.setItem('selectedChatId', chatIdSelect.value);
}

if (!localStorage.getItem('chatId')) {
  const newChatId = Math.random().toString(36).substring(2, 15);
  localStorage.setItem('chatId', newChatId);
  const chatIds = [newChatId];
  localStorage.setItem('chatIds', JSON.stringify(chatIds));
  const option = document.createElement('option');
  

}

if (localStorage.getItem('chatIds')) {
  const chatIds = JSON.parse(localStorage.getItem('chatIds'));
  chatIds.forEach(chatId => {
    const option = document.createElement('option');
    option.value = chatId;
    option.textContent = chatId;
    chatIdSelect.appendChild(option);
    localStorage.setItem('selectedChatId', chatIdSelect.value);
  });
}

clearButton.addEventListener('click', clearChatId);
