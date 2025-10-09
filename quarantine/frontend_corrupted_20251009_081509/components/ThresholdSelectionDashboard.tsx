"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { useToast } from '../hooks/use-toast';

interface ThresholdOption {
  id: string;
  name: string;
  precision: number;
  accuracy: number;
  responseTime: string;
  computationalCost: string;
  price: number;
  features: string[];
  useCases: string[];
  description: string;
  recommended: boolean;
}

interface BillingOption {
  id: string;
  name: string;
  type: 'pay_per_use' | 'monthly' | 'yearly';
  price: number;
  requests: number;
  features: string[];
  savings?: number;
  popular?: boolean;
}

interface UserPreferences {
  thresholdType: string;
  billingOption: string;
  autoOptimize: boolean;
  notifications: boolean;
}

export default function ThresholdSelectionDashboard() {
  const [thresholdOptions, setThresholdOptions] = useState<ThresholdOption[]>([]);
  const [billingOptions, setBillingOptions] = useState<BillingOption[]>([]);
  const [userPreferences, setUserPreferences] = useState<UserPreferences>({
    thresholdType: 'optimized',
    billingOption: 'monthly',
    autoOptimize: true,
    notifications: true
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedThreshold, setSelectedThreshold] = useState<string>('optimized');
  const [selectedBilling, setSelectedBilling] = useState<string>('monthly');
  const { toast } = useToast();

  useEffect(() => {
    initializeDashboard();
  }, []);

  const initializeDashboard = async () => {
    try {
      setLoading(true);
      setError(null);

      // Initialize threshold options
      const thresholdData = [
        {
          id: 'maximum',
          name: 'Maximum Precision',
          precision: 0.99,
          accuracy: 0.99,
          responseTime: '300-500ms',
          computationalCost: 'High',
          price: 0.05,
          features: [
            '99%+ Precision & Accuracy',
            'Advanced Validation (8 layers)',
            'Maximum Reliability',
            'Enterprise Security',
            'Real-time Monitoring',
            'Priority Support'
          ],
          useCases: [
            'Financial Applications',
            'Healthcare Systems',
            'Legal Services',
            'Critical Business Operations',
            'Enterprise Solutions'
          ],
          description: 'Maximum precision and accuracy for critical applications requiring 99%+ reliability.',
          recommended: false
        },
        {
          id: 'optimized',
          name: 'Optimized Balance',
          precision: 0.95,
          accuracy: 0.95,
          responseTime: '100-200ms',
          computationalCost: 'Medium',
          price: 0.02,
          features: [
            '95%+ Precision & Accuracy',
            'Balanced Validation (4 layers)',
            'Good Reliability',
            'Standard Security',
            'Performance Monitoring',
            'Standard Support'
          ],
          useCases: [
            'General Applications',
            'Customer Support',
            'Content Generation',
            'Business Operations',
            'Standard Solutions'
          ],
          description: 'Optimal balance of precision, speed, and cost for most applications.',
          recommended: true
        },
        {
          id: 'fast',
          name: 'Fast Processing',
          precision: 0.90,
          accuracy: 0.90,
          responseTime: '50-100ms',
          computationalCost: 'Low',
          price: 0.01,
          features: [
            '90%+ Precision & Accuracy',
            'Fast Validation (2 layers)',
            'Basic Reliability',
            'Standard Security',
            'Basic Monitoring',
            'Community Support'
          ],
          useCases: [
            'High-Volume Systems',
            'Real-time Applications',
            'Development & Testing',
            'Prototype Solutions',
            'Cost-Sensitive Projects'
          ],
          description: 'Fast processing with good precision for high-volume or real-time applications.',
          recommended: false
        }
      ];

      // Initialize billing options
      const billingData = [
        {
          id: 'pay_per_use',
          name: 'Pay Per Use',
          type: 'pay_per_use' as const,
          price: 0.01,
          requests: 0,
          features: [
            'Pay only for what you use',
            'No monthly commitments',
            'Flexible scaling',
            'Perfect for testing',
            'Start with $0'
          ],
          description: 'Perfect for testing and low-volume usage.'
        },
        {
          id: 'monthly',
          name: 'Monthly Plan',
          type: 'monthly' as const,
          price: 29.99,
          requests: 10000,
          features: [
            '10,000 requests included',
            'Monthly billing',
            'Standard support',
            'Performance monitoring',
            '2x better value than pay-per-use'
          ],
          savings: 50,
          popular: true,
          description: 'Best value for regular usage with included requests.'
        },
        {
          id: 'yearly',
          name: 'Yearly Plan',
          type: 'yearly' as const,
          price: 299.99,
          requests: 150000,
          features: [
            '150,000 requests included',
            'Annual billing',
            'Priority support',
            'Advanced monitoring',
            '3x better value than monthly'
          ],
          savings: 67,
          description: 'Maximum value for high-volume usage with significant savings.'
        }
      ];

      setThresholdOptions(thresholdData);
      setBillingOptions(billingData);

    } catch (err) {
      console.error('Error initializing dashboard:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
      toast({
        title: "Dashboard Error",
        description: "Failed to initialize threshold selection dashboard",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleThresholdSelection = (thresholdId: string) => {
    setSelectedThreshold(thresholdId);
    setUserPreferences(prev => ({ ...prev, thresholdType: thresholdId }));
    
    toast({
      title: "Threshold Selected",
      description: `Selected ${thresholdOptions.find(t => t.id === thresholdId)?.name} threshold`,
    });
  };

  const handleBillingSelection = (billingId: string) => {
    setSelectedBilling(billingId);
    setUserPreferences(prev => ({ ...prev, billingOption: billingId }));
    
    toast({
      title: "Billing Selected",
      description: `Selected ${billingOptions.find(b => b.id === billingId)?.name} billing option`,
    });
  };

  const handleSavePreferences = async () => {
    try {
      // Save user preferences
      const response = await fetch('/api/user/preferences', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userPreferences),
      });

      if (!response.ok) {
        throw new Error('Failed to save preferences');
      }

      toast({
        title: "Preferences Saved",
        description: "Your threshold and billing preferences have been saved successfully",
      });

    } catch (err) {
      console.error('Error saving preferences:', err);
      toast({
        title: "Save Error",
        description: "Failed to save preferences. Please try again.",
        variant: "destructive",
      });
    }
  };

  const calculateTotalCost = () => {
    const selectedThresholdOption = thresholdOptions.find(t => t.id === selectedThreshold);
    const selectedBillingOption = billingOptions.find(b => b.id === selectedBilling);
    
    if (!selectedThresholdOption || !selectedBillingOption) return 0;
    
    if (selectedBillingOption.type === 'pay_per_use') {
      return selectedThresholdOption.price;
    }
    
    return selectedBillingOption.price;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Threshold Selection Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <Card className="border-red-200 bg-red-50">
          <CardHeader>
            <CardTitle className="text-red-800">Dashboard Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error}</p>
            <Button 
              onClick={initializeDashboard}
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
    <div className="p-6 space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">AI Agent Threshold Selection</h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Choose your preferred precision level and billing option to optimize your AI agent system
        </p>
      </div>

      {/* Threshold Options */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Select Threshold Precision</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {thresholdOptions.map((option) => (
            <Card 
              key={option.id} 
              className={`cursor-pointer transition-all duration-200 ${
                selectedThreshold === option.id 
                  ? 'ring-2 ring-blue-500 bg-blue-50' 
                  : 'hover:shadow-lg'
              } ${option.recommended ? 'border-green-500' : ''}`}
              onClick={() => handleThresholdSelection(option.id)}
            >
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{option.name}</CardTitle>
                  {option.recommended && (
                    <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded-full">
                      Recommended
                    </span>
                  )}
                </div>
                <CardDescription>{option.name}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Precision:</span>
                    <span className="ml-2 text-blue-600">{(option.precision * 100).toFixed(0)}%</span>
                  </div>
                  <div>
                    <span className="font-medium">Accuracy:</span>
                    <span className="ml-2 text-green-600">{(option.accuracy * 100).toFixed(0)}%</span>
                  </div>
                  <div>
                    <span className="font-medium">Response Time:</span>
                    <span className="ml-2 text-purple-600">{option.responseTime}</span>
                  </div>
                  <div>
                    <span className="font-medium">Cost:</span>
                    <span className="ml-2 text-orange-600">${option.price.toFixed(2)}/request</span>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-sm mb-2">Key Features:</h4>
                  <ul className="text-xs space-y-1">
                    {option.features.slice(0, 3).map((feature, index) => (
                      <li key={index} className="flex items-center">
                        <span className="w-1 h-1 bg-blue-500 rounded-full mr-2"></span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-medium text-sm mb-2">Best For:</h4>
                  <ul className="text-xs space-y-1">
                    {option.useCases.slice(0, 2).map((useCase, index) => (
                      <li key={index} className="flex items-center">
                        <span className="w-1 h-1 bg-green-500 rounded-full mr-2"></span>
                        {useCase}
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Billing Options */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">Select Billing Option</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {billingOptions.map((option) => (
            <Card 
              key={option.id} 
              className={`cursor-pointer transition-all duration-200 ${
                selectedBilling === option.id 
                  ? 'ring-2 ring-blue-500 bg-blue-50' 
                  : 'hover:shadow-lg'
              } ${option.popular ? 'border-green-500' : ''}`}
              onClick={() => handleBillingSelection(option.id)}
            >
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{option.name}</CardTitle>
                  {option.popular && (
                    <span className="bg-green-100 text-green-800 text-xs font-medium px-2 py-1 rounded-full">
                      Popular
                    </span>
                  )}
                </div>
                <CardDescription>{option.name}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">
                    ${option.price.toFixed(2)}
                    {option.type === 'pay_per_use' && <span className="text-sm text-gray-500">/request</span>}
                    {option.type === 'monthly' && <span className="text-sm text-gray-500">/month</span>}
                    {option.type === 'yearly' && <span className="text-sm text-gray-500">/year</span>}
                  </div>
                  {option.savings && (
                    <div className="text-sm text-green-600 font-medium">
                      Save {option.savings}%
                    </div>
                  )}
                </div>
                
                <div>
                  <h4 className="font-medium text-sm mb-2">Features:</h4>
                  <ul className="text-xs space-y-1">
                    {option.features.map((feature, index) => (
                      <li key={index} className="flex items-center">
                        <span className="w-1 h-1 bg-blue-500 rounded-full mr-2"></span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                
                {option.requests > 0 && (
                  <div className="text-center text-sm text-gray-600">
                    {option.requests.toLocaleString()} requests included
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Cost Summary */}
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">Cost Summary</CardTitle>
          <CardDescription>
            Estimated monthly cost based on your selections
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span>Selected Threshold:</span>
                <span className="font-medium">
                  {thresholdOptions.find(t => t.id === selectedThreshold)?.name}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Selected Billing:</span>
                <span className="font-medium">
                  {billingOptions.find(b => b.id === selectedBilling)?.name}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Precision Level:</span>
                <span className="font-medium">
                  {(thresholdOptions.find(t => t.id === selectedThreshold)?.precision || 0) * 100}%
                </span>
              </div>
              <div className="flex justify-between">
                <span>Response Time:</span>
                <span className="font-medium">
                  {thresholdOptions.find(t => t.id === selectedThreshold)?.responseTime}
                </span>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-lg font-bold">
                <span>Estimated Cost:</span>
                <span className="text-blue-600">
                  ${calculateTotalCost().toFixed(2)}
                  {selectedBilling === 'pay_per_use' ? '/request' : 
                   selectedBilling === 'monthly' ? '/month' : '/year'}
                </span>
              </div>
              {selectedBilling !== 'pay_per_use' && (
                <div className="text-sm text-gray-600">
                  Includes {billingOptions.find(b => b.id === selectedBilling)?.requests.toLocaleString()} requests
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <Button 
          onClick={handleSavePreferences}
          className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3"
        >
          Save Preferences
        </Button>
        <Button 
          variant="outline"
          className="px-8 py-3"
        >
          Preview Configuration
        </Button>
      </div>
    </div>
  );
}
