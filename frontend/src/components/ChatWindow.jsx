import { useState } from "react";
import api from "../services/api";

export default function ChatWindow() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
        role: "assistant",
        content:
    `Welcome to Zoho AI Project Assistant

    Available Commands

    📁 Show projects

    📋 Show tasks for AI SaaS

    ✅ Mark task Build backend as Closed

    🧠 Remember that AI SaaS is my favorite project

    Use the quick action buttons below to get started.`
    }
    ]);
  
  const sendMessage = async () => {

    if (!input.trim()) return;

    const userMessage = {
      role: "user",
      content: input
    };

    setMessages(prev => [...prev, userMessage]);

    const currentInput = input;

    setInput("");
    setLoading(true);

    try {

      const response = await api.post(
        "/chatbot/chat",
        {
          messages: [
            {
              role: "user",
              content: currentInput
            }
          ]
        }
      );

      console.log(response.data);

      let botReply = "No response received";

      if (
        response.data.messages &&
        response.data.messages.length > 0
      ) {
        botReply =
          response.data.messages[
            response.data.messages.length - 1
          ].content;
      }

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: botReply
        }
      ]);
      setLoading(false);

    } catch (error) {

      console.error(error);
      
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content: "Backend connection failed."
        }
      ]);
    } finally {
        setLoading(false);
        }
            
  };

  return (
    <div className="flex-1 flex flex-col">

      <div className="flex-1 p-6 overflow-y-auto">

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-3 p-3 rounded w-fit max-w-3xl ${
              msg.role === "user"
                ? "bg-blue-600 ml-auto"
                :"bg-slate-700 border border-slate-600"
            }`}
          >
            <div className="whitespace-pre-line">
                <div className="whitespace-pre-line">
                    {msg.content}
                    </div>
                </div>
          </div>
        ))}

      </div>

      <div className="p-4 border-t border-slate-700">
        {loading && (
            <div className="mb-3 text-gray-400">
                Assistant is thinking...
            </div>
            )}
        <div className="flex gap-2 mb-3 flex-wrap">

            <button
                onClick={() => setInput("Show projects")}
                className="px-4 py-2 bg-slate-700 rounded-lg hover:bg-slate-600 transition"
            >
                Show Projects
            </button>
            <button
                onClick={() =>
                    setInput(
                    "Remember that AI SaaS is my favorite project"
                    )
                }
                className="px-4 py-2 bg-slate-700 rounded-lg hover:bg-slate-600 transition"
                >
                Memory Demo
                </button>
            <button
                onClick={() => setInput("Show tasks for AI SaaS")}
                className="px-4 py-2 bg-slate-700 rounded-lg hover:bg-slate-600 transition"
            >
                Show Tasks
            </button>

            <button
                onClick={() => setInput("Mark task Build backend as Closed")}
                className="px-4 py-2 bg-slate-700 rounded-lg hover:bg-slate-600 transition"
            >
                Close Task
            </button>

            </div>
        <div className="flex gap-2">

          <input
            value={input}
            onChange={(e) =>
              setInput(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            className="flex-1 p-3 rounded bg-slate-700 outline-none"
            placeholder="Type a message..."
          />

          <button
             onClick={sendMessage}
            disabled={loading}
            className="px-6 bg-blue-600 rounded disabled:opacity-50"
            
            
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}