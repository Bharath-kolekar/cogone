import React, { useRef, useEffect } from 'react';
import { useLiveValidationStatus } from '@/hooks/useLiveValidationStatus';

interface SmartCodingAILiveEventPanelProps {
  sessionId: string;
}

export function SmartCodingAILiveEventPanel({ sessionId }: SmartCodingAILiveEventPanelProps) {
  const events = useLiveValidationStatus(sessionId);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [events]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'text-blue-400';
      case 'passed': return 'text-green-400';
      case 'failed': return 'text-red-400';
      case 'corrected': return 'text-yellow-400';
      case 'pending': return 'text-purple-400';
      default: return 'text-gray-400';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return '⏳';
      case 'passed': return '✅';
      case 'failed': return '❌';
      case 'corrected': return '🛠️';
      case 'pending': return '⏸️';
      default: return '⚪';
    }
  };

  const getWhoIcon = (who: string) => {
    return who === 'user' ? '👤' : '🤖';
  };

  const getWhoColor = (who: string) => {
    return who === 'user' ? 'text-purple-300' : 'text-blue-300';
  };

  return (
    <div className="live-status-panel bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-6 rounded-xl shadow-2xl max-h-[500px] overflow-y-auto border border-gray-700">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-700">
        <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          🚀 Live Cognomega Activity
        </h3>
        <div className="text-xs text-gray-400">
          {events.length} events
        </div>
      </div>
      {events.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-gray-500">
          <div className="text-4xl mb-3">⏳</div>
          <p className="text-lg">Waiting for events...</p>
          <p className="text-xs mt-2">Connect to session: {sessionId}</p>
        </div>
      ) : (
        <ul className="space-y-2">
          {events.map((e, i) => (
            <li key={i} className="bg-gray-800/50 p-3 rounded-lg border border-gray-700/50 hover:border-gray-600 transition-all">
              <div className="flex items-start gap-3">
                <span className={`text-2xl ${getWhoColor(e.who)}`}>
                  {getWhoIcon(e.who)}
                </span>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-gray-500">
                      {new Date(e.timestamp).toLocaleTimeString()}
                    </span>
                    <span className={`${getStatusColor(e.status)} font-semibold text-sm flex items-center gap-1`}>
                      <span>{getStatusIcon(e.status)}</span>
                      <span>{e.step}</span>
                    </span>
                    <span className={`${getStatusColor(e.status)} text-xs uppercase font-bold px-2 py-0.5 rounded-full bg-gray-900/50`}>
                      {e.status}
                    </span>
                  </div>
                  {e.details && (
                    <p className="text-gray-400 text-xs mt-1 pl-1 border-l-2 border-gray-700">
                      {e.details}
                    </p>
                  )}
                </div>
              </div>
            </li>
          ))}
          <div ref={endOfMessagesRef} />
        </ul>
      )}
    </div>
  );
}
