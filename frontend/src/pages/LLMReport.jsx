import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import mockData from '../data/mockData.json';

const LLMReport = () => {
    const { id: sessionId } = useParams();
    const navigate = useNavigate();
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchReport = async () => {
            try {
                const response = await fetch(`/api/session/${sessionId}/llm-report?format=json`);
                if (!response.ok) throw new Error('Failed to fetch LLM report');
                const reportData = await response.json();
                if (reportData.quality_score !== undefined && reportData.quality_score > 0) {
                    setData(reportData);
                } else {
                    setData(mockData.llmReport["1"]);
                }
            } catch (error) {
                console.error('Error fetching LLM report:', error);
                setData(mockData.llmReport[sessionId] || mockData.llmReport["1"]);
            } finally {
                setIsLoading(false);
            }
        };

        fetchReport();
    }, [sessionId]);

    if (isLoading) {
        return (
            <div className="grow flex flex-col items-center justify-center space-y-4">
                <span className="material-symbols-outlined text-5xl text-primary animate-pulse">psychology</span>
                <p className="text-on-surface-variant animate-pulse">Synthesizing executive intelligence...</p>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="grow flex flex-col items-center justify-center space-y-4">
                <span className="material-symbols-outlined text-5xl text-error">error</span>
                <p className="text-on-surface-variant">Cognitive report generation failed.</p>
                <button onClick={() => navigate(-1)} className="text-primary hover:underline font-bold uppercase tracking-widest text-xs">Return to Session</button>
            </div>
        );
    }

    // fallback data if some fields are missing from backend
    const report = data.report || data;
    const session = data.session || { url: 'https://example.com' };
    const markdownReport = data.markdown_report || '# No markdown available';

    return (
        <main className="grow pt-12 px-12 pb-16 max-w-[1920px] mx-auto w-full animate-fade-in">
            {/* Header Section */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6">
                <div className="space-y-1">
                    <div className="flex items-center gap-2 text-primary text-xs font-bold tracking-widest uppercase mb-2">
                        <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                        Live Analysis
                    </div>
                    <h1 className="text-4xl font-extrabold tracking-tight text-white">LLM-Generated QA Report</h1>
                    <p className="text-on-surface-variant font-mono text-sm">{session.url}</p>
                </div>
                <div className="flex gap-4">
                    <button onClick={() => navigate(-1)} className="px-6 py-2.5 bg-surface-container-high text-primary rounded-full text-sm font-semibold transition-all hover:bg-surface-bright flex items-center gap-2">
                        <span className="material-symbols-outlined text-sm">arrow_back</span>
                        Back to Session
                    </button>
                    <Link to={`/session/${sessionId}/actions`} className="px-6 py-2.5 bg-linear-to-r from-primary to-secondary text-on-primary rounded-full text-sm font-bold shadow-lg shadow-primary/10 flex items-center gap-2 text-center">
                        View Action Timeline
                        <span className="material-symbols-outlined text-sm">timeline</span>
                    </Link>
                </div>
            </div>

            {/* Executive Summary Bento Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                {/* Quality Score */}
                <div className="md:col-span-1 bg-surface-container-low rounded-3xl p-8 flex flex-col justify-between border border-white/2">
                    <span className="text-[10px] font-black uppercase tracking-widest text-on-surface-variant">Quality Score</span>
                    <div className={`text-7xl font-black tracking-tighter py-4 ${report.quality_score < 50 ? 'text-error' : 'text-primary'}`}>
                        {report.quality_score || 0}
                    </div>
                    <div className={`flex items-center gap-2 text-sm font-bold ${report.quality_score < 50 ? 'text-error' : 'text-primary'}`}>
                        <span className="material-symbols-outlined text-sm">{report.quality_score < 50 ? 'trending_down' : 'trending_up'}</span>
                        {report.quality_score < 50 ? 'Critical Threshold' : 'Optimized State'}
                    </div>
                </div>

                {/* Risk Level */}
                <div className="md:col-span-1 bg-surface-container-low rounded-3xl p-8 flex flex-col justify-between border border-white/2">
                    <span className="text-[10px] font-black uppercase tracking-widest text-on-surface-variant">Risk Level</span>
                    <div className="flex items-center gap-3 py-4">
                        <div className="w-4 h-12 bg-surface-container-highest rounded-full overflow-hidden flex flex-col-reverse">
                            <div className="h-full bg-secondary shadow-[0_0_15px_rgba(208,188,255,0.4)]" style={{ height: report.risk_level === 'HIGH' ? '100%' : report.risk_level === 'MEDIUM' ? '60%' : '30%' }}></div>
                        </div>
                        <span className="text-4xl font-black text-secondary uppercase">{report.risk_level || 'LOW'}</span>
                    </div>
                    <p className="text-[10px] font-bold text-on-surface-variant leading-relaxed opacity-70">System identified volatility in behavioral patterns.</p>
                </div>

                {/* Execution Metrics */}
                <div className="md:col-span-2 bg-surface-container-low rounded-3xl p-8 overflow-hidden relative group border border-white/2">
                    <div className="relative z-10 h-full flex flex-col justify-between">
                        <span className="text-[10px] font-black uppercase tracking-widest text-on-surface-variant">Execution Metrics</span>
                        <div className="flex items-end justify-between mt-4">
                            <div className="space-y-4">
                                <div>
                                    <div className="text-[10px] font-black text-on-surface-variant mb-1 uppercase tracking-widest">Total Actions</div>
                                    <div className="text-5xl font-black">{report.execution_metrics?.total_actions || 0}</div>
                                </div>
                                <div className="flex gap-8">
                                    <div>
                                        <div className="text-[10px] text-tertiary uppercase font-black tracking-tighter">Passed</div>
                                        <div className="text-2xl font-bold">{report.execution_metrics?.passed || 0}</div>
                                    </div>
                                    <div>
                                        <div className="text-[10px] text-error uppercase font-black tracking-tighter">Failed</div>
                                        <div className="text-2xl font-bold">{report.execution_metrics?.failed || 0}</div>
                                    </div>
                                </div>
                            </div>
                            <div className="w-32 h-32 flex items-center justify-center opacity-20">
                                <span className="material-symbols-outlined text-8xl text-primary animate-pulse">analytics</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Test Execution & Issues Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
                {/* Execution Timeline */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="flex justify-between items-center px-2">
                        <h3 className="text-xl font-bold tracking-tight">Test Execution Timeline</h3>
                        <div className="h-px flex-1 mx-6 bg-linear-to-r from-white/5 to-transparent"></div>
                    </div>
                    <div className="space-y-3">
                        {(report.actions || []).map((action, i) => (
                            <div key={i} className="bg-surface-container-low hover:bg-surface-container-high border border-white/2 transition-all p-6 rounded-2xl flex items-center gap-6 group cursor-pointer" onClick={() => navigate(`/session/${sessionId}/actions`)}>
                                <div className="w-12 h-12 rounded-xl bg-surface-container-highest flex items-center justify-center text-on-surface-variant group-hover:text-primary transition-colors">
                                    <span className="text-sm font-mono font-bold">{(i + 1).toString().padStart(2, '0')}</span>
                                </div>
                                <div className="flex-1">
                                    <div className="flex items-center justify-between mb-1">
                                        <h4 className="font-bold tracking-tight text-on-surface uppercase">{action.action}</h4>
                                        <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest flex items-center gap-1 ${action.status === 'WARNING' ? 'bg-error/10 text-error' : 'bg-primary/10 text-primary'}`}>
                                            <span className="material-symbols-outlined text-[10px]" style={{ fontVariationSettings: "'FILL' 1" }}>{action.status === 'WARNING' ? 'warning' : 'check_circle'}</span>
                                            {action.status}
                                        </span>
                                    </div>
                                    <p className="text-xs text-on-surface-variant">{action.summary}</p>
                                </div>
                                <span className="material-symbols-outlined text-on-surface-variant group-hover:translate-x-1 transition-transform">chevron_right</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Issues Found & Recommendations */}
                <div className="space-y-6">
                    {/* Issues Card */}
                    <div className="bg-surface-container-low rounded-3xl p-8 border border-white/2 shadow-2xl shadow-black/20">
                        <div className="flex items-center gap-3 mb-6">
                            <span className="material-symbols-outlined text-secondary">bug_report</span>
                            <h3 className="font-bold tracking-tight">Issues Found</h3>
                        </div>
                        <div className="space-y-4">
                            {(report.issues_found || []).map((issue, i) => (
                                <div key={i} className="p-5 rounded-2xl bg-surface-container-high/50 border-l-4 border-secondary">
                                    <div className="text-[10px] font-black text-secondary mb-2 uppercase tracking-widest">{issue.severity} Severity</div>
                                    <div className="text-sm font-bold mb-1">{issue.title}</div>
                                    <p className="text-[11px] text-on-surface-variant leading-relaxed opacity-80">{issue.description}</p>
                                </div>
                            ))}
                            {(!report.issues_found || report.issues_found.length === 0) && (
                                <p className="text-xs text-on-surface-variant italic">No major issues identified in this cycle.</p>
                            )}
                        </div>
                    </div>

                    {/* Recommendations Card */}
                    <div className="bg-surface-container-low rounded-3xl p-8 border border-white/2">
                        <div className="flex items-center gap-3 mb-4">
                            <span className="material-symbols-outlined text-tertiary">lightbulb</span>
                            <h3 className="font-bold tracking-tight">Recommendations</h3>
                        </div>
                        <ul className="space-y-3 text-sm text-on-surface-variant">
                            {(report.recommendations || []).map((rec, i) => (
                                <li key={i} className="flex gap-3">
                                    <span className="w-1.5 h-1.5 rounded-full bg-tertiary mt-1.5 shrink-0 shadow-[0_0_8px_rgba(137,206,255,0.4)]"></span>
                                    {rec}
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            {/* Full Report Markdown Section */}
            <div className="mt-12">
                <div className="bg-surface-container-lowest rounded-4xl p-8 border-t border-white/5 relative overflow-hidden glass-panel">
                    <div className="flex items-center justify-between mb-8">
                        <div className="flex items-center gap-4">
                            <div className="p-3 rounded-2xl bg-surface-container-low text-primary">
                                <span className="material-symbols-outlined">description</span>
                            </div>
                            <div>
                                <h3 className="text-lg font-bold">Full Report (Markdown)</h3>
                                <p className="text-xs text-on-surface-variant font-medium opacity-60">Raw execution logs and system-generated analysis</p>
                            </div>
                        </div>
                        <button className="p-2 hover:bg-white/5 rounded-lg transition-colors text-on-surface-variant" onClick={() => navigator.clipboard.writeText(markdownReport)}>
                            <span className="material-symbols-outlined">content_copy</span>
                        </button>
                    </div>
                    <div className="bg-black/20 rounded-2xl p-8 font-mono text-sm text-on-surface-variant leading-relaxed border border-white/5 overflow-auto max-h-[500px]">
                        <pre className="whitespace-pre-wrap">{markdownReport}</pre>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default LLMReport;
