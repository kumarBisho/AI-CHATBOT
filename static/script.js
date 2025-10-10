

document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");
  const clearBtn = document.getElementById("clear-btn");
  const fileInput = document.getElementById("file-input");
  const uploadBtn = document.getElementById("upload-btn");
  const fileStatus = document.getElementById("file-status");
  const themeToggle = document.getElementById("theme-toggle");

  let chatHistory = [];

  // Send user message
  async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    appendMessage("You", question, "user");
    userInput.value = "";

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, history: chatHistory })
      });

      const data = await response.json();
      if (data.answer) {
        appendMessage("Bot", data.answer, "bot");
        chatHistory.push({ role: "user", content: question });
        chatHistory.push({ role: "assistant", content: data.answer });
      } else {
        appendMessage("Error", data.error || "Something went wrong!", "bot");
      }
    } catch (err) {
      appendMessage("Error", "Server connection failed.", "bot");
      console.error(err);
    }
  }

  // Upload file
  async function uploadFile() {
    const file = fileInput.files[0];
    if (!file) {
      alert("Please select a file to upload!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fileStatus.textContent = "Uploading...";

    try {
      const res = await fetch("/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      if (res.ok) {
        fileStatus.textContent = "File uploaded successfully!";
      } else {
        fileStatus.textContent = "Error: " + (data.error || "Upload failed.");
      }
    } catch (err) {
      fileStatus.textContent = "Error uploading file.";
      console.error(err);
    }
  }
// Clear chat
  function clearChat() {
    chatBox.innerHTML = "";
    chatHistory = [];
  }

  // Append message to chat
  function appendMessage(sender, text, className) {
    const message = document.createElement("div");
    message.classList.add("message", className);
    message.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Event listeners
  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
  });
  uploadBtn.addEventListener("click", uploadFile);
  clearBtn.addEventListener("click", clearChat);


  themeToggle.addEventListener("click", ()=>{
    document.body.classList.toggle("dark-mode");
    if(document.body.classList.contains("dark-mode")){
      themeToggle.textContent = "🌙";
    } else{
      themeToggle.textContent = "☀️";
    }
  });
});


// Theme toggle
