import React from 'react';
import { Link } from 'react-router-dom';

const SignupForm = () => {
  return (
    <div className="max-w-md mx-auto w-full">
      <div className="mb-10">
        <h2 className="text-2xl font-bold tracking-tight text-on-surface mb-2">Create your account</h2>
        <p className="text-on-surface-variant text-sm">Start your 14-day premium trial. No credit card required.</p>
      </div>
      
      <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-[10px] uppercase tracking-widest font-bold text-on-surface-variant px-1">Full Name</label>
            <input 
              className="w-full bg-surface-container-highest border-none rounded-lg px-4 py-3 text-on-surface focus:ring-2 focus:ring-primary/50 transition-all placeholder:text-on-surface-variant/30" 
              placeholder="John Doe" 
              type="text" 
            />
          </div>
          <div className="space-y-2">
            <label className="text-[10px] uppercase tracking-widest font-bold text-on-surface-variant px-1">Company Name</label>
            <input 
              className="w-full bg-surface-container-highest border-none rounded-lg px-4 py-3 text-on-surface focus:ring-2 focus:ring-primary/50 transition-all placeholder:text-on-surface-variant/30" 
              placeholder="Acme Inc." 
              type="text" 
            />
          </div>
        </div>
        
        <div className="space-y-2">
          <label className="text-[10px] uppercase tracking-widest font-bold text-on-surface-variant px-1">Work Email</label>
          <input 
            className="w-full bg-surface-container-highest border-none rounded-lg px-4 py-3 text-on-surface focus:ring-2 focus:ring-primary/50 transition-all placeholder:text-on-surface-variant/30" 
            placeholder="john@company.com" 
            type="email" 
          />
        </div>
        
        <div className="space-y-2">
          <label className="text-[10px] uppercase tracking-widest font-bold text-on-surface-variant px-1">Password</label>
          <input 
            className="w-full bg-surface-container-highest border-none rounded-lg px-4 py-3 text-on-surface focus:ring-2 focus:ring-primary/50 transition-all placeholder:text-on-surface-variant/30" 
            placeholder="••••••••" 
            type="password" 
          />
        </div>
        
        <div className="flex items-start gap-3 py-2">
          <input 
            className="mt-1 rounded bg-surface-container-highest border-none text-primary focus:ring-offset-background focus:ring-primary" 
            id="terms" 
            type="checkbox" 
          />
          <label className="text-xs text-on-surface-variant leading-relaxed" htmlFor="terms">
            I agree to the <a className="text-primary hover:underline" href="#">Terms of Service</a> and <a className="text-primary hover:underline" href="#">Privacy Policy</a>. I also consent to receiving product updates and newsletters.
          </label>
        </div>
        
        <button className="w-full py-4 rounded-lg bg-linear-to-r from-primary to-secondary text-on-primary font-bold tracking-tight shadow-xl shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all duration-300">
          Get Started
        </button>
      </form>
      
      <div className="mt-10 flex flex-col items-center gap-6">
        <div className="flex items-center w-full gap-4">
          <div className="h-px bg-outline-variant/30 flex-grow"></div>
          <span className="text-[10px] uppercase tracking-widest font-medium text-on-surface-variant">or continue with</span>
          <div className="h-px bg-outline-variant/30 flex-grow"></div>
        </div>
        
        <div className="flex gap-4 w-full">
          <button className="flex-1 py-3 rounded-lg bg-surface-container-high flex items-center justify-center gap-2 hover:bg-surface-bright transition-colors border border-outline-variant/10">
            <img alt="Google" className="w-4 h-4 grayscale opacity-70" src="https://www.gstatic.com/images/branding/product/1x/googleg_48dp.png" />
            <span className="text-xs font-semibold">Google</span>
          </button>
          <button className="flex-1 py-3 rounded-lg bg-surface-container-high flex items-center justify-center gap-2 hover:bg-surface-bright transition-colors border border-outline-variant/10">
            <span className="material-symbols-outlined text-sm">terminal</span>
            <span className="text-xs font-semibold">GitHub</span>
          </button>
        </div>
        
        <p className="text-sm text-on-surface-variant">
          Already have an account? <Link className="text-primary font-semibold hover:underline" to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default SignupForm;
