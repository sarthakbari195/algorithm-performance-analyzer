import React from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink, useLocation } from 'react-router-dom';
import { LayoutDashboard, History, Activity, Terminal, Cpu } from 'lucide-react';
import { Toaster } from 'react-hot-toast';
import { clsx } from 'clsx';

// Components
import Dashboard from './pages/Dashboard';
import HistoryPage from './pages/History';

const NavItem = ({ to, icon: Icon, children }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <NavLink
      to={to}
      className={clsx(
        "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 group text-sm font-medium",
        isActive
          ? "bg-indigo-600/10 text-indigo-400"
          : "text-gray-400 hover:bg-gray-800 hover:text-white"
      )}
    >
      <Icon size={20} className={clsx(isActive ? "text-indigo-500" : "text-gray-500 group-hover:text-white")} />
      <span>{children}</span>
      {isActive && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.6)]" />}
    </NavLink>
  );
};

const Sidebar = () => (
  <aside className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col fixed h-full z-20 hidden md:flex">
    <div className="p-6 border-b border-gray-800">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <Activity className="text-white" size={20} />
        </div>
        <div>
          <h1 className="font-bold text-white text-lg leading-tight tracking-tight">AlgoPerf</h1>
          <p className="text-[10px] font-black text-indigo-400 uppercase tracking-widest">Analyzer Pro</p>
        </div>
      </div>
    </div>

    <nav className="flex-1 p-4 space-y-2">
      <NavItem to="/" icon={LayoutDashboard}>Dashboard</NavItem>
      <NavItem to="/history" icon={History}>History</NavItem>
    </nav>

    <div className="p-4 border-t border-gray-800">
      <div className="bg-gray-800/50 rounded-2xl p-4 border border-gray-700/50">
        <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2">Engine Engine</p>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.5)]"></div>
          <span className="text-xs text-emerald-400 font-bold">RESEARCH_READY</span>
        </div>
      </div>
    </div>
  </aside>
);

const MobileNav = () => (
  <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-gray-900 border-t border-gray-800 p-2 flex justify-around z-50">
    <NavLink to="/" className={({ isActive }) => clsx("flex flex-col items-center p-2 gap-1 rounded-lg", isActive ? "text-indigo-400" : "text-gray-500")}>
      <LayoutDashboard size={22} />
      <span className="text-[10px] font-bold">Dash</span>
    </NavLink>
    <NavLink to="/history" className={({ isActive }) => clsx("flex flex-col items-center p-2 gap-1 rounded-lg", isActive ? "text-indigo-400" : "text-gray-500")}>
      <History size={22} />
      <span className="text-[10px] font-bold">History</span>
    </NavLink>
  </nav>
);

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#0b0c10] text-gray-100 font-sans selection:bg-indigo-500/30">
        <Sidebar />
        <MobileNav />
        <main className="md:ml-64 min-h-screen">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
        <Toaster position="top-right" toastOptions={{
          style: {
            background: '#111827',
            color: '#fff',
            border: '1px solid #374151',
            borderRadius: '12px'
          }
        }} />
      </div>
    </Router>
  );
}

export default App;
