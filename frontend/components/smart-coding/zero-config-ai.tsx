'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, MessageSquare, Lightbulb, Wand2 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface ZeroConfigRequest {
  id: string
  request: string
  type: 'ui' | 'functionality' | 'layout' | 'validation' | 'styling' | 'data'
  complexity: 'simple' | 'medium' | 'complex'
  generatedCode: string
  description: string
  confidence: number
  suggestions: string[]
  timestamp: Date
}

interface ZeroConfigAIProps {
  onCodeGenerated?: (code: ZeroConfigRequest) => void
  showRealTimeGeneration?: boolean
  enablePatternLearning?: boolean
  className?: string
}

const SAMPLE_REQUESTS = [
  {
    id: 'button-hover',
    request: 'Make the button change color when hovered',
    type: 'styling',
    complexity: 'simple',
    description: 'Add hover effect to button component'
  },
  {
    id: 'form-validation',
    request: 'Add form validation for the email field',
    type: 'validation',
    complexity: 'medium',
    description: 'Implement email validation with error messages'
  },
  {
    id: 'dashboard-layout',
    request: 'Create a dashboard layout with sidebar',
    type: 'layout',
    complexity: 'complex',
    description: 'Build responsive dashboard with navigation sidebar'
  },
  {
    id: 'loading-spinner',
    request: 'Add a loading spinner while data is fetching',
    type: 'ui',
    complexity: 'simple',
    description: 'Implement loading state with spinner animation'
  },
  {
    id: 'dark-mode',
    request: 'Add dark mode toggle to the header',
    type: 'functionality',
    complexity: 'medium',
    description: 'Implement dark mode toggle with theme persistence'
  },
  {
    id: 'user-profile',
    request: 'Create a user profile page with avatar upload and bio editing',
    type: 'data',
    complexity: 'complex',
    description: 'Build complete user profile with file upload and editing'
  }
]

const CONTEXT_PATTERNS = {
  'button': {
    patterns: ['hover', 'click', 'disabled', 'loading'],
    suggestions: ['Add hover effects', 'Implement click handlers', 'Add loading states']
  },
  'form': {
    patterns: ['validation', 'submission', 'error handling'],
    suggestions: ['Add form validation', 'Implement error messages', 'Add submission handling']
  },
  'layout': {
    patterns: ['responsive', 'sidebar', 'header', 'footer'],
    suggestions: ['Make responsive', 'Add navigation', 'Implement grid layout']
  },
  'data': {
    patterns: ['fetching', 'caching', 'error handling'],
    suggestions: ['Add data fetching', 'Implement caching', 'Add error boundaries']
  }
}

export function ZeroConfigAI({
  onCodeGenerated,
  showRealTimeGeneration = true,
  enablePatternLearning = true,
  className = ''
}: ZeroConfigAIProps) {
  const [userRequest, setUserRequest] = useState('')
  const [generatedRequests, setGeneratedRequests] = useState<ZeroConfigRequest[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStep, setGenerationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('generator')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedRequest, setSelectedRequest] = useState<string | null>(null)
  const [userPatterns, setUserPatterns] = useState<any>({})
  const [contextualSuggestions, setContextualSuggestions] = useState<string[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  useEffect(() => {
    if (userRequest && enablePatternLearning) {
      analyzeUserPatterns(userRequest)
    }
  }, [userRequest, enablePatternLearning])

  const analyzeUserPatterns = async (request: string) => {
    setIsAnalyzing(true)
    
    try {
      // Simulate pattern analysis
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const lowerRequest = request.toLowerCase()
      const detectedPatterns = []
      const suggestions = []
      
      // Analyze request for patterns
      for (const [pattern, data] of Object.entries(CONTEXT_PATTERNS)) {
        if (lowerRequest.includes(pattern)) {
          detectedPatterns.push(pattern)
          suggestions.push(...data.suggestions)
        }
      }
      
      setContextualSuggestions(suggestions)
      setUserPatterns(prev => ({
        ...prev,
        [request]: {
          patterns: detectedPatterns,
          suggestions: suggestions,
          timestamp: new Date()
        }
      }))
      
    } catch (error) {
      console.error('Pattern analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const generateCode = async (request: string) => {
    if (!request.trim()) return

    setIsGenerating(true)
    setProgress(0)
    setGenerationStep('Analyzing request...')

    try {
      // Simulate code generation steps
      const steps = [
        'Analyzing natural language request...',
        'Identifying code patterns and requirements...',
        'Determining complexity and scope...',
        'Generating contextual code...',
        'Applying user patterns and preferences...',
        'Optimizing for best practices...',
        'Adding error handling and validation...',
        'Finalizing generated code...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setGenerationStep(steps[i])
        setProgress((i + 1) * 12.5)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Generate mock code based on request
      const mockCode = generateMockCode(request)
      const requestType = determineRequestType(request)
      const complexity = determineComplexity(request)
      
      const generatedRequest: ZeroConfigRequest = {
        id: `req-${Date.now()}`,
        request,
        type: requestType,
        complexity,
        generatedCode: mockCode,
        description: generateDescription(request),
        confidence: 0.85 + Math.random() * 0.15,
        suggestions: generateSuggestions(request),
        timestamp: new Date()
      }

      setGeneratedRequests(prev => [...prev, generatedRequest])
      onCodeGenerated?.(generatedRequest)

    } catch (error) {
      console.error('Code generation failed:', error)
    } finally {
      setIsGenerating(false)
      setProgress(100)
      setGenerationStep('Code generation complete!')
    }
  }

  const generateMockCode = (request: string): string => {
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('button') && lowerRequest.includes('hover')) {
      return `// Button with hover effect
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export function Button({ children, onClick, variant = 'primary', disabled = false }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={\`
        px-4 py-2 rounded-md font-medium transition-colors duration-200
        \${variant === 'primary' 
          ? 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500' 
          : 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-2 focus:ring-gray-500'
        }
        \${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
      \`}
    >
      {children}
    </button>
  );
}`
    } else if (lowerRequest.includes('form') && lowerRequest.includes('validation')) {
      return `// Form with email validation
import React, { useState } from 'react';

interface FormData {
  email: string;
  name: string;
}

export function ContactForm() {
  const [formData, setFormData] = useState<FormData>({ email: '', name: '' });
  const [errors, setErrors] = useState<Partial<FormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Validate form
    const newErrors: Partial<FormData> = {};
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!validateEmail(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    if (!formData.name) {
      newErrors.name = 'Name is required';
    }
    
    setErrors(newErrors);
    
    if (Object.keys(newErrors).length === 0) {
      // Submit form
      console.log('Form submitted:', formData);
    }
    
    setIsSubmitting(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Name
        </label>
        <input
          type="text"
          id="name"
          value={formData.name}
          onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
        {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
      </div>
      
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          type="email"
          id="email"
          value={formData.email}
          onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
        {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email}</p>}
      </div>
      
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}`
    } else if (lowerRequest.includes('dashboard') && lowerRequest.includes('sidebar')) {
      return `// Dashboard layout with sidebar
import React, { useState } from 'react';
import { Menu, X, Home, Users, Settings, BarChart3 } from 'lucide-react';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Users', href: '/users', icon: Users },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className={\`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform \${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out lg:translate-x-0\`}>
        <div className="flex items-center justify-between h-16 px-4 border-b">
          <h1 className="text-xl font-bold text-gray-900">Dashboard</h1>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden"
          >
            <X className="h-6 w-6" />
          </button>
        </div>
        
        <nav className="mt-4">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <a
                key={item.name}
                href={item.href}
                className="flex items-center px-4 py-2 text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              >
                <Icon className="h-5 w-5 mr-3" />
                {item.name}
              </a>
            );
          })}
        </nav>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        <div className="flex items-center justify-between h-16 px-4 bg-white shadow-sm lg:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100"
          >
            <Menu className="h-6 w-6" />
          </button>
        </div>
        
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
}`
    } else {
      return `// Generated code for: ${request}
import React from 'react';

export function GeneratedComponent() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold text-gray-900">Generated Component</h1>
      <p className="text-gray-600">This component was generated based on your request: "${request}"</p>
    </div>
  );
}`
    }
  }

  const determineRequestType = (request: string): 'ui' | 'functionality' | 'layout' | 'validation' | 'styling' | 'data' => {
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('button') || lowerRequest.includes('hover') || lowerRequest.includes('color')) {
      return 'styling'
    } else if (lowerRequest.includes('form') || lowerRequest.includes('validation')) {
      return 'validation'
    } else if (lowerRequest.includes('dashboard') || lowerRequest.includes('layout') || lowerRequest.includes('sidebar')) {
      return 'layout'
    } else if (lowerRequest.includes('data') || lowerRequest.includes('fetch') || lowerRequest.includes('api')) {
      return 'data'
    } else if (lowerRequest.includes('function') || lowerRequest.includes('logic')) {
      return 'functionality'
    } else {
      return 'ui'
    }
  }

  const determineComplexity = (request: string): 'simple' | 'medium' | 'complex' => {
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('dashboard') || lowerRequest.includes('layout') || lowerRequest.includes('profile')) {
      return 'complex'
    } else if (lowerRequest.includes('form') || lowerRequest.includes('validation') || lowerRequest.includes('upload')) {
      return 'medium'
    } else {
      return 'simple'
    }
  }

  const generateDescription = (request: string): string => {
    const type = determineRequestType(request)
    const complexity = determineComplexity(request)
    
    return `${complexity} ${type} component: ${request}`
  }

  const generateSuggestions = (request: string): string[] => {
    const suggestions = []
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('button')) {
      suggestions.push('Add loading states', 'Implement click handlers', 'Add accessibility features')
    } else if (lowerRequest.includes('form')) {
      suggestions.push('Add form validation', 'Implement error messages', 'Add submission handling')
    } else if (lowerRequest.includes('dashboard')) {
      suggestions.push('Add responsive design', 'Implement navigation', 'Add user authentication')
    }
    
    return suggestions
  }

  const runSampleRequest = (request: string) => {
    setUserRequest(request)
    generateCode(request)
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'ui': return 'text-blue-600 bg-blue-100'
      case 'functionality': return 'text-green-600 bg-green-100'
      case 'layout': return 'text-purple-600 bg-purple-100'
      case 'validation': return 'text-orange-600 bg-orange-100'
      case 'styling': return 'text-pink-600 bg-pink-100'
      case 'data': return 'text-indigo-600 bg-indigo-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'simple': return 'text-green-600 bg-green-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'complex': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const renderGeneratedRequest = (request: ZeroConfigRequest) => {
    const isSelected = selectedRequest === request.id

    return (
      <motion.div
        key={request.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        }`}
        onClick={() => setSelectedRequest(selectedRequest === request.id ? null : selectedRequest)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <MessageSquare className="h-4 w-4" />
            <span className="font-medium">{request.description}</span>
            <Badge className={getTypeColor(request.type)}>
              {request.type.toUpperCase()}
            </Badge>
            <Badge className={getComplexityColor(request.complexity)}>
              {request.complexity.toUpperCase()}
            </Badge>
            <Badge className={getConfidenceColor(request.confidence)}>
              {(request.confidence * 100).toFixed(0)}%
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                navigator.clipboard.writeText(request.generatedCode)
              }}
            >
              <Copy className="h-4 w-4 mr-1" />
              Copy
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                const blob = new Blob([request.generatedCode], { type: 'text/plain' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `${request.type}.tsx`
                a.click()
                URL.revokeObjectURL(url)
              }}
            >
              <Download className="h-4 w-4 mr-1" />
              Download
            </Button>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          Request: "{request.request}"
        </div>

        {isSelected && (
          <div className="mt-3 space-y-3">
            <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm overflow-x-auto">
              <pre>{request.generatedCode}</pre>
            </div>
            
            {request.suggestions.length > 0 && (
              <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded">
                <div className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">
                  Suggestions:
                </div>
                <ul className="text-xs text-blue-600 dark:text-blue-400 space-y-1">
                  {request.suggestions.map((suggestion, index) => (
                    <li key={index}>• {suggestion}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </motion.div>
    )
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Wand2 className="h-6 w-6 text-green-600" />
                <span>Zero Configuration AI</span>
              </CardTitle>
              <CardDescription>
                Describe what you want in plain English - no prompt engineering needed
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowAdvanced(!showAdvanced)}
              >
                <Settings className="h-4 w-4 mr-1" />
                {showAdvanced ? 'Hide' : 'Show'} Advanced
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Generation Status */}
          {isGenerating && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"></div>
                <span className="text-sm font-medium text-green-800 dark:text-green-200">
                  {generationStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}

          {/* Pattern Analysis */}
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <Brain className="h-5 w-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
                  Analyzing user patterns...
                </span>
              </div>
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Zero Config AI */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="generator">Generator</TabsTrigger>
          <TabsTrigger value="samples">Samples</TabsTrigger>
          <TabsTrigger value="patterns">Patterns</TabsTrigger>
          <TabsTrigger value="generated">Generated ({generatedRequests.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="generator" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <MessageSquare className="h-4 w-4" />
                  <span>Natural Language Request</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="user-request">Describe what you want in plain English</Label>
                    <Textarea
                      id="user-request"
                      value={userRequest}
                      onChange={(e) => setUserRequest(e.target.value)}
                      placeholder="e.g., Make the button change color when hovered"
                      className="min-h-[100px]"
                    />
                  </div>
                  <Button
                    onClick={() => generateCode(userRequest)}
                    disabled={isGenerating || !userRequest.trim()}
                    className="w-full"
                  >
                    <Wand2 className="h-4 w-4 mr-2" />
                    {isGenerating ? 'Generating...' : 'Generate Code'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Contextual Suggestions</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {contextualSuggestions.length > 0 ? (
                    contextualSuggestions.map((suggestion, index) => (
                      <div key={index} className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-sm">
                        {suggestion}
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-4 text-gray-500">
                      Start typing to see contextual suggestions
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="samples" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Target className="h-4 w-4" />
                <span>Sample Requests</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {SAMPLE_REQUESTS.map((sample) => (
                  <div
                    key={sample.id}
                    className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                    onClick={() => runSampleRequest(sample.request)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <code className="text-sm font-mono">{sample.request}</code>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          {sample.description}
                        </p>
                        <div className="flex items-center space-x-2 mt-2">
                          <Badge className={getTypeColor(sample.type)}>
                            {sample.type}
                          </Badge>
                          <Badge className={getComplexityColor(sample.complexity)}>
                            {sample.complexity}
                          </Badge>
                        </div>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          runSampleRequest(sample.request)
                        }}
                        disabled={isGenerating}
                      >
                        <Play className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="patterns" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Brain className="h-4 w-4" />
                <span>Learned Patterns</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(userPatterns).map(([request, pattern]: [string, any]) => (
                  <div key={request} className="p-3 border rounded-lg">
                    <div className="text-sm font-medium mb-2">"{request}"</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                      Detected patterns: {pattern.patterns.join(', ')}
                    </div>
                    <div className="text-xs text-gray-500">
                      Suggestions: {pattern.suggestions.join(', ')}
                    </div>
                  </div>
                ))}
                {Object.keys(userPatterns).length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    No patterns learned yet. Start making requests to see pattern learning in action.
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="generated" className="space-y-4">
          {generatedRequests.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <Wand2 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                  No Code Generated Yet
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Describe what you want in plain English to see AI-generated code here.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Badge variant="outline">
                    Total Generated: {generatedRequests.length}
                  </Badge>
                  <Badge variant="outline" className="text-green-600">
                    Success Rate: 95%
                  </Badge>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowAdvanced(!showAdvanced)}
                  >
                    <Settings className="h-4 w-4 mr-1" />
                    {showAdvanced ? 'Hide' : 'Show'} Advanced
                  </Button>
                </div>
              </div>

              <div className="space-y-3">
                {generatedRequests.map(renderGeneratedRequest)}
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
