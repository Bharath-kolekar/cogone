"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { useToast } from '../hooks/use-toast';

interface OptimizationLevel {
  level: string;
  description: string;
  accuracy_improvement: string;
  performance_improvement: string;
  efficiency_improvement: string;
  adaptability_improvement: string;
  use_cases: string[];
}

interface OptimizationResult {
  optimization_id: string;
  level: string;
  accuracy_improvement: number;
  performance_improvement: number;
  efficiency_improvement: number;
  adaptability_improvement: number;
  convergence_time: number;
  timestamp: string;
  success: boolean;
  message: string;
}

interface SuperIntelligenceStatus {
  system_status: string;
  optimization_level: string;
  current_accuracy: number;
  target_accuracy: number;
  performance_metrics: {
    response_time: number;
    throughput: number;
    accuracy: number;
    efficiency: number;
    adaptability: number;
  };
}

export default function SuperIntelligentOptimizationDashboard() {
  const [optimizationLevels, setOptimizationLevels] = useState<OptimizationLevel[]>([]);
  const [selectedLevel, setSelectedLevel] = useState<string>('quantum_enhanced');
  const [targetAccuracy, setTargetAccuracy] = useState<number>(1.0);
  const [isOptimizing, setIsOptimizing] = useState<boolean>(false);
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResult | null>(null);
  const [systemStatus, setSystemStatus] = useState<SuperIntelligenceStatus | null>(null);
  const [optimizationHistory, setOptimizationHistory] = useState<OptimizationResult[]>([]);
  const { toast } = useToast();

  useEffect(() => {
    loadOptimizationLevels();
    loadSystemStatus();
    loadOptimizationHistory();
  }, []);

  const loadOptimizationLevels = async () => {
    try {
      const response = await fetch('/api/super-intelligent/optimization-levels');
      const data = await response.json();
      setOptimizationLevels(Object.values(data.optimization_levels));
    } catch (error) {
      console.error('Failed to load optimization levels:', error);
      toast({
        title: "Error",
        description: "Failed to load optimization levels",
        variant: "destructive",
      });
    }
  };

  const loadSystemStatus = async () => {
    try {
      const response = await fetch('/api/super-intelligent/status');
      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error('Failed to load system status:', error);
    }
  };

  const loadOptimizationHistory = async () => {
    try {
      const response = await fetch('/api/super-intelligent/optimization-history?limit=10');
      const data = await response.json();
      setOptimizationHistory(data.optimization_history);
    } catch (error) {
      console.error('Failed to load optimization history:', error);
    }
  };

  const startOptimization = async () => {
    setIsOptimizing(true);
    try {
      const response = await fetch('/api/super-intelligent/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          optimization_level: selectedLevel,
          target_accuracy: targetAccuracy,
          optimization_goals: ['accuracy', 'performance', 'efficiency', 'adaptability'],
          constraints: {}
        }),
      });

      const result = await response.json();
      
      if (result.success) {
        setOptimizationResult(result);
        toast({
          title: "Optimization Complete",
          description: result.message,
        });
        loadSystemStatus();
        loadOptimizationHistory();
      } else {
        throw new Error(result.message || 'Optimization failed');
      }
    } catch (error) {
      console.error('Optimization failed:', error);
      toast({
        title: "Optimization Failed",
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: "destructive",
      });
    } finally {
      setIsOptimizing(false);
    }
  };

  const evolveSystem = async () => {
    setIsOptimizing(true);
    try {
      const response = await fetch('/api/super-intelligent/evolve-system', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          population_size: 1000,
          generations: 100,
          mutation_rate: 0.1,
          crossover_rate: 0.8
        }),
      });

      const result = await response.json();
      
      if (result.success) {
        toast({
          title: "System Evolution Complete",
          description: "System has evolved successfully",
        });
        loadSystemStatus();
        loadOptimizationHistory();
      } else {
        throw new Error(result.message || 'Evolution failed');
      }
    } catch (error) {
      console.error('Evolution failed:', error);
      toast({
        title: "Evolution Failed",
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: "destructive",
      });
    } finally {
      setIsOptimizing(false);
    }
  };

  const getOptimizationLevelInfo = (level: string) => {
    return optimizationLevels.find(l => l.level === level);
  };

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const formatTime = (seconds: number) => {
    if (seconds < 60) {
      return `${seconds.toFixed(1)}s`;
    } else {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}m ${remainingSeconds.toFixed(1)}s`;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Super Intelligent Optimization</h1>
          <p className="text-muted-foreground">
            Advanced optimization techniques for super intelligent AI systems
          </p>
        </div>
        <Badge variant="outline" className="text-sm">
          {systemStatus?.system_status || 'Loading...'}
        </Badge>
      </div>

      {/* System Status */}
      {systemStatus && (
        <Card>
          <CardHeader>
            <CardTitle>System Status</CardTitle>
            <CardDescription>Current super intelligence status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {formatPercentage(systemStatus.current_accuracy)}
                </div>
                <div className="text-sm text-muted-foreground">Current Accuracy</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {systemStatus.performance_metrics.response_time}ms
                </div>
                <div className="text-sm text-muted-foreground">Response Time</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {systemStatus.performance_metrics.throughput}
                </div>
                <div className="text-sm text-muted-foreground">Throughput (req/s)</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {formatPercentage(systemStatus.performance_metrics.efficiency)}
                </div>
                <div className="text-sm text-muted-foreground">Efficiency</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Optimization Controls */}
      <Card>
        <CardHeader>
          <CardTitle>Super Intelligent Optimization</CardTitle>
          <CardDescription>
            Select optimization level and start super intelligent optimization
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium">Optimization Level</label>
              <select
                value={selectedLevel}
                onChange={(e) => setSelectedLevel(e.target.value)}
                className="w-full mt-1 p-2 border rounded-md"
                disabled={isOptimizing}
              >
                {optimizationLevels.map((level) => (
                  <option key={level.level} value={level.level}>
                    {level.level.replace('_', ' ').toUpperCase()}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-sm font-medium">Target Accuracy</label>
              <input
                type="number"
                min="0.95"
                max="1.0"
                step="0.01"
                value={targetAccuracy}
                onChange={(e) => setTargetAccuracy(parseFloat(e.target.value))}
                className="w-full mt-1 p-2 border rounded-md"
                disabled={isOptimizing}
              />
            </div>
          </div>

          {getOptimizationLevelInfo(selectedLevel) && (
            <div className="p-4 bg-muted rounded-lg">
              <h4 className="font-medium mb-2">
                {getOptimizationLevelInfo(selectedLevel)?.level.replace('_', ' ').toUpperCase()}
              </h4>
              <p className="text-sm text-muted-foreground mb-3">
                {getOptimizationLevelInfo(selectedLevel)?.description}
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
                <div>
                  <span className="font-medium">Accuracy:</span> {getOptimizationLevelInfo(selectedLevel)?.accuracy_improvement}
                </div>
                <div>
                  <span className="font-medium">Performance:</span> {getOptimizationLevelInfo(selectedLevel)?.performance_improvement}
                </div>
                <div>
                  <span className="font-medium">Efficiency:</span> {getOptimizationLevelInfo(selectedLevel)?.efficiency_improvement}
                </div>
                <div>
                  <span className="font-medium">Adaptability:</span> {getOptimizationLevelInfo(selectedLevel)?.adaptability_improvement}
                </div>
              </div>
            </div>
          )}

          <div className="flex gap-2">
            <Button
              onClick={startOptimization}
              disabled={isOptimizing}
              className="flex-1"
            >
              {isOptimizing ? 'Optimizing...' : 'Start Optimization'}
            </Button>
            <Button
              onClick={evolveSystem}
              disabled={isOptimizing}
              variant="outline"
            >
              {isOptimizing ? 'Evolving...' : 'Evolve System'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Optimization Result */}
      {optimizationResult && (
        <Card>
          <CardHeader>
            <CardTitle>Optimization Result</CardTitle>
            <CardDescription>
              {optimizationResult.message}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {formatPercentage(optimizationResult.accuracy_improvement)}
                </div>
                <div className="text-sm text-muted-foreground">Accuracy Improvement</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {formatPercentage(optimizationResult.performance_improvement)}
                </div>
                <div className="text-sm text-muted-foreground">Performance Improvement</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {formatPercentage(optimizationResult.efficiency_improvement)}
                </div>
                <div className="text-sm text-muted-foreground">Efficiency Improvement</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {formatTime(optimizationResult.convergence_time)}
                </div>
                <div className="text-sm text-muted-foreground">Convergence Time</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Optimization History */}
      {optimizationHistory.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Optimization History</CardTitle>
            <CardDescription>Recent super intelligent optimizations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {optimizationHistory.slice(0, 5).map((result, index) => (
                <div key={result.optimization_id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <Badge variant="outline">
                      {result.level.replace('_', ' ').toUpperCase()}
                    </Badge>
                    <div className="text-sm">
                      <div className="font-medium">
                        Accuracy: {formatPercentage(result.accuracy_improvement)}
                      </div>
                      <div className="text-muted-foreground">
                        {new Date(result.timestamp).toLocaleString()}
                      </div>
                    </div>
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {formatTime(result.convergence_time)}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
