import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-slate-950 w-full py-12 mt-auto flex flex-col md:flex-row justify-between items-center px-12 border-t border-white/5">
      <div className="mb-6 md:mb-0">
        <span className="text-indigo-500 font-bold tracking-tight">WebSpector AI.</span>
        <span className="font-sans text-xs uppercase tracking-widest text-slate-500 ml-2">Precision Orchestration.</span>
      </div>
      <div className="flex gap-8">
        <a className="font-sans text-xs uppercase tracking-widest text-slate-500 hover:text-indigo-200 transition-colors opacity-80 hover:opacity-100" href="#">API Docs</a>
        <a className="font-sans text-xs uppercase tracking-widest text-slate-500 hover:text-indigo-200 transition-colors opacity-80 hover:opacity-100" href="#">System Status</a>
        <a className="font-sans text-xs uppercase tracking-widest text-slate-500 hover:text-indigo-200 transition-colors opacity-80 hover:opacity-100" href="#">Security</a>
        <a className="font-sans text-xs uppercase tracking-widest text-slate-500 hover:text-indigo-200 transition-colors opacity-80 hover:opacity-100" href="#">Support</a>
      </div>
      <div className="mt-6 md:mt-0">
        <p className="font-sans text-xs uppercase tracking-widest text-slate-500">© 2026 WebSpector AI. Precision Orchestration.</p>
      </div>
    </footer>
  );
};

export default Footer;
