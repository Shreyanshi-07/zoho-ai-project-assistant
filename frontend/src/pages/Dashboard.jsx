import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

export default function Dashboard() {
  return (
    <div className="h-screen flex flex-col">

      <Header />

      <div className="flex flex-1">
        <Sidebar />
        <ChatWindow />
      </div>

    </div>
  );
}