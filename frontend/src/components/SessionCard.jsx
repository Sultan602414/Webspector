import React from 'react';
import { Link } from 'react-router-dom';

const SessionCard = ({ session }) => {
    const isCompleted = session.status === 'completed';
    const isFailed = session.status === 'failed';
    const isRunning = session.status === 'running' || session.status === 'pending';

    return (
        <div className={`glass-panel rounded-4xl p-8 flex flex-col gap-6 group hover:border-primary/20 transition-all animate-fade-in`}>
            <div className="flex justify-between items-start">
                <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-2xl bg-surface-container-high flex items-center justify-center border border-outline-variant/10">
                        <span className="material-symbols-outlined text-primary text-3xl">
                            {isRunning ? 'terminal' : 'language'}
                        </span>
                    </div>
                    <div className="max-w-[200px] md:max-w-none">
                        <h3 className="text-lg font-bold text-on-surface truncate whitespace-nowrap overflow-hidden text-ellipsis">{session.url.replace(/^https?:\/\//, '')}</h3>
                        <p className="text-slate-500 text-[10px] font-bold uppercase tracking-widest">Session ID: #WS-{session.id}-XP</p>
                    </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                    <div className={`px-3 py-1 rounded-full bg-${isCompleted ? 'secondary' : isFailed ? 'error' : 'tertiary'}/10 border border-${isCompleted ? 'secondary' : isFailed ? 'error' : 'tertiary'}/20 flex items-center gap-2`}>
                        <span className={`w-1.5 h-1.5 rounded-full bg-${isCompleted ? 'secondary' : isFailed ? 'error' : 'tertiary'} ${isRunning ? 'animate-pulse' : ''} shadow-[0_0_8px_rgba(208,188,255,0.8)]`}></span>
                        <span className={`text-[9px] font-black tracking-widest uppercase text-${isCompleted ? 'secondary' : isFailed ? 'error' : 'tertiary'}`}>{session.status}</span>
                    </div>
                    <span className="text-[10px] text-slate-500 italic">{new Date(session.created_at).toLocaleDateString()}</span>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div className="bg-surface-container-lowest/50 rounded-2xl p-4 border border-outline-variant/5">
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1 block">Issues Detected</span>
                    <div className="flex items-end gap-2">
                        <span className={`text-3xl font-bold ${session.issue_count > 0 ? 'text-error' : 'text-on-surface'}`}>{session.issue_count || 0}</span>
                        <span className="text-[10px] text-slate-500 mb-1 font-bold uppercase">Warnings</span>
                    </div>
                </div>
                <div className="bg-surface-container-lowest/50 rounded-2xl p-4 border border-outline-variant/5">
                    <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1 block">Artifacts</span>
                    <div className="flex items-end gap-2">
                        <span className="text-3xl font-bold text-tertiary">{session.screenshot_count || 0}</span>
                        <span className="text-[10px] text-slate-500 mb-1 font-bold uppercase">Captures</span>
                    </div>
                </div>
            </div>

            <Link
                to={`/session/${session.id}`}
                className={`w-full bg-surface-container-high hover:bg-surface-bright py-4 rounded-2xl text-primary font-bold text-sm tracking-wide transition-colors flex items-center justify-center gap-2`}
            >
                {isFailed ? 'Debug Stack Trace' : 'View Detailed Report'}
                <span className="material-symbols-outlined text-sm">{isFailed ? 'bug_report' : 'arrow_forward'}</span>
            </Link>
        </div>
    );
};

export default SessionCard;
