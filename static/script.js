document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chat-box");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  async function sendMessage() {
    const question = userInput.value.trim();
    if (!question) return;

    appendMessage("You", question, "user");
    userInput.value = "";

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });

      const data = await response.json();
      if (data.answer) {
        appendMessage("Bot", data.answer, "bot");
      } else {
        appendMessage("Error", data.error || "Something went wrong!", "bot");
      }
    } catch (err) {
      appendMessage("Error", "Server connection failed.", "bot");
      console.error(err);
    }
  }

  function appendMessage(sender, text, className) {
    const message = document.createElement("div");
    message.classList.add("message", className);
    message.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", e => {
    if (e.key === "Enter") sendMessage();
  });
});
