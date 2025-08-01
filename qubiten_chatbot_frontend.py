import React, { useState, useRef, useEffect } from 'react';

// Using lucide-react for clean, modern icons.
// In a real project, you would install this with: npm install lucide-react
// For this self-contained example, we'll use SVG paths directly.

const IconSend = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="m22 2-7 20-4-9-9-4Z" />
    <path d="M22 2 11 13" />
  </svg>
);

const IconPaperclip = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    {...props}
  >
    <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.59a2 2 0 0 1-2.83-2.83l8.49-8.48" />
  </svg>
);

const IconX = (props) => (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
);


// Main App Component
function App() {
  // State Management
  const [messages, setMessages] = useState([
    {
      id: 'init',
      text: "Hello! I'm the Qubiten Compliance Services assistant. How can I help you today? You can ask me questions about our services or upload a file for analysis.",
      sender: 'bot',
      files: [],
    },
  ]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // Refs for DOM elements
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  // API Configuration
  // Based on your python snippet, api_name="/chat" translates to the /run/chat endpoint.
  const API_URL = "https://genai-app-qubitencompanychatbot-1-1754054984005-797989844029.us-central1.run.app/run/chat";

  // Automatically scroll to the latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Helper function to convert a file to a Base64 data URL
  const fileToDataURL = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
      reader.readAsDataURL(file);
    });
  };

  // Handle sending a message
  const handleSend = async () => {
    if ((!input.trim() && !file) || isLoading) return;

    setIsLoading(true);
    
    // 1. Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      text: input,
      sender: 'user',
      files: file ? [file.name] : [],
    };
    setMessages((prev) => [...prev, userMessage]);
    
    // 2. Prepare the message object for the Gradio API
    let messageObject = {
      text: input,
      files: [],
    };

    if (file) {
      try {
        const dataUrl = await fileToDataURL(file);
        messageObject.files.push({
          name: file.name,
          data: dataUrl,
          is_file: true // Gradio client often sends this flag
        });
      } catch (error) {
        console.error("Error reading file:", error);
        setMessages((prev) => [...prev, {
            id: 'error-file-' + Date.now(),
            text: "Sorry, there was an error processing the file you uploaded.",
            sender: 'bot',
            files: []
        }]);
        setIsLoading(false);
        return;
      }
    }

    // 3. Clear inputs
    setInput('');
    setFile(null);

    // 4. Call the API
    try {
      // Gradio API expects the payload to be wrapped in a 'data' array.
      const apiPayload = {
          data: [messageObject]
      };

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(apiPayload),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const result = await response.json();
      
      // The bot's response is inside the 'data' array of the result object.
      const botText = result.data && result.data.length > 0 ? result.data[0] : "Sorry, I received an empty response.";
      
      const botResponse = {
        id: Date.now() + 1,
        text: botText,
        sender: 'bot',
        files: [],
      };
      setMessages((prev) => [...prev, botResponse]);

    } catch (error) {
      console.error("Failed to fetch from Gradio API:", error);
      const errorResponse = {
        id: 'error-api-' + Date.now(),
        text: "I'm sorry, but I couldn't connect to my knowledge base. Please check the API endpoint or try again later.",
        sender: 'bot',
        files: [],
      };
      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Handle file selection
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  // Handle key press for sending message
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="font-sans bg-gray-900 text-white flex flex-col h-screen">
      {/* Header */}
      <header className="bg-gray-800/50 backdrop-blur-sm border-b border-gray-700 p-4 shadow-md">
        <h1 className="text-xl font-bold text-center text-gray-200">Qubiten Compliance AI Assistant</h1>
      </header>

      {/* Chat Window */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
        {messages.map((msg, index) => (
          <div key={msg.id || index} className={`flex items-end gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            {/* Bot Avatar */}
            {msg.sender === 'bot' && (
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex-shrink-0"></div>
            )}

            {/* Message Bubble */}
            <div className={`max-w-xl rounded-2xl px-4 py-3 shadow-lg ${
                msg.sender === 'user'
                  ? 'bg-blue-600 rounded-br-none'
                  : 'bg-gray-700 rounded-bl-none'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
              {msg.files && msg.files.length > 0 && (
                <div className="mt-2 text-xs text-gray-300 bg-gray-600/50 px-2 py-1 rounded-md">
                  Attachment: {msg.files[0]}
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex items-end gap-3 justify-start">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex-shrink-0"></div>
            <div className="max-w-xl rounded-2xl px-4 py-3 shadow-lg bg-gray-700 rounded-bl-none">
              <div className="flex items-center justify-center space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse [animation-delay:-0.3s]"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse [animation-delay:-0.15s]"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </main>

      {/* Input Area */}
      <footer className="bg-gray-800/70 backdrop-blur-sm border-t border-gray-700 p-4">
        <div className="max-w-3xl mx-auto bg-gray-900 rounded-xl p-2 flex items-center gap-2 border border-gray-600 focus-within:border-blue-500 transition-all duration-300">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
            accept="image/*,application/pdf,.csv,.txt,.md"
          />
          <button
            onClick={() => fileInputRef.current.click()}
            className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-full transition-colors"
            aria-label="Attach file"
          >
            <IconPaperclip className="w-5 h-5" />
          </button>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question or describe the file..."
            className="flex-1 bg-transparent text-gray-200 placeholder-gray-500 focus:outline-none resize-none max-h-32"
            rows="1"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || (!input.trim() && !file)}
            className="p-2 rounded-full bg-blue-600 text-white disabled:bg-gray-600 disabled:cursor-not-allowed hover:bg-blue-500 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-gray-900"
            aria-label="Send message"
          >
            <IconSend className="w-5 h-5" />
          </button>
        </div>
        {file && (
            <div className="max-w-3xl mx-auto mt-2">
                <div className="bg-gray-700/50 text-xs text-gray-300 px-3 py-1 rounded-full inline-flex items-center gap-2">
                    <span>{file.name}</span>
                    <button onClick={() => setFile(null)} className="text-gray-400 hover:text-white">
                        <IconX />
                    </button>
                </div>
            </div>
        )}
      </footer>
    </div>
  );
}

export default App;
