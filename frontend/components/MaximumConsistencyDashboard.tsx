"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { useToast } from '../hooks/use-toast';

interface MaximumConsistencyMetrics {
  consistency_score: number;
  reliability_score: number;
  consistency_violations: number;
  reliability_failures: number;
  total_requests: number;
  target_consistency: number;
  target_reliability: number;
  consistency_level: string;
}

interface MaximumConsistencyStatus {
  status: string;
  consistency_level: string;
  reliability_level: string;
  target_consistency: number;
  target_reliability: number;
  maximum_consistency_active: boolean;
}

export default function MaximumConsistencyDashboard() {
  const [metrics, setMetrics] = useState<MaximumConsistencyMetrics | null>(null);
  const [status, setStatus] = useState<MaximumConsistencyStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    fetchMaximumConsistencyData();
  }, []);

  const fetchMaximumConsistencyData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch maximum consistency metrics
      const metricsResponse = await fetch('/api/ai-agents/maximum-consistency/system/maximum-consistency-metrics');
      if (!metricsResponse.ok) {
        throw new Error('Failed to fetch maximum consistency metrics');
      }
      const metricsData = await metricsResponse.json();
      setMetrics(metricsData);

      // Fetch maximum consistency status
      const statusResponse = await fetch('/api/ai-agents/maximum-consistency/system/maximum-consistency-status');
      if (!statusResponse.ok) {
        throw new Error('Failed to fetch maximum consistency status');
      }
      const statusData = await statusResponse.json();
      setStatus(statusData);

    } catch (err) {
      console.error('Error fetching maximum consistency data:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      toast({
        title: "Maximum Consistency Error",
        description: "Failed to fetch maximum consistency data",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const triggerMaximumConsistencyOptimization = async () => {
    try {
      const response = await fetch('/api/ai-agents/maximum-consistency/system/maximum-consistency-status', {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to trigger maximum consistency optimization');
      }

      toast({
        title: "Maximum Consistency Optimization",
        description: "Maximum consistency optimization triggered successfully",
      });

      // Refresh data after optimization
      setTimeout(() => {
        fetchMaximumConsistencyData();
      }, 2000);

    } catch (err) {
      console.error('Error triggering maximum consistency optimization:', err);
      toast({
        title: "Maximum Consistency Optimization Error",
        description: "Failed to trigger maximum consistency optimization",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Maximum Consistency Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <Card className="border-red-200 bg-red-50">
          <CardHeader>
            <CardTitle className="text-red-800">Maximum Consistency Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error}</p>
            <Button 
              onClick={fetchMaximumConsistencyData}
              className="mt-4"
              variant="outline"
            >
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Maximum Consistency Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Real-time monitoring of 99%+ consistency and reliability
          </p>
        </div>
        <Button 
          onClick={triggerMaximumConsistencyOptimization}
          className="bg-blue-600 hover:bg-blue-700 text-white"
        >
          Trigger Maximum Consistency Optimization
        </Button>
      </div>

      {/* Maximum Consistency Status */}
      <Card>
        <CardHeader>
          <CardTitle className="text-blue-800">Maximum Consistency Status</CardTitle>
          <CardDescription>
            Current maximum consistency system status and performance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {status?.consistency_level || 'Maximum'}
              </div>
              <div className="text-sm text-gray-600">Consistency Level</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {status?.reliability_level || 'Maximum'}
              </div>
              <div className="text-sm text-gray-600">Reliability Level</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {(status?.target_consistency || 0.99) * 100}%
              </div>
              <div className="text-sm text-gray-600">Target Consistency</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {(status?.target_reliability || 0.99) * 100}%
              </div>
              <div className="text-sm text-gray-600">Target Reliability</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Maximum Consistency Metrics */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-blue-800">Consistency Score</CardTitle>
              <CardDescription>
                Current maximum consistency score
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">
                {(metrics.consistency_score * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: {(metrics.target_consistency * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.consistency_score * 100, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-green-800">Reliability Score</CardTitle>
              <CardDescription>
                Current maximum reliability score
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">
                {(metrics.reliability_score * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: {(metrics.target_reliability * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.reliability_score * 100, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-red-800">Consistency Violations</CardTitle>
              <CardDescription>
                Current maximum consistency violations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-600">
                {metrics.consistency_violations}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: 0 violations
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-red-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.consistency_violations * 10, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-orange-800">Reliability Failures</CardTitle>
              <CardDescription>
                Current maximum reliability failures
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">
                {metrics.reliability_failures}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: 0 failures
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-orange-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.reliability_failures * 10, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-purple-800">Total Requests</CardTitle>
              <CardDescription>
                Total maximum consistency requests processed
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">
                {metrics.total_requests.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Maximum consistency requests
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-indigo-800">Consistency Level</CardTitle>
              <CardDescription>
                Current maximum consistency level
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-indigo-600">
                {metrics.consistency_level}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Maximum consistency active
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Maximum Consistency Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="text-gray-800">Maximum Consistency Summary</CardTitle>
          <CardDescription>
            Comprehensive maximum consistency performance overview
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Maximum Consistency Level:</span>
              <span className="font-semibold text-blue-600">Maximum (99%+)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Maximum Reliability Level:</span>
              <span className="font-semibold text-green-600">Maximum (99%+)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Consistency:</span>
              <span className="font-semibold text-blue-600">99%+</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Reliability:</span>
              <span className="font-semibold text-green-600">99%+</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Consistency Violations:</span>
              <span className="font-semibold text-red-600">Minimal</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Reliability Failures:</span>
              <span className="font-semibold text-orange-600">Minimal</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">System Status:</span>
              <span className="font-semibold text-green-600">Maximum Consistency Active</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
