import React from 'react';
import { CheckCircle2, XCircle, AlertCircle } from 'lucide-react';

interface SkillPillProps {
  name: string;
  category?: string;
  type?: 'matched' | 'missing_required' | 'missing_preferred' | 'additional';
  matchedAs?: string;
}

export const SkillPill: React.FC<SkillPillProps> = ({
  name,
  category,
  type = 'matched',
  matchedAs,
}) => {
  const styles = {
    matched: 'bg-emerald-50 text-emerald-800 border-emerald-200/80 hover:bg-emerald-100',
    missing_required: 'bg-rose-50 text-rose-800 border-rose-200/80 hover:bg-rose-100',
    missing_preferred: 'bg-amber-50 text-amber-800 border-amber-200/80 hover:bg-amber-100',
    additional: 'bg-slate-50 text-slate-700 border-slate-200/80 hover:bg-slate-100',
  };

  const icons = {
    matched: <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />,
    missing_required: <XCircle className="w-3.5 h-3.5 text-rose-600 shrink-0" />,
    missing_preferred: <AlertCircle className="w-3.5 h-3.5 text-amber-600 shrink-0" />,
    additional: <span className="w-1.5 h-1.5 rounded-full bg-slate-400 shrink-0" />,
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border transition-colors shadow-2xs ${styles[type]}`}
      title={category ? `Category: ${category}${matchedAs ? ` (Matched via '${matchedAs}')` : ''}` : undefined}
    >
      {icons[type]}
      <span className="capitalize">{name}</span>
      {category && (
        <span className="text-[10px] opacity-60 ml-0.5">· {category.split(' ')[0]}</span>
      )}
    </span>
  );
};

