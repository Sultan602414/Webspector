import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard' },
    { name: 'Run Test', path: '/run-test' },
    { name: 'Sessions', path: '/sessions' },
  ];

  return (
    <header className="bg-slate-950/80 backdrop-blur-2xl text-indigo-400 font-sans text-sm font-medium tracking-wide docked full-width top-0 sticky z-50 h-20 shadow-[0_8px_30px_rgb(99,102,241,0.04)]">
      <div className="flex justify-between items-center w-full px-12 max-w-[1920px] mx-auto h-full">
        <div className="flex items-center gap-12">
          <Link to="/dashboard" className="text-2xl font-black tracking-tighter bg-linear-to-r from-indigo-300 to-purple-300 bg-clip-text text-transparent">
            WebSpector
          </Link>
          <nav className="hidden md:flex gap-8 relative">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                className={`relative px-1 py-1 transition-colors duration-300 ease-in-out active:scale-[0.98] rounded-lg ${isActive(link.path) ? 'text-indigo-300' : 'text-slate-400 hover:text-indigo-200 hover:bg-indigo-500/5'
                  }`}
                to={link.path}
              >
                {link.name}
                {isActive(link.path) && (
                  <div className="absolute -bottom-1 left-0 right-0 h-0.5 bg-linear-to-r from-indigo-500 to-purple-500 shadow-[0_0_12px_rgba(99,102,241,0.6)]" />
                )}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-4">
            <button className="material-symbols-outlined text-slate-400 hover:text-indigo-200 transition-all">notifications</button>
            <button className="material-symbols-outlined text-slate-400 hover:text-indigo-200 transition-all">settings</button>
          </div>
          <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-indigo-500/20">
            <img alt="User profile" src="/profile.png" onError={(e) => e.target.src = 'https://via.placeholder.com/40'} />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
