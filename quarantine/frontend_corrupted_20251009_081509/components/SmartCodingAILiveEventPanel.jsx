'use client';

import React, { useEffect, useRef, useState } from 'react';
import { useAutoSummarizedEvents } from '@/hooks/useAutoSummarizedEvents';
import { EventSummarySection } from '@/components/EventSummarySection';

export function SmartCodingAILiveEventPanel({ sessionId }) {
  const [events, setEvents] = useState([]);
  const panelRef = useRef(null);

  // Use auto-summarization hook
  const { recentEvents, summarizedSections, totalEventCount, toggleSummary } = useAutoSummarizedEvents(events, {
    maxEventsBeforeSummarize: 30,
    keepRecentEvents: 15,
  });

  useEffect(() => {
    if (!sessionId) return;
    const ws = new WebSocket(`ws://localhost:8000/ws/smart-coding-ai/status/${sessionId}`);
    ws.onmessage = (event) => {
      setEvents((prev) => [...prev, JSON.parse(event.data)]);
    };
    return () => ws.close();
  }, [sessionId]);

  useEffect(() => {
    if (panelRef.current) {
      panelRef.current.scrollTop = panelRef.current.scrollHeight;
    }
  }, [recentEvents, summarizedSections]);

  const statusColor = (status) => {
    switch (status) {
      case 'running': return 'text-blue-600';
      case 'passed': return 'text-green-600';
      case 'failed': return 'text-red-600';
      case 'corrected': return 'text-yellow-600';
      default: return 'text-gray-700';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'running': return '⏳';
      case 'passed': return '✅';
      case 'failed': return '❌';
      case 'corrected': return '🛠️';
      default: return '⚪';
    }
  };

  return (
    <div className="bg-white border rounded-lg shadow-lg p-4 max-h-96 overflow-y-auto" ref={panelRef}>
      <div className="flex items-center justify-between mb-3 pb-2 border-b border-gray-200">
        <h3 className="font-bold text-gray-800">Live Validation Event Panel</h3>
        {totalEventCount > 0 && (
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              {totalEventCount} total events
            </span>
            {summarizedSections.length > 0 && (
              <span className="text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded">
                {summarizedSections.length} summary section{summarizedSections.length !== 1 ? 's' : ''}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Summarized sections */}
      {summarizedSections.map((summary) => (
        <EventSummarySection key={summary.id} summary={summary} onToggle={toggleSummary} />
      ))}

      {/* Recent events */}
      {recentEvents.length > 0 && (
        <div className="space-y-1">
          {summarizedSections.length > 0 && (
            <div className="text-xs text-gray-500 font-semibold mb-2 pt-2 border-t border-gray-200">
              Recent Events:
            </div>
          )}
          <ul className="space-y-1 text-sm">
            {recentEvents.map((e, i) => (
              <li key={i} className={`flex items-start space-x-2 ${statusColor(e.status)} border-l-2 pl-2 py-1 rounded-r hover:bg-gray-50 transition-colors`}>
                <span className="flex-shrink-0">{getStatusIcon(e.status)}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline space-x-2">
                    <span className="font-mono text-xs text-gray-400 flex-shrink-0">
                      [{new Date(e.timestamp).toLocaleTimeString()}]
                    </span>
                    <span className="font-semibold truncate">{e.step}:</span>
                    <span className="capitalize">{e.status}</span>
                  </div>
                  {e.details && (
                    <div className="text-xs text-gray-500 mt-0.5 ml-0">
                      {e.details}
                    </div>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {recentEvents.length === 0 && summarizedSections.length === 0 && (
        <div className="text-gray-400 text-center py-8">
          <div className="text-4xl mb-2">⏳</div>
          <div className="font-medium">Waiting for events...</div>
          <div className="text-xs mt-1">Events will appear here as they stream in</div>
        </div>
      )}
    </div>
  );
}
