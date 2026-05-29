export default function Header() {
  const clearChat = () => {
    window.location.reload();
  };

  return (
    <div className="h-16 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-6">

      <div>
        <h1 className="text-2xl font-bold">
          Zoho AI Project Assistant
        </h1>

        <p className="text-xs text-slate-400">
          OAuth Authentication • LangGraph Agents • Zoho Projects API
        </p>
      </div>

      <div className="flex gap-2">

        <button
          onClick={clearChat}
          className="px-4 py-2 bg-slate-600 rounded hover:bg-slate-500"
        >
          Refresh
        </button>

        <button
          onClick={() => {
            window.location.href =
              "http://127.0.0.1:8000/api/v1/auth/login";
          }}
          className="px-4 py-2 bg-green-600 rounded hover:bg-green-700"
        >
          Login with Zoho
        </button>

      </div>

    </div>
  );
}