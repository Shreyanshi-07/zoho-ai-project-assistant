export default function Sidebar() {
  const projects = [
    "AI SaaS",
    "Demo Project",
    "Testing Project"
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

      <div className="p-4 text-xs text-slate-500 mt-4">
        Zoho AI Project Assistant
        <br />
        Version 1.0
      </div>
    </div>
  );
}