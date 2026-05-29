export default function Sidebar() {
  const projects = [
    "AI SaaS",
    "TEST PROJECT"
  ];

  return (
    <div className="w-72 bg-slate-800 border-r border-slate-700 p-4">
      <h2 className="text-xl font-bold mb-4">
        Projects
      </h2>

      {projects.map((project) => (
        <div
          key={project}
          className="p-3 mb-2 rounded bg-slate-700 cursor-pointer hover:bg-slate-600"
        >
          {project}
        </div>
      ))}

      <div className="mt-6 text-sm">
        <h3 className="font-bold mb-2">
          Features
        </h3>

        <div className="mb-1">✓ OAuth Login</div>
        <div className="mb-1">✓ Project Listing</div>
        <div className="mb-1">✓ Task Listing</div>
        <div className="mb-1">✓ Task Updates</div>
        <div className="mb-1">✓ Long-Term Memory</div>
      </div>

      {/* ADD THIS SECTION */}
      <div className="mt-6 text-sm">
        <h3 className="font-bold mb-2">
          System Status
        </h3>

        <div>🟢 Zoho OAuth</div>
        <div>🟢 LangGraph Agent</div>
        <div>🟢 FastAPI Backend</div>
        <div>🟢 Memory Active</div>
      </div>

      <div className="p-4 text-xs text-slate-500 mt-4">
        Zoho AI Project Assistant
        <br />
        Version 1.0
      </div>
    </div>
  );
}