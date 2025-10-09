import { useState, useEffect } from 'react';

export interface EventSummary {
  id: number;
  stats: {
    passed: number;
    failed: number;
    corrected: number;
    running: number;
    pending: number;
    total: number;
    steps: Set<string>;
    timeRange: {
      start: string;
      end: string;
    };
  };
  eventsCount: number;
  collapsed: boolean;
}

export interface AutoSummarizedEvents<T> {
  recentEvents: T[];
  summarizedSections: EventSummary[];
  totalEventCount: number;
  toggleSummary: (summaryId: number) => void;
}

interface UseAutoSummarizedEventsOptions {
  maxEventsBeforeSummarize?: number;
  keepRecentEvents?: number;
}

/**
 * Hook to automatically summarize events when they exceed a limit
 * Keeps recent events visible while condensing older ones into expandable summaries
 */
export function useAutoSummarizedEvents<T extends { status: string; step: string; timestamp: string }>(
  events: T[],
  options: UseAutoSummarizedEventsOptions = {}
): AutoSummarizedEvents<T> {
  const {
    maxEventsBeforeSummarize = 30,
    keepRecentEvents = 15,
  } = options;

  const [recentEvents, setRecentEvents] = useState<T[]>(events);
  const [summarizedSections, setSummarizedSections] = useState<EventSummary[]>([]);

  // Auto-summarize when events exceed limit
  useEffect(() => {
    if (events.length > maxEventsBeforeSummarize) {
      const eventsToSummarize = events.slice(0, events.length - keepRecentEvents);
      const newRecentEvents = events.slice(-keepRecentEvents);

      const summary = generateSummary(eventsToSummarize);
      setSummarizedSections((prev) => [...prev, summary]);
      setRecentEvents(newRecentEvents);
    } else {
      setRecentEvents(events);
    }
  }, [events, maxEventsBeforeSummarize, keepRecentEvents]);

  const generateSummary = (eventsToSummarize: T[]): EventSummary => {
    const stats = {
      passed: 0,
      failed: 0,
      corrected: 0,
      running: 0,
      pending: 0,
      total: eventsToSummarize.length,
      steps: new Set<string>(),
      timeRange: {
        start: eventsToSummarize[0]?.timestamp || new Date().toISOString(),
        end: eventsToSummarize[eventsToSummarize.length - 1]?.timestamp || new Date().toISOString(),
      },
    };

    eventsToSummarize.forEach((event) => {
      const status = event.status.toLowerCase();
      // Count status types
      if (status === 'passed') stats.passed++;
      else if (status === 'failed') stats.failed++;
      else if (status === 'corrected') stats.corrected++;
      else if (status === 'running') stats.running++;
      else if (status === 'pending') stats.pending++;
      
      stats.steps.add(event.step);
    });

    return {
      id: Date.now() + Math.random(), // Ensure unique ID
      stats,
      eventsCount: eventsToSummarize.length,
      collapsed: true,
    };
  };

  const toggleSummary = (summaryId: number) => {
    setSummarizedSections((prev) =>
      prev.map((section) =>
        section.id === summaryId ? { ...section, collapsed: !section.collapsed } : section
      )
    );
  };

  const totalEventCount =
    summarizedSections.reduce((sum, s) => sum + s.eventsCount, 0) + recentEvents.length;

  return {
    recentEvents,
    summarizedSections,
    totalEventCount,
    toggleSummary,
  };
}

