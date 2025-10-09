import React from 'react';
import { useLiveValidationStatus } from '@/hooks/useLiveValidationStatus';

interface SmartCodingAIWhoActsNextProps {
  sessionId: string;
}

export function SmartCodingAIWhoActsNext({ sessionId }: SmartCodingAIWhoActsNextProps) {
  const events = useLiveValidationStatus(sessionId);
  const lastEvent = events[events.length - 1];

  let nextActor = 'Cognomega'; // Default
  let message = 'Cognomega is processing...';
  let actorType: 'ai' | 'user' = 'ai';

  if (lastEvent) {
    if (lastEvent.step === 'Code Delivery' && lastEvent.status === 'passed') {
      nextActor = 'User';
      actorType = 'user';
      message = 'All done! Ready for your next request.';
    } else if (lastEvent.step === 'User Review' && lastEvent.status === 'pending') {
      nextActor = 'User';
      actorType = 'user';
      message = 'Waiting for your review and approval...';
    } else if (lastEvent.who === 'user' && lastEvent.status === 'passed') {
      nextActor = 'Cognomega';
      actorType = 'ai';
      message = 'Cognomega is continuing processing...';
    } else if (lastEvent.status === 'running' || lastEvent.status === 'corrected') {
      nextActor = 'Cognomega';
      actorType = 'ai';
      message = `Cognomega is ${lastEvent.status === 'corrected' ? 'correcting' : 'working on'} ${lastEvent.step.toLowerCase()}...`;
    } else if (lastEvent.status === 'passed' || lastEvent.status === 'failed') {
      nextActor = 'Cognomega';
      actorType = 'ai';
      message = `Cognomega is proceeding after ${lastEvent.step.toLowerCase()}...`;
    }
  }

  const actorColor = actorType === 'user' ? 'from-purple-500 to-pink-500' : 'from-blue-500 to-cyan-500';
  const actorIcon = actorType === 'user' ? '👤' : '🤖';
  const bgGradient = actorType === 'user' ? 'from-purple-900/20 to-pink-900/20' : 'from-blue-900/20 to-cyan-900/20';

  return (
    <div className={`who-acts-next-panel bg-gradient-to-r ${bgGradient} backdrop-blur-sm text-white p-4 rounded-xl shadow-lg border border-gray-700/50`}>
      <div className="flex items-center justify-center gap-4">
        <div className={`text-4xl animate-pulse`}>
          {actorIcon}
        </div>
        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-400 uppercase tracking-wider">Next Action</span>
            <span className={`text-2xl font-bold bg-gradient-to-r ${actorColor} bg-clip-text text-transparent`}>
              {nextActor}
            </span>
          </div>
          <span className="text-sm text-gray-300 mt-1">{message}</span>
        </div>
      </div>
    </div>
  );
}
