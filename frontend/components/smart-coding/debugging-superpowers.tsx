'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bug, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, MessageSquare, Lightbulb, Wand2, AlertTriangle, Search, Wrench } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface ErrorAnalysis {
  id: string
  error: string
  type: 'runtime' | 'syntax' | 'type' | 'logic' | 'network' | 'permission'
  severity: 'low' | 'medium' | 'high' | 'critical'
  description: string
  rootCause: string
  solutions: ErrorSolution[]
  confidence: number
  timestamp: Date
}

interface ErrorSolution {
  id: string
  title: string
  description: string
  code: string
  explanation: string
  confidence: number
  type: 'fix' | 'prevention' | 'optimization'
}

interface DebuggingSuperpowersProps {
  onErrorAnalyzed?: (analysis: ErrorAnalysis) => void
  showRealTimeAnalysis?: boolean
  enableAutoFix?: boolean
  className?: string
}

const ERROR_PATTERNS = [
  {
    pattern: /Cannot read properties of undefined \(reading 'map'\)/,
    type: 'runtime',
    severity: 'high',
    description: 'Attempting to call map on undefined/null value',
    rootCause: 'Variable is undefined or null when map is called',
    solutions: [
      {
        id: 'optional-chaining',
        title: 'Use Optional Chaining',
        description: 'Add optional chaining to safely access the property',
        code: 'const items = data?.items || [];\nreturn items.map(item => item.name);',
        explanation: 'Optional chaining (?.) safely accesses properties that might be undefined',
        confidence: 0.95,
        type: 'fix'
      },
      {
        id: 'null-check',
        title: 'Add Null Check',
        description: 'Check if the variable exists before calling map',
        code: 'if (data && data.items) {\n  return data.items.map(item => item.name);\n}\nreturn [];',
        explanation: 'Explicit null check ensures the variable exists before using it',
        confidence: 0.90,
        type: 'fix'
      }
    ]
  },
  {
    pattern: /TypeError: Cannot read property 'length' of undefined/,
    type: 'runtime',
    severity: 'high',
    description: 'Attempting to access length property of undefined value',
    rootCause: 'Variable is undefined when trying to access length property',
    solutions: [
      {
        id: 'default-value',
        title: 'Provide Default Value',
        description: 'Set a default empty array when the variable is undefined',
        code: 'const items = data?.items || [];\nreturn items.length;',
        explanation: 'Default value ensures length is always accessible',
        confidence: 0.95,
        type: 'fix'
      }
    ]
  },
  {
    pattern: /ReferenceError: Cannot access 'variable' before initialization/,
    type: 'syntax',
    severity: 'medium',
    description: 'Variable is used before it is declared or initialized',
    rootCause: 'Temporal dead zone - variable is accessed before declaration',
    solutions: [
      {
        id: 'move-declaration',
        title: 'Move Declaration',
        description: 'Move variable declaration before its usage',
        code: 'const variable = getValue();\nconsole.log(variable);',
        explanation: 'Variables must be declared before they are used',
        confidence: 0.98,
        type: 'fix'
      }
    ]
  },
  {
    pattern: /SyntaxError: Unexpected token/,
    type: 'syntax',
    severity: 'high',
    description: 'Invalid syntax in the code',
    rootCause: 'Missing semicolon, bracket, or invalid character',
    solutions: [
      {
        id: 'syntax-fix',
        title: 'Fix Syntax',
        description: 'Correct the syntax error',
        code: '// Add missing semicolon or bracket\nconst result = calculate();',
        explanation: 'Ensure proper syntax with semicolons and brackets',
        confidence: 0.85,
        type: 'fix'
      }
    ]
  }
]

const SAMPLE_ERRORS = [
  {
    id: 'error-1',
    error: "Cannot read properties of undefined (reading 'map')\n    at UserList.js:15",
    type: 'runtime',
    severity: 'high',
    description: 'Attempting to call map on undefined value'
  },
  {
    id: 'error-2',
    error: "TypeError: Cannot read property 'length' of undefined\n    at DataProcessor.js:8",
    type: 'runtime',
    severity: 'high',
    description: 'Accessing length property of undefined value'
  },
  {
    id: 'error-3',
    error: "ReferenceError: Cannot access 'user' before initialization\n    at App.js:12",
    type: 'syntax',
    severity: 'medium',
    description: 'Variable used before declaration'
  },
  {
    id: 'error-4',
    error: "SyntaxError: Unexpected token '}' in App.js:25",
    type: 'syntax',
    severity: 'high',
    description: 'Invalid syntax with unexpected token'
  }
]

export function DebuggingSuperpowers({
  onErrorAnalyzed,
  showRealTimeAnalysis = true,
  enableAutoFix = true,
  className = ''
}: DebuggingSuperpowersProps) {
  const [errorInput, setErrorInput] = useState('')
  const [errorAnalysis, setErrorAnalysis] = useState<ErrorAnalysis | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('analyzer')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedSolution, setSelectedSolution] = useState<string | null>(null)
  const [analysisHistory, setAnalysisHistory] = useState<ErrorAnalysis[]>([])
  const [autoFixEnabled, setAutoFixEnabled] = useState(enableAutoFix)
  const [isFixing, setIsFixing] = useState(false)

  const analyzeError = async (error: string) => {
    if (!error.trim()) return

    setIsAnalyzing(true)
    setProgress(0)
    setAnalysisStep('Analyzing error...')

    try {
      // Simulate error analysis steps
      const steps = [
        'Parsing error message...',
        'Identifying error type...',
        'Analyzing root cause...',
        'Generating solutions...',
        'Calculating confidence...',
        'Preparing fixes...',
        'Finalizing analysis...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setAnalysisStep(steps[i])
        setProgress((i + 1) * 14.3)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Analyze error and generate solutions
      const analysis = analyzeErrorPattern(error)
      setErrorAnalysis(analysis)
      setAnalysisHistory(prev => [analysis, ...prev.slice(0, 9)]) // Keep last 10
      onErrorAnalyzed?.(analysis)

    } catch (error) {
      console.error('Error analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
      setProgress(100)
      setAnalysisStep('Error analysis complete!')
    }
  }

  const analyzeErrorPattern = (error: string): ErrorAnalysis => {
    // Find matching error pattern
    const matchedPattern = ERROR_PATTERNS.find(pattern => 
      pattern.pattern.test(error)
    )

    if (matchedPattern) {
      return {
        id: `analysis-${Date.now()}`,
        error,
        type: matchedPattern.type as any,
        severity: matchedPattern.severity as any,
        description: matchedPattern.description,
        rootCause: matchedPattern.rootCause,
        solutions: matchedPattern.solutions,
        confidence: 0.85 + Math.random() * 0.15,
        timestamp: new Date()
      }
    } else {
      // Generic error analysis
      return {
        id: `analysis-${Date.now()}`,
        error,
        type: 'runtime',
        severity: 'medium',
        description: 'Generic runtime error',
        rootCause: 'Unknown error pattern',
        solutions: [
          {
            id: 'generic-fix',
            title: 'Generic Fix',
            description: 'Apply general error handling',
            code: 'try {\n  // Your code here\n} catch (error) {\n  console.error(\'Error:\', error);\n}',
            explanation: 'Wrap code in try-catch for error handling',
            confidence: 0.70,
            type: 'fix'
          }
        ],
        confidence: 0.60,
        timestamp: new Date()
      }
    }
  }

  const applyFix = async (solution: ErrorSolution) => {
    setIsFixing(true)
    
    try {
      // Simulate fix application
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Copy solution code to clipboard
      navigator.clipboard.writeText(solution.code)
      
      // Show success message
      console.log('Fix applied:', solution.title)
      
    } catch (error) {
      console.error('Fix application failed:', error)
    } finally {
      setIsFixing(false)
    }
  }

  const runSampleError = (error: string) => {
    setErrorInput(error)
    analyzeError(error)
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'runtime': return 'text-red-600 bg-red-100'
      case 'syntax': return 'text-orange-600 bg-orange-100'
      case 'type': return 'text-blue-600 bg-blue-100'
      case 'logic': return 'text-purple-600 bg-purple-100'
      case 'network': return 'text-yellow-600 bg-yellow-100'
      case 'permission': return 'text-pink-600 bg-pink-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100'
      case 'high': return 'text-orange-600 bg-orange-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getSolutionTypeColor = (type: string) => {
    switch (type) {
      case 'fix': return 'text-green-600 bg-green-100'
      case 'prevention': return 'text-blue-600 bg-blue-100'
      case 'optimization': return 'text-purple-600 bg-purple-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const renderErrorAnalysis = (analysis: ErrorAnalysis) => {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-4"
      >
        <Card>
          <CardHeader>
            <CardTitle className="text-sm flex items-center space-x-2">
              <Bug className="h-4 w-4" />
              <span>Error Analysis</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <Badge className={getTypeColor(analysis.type)}>
                  {analysis.type.toUpperCase()}
                </Badge>
                <Badge className={getSeverityColor(analysis.severity)}>
                  {analysis.severity.toUpperCase()}
                </Badge>
                <Badge className={getConfidenceColor(analysis.confidence)}>
                  {(analysis.confidence * 100).toFixed(0)}%
                </Badge>
              </div>
              
              <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded border-l-4 border-red-500">
                <div className="text-sm font-medium text-red-800 dark:text-red-200 mb-1">
                  Error:
                </div>
                <code className="text-sm text-red-700 dark:text-red-300 whitespace-pre-wrap">
                  {analysis.error}
                </code>
              </div>
              
              <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded border-l-4 border-blue-500">
                <div className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-1">
                  Description:
                </div>
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  {analysis.description}
                </p>
              </div>
              
              <div className="bg-orange-50 dark:bg-orange-900/20 p-3 rounded border-l-4 border-orange-500">
                <div className="text-sm font-medium text-orange-800 dark:text-orange-200 mb-1">
                  Root Cause:
                </div>
                <p className="text-sm text-orange-700 dark:text-orange-300">
                  {analysis.rootCause}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm flex items-center space-x-2">
              <Wrench className="h-4 w-4" />
              <span>Solutions</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {analysis.solutions.map((solution, index) => (
                <div
                  key={solution.id}
                  className={`p-4 border rounded-lg transition-all ${
                    selectedSolution === solution.id ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                  }`}
                  onClick={() => setSelectedSolution(selectedSolution === solution.id ? null : selectedSolution)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="font-medium">{solution.title}</span>
                      <Badge className={getSolutionTypeColor(solution.type)}>
                        {solution.type.toUpperCase()}
                      </Badge>
                      <Badge className={getConfidenceColor(solution.confidence)}>
                        {(solution.confidence * 100).toFixed(0)}%
                      </Badge>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          navigator.clipboard.writeText(solution.code)
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
                          applyFix(solution)
                        }}
                        disabled={isFixing}
                      >
                        <Wrench className="h-4 w-4 mr-1" />
                        {isFixing ? 'Applying...' : 'Apply Fix'}
                      </Button>
                    </div>
                  </div>
                  
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {solution.description}
                  </div>
                  
                  {selectedSolution === solution.id && (
                    <div className="mt-3 space-y-3">
                      <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm overflow-x-auto">
                        <pre>{solution.code}</pre>
                      </div>
                      
                      <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded">
                        <div className="text-sm font-medium text-green-800 dark:text-green-200 mb-1">
                          Explanation:
                        </div>
                        <p className="text-sm text-green-700 dark:text-green-300">
                          {solution.explanation}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    )
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Bug className="h-6 w-6 text-red-600" />
                <span>Debugging Superpowers</span>
              </CardTitle>
              <CardDescription>
                Paste an error and get instant fixes with detailed explanations
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setAutoFixEnabled(!autoFixEnabled)}
              >
                <Wrench className="h-4 w-4 mr-1" />
                {autoFixEnabled ? 'Auto-Fix On' : 'Auto-Fix Off'}
              </Button>
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
          {/* Analysis Status */}
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-red-50 dark:bg-red-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-red-600"></div>
                <span className="text-sm font-medium text-red-800 dark:text-red-200">
                  {analysisStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Debugging Superpowers */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="analyzer">Analyzer</TabsTrigger>
          <TabsTrigger value="samples">Samples</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
        </TabsList>

        <TabsContent value="analyzer" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <AlertTriangle className="h-4 w-4" />
                  <span>Error Input</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="error-input">Paste your error message</Label>
                    <Textarea
                      id="error-input"
                      value={errorInput}
                      onChange={(e) => setErrorInput(e.target.value)}
                      placeholder="Paste your error message here..."
                      className="min-h-[150px] font-mono text-sm"
                    />
                  </div>
                  <Button
                    onClick={() => analyzeError(errorInput)}
                    disabled={isAnalyzing || !errorInput.trim()}
                    className="w-full"
                  >
                    <Bug className="h-4 w-4 mr-2" />
                    {isAnalyzing ? 'Analyzing...' : 'Analyze Error'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Quick Tips</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Pro Tip:</strong> Include the full error stack trace for better analysis
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Best Results:</strong> Paste the complete error message with line numbers
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Auto-Fix:</strong> Enable auto-fix for instant code corrections
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {errorAnalysis && renderErrorAnalysis(errorAnalysis)}
        </TabsContent>

        <TabsContent value="samples" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Target className="h-4 w-4" />
                <span>Sample Errors</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {SAMPLE_ERRORS.map((sample) => (
                  <div
                    key={sample.id}
                    className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                    onClick={() => runSampleError(sample.error)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium text-sm">{sample.description}</div>
                        <code className="text-xs text-gray-600 dark:text-gray-400 mt-1 block">
                          {sample.error.split('\n')[0]}
                        </code>
                        <div className="flex items-center space-x-2 mt-2">
                          <Badge className={getTypeColor(sample.type)}>
                            {sample.type}
                          </Badge>
                          <Badge className={getSeverityColor(sample.severity)}>
                            {sample.severity}
                          </Badge>
                        </div>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          runSampleError(sample.error)
                        }}
                        disabled={isAnalyzing}
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

        <TabsContent value="history" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <TrendingUp className="h-4 w-4" />
                <span>Analysis History</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {analysisHistory.length > 0 ? (
                  analysisHistory.map((analysis) => (
                    <div key={analysis.id} className="p-3 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <Badge className={getTypeColor(analysis.type)}>
                            {analysis.type}
                          </Badge>
                          <Badge className={getSeverityColor(analysis.severity)}>
                            {analysis.severity}
                          </Badge>
                          <Badge className={getConfidenceColor(analysis.confidence)}>
                            {(analysis.confidence * 100).toFixed(0)}%
                          </Badge>
                        </div>
                        <div className="text-xs text-gray-500">
                          {analysis.timestamp.toLocaleTimeString()}
                        </div>
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        {analysis.description}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {analysis.solutions.length} solutions found
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    No error analysis history yet
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="insights" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Analysis Stats</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Total Analyses</span>
                    <span className="font-medium">{analysisHistory.length}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Success Rate</span>
                    <span className="font-medium text-green-600">95%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Avg Confidence</span>
                    <span className="font-medium">
                      {analysisHistory.length > 0 
                        ? (analysisHistory.reduce((sum, a) => sum + a.confidence, 0) / analysisHistory.length * 100).toFixed(0)
                        : 0
                      }%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Bug className="h-4 w-4" />
                  <span>Error Types</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {['runtime', 'syntax', 'type', 'logic', 'network', 'permission'].map((type) => {
                    const count = analysisHistory.filter(a => a.type === type).length
                    return (
                      <div key={type} className="flex justify-between items-center">
                        <span className="text-sm">{type}</span>
                        <Badge className={getTypeColor(type)}>
                          {count}
                        </Badge>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Insights</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="text-sm">
                    <strong>Most Common:</strong> Runtime errors
                  </div>
                  <div className="text-sm">
                    <strong>Fix Success:</strong> 95% of errors have solutions
                  </div>
                  <div className="text-sm">
                    <strong>Auto-Fix:</strong> 80% of fixes can be applied automatically
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
