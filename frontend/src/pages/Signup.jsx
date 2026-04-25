import React from 'react';
import SignupForm from '../components/SignupForm';

const Signup = () => {
  return (
    <div className="bg-background text-on-background selection:bg-primary/30 min-h-screen flex flex-col items-center justify-center p-4">
      {/* Brand Header */}
      <header className="fixed top-8 left-0 w-full flex justify-center z-50 pointer-events-none">
        <div className="flex items-center">
          <span className="text-3xl font-black tracking-tighter bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent">WebSpector</span>
        </div>
      </header>

      {/* Main Sign Up Canvas */}
      <main className="w-full max-w-6xl mt-20 mb-12 flex flex-col md:flex-row gap-0 overflow-hidden rounded-xl shadow-2xl bg-surface-container-low animate-fade-in">
        {/* Left Section: Editorial/Benefits */}
        <section className="w-full md:w-5/12 p-8 md:p-12 relative flex flex-col justify-between overflow-hidden">
          <div className="absolute inset-0 z-0">
            <div className="absolute inset-0 bg-linear-to-b from-primary/10 to-background/90"></div>
            <img 
              alt="Cinematic data visualization" 
              className="w-full h-full object-cover opacity-30 grayscale" 
              src="https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=2000&auto=format&fit=crop" 
            />
          </div>
          
          <div className="relative z-10 space-y-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
              <span className="text-[10px] uppercase tracking-widest font-bold text-primary">Vigilant Intelligence</span>
            </div>
            
            <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight leading-tight">
              Transcend the standard <span className="text-transparent bg-clip-text bg-linear-to-r from-primary to-secondary">QA cycle.</span>
            </h1>
            
            <div className="space-y-6">
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center flex-shrink-0">
                  <span className="material-symbols-outlined text-primary">groups</span>
                </div>
                <div>
                  <p className="font-semibold text-on-surface">Join 5000+ teams</p>
                  <p className="text-sm text-on-surface-variant">Powering the next generation of resilient engineering workflows.</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center flex-shrink-0">
                  <span className="material-symbols-outlined text-primary">bolt</span>
                </div>
                <div>
                  <p className="font-semibold text-on-surface">Instant QA insights</p>
                  <p className="text-sm text-on-surface-variant">Real-time deep-scan technology that surfaces bugs before they deploy.</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <div className="w-10 h-10 rounded bg-surface-container-high flex items-center justify-center flex-shrink-0">
                  <span className="material-symbols-outlined text-primary">visibility</span>
                </div>
                <div>
                  <p className="font-semibold text-on-surface">WebSpector Core</p>
                  <p className="text-sm text-on-surface-variant">Proprietary AI vision model built for semantic code auditing.</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="relative z-10 pt-12">
            <div className="glass-panel p-6 rounded-lg border border-outline-variant/30">
              <p className="text-xs italic text-on-surface-variant mb-4">"The precision of WebSpector has completely redefined our release velocity. It's like having a hundred QA engineers watching every line of code simultaneously."</p>
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-surface-bright"></div>
                <div>
                  <p className="text-xs font-bold text-on-surface">Marcus Thorne</p>
                  <p className="text-[10px] text-primary">CTO, Veridian Systems</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Right Section: Sign Up Form */}
        <section className="w-full md:w-7/12 bg-surface-container p-8 md:p-16 flex flex-col justify-center">
          <SignupForm />
        </section>
      </main>
    </div>
  );
};

export default Signup;
