import React from 'react';

const StatCard = ({ icon, label, value, trend, color, border }) => (
  <div className={`bg-surface-container-low p-8 rounded-2xl relative overflow-hidden group ${border ? 'border border-primary/5' : ''}`}>
    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
      <span className="material-symbols-outlined text-6xl">{icon}</span>
    </div>
    <p className="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold mb-4">{label}</p>
    <div className="flex items-baseline gap-2">
      <span className="text-5xl font-black text-on-surface">{value}</span>
      <span className={`text-${color} text-xs font-bold`}>{trend}</span>
    </div>
  </div>
);

export default StatCard;
