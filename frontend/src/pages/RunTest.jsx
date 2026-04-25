import React, { useState, useEffect, useRef } from 'react';
import { triggerRun, getSessionStatus } from '../api';
import FeatureCard from '../components/FeatureCard';

const RunTest = () => {
  const [url, setUrl] = useState('');
  const [depth, setDepth] = useState(1);
  const [label, setLabel] = useState('');
  const [viewport, setViewport] = useState('desktop');
  const [isAdvancedOpen, setIsAdvancedOpen] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('Initializing orchestration engine...');
  const [statusSubtext, setStatusSubtext] = useState('Connecting to Ethereal Observer...');
  const [sessionId, setSessionId] = useState(null);
  const [isCompleted, setIsCompleted] = useState(false);
  const [isFailed, setIsFailed] = useState(false);

  const pollInterval = useRef(null);
  const messageInterval = useRef(null);

  const statusMessages = [
    'Launching Ethereal Observer...',
    'Establishing secure socket...',
    'Injecting telemetry scripts...',
    'Capturing visual signatures...',
    'Running neural perception...',
    'Detecting structural anomalies...',
    'Analyzing performance spikes...',
    'Finalizing orchestration report...'
  ];

  const subMessages = [
    'Waking up Playwright instances...',
    'Bypassing CDN layers...',
    'Mapping document object model...',
    'Processing high-fidelity frames...',
    'Inference engine is dreaming...',
    'Comparing against accessibility standards...',
    'Measuring time to first byte...',
    'Compressing data artifacts...'
  ];

  const handleStartAnalysis = async (e) => {
    e.preventDefault();
    setIsRunning(true);
    setProgress(0);
    setIsFailed(false);
    setIsCompleted(false);

    const formData = new FormData();
    formData.append('url', url);
    formData.append('depth', depth);
    formData.append('label', label);
    formData.append('viewport', viewport);

    try {
      const result = await triggerRun(formData);
      setSessionId(result.session_id);
      startPolling(result.session_id);
    } catch (error) {
      console.error('Error starting test:', error);
      alert('Failed to start test: ' + error.message);
      setIsRunning(false);
    }
  };

  const startPolling = (sid) => {
    let messageIndex = 0;

    // Fake progress and messages
    messageInterval.current = setInterval(() => {
      if (messageIndex < statusMessages.length) {
        setStatusText(statusMessages[messageIndex]);
        setStatusSubtext(subMessages[messageIndex]);
        messageIndex++;
        setProgress(prev => Math.min(prev + 10, 90));
      }
    }, 2500);

    // Real polling
    pollInterval.current = setInterval(async () => {
      try {
        const data = await getSessionStatus(sid);
        if (data.session.status === 'completed') {
          clearInterval(pollInterval.current);
          clearInterval(messageInterval.current);
          setIsCompleted(true);
          setProgress(100);
          setStatusText('✓ Analysis Completed!');
          setStatusSubtext(`Identified ${data.session.issue_count || 0} critical architectural insights.`);
        } else if (data.session.status === 'failed') {
          clearInterval(pollInterval.current);
          clearInterval(messageInterval.current);
          setIsFailed(true);
          setStatusText('✗ Orchestration Failed');
          setStatusSubtext('The observer encountered an unexpected termination. See logs.');
        }
      } catch (error) {
        console.error('Error polling status:', error);
      }
    }, 3000);
  };

  useEffect(() => {
    return () => {
      if (pollInterval.current) clearInterval(pollInterval.current);
      if (messageInterval.current) clearInterval(messageInterval.current);
    };
  }, []);

  return (
    <div className="grow flex flex-col items-center justify-center relative px-6 py-20 overflow-hidden">
      {/* Ambient Light Background Elements */}
      <div className="absolute top-1/4 -left-20 w-96 h-96 bg-primary/10 blur-[120px] rounded-full pointer-events-none animate-pulse"></div>
      <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-secondary/10 blur-[120px] rounded-full pointer-events-none animate-pulse delay-700"></div>

      <div className="max-w-4xl w-full z-10 text-center space-y-12">
        {/* Hero Header */}
        <div className="space-y-4 animate-fade-in">
          <span className="text-[10px] uppercase tracking-[0.3em] text-primary/80 font-bold">Orchestration Engine</span>
          <h1 className="text-5xl md:text-7xl font-black tracking-tight text-on-surface leading-tight">Start New QA Analysis</h1>
          <p className="text-on-surface-variant text-lg md:text-xl max-w-2xl mx-auto font-light leading-relaxed">
            Deploy our Ethereal Observer to scan your interface for architectural inconsistencies and performance bottlenecks in real-time.
          </p>
        </div>

        {/* Central Form Container */}
        <div className="glass-panel rounded-4xl p-2 md:p-3 shadow-2xl relative group">
          {/* Inner Glow Effect */}
          <div className="absolute inset-0 rounded-4xl bg-linear-to-br from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none"></div>

          <div className="bg-surface-container rounded-[1.8rem] p-8 md:p-12 space-y-8 relative overflow-hidden">
            {!isRunning || isCompleted || isFailed ? (
              <form onSubmit={handleStartAnalysis} className="w-full space-y-6">
                <div className={`space-y-3 text-left transition-opacity duration-300 ${isRunning ? 'opacity-50 pointer-events-none' : ''}`}>
                  <label className="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold ml-1" htmlFor="url">Target Application Endpoint</label>
                  <div className="relative group/input">
                    <div className="absolute inset-y-0 left-6 flex items-center pointer-events-none text-outline group-focus-within/input:text-primary transition-colors">
                      <span className="material-symbols-outlined">language</span>
                    </div>
                    <input className="w-full bg-surface-container-highest border-none rounded-xl py-6 pl-16 pr-6 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:outline-none transition-all duration-300 text-lg font-medium"
                      id="url" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://your-application.com" type="url" required />
                    <div className="absolute bottom-0 left-0 h-[2px] w-0 bg-linear-to-r from-primary to-secondary group-focus-within/input:w-full transition-all duration-500 rounded-full"></div>
                  </div>
                </div>

                <div className="text-left">
                  <button type="button" onClick={() => setIsAdvancedOpen(!isAdvancedOpen)} className="text-[10px] uppercase tracking-widest text-primary hover:text-secondary font-bold flex items-center gap-2 transition-colors">
                    <span className="material-symbols-outlined text-sm">{isAdvancedOpen ? 'expand_less' : 'expand_more'}</span>
                    Advanced Configuration
                  </button>
                </div>

                {isAdvancedOpen && (
                  <div className="space-y-6 pt-4 border-t border-white/5 text-left animate-slide-down">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-3">
                        <label className="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold">Viewport</label>
                        <div className="flex flex-wrap gap-4">
                          {['desktop', 'tablet', 'mobile'].map((v) => (
                            <label key={v} className="flex items-center gap-2 cursor-pointer group">
                              <input type="radio" checked={viewport === v} onChange={() => setViewport(v)} className="w-4 h-4 bg-surface-container-highest border-none text-primary focus:ring-primary focus:ring-offset-surface-container" />
                              <span className="text-xs text-on-surface-variant group-hover:text-primary transition-colors capitalize">{v}</span>
                            </label>
                          ))}
                        </div>
                      </div>

                      <div className="space-y-3">
                        <label className="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold">Exploration Depth: <span className="text-primary">{depth}</span></label>
                        <input type="range" min="1" max="3" value={depth} onChange={(e) => setDepth(e.target.value)}
                          className="w-full h-2 bg-surface-container-highest rounded-lg appearance-none cursor-pointer accent-primary" />
                        <p className="text-[10px] text-outline italic">Higher depth = more pages explored</p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <label className="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold">Test Label (Optional)</label>
                      <input type="text" value={label} onChange={(e) => setLabel(e.target.value)} className="w-full bg-surface-container-highest border-none rounded-xl py-4 px-6 text-on-surface placeholder:text-outline/50 focus:ring-0 focus:outline-none transition-all duration-300 text-sm font-medium"
                        placeholder="e.g., Homepage redesign test" />
                    </div>
                  </div>
                )}

                {!isRunning && (
                  <button type="submit" className="w-full bg-linear-to-r from-primary to-secondary text-on-primary font-bold py-6 rounded-xl text-lg flex items-center justify-center gap-3 shadow-lg shadow-primary/20 hover:shadow-primary/30 active:scale-[0.99] transition-all duration-300">
                    <span className="material-symbols-outlined">search</span>
                    Start QA Analysis
                  </button>
                )}
              </form>
            ) : null}

            {(isRunning || isCompleted || isFailed) && (
              <div className="space-y-8 animate-fade-in">
                <div className="space-y-4">
                  <div className="flex justify-between items-center text-[10px] uppercase tracking-widest font-bold">
                    <span className="text-on-surface-variant">{isCompleted ? 'Orchestration complete' : 'Analysis in progress'}</span>
                    <span className="text-primary">{progress}%</span>
                  </div>
                  <div className="w-full h-2 bg-surface-container-highest rounded-full overflow-hidden">
                    <div style={{ width: `${progress}%` }} className="h-full bg-linear-to-r from-primary to-secondary transition-all duration-500 ease-out"></div>
                  </div>
                </div>

                <div className="bg-surface-container-highest/50 rounded-2xl p-6 flex items-center gap-6">
                  <div className="relative flex items-center justify-center">
                    <div className={`w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full ${isRunning && !isCompleted && !isFailed ? 'animate-spin' : ''}`}></div>
                    <span className={`material-symbols-outlined absolute text-primary text-xl ${isCompleted ? 'text-tertiary' : ''}`}>
                      {isCompleted ? 'check_circle' : isFailed ? 'error' : 'biotech'}
                    </span>
                  </div>
                  <div className="space-y-1 text-left">
                    <p className={`font-medium ${isCompleted ? 'text-tertiary' : isFailed ? 'text-error' : 'text-on-surface'}`}>{statusText}</p>
                    <p className="text-xs text-outline italic">{statusSubtext}</p>
                  </div>
                </div>

                {isCompleted && (
                  <div className="text-center pt-4 animate-bounce">
                    <a href={`/session/${sessionId}`} className="inline-flex items-center gap-2 text-primary font-bold uppercase tracking-widest text-sm hover:text-secondary transition-colors">
                      View Live Analysis Results
                      <span className="material-symbols-outlined">arrow_forward</span>
                    </a>
                  </div>
                )}

                {isFailed && (
                  <button onClick={() => setIsRunning(false)} className="text-primary font-bold uppercase tracking-widest text-xs hover:underline">Try Again</button>
                )}
              </div>
            )}

            {/* Meta Info Chips */}
            <div className="flex flex-wrap justify-center gap-4 pt-4">
              {['Visual Regression', 'API Integrity', 'Performance Audit'].map((chip, i) => (
                <div key={chip} className="bg-surface-container-highest/50 backdrop-blur px-4 py-2 rounded-full flex items-center gap-2 border border-white/5">
                  <span className={`w-2 h-2 rounded-full ${i === 0 ? 'bg-tertiary' : i === 1 ? 'bg-secondary' : 'bg-primary-container'}`}></span>
                  <span className="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold">{chip}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Feature Highlights */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-12">
          {[
            { icon: 'bolt', title: 'Instant Telemetry', desc: 'Analysis begins milliseconds after injection, providing live stream results.' },
            { icon: 'psychology', title: 'AI Inference', desc: 'Neural patterns identify UX friction points that standard scripts miss.' },
            { icon: 'security', title: 'Secure Sandbox', desc: 'Tests run in isolated, high-compute environments for maximum safety.' }
          ].map((f) => (
            <FeatureCard key={f.title} icon={f.icon} title={f.title} desc={f.desc} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default RunTest;
