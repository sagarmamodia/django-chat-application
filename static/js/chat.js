const sendBtn = document.getElementById("send-btn");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");
const receiver_username = JSON.parse(
  document.getElementById("username_tag").textContent
);

// Determine the correct WebSocket protocol (ws or wss) based on the page's protocol
const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
// Change the URL below to match your routing for websockets
const chatSocket = new WebSocket(
  wsScheme +
    "://" +
    window.location.host +
    "/ws/chat/" +
    `${receiver_username}/`
);

// Function to append a message bubble to the chat area
function appendMessage(message, type) {
  const messageBubble = document.createElement("div");
  messageBubble.classList.add("message", type);
  messageBubble.textContent = message;
  chatMessages.appendChild(messageBubble);
  // Auto-scroll to the bottom of the chat
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send a message via the WebSocket
function sendMessage() {
  const text = chatInput.value.trim();
  if (text !== "") {
    // Send the message data via WebSocket in JSON format
    chatSocket.send(JSON.stringify({ message: text }));
    // Optionally, you can immediately show the sent message as a "sent" bubble
    appendMessage(text, "sent");
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
  if (data.message) {
    // Append received messages with the "received" class
    appendMessage(data.message, "received");
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
