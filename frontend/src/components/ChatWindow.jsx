import { useState } from "react";
import api from "../services/api";

export default function ChatWindow() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
        role: "assistant",
        content:
        "Welcome to Zoho AI Project Assistant\n\nTry:\n• Show projects\n• Show tasks for AI SaaS\n• Mark task Build backend as Closed"
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
        response.data.messages.length > 1
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
      setLoading(false);
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
            className={`mb-3 p-3 rounded w-fit max-w-xl ${
              msg.role === "user"
                ? "bg-blue-600 ml-auto"
                : "bg-slate-700"
            }`}
          >
            <div className="whitespace-pre-line">
                {msg.content}
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
                className="px-3 py-1 bg-slate-700 rounded"
            >
                Show Projects
            </button>

            <button
                onClick={() => setInput("Show tasks for AI SaaS")}
                className="px-3 py-1 bg-slate-700 rounded"
            >
                Show Tasks
            </button>

            <button
                onClick={() => setInput("Mark task Build backend as Closed")}
                className="px-3 py-1 bg-slate-700 rounded"
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
            className="px-6 bg-blue-600 rounded"
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}