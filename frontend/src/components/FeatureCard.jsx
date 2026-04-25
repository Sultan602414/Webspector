import React from 'react';

const FeatureCard = ({ icon, title, desc, color = 'primary' }) => (
  <div className="glass-panel rounded-4xl p-8 relative overflow-hidden group border border-white/5 text-center flex flex-col items-center">
    <div className="absolute -right-4 -top-4 opacity-5 group-hover:opacity-10 transition-opacity">
      <span className="material-symbols-outlined text-8xl">{icon}</span>
    </div>

    <div className={`w-16 h-16 rounded-full bg-linear-to-br from-primary via-secondary to-tertiary flex items-center justify-center mb-6 border border-white/10 shadow-2xl shadow-primary/40 group-hover:scale-110 transition-transform duration-500`}>
      <span className="material-symbols-outlined text-gray-900 text-3xl drop-shadow-md">{icon}</span>
    </div>

    <h4 className="text-on-surface font-bold text-lg mb-3 tracking-tight">{title}</h4>
    <p className="text-on-surface-variant text-xs leading-relaxed max-w-[240px]">{desc}</p>

    <div className="mt-6 w-8 h-1 bg-linear-to-r from-primary/30 to-transparent rounded-full group-hover:w-16 transition-all duration-700"></div>
  </div>
);

export default FeatureCard;
