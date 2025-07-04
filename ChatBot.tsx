import React, { useState } from "react";

const ChatBot: React.FC = () => {
  const [visible, setVisible] = useState(true);

  return visible ? (
    <div style={{ padding: 10 }}>
      <p>ChatBot UI here</p>
      <button onClick={() => setVisible(false)}>Close</button>
    </div>
  ) : null;
};

export default ChatBot;
