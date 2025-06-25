import React, { useState } from "react";
import GroSafeLogo from "../src/assets/images/GroSafeLogo.png";

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
        <div className="container pt-5">
            <div className="row">
                <div className="col-8 mx-auto bg-light p-3 shadow rounded">
                    {/* <h2 className="text-center mb-4">GroSafe Chatbot</h2> */}
                    <img src={GroSafeLogo} alt="Logo" className="img-fluid logo w-25 d-block mx-auto"></img>

                    <div className="border rounded p-3 mb-3 bg-white" style={{ height: '400px', overflowY: 'auto' }}>
                        <div className="alert alert-info text-center mb-4" role="alert">
                            <h4>Welcome to GroSafe Chatbot!</h4>
                            <p>Your AI assistant for child grooming awareness and support.</p>
                        </div>
                        {messages.map((msg, index) => (
                            <div key={index} className={`d-flex mb-2 ${msg.role === 'user' ? 'justify-content-end' : 'justify-content-start'}`}>
                                <div className={`p-2 rounded ${msg.role === 'user' ? 'bg-primary text-white' : 'bg-light'}`} style={{ maxWidth: '70%' }}>
                                    <p className="mb-0">{msg.text}</p>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="input-group">
                        <textarea
                            className="form-control bg-white"
                            placeholder="Welcome to GroSafe..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            rows={2}
                        />
                        <button
                            onClick={handleChat}
                            disabled={loading}
                            className="btn btn-primary"
                        >
                            {loading ? "..." : send_sv}
                        </button>
                    </div>
                </div>
            </div>
        </div>

    );
}

export default App;
