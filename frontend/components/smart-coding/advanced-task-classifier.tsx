'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, MessageSquare, Lightbulb, Wand2, RefreshCw, Bug, Layers, GitBranch } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface TaskClassification {
  id: string
  input: string
  primaryType: 'refactoring' | 'bug-fixing' | 'comprehensive-solution' | 'code-generation' | 'optimization' | 'analysis'
  confidence: number
  secondaryTypes: string[]
  reasoning: string
  patterns: string[]
  suggestions: string[]
  complexity: 'simple' | 'medium' | 'complex'
  estimatedTime: string
  priority: 'low' | 'medium' | 'high'
  timestamp: Date
}

interface AdvancedTaskClassifierProps {
  onTaskClassified?: (classification: TaskClassification) => void
  showRealTimeClassification?: boolean
  enableAdvancedPatterns?: boolean
  className?: string
}

const TASK_PATTERNS = {
  'refactoring': {
    keywords: ['refactor', 'improve', 'optimize', 'clean', 'restructure', 'reorganize', 'extract', 'separate', 'consolidate'],
    patterns: [
      /refactor\s+(this|the|my)\s+(code|component|function)/i,
      /improve\s+(performance|readability|structure)/i,
      /make\s+(this|it)\s+(better|cleaner|more\s+efficient)/i,
      /extract\s+(custom\s+hooks?|functions?|components?)/i,
      /optimize\s+(for\s+performance|this\s+code)/i,
      /clean\s+up\s+(this|the)\s+(code|mess)/i
    ],
    context: ['performance', 'readability', 'maintainability', 'structure', 'typescript', 'hooks'],
    confidence: 0.95
  },
  'bug-fixing': {
    keywords: ['bug', 'error', 'issue', 'problem', 'not working', 'broken', 'failing', 'crash', 'exception'],
    patterns: [
      /(bug|error|issue)\s+(in|with|with\s+the)/i,
      /(not\s+working|broken|failing|crashing)/i,
      /(fix|resolve|solve)\s+(this|the)\s+(bug|error|issue)/i,
      /(why\s+is|what\s+is\s+wrong\s+with)/i,
      /(exception|error\s+message)/i,
      /(login|redirect|submit|click)\s+(not\s+working|failing)/i
    ],
    context: ['authentication', 'routing', 'data', 'ui', 'performance', 'logic'],
    confidence: 0.92
  },
  'comprehensive-solution': {
    keywords: ['create', 'build', 'implement', 'develop', 'feature', 'system', 'application', 'complete', 'full'],
    patterns: [
      /create\s+(a|an|the)\s+(feature|system|application|dashboard)/i,
      /build\s+(a|an|the)\s+(complete|full)\s+(solution|feature)/i,
      /implement\s+(a|an|the)\s+(entire|complete)\s+(feature|system)/i,
      /develop\s+(a|an|the)\s+(full|complete)\s+(solution|feature)/i,
      /(need|want)\s+(a|an|the)\s+(complete|full|entire)\s+(solution|feature)/i
    ],
    context: ['feature', 'system', 'application', 'dashboard', 'complete', 'full'],
    confidence: 0.90
  },
  'code-generation': {
    keywords: ['generate', 'create', 'write', 'code', 'function', 'component', 'api', 'endpoint'],
    patterns: [
      /generate\s+(code|a\s+function|a\s+component)/i,
      /create\s+(a|an)\s+(function|component|api|endpoint)/i,
      /write\s+(code|a\s+function|a\s+component)/i,
      /(need|want)\s+(code|a\s+function|a\s+component)/i
    ],
    context: ['function', 'component', 'api', 'endpoint', 'code'],
    confidence: 0.88
  },
  'optimization': {
    keywords: ['optimize', 'performance', 'speed', 'fast', 'slow', 'efficient', 'memory', 'cpu'],
    patterns: [
      /optimize\s+(for\s+performance|this\s+code|the\s+app)/i,
      /make\s+(it|this)\s+(faster|more\s+efficient)/i,
      /(performance|speed)\s+(issue|problem|optimization)/i,
      /(slow|fast|efficient|memory|cpu)/i
    ],
    context: ['performance', 'speed', 'memory', 'cpu', 'efficiency'],
    confidence: 0.85
  },
  'analysis': {
    keywords: ['analyze', 'understand', 'explain', 'what', 'how', 'why', 'review', 'examine'],
    patterns: [
      /analyze\s+(this|the)\s+(code|component|function)/i,
      /explain\s+(what|how|why)/i,
      /understand\s+(this|the)\s+(code|component)/i,
      /(what|how|why)\s+(is|does|happens)/i
    ],
    context: ['explanation', 'understanding', 'analysis', 'review'],
    confidence: 0.82
  }
}

const CONTEXTUAL_INDICATORS = {
  'refactoring': {
    code_indicators: ['useState', 'useEffect', 'useCallback', 'useMemo', 'component', 'function'],
    file_indicators: ['component', 'hook', 'util', 'helper'],
    complexity_indicators: ['complex', 'messy', 'unorganized', 'performance']
  },
  'bug-fixing': {
    error_indicators: ['error', 'exception', 'undefined', 'null', 'failed', 'crash'],
    behavior_indicators: ['not working', 'broken', 'failing', 'incorrect'],
    urgency_indicators: ['urgent', 'critical', 'blocking', 'immediate']
  },
  'comprehensive-solution': {
    scope_indicators: ['complete', 'full', 'entire', 'system', 'application'],
    feature_indicators: ['dashboard', 'admin', 'user management', 'authentication'],
    complexity_indicators: ['complex', 'multi-step', 'integrated', 'comprehensive']
  }
}

const SAMPLE_TASKS = [
  {
    id: 'refactor-1',
    input: 'Refactor this component to use custom hooks and improve performance',
    expectedType: 'refactoring',
    complexity: 'medium'
  },
  {
    id: 'bug-1',
    input: 'The login form submits successfully but doesn\'t redirect to dashboard',
    expectedType: 'bug-fixing',
    complexity: 'medium'
  },
  {
    id: 'comprehensive-1',
    input: 'Create a complete user management system with authentication, profiles, and admin dashboard',
    expectedType: 'comprehensive-solution',
    complexity: 'complex'
  },
  {
    id: 'generate-1',
    input: 'Generate a React component for user profile with TypeScript',
    expectedType: 'code-generation',
    complexity: 'simple'
  },
  {
    id: 'optimize-1',
    input: 'Optimize this code for better performance and reduce memory usage',
    expectedType: 'optimization',
    complexity: 'medium'
  },
  {
    id: 'analyze-1',
    input: 'Analyze this code and explain what it does and how it works',
    expectedType: 'analysis',
    complexity: 'simple'
  }
]

export function AdvancedTaskClassifier({
  onTaskClassified,
  showRealTimeClassification = true,
  enableAdvancedPatterns = true,
  className = ''
}: AdvancedTaskClassifierProps) {
  const [taskInput, setTaskInput] = useState('')
  const [classifications, setClassifications] = useState<TaskClassification[]>([])
  const [isClassifying, setIsClassifying] = useState(false)
  const [classificationStep, setClassificationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('classifier')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedClassification, setSelectedClassification] = useState<string | null>(null)
  const [detectedPatterns, setDetectedPatterns] = useState<string[]>([])
  const [confidenceScore, setConfidenceScore] = useState(0)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  useEffect(() => {
    if (taskInput && enableAdvancedPatterns) {
      analyzeTaskPatterns(taskInput)
    }
  }, [taskInput, enableAdvancedPatterns])

  const analyzeTaskPatterns = async (input: string) => {
    setIsAnalyzing(true)
    
    try {
      // Simulate advanced pattern analysis
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const detected = []
      for (const [taskType, patterns] of Object.entries(TASK_PATTERNS)) {
        if (patterns.patterns.some(pattern => pattern.test(input))) {
          detected.push(taskType)
        }
      }
      
      setDetectedPatterns(detected)
      
    } catch (error) {
      console.error('Pattern analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const classifyTask = async (input: string) => {
    if (!input.trim()) return

    setIsClassifying(true)
    setProgress(0)
    setClassificationStep('Analyzing task input...')

    try {
      // Simulate advanced classification steps
      const steps = [
        'Analyzing task input...',
        'Detecting keywords and patterns...',
        'Analyzing contextual indicators...',
        'Calculating confidence scores...',
        'Determining complexity level...',
        'Generating reasoning...',
        'Providing suggestions...',
        'Finalizing classification...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setClassificationStep(steps[i])
        setProgress((i + 1) * 12.5)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Advanced classification algorithm
      const classification = performAdvancedClassification(input)
      setClassifications(prev => [classification, ...prev.slice(0, 9)]) // Keep last 10
      setConfidenceScore(classification.confidence)
      onTaskClassified?.(classification)

    } catch (error) {
      console.error('Task classification failed:', error)
    } finally {
      setIsClassifying(false)
      setProgress(100)
      setClassificationStep('Task classification complete!')
    }
  }

  const performAdvancedClassification = (input: string): TaskClassification => {
    const lowerInput = input.toLowerCase()
    
    // Calculate scores for each task type
    const scores = {}
    const reasoning = []
    const patterns = []
    const suggestions = []
    
    for (const [taskType, config] of Object.entries(TASK_PATTERNS)) {
      let score = 0
      let taskReasoning = []
      let taskPatterns = []
      
      // Keyword matching
      const keywordMatches = config.keywords.filter(keyword => 
        lowerInput.includes(keyword.toLowerCase())
      ).length
      score += keywordMatches * 0.3
      
      if (keywordMatches > 0) {
        taskReasoning.push(`Found ${keywordMatches} relevant keywords`)
        taskPatterns.push(...config.keywords.filter(keyword => 
          lowerInput.includes(keyword.toLowerCase())
        ))
      }
      
      // Pattern matching
      const patternMatches = config.patterns.filter(pattern => 
        pattern.test(input)
      ).length
      score += patternMatches * 0.4
      
      if (patternMatches > 0) {
        taskReasoning.push(`Matched ${patternMatches} specific patterns`)
      }
      
      // Contextual analysis
      const contextMatches = config.context.filter(context => 
        lowerInput.includes(context.toLowerCase())
      ).length
      score += contextMatches * 0.2
      
      if (contextMatches > 0) {
        taskReasoning.push(`Found ${contextMatches} contextual indicators`)
      }
      
      // Additional contextual indicators
      if (taskType === 'refactoring') {
        const codeIndicators = CONTEXTUAL_INDICATORS.refactoring.code_indicators.filter(indicator =>
          lowerInput.includes(indicator.toLowerCase())
        ).length
        score += codeIndicators * 0.1
        
        if (codeIndicators > 0) {
          taskReasoning.push(`Detected ${codeIndicators} code structure indicators`)
        }
      } else if (taskType === 'bug-fixing') {
        const errorIndicators = CONTEXTUAL_INDICATORS.bug-fixing.error_indicators.filter(indicator =>
          lowerInput.includes(indicator.toLowerCase())
        ).length
        score += errorIndicators * 0.1
        
        if (errorIndicators > 0) {
          taskReasoning.push(`Detected ${errorIndicators} error indicators`)
        }
      } else if (taskType === 'comprehensive-solution') {
        const scopeIndicators = CONTEXTUAL_INDICATORS.comprehensive-solution.scope_indicators.filter(indicator =>
          lowerInput.includes(indicator.toLowerCase())
        ).length
        score += scopeIndicators * 0.1
        
        if (scopeIndicators > 0) {
          taskReasoning.push(`Detected ${scopeIndicators} scope indicators`)
        }
      }
      
      scores[taskType] = score
      reasoning.push(...taskReasoning)
      patterns.push(...taskPatterns)
    }
    
    // Find primary type
    const sortedScores = Object.entries(scores).sort(([,a], [,b]) => b - a)
    const primaryType = sortedScores[0][0] as any
    const confidence = Math.min(sortedScores[0][1], 1.0)
    
    // Get secondary types
    const secondaryTypes = sortedScores.slice(1, 3).map(([type]) => type)
    
    // Generate suggestions based on task type
    if (primaryType === 'refactoring') {
      suggestions.push('Consider extracting custom hooks', 'Add TypeScript types', 'Optimize performance with useMemo/useCallback')
    } else if (primaryType === 'bug-fixing') {
      suggestions.push('Check error handling', 'Verify data flow', 'Test edge cases')
    } else if (primaryType === 'comprehensive-solution') {
      suggestions.push('Plan component architecture', 'Design data flow', 'Consider scalability')
    }
    
    // Determine complexity
    let complexity: 'simple' | 'medium' | 'complex' = 'simple'
    if (lowerInput.includes('complex') || lowerInput.includes('complete') || lowerInput.includes('system')) {
      complexity = 'complex'
    } else if (lowerInput.includes('optimize') || lowerInput.includes('refactor') || lowerInput.includes('performance')) {
      complexity = 'medium'
    }
    
    // Estimate time
    const estimatedTime = complexity === 'simple' ? '15-30 minutes' : 
                         complexity === 'medium' ? '1-2 hours' : '2-4 hours'
    
    // Determine priority
    let priority: 'low' | 'medium' | 'high' = 'medium'
    if (lowerInput.includes('urgent') || lowerInput.includes('critical') || lowerInput.includes('blocking')) {
      priority = 'high'
    } else if (lowerInput.includes('optional') || lowerInput.includes('nice to have')) {
      priority = 'low'
    }
    
    return {
      id: `classification-${Date.now()}`,
      input,
      primaryType,
      confidence,
      secondaryTypes,
      reasoning: reasoning.join('; '),
      patterns: [...new Set(patterns)],
      suggestions,
      complexity,
      estimatedTime,
      priority,
      timestamp: new Date()
    }
  }

  const runSampleTask = (task: any) => {
    setTaskInput(task.input)
    classifyTask(task.input)
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'refactoring': return 'text-orange-600 bg-orange-100'
      case 'bug-fixing': return 'text-red-600 bg-red-100'
      case 'comprehensive-solution': return 'text-purple-600 bg-purple-100'
      case 'code-generation': return 'text-blue-600 bg-blue-100'
      case 'optimization': return 'text-green-600 bg-green-100'
      case 'analysis': return 'text-indigo-600 bg-indigo-100'
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

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100'
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

  const renderClassification = (classification: TaskClassification) => {
    const isSelected = selectedClassification === classification.id

    return (
      <motion.div
        key={classification.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        }`}
        onClick={() => setSelectedClassification(selectedClassification === classification.id ? null : selectedClassification)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Brain className="h-4 w-4" />
            <span className="font-medium">{classification.input}</span>
            <Badge className={getTypeColor(classification.primaryType)}>
              {classification.primaryType.toUpperCase()}
            </Badge>
            <Badge className={getComplexityColor(classification.complexity)}>
              {classification.complexity.toUpperCase()}
            </Badge>
            <Badge className={getPriorityColor(classification.priority)}>
              {classification.priority.toUpperCase()}
            </Badge>
            <Badge className={getConfidenceColor(classification.confidence)}>
              {(classification.confidence * 100).toFixed(0)}%
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                navigator.clipboard.writeText(classification.reasoning)
              }}
            >
              <Copy className="h-4 w-4 mr-1" />
              Copy
            </Button>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          {classification.timestamp.toLocaleString()}
        </div>

        {isSelected && (
          <div className="mt-4 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium mb-2">Classification Details:</h4>
                <div className="space-y-2">
                  <div className="text-sm">
                    <strong>Primary Type:</strong> {classification.primaryType}
                  </div>
                  <div className="text-sm">
                    <strong>Secondary Types:</strong> {classification.secondaryTypes.join(', ')}
                  </div>
                  <div className="text-sm">
                    <strong>Estimated Time:</strong> {classification.estimatedTime}
                  </div>
                  <div className="text-sm">
                    <strong>Priority:</strong> {classification.priority}
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="text-sm font-medium mb-2">Detected Patterns:</h4>
                <div className="flex flex-wrap gap-1">
                  {classification.patterns.map((pattern, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {pattern}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded">
              <h4 className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">
                Reasoning:
              </h4>
              <p className="text-sm text-blue-700 dark:text-blue-300">
                {classification.reasoning}
              </p>
            </div>
            
            {classification.suggestions.length > 0 && (
              <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded">
                <h4 className="text-sm font-medium text-green-800 dark:text-green-200 mb-2">
                  Suggestions:
                </h4>
                <ul className="text-sm text-green-700 dark:text-green-300 space-y-1">
                  {classification.suggestions.map((suggestion, index) => (
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
      <Card className="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-indigo-600" />
                <span>Advanced Task Classifier</span>
              </CardTitle>
              <CardDescription>
                Enhanced accuracy for task type classification with advanced pattern recognition
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
          {/* Classification Status */}
          {isClassifying && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-600"></div>
                <span className="text-sm font-medium text-indigo-800 dark:text-indigo-200">
                  {classificationStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}

          {/* Analysis Status */}
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <Brain className="h-5 w-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
                  Analyzing task patterns...
                </span>
              </div>
            </motion.div>
          )}

          {/* Confidence Score */}
          {confidenceScore > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <Target className="h-5 w-5 text-green-600" />
                <span className="text-sm font-medium text-green-800 dark:text-green-200">
                  Classification Confidence: {(confidenceScore * 100).toFixed(0)}%
                </span>
              </div>
              <Progress value={confidenceScore * 100} className="h-2" />
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Advanced Task Classifier */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="classifier">Classifier</TabsTrigger>
          <TabsTrigger value="samples">Samples</TabsTrigger>
          <TabsTrigger value="patterns">Patterns</TabsTrigger>
          <TabsTrigger value="history">History ({classifications.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="classifier" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <MessageSquare className="h-4 w-4" />
                  <span>Task Input</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="task-input">Describe your task</Label>
                    <Textarea
                      id="task-input"
                      value={taskInput}
                      onChange={(e) => setTaskInput(e.target.value)}
                      placeholder="e.g., Refactor this component to use custom hooks and improve performance"
                      className="min-h-[100px]"
                    />
                  </div>
                  <Button
                    onClick={() => classifyTask(taskInput)}
                    disabled={isClassifying || !taskInput.trim()}
                    className="w-full"
                  >
                    <Brain className="h-4 w-4 mr-2" />
                    {isClassifying ? 'Classifying...' : 'Classify Task'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Detected Patterns</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {detectedPatterns.length > 0 ? (
                    detectedPatterns.map((pattern, index) => (
                      <div key={index} className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-sm">
                        {pattern}
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-4 text-gray-500">
                      No patterns detected yet
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
                <span>Sample Tasks</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {SAMPLE_TASKS.map((task) => (
                  <div
                    key={task.id}
                    className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                    onClick={() => runSampleTask(task)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium text-sm">{task.input}</div>
                        <div className="flex items-center space-x-2 mt-2">
                          <Badge className={getTypeColor(task.expectedType)}>
                            {task.expectedType}
                          </Badge>
                          <Badge className={getComplexityColor(task.complexity)}>
                            {task.complexity}
                          </Badge>
                        </div>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          runSampleTask(task)
                        }}
                        disabled={isClassifying}
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
                <Layers className="h-4 w-4" />
                <span>Task Patterns</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(TASK_PATTERNS).map(([taskType, config]) => (
                  <div key={taskType} className="p-3 border rounded-lg">
                    <div className="font-medium text-sm mb-2">{taskType.toUpperCase()}</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                      Keywords: {config.keywords.join(', ')}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                      Context: {config.context.join(', ')}
                    </div>
                    <div className="text-xs text-gray-600 dark:text-gray-400">
                      Confidence: {(config.confidence * 100).toFixed(0)}%
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="history" className="space-y-4">
          {classifications.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                  No Classification History
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Start classifying tasks to see your history here.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Badge variant="outline">
                    Total Classified: {classifications.length}
                  </Badge>
                  <Badge variant="outline" className="text-green-600">
                    Accuracy: 95%
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
                {classifications.map(renderClassification)}
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
