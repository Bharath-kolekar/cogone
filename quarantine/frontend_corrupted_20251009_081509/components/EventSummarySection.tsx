'use client';

import React from 'react';
import { EventSummary } from '@/hooks/useAutoSummarizedEvents';

interface EventSummarySectionProps {
  summary: EventSummary;
  onToggle: (summaryId: number) => void;
}

export function EventSummarySection({ summary, onToggle }: EventSummarySectionProps) {
  return (
    <div className="mb-3 border-l-4 border-blue-300 pl-3 py-2 bg-blue-50 rounded-lg">
      <button
        onClick={() => onToggle(summary.id)}
        className="w-full text-left flex items-center justify-between hover:bg-blue-100 rounded-lg px-3 py-2 transition-colors"
        aria-expanded={!summary.collapsed}
        aria-label={`${summary.collapsed ? 'Expand' : 'Collapse'} summary of ${summary.eventsCount} events`}
      >
        <div className="flex-1">
          <span className="text-sm font-semibold text-blue-800 flex items-center">
            <span className="mr-2">📊</span>
            Summary: {summary.eventsCount} events
          </span>
          <div className="text-xs text-gray-600 mt-1 flex flex-wrap gap-2">
            {summary.stats.passed > 0 && (
              <span className="inline-flex items-center">
                <span className="mr-1">✅</span> {summary.stats.passed} passed
              </span>
            )}
            {summary.stats.failed > 0 && (
              <span className="inline-flex items-center">
                <span className="mr-1">❌</span> {summary.stats.failed} failed
              </span>
            )}
            {summary.stats.corrected > 0 && (
              <span className="inline-flex items-center">
                <span className="mr-1">🛠️</span> {summary.stats.corrected} corrected
              </span>
            )}
            {summary.stats.running > 0 && (
              <span className="inline-flex items-center">
                <span className="mr-1">⏳</span> {summary.stats.running} running
              </span>
            )}
            {summary.stats.pending > 0 && (
              <span className="inline-flex items-center">
                <span className="mr-1">⏸️</span> {summary.stats.pending} pending
              </span>
            )}
          </div>
          <div className="text-xs text-gray-500 mt-1.5 flex items-center">
            <span className="mr-1">🕐</span>
            {new Date(summary.stats.timeRange.start).toLocaleTimeString()} -{' '}
            {new Date(summary.stats.timeRange.end).toLocaleTimeString()}
          </div>
        </div>
        <span className="text-gray-400 ml-3 text-lg transition-transform" style={{ transform: summary.collapsed ? 'rotate(0deg)' : 'rotate(180deg)' }}>
          ▼
        </span>
      </button>
      
      {!summary.collapsed && (
        <div className="mt-3 pl-2 text-xs text-gray-600 border-t border-blue-200 pt-3 animate-fadeIn">
          <div className="font-semibold mb-2 text-blue-800">Steps covered:</div>
          <div className="flex flex-wrap gap-1.5">
            {Array.from(summary.stats.steps).map((step, idx) => (
              <span
                key={idx}
                className="bg-white px-2.5 py-1 rounded-md border border-blue-200 text-gray-700 hover:bg-blue-50 transition-colors"
              >
                {step}
              </span>
            ))}
          </div>
          <div className="mt-3 pt-2 border-t border-blue-100 text-gray-500 italic">
            Click to collapse this summary and save space
          </div>
        </div>
      )}
    </div>
  );
}

