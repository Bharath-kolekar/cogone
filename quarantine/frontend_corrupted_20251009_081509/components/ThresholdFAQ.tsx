"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';

interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: string;
}

export default function ThresholdFAQ() {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const faqItems: FAQItem[] = [
    {
      id: 'what-is-threshold',
      question: 'What is a threshold in AI?',
      answer: 'A threshold is like a "quality setting" for AI. Think of it like the quality setting on your phone camera - higher quality takes more time and uses more battery, but gives better results.',
      category: 'basics'
    },
    {
      id: 'why-different-thresholds',
      question: 'Why are there different threshold levels?',
      answer: 'Different tasks need different levels of accuracy. Asking "What\'s the weather?" doesn\'t need perfect accuracy, but asking "Should I invest my life savings?" definitely does!',
      category: 'basics'
    },
    {
      id: 'fast-vs-maximum',
      question: 'What\'s the difference between Fast (90%) and Maximum (99%)?',
      answer: 'Fast is like a quick text message - fast and good enough for most things. Maximum is like a formal letter - takes longer but is perfect. The 9% difference means Maximum makes 1 mistake per 100 answers, while Fast makes 10 mistakes per 100 answers.',
      category: 'comparison'
    },
    {
      id: 'when-use-fast',
      question: 'When should I use Fast (90%)?',
      answer: 'Use Fast for: customer support chat, social media posts, simple questions, testing new features, or when you need lots of responses quickly.',
      category: 'usage'
    },
    {
      id: 'when-use-optimized',
      question: 'When should I use Optimized (95%)?',
      answer: 'Use Optimized for: business emails, content writing, general analysis, most business tasks, or when you want good quality without the highest cost.',
      category: 'usage'
    },
    {
      id: 'when-use-maximum',
      question: 'When should I use Maximum (99%)?',
      answer: 'Use Maximum for: financial advice, medical consultation, legal documents, critical business decisions, or anything where mistakes could be expensive or dangerous.',
      category: 'usage'
    },
    {
      id: 'cost-difference',
      question: 'How much more expensive is Maximum vs Fast?',
      answer: 'Maximum costs 5x more than Fast ($0.05 vs $0.01 per request). But for critical decisions, the extra cost is worth it to avoid expensive mistakes.',
      category: 'cost'
    },
    {
      id: 'can-change-later',
      question: 'Can I change my threshold later?',
      answer: 'Yes! You can change your threshold anytime. You might start with Fast for testing, then upgrade to Optimized for regular use, and Maximum for important projects.',
      category: 'usage'
    },
    {
      id: 'speed-difference',
      question: 'How much slower is Maximum than Fast?',
      answer: 'Maximum takes 300-500ms (about half a second), while Fast takes 50-100ms (about a tenth of a second). For most people, this difference is barely noticeable.',
      category: 'performance'
    },
    {
      id: 'what-if-wrong-choice',
      question: 'What if I choose the wrong threshold?',
      answer: 'No problem! You can always change it. If you choose too low and get too many mistakes, just upgrade. If you choose too high and pay too much, just downgrade.',
      category: 'usage'
    },
    {
      id: 'billing-options',
      question: 'What are the billing options?',
      answer: 'Pay-per-use: Pay only for what you use (good for testing). Monthly: $29.99 for 10,000 requests (good for regular use). Yearly: $299.99 for 150,000 requests (best value for heavy use).',
      category: 'billing'
    },
    {
      id: 'recommendation',
      question: 'What do you recommend for most people?',
      answer: 'Start with Optimized (95%) - it\'s the sweet spot for most business tasks. You get good quality, reasonable speed, and fair cost. You can always adjust later based on your needs.',
      category: 'recommendation'
    }
  ];

  const categories = [
    { id: 'all', name: 'All Questions', count: faqItems.length },
    { id: 'basics', name: 'Basics', count: faqItems.filter(item => item.category === 'basics').length },
    { id: 'comparison', name: 'Comparison', count: faqItems.filter(item => item.category === 'comparison').length },
    { id: 'usage', name: 'When to Use', count: faqItems.filter(item => item.category === 'usage').length },
    { id: 'cost', name: 'Cost & Billing', count: faqItems.filter(item => item.category === 'cost' || item.category === 'billing').length },
    { id: 'performance', name: 'Performance', count: faqItems.filter(item => item.category === 'performance').length },
    { id: 'recommendation', name: 'Recommendations', count: faqItems.filter(item => item.category === 'recommendation').length }
  ];

  const filteredItems = selectedCategory === 'all' 
    ? faqItems 
    : faqItems.filter(item => item.category === selectedCategory);

  const toggleExpanded = (itemId: string) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(itemId)) {
      newExpanded.delete(itemId);
    } else {
      newExpanded.add(itemId);
    }
    setExpandedItems(newExpanded);
  };

  return (
    <div className="p-6 space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h1>
        <p className="text-lg text-gray-600">
          Simple answers to common questions about AI thresholds
        </p>
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2 justify-center">
        {categories.map((category) => (
          <Button
            key={category.id}
            variant={selectedCategory === category.id ? "default" : "outline"}
            size="sm"
            onClick={() => setSelectedCategory(category.id)}
            className="text-sm"
          >
            {category.name} ({category.count})
          </Button>
        ))}
      </div>

      {/* FAQ Items */}
      <div className="space-y-4">
        {filteredItems.map((item) => (
          <Card key={item.id} className="hover:shadow-md transition-shadow">
            <CardHeader 
              className="cursor-pointer"
              onClick={() => toggleExpanded(item.id)}
            >
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{item.question}</CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-gray-500"
                >
                  {expandedItems.has(item.id) ? '−' : '+'}
                </Button>
              </div>
            </CardHeader>
            {expandedItems.has(item.id) && (
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  {item.answer}
                </CardDescription>
              </CardContent>
            )}
          </Card>
        ))}
      </div>

      {/* Quick Tips */}
      <Card className="bg-blue-50 border-blue-200">
        <CardHeader>
          <CardTitle className="text-blue-800">💡 Quick Tips</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold text-blue-700 mb-2">Start Simple</h4>
              <p className="text-sm text-blue-600">
                Begin with Optimized (95%) for most tasks. You can always upgrade or downgrade later.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-blue-700 mb-2">Save Money</h4>
              <p className="text-sm text-blue-600">
                Use Fast (90%) for testing and simple tasks. Save Maximum (99%) for important decisions.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-blue-700 mb-2">Monitor Usage</h4>
              <p className="text-sm text-blue-600">
                Check your usage patterns. If you're using a lot, consider monthly or yearly plans.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-blue-700 mb-2">Ask for Help</h4>
              <p className="text-sm text-blue-600">
                Not sure which to choose? Contact support for personalized recommendations.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Still Have Questions */}
      <Card>
        <CardHeader>
          <CardTitle className="text-center">Still Have Questions?</CardTitle>
          <CardDescription className="text-center">
            We're here to help you choose the perfect threshold for your needs
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center">
          <div className="flex justify-center space-x-4">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white">
              Contact Support
            </Button>
            <Button variant="outline">
              Schedule a Call
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
