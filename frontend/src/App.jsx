import React, { useState } from "react";

function App() {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleChat = async () => {
        if (!input.trim()) return;

        setInput("");
        setLoading(true);
        const newMessages = [...messages, { role: "user", text: input }];
        setMessages(newMessages);

        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: input }),
        });

        const data = await res.json();

        setMessages([...newMessages, { role: "bot", text: data.response }]);
        setLoading(false);
    };

    const send_sv = <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        >
                        <line x1="12" y1="19" x2="12" y2="5" />
                        <polyline points="5 12 12 5 19 12" />
                    </svg>

    return (
        <div className="container">
            <h1 className="chat-title">GroSafe Chatbot</h1>
            <div className="chat-container">
                {messages.map((msg, index) => (
                    <div key={index} className={`chat-bubble ${msg.role}`}>
                        <p>{msg.text}</p>
                    </div>
                ))}
            </div>
            <div className="input-area">
                <textarea
                    placeholder="Welcome to GroSafe..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    rows={3}
                />
                
                <button onClick={handleChat} disabled={loading} className="send-button">
                    {loading ? "..." : send_sv}
                </button>
            </div>
        </div>
    );
}

export default App;
