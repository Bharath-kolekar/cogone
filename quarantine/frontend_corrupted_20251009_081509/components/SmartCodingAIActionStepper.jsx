import React from 'react';
import { FaRobot, FaUser, FaCheckCircle } from 'react-icons/fa';

const steps = [
  { label: 'User Request', who: 'user', icon: <FaUser /> },
  { label: 'AI Validation', who: 'ai', icon: <FaRobot /> },
  { label: 'User Review', who: 'user', icon: <FaUser /> },
  { label: 'AI Correction', who: 'ai', icon: <FaRobot /> },
  { label: 'Final Delivery', who: 'ai', icon: <FaCheckCircle /> },
];

function getCurrentStepIndex(latestEvent) {
  if (!latestEvent) return 0;
  const stepMap = {
    'User Request': 0,
    'Static Analysis': 1,
    'Security Validation': 1,
    'Test Generation': 1,
    'Best Practices': 1,
    'Consistency Check': 1,
    'User Review': 2,
    'Proactive Correction': 3,
    'AI Correction': 3,
    'Final Quality Gate': 4,
    'Code Delivery': 4,
  };
  return stepMap[latestEvent.step] ?? 0;
}

export function SmartCodingAIActionStepper({ latestEvent, onStepClick }) {
  const currentStep = getCurrentStepIndex(latestEvent);
  return (
    <div className="flex items-center justify-center space-x-4 my-4">
      {steps.map((step, idx) => (
        <div
          key={step.label}
          className={`flex flex-col items-center cursor-pointer ${
            idx === currentStep ? 'text-blue-600 font-bold' : 'text-gray-400'
          }`}
          onClick={onStepClick ? () => onStepClick(idx) : undefined}
        >
          <div className={`text-2xl mb-1 ${idx === currentStep ? 'animate-bounce' : ''}`}>{step.icon}</div>
          <span className="text-xs text-center whitespace-nowrap">{step.label}</span>
          {idx < steps.length - 1 && (
            <div className="w-8 h-1 bg-gray-200 mx-2 my-1 rounded-full" />
          )}
        </div>
      ))}
    </div>
  );
}
