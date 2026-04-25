import React from 'react';

const DetailStatCard = ({ label, value, icon, color }) => (
    <div className="p-6 bg-surface-container-low rounded-2xl flex items-center justify-between group hover:bg-surface-container-high transition-colors border border-outline-variant/5">
        <div className="space-y-1">
            <span className="text-[10px] font-bold text-on-surface-variant uppercase tracking-wider">{label}</span>
            <p className="text-4xl font-bold text-white">{value}</p>
        </div>
        <div className={`p-4 bg-${color === 'error' ? 'error-container/20' : color + '/10'} rounded-xl text-${color}`}>
            <span className="material-symbols-outlined text-3xl">{icon}</span>
        </div>
    </div>
);

export default DetailStatCard;
