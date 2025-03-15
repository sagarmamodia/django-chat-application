// active chat objects
const chats = JSON.parse(
  document.getElementById("active-chats-data").textContent
);
console.log(chats);
// Render the chat list based on the provided chat array
function renderChats(chatArray) {
  const chatList = document.getElementById("chatList");
  chatList.innerHTML = ""; // Clear the current list
  chatArray.forEach((chat) => {
    // Create container for each chat item
    const chatItem = document.createElement("div");
    chatItem.classList.add("chat-item");

    // Create inner HTML structure
    chatItem.innerHTML = `
          <img src="${chat.profile_icon}" alt="${chat.username}" class="profile-icon">
          <div class="chat-info">
            <div class="chat-name">${chat.username}</div>
            <div class="chat-message">${chat.last_message}</div>
          </div>
        `;
    chatList.appendChild(chatItem);
  });
}

// Filter chats based on the search input value
function filterChats() {
  const query = document.getElementById("searchInput").value.toLowerCase();
  const filteredChats = chats.filter(
    (chat) =>
      chat.username.toLowerCase().includes(query) ||
      chat.last_message.toLowerCase().includes(query)
  );
  renderChats(filteredChats);
}
