import React, { useState } from "react";

// Add a type for chat messages
type Message = { role: string; content: string };

const Dashboard: React.FC = () => {
  const [showChat, setShowChat] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  async function sendMessage() {
    if (!input.trim()) return;
    const userMessage = { role: "user", content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput("");
    try {
      // Replace with your OpenAI backend endpoint
      const res = await fetch("http://localhost:9000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      const botReply = { role: "assistant", content: data.reply };
      setMessages([...newMessages, botReply]);
    } catch (err) {
      setMessages([...newMessages, { role: "assistant", content: "Error: could not reach OpenAI backend." }]);
    }
  }

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>Hello World from FX Platform</h1>

      {showChat && (
        <div
          style={{
            position: "fixed",
            bottom: "80px",
            right: "20px",
            width: "350px",
            height: "500px",
            boxShadow: "0 0 15px rgba(0,0,0,0.2)",
            borderRadius: "10px",
            overflow: "hidden",
            background: "white",
            zIndex: 9999,
            display: 'flex', flexDirection: 'column'
          }}
        >
          {/* Embedded OpenAI ChatBot UI */}
          <div style={{ padding: 20, height: '100%', display: 'flex', flexDirection: 'column' }}>
            <div id="chat-messages" style={{ flex: 1, overflowY: 'auto', marginBottom: 10, border: '1px solid #eee', borderRadius: 6, padding: 8, background: '#f9f9f9' }}>
              {messages && messages.map((m, idx) => (
                <div key={idx} style={{ marginBottom: 6 }}>
                  <b>{m.role === 'user' ? 'You' : 'OpenAI'}:</b> {m.content}
                </div>
              ))}
            </div>
            <div style={{ display: 'flex' }}>
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') sendMessage(); }}
                placeholder="Ask OpenAI..."
                style={{ flex: 1, padding: 6, borderRadius: 4, border: '1px solid #ccc' }}
              />
              <button onClick={sendMessage} style={{ marginLeft: 8, padding: '6px 16px', borderRadius: 4, background: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}>Send</button>
            </div>
          </div>
        </div>
      )}

      <div
        onClick={() => setShowChat(!showChat)}
        title="I am SpikiFi, how may I help you?"
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          background: "#007bff",
          color: "white",
          padding: "12px 16px",
          borderRadius: "50%",
          cursor: "pointer",
          boxShadow: "0 4px 10px rgba(0, 0, 0, 0.3)",
          zIndex: 9999,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {/* Render the logo.svg as the icon */}
        <img src={require("./logo.svg").default} alt="Logo" style={{ width: 32, height: 32 }} />
      </div>
    </div>
  );
};

export default Dashboard;
