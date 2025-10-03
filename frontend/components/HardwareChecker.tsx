"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { useToast } from './ui/use-toast';

interface HardwareSpecs {
  cpu: {
    cores: number;
    speed: number;
    model: string;
  };
  memory: {
    total: number;
    available: number;
    speed: string;
  };
  storage: {
    total: number;
    available: number;
    type: string;
  };
  network: {
    speed: number;
    latency: number;
  };
}

interface SystemRequirements {
  minimum: {
    cpu: number;
    memory: number;
    storage: number;
    network: number;
  };
  recommended: {
    cpu: number;
    memory: number;
    storage: number;
    network: number;
  };
  optimal: {
    cpu: number;
    memory: number;
    storage: number;
    network: number;
  };
}

export default function HardwareChecker() {
  const [hardwareSpecs, setHardwareSpecs] = useState<HardwareSpecs | null>(null);
  const [systemRequirements, setSystemRequirements] = useState<SystemRequirements | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [compatibility, setCompatibility] = useState<{
    level: 'minimum' | 'recommended' | 'optimal' | 'insufficient';
    score: number;
    issues: string[];
    recommendations: string[];
  } | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    checkHardware();
  }, []);

  const checkHardware = async () => {
    try {
      setLoading(true);
      setError(null);

      // Simulate hardware detection (in real implementation, this would use system APIs)
      const mockSpecs: HardwareSpecs = {
        cpu: {
          cores: navigator.hardwareConcurrency || 4,
          speed: 2.5, // This would be detected from system
          model: 'Intel Core i5-8400' // This would be detected from system
        },
        memory: {
          total: 8, // This would be detected from system
          available: 6, // This would be detected from system
          speed: 'DDR4-2400' // This would be detected from system
        },
        storage: {
          total: 500, // This would be detected from system
          available: 400, // This would be detected from system
          type: 'SSD' // This would be detected from system
        },
        network: {
          speed: 100, // This would be detected from network test
          latency: 5 // This would be detected from network test
        }
      };

      const requirements: SystemRequirements = {
        minimum: {
          cpu: 4,
          memory: 8,
          storage: 100,
          network: 50
        },
        recommended: {
          cpu: 8,
          memory: 16,
          storage: 200,
          network: 100
        },
        optimal: {
          cpu: 12,
          memory: 32,
          storage: 500,
          network: 1000
        }
      };

      setHardwareSpecs(mockSpecs);
      setSystemRequirements(requirements);

      // Calculate compatibility
      const compatibilityResult = calculateCompatibility(mockSpecs, requirements);
      setCompatibility(compatibilityResult);

    } catch (err) {
      console.error('Error checking hardware:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      toast({
        title: "Hardware Check Error",
        description: "Failed to check hardware specifications",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const calculateCompatibility = (specs: HardwareSpecs, requirements: SystemRequirements) => {
    const issues: string[] = [];
    const recommendations: string[] = [];
    let score = 0;
    let level: 'minimum' | 'recommended' | 'optimal' | 'insufficient' = 'minimum';

    // Check CPU
    if (specs.cpu.cores >= requirements.optimal.cpu) {
      score += 25;
      level = 'optimal';
    } else if (specs.cpu.cores >= requirements.recommended.cpu) {
      score += 20;
      level = 'recommended';
    } else if (specs.cpu.cores >= requirements.minimum.cpu) {
      score += 15;
      level = 'minimum';
    } else {
      score += 5;
      level = 'insufficient';
      issues.push(`CPU: Only ${specs.cpu.cores} cores, need at least ${requirements.minimum.cpu}`);
      recommendations.push('Upgrade to a CPU with at least 4 cores');
    }

    // Check Memory
    if (specs.memory.total >= requirements.optimal.memory) {
      score += 25;
    } else if (specs.memory.total >= requirements.recommended.memory) {
      score += 20;
    } else if (specs.memory.total >= requirements.minimum.memory) {
      score += 15;
    } else {
      score += 5;
      issues.push(`RAM: Only ${specs.memory.total}GB, need at least ${requirements.minimum.memory}GB`);
      recommendations.push('Upgrade to at least 8GB RAM');
    }

    // Check Storage
    if (specs.storage.total >= requirements.optimal.storage) {
      score += 25;
    } else if (specs.storage.total >= requirements.recommended.storage) {
      score += 20;
    } else if (specs.storage.total >= requirements.minimum.storage) {
      score += 15;
    } else {
      score += 5;
      issues.push(`Storage: Only ${specs.storage.total}GB, need at least ${requirements.minimum.storage}GB`);
      recommendations.push('Upgrade to at least 100GB storage');
    }

    // Check Network
    if (specs.network.speed >= requirements.optimal.network) {
      score += 25;
    } else if (specs.network.speed >= requirements.recommended.network) {
      score += 20;
    } else if (specs.network.speed >= requirements.minimum.network) {
      score += 15;
    } else {
      score += 5;
      issues.push(`Network: Only ${specs.network.speed}Mbps, need at least ${requirements.minimum.network}Mbps`);
      recommendations.push('Upgrade to at least 50Mbps internet connection');
    }

    return {
      level,
      score,
      issues,
      recommendations
    };
  };

  const getCompatibilityColor = (level: string) => {
    switch (level) {
      case 'optimal': return 'text-green-600 bg-green-50 border-green-200';
      case 'recommended': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'minimum': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'insufficient': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getCompatibilityIcon = (level: string) => {
    switch (level) {
      case 'optimal': return '🎯';
      case 'recommended': return '✅';
      case 'minimum': return '⚠️';
      case 'insufficient': return '❌';
      default: return '❓';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Checking your hardware specifications...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <Card className="border-red-200 bg-red-50">
          <CardHeader>
            <CardTitle className="text-red-800">Hardware Check Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error}</p>
            <Button 
              onClick={checkHardware}
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
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Hardware Compatibility Checker</h1>
        <p className="text-lg text-gray-600">
          Check if your system can run the optimized AI agent system
        </p>
      </div>

      {/* Compatibility Result */}
      {compatibility && (
        <Card className={`${getCompatibilityColor(compatibility.level)}`}>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <span className="text-2xl">{getCompatibilityIcon(compatibility.level)}</span>
              <span>Compatibility: {compatibility.level.toUpperCase()}</span>
            </CardTitle>
            <CardDescription>
              Your system scored {compatibility.score}/100 for running the AI agent system
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span>Compatibility Score:</span>
                <span className="font-semibold">{compatibility.score}/100</span>
              </div>
              
              {compatibility.issues.length > 0 && (
                <div>
                  <h4 className="font-medium text-red-700 mb-2">Issues Found:</h4>
                  <ul className="text-sm space-y-1">
                    {compatibility.issues.map((issue, index) => (
                      <li key={index} className="flex items-center">
                        <span className="text-red-500 mr-2">⚠</span>
                        {issue}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {compatibility.recommendations.length > 0 && (
                <div>
                  <h4 className="font-medium text-blue-700 mb-2">Recommendations:</h4>
                  <ul className="text-sm space-y-1">
                    {compatibility.recommendations.map((recommendation, index) => (
                      <li key={index} className="flex items-center">
                        <span className="text-blue-500 mr-2">💡</span>
                        {recommendation}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Hardware Specifications */}
      {hardwareSpecs && (
        <Card>
          <CardHeader>
            <CardTitle>Your Current Hardware</CardTitle>
            <CardDescription>
              Detected hardware specifications
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-700">CPU</h4>
                  <div className="text-sm text-gray-600">
                    <div>Model: {hardwareSpecs.cpu.model}</div>
                    <div>Cores: {hardwareSpecs.cpu.cores}</div>
                    <div>Speed: {hardwareSpecs.cpu.speed}GHz</div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-700">Memory</h4>
                  <div className="text-sm text-gray-600">
                    <div>Total: {hardwareSpecs.memory.total}GB</div>
                    <div>Available: {hardwareSpecs.memory.available}GB</div>
                    <div>Speed: {hardwareSpecs.memory.speed}</div>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-700">Storage</h4>
                  <div className="text-sm text-gray-600">
                    <div>Total: {hardwareSpecs.storage.total}GB</div>
                    <div>Available: {hardwareSpecs.storage.available}GB</div>
                    <div>Type: {hardwareSpecs.storage.type}</div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-700">Network</h4>
                  <div className="text-sm text-gray-600">
                    <div>Speed: {hardwareSpecs.network.speed}Mbps</div>
                    <div>Latency: {hardwareSpecs.network.latency}ms</div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* System Requirements */}
      {systemRequirements && (
        <Card>
          <CardHeader>
            <CardTitle>System Requirements</CardTitle>
            <CardDescription>
              Required specifications for different deployment levels
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4 bg-yellow-50 rounded-lg">
                <h3 className="font-semibold text-yellow-700 mb-2">Minimum</h3>
                <div className="text-sm space-y-1">
                  <div>CPU: {systemRequirements.minimum.cpu} cores</div>
                  <div>RAM: {systemRequirements.minimum.memory}GB</div>
                  <div>Storage: {systemRequirements.minimum.storage}GB</div>
                  <div>Network: {systemRequirements.minimum.network}Mbps</div>
                </div>
                <div className="text-xs text-yellow-600 mt-2">
                  Basic functionality
                </div>
              </div>

              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <h3 className="font-semibold text-blue-700 mb-2">Recommended</h3>
                <div className="text-sm space-y-1">
                  <div>CPU: {systemRequirements.recommended.cpu} cores</div>
                  <div>RAM: {systemRequirements.recommended.memory}GB</div>
                  <div>Storage: {systemRequirements.recommended.storage}GB</div>
                  <div>Network: {systemRequirements.recommended.network}Mbps</div>
                </div>
                <div className="text-xs text-blue-600 mt-2">
                  Good performance
                </div>
              </div>

              <div className="text-center p-4 bg-green-50 rounded-lg">
                <h3 className="font-semibold text-green-700 mb-2">Optimal</h3>
                <div className="text-sm space-y-1">
                  <div>CPU: {systemRequirements.optimal.cpu} cores</div>
                  <div>RAM: {systemRequirements.optimal.memory}GB</div>
                  <div>Storage: {systemRequirements.optimal.storage}GB</div>
                  <div>Network: {systemRequirements.optimal.network}Mbps</div>
                </div>
                <div className="text-xs text-green-600 mt-2">
                  Best performance
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Deployment Recommendations */}
      <Card>
        <CardHeader>
          <CardTitle>Deployment Recommendations</CardTitle>
          <CardDescription>
            Based on your hardware specifications
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {compatibility?.level === 'optimal' && (
              <div className="p-4 bg-green-50 rounded-lg">
                <h4 className="font-semibold text-green-700 mb-2">🎯 Optimal Performance</h4>
                <p className="text-sm text-green-600">
                  Your system can run the AI agent system at maximum performance. 
                  You can use all features including Maximum (99%) threshold precision.
                </p>
              </div>
            )}

            {compatibility?.level === 'recommended' && (
              <div className="p-4 bg-blue-50 rounded-lg">
                <h4 className="font-semibold text-blue-700 mb-2">✅ Good Performance</h4>
                <p className="text-sm text-blue-600">
                  Your system can run the AI agent system well. 
                  You can use Optimized (95%) threshold precision with good performance.
                </p>
              </div>
            )}

            {compatibility?.level === 'minimum' && (
              <div className="p-4 bg-yellow-50 rounded-lg">
                <h4 className="font-semibold text-yellow-700 mb-2">⚠️ Basic Performance</h4>
                <p className="text-sm text-yellow-600">
                  Your system can run the AI agent system with basic performance. 
                  Consider using Fast (90%) threshold precision for better speed.
                </p>
              </div>
            )}

            {compatibility?.level === 'insufficient' && (
              <div className="p-4 bg-red-50 rounded-lg">
                <h4 className="font-semibold text-red-700 mb-2">❌ Insufficient Hardware</h4>
                <p className="text-sm text-red-600">
                  Your system may not be able to run the AI agent system properly. 
                  Consider upgrading your hardware or using cloud deployment.
                </p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <Button 
          onClick={checkHardware}
          className="bg-blue-600 hover:bg-blue-700 text-white"
        >
          Recheck Hardware
        </Button>
        <Button 
          variant="outline"
          onClick={() => toast({
            title: "Cloud Deployment",
            description: "Consider cloud deployment for better performance",
          })}
        >
          Cloud Deployment Options
        </Button>
      </div>
    </div>
  );
}
