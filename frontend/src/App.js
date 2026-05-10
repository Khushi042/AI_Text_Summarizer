import React, { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTextSubmit = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
      });

      const data = await response.json();
      setSummary(data.summary || data.error);

    } catch (error) {
      setSummary("Error connecting to backend");
    }

    setLoading(false);
  };

  const handleFileSubmit = async () => {
    if (!file) {
      alert("Please select a PDF");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/summarize-pdf", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      setSummary(data.summary || data.error);

    } catch (error) {
      setSummary("Error uploading PDF");
    }

    setLoading(false);
  };

  return (
    <div className="app">

      <div className="container">

        <h1> AI Text Summarizer</h1>

        <textarea
          placeholder="Enter your text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div className="buttons">

          <button onClick={handleTextSubmit}>
            Summarize Text
          </button>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button onClick={handleFileSubmit}>
            Summarize PDF
          </button>

        </div>

        <div className="summary-box">

          <h2>Summary</h2>

          {loading ? (
            <p className="loading">⏳ Generating summary...</p>
          ) : (
            <p>
              {summary || "Your summary will appear here..."}
            </p>
          )}

        </div>

      </div>

    </div>
  );
}

export default App;