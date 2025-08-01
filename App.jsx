import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;  // dynamically set the backend URL

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const ask = async (e) => {
    e.preventDefault();
    if (!question.trim()) { setError("Please enter a question."); return; }

    setLoading(true); setError(""); setAnswer("");
    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });

      if (!res.ok) throw new Error((await res.json()).error || "Server error");
      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      setError(err.message);
    } finally { setLoading(false); }
  };

  return (
    <div className="App">
      <form onSubmit={ask}>
        <textarea
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>Ask</button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {answer && <p>{answer}</p>}
    </div>
  );
}
