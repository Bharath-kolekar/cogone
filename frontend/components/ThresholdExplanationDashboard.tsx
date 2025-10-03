"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { useToast } from '../hooks/use-toast';

interface ExampleScenario {
  id: string;
  title: string;
  description: string;
  example: string;
  threshold: string;
  why: string;
  cost: string;
}

export default function ThresholdExplanationDashboard() {
  const [selectedScenario, setSelectedScenario] = useState<string>('customer_support');
  const { toast } = useToast();

  const scenarios: ExampleScenario[] = [
    {
      id: 'customer_support',
      title: 'Customer Support Chat',
      description: 'Helping customers with questions and problems',
      example: 'Customer asks: "I forgot my password, how do I reset it?"',
      threshold: 'Fast (90%)',
      why: 'Customers want quick answers. 90% accuracy is perfect for common questions.',
      cost: '$0.01 per question'
    },
    {
      id: 'financial_advice',
      title: 'Financial Investment Advice',
      description: 'Providing investment recommendations and analysis',
      example: 'User asks: "Should I invest $10,000 in Apple stock right now?"',
      threshold: 'Maximum (99%)',
      why: 'Money decisions need perfect accuracy. 99% precision prevents costly mistakes.',
      cost: '$0.05 per analysis'
    },
    {
      id: 'content_writing',
      title: 'Blog Post Writing',
      description: 'Creating articles and marketing content',
      example: 'User asks: "Write a blog post about healthy eating tips"',
      threshold: 'Optimized (95%)',
      why: 'Good quality content with reasonable speed. 95% accuracy is perfect for writing.',
      cost: '$0.02 per article'
    },
    {
      id: 'medical_consultation',
      title: 'Medical Health Consultation',
      description: 'Providing health advice and symptom analysis',
      example: 'User asks: "I have chest pain, should I go to the emergency room?"',
      threshold: 'Maximum (99%)',
      why: 'Health decisions are critical. 99% accuracy could save lives.',
      cost: '$0.05 per consultation'
    },
    {
      id: 'social_media',
      title: 'Social Media Posts',
      description: 'Creating posts for Twitter, Facebook, Instagram',
      example: 'User asks: "Create a fun post about our new product launch"',
      threshold: 'Fast (90%)',
      why: 'Social media needs quick, engaging content. 90% accuracy is sufficient.',
      cost: '$0.01 per post'
    },
    {
      id: 'legal_document',
      title: 'Legal Document Review',
      description: 'Reviewing contracts and legal documents',
      example: 'User asks: "Review this employment contract for any issues"',
      threshold: 'Maximum (99%)',
      why: 'Legal documents require perfect accuracy. 99% precision prevents legal problems.',
      cost: '$0.05 per document'
    }
  ];

  const thresholdExplanations = {
    fast: {
      name: 'Fast Processing (90%)',
      icon: '⚡',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200',
      description: 'Quick responses for everyday tasks',
      examples: [
        'Customer support chat',
        'Social media posts',
        'Basic questions',
        'High-volume tasks'
      ],
      pros: [
        'Very fast (50-100ms)',
        'Low cost ($0.01/request)',
        'Good for simple tasks',
        'Perfect for testing'
      ],
      cons: [
        'Lower accuracy (90%)',
        'Not for critical decisions',
        'May need corrections'
      ],
      bestFor: 'Everyday tasks, social media, customer support, testing'
    },
    optimized: {
      name: 'Optimized Balance (95%)',
      icon: '⚖️',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      description: 'Perfect balance of speed and accuracy',
      examples: [
        'Content writing',
        'Business emails',
        'General analysis',
        'Most applications'
      ],
      pros: [
        'Good speed (100-200ms)',
        'High accuracy (95%)',
        'Reasonable cost ($0.02/request)',
        'Works for most tasks'
      ],
      cons: [
        'Not perfect for critical tasks',
        'May need occasional corrections'
      ],
      bestFor: 'Most business tasks, content creation, general use'
    },
    maximum: {
      name: 'Maximum Precision (99%)',
      icon: '🎯',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200',
      description: 'Perfect accuracy for critical decisions',
      examples: [
        'Financial advice',
        'Medical consultation',
        'Legal documents',
        'Critical business decisions'
      ],
      pros: [
        'Perfect accuracy (99%)',
        'No mistakes',
        'Enterprise-grade',
        'Priority support'
      ],
      cons: [
        'Slower (300-500ms)',
        'Higher cost ($0.05/request)',
        'More expensive'
      ],
      bestFor: 'Critical decisions, financial, medical, legal, enterprise'
    }
  };

  const currentScenario = scenarios.find(s => s.id === selectedScenario);
  const currentThreshold = currentScenario ? 
    (currentScenario.threshold.includes('90%') ? 'fast' : 
     currentScenario.threshold.includes('95%') ? 'optimized' : 'maximum') : 'optimized';

  return (
    <div className="p-6 space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">AI Agent Thresholds Explained</h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Simple examples to help you choose the right precision level for your needs
        </p>
      </div>

      {/* Interactive Examples */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Real-World Examples</CardTitle>
          <CardDescription>
            Click on different scenarios to see which threshold works best
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {scenarios.map((scenario) => (
              <Button
                key={scenario.id}
                variant={selectedScenario === scenario.id ? "default" : "outline"}
                className={`h-auto p-4 text-left ${
                  selectedScenario === scenario.id 
                    ? 'bg-blue-600 text-white' 
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => setSelectedScenario(scenario.id)}
              >
                <div>
                  <div className="font-semibold mb-2">{scenario.title}</div>
                  <div className="text-sm opacity-90">{scenario.description}</div>
                </div>
              </Button>
            ))}
          </div>

          {currentScenario && (
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-4">{currentScenario.title}</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-700">Example Question:</h4>
                  <p className="text-gray-600 italic">"{currentScenario.example}"</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700">Recommended Threshold:</h4>
                  <p className="text-blue-600 font-semibold">{currentScenario.threshold}</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700">Why This Threshold:</h4>
                  <p className="text-gray-600">{currentScenario.why}</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700">Cost:</h4>
                  <p className="text-green-600 font-semibold">{currentScenario.cost}</p>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Threshold Explanations */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {Object.entries(thresholdExplanations).map(([key, threshold]) => (
          <Card 
            key={key}
            className={`${threshold.bgColor} ${threshold.borderColor} ${
              currentThreshold === key ? 'ring-2 ring-blue-500' : ''
            }`}
          >
            <CardHeader>
              <div className="flex items-center space-x-2">
                <span className="text-2xl">{threshold.icon}</span>
                <CardTitle className={threshold.color}>{threshold.name}</CardTitle>
              </div>
              <CardDescription>{threshold.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Good for:</h4>
                <ul className="text-sm space-y-1">
                  {threshold.examples.map((example, index) => (
                    <li key={index} className="flex items-center">
                      <span className="w-1 h-1 bg-gray-500 rounded-full mr-2"></span>
                      {example}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="font-medium mb-2 text-green-600">Advantages:</h4>
                <ul className="text-sm space-y-1">
                  {threshold.pros.map((pro, index) => (
                    <li key={index} className="flex items-center">
                      <span className="text-green-500 mr-2">✓</span>
                      {pro}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4 className="font-medium mb-2 text-red-600">Considerations:</h4>
                <ul className="text-sm space-y-1">
                  {threshold.cons.map((con, index) => (
                    <li key={index} className="flex items-center">
                      <span className="text-red-500 mr-2">⚠</span>
                      {con}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="pt-2 border-t">
                <p className="text-sm font-medium text-gray-700">
                  Best for: {threshold.bestFor}
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Simple Comparison */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Simple Comparison</CardTitle>
          <CardDescription>
            Think of it like choosing a car: economy, standard, or luxury
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl mb-2">🚗</div>
              <h3 className="text-lg font-semibold mb-2">Fast (90%)</h3>
              <p className="text-sm text-gray-600 mb-4">Like a reliable economy car</p>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Speed:</span>
                  <span className="text-green-600">Very Fast</span>
                </div>
                <div className="flex justify-between">
                  <span>Accuracy:</span>
                  <span className="text-yellow-600">Good</span>
                </div>
                <div className="flex justify-between">
                  <span>Cost:</span>
                  <span className="text-green-600">Low</span>
                </div>
              </div>
            </div>

            <div className="text-center">
              <div className="text-4xl mb-2">🚙</div>
              <h3 className="text-lg font-semibold mb-2">Optimized (95%)</h3>
              <p className="text-sm text-gray-600 mb-4">Like a comfortable family car</p>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Speed:</span>
                  <span className="text-blue-600">Fast</span>
                </div>
                <div className="flex justify-between">
                  <span>Accuracy:</span>
                  <span className="text-blue-600">Very Good</span>
                </div>
                <div className="flex justify-between">
                  <span>Cost:</span>
                  <span className="text-blue-600">Medium</span>
                </div>
              </div>
            </div>

            <div className="text-center">
              <div className="text-4xl mb-2">🚗</div>
              <h3 className="text-lg font-semibold mb-2">Maximum (99%)</h3>
              <p className="text-sm text-gray-600 mb-4">Like a luxury sports car</p>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Speed:</span>
                  <span className="text-purple-600">Good</span>
                </div>
                <div className="flex justify-between">
                  <span>Accuracy:</span>
                  <span className="text-purple-600">Perfect</span>
                </div>
                <div className="flex justify-between">
                  <span>Cost:</span>
                  <span className="text-purple-600">High</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Cost Examples */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Cost Examples</CardTitle>
          <CardDescription>
            Real examples of how much different thresholds cost
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <h3 className="font-semibold mb-2">Fast (90%)</h3>
              <div className="space-y-2 text-sm">
                <div>100 questions = $1.00</div>
                <div>1,000 questions = $10.00</div>
                <div>10,000 questions = $100.00</div>
              </div>
            </div>

            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold mb-2">Optimized (95%)</h3>
              <div className="space-y-2 text-sm">
                <div>100 questions = $2.00</div>
                <div>1,000 questions = $20.00</div>
                <div>10,000 questions = $200.00</div>
              </div>
            </div>

            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <h3 className="font-semibold mb-2">Maximum (99%)</h3>
              <div className="space-y-2 text-sm">
                <div>100 questions = $5.00</div>
                <div>1,000 questions = $50.00</div>
                <div>10,000 questions = $500.00</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Decision Guide */}
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Quick Decision Guide</CardTitle>
          <CardDescription>
            Answer these questions to find your perfect threshold
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="font-semibold mb-2">🤔 Is this for critical decisions involving money, health, or legal matters?</h4>
              <p className="text-sm text-gray-600">
                <strong>Yes:</strong> Choose Maximum (99%) - Perfect accuracy for important decisions<br/>
                <strong>No:</strong> Continue to next question
              </p>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="font-semibold mb-2">⚡ Do you need very fast responses for high-volume tasks?</h4>
              <p className="text-sm text-gray-600">
                <strong>Yes:</strong> Choose Fast (90%) - Quick responses for simple tasks<br/>
                <strong>No:</strong> Continue to next question
              </p>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <h4 className="font-semibold mb-2">⚖️ Do you want a good balance of speed, accuracy, and cost?</h4>
              <p className="text-sm text-gray-600">
                <strong>Yes:</strong> Choose Optimized (95%) - Perfect for most business tasks<br/>
                <strong>No:</strong> Consider your specific needs
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <Button 
          className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3"
          onClick={() => toast({
            title: "Ready to Choose",
            description: "You're ready to select your threshold preference!",
          })}
        >
          I'm Ready to Choose
        </Button>
        <Button 
          variant="outline"
          className="px-8 py-3"
          onClick={() => toast({
            title: "Need Help",
            description: "Contact support for personalized recommendations",
          })}
        >
          I Need More Help
        </Button>
      </div>
    </div>
  );
}
