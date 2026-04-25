import React from 'react';

const TimelineStep = ({ action, index, isLast }) => {
    const hasWarnings = action.llm_analysis?.issues?.length > 0;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 group">
            {/* Timeline Step Sidebar */}
            <div className="lg:col-span-1 flex flex-col items-center py-4">
                <div className="w-10 h-10 rounded-full bg-primary/20 border border-primary/40 flex items-center justify-center text-primary font-bold mb-4 z-10">
                    {index}
                </div>
                {!isLast && <div className="flex-1 w-0.5 bg-gradient-to-b from-primary/40 to-transparent rounded-full -mt-2"></div>}
            </div>

            {/* Main Step Content */}
            <div className="lg:col-span-11 space-y-6">
                {/* Action Header Card */}
                <div className="bg-surface-container-low rounded-3xl p-6 flex flex-wrap items-center justify-between gap-4 border border-outline-variant/10 hover:border-primary/20 transition-all duration-300">
                    <div className="flex items-center gap-6">
                        <div className={`px-4 py-1.5 rounded-full ${hasWarnings ? 'bg-error-container/20 text-error border border-error/20' : 'bg-primary/10 text-primary border border-primary/20'} flex items-center gap-2`}>
                            <span className="material-symbols-outlined text-sm" style={{ fontVariationSettings: "'FILL' 1" }}>
                                {hasWarnings ? 'warning' : 'check_circle'}
                            </span>
                            <span className="text-[10px] font-black tracking-widest uppercase">{hasWarnings ? 'WARNING' : 'SUCCESS'}</span>
                        </div>
                        <div className="flex flex-col">
                            <span className="text-on-surface font-black text-xl uppercase tracking-tight">{action.action_type}</span>
                            <span className="text-on-surface-variant text-[10px] font-mono opacity-70">{new Date(action.timestamp).toLocaleString()}</span>
                        </div>
                    </div>
                    <div className="flex items-center gap-2 bg-surface-container-high px-4 py-2 rounded-xl border border-white/5">
                        <span className="text-primary material-symbols-outlined text-sm">target</span>
                        <span className="text-on-surface-variant font-mono text-sm max-w-[200px] truncate">{action.target_element || 'N/A'}</span>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Before View */}
                    <div className="space-y-3">
                        <h3 className="text-[10px] font-black uppercase tracking-widest text-on-surface-variant px-1 flex items-center gap-2 opacity-60">
                            <span className="material-symbols-outlined text-xs">first_page</span>
                            Before Action
                        </h3>
                        <div className="aspect-video glass-panel rounded-2xl overflow-hidden group/img border border-outline-variant/20 hover:border-primary/30 transition-all">
                            <div className="w-full h-full bg-surface-container relative">
                                <img 
                                    alt="Before Action Screenshot" 
                                    className="w-full h-full object-cover opacity-60 grayscale group-hover/img:grayscale-0 group-hover/img:opacity-100 transition-all duration-700" 
                                    src={action.before_screenshot_path?.startsWith('http') ? action.before_screenshot_path : `/screenshot-file/${action.before_screenshot_path}`} 
                                />
                                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                                    <div className="bg-surface-dim/80 backdrop-blur-md px-4 py-2 rounded-lg border border-outline-variant/30">
                                        <span className="text-[10px] text-on-surface-variant uppercase font-black tracking-widest">Initial State</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* After View */}
                    <div className="space-y-3">
                        <h3 className="text-[10px] font-black uppercase tracking-widest text-on-surface-variant px-1 flex items-center gap-2 opacity-60">
                            <span className="material-symbols-outlined text-xs">last_page</span>
                            After Action
                        </h3>
                        <div className={`aspect-video glass-panel rounded-2xl overflow-hidden group/img border ${hasWarnings ? 'border-error/20 hover:border-error/40' : 'border-tertiary/20 hover:border-tertiary/40'} transition-all`}>
                            <div className="w-full h-full bg-surface-container relative">
                                <img 
                                    alt="After Action Screenshot" 
                                    className="w-full h-full object-cover opacity-60 group-hover/img:opacity-100 transition-all duration-700" 
                                    src={action.after_screenshot_path?.startsWith('http') ? action.after_screenshot_path : `/screenshot-file/${action.after_screenshot_path}`} 
                                />
                                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                                    <div className={`backdrop-blur-md px-4 py-2 rounded-lg border ${hasWarnings ? 'bg-error-container/80 border-error/30' : 'bg-tertiary-container/80 border-tertiary/30'}`}>
                                        <span className={`text-[10px] uppercase font-black tracking-widest ${hasWarnings ? 'text-on-error' : 'text-on-tertiary'}`}>
                                            {hasWarnings ? 'Post-Event Anomaly' : 'Post-Event Analysis'}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* AI Insights Panel */}
                {action.llm_analysis && (
                    <div className="bg-surface-container-high rounded-3xl p-8 relative overflow-hidden border border-white/[0.03] group-hover:border-primary/10 transition-colors">
                        <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
                            <span className="material-symbols-outlined text-8xl">psychology</span>
                        </div>
                        <div className="relative z-10">
                            <div className="flex items-center gap-3 mb-6">
                                <div className="w-8 h-8 rounded-lg bg-tertiary/20 flex items-center justify-center text-tertiary">
                                    <span className="material-symbols-outlined text-sm">bolt</span>
                                </div>
                                <h2 className="text-xl font-bold tracking-tight text-on-surface">LLM Analysis Insights</h2>
                                <div className="ml-auto text-[10px] font-black tracking-[0.2em] uppercase text-on-surface-variant bg-surface-container-highest px-3 py-1 rounded-full">
                                    EXEC_TIME: {action.llm_analysis.elapsed_seconds}s
                                </div>
                            </div>
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                <div className="bg-surface-container-lowest/50 rounded-2xl p-6 border border-outline-variant/10">
                                    <span className="text-[10px] font-bold text-tertiary uppercase tracking-[0.2em] mb-4 block">Action Result</span>
                                    <code className="text-secondary font-mono text-sm leading-relaxed overflow-auto block whitespace-pre-wrap">
                                        {action.llm_analysis.response}
                                    </code>
                                </div>
                                <div className="space-y-4">
                                    {action.llm_analysis.issues.map((issue, i) => (
                                        <div key={i} className="flex items-start gap-4 animate-fade-in" style={{ animationDelay: `${i * 100}ms` }}>
                                            <div className={`mt-1.5 w-1.5 h-1.5 rounded-full shrink-0 ${issue.severity === 'critical' ? 'bg-error shadow-[0_0_8px_rgba(255,180,171,0.8)]' : 'bg-tertiary'}`}></div>
                                            <p className="text-on-surface-variant text-sm leading-relaxed">
                                                {issue.description || issue}
                                            </p>
                                        </div>
                                    ))}
                                    {action.llm_analysis.issues.length === 0 && (
                                        <div className="flex items-start gap-4">
                                            <div className="mt-1.5 w-1.5 h-1.5 rounded-full bg-tertiary shrink-0"></div>
                                            <p className="text-on-surface-variant text-sm leading-relaxed">
                                                No regressions or structural anomalies detected in this transition state.
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default TimelineStep;
