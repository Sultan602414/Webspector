import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import SeverityBadge from '../components/SeverityBadge';
import mockData from '../data/mockData.json';

const IssueDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [issue, setIssue] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchIssueDetail = async () => {
            try {
                const response = await fetch(`/api/issue/${id}?format=json`);
                if (!response.ok) throw new Error('Failed to fetch issue details');
                const result = await response.json();
                if (result.id && result.title) {
                    setIssue(result);
                } else {
                    setIssue(mockData.issueDetails["1"]);
                }
            } catch (error) {
                console.error('Error fetching issue details:', error);
                setIssue(mockData.issueDetails[id] || mockData.issueDetails["1"]);
            } finally {
                setIsLoading(false);
            }
        };

        fetchIssueDetail();
    }, [id]);

    if (isLoading) {
        return (
            <div className="grow flex flex-col items-center justify-center space-y-4">
                <span className="material-symbols-outlined text-5xl text-primary animate-spin">refresh</span>
                <p className="text-on-surface-variant animate-pulse">Analyzing anomaly signatures...</p>
            </div>
        );
    }

    if (!issue) {
        return (
            <div className="grow flex flex-col items-center justify-center space-y-4">
                <span className="material-symbols-outlined text-5xl text-error">error</span>
                <p className="text-on-surface-variant">Issue signature corrupted or not found.</p>
                <button onClick={() => navigate(-1)} className="text-primary hover:underline font-bold uppercase tracking-widest text-xs">Return to Session</button>
            </div>
        );
    }

    return (
        <main className="pt-12 px-12 pb-12 max-w-[1920px] mx-auto w-full animate-fade-in">
            {/* Breadcrumb & Back Action */}
            <div className="mb-8 flex items-center justify-between">
                <button onClick={() => navigate(-1)} className="flex items-center gap-2 text-primary font-medium hover:opacity-80 transition-opacity">
                    <span className="material-symbols-outlined text-[20px]">arrow_back</span>
                    <span className="text-sm font-label">Back to Session</span>
                </button>
                <div className="flex gap-2">
                    <span className="px-3 py-1 rounded-full text-[10px] font-bold tracking-widest uppercase bg-surface-container-highest text-on-surface-variant border border-outline-variant/20">ISSUE_ID: #{issue.id}</span>
                </div>
            </div>

            {/* Hero Section: Issue Title & Badges */}
            <div className="grid grid-cols-12 gap-8 mb-12">
                <div className="col-span-12 lg:col-span-8">
                    <div className="flex flex-wrap items-center gap-4 mb-4">
                        <SeverityBadge severity={issue.severity} />
                        <span className="px-4 py-1 rounded-full bg-tertiary-container/30 text-on-tertiary-container text-xs font-bold tracking-wide border border-tertiary-container/20 uppercase">{issue.issue_class}</span>
                        <span className="px-4 py-1 rounded-full bg-surface-container-highest text-on-surface-variant text-xs font-bold tracking-wide border border-outline-variant/20 uppercase">{issue.issue_type}</span>
                    </div>
                    <h1 className="text-5xl font-extrabold tracking-tighter text-on-background mb-6">{issue.title}</h1>
                    <div className="p-8 rounded-3xl glass-panel relative overflow-hidden group">
                        <div className="absolute top-0 left-0 w-1 h-full bg-linear-to-b from-primary to-secondary"></div>
                        <div className="flex items-start gap-4">
                            <span className="material-symbols-outlined text-primary mt-1">info</span>
                            <div>
                                <h3 className="text-sm uppercase tracking-widest text-outline mb-2 font-bold">{issue.issue_type}</h3>
                                <p className="text-xl text-on-surface-variant leading-relaxed">{issue.description}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="col-span-12 lg:col-span-4">
                    <div className="h-full rounded-3xl bg-surface-container-low p-8 flex flex-col justify-center border border-white/2">
                        <div className="mb-8">
                            <p className="text-xs font-bold uppercase tracking-[0.2em] text-outline mb-4">Classification Details</p>
                            <div className="space-y-6">
                                <div className="flex items-center justify-between">
                                    <span className="text-on-surface-variant text-sm">Schema Severity</span>
                                    <span className="text-on-background font-mono text-sm px-2 py-0.5 bg-surface-container-high rounded capitalize">{issue.schema_severity}</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-on-surface-variant text-sm">Recommended Action</span>
                                    <span className="text-primary font-mono text-sm px-2 py-0.5 bg-primary/10 rounded">{issue.recommended_action}</span>
                                </div>
                            </div>
                        </div>
                        <button className="w-full py-4 rounded-xl bg-linear-to-r from-primary to-secondary text-on-primary font-bold tracking-tight hover:brightness-110 transition-all flex items-center justify-center gap-2">
                            <span className="material-symbols-outlined">bolt</span>
                            Execute Fix
                        </button>
                    </div>
                </div>
            </div>

            {/* Detailed Analysis & Technical Data Section */}
            <div className="grid grid-cols-12 gap-8">
                <div className="col-span-12">
                    <div className="mb-4 flex items-center gap-3">
                        <span className="material-symbols-outlined text-tertiary">data_object</span>
                        <h2 className="text-xl font-bold tracking-tight">Detailed Analysis</h2>
                    </div>
                    <div className="rounded-3xl bg-surface-container-lowest border border-outline-variant/10 overflow-hidden shadow-2xl">
                        <div className="flex items-center justify-between px-6 py-4 bg-surface-container">
                            <div className="flex gap-1.5">
                                <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
                                <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                                <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
                            </div>
                            <span className="text-xs font-mono text-outline">payload.json</span>
                        </div>
                        <div className="p-8 code-block text-lg leading-relaxed font-mono">
                            <pre className="text-secondary overflow-auto">
                                {JSON.stringify(issue.structured_report || { issue: issue.title }, null, 4)}
                            </pre>
                        </div>
                    </div>
                </div>

                {/* Visualization / Evidence Placeholder */}
                <div className="col-span-12 lg:col-span-7 h-80 rounded-3xl overflow-hidden relative group border border-white/5">
                    {issue.screenshot?.file_path && (
                        <img className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                            alt="Issue evidence capture"
                            src={issue.screenshot.file_path.startsWith('http') ? issue.screenshot.file_path : `/captures/${issue.screenshot.file_path}`} />
                    )}
                    {!issue.screenshot?.file_path && (
                        <div className="w-full h-full bg-surface-container-high flex items-center justify-center italic text-on-surface-variant">
                            No visual evidence linked to this anomaly.
                        </div>
                    )}
                    <div className="absolute inset-0 bg-linear-to-t from-background via-transparent to-transparent opacity-60"></div>
                    <div className="absolute bottom-6 left-6">
                        <span className="px-3 py-1 rounded-lg bg-black/40 backdrop-blur-md text-[10px] font-bold text-white uppercase tracking-widest border border-white/10">Evidence Capture</span>
                    </div>
                </div>

                <div className="col-span-12 lg:col-span-5 h-80 grid grid-rows-2 gap-8">
                    <div className="rounded-3xl bg-linear-to-br from-surface-container to-surface-container-high p-6 flex items-center gap-6 border border-primary/5">
                        <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                            <span className="material-symbols-outlined text-primary text-3xl">history</span>
                        </div>
                        <div>
                            <p className="text-[10px] font-bold uppercase tracking-widest text-outline mb-1">Occurrence Frequency</p>
                            <p className="text-on-background font-medium text-sm">Recurring {issue.issue_class} patterns detected in active stream.</p>
                            <span className="text-[10px] text-primary/60 font-mono mt-2 block">LATERAL_TELEMETRY: ACTIVE</span>
                        </div>
                    </div>
                    <div className="rounded-3xl bg-linear-to-br from-surface-container to-surface-container-high p-6 flex items-center gap-6 border border-tertiary/5">
                        <div className="h-16 w-16 rounded-full bg-tertiary/10 flex items-center justify-center shrink-0">
                            <span className="material-symbols-outlined text-tertiary text-3xl">hub</span>
                        </div>
                        <div>
                            <p className="text-[10px] font-bold uppercase tracking-widest text-outline mb-1">Impact Radius</p>
                            <p className="text-on-background font-medium text-sm">Affects regional components within the {issue.issue_class} sub-system.</p>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default IssueDetail;
