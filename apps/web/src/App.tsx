import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { ShieldCheck, Activity, Database, Users, TrendingUp, BarChart4, Settings, LayoutDashboard, Globe, Zap, Box, AlertTriangle, Eye, Clock, ListChecks } from 'lucide-react';
import Dashboard from './pages/Dashboard';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
        {/* Navigation Sidebar */}
        <aside className="w-72 bg-slate-900/40 backdrop-blur-3xl border-r border-slate-800 flex flex-col p-8 fixed h-full shadow-2xl">
          <div className="flex items-center gap-4 mb-12">
            <div className="w-12 h-12 bg-sky-600 rounded-2xl flex items-center justify-center font-bold text-2xl shadow-xl shadow-sky-900/20 text-white">
               <Eye size={28} />
            </div>
            <span className="text-xl font-black tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">Reliability IQ</span>
          </div>
          
          <nav className="flex-1 space-y-2">
            <NavItem to="/" icon={<LayoutDashboard size={20} />} label="Executive Summary" active />
            <NavItem to="/pipelines" icon={<Activity size={20} />} label="Pipeline Health" />
            <NavItem to="/incidents" icon={<AlertTriangle size={20} />} label="Incident Center" />
            <NavItem to="/freshness" icon={<Clock size={20} />} label="Freshness SLAs" />
            <NavItem to="/quality" icon={<ListChecks size={20} />} label="Quality Scores" />
            <NavItem to="/anomalies" icon={<TrendingUp size={20} />} label="Anomaly Explorer" />
            <NavItem to="/lineage" icon={<Box size={20} />} label="Impact Radius" />
          </nav>

          <div className="pt-6 border-t border-slate-800">
            <NavItem to="/settings" icon={<Settings size={20} />} label="Platform Settings" />
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 ml-72">
          <header className="h-20 border-b border-slate-800 flex items-center justify-between px-10 bg-slate-950/50 backdrop-blur-md sticky top-0 z-10">
            <div className="flex items-center gap-2 text-slate-400 text-sm font-medium uppercase tracking-widest">
              <span>Enterprise Reliability</span>
              <span>/</span>
              <span className="text-white font-bold">Observability Control Plane</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-bold text-white">Data SRE Lead</p>
                <p className="text-[10px] text-sky-400 uppercase tracking-widest font-black">Pipeline Observatory</p>
              </div>
              <div className="w-10 h-10 bg-slate-800 rounded-full border border-slate-700 flex items-center justify-center font-bold text-slate-300">RS</div>
            </div>
          </header>

          <div className="p-10 max-w-7xl mx-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
            </Routes>
          </div>
        </main>
      </div>
    </BrowserRouter>
  );
};

const NavItem = ({ to, icon, label, active }: any) => (
  <Link 
    to={to} 
    className={`flex items-center gap-4 px-4 py-4 rounded-2xl transition-all duration-300 group ${active ? 'bg-sky-600/10 text-sky-400 border border-sky-500/10 shadow-lg shadow-sky-950/50' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`}
  >
    <span className={`${active ? 'text-sky-400' : 'group-hover:text-sky-400 transition transform group-hover:scale-110'}`}>{icon}</span>
    <span className="font-bold text-sm tracking-tight">{label}</span>
  </Link>
);

export default App;
