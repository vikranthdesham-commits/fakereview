import React from 'react';
import { AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function InspectionStamp({ verdict, confidence }) {
  const isSuspicious = verdict === 'Suspicious' || verdict === 'FLAGGED';

  return (
    <div className="relative inline-block select-none animate-stamp-impact my-2">
      {isSuspicious ? (
        <div className="relative px-5 py-2.5 rounded-lg stamp-border-flagged bg-case-red/10 backdrop-blur-xs transform -rotate-6 shadow-stamp flex items-center space-x-2">
          <AlertTriangle className="w-7 h-7 text-case-red animate-pulse" />
          <div className="text-left">
            <span className="block font-mono font-black text-2xl uppercase tracking-wider text-case-red leading-none">
              SUSPICIOUS
            </span>
            <span className="block font-mono text-[10px] text-case-red/80 uppercase tracking-widest mt-0.5">
              CONFIDENCE: {confidence || 'HIGH'}
            </span>
          </div>
        </div>
      ) : (
        <div className="relative px-5 py-2.5 rounded-lg stamp-border-verified bg-case-teal/10 backdrop-blur-xs transform -rotate-3 shadow-stamp-verified flex items-center space-x-2">
          <CheckCircle2 className="w-7 h-7 text-case-teal" />
          <div className="text-left">
            <span className="block font-mono font-black text-2xl uppercase tracking-wider text-case-teal leading-none">
              VERIFIED
            </span>
            <span className="block font-mono text-[10px] text-case-teal/80 uppercase tracking-widest mt-0.5">
              GENUINE PATTERN MATCH
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
