import React from 'react';
import { Tag, AlertCircle } from 'lucide-react';

export default function HighlightedTextViewer({ text, highlightedPhrases = [] }) {
  if (!text) return null;

  const validPhrases = (highlightedPhrases || []).filter(p => p && p.trim().length > 0);

  if (validPhrases.length === 0) {
    return (
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 text-sm leading-relaxed">
        {text}
      </div>
    );
  }

  const escapedPhrases = validPhrases.map(p => p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const regex = new RegExp(`(${escapedPhrases.join('|')})`, 'gi');
  const parts = text.split(regex);

  return (
    <div className="space-y-3">
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 text-sm leading-relaxed">
        {parts.map((part, idx) => {
          const isHighlighted = validPhrases.some(
            p => p.toLowerCase() === part.toLowerCase()
          );
          if (isHighlighted) {
            return (
              <mark
                key={idx}
                className="bg-rose-100 text-rose-900 font-semibold px-1.5 py-0.5 rounded border border-rose-300 mx-0.5 inline-block"
              >
                {part}
              </mark>
            );
          }
          return <span key={idx}>{part}</span>;
        })}
      </div>

      {/* Flagged tokens list */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-medium text-slate-500 flex items-center gap-1">
          <Tag className="w-3.5 h-3.5 text-slate-400" /> Flagged Patterns:
        </span>
        {validPhrases.map((phrase, idx) => (
          <span
            key={idx}
            className="text-xs font-semibold bg-rose-50 text-rose-700 px-2.5 py-1 rounded-md border border-rose-200"
          >
            "{phrase}"
          </span>
        ))}
      </div>
    </div>
  );
}
