'use client';

import React, { useMemo } from 'react';
import { useLiveValidationStatus, ValidationStatusEvent } from '@/hooks/useLiveValidationStatus';

interface SmartCodingAIIssuesPanelProps {
  sessionId: string;
}

interface Issue {
  id: string;
  severity: 'critical' | 'error' | 'warning' | 'info';
  category: string;
  message: string;
  status: 'active' | 'fixing' | 'resolved';
  timestamp: string;
  step: string;
}

export function SmartCodingAIIssuesPanel({ sessionId }: SmartCodingAIIssuesPanelProps) {
  const events = useLiveValidationStatus(sessionId);

  // Extract issues from events
  const issues = useMemo(() => {
    const issuesList: Issue[] = [];
    let issueCounter = 0;

    events.forEach((event, index) => {
      // Detect failures
      if (event.status === 'failed') {
        const issue: Issue = {
          id: `issue-${issueCounter++}`,
          severity: event.step.includes('Security') ? 'critical' : 'error',
          category: event.step,
          message: event.details || `${event.step} failed`,
          status: 'active',
          timestamp: event.timestamp,
          step: event.step,
        };
        issuesList.push(issue);
      }

      // Detect corrections (mark previous issue as fixing)
      if (event.status === 'running' && event.step.includes('Correction')) {
        const lastIssue = issuesList[issuesList.length - 1];
        if (lastIssue && lastIssue.status === 'active') {
          lastIssue.status = 'fixing';
        }
      }

      // Detect resolutions (mark issue as resolved)
      if (event.status === 'passed' && event.details?.includes('after correction')) {
        const relatedIssues = issuesList.filter(
          i => i.category === event.step && i.status === 'fixing'
        );
        relatedIssues.forEach(issue => {
          issue.status = 'resolved';
        });
      }
    });

    // Add warnings for pending reviews
    events.forEach((event) => {
      if (event.status === 'pending' && event.who === 'user') {
        issuesList.push({
          id: `warning-${issueCounter++}`,
          severity: 'warning',
          category: event.step,
          message: event.details || 'Action required',
          status: 'active',
          timestamp: event.timestamp,
          step: event.step,
        });
      }
    });

    return issuesList;
  }, [events]);

  // Calculate statistics
  const stats = useMemo(() => {
    const active = issues.filter(i => i.status === 'active').length;
    const fixing = issues.filter(i => i.status === 'fixing').length;
    const resolved = issues.filter(i => i.status === 'resolved').length;
    const critical = issues.filter(i => i.severity === 'critical' && i.status === 'active').length;
    const errors = issues.filter(i => i.severity === 'error' && i.status === 'active').length;
    const warnings = issues.filter(i => i.severity === 'warning' && i.status === 'active').length;

    return { active, fixing, resolved, critical, errors, warnings, total: issues.length };
  }, [issues]);

  const getSeverityColor = (severity: Issue['severity']) => {
    switch (severity) {
      case 'critical': return 'text-red-500 bg-red-500/10 border-red-500/50';
      case 'error': return 'text-orange-500 bg-orange-500/10 border-orange-500/50';
      case 'warning': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/50';
      case 'info': return 'text-blue-500 bg-blue-500/10 border-blue-500/50';
    }
  };

  const getSeverityIcon = (severity: Issue['severity']) => {
    switch (severity) {
      case 'critical': return '🔴';
      case 'error': return '🟠';
      case 'warning': return '🟡';
      case 'info': return '🔵';
    }
  };

  const getStatusBadge = (status: Issue['status']) => {
    switch (status) {
      case 'active':
        return <span className="px-2 py-0.5 text-xs rounded-full bg-red-500/20 text-red-400 border border-red-500/50">Active</span>;
      case 'fixing':
        return <span className="px-2 py-0.5 text-xs rounded-full bg-yellow-500/20 text-yellow-400 border border-yellow-500/50 animate-pulse">Fixing...</span>;
      case 'resolved':
        return <span className="px-2 py-0.5 text-xs rounded-full bg-green-500/20 text-green-400 border border-green-500/50">Resolved</span>;
    }
  };

  const getHealthStatus = () => {
    if (stats.critical > 0) return { label: 'Critical', color: 'text-red-400', icon: '🔴' };
    if (stats.errors > 0) return { label: 'Issues Found', color: 'text-orange-400', icon: '🟠' };
    if (stats.warnings > 0) return { label: 'Attention Needed', color: 'text-yellow-400', icon: '🟡' };
    if (stats.fixing > 0) return { label: 'Fixing Issues', color: 'text-blue-400', icon: '🔧' };
    if (stats.resolved > 0 && stats.active === 0) return { label: 'All Clear', color: 'text-green-400', icon: '✅' };
    return { label: 'Monitoring', color: 'text-gray-400', icon: '👁️' };
  };

  const health = getHealthStatus();

  return (
    <div className="issues-panel bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-6 rounded-xl shadow-2xl border border-gray-700">
      {/* Header */}
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-gray-700">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{health.icon}</span>
          <div>
            <h3 className="text-2xl font-bold">Issues Monitor</h3>
            <p className={`text-sm ${health.color} font-semibold`}>{health.label}</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold">{stats.total}</div>
          <div className="text-xs text-gray-400">Total Issues</div>
        </div>
      </div>

      {/* Statistics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-3 mb-6">
        <div className="bg-red-900/20 border border-red-700/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-red-400">{stats.critical}</div>
          <div className="text-xs text-gray-400 mt-1">Critical</div>
        </div>
        <div className="bg-orange-900/20 border border-orange-700/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-orange-400">{stats.errors}</div>
          <div className="text-xs text-gray-400 mt-1">Errors</div>
        </div>
        <div className="bg-yellow-900/20 border border-yellow-700/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-yellow-400">{stats.warnings}</div>
          <div className="text-xs text-gray-400 mt-1">Warnings</div>
        </div>
        <div className="bg-blue-900/20 border border-blue-700/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-blue-400">{stats.active}</div>
          <div className="text-xs text-gray-400 mt-1">Active</div>
        </div>
        <div className="bg-purple-900/20 border border-purple-700/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-purple-400">{stats.fixing}</div>
          <div className="text-xs text-gray-400 mt-1">Fixing</div>
        </div>
        <div className="bg-green-900/20 border border-green-700/50 rounded-lg p-3 text-center">
          <div className="text-2xl font-bold text-green-400">{stats.resolved}</div>
          <div className="text-xs text-gray-400 mt-1">Resolved</div>
        </div>
      </div>

      {/* Issues List */}
      <div className="space-y-3 max-h-[400px] overflow-y-auto">
        {issues.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">✨</div>
            <h4 className="text-xl font-semibold text-gray-300 mb-2">No Issues Detected</h4>
            <p className="text-sm text-gray-500">All validation checks are passing smoothly</p>
          </div>
        ) : (
          issues.map((issue) => (
            <div
              key={issue.id}
              className={`${getSeverityColor(issue.severity)} border rounded-lg p-4 transition-all duration-300 hover:scale-[1.02]`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-start gap-3 flex-1">
                  <span className="text-2xl">{getSeverityIcon(issue.severity)}</span>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold text-sm">{issue.category}</span>
                      {getStatusBadge(issue.status)}
                    </div>
                    <p className="text-sm text-gray-300 mb-2">{issue.message}</p>
                    <div className="flex items-center gap-4 text-xs text-gray-500">
                      <span>
                        {new Date(issue.timestamp).toLocaleTimeString()}
                      </span>
                      <span className="uppercase font-mono">{issue.severity}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Footer Summary */}
      {issues.length > 0 && (
        <div className="mt-6 pt-4 border-t border-gray-700">
          <div className="flex items-center justify-between text-sm">
            <div className="text-gray-400">
              {stats.active > 0 && (
                <span className="text-red-400 font-semibold">
                  {stats.active} active issue{stats.active !== 1 ? 's' : ''} require{stats.active === 1 ? 's' : ''} attention
                </span>
              )}
              {stats.active === 0 && stats.fixing > 0 && (
                <span className="text-yellow-400 font-semibold">
                  Cognomega is fixing {stats.fixing} issue{stats.fixing !== 1 ? 's' : ''}
                </span>
              )}
              {stats.active === 0 && stats.fixing === 0 && stats.resolved > 0 && (
                <span className="text-green-400 font-semibold">
                  All {stats.resolved} issue{stats.resolved !== 1 ? 's' : ''} resolved ✅
                </span>
              )}
            </div>
            <div className="text-gray-500 text-xs">
              Last updated: {new Date().toLocaleTimeString()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
