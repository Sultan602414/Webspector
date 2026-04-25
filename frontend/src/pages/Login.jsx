import React from 'react';
import LoginForm from '../components/LoginForm';

const Login = () => {
  return (
    <div className="bg-background text-on-background selection:bg-primary/30 min-h-screen py-10 md:py-0 flex flex-col md:flex-row relative">
      {/* Ambient Light Effects */}
      <div className="absolute top-1/2 left-1/4 -translate-x-1/2 -translate-y-1/2 w-full h-full pointer-events-none z-0">
        <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-primary/5 blur-[120px] rounded-full animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-secondary/5 blur-[120px] rounded-full animate-pulse delay-700"></div>
      </div>

      {/* Left Column: Branding, Welcome, Orbital */}
      <section className="w-full md:w-5/12 p-12 md:p-20 flex flex-col justify-between relative z-10 border-r border-outline-variant/10 bg-surface/30 backdrop-blur-sm">
        {/* Branding */}
        <div className="flex items-center mb-8 md:mb-0">
          <span className="text-4xl font-black tracking-tighter bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent">WebSpector</span>
        </div>

        {/* Welcome Section */}
        <div className="space-y-6 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            <span className="text-[10px] uppercase tracking-widest font-bold text-primary">System Ready</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-black tracking-tight leading-tight text-on-surface">
            Welcome <br /> 
            <span className="text-transparent bg-clip-text bg-linear-to-r from-primary to-secondary">Back.</span>
          </h1>
          <p className="text-xl text-on-surface-variant leading-relaxed max-w-sm">
            Resuming cinematic orchestration and QA telemetry for your connected applications.
          </p>
        </div>

        {/* Orbital Block (Status) */}
        <div className="flex flex-col gap-4 animate-fade-in opacity-60">
          <div className="h-px bg-linear-to-r from-outline-variant/50 to-transparent w-full"></div>
          <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-[10px] uppercase font-black tracking-[0.2em] text-on-surface-variant">
            <span className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-primary"></span>
              Operational
            </span>
            <span>v2.0.4-Orbital</span>
            <span>Neural Encryption</span>
          </div>
        </div>
      </section>

      {/* Right Column: Form */}
      <section className="w-full md:w-7/12 flex items-center justify-center p-8 md:p-12 relative z-10">
        <main className="w-full max-w-lg animate-fade-in">
          <div className="glass-panel rounded-[2.5rem] p-1 border border-white/5 shadow-3xl">
            <div className="bg-surface-container rounded-[2.4rem] p-8 md:p-12 relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1.5 h-full bg-linear-to-b from-primary to-secondary opacity-50"></div>
              <LoginForm />
            </div>
          </div>
        </main>
      </section>
    </div>
  );
};

export default Login;
