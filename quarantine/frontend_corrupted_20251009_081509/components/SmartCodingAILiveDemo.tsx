'use client';

import React, { useState, useEffect } from 'react';
import { SmartCodingAILiveEventPanel } from '@/components/SmartCodingAILiveEventPanel';
import { SmartCodingAIWhoActsNext } from '@/components/SmartCodingAIWhoActsNext';
import { SmartCodingAIActionStepper } from '@/components/SmartCodingAIActionStepper';
import { SmartCodingAIIssuesPanel } from '@/components/SmartCodingAIIssuesPanel';

interface SmartCodingAILiveDemoProps {
  autoStart?: boolean;
  autoTriggerDemo?: boolean;
}

export function SmartCodingAILiveDemo({ 
  autoStart = true, 
  autoTriggerDemo = true 
}: SmartCodingAILiveDemoProps) {
  const [sessionId, setSessionId] = useState('');
  const [activeSessionId, setActiveSessionId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [demoTriggered, setDemoTriggered] = useState(false);

  // Auto-generate session ID on mount
  useEffect(() => {
    if (autoStart) {
      const generatedSessionId = `demo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      setSessionId(generatedSessionId);
      setActiveSessionId(generatedSessionId);
    }
  }, [autoStart]);

  // Auto-trigger demo after session is active
  useEffect(() => {
    if (autoTriggerDemo && activeSessionId && !demoTriggered) {
      // Wait a moment for WebSocket to connect
      const timer = setTimeout(() => {
        handleTriggerDemo();
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [activeSessionId, autoTriggerDemo, demoTriggered]);

  const handleStartSession = async () => {
    if (!sessionId.trim()) {
      const generatedSessionId = `demo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      setSessionId(generatedSessionId);
      setActiveSessionId(generatedSessionId);
    } else {
      setActiveSessionId(sessionId);
    }
  };

  const handleTriggerDemo = async () => {
    if (!activeSessionId) {
      return;
    }

    setIsLoading(true);
    setDemoTriggered(true);
    
    try {
      const response = await fetch(`http://localhost:8000/test/smart-coding-ai/emit-events/${activeSessionId}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Demo triggered:', data);
      }
    } catch (error) {
      console.error('Error triggering demo:', error);
      // Don't show alert on auto-trigger
      if (!autoTriggerDemo) {
        alert('Failed to trigger demo. Make sure the backend is running on port 8000.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestart = () => {
    const newSessionId = `demo-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(newSessionId);
    setActiveSessionId(newSessionId);
    setDemoTriggered(false);
  };

  return (
    <div className="w-full">
      {/* Control Panel - Compact for home page */}
      <div className="bg-gray-800/30 backdrop-blur-sm p-4 rounded-xl shadow-lg border border-gray-700/50 mb-6">
        <div className="flex flex-wrap gap-3 items-center justify-between">
          <div className="flex items-center gap-3 flex-1 min-w-[200px]">
            <div className="flex-1">
              <input
                type="text"
                value={sessionId}
                onChange={(e) => setSessionId(e.target.value)}
                placeholder="Session ID (auto-generated)"
                className="w-full px-3 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-white text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={autoStart}
              />
            </div>
          </div>
          
          <div className="flex gap-2">
            {!autoStart && (
              <button
                onClick={handleStartSession}
                className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 rounded-lg font-semibold text-sm transition-all shadow-lg hover:shadow-xl"
              >
                Start Session
              </button>
            )}
            
            <button
              onClick={handleTriggerDemo}
              disabled={!activeSessionId || isLoading}
              className="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 rounded-lg font-semibold text-sm transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Running...' : demoTriggered ? 'Run Again' : 'Run Demo'}
            </button>
            
            {demoTriggered && (
              <button
                onClick={handleRestart}
                className="px-4 py-2 bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 rounded-lg font-semibold text-sm transition-all shadow-lg hover:shadow-xl"
              >
                Restart
              </button>
            )}
          </div>
        </div>
        
        {activeSessionId && (
          <div className="mt-3 flex items-center gap-2 text-xs">
            <span className="text-gray-400">Session:</span>
            <span className="text-blue-400 font-mono bg-gray-900/50 px-2 py-1 rounded">{activeSessionId}</span>
            <span className="flex items-center gap-1 text-green-400">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              Live
            </span>
          </div>
        )}
      </div>

      {activeSessionId ? (
        <>
          {/* Who Acts Next */}
          <div className="mb-6">
            <SmartCodingAIWhoActsNext sessionId={activeSessionId} />
          </div>

          {/* Action Stepper */}
          <div className="mb-6">
            <SmartCodingAIActionStepper sessionId={activeSessionId} />
          </div>

          {/* Issues Monitor */}
          <div className="mb-6">
            <SmartCodingAIIssuesPanel sessionId={activeSessionId} />
          </div>

          {/* Live Event Panel */}
          <div>
            <SmartCodingAILiveEventPanel sessionId={activeSessionId} />
          </div>
        </>
      ) : (
        <div className="text-center py-12 bg-gray-800/20 rounded-xl border border-gray-700/50">
          <div className="text-4xl mb-3">🚀</div>
          <h3 className="text-xl font-semibold text-gray-300 mb-2">
            Ready to Start
          </h3>
          <p className="text-gray-500 text-sm">
            Click "Start Session" to begin watching Cognomega's Six Sigma quality pipeline
          </p>
        </div>
      )}
    </div>
  );
}
