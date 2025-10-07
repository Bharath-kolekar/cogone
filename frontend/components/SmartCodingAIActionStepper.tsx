import React, { useState, useEffect } from 'react';
import { useLiveValidationStatus } from '@/hooks/useLiveValidationStatus';

interface SmartCodingAIActionStepperProps {
  sessionId: string;
}

interface Step {
  id: string;
  name: string;
  actor: 'User' | 'Cognomega';
  icon: string;
}

const STEPS: Step[] = [
  { id: 'user_request', name: 'User Request', actor: 'User', icon: '📝' },
  { id: 'ai_validation', name: 'AI Validation', actor: 'Cognomega', icon: '🔍' },
  { id: 'ai_correction', name: 'AI Correction', actor: 'Cognomega', icon: '🛠️' },
  { id: 'user_review', name: 'User Review', actor: 'User', icon: '👁️' },
  { id: 'final_delivery', name: 'Final Delivery', actor: 'Cognomega', icon: '🚀' },
];

export function SmartCodingAIActionStepper({ sessionId }: SmartCodingAIActionStepperProps) {
  const events = useLiveValidationStatus(sessionId);
  const [currentStepId, setCurrentStepId] = useState('user_request');
  const [completedSteps, setCompletedSteps] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (events.length > 0) {
      const lastEvent = events[events.length - 1];
      const newCompletedSteps = new Set(completedSteps);

      // Logic to determine current high-level step based on detailed validation events
      if (lastEvent.step === 'Code Delivery' && lastEvent.status === 'passed') {
        setCurrentStepId('final_delivery');
        newCompletedSteps.add('user_request');
        newCompletedSteps.add('ai_validation');
        newCompletedSteps.add('ai_correction');
        newCompletedSteps.add('user_review');
        newCompletedSteps.add('final_delivery');
      } else if (lastEvent.step === 'User Review') {
        setCurrentStepId('user_review');
        newCompletedSteps.add('user_request');
        newCompletedSteps.add('ai_validation');
        newCompletedSteps.add('ai_correction');
        if (lastEvent.status === 'passed') {
          newCompletedSteps.add('user_review');
        }
      } else if (lastEvent.step.includes('Correction') || lastEvent.status === 'corrected') {
        setCurrentStepId('ai_correction');
        newCompletedSteps.add('user_request');
        newCompletedSteps.add('ai_validation');
      } else if (lastEvent.step === 'User Request') {
        setCurrentStepId('user_request');
        if (lastEvent.status === 'passed') {
          newCompletedSteps.add('user_request');
        }
      } else if (lastEvent.status === 'running' || lastEvent.status === 'passed' || lastEvent.status === 'failed') {
        setCurrentStepId('ai_validation');
        newCompletedSteps.add('user_request');
      }

      setCompletedSteps(newCompletedSteps);
    }
  }, [events]);

  const getStepStatus = (stepId: string) => {
    if (completedSteps.has(stepId)) return 'completed';
    if (stepId === currentStepId) return 'current';
    return 'pending';
  };

  const getStepColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500 text-white border-green-400';
      case 'current': return 'bg-blue-500 text-white border-blue-400 animate-pulse';
      case 'pending': return 'bg-gray-700 text-gray-400 border-gray-600';
      default: return 'bg-gray-700 text-gray-400 border-gray-600';
    }
  };

  const getConnectorColor = (stepIndex: number) => {
    const currentIndex = STEPS.findIndex(s => s.id === currentStepId);
    return stepIndex < currentIndex ? 'bg-green-500' : 'bg-gray-700';
  };

  return (
    <div className="action-stepper bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6 rounded-xl shadow-2xl border border-gray-700">
      <h3 className="text-xl font-bold mb-6 text-center bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
        Process Flow
      </h3>
      <div className="flex justify-between items-center">
        {STEPS.map((step, index) => (
          <React.Fragment key={step.id}>
            <div className="flex flex-col items-center flex-1">
              <div
                className={`w-16 h-16 rounded-full flex items-center justify-center font-bold text-2xl border-2 transition-all duration-300 ${getStepColor(getStepStatus(step.id))}`}
              >
                {step.icon}
              </div>
              <div className="mt-3 text-center">
                <div className="text-xs font-semibold text-white">{step.name}</div>
                <div className={`text-xs mt-1 ${step.actor === 'User' ? 'text-purple-400' : 'text-blue-400'}`}>
                  ({step.actor})
                </div>
              </div>
            </div>
            {index < STEPS.length - 1 && (
              <div className={`flex-1 h-1 ${getConnectorColor(index)} mx-2 transition-all duration-300`}></div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
