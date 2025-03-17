const sendBtn = document.getElementById("send-btn");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");
const receiverUsername = JSON.parse(
  document.getElementById("receiver-username-tag").textContent
);
const senderUsername = JSON.parse(
  document.getElementById("sender-username-tag").textContent
);
const deleteIconUrl = JSON.parse(
  document.getElementById("delete-icon-url").textContent
);
const editIconUrl = JSON.parse(
  document.getElementById("edit-icon-url").textContent
);
const deleteBtns = document.querySelectorAll("#message-delete-btn");
// const editBtns = document.querySelectorAll("#message-edit-btn");

// Determine the correct WebSocket protocol (ws or wss) based on the page's protocol
const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
// Change the URL below to match your routing for websockets
const chatSocket = new WebSocket(
  wsScheme + "://" + window.location.host + "/ws/chat/" + `${receiverUsername}/`
);

// Function to append a message bubble to the chat area
function appendMessage(messageId, messageText, type) {
  const messageBubble = document.createElement("div");
  messageBubble.classList.add("message", type);
  if (type == "sent") {
    messageBubble.innerHTML = `<div class="message-text">${messageText}</div>
        <div class="message-actions">
          <div
            id="message-edit-btn"
            class="edit-btn"
            data-info="${messageId}"
          >
            <img src="${editIconUrl}" alt="edit" />
          </div>
          <div
            id="message-delete-btn"
            class="delete-btn"
            data-info="${messageId}"
          >
            <img src="${deleteIconUrl}" alt="delete" />
          </div>
        </div>`;
  } else {
    messageBubble.innerHTML = `${messageText}`;
  }

  chatMessages.appendChild(messageBubble);
  if (type == "sent") {
    deleteBtn = messageBubble.querySelector("#message-delete-btn");
    deleteBtn.addEventListener("click", (e) => {
      const messageId = deleteBtn.getAttribute("data-info");
      showConfirmationDialog(deleteMessageRequest, messageId);
    });
  }

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send a message via the WebSocket
function sendMessage() {
  const text = chatInput.value.trim();
  if (text !== "") {
    // Send the message data via WebSocket in JSON format
    chatSocket.send(JSON.stringify({ message: text }));
    // Clear the input field
    chatInput.value = "";
  }
}

// Event listeners for sending messages
sendBtn.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
    e.preventDefault();
  }
});

// WebSocket event: connection established
chatSocket.onopen = function (e) {
  console.log("WebSocket connection established.");
};

// WebSocket event: message received
chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  // Assuming the server sends data with a "message" property
  if (data.messageText) {
    const type = data.senderUsername == senderUsername ? "sent" : "received";
    appendMessage(data.id, data.messageText, type);
  }
};

// WebSocket event: error handling
chatSocket.onerror = function (e) {
  console.error("WebSocket error:", e);
};

// WebSocket event: connection closed
chatSocket.onclose = function (e) {
  console.log("WebSocket connection closed.");
};

// function to delete message
function showConfirmationDialog(callback, messageId) {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("confirmationDialog").style.display = "block";
  document.getElementById("confirmBtn").onclick = function () {
    callback(messageId);
    closeDialog();
  };
  document.getElementById("cancelBtn").onclick = function () {
    closeDialog();
  };
}

function closeDialog() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("confirmationDialog").style.display = "none";
}

function deleteMessageRequest(messageId) {
  window.location.href = window.location.href + "delete/" + messageId;
}

deleteBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const messageId = btn.getAttribute("data-info");
    showConfirmationDialog(deleteMessageRequest, messageId);
  });
});
