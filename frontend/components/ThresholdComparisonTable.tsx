"use client";

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';

interface ComparisonFeature {
  name: string;
  fast: string | number;
  optimized: string | number;
  maximum: string | number;
  description?: string;
}

export default function ThresholdComparisonTable() {
  const features: ComparisonFeature[] = [
    {
      name: 'Accuracy',
      fast: '90%',
      optimized: '95%',
      maximum: '99%',
      description: 'How often the AI gives correct answers'
    },
    {
      name: 'Speed',
      fast: '50-100ms',
      optimized: '100-200ms',
      maximum: '300-500ms',
      description: 'How fast you get responses'
    },
    {
      name: 'Cost per Request',
      fast: '$0.01',
      optimized: '$0.02',
      maximum: '$0.05',
      description: 'Price for each question you ask'
    },
    {
      name: 'Mistakes per 100 Answers',
      fast: '10 mistakes',
      optimized: '5 mistakes',
      maximum: '1 mistake',
      description: 'How many wrong answers you might get'
    },
    {
      name: 'Best For',
      fast: 'Quick tasks',
      optimized: 'Most business tasks',
      maximum: 'Critical decisions',
      description: 'What type of work it\'s perfect for'
    },
    {
      name: 'Example Use',
      fast: 'Customer chat',
      optimized: 'Email writing',
      maximum: 'Financial advice',
      description: 'Real-world examples'
    },
    {
      name: 'Monthly Cost (1,000 requests)',
      fast: '$10',
      optimized: '$20',
      maximum: '$50',
      description: 'Approximate monthly cost'
    }
  ];

  const getFeatureColor = (value: string | number, type: string) => {
    if (type === 'fast') {
      if (typeof value === 'string' && value.includes('$')) return 'text-green-600';
      if (typeof value === 'string' && value.includes('ms')) return 'text-green-600';
      if (typeof value === 'string' && value.includes('%')) return 'text-yellow-600';
      return 'text-green-600';
    }
    if (type === 'optimized') {
      if (typeof value === 'string' && value.includes('$')) return 'text-blue-600';
      if (typeof value === 'string' && value.includes('ms')) return 'text-blue-600';
      if (typeof value === 'string' && value.includes('%')) return 'text-blue-600';
      return 'text-blue-600';
    }
    if (type === 'maximum') {
      if (typeof value === 'string' && value.includes('$')) return 'text-purple-600';
      if (typeof value === 'string' && value.includes('ms')) return 'text-purple-600';
      if (typeof value === 'string' && value.includes('%')) return 'text-purple-600';
      return 'text-purple-600';
    }
    return 'text-gray-600';
  };

  const getBestValue = (featureName: string) => {
    switch (featureName) {
      case 'Accuracy':
        return 'maximum';
      case 'Speed':
        return 'fast';
      case 'Cost per Request':
        return 'fast';
      case 'Mistakes per 100 Answers':
        return 'maximum';
      case 'Best For':
        return 'optimized';
      case 'Example Use':
        return 'optimized';
      case 'Monthly Cost (1,000 requests)':
        return 'fast';
      default:
        return null;
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Threshold Comparison</h1>
        <p className="text-lg text-gray-600">
          Easy-to-understand comparison of all three threshold options
        </p>
      </div>

      {/* Mobile-Friendly Cards */}
      <div className="block md:hidden space-y-4">
        {[
          { id: 'fast', name: 'Fast (90%)', color: 'green', icon: '⚡' },
          { id: 'optimized', name: 'Optimized (95%)', color: 'blue', icon: '⚖️' },
          { id: 'maximum', name: 'Maximum (99%)', color: 'purple', icon: '🎯' }
        ].map((threshold) => (
          <Card key={threshold.id} className={`border-${threshold.color}-200 bg-${threshold.color}-50`}>
            <CardHeader>
              <CardTitle className={`text-${threshold.color}-800`}>
                {threshold.icon} {threshold.name}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {features.map((feature) => (
                <div key={feature.name} className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">{feature.name}:</span>
                  <span className={`text-sm font-semibold ${getFeatureColor(feature[threshold.id as keyof ComparisonFeature] || '', threshold.id)}`}>
                    {feature[threshold.id as keyof ComparisonFeature] || ''}
                  </span>
                </div>
              ))}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Desktop Table */}
      <div className="hidden md:block">
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-4 font-semibold text-gray-700">Feature</th>
                    <th className="text-center p-4 font-semibold text-green-700">Fast (90%)</th>
                    <th className="text-center p-4 font-semibold text-blue-700">Optimized (95%)</th>
                    <th className="text-center p-4 font-semibold text-purple-700">Maximum (99%)</th>
                  </tr>
                </thead>
                <tbody>
                  {features.map((feature, index) => (
                    <tr key={index} className="border-b hover:bg-gray-50">
                      <td className="p-4">
                        <div>
                          <div className="font-medium text-gray-900">{feature.name}</div>
                          {feature.description && (
                            <div className="text-xs text-gray-500 mt-1">{feature.description}</div>
                          )}
                        </div>
                      </td>
                      <td className="p-4 text-center">
                        <span className={`font-semibold ${getFeatureColor(feature.fast, 'fast')} ${
                          getBestValue(feature.name) === 'fast' ? 'bg-green-100 px-2 py-1 rounded' : ''
                        }`}>
                          {feature.fast}
                        </span>
                        {getBestValue(feature.name) === 'fast' && (
                          <div className="text-xs text-green-600 mt-1">Best</div>
                        )}
                      </td>
                      <td className="p-4 text-center">
                        <span className={`font-semibold ${getFeatureColor(feature.optimized, 'optimized')} ${
                          getBestValue(feature.name) === 'optimized' ? 'bg-blue-100 px-2 py-1 rounded' : ''
                        }`}>
                          {feature.optimized}
                        </span>
                        {getBestValue(feature.name) === 'optimized' && (
                          <div className="text-xs text-blue-600 mt-1">Best</div>
                        )}
                      </td>
                      <td className="p-4 text-center">
                        <span className={`font-semibold ${getFeatureColor(feature.maximum, 'maximum')} ${
                          getBestValue(feature.name) === 'maximum' ? 'bg-purple-100 px-2 py-1 rounded' : ''
                        }`}>
                          {feature.maximum}
                        </span>
                        {getBestValue(feature.name) === 'maximum' && (
                          <div className="text-xs text-purple-600 mt-1">Best</div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Simple Summary */}
      <Card className="bg-gray-50">
        <CardHeader>
          <CardTitle className="text-center">Simple Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl mb-2">⚡</div>
              <h3 className="font-semibold text-green-700 mb-2">Fast (90%)</h3>
              <p className="text-sm text-gray-600 mb-3">
                <strong>Cheapest & Fastest</strong><br/>
                Good for simple tasks
              </p>
              <div className="text-xs text-gray-500">
                Best for: Customer support, social media, testing
              </div>
            </div>

            <div className="text-center">
              <div className="text-4xl mb-2">⚖️</div>
              <h3 className="font-semibold text-blue-700 mb-2">Optimized (95%)</h3>
              <p className="text-sm text-gray-600 mb-3">
                <strong>Best Balance</strong><br/>
                Good quality + reasonable cost
              </p>
              <div className="text-xs text-gray-500">
                Best for: Most business tasks, content writing
              </div>
            </div>

            <div className="text-center">
              <div className="text-4xl mb-2">🎯</div>
              <h3 className="font-semibold text-purple-700 mb-2">Maximum (99%)</h3>
              <p className="text-sm text-gray-600 mb-3">
                <strong>Most Accurate</strong><br/>
                Perfect for critical decisions
              </p>
              <div className="text-xs text-gray-500">
                Best for: Financial advice, medical, legal
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recommendation */}
      <Card className="bg-blue-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-blue-800 text-center">Our Recommendation</CardTitle>
        </CardHeader>
        <CardContent className="text-center">
          <div className="text-lg text-blue-700 mb-4">
            <strong>Start with Optimized (95%)</strong>
          </div>
          <p className="text-blue-600 mb-4">
            It's the perfect balance for most people - good quality, reasonable speed, and fair cost.
            You can always upgrade or downgrade later based on your needs.
          </p>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white">
            Choose Optimized (95%)
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
