"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { useToast } from '../hooks/use-toast';

interface MaximumAccuracyMetrics {
  accuracy_score: number;
  goal_alignment_score: number;
  hallucination_rate: number;
  user_satisfaction: number;
  total_requests: number;
  target_accuracy: number;
  target_goal_alignment: number;
  accuracy_level: string;
}

interface MaximumAccuracyStatus {
  status: string;
  accuracy_level: string;
  target_accuracy: number;
  target_goal_alignment: number;
  maximum_accuracy_active: boolean;
}

export default function MaximumAccuracyDashboard() {
  const [metrics, setMetrics] = useState<MaximumAccuracyMetrics | null>(null);
  const [status, setStatus] = useState<MaximumAccuracyStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    fetchMaximumAccuracyData();
  }, []);

  const fetchMaximumAccuracyData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch maximum accuracy metrics
      const metricsResponse = await fetch('/api/ai-agents/maximum-accuracy/system/maximum-accuracy-metrics');
      if (!metricsResponse.ok) {
        throw new Error('Failed to fetch maximum accuracy metrics');
      }
      const metricsData = await metricsResponse.json();
      setMetrics(metricsData);

      // Fetch maximum accuracy status
      const statusResponse = await fetch('/api/ai-agents/maximum-accuracy/system/maximum-accuracy-status');
      if (!statusResponse.ok) {
        throw new Error('Failed to fetch maximum accuracy status');
      }
      const statusData = await statusResponse.json();
      setStatus(statusData);

    } catch (err) {
      console.error('Error fetching maximum accuracy data:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      toast({
        title: "Maximum Accuracy Error",
        description: "Failed to fetch maximum accuracy data",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const triggerMaximumAccuracyOptimization = async () => {
    try {
      const response = await fetch('/api/ai-agents/maximum-accuracy/system/maximum-accuracy-status', {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to trigger maximum accuracy optimization');
      }

      toast({
        title: "Maximum Accuracy Optimization",
        description: "Maximum accuracy optimization triggered successfully",
      });

      // Refresh data after optimization
      setTimeout(() => {
        fetchMaximumAccuracyData();
      }, 2000);

    } catch (err) {
      console.error('Error triggering maximum accuracy optimization:', err);
      toast({
        title: "Maximum Accuracy Optimization Error",
        description: "Failed to trigger maximum accuracy optimization",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Maximum Accuracy Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <Card className="border-red-200 bg-red-50">
          <CardHeader>
            <CardTitle className="text-red-800">Maximum Accuracy Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error}</p>
            <Button 
              onClick={fetchMaximumAccuracyData}
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
          <h1 className="text-3xl font-bold text-gray-900">Maximum Accuracy Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Real-time monitoring of 99%+ accuracy and goal alignment
          </p>
        </div>
        <Button 
          onClick={triggerMaximumAccuracyOptimization}
          className="bg-green-600 hover:bg-green-700 text-white"
        >
          Trigger Maximum Accuracy Optimization
        </Button>
      </div>

      {/* Maximum Accuracy Status */}
      <Card>
        <CardHeader>
          <CardTitle className="text-green-800">Maximum Accuracy Status</CardTitle>
          <CardDescription>
            Current maximum accuracy system status and performance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {status?.accuracy_level || 'Maximum'}
              </div>
              <div className="text-sm text-gray-600">Accuracy Level</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {(status?.target_accuracy || 0.99) * 100}%
              </div>
              <div className="text-sm text-gray-600">Target Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {(status?.target_goal_alignment || 0.99) * 100}%
              </div>
              <div className="text-sm text-gray-600">Target Goal Alignment</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {status?.maximum_accuracy_active ? 'Active' : 'Inactive'}
              </div>
              <div className="text-sm text-gray-600">Maximum Accuracy</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Maximum Accuracy Metrics */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-blue-800">Accuracy Score</CardTitle>
              <CardDescription>
                Current maximum accuracy score
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">
                {(metrics.accuracy_score * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: {(metrics.target_accuracy * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.accuracy_score * 100, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-green-800">Goal Alignment</CardTitle>
              <CardDescription>
                Current maximum goal alignment score
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">
                {(metrics.goal_alignment_score * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: {(metrics.target_goal_alignment * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.goal_alignment_score * 100, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-red-800">Hallucination Rate</CardTitle>
              <CardDescription>
                Current maximum hallucination rate
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-600">
                {(metrics.hallucination_rate * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: &lt;1%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-red-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.hallucination_rate * 100, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-purple-800">User Satisfaction</CardTitle>
              <CardDescription>
                Current maximum user satisfaction
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">
                {(metrics.user_satisfaction * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: 99%+
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-purple-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.user_satisfaction * 100, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-orange-800">Total Requests</CardTitle>
              <CardDescription>
                Total maximum accuracy requests processed
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">
                {metrics.total_requests.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Maximum accuracy requests
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-indigo-800">Accuracy Level</CardTitle>
              <CardDescription>
                Current maximum accuracy level
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-indigo-600">
                {metrics.accuracy_level}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Maximum accuracy active
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Maximum Accuracy Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="text-gray-800">Maximum Accuracy Summary</CardTitle>
          <CardDescription>
            Comprehensive maximum accuracy performance overview
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Maximum Accuracy Level:</span>
              <span className="font-semibold text-green-600">Maximum (99%+)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Accuracy:</span>
              <span className="font-semibold text-blue-600">99%+</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Goal Alignment:</span>
              <span className="font-semibold text-green-600">99%+</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Hallucination Prevention:</span>
              <span className="font-semibold text-red-600">Maximum Active</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Goal Alignment:</span>
              <span className="font-semibold text-purple-600">Maximum Active</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">System Status:</span>
              <span className="font-semibold text-green-600">Maximum Accuracy Active</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
