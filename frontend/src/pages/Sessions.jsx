import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import SessionCard from '../components/SessionCard';
import FeatureCard from '../components/FeatureCard';
import mockData from '../data/mockData.json';

const Sessions = () => {
  const [sessions, setSessions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const response = await fetch('/api/sessions?format=json');
        if (!response.ok) throw new Error('Failed to fetch sessions');
        const data = await response.json();
        if (data.length > 0) setSessions(data);
      } catch (error) {
        console.error('Error fetching sessions:', error);
        setSessions(mockData.sessions);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSessions();
  }, []);

  const filteredSessions = sessions.filter(s => 
    s.url.toLowerCase().includes(searchQuery.toLowerCase()) ||
    s.id.toString().includes(searchQuery)
  );

  return (
    <div className="flex-grow p-8 bg-surface">
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-12 gap-6 animate-fade-in">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <div className="h-[2px] w-8 bg-primary"></div>
              <span className="text-[10px] font-bold text-slate-500 tracking-[0.2em] uppercase">ORCHESTRATION OVERVIEW</span>
            </div>
            <h1 className="text-4xl font-bold text-on-surface tracking-tight mb-2">Test Sessions</h1>
            <p className="text-on-surface-variant max-w-md">Real-time surveillance of automated testing pipelines and active deployments.</p>
          </div>
          
          <div className="flex flex-col md:flex-row gap-4 w-full md:w-auto">
            <div className="flex items-center bg-slate-900 rounded-full px-4 py-1.5 border border-outline-variant/10">
              <span className="material-symbols-outlined text-slate-400 text-sm mr-2">search</span>
              <input 
                className="bg-transparent border-none focus:ring-0 text-sm text-on-surface w-48 p-0" 
                placeholder="Search sessions..." 
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <Link to="/run-test" className="bg-gradient-to-r from-primary to-secondary text-on-primary px-8 py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-3 shadow-xl shadow-primary/10 hover:opacity-90 transition-opacity whitespace-nowrap">
              <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>play_arrow</span>
              Run New Test
            </Link>
          </div>
        </div>

        {/* Session Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-12">
          {filteredSessions.map((session) => (
            <SessionCard key={session.id} session={session} />
          ))}
          
          {isLoading && (
            <div className="col-span-full py-20 text-center animate-pulse">
                <span className="material-symbols-outlined text-4xl text-primary animate-spin mb-4">refresh</span>
                <p className="text-on-surface-variant">Synchronizing with Orchestration Layer...</p>
            </div>
          )}
          
          {!isLoading && filteredSessions.length === 0 && (
            <div className="col-span-full py-20 text-center glass-panel rounded-3xl border border-dashed border-white/10">
                <p className="text-on-surface-variant italic">No sessions found matching your criteria.</p>
            </div>
          )}
        </div>

        {/* Bottom Feature Bento */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <FeatureCard icon="query_stats" title="Efficiency Analysis" desc="AI-driven calculation of session overhead and script optimization paths." color="tertiary" />
          <FeatureCard icon="history_edu" title="Recent Logs" desc="Raw streaming data from the most recent 100 interaction events." color="primary" />
          <FeatureCard icon="verified_user" title="Security Shield" desc="Automated pen-testing layers scanning for XSS and injection vulnerabilities." color="secondary" />
        </div>
      </div>
    </div>
  );
};

export default Sessions;
