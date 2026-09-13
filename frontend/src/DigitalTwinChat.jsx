import { useState, useRef, useEffect } from "react";
import { Send, Sparkles } from "lucide-react";


const API_URL = "https://my-digital-twin-fkkv.onrender.com/chat";

const WELCOME_MESSAGE = {
  role: "assistant",
  content:
    "Hi, I'm Kavya's digital twin. Ask me anything about her professional background - her projects, skills, or experience.",
};

export default function DigitalTwinChat() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [isThinking, setIsThinking] = useState(false);
  const [inputFocused, setInputFocused] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  async function sendMessage() {
    const text = input.trim();
    if (!text || isThinking) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setIsThinking(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, message: text }),
      });
      if (!response.ok) throw new Error("Request failed");
      const data = await response.json();
      setSessionId(data.session_id);
      setMessages((prev) => [...prev, { role: "assistant", content: data.reply }]);
    } catch (err) {
      // Fallback only so this design can be previewed without a live backend.
      // Remove this catch's content once wired to your real deployed API.
      await new Promise((resolve) => setTimeout(resolve, 900));
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "(Preview mode - backend not reachable here.) Once deployed, this is where Kavya's real answer would appear, pulled from her GitHub and LinkedIn knowledge base.",
        },
      ]);
    } finally {
      setIsThinking(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div
      style={{
        height: "100vh",
        width: "100%",
        background: "#FFFFFF",
        display: "flex",
        flexDirection: "column",
        fontFamily: "'Inter', sans-serif",
        boxSizing: "border-box",
      }}
    >
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500;600&display=swap');

        * { box-sizing: border-box; }
        html, body, #root { height: 100%; margin: 0; }

        @keyframes orb-spin { to { transform: rotate(360deg); } }
        @keyframes orb-breathe {
          0%, 100% { transform: scale(0.85); opacity: 0.75; }
          50% { transform: scale(1.15); opacity: 1; }
        }
        .thinking-orb {
          width: 20px;
          height: 20px;
          border-radius: 9999px;
          background: conic-gradient(from 0deg, #4F46E5, #A855F7, #EC4899, #4F46E5);
          animation: orb-spin 1.6s linear infinite, orb-breathe 1.6s ease-in-out infinite;
        }
        @media (prefers-reduced-motion: reduce) {
          .thinking-orb { animation: none; }
          .send-btn { transition: none !important; }
        }

        .gradient-bar { background: #000000; }
        .gradient-ring { background: linear-gradient(135deg, #4F46E5, #A855F7, #EC4899); }
        .gradient-text {
          background: linear-gradient(135deg, #4F46E5, #A855F7, #EC4899);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
        }
        .send-btn { background: linear-gradient(135deg, #4F46E5, #A855F7, #EC4899); transition: transform 0.15s ease, box-shadow 0.15s ease; }
        .send-btn:hover:not(:disabled) { transform: scale(1.06); box-shadow: 0 6px 20px rgba(168, 85, 247, 0.35); }
        .send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
        .send-btn:focus-visible { outline: 2px solid #A855F7; outline-offset: 2px; }

        .chat-input:focus-visible { outline: none; }

        .chat-scroll::-webkit-scrollbar { width: 8px; }
        .chat-scroll::-webkit-scrollbar-thumb { background: #E4E1F5; border-radius: 999px; }
      `}</style>

      {/* thin gradient brand bar across the top of the page */}
      <div className="gradient-bar" style={{ height: "4px", width: "100%", flexShrink: 0 }} />

      {/* Header */}
      <div
        style={{
          padding: "28px 32px 20px",
          display: "flex",
          flexDirection: "column",
          gap: "6px",
          borderBottom: "1px solid #F0EFF6",
          maxWidth: "880px",
          width: "100%",
          margin: "0 auto",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div
            className="gradient-ring"
            style={{
              width: "42px",
              height: "42px",
              borderRadius: "9999px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
            }}
          >
            <div
              style={{
                width: "36px",
                height: "36px",
                borderRadius: "9999px",
                background: "#FFFFFF",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Sparkles size={17} color="#A855F7" />
            </div>
          </div>
          <h1
            className="gradient-text"
            style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 700, fontSize: "26px", margin: 0 }}
          >
            Kavya's Digital Twin
          </h1>
        </div>
        <p style={{ margin: 0, fontSize: "14.5px", color: "#6B7280", lineHeight: 1.45 }}>
          Ask me anything about Kavya's professional background - her projects, skills, and experience.
        </p>
      </div>

      {/* Messages */}
      <div
        className="chat-scroll"
        style={{ flex: 1, overflowY: "auto", display: "flex", justifyContent: "center" }}
      >
        <div style={{ width: "100%", maxWidth: "880px", padding: "28px 32px", display: "flex", flexDirection: "column", gap: "16px" }}>
          {messages.map((m, i) => (
            <div key={i} style={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
              <div
                style={{
                  maxWidth: "70%",
                  padding: "12px 16px",
                  borderRadius: m.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                  fontSize: "15px",
                  lineHeight: 1.55,
                  background: m.role === "user" ? "#EEF0FF" : "#F5F5F7",
                  color: "#211C36",
                }}
              >
                {m.content}
              </div>
            </div>
          ))}

          {isThinking && (
            <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "center", gap: "8px", padding: "4px 2px" }}>
              <div className="thinking-orb" />
              <span style={{ fontSize: "13.5px", color: "#9CA3AF" }}>thinking</span>
            </div>
          )}
          <div ref={scrollRef} />
        </div>
      </div>

      {/* Input */}
      <div style={{ borderTop: "1px solid #F0EFF6", display: "flex", justifyContent: "center", flexShrink: 0 }}>
        <div style={{ width: "100%", maxWidth: "880px", padding: "18px 32px 24px", display: "flex", gap: "12px", alignItems: "center" }}>
          <input
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setInputFocused(true)}
            onBlur={() => setInputFocused(false)}
            placeholder="Ask about her projects, skills..."
            style={{
              flex: 1,
              border: inputFocused ? "1px solid #A855F7" : "1px solid #E5E3F0",
              boxShadow: inputFocused ? "0 0 0 3px rgba(168,85,247,0.15)" : "none",
              borderRadius: "9999px",
              padding: "13px 20px",
              fontSize: "15px",
              outline: "none",
              fontFamily: "'Inter', sans-serif",
              color: "#211C36",
              transition: "box-shadow 0.15s ease, border-color 0.15s ease",
            }}
          />
          <button
            className="send-btn"
            onClick={sendMessage}
            disabled={!input.trim() || isThinking}
            aria-label="Send message"
            style={{
              width: "46px",
              height: "46px",
              borderRadius: "9999px",
              border: "none",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
            }}
          >
            <Send size={19} color="#FFFFFF" />
          </button>
        </div>
      </div>
    </div>
  );
}