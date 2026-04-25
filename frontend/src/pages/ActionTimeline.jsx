import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import TimelineStep from '../components/TimelineStep';
import mockData from '../data/mockData.json';

const ActionTimeline = () => {
    const { id: sessionId } = useParams();
    const navigate = useNavigate();
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchActions = async () => {
            try {
                const response = await fetch(`/api/session/${sessionId}/actions?format=json`);
                if (!response.ok) throw new Error('Failed to fetch action timeline');
                const result = await response.json();
                if (result.actions && result.actions.length > 0) {
                    setData(result);
                } else {
                    setData(mockData.actionTimeline["1"]);
                }
            } catch (error) {
                console.error('Error fetching actions:', error);
                setData(mockData.actionTimeline[sessionId] || mockData.actionTimeline["1"]);
            } finally {
                setIsLoading(false);
            }
        };

        fetchActions();
    }, [sessionId]);

    if (isLoading) {
        return (
            <div className="grow flex flex-col items-center justify-center space-y-4">
                <span className="material-symbols-outlined text-5xl text-primary animate-spin">refresh</span>
                <p className="text-on-surface-variant animate-pulse">Reconstructing execution sequence...</p>
            </div>
        );
    }

    if (!data || !data.actions) {
        return (
            <div className="grow flex flex-col items-center justify-center space-y-4">
                <span className="material-symbols-outlined text-5xl text-error">error</span>
                <p className="text-on-surface-variant">Timeline data missing or session expired.</p>
                <button onClick={() => navigate(-1)} className="text-primary hover:underline font-bold uppercase tracking-widest text-xs">Return to Session</button>
            </div>
        );
    }

    return (
        <main className="p-12 min-h-screen bg-surface w-full max-w-[1920px] mx-auto animate-fade-in">
            <div className="max-w-7xl mx-auto">
                {/* Header Section */}
                <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
                    <div>
                        <div className="flex items-center gap-2 text-primary mb-2">
                            <span className="material-symbols-outlined text-sm">precision_manufacturing</span>
                            <span className="text-xs font-bold tracking-widest uppercase">Session Audit</span>
                        </div>
                        <h1 className="text-4xl font-extrabold tracking-tight text-on-surface mb-2">Action Timeline</h1>
                        <div className="flex items-center gap-4 text-on-surface-variant text-sm">
                            <div className="flex items-center gap-1">
                                <span className="material-symbols-outlined text-xs">link</span>
                                <span>Session #{sessionId}</span>
                            </div>
                            <div className="w-1 h-1 rounded-full bg-outline-variant"></div>
                            <div className="flex items-center gap-1">
                                <span className="material-symbols-outlined text-xs">list_alt</span>
                                <span>Total Actions: {data.actions.length}</span>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        <button onClick={() => navigate(-1)} className="px-6 py-2.5 rounded-full border border-outline-variant/30 text-primary font-semibold text-sm hover:bg-surface-container-high transition-all">
                            Back to Session
                        </button>
                        <Link to={`/session/${sessionId}/llm-report`} className="px-6 py-2.5 rounded-full bg-linear-to-r from-primary to-secondary text-on-primary font-bold text-sm shadow-xl shadow-primary/10 hover:brightness-110 transition-all text-center">
                            View LLM Report
                        </Link>
                    </div>
                </div>

                {/* Timeline Grid */}
                <div className="space-y-12">
                    {data.actions.map((action, index) => (
                        <TimelineStep key={action.id} action={action} index={index + 1} isLast={index === data.actions.length - 1} />
                    ))}
                    {data.actions.length === 0 && (
                        <div className="py-20 text-center glass-panel rounded-3xl border border-dashed border-white/10">
                            <p className="text-on-surface-variant italic">No interaction events recorded for this session.</p>
                        </div>
                    )}
                </div>

                {/* Footer Pagination Placeholder */}
                <div className="mt-12 pt-8 border-t border-outline-variant/10 flex justify-between items-center text-on-surface-variant">
                    <button className="flex items-center gap-2 text-sm hover:text-primary transition-colors disabled:opacity-30" disabled>
                        <span className="material-symbols-outlined">arrow_back</span>
                        Previous
                    </button>
                    <div className="flex gap-2">
                        <span className="w-8 h-8 rounded-lg bg-primary text-on-primary flex items-center justify-center text-xs font-bold">1</span>
                    </div>
                    <button className="flex items-center gap-2 text-sm hover:text-primary transition-colors disabled:opacity-30" disabled>
                        Next
                        <span className="material-symbols-outlined">arrow_forward</span>
                    </button>
                </div>
            </div>
        </main>
    );
};

export default ActionTimeline;
