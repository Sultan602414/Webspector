import React from 'react';

const SeverityBadge = ({ severity }) => {
    const s = (severity || 'low').toLowerCase();
    const colors = {
        critical: 'bg-error/20 text-error border-error/30',
        high: 'bg-error/10 text-error border-error/20',
        medium: 'bg-secondary-container/30 text-secondary-fixed-dim border-secondary/20',
        low: 'bg-tertiary/10 text-tertiary border-tertiary/20'
    };
    const style = colors[s] || colors.low;
    return (
        <span className={`px-3 py-1 rounded-full text-[10px] font-black tracking-tighter uppercase border ${style}`}>
            {s}
        </span>
    );
};

export default SeverityBadge;
