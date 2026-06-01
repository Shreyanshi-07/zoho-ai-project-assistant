import { useEffect, useState } from "react";
import api from "../services/api";

export default function Sidebar() {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  async function loadProjects() {
    try {
      const response = await api.get("/projects");

      setProjects(
        response.data.projects || []
      );
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <div className="w-72 bg-slate-800 border-r border-slate-700 p-4">

      <h2 className="text-xl font-bold mb-4">
        Projects
      </h2>

      {projects.length === 0 && (
        <div className="text-slate-400 mb-4">
          Loading projects...
        </div>
      )}

      {projects.map((project) => (
        <div
          key={project.id_string}
          onClick={() => {

            setSelectedProject(project.name);

            window.dispatchEvent(
              new CustomEvent(
                "project-selected",
                {
                  detail: project.name,
                }
              )
            );
          }}
          className={`p-3 mb-2 rounded cursor-pointer transition ${
            selectedProject === project.name
              ? "bg-blue-600"
              : "bg-slate-700 hover:bg-slate-600"
          }`}
        >
          {project.name}
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
        <div className="mb-1">✓ Task Creation</div>
        <div className="mb-1">✓ Long-Term Memory</div>
        <div className="mb-1">✓ Human Approval Workflow</div>
      </div>

      <div className="mt-6 text-sm">
        <h3 className="font-bold mb-2">
          System Status
        </h3>

        <div>🟢 Zoho OAuth</div>
        <div>🟢 LangGraph Agent</div>
        <div>🟢 FastAPI Backend</div>
        <div>🟢 Memory Active</div>
        <div>🟢 Human Approval Enabled</div>
      </div>

      <div className="p-4 text-xs text-slate-500 mt-4">
        Zoho AI Project Assistant
        <br />
        Version 2.0
      </div>

    </div>
  );
}
