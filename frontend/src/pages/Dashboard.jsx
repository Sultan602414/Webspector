import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import StatCard from '../components/StatCard';
import mockData from '../data/mockData.json';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  Cell,
  Legend
} from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalTests: mockData.dashboard.stats.total_tests,
    totalIssues: mockData.dashboard.stats.issues_found,
    criticalIssues: mockData.dashboard.stats.critical_issues,
    testsToday: mockData.dashboard.stats.tests_today
  });
  const [recentSessions, setRecentSessions] = useState(mockData.dashboard.recent_sessions);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch('/api/sessions?format=json');
        if (!response.ok) throw new Error('Failed to fetch sessions');
        const data = await response.json();

        const totalTests = data.length;
        if (totalTests > 0) {
          const totalIssues = data.reduce((sum, s) => sum + (s.issue_count || 0), 0);
          const criticalIssues = 0;
          const today = new Date().toISOString().split('T')[0];
          const testsToday = data.filter(s => s.created_at?.startsWith(today)).length;
          setStats({ totalTests, totalIssues, criticalIssues, testsToday });
          setRecentSessions(data.slice(0, 5));
        } else {
          // Keep initial state from mockData
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Fallback already handled by initial state
      } finally {
        setIsLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-surface-container-highest/90 backdrop-blur-xl border border-white/10 p-4 rounded-xl shadow-2xl">
          <p className="text-[10px] font-black uppercase tracking-widest text-on-surface-variant mb-2">{label}</p>
          {payload.map((entry, index) => (
            <div key={index} className="flex items-center gap-3">
              <div className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.color }}></div>
              <span className="text-sm font-bold text-on-surface capitalize">{entry.name}: {entry.value}</span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="grow px-12 py-12 max-w-[1920px] mx-auto w-full animate-fade-in">
      {/* Header Section */}
      <header className="mb-12">
        <p className="text-secondary font-medium tracking-[0.2em] uppercase text-[10px] mb-2">Command Center</p>
        <h1 className="text-5xl md:text-6xl font-extrabold text-on-surface tracking-tight leading-none mb-4 uppercase">Precision Intelligence</h1>
        <div className="h-1 w-24 bg-linear-to-r from-primary to-secondary rounded-full"></div>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        <StatCard icon="analytics" label="Total Tests" value={stats.totalTests} trend="+100%" color="tertiary" />
        <StatCard icon="bug_report" label="Issues Found" value={stats.totalIssues} trend={stats.totalIssues > 0 ? "Action Required" : "Stable"} color="error" />
        <StatCard icon="priority_high" label="Critical Issues" value={stats.criticalIssues} trend="Clear" color="primary" />
        <StatCard icon="today" label="Tests Today" value={stats.testsToday} trend="Active" color="secondary" border />
      </div>

      {/* Analytics Visualization Suite */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
        {/* Analysis Velocity (Wide) */}
        <div className="lg:col-span-8 bg-surface-container-low p-10 rounded-3xl border border-white/2 relative overflow-hidden group">
          <div className="flex justify-between items-start mb-10 relative z-10">
            <div>
              <h3 className="text-xl font-bold text-white mb-1">Analysis Velocity</h3>
              <p className="text-on-surface-variant text-sm">Real-time telemetry stream throughput</p>
            </div>
            <div className="flex gap-2">
              <span className="px-3 py-1 rounded-lg bg-primary/10 text-primary text-[10px] font-black uppercase tracking-widest border border-primary/20">LIVE_FEED</span>
            </div>
          </div>
          <div className="h-[300px] w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockData.dashboard.stats.velocity_data}>
                <defs>
                  <linearGradient id="colorTests" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#c0c1ff" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#c0c1ff" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorIssues" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ffb4ab" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#ffb4ab" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ffffff05" />
                <XAxis
                  dataKey="name"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#c7c4d7', fontSize: 10, fontWeight: 700 }}
                  dy={10}
                />
                <YAxis hide />
                <Tooltip content={<CustomTooltip />} />
                <Area type="monotone" dataKey="tests" stroke="#c0c1ff" strokeWidth={3} fillOpacity={1} fill="url(#colorTests)" />
                <Area type="monotone" dataKey="issues" stroke="#ffb4ab" strokeWidth={3} fillOpacity={1} fill="url(#colorIssues)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Issue Types Breakdown (Right) */}
        <div className="lg:col-span-4 bg-surface-container-low p-10 rounded-3xl border border-white/2 flex flex-col justify-between">
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-1">Issue Index</h3>
            <p className="text-on-surface-variant text-sm">Typology distribution density</p>
          </div>
          <div className="h-[250px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockData.dashboard.stats.issue_distribution}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#ffffff05" />
                <XAxis
                  dataKey="type"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#c7c4d7', fontSize: 10, fontWeight: 700 }}
                />
                <YAxis hide />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'white', opacity: 0.05 }} />
                <Bar dataKey="count" radius={[10, 10, 10, 10]} barSize={32}>
                  {mockData.dashboard.stats.issue_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-8 flex justify-between items-center text-[10px] font-black uppercase tracking-widest text-on-surface-variant">
            <span>Optimized Performance</span>
            <span className="text-secondary">92% Accuracy</span>
          </div>
        </div>
      </div>

      {/* Recent Sessions Table */}
      <section className="mb-12">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h2 className="text-2xl font-bold tracking-tight mb-1">Detailed Logs</h2>
            <p className="text-on-surface-variant text-sm">Reviewing live orchestration stream</p>
          </div>
          <Link to="/sessions" className="bg-surface-container-high hover:bg-surface-bright px-6 py-2.5 rounded-xl text-sm font-bold transition-all duration-300">Expand Repository</Link>
        </div>

        <div className="overflow-hidden rounded-3xl glass-panel border border-white/5">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-container/30">
                <th className="px-8 py-5 text-[10px] uppercase tracking-widest text-on-surface-variant font-black">Website</th>
                <th className="px-8 py-5 text-[10px] uppercase tracking-widest text-on-surface-variant font-black">Status</th>
                <th className="px-8 py-5 text-[10px] uppercase tracking-widest text-on-surface-variant font-black">Analysis</th>
                <th className="px-8 py-5 text-[10px] uppercase tracking-widest text-on-surface-variant font-black">Timestamp</th>
                <th className="px-8 py-5 text-[10px] uppercase tracking-widest text-on-surface-variant font-black text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/2">
              {recentSessions.map((session) => (
                <tr key={session.id} className="hover:bg-white/2 transition-colors group">
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-4">
                      <div className="w-8 h-8 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                        <span className="material-symbols-outlined text-indigo-400 text-sm">language</span>
                      </div>
                      <span className="font-medium text-on-surface">{session.url.replace(/^https?:\/\//, '')}</span>
                    </div>
                  </td>
                  <td className="px-8 py-6">
                    <span className={`px-3 py-1 bg-${session.status === 'completed' ? 'tertiary' : 'error'}/10 text-${session.status === 'completed' ? 'tertiary' : 'error'} text-[10px] font-black uppercase tracking-tighter rounded-full border border-tertiary/20`}>
                      {session.status}
                    </span>
                  </td>
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-1.5">
                      <span className="text-on-surface font-semibold">{session.issue_count || 0}</span>
                      <span className="text-[10px] uppercase font-black tracking-widest text-on-surface-variant">Anomalies</span>
                    </div>
                  </td>
                  <td className="px-8 py-6 text-on-surface-variant text-sm font-mono">
                    {new Date(session.created_at || session.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </td>
                  <td className="px-8 py-6 text-right">
                    <Link to={`/session/${session.id}`} className="p-2 hover:bg-primary/10 rounded-lg text-primary transition-colors inline-block">
                      <span className="material-symbols-outlined">analytics</span>
                    </Link>
                  </td>
                </tr>
              ))}
              {recentSessions.length === 0 && !isLoading && (
                <tr>
                  <td colSpan="5" className="px-8 py-12 text-center text-on-surface-variant italic">No telemetry recorded for this cycle.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
