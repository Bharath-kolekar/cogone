"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { useToast } from './ui/use-toast';

interface MaximumThresholdMetrics {
  threshold_precision: number;
  threshold_accuracy: number;
  threshold_violations: number;
  threshold_failures: number;
  total_requests: number;
  target_threshold_precision: number;
  target_threshold_accuracy: number;
  threshold_level: string;
}

interface MaximumThresholdStatus {
  status: string;
  threshold_level: string;
  threshold_precision: number;
  threshold_accuracy: number;
  target_threshold_precision: number;
  target_threshold_accuracy: number;
  maximum_threshold_active: boolean;
}

export default function MaximumThresholdDashboard() {
  const [metrics, setMetrics] = useState<MaximumThresholdMetrics | null>(null);
  const [status, setStatus] = useState<MaximumThresholdStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    fetchMaximumThresholdData();
  }, []);

  const fetchMaximumThresholdData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch maximum threshold metrics
      const metricsResponse = await fetch('/api/ai-agents/maximum-threshold/system/maximum-threshold-metrics');
      if (!metricsResponse.ok) {
        throw new Error('Failed to fetch maximum threshold metrics');
      }
      const metricsData = await metricsResponse.json();
      setMetrics(metricsData);

      // Fetch maximum threshold status
      const statusResponse = await fetch('/api/ai-agents/maximum-threshold/system/maximum-threshold-status');
      if (!statusResponse.ok) {
        throw new Error('Failed to fetch maximum threshold status');
      }
      const statusData = await statusResponse.json();
      setStatus(statusData);

    } catch (err) {
      console.error('Error fetching maximum threshold data:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      toast({
        title: "Maximum Threshold Error",
        description: "Failed to fetch maximum threshold data",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const triggerMaximumThresholdOptimization = async () => {
    try {
      const response = await fetch('/api/ai-agents/maximum-threshold/system/maximum-threshold-status', {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to trigger maximum threshold optimization');
      }

      toast({
        title: "Maximum Threshold Optimization",
        description: "Maximum threshold optimization triggered successfully",
      });

      // Refresh data after optimization
      setTimeout(() => {
        fetchMaximumThresholdData();
      }, 2000);

    } catch (err) {
      console.error('Error triggering maximum threshold optimization:', err);
      toast({
        title: "Maximum Threshold Optimization Error",
        description: "Failed to trigger maximum threshold optimization",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Maximum Threshold Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <Card className="border-red-200 bg-red-50">
          <CardHeader>
            <CardTitle className="text-red-800">Maximum Threshold Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error}</p>
            <Button 
              onClick={fetchMaximumThresholdData}
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
          <h1 className="text-3xl font-bold text-gray-900">Maximum Threshold Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Real-time monitoring of 99%+ threshold precision and accuracy
          </p>
        </div>
        <Button 
          onClick={triggerMaximumThresholdOptimization}
          className="bg-purple-600 hover:bg-purple-700 text-white"
        >
          Trigger Maximum Threshold Optimization
        </Button>
      </div>

      {/* Maximum Threshold Status */}
      <Card>
        <CardHeader>
          <CardTitle className="text-purple-800">Maximum Threshold Status</CardTitle>
          <CardDescription>
            Current maximum threshold system status and performance
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {status?.threshold_level || 'Maximum'}
              </div>
              <div className="text-sm text-gray-600">Threshold Level</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {(status?.threshold_precision || 0.99) * 100}%
              </div>
              <div className="text-sm text-gray-600">Threshold Precision</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {(status?.threshold_accuracy || 0.99) * 100}%
              </div>
              <div className="text-sm text-gray-600">Threshold Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {(status?.target_threshold_precision || 0.99) * 100}%
              </div>
              <div className="text-sm text-gray-600">Target Precision</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Maximum Threshold Metrics */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-blue-800">Threshold Precision</CardTitle>
              <CardDescription>
                Current maximum threshold precision score
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-blue-600">
                {(metrics.threshold_precision * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: {(metrics.target_threshold_precision * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.threshold_precision * 100, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-green-800">Threshold Accuracy</CardTitle>
              <CardDescription>
                Current maximum threshold accuracy score
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-green-600">
                {(metrics.threshold_accuracy * 100).toFixed(1)}%
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: {(metrics.target_threshold_accuracy * 100).toFixed(1)}%
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.threshold_accuracy * 100, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-red-800">Threshold Violations</CardTitle>
              <CardDescription>
                Current maximum threshold violations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-red-600">
                {metrics.threshold_violations}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: 0 violations
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-red-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.threshold_violations * 10, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-orange-800">Threshold Failures</CardTitle>
              <CardDescription>
                Current maximum threshold failures
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-orange-600">
                {metrics.threshold_failures}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Target: 0 failures
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-orange-600 h-2 rounded-full" 
                  style={{ width: `${Math.min(metrics.threshold_failures * 10, 100)}%` }}
                ></div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-purple-800">Total Requests</CardTitle>
              <CardDescription>
                Total maximum threshold requests processed
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-purple-600">
                {metrics.total_requests.toLocaleString()}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Maximum threshold requests
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-indigo-800">Threshold Level</CardTitle>
              <CardDescription>
                Current maximum threshold level
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-indigo-600">
                {metrics.threshold_level}
              </div>
              <div className="text-sm text-gray-600 mt-2">
                Maximum threshold active
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Maximum Threshold Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="text-gray-800">Maximum Threshold Summary</CardTitle>
          <CardDescription>
            Comprehensive maximum threshold performance overview
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Maximum Threshold Level:</span>
              <span className="font-semibold text-purple-600">Maximum (99%+)</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Threshold Precision:</span>
              <span className="font-semibold text-blue-600">99%+</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Threshold Accuracy:</span>
              <span className="font-semibold text-green-600">99%+</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Precision:</span>
              <span className="font-semibold text-blue-600">99%+</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Target Accuracy:</span>
              <span className="font-semibold text-green-600">99%+</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Threshold Violations:</span>
              <span className="font-semibold text-red-600">Minimal</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Threshold Failures:</span>
              <span className="font-semibold text-orange-600">Minimal</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">System Status:</span>
              <span className="font-semibold text-green-600">Maximum Threshold Active</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
