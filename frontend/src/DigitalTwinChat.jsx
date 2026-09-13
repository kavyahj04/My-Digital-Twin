import { useState, useRef, useEffect } from "react";
import { Plus, Send, Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";


const API_URL = "https://my-digital-twin-fkkv.onrender.com/chat";

export default function DigitalTwinChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [isThinking, setIsThinking] = useState(false);
  const [inputFocused, setInputFocused] = useState(false);
  const scrollRef = useRef(null);

  const hasStarted = messages.length > 0;

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
      setMessages((prev) => [...prev, { role: "assistant", content: data.reply, sources: data.sources }]);
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

  function renderInputBar(variant) {
    const isHero = variant === "hero";
    return (
      <div
        style={{
          width: "100%",
          maxWidth: "100%",
          minWidth: 0,
          display: "flex",
          gap: "10px",
          alignItems: "center",
          background: "#FFFFFF",
          borderRadius: "9999px",
          overflow: "hidden",
          border: inputFocused ? "1px solid #A855F7" : "1px solid #E5E3F0",
          boxShadow: inputFocused
            ? "0 0 0 3px rgba(168,85,247,0.15)"
            : isHero
            ? "0 8px 30px rgba(79, 70, 229, 0.08)"
            : "none",
          padding: isHero ? "10px 12px 10px 22px" : "6px 8px 6px 20px",
          transition: "box-shadow 0.15s ease, border-color 0.15s ease",
        }}
      >
        {isHero && <Plus size={20} color="#9CA3AF" style={{ flexShrink: 0 }} />}
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => setInputFocused(true)}
          onBlur={() => setInputFocused(false)}
          placeholder="Ask anything about Kavya..."
          style={{
            flex: 1,
            minWidth: 0,
            border: "none",
            padding: isHero ? "10px 4px" : "7px 4px",
            fontSize: isHero ? "17px" : "16px",
            outline: "none",
            background: "transparent",
            fontFamily: "'Inter', sans-serif",
            color: "#211C36",
          }}
        />
        <button
          className="send-btn"
          onClick={sendMessage}
          disabled={!input.trim() || isThinking}
          aria-label="Send message"
          style={{
            width: isHero ? "44px" : "40px",
            height: isHero ? "44px" : "40px",
            borderRadius: "9999px",
            border: "none",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
          }}
        >
          <Send size={18} color="#FFFFFF" />
        </button>
      </div>
    );
  }

  return (
    <div
      className="hero-bg app-shell"
      style={{
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
        html, body, #root { height: 100%; margin: 0; overflow-x: hidden; }

        .app-shell { height: 100vh; height: 100dvh; }

        .hero-section { padding: 24px 32px; }
        .hero-heading { font-size: 44px; }
        .header-bar { padding: 24px 32px; }
        .messages-inner { padding: 28px 32px; }
        .input-outer { padding: 18px 32px 24px; }
        .msg-bubble { max-width: 70%; }

        @media (max-width: 640px) {
          .hero-section { padding: 16px 16px; gap: 20px !important; }
          .hero-heading { font-size: 26px !important; line-height: 1.25; }
          .header-bar { padding: 16px 16px !important; }
          .header-bar h1 { font-size: 20px !important; }
          .header-bar p { font-size: 13px !important; }
          .messages-inner { padding: 16px 12px !important; gap: 12px !important; }
          .input-outer { padding: 10px 12px 14px !important; }
          .msg-bubble { max-width: 88% !important; font-size: 14.5px !important; }
          .gradient-ring { width: 34px !important; height: 34px !important; }
          .gradient-ring > div { width: 28px !important; height: 28px !important; }
        }

        @media (max-width: 380px) {
          .hero-heading { font-size: 22px !important; }
        }

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

        .hero-bg {
          background: radial-gradient(circle at 65% 45%, rgba(168, 85, 247, 0.12), transparent 55%),
            radial-gradient(circle at 30% 60%, rgba(79, 70, 229, 0.08), transparent 50%);
        }

        .md p { margin: 0 0 8px; }
        .md p:last-child { margin-bottom: 0; }
        .md ul, .md ol { margin: 0 0 8px; padding-left: 20px; }
        .md ul:last-child, .md ol:last-child { margin-bottom: 0; }
        .md li { margin-bottom: 4px; }
        .md strong { color: #211C36; font-weight: 600; }
        .md a { color: #A855F7; }
        .md code { background: rgba(0,0,0,0.06); border-radius: 4px; padding: 1px 5px; font-size: 0.9em; }
        .md pre { background: rgba(0,0,0,0.06); border-radius: 8px; padding: 10px 12px; overflow-x: auto; margin: 0 0 8px; }
        .md pre code { background: none; padding: 0; }
        .md h1, .md h2, .md h3 { margin: 0 0 8px; font-size: 1em; font-weight: 600; color: #211C36; }
        .md table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; border-collapse: collapse; width: max-content; max-width: 100%; font-size: 0.92em; margin: 0 0 8px; }
        .md th, .md td { border: 1px solid #E5E3F0; padding: 6px 12px; text-align: left; white-space: nowrap; }
        .md th { background: rgba(168, 85, 247, 0.08); font-weight: 600; color: #211C36; }
      `}</style>

      {/* thin black bar across the top of the page */}
      <div className="gradient-bar" style={{ height: "4px", width: "100%", flexShrink: 0 }} />

      {!hasStarted ? (
        /* Hero / empty state */
        <div
          className="hero-section"
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: "32px",
          }}
        >
          <h1
            className="hero-heading"
            style={{
              fontFamily: "'Space Grotesk', sans-serif",
              fontWeight: 500,
              color: "#211C36",
              margin: 0,
              textAlign: "center",
            }}
          >
            Hi, what would you like to know about Kavya?
          </h1>
          <div style={{ width: "100%", maxWidth: "700px" }}>{renderInputBar("hero")}</div>
        </div>
      ) : (
        <>
          {/* Header */}
          <div
            className="header-bar"
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "6px",
              background: "#14121F",
              boxShadow: "0 4px 20px rgba(20, 18, 31, 0.15)",
            }}
          >
            <div style={{ maxWidth: "880px", width: "100%", margin: "0 auto", display: "flex", flexDirection: "column", gap: "6px" }}>
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
                      background: "#14121F",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <Sparkles size={17} color="#C084FC" />
                  </div>
                </div>
                <h1
                  className="gradient-text"
                  style={{ fontFamily: "'Space Grotesk', sans-serif", fontWeight: 700, fontSize: "26px", margin: 0 }}
                >
                  Kavya's Digital Twin
                </h1>
              </div>
              <p style={{ margin: 0, fontSize: "14.5px", color: "#A9A6BD", lineHeight: 1.45 }}>
                Ask me anything about Kavya's professional background - her projects, skills, and experience.
              </p>
            </div>
          </div>

          {/* Messages */}
          <div
            className="chat-scroll"
            style={{ flex: 1, overflowY: "auto", display: "flex", justifyContent: "center" }}
          >
            <div className="messages-inner" style={{ width: "100%", maxWidth: "880px", display: "flex", flexDirection: "column", gap: "16px" }}>
              {messages.map((m, i) => (
                <div key={i} style={{ display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
                  <div
                    className={m.role === "user" ? "msg-bubble" : ""}
                    style={{
                      maxWidth: m.role === "user" ? undefined : "100%",
                      padding: "12px 16px",
                      borderRadius: m.role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
                      fontSize: "15px",
                      lineHeight: 1.55,
                      background: m.role === "user" ? "#EEF0FF" : "#F5F5F7",
                      color: "#211C36",
                    }}
                  >
                    {m.role === "assistant" ? (
                      <div className="md">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                      </div>
                    ) : (
                      m.content
                    )}
                    {m.role === "assistant" && m.sources?.length > 0 && (
                      <div
                        style={{
                          marginTop: "10px",
                          paddingTop: "8px",
                          borderTop: "1px solid rgba(0,0,0,0.08)",
                          fontSize: "12.5px",
                          color: "#6B7280",
                          display: "flex",
                          flexWrap: "wrap",
                          gap: "10px",
                        }}
                      >
                        <span>Sources:</span>
                        {m.sources.map((s, idx) =>
                          s.url ? (
                            <a
                              key={idx}
                              href={s.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              style={{ color: "#A855F7" }}
                            >
                              {s.title}
                            </a>
                          ) : (
                            <span key={idx}>{s.title}</span>
                          )
                        )}
                      </div>
                    )}
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
          <div style={{ borderTop: "1px solid rgba(20, 18, 31, 0.08)", display: "flex", justifyContent: "center", flexShrink: 0 }}>
            <div className="input-outer" style={{ width: "100%", maxWidth: "880px" }}>{renderInputBar("bar")}</div>
          </div>
        </>
      )}
    </div>
  );
}
