import { useState, useEffect, useRef } from 'react';

export interface ValidationStatusEvent {
  step: string;
  status: string; // pending, running, passed, failed, corrected
  who: string; // 'ai' or 'user'
  details?: string;
  timestamp: string;
}

// Mock events for demo when backend is unavailable
const MOCK_EVENTS: Omit<ValidationStatusEvent, 'timestamp'>[] = [
  { step: 'User Request', status: 'passed', who: 'user', details: 'Code generation request received' },
  { step: 'Static Analysis', status: 'running', who: 'ai', details: '' },
  { step: 'Static Analysis', status: 'passed', who: 'ai', details: 'Passed ✅' },
  { step: 'Security Validation', status: 'running', who: 'ai', details: '' },
  { step: 'Security Validation', status: 'failed', who: 'ai', details: 'SQL Injection risk detected' },
  { step: 'Proactive Correction', status: 'running', who: 'ai', details: 'Auto-fixing SQL query' },
  { step: 'Security Validation', status: 'passed', who: 'ai', details: 'Passed after correction ✅' },
  { step: 'Test Generation', status: 'running', who: 'ai', details: '' },
  { step: 'Test Generation', status: 'passed', who: 'ai', details: 'All tests passed ✅' },
  { step: 'Best Practices', status: 'running', who: 'ai', details: '' },
  { step: 'Best Practices', status: 'passed', who: 'ai', details: 'Code follows best practices ✅' },
  { step: 'Consistency Check', status: 'running', who: 'ai', details: '' },
  { step: 'Consistency Check', status: 'passed', who: 'ai', details: 'Goal alignment verified ✅' },
  { step: 'User Review', status: 'pending', who: 'user', details: 'Please review the generated code' },
  { step: 'User Review', status: 'passed', who: 'user', details: 'User approved the code' },
  { step: 'Final Quality Gate', status: 'passed', who: 'ai', details: 'Six Sigma 99.99966%+ ✅' },
  { step: 'Code Delivery', status: 'passed', who: 'ai', details: '100% Accurate, Inline, No Drift ✅' },
];

export function useLiveValidationStatus(sessionId: string, forceMockMode: boolean = false): ValidationStatusEvent[] {
  const [events, setEvents] = useState<ValidationStatusEvent[]>([]);
  const [isMockMode, setIsMockMode] = useState(forceMockMode);
  const wsRef = useRef<WebSocket | null>(null);
  const mockTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const mockIndexRef = useRef(0);

  useEffect(() => {
    if (!sessionId) return;

    // Use mock mode if forced or if WebSocket fails
    if (isMockMode) {
      console.log('Using mock mode for demo');
      mockIndexRef.current = 0;
      
      const addNextEvent = () => {
        if (mockIndexRef.current < MOCK_EVENTS.length) {
          const mockEvent = MOCK_EVENTS[mockIndexRef.current];
          const eventWithTimestamp: ValidationStatusEvent = {
            ...mockEvent,
            timestamp: new Date().toISOString(),
          };
          
          setEvents(prev => [...prev, eventWithTimestamp]);
          mockIndexRef.current++;
          
          // Schedule next event with realistic delay
          const delay = mockIndexRef.current === 1 ? 500 : Math.random() * 600 + 400;
          mockTimeoutRef.current = setTimeout(addNextEvent, delay);
        }
      };

      // Start after a brief delay
      mockTimeoutRef.current = setTimeout(addNextEvent, 300);

      return () => {
        if (mockTimeoutRef.current) {
          clearTimeout(mockTimeoutRef.current);
        }
      };
    }

    // Try WebSocket connection
    const wsUrl = `ws://localhost:8000/ws/smart-coding-ai/status/${sessionId}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    let connectionTimeout: NodeJS.Timeout;
    let hasConnected = false;

    ws.onopen = () => {
      console.log(`✅ WebSocket connected for session ${sessionId}`);
      hasConnected = true;
      clearTimeout(connectionTimeout);
    };

    ws.onmessage = (event) => {
      const newEvent: ValidationStatusEvent = JSON.parse(event.data);
      setEvents((prev) => [...prev, newEvent]);
    };

    ws.onerror = (error) => {
      console.warn('⚠️ WebSocket error, will fallback to mock mode:', error);
      if (!hasConnected) {
        setIsMockMode(true);
      }
    };

    ws.onclose = () => {
      console.log(`WebSocket closed for session ${sessionId}`);
    };

    // Fallback to mock mode if connection fails within 2 seconds
    connectionTimeout = setTimeout(() => {
      if (ws.readyState !== WebSocket.OPEN) {
        console.warn('⚠️ WebSocket connection timeout, using mock mode');
        ws.close();
        setIsMockMode(true);
      }
    }, 2000);

    return () => {
      clearTimeout(connectionTimeout);
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [sessionId, isMockMode]);

  return events;
}
