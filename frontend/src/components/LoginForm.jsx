import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <div className="max-w-md mx-auto w-full">

      <form className="space-y-6" onSubmit={handleLogin}>
        <div className="space-y-2">
          <label className="text-[10px] uppercase tracking-widest font-bold text-on-surface-variant px-1">Email Address</label>
          <input
            className="w-full bg-surface-container-highest border-none rounded-xl px-4 py-4 text-on-surface focus:ring-2 focus:ring-primary/50 transition-all placeholder:text-on-surface-variant/30 font-medium"
            placeholder="john@company.com"
            type="email"
          />
        </div>

        <div className="space-y-2">
          <div className="flex justify-between items-center px-1">
            <label className="text-[10px] uppercase tracking-widest font-bold text-on-surface-variant">Password</label>
            <a href="#" className="text-[10px] uppercase tracking-widest font-bold text-primary hover:underline">Forgot?</a>
          </div>
          <input
            className="w-full bg-surface-container-highest border-none rounded-xl px-4 py-4 text-on-surface focus:ring-2 focus:ring-primary/50 transition-all placeholder:text-on-surface-variant/30 font-medium"
            placeholder="••••••••"
            type="password"
          />
        </div>

        <div className="flex items-center gap-3 py-2">
          <input
            className="rounded bg-surface-container-highest border-none text-primary focus:ring-offset-background focus:ring-primary"
            id="remember"
            type="checkbox"
          />
          <label className="text-xs text-on-surface-variant" htmlFor="remember">Keep me authenticated across sessions</label>
        </div>

        <button className="w-full py-4 rounded-xl bg-linear-to-r from-primary to-secondary text-on-primary font-bold tracking-tight shadow-2xl shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300">
          Sign In to Dashboard
        </button>
      </form>

      <div className="mt-12 flex flex-col items-center gap-6">
        <div className="flex items-center w-full gap-4">
          <div className="h-px bg-outline-variant/20 grow"></div>
          <span className="text-[10px] uppercase tracking-widest font-medium text-on-surface-variant">Orbital Auth</span>
          <div className="h-px bg-outline-variant/20 grow"></div>
        </div>

        <div className="flex gap-4 w-full">
          <button className="flex-1 py-3 rounded-xl bg-surface-container-high flex items-center justify-center gap-2 hover:bg-surface-bright transition-colors border border-outline-variant/10">
            <img alt="Google" className="w-4 h-4 grayscale opacity-70" src="https://www.gstatic.com/images/branding/product/1x/googleg_48dp.png" />
            <span className="text-xs font-semibold">Google</span>
          </button>
          <button className="flex-1 py-3 rounded-xl bg-surface-container-high flex items-center justify-center gap-2 hover:bg-surface-bright transition-colors border border-outline-variant/10">
            <span className="material-symbols-outlined text-sm">terminal</span>
            <span className="text-xs font-semibold">GitHub</span>
          </button>
        </div>

        <p className="text-sm text-on-surface-variant">
          New to WebSpector? <Link className="text-primary font-semibold hover:underline" to="/signup">Initialize Account</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginForm;
