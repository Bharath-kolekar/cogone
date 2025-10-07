import React from 'react';
import { FaRobot, FaUser } from 'react-icons/fa';

export function SmartCodingAIWhoActsNext({ latestEvent }) {
  if (!latestEvent) return null;
  let who = latestEvent.who || 'ai'; // default to AI if not specified
  let status = latestEvent.status;
  let message = '';
  let icon = null;

  if (who === 'ai') {
    if (status === 'running' || status === 'pending') {
      message = 'Cognomega is working...';
      icon = <FaRobot className="inline mr-2 text-blue-600" />;
    } else if (status === 'passed' || status === 'corrected') {
      message = 'Cognomega completed this step.';
      icon = <FaRobot className="inline mr-2 text-green-600" />;
    } else if (status === 'failed') {
      message = 'Cognomega encountered an issue.';
      icon = <FaRobot className="inline mr-2 text-red-600" />;
    }
  } else if (who === 'user') {
    message = 'Waiting for your input...';
    icon = <FaUser className="inline mr-2 text-purple-600" />;
  }

  return (
    <div className="flex items-center bg-gray-100 border rounded px-4 py-2 mb-2 shadow">
      {icon}
      <span className="font-semibold text-gray-700">{message}</span>
    </div>
  );
}
