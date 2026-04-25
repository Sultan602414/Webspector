import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import DetailStatCard from '../components/DetailStatCard';
import SeverityBadge from '../components/SeverityBadge';
import mockData from '../data/mockData.json';

const SessionDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchSessionDetail = async () => {
            try {
                const response = await fetch(`/api/session/${id}?format=json`);
                if (!response.ok) throw new Error('Failed to fetch session details');
                const result = await response.json();
                if (result.session && (result.issues?.length > 0 || result.screenshots?.length > 0)) {
                    setData(result);
                } else {
                    setData(mockData.sessionDetails["1"]);
                }
            } catch (error) {
                console.error('Error fetching session details:', error);
                setData(mockData.sessionDetails[id] || mockData.sessionDetails["1"]);
            } finally {
                setIsLoading(false);
            }
        };

        fetchSessionDetail();
    }, [id]);

    if (isLoading) {
        return (
            <div className="flex-grow flex flex-col items-center justify-center space-y-4">
                <span className="material-symbols-outlined text-5xl text-primary animate-spin">refresh</span>
                <p className="text-on-surface-variant animate-pulse">Synchronizing with Orchestration Layer...</p>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="flex-grow flex flex-col items-center justify-center space-y-4">
                <span className="material-symbols-outlined text-5xl text-error">error</span>
                <p className="text-on-surface-variant">Session not found or telemetry lost.</p>
                <Link to="/sessions" className="text-primary hover:underline font-bold uppercase tracking-widest text-xs">Back to Sessions</Link>
            </div>
        );
    }

    const { session, screenshots, issues } = data;
    const score = 85; // Placeholder for now or calculate from issues

    return (
        <main className="flex-1 w-full max-w-[1440px] mx-auto px-12 py-10 space-y-10 animate-fade-in">
            {/* Header Section */}
            <section className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                <div className="space-y-2">
                    <div className="flex items-center gap-3">
                        <h1 className="text-4xl font-extrabold tracking-tight text-white">Session #{session.id}</h1>
                        <span className={`px-3 py-1 bg-${session.status === 'completed' ? 'tertiary' : 'error'}/10 text-${session.status === 'completed' ? 'tertiary' : 'error'} text-xs font-bold tracking-widest uppercase rounded-full border border-${session.status === 'completed' ? 'tertiary' : 'error'}/20`}>
                            {session.status}
                        </span>
                    </div>
                    <div className="flex items-center gap-2 text-on-surface-variant font-mono text-sm opacity-80">
                        <span className="material-symbols-outlined text-sm">link</span>
                        {session.url}
                    </div>
                </div>
                <div className="flex gap-4">
                    <Link to={`/session/${session.id}/actions`} className="flex items-center gap-2 px-5 py-2.5 bg-surface-container-high text-primary font-semibold rounded-lg border border-outline-variant/15 hover:bg-surface-bright transition-all duration-300">
                        <span className="material-symbols-outlined">history</span>
                        Action Timeline
                    </Link>
                    <Link to={`/session/${session.id}/llm-report`} className="flex items-center gap-2 px-6 py-2.5 bg-gradient-to-r from-primary to-secondary text-on-primary font-bold rounded-lg shadow-lg hover:opacity-90 transition-all duration-300 active:scale-95 text-center">
                        <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>auto_awesome</span>
                        LLM Report
                    </Link>
                </div>
            </section>

            {/* Stats Grid & Score */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                {/* Score Card */}
                <div className="lg:col-span-8 p-10 bg-surface-container rounded-2xl relative overflow-hidden group">
                    <div className="absolute -top-24 -left-24 w-64 h-64 bg-primary/5 blur-[100px] rounded-full"></div>
                    <div className="relative z-10 space-y-8">
                        <div className="flex justify-between items-end">
                            <div className="space-y-1">
                                <span className="text-xs uppercase tracking-widest text-on-surface-variant font-semibold">Performance Metric</span>
                                <h2 className="text-3xl font-bold text-white">Overall Quality Score</h2>
                            </div>
                            <div className="text-right">
                                <span className="text-6xl font-black tracking-tighter text-primary">{score}<span className="text-2xl text-on-surface-variant font-medium">/100</span></span>
                            </div>
                        </div>
                        <div className="space-y-3">
                            <div className="w-full h-4 bg-surface-container-highest rounded-full overflow-hidden">
                                <div style={{ width: `${score}%` }} className="h-full bg-gradient-to-r from-primary via-tertiary to-secondary rounded-full shadow-[0_0_20px_rgba(192,193,255,0.3)]"></div>
                            </div>
                            <div className="flex justify-between text-xs text-on-surface-variant font-medium">
                                <span>RELIABILITY OPTIMIZED</span>
                                <span>92% ACCURACY TARGET</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Mini Stats */}
                <div className="lg:col-span-4 grid grid-cols-1 gap-4">
                    <DetailStatCard label="Detected Issues" value={issues.length} icon="bug_report" color="primary" />
                    <DetailStatCard label="Critical Failures" value={issues.filter(i => i.severity === 'critical' || i.severity === 'high').length} icon="report" color="error" />
                    <DetailStatCard label="Screenshots" value={screenshots.length} icon="photo_library" color="tertiary" />
                </div>
            </div>

            {/* Detected Issues Section */}
            <section className="space-y-6">
                <div className="flex items-center gap-4">
                    <h3 className="text-2xl font-bold text-white tracking-tight">Detected Issues</h3>
                    <div className="h-[1px] flex-1 bg-outline-variant/10"></div>
                </div>
                <div className="overflow-hidden rounded-2xl bg-surface-container border border-outline-variant/5">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-surface-container-high/50 text-[10px] text-on-surface-variant uppercase tracking-widest border-b border-outline-variant/10">
                                <th className="px-8 py-5 font-bold">Severity</th>
                                <th className="px-8 py-5 font-bold">Type</th>
                                <th className="px-8 py-5 font-bold">Details</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-outline-variant/10">
                            {issues.map((issue) => (
                                <tr
                                    key={issue.id}
                                    onClick={() => navigate(`/issue/${issue.id}`)}
                                    className="hover:bg-surface-bright/30 transition-colors group cursor-pointer"
                                >
                                    <td className="px-8 py-6">
                                        <SeverityBadge severity={issue.severity} />
                                    </td>
                                    <td className="px-8 py-6 text-on-surface font-semibold">{issue.issue_type}</td>
                                    <td className="px-8 py-6 text-on-surface-variant flex justify-between items-center">
                                        {issue.description}
                                        <span className="material-symbols-outlined text-primary opacity-0 group-hover:opacity-100 transition-opacity text-sm">arrow_forward</span>
                                    </td>
                                </tr>
                            ))}
                            {issues.length === 0 && (
                                <tr>
                                    <td colSpan="3" className="px-8 py-12 text-center text-on-surface-variant italic">No issues detected in this session.</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </section>

            {/* Screenshots Gallery */}
            <section className="space-y-6">
                <div className="flex justify-between items-center">
                    <h3 className="text-2xl font-bold text-white tracking-tight">Screenshots Gallery</h3>
                    <button className="text-primary text-sm font-bold flex items-center gap-1 hover:underline">
                        Download All <span className="material-symbols-outlined text-base">download</span>
                    </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {screenshots.map((shot) => {
                        const path = shot.screenshot_path || shot.file_path || '';
                        return (
                            <div key={shot.id} className="group relative aspect-video bg-surface-container rounded-xl overflow-hidden cursor-zoom-in border border-outline-variant/5">
                                <img className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                                    alt={shot.alt_text || 'Screenshot artifact'}
                                    src={path.startsWith('http') ? path : `/captures/${path}`} />
                                <div className="absolute inset-0 bg-linear-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
                                    <span className="text-white text-[10px] font-bold uppercase tracking-widest">{shot.timestamp || shot.captured_at ? new Date(shot.timestamp || shot.captured_at).toLocaleTimeString() : 'Static Capture'}</span>
                                </div>
                            </div>
                        )
                    })}
                    {screenshots.length === 0 && (
                        <div className="col-span-full py-20 text-center glass-panel rounded-xl border border-dashed border-white/10">
                            <p className="text-on-surface-variant italic">No visual artifacts captured for this session.</p>
                        </div>
                    )}
                </div>
            </section>
        </main>
    );
};

export default SessionDetail;
