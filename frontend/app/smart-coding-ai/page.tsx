'use client';

import React, { useState } from 'react';
import { SmartCodingAILiveEventPanel } from '@/components/SmartCodingAILiveEventPanel';
import { SmartCodingAIWhoActsNext } from '@/components/SmartCodingAIWhoActsNext';
import { SmartCodingAIActionStepper } from '@/components/SmartCodingAIActionStepper';

export default function SmartCodingAIPage() {
  const [sessionId, setSessionId] = useState('');
  const [activeSessionId, setActiveSessionId] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleStartSession = async () => {
    if (!sessionId.trim()) {
      alert('Please enter a session ID');
      return;
    }
    setActiveSessionId(sessionId);
  };

  const handleTriggerDemo = async () => {
    if (!activeSessionId) {
      alert('Please start a session first');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/test/smart-coding-ai/emit-events/${activeSessionId}`, {
        method: 'POST',
      });
      const data = await response.json();
      console.log('Demo triggered:', data);
    } catch (error) {
      console.error('Error triggering demo:', error);
      alert('Failed to trigger demo. Make sure the backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black text-white p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
            🧠 Smart Coding AI Dashboard
          </h1>
          <p className="text-gray-400 text-lg">
            Real-time Six Sigma Quality Gates • 100% Accurate Code • Zero Drift
          </p>
        </div>

        {/* Session Control */}
        <div className="bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl shadow-xl border border-gray-700 mb-8">
          <div className="flex gap-4 items-end">
            <div className="flex-1">
              <label className="block text-sm font-semibold text-gray-300 mb-2">
                Session ID
              </label>
              <input
                type="text"
                value={sessionId}
                onChange={(e) => setSessionId(e.target.value)}
                placeholder="Enter session ID (e.g., session123)"
                className="w-full px-4 py-3 bg-gray-900 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button
              onClick={handleStartSession}
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl"
            >
              Start Session
            </button>
            <button
              onClick={handleTriggerDemo}
              disabled={!activeSessionId || isLoading}
              className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Triggering...' : 'Trigger Demo'}
            </button>
          </div>
          {activeSessionId && (
            <div className="mt-4 text-sm text-gray-400">
              Active Session: <span className="text-blue-400 font-mono">{activeSessionId}</span>
            </div>
          )}
        </div>

        {activeSessionId && (
          <>
            {/* Who Acts Next */}
            <div className="mb-8">
              <SmartCodingAIWhoActsNext sessionId={activeSessionId} />
            </div>

            {/* Action Stepper */}
            <div className="mb-8">
              <SmartCodingAIActionStepper sessionId={activeSessionId} />
            </div>

            {/* Live Event Panel */}
            <div>
              <SmartCodingAILiveEventPanel sessionId={activeSessionId} />
            </div>
          </>
        )}

        {!activeSessionId && (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">🚀</div>
            <h2 className="text-2xl font-semibold text-gray-400 mb-2">
              Ready to Start
            </h2>
            <p className="text-gray-500">
              Enter a session ID above to begin monitoring Smart Coding AI activity
            </p>
          </div>
        )}

        {/* Feature Highlights */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-blue-900/20 to-blue-800/20 p-6 rounded-xl border border-blue-700/50">
            <div className="text-3xl mb-3">🎯</div>
            <h3 className="text-lg font-semibold mb-2">Six Sigma Quality</h3>
            <p className="text-sm text-gray-400">
              99.99966% accuracy with multi-layer validation pipeline
            </p>
          </div>
          <div className="bg-gradient-to-br from-purple-900/20 to-purple-800/20 p-6 rounded-xl border border-purple-700/50">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="text-lg font-semibold mb-2">Real-time Streaming</h3>
            <p className="text-sm text-gray-400">
              Live updates via WebSocket for instant feedback
            </p>
          </div>
          <div className="bg-gradient-to-br from-green-900/20 to-green-800/20 p-6 rounded-xl border border-green-700/50">
            <div className="text-3xl mb-3">🛠️</div>
            <h3 className="text-lg font-semibold mb-2">Proactive Correction</h3>
            <p className="text-sm text-gray-400">
              Auto-fix issues before delivery with zero drift
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}