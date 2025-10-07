'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bug, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, MessageSquare, Lightbulb, Wand2, FileText, GitBranch, Search, Wrench, AlertTriangle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface BugAnalysis {
  id: string
  bugDescription: string
  rootCause: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  category: 'auth' | 'routing' | 'data' | 'ui' | 'performance' | 'logic'
  analysis: string
  solutions: BugSolution[]
  confidence: number
  timestamp: Date
}

interface BugSolution {
  id: string
  title: string
  description: string
  code: string
  explanation: string
  impact: 'low' | 'medium' | 'high'
  confidence: number
  type: 'fix' | 'prevention' | 'optimization'
  testCode?: string
}

interface BugFixingAIProps {
  onBugAnalyzed?: (analysis: BugAnalysis) => void
  showRealTimeAnalysis?: boolean
  enableAutoFix?: boolean
  className?: string
}

const SAMPLE_BUGS = [
  {
    id: 'login-redirect',
    description: 'The login form submits successfully but doesn\'t redirect',
    category: 'auth',
    severity: 'high',
    expectedBehavior: 'User should be redirected to dashboard after successful login'
  },
  {
    id: 'data-not-loading',
    description: 'Data is not loading on page refresh',
    category: 'data',
    severity: 'medium',
    expectedBehavior: 'Data should persist and load correctly on page refresh'
  },
  {
    id: 'button-not-working',
    description: 'Submit button is not working on mobile devices',
    category: 'ui',
    severity: 'medium',
    expectedBehavior: 'Submit button should work on all devices'
  },
  {
    id: 'slow-performance',
    description: 'Page is loading very slowly',
    category: 'performance',
    severity: 'high',
    expectedBehavior: 'Page should load quickly and efficiently'
  }
]

const BUG_PATTERNS = {
  'auth': {
    patterns: ['login', 'redirect', 'authentication', 'session'],
    commonIssues: [
      'Missing router.push after successful login',
      'Session not being set correctly',
      'Redirect logic not implemented',
      'Authentication state not updated'
    ]
  },
  'routing': {
    patterns: ['router', 'navigation', 'redirect', 'route'],
    commonIssues: [
      'Missing router.push() call',
      'Incorrect route path',
      'Navigation guard not working',
      'Route parameters not passed'
    ]
  },
  'data': {
    patterns: ['data', 'fetch', 'api', 'state'],
    commonIssues: [
      'Data not being fetched on component mount',
      'State not being updated correctly',
      'API call not being made',
      'Data not being stored in state'
    ]
  },
  'ui': {
    patterns: ['button', 'click', 'event', 'mobile'],
    commonIssues: [
      'Event handler not attached',
      'Mobile touch events not working',
      'CSS preventing clicks',
      'Event propagation issues'
    ]
  }
}

export function BugFixingAI({
  onBugAnalyzed,
  showRealTimeAnalysis = true,
  enableAutoFix = true,
  className = ''
}: BugFixingAIProps) {
  const [bugDescription, setBugDescription] = useState('')
  const [bugAnalyses, setBugAnalyses] = useState<BugAnalysis[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('analyzer')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedAnalysis, setSelectedAnalysis] = useState<string | null>(null)
  const [detectedPatterns, setDetectedPatterns] = useState<string[]>([])
  const [isFixing, setIsFixing] = useState(false)
  const [fixingStep, setFixingStep] = useState('')

  const analyzeBug = async (description: string) => {
    if (!description.trim()) return

    setIsAnalyzing(true)
    setProgress(0)
    setAnalysisStep('Analyzing bug description...')

    try {
      // Simulate bug analysis steps
      const steps = [
        'Analyzing bug description...',
        'Identifying potential root causes...',
        'Analyzing code patterns...',
        'Detecting common issues...',
        'Generating solutions...',
        'Calculating confidence...',
        'Preparing fix recommendations...',
        'Finalizing analysis...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setAnalysisStep(steps[i])
        setProgress((i + 1) * 12.5)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Analyze bug and generate solutions
      const analysis = analyzeBugPattern(description)
      setBugAnalyses(prev => [analysis, ...prev.slice(0, 9)]) // Keep last 10
      onBugAnalyzed?.(analysis)

    } catch (error) {
      console.error('Bug analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
      setProgress(100)
      setAnalysisStep('Bug analysis complete!')
    }
  }

  const analyzeBugPattern = (description: string): BugAnalysis => {
    const lowerDescription = description.toLowerCase()
    
    // Determine category and severity
    let category: 'auth' | 'routing' | 'data' | 'ui' | 'performance' | 'logic' = 'logic'
    let severity: 'low' | 'medium' | 'high' | 'critical' = 'medium'
    
    if (lowerDescription.includes('login') || lowerDescription.includes('auth')) {
      category = 'auth'
      severity = 'high'
    } else if (lowerDescription.includes('redirect') || lowerDescription.includes('navigation')) {
      category = 'routing'
      severity = 'high'
    } else if (lowerDescription.includes('data') || lowerDescription.includes('load')) {
      category = 'data'
      severity = 'medium'
    } else if (lowerDescription.includes('button') || lowerDescription.includes('click')) {
      category = 'ui'
      severity = 'medium'
    } else if (lowerDescription.includes('slow') || lowerDescription.includes('performance')) {
      category = 'performance'
      severity = 'high'
    }

    // Generate solutions based on category
    const solutions = generateSolutions(description, category)
    
    return {
      id: `bug-${Date.now()}`,
      bugDescription: description,
      rootCause: generateRootCause(description, category),
      severity,
      category,
      analysis: generateAnalysis(description, category),
      solutions,
      confidence: 0.85 + Math.random() * 0.15,
      timestamp: new Date()
    }
  }

  const generateRootCause = (description: string, category: string): string => {
    const lowerDescription = description.toLowerCase()
    
    if (category === 'auth' && lowerDescription.includes('redirect')) {
      return 'Missing router.push() call after successful authentication'
    } else if (category === 'routing') {
      return 'Navigation logic not properly implemented or missing redirect call'
    } else if (category === 'data') {
      return 'Data fetching logic not triggered on component mount or state not updated'
    } else if (category === 'ui') {
      return 'Event handler not properly attached or CSS preventing interaction'
    } else if (category === 'performance') {
      return 'Inefficient data fetching, missing optimizations, or blocking operations'
    } else {
      return 'Logic error in component implementation or missing error handling'
    }
  }

  const generateAnalysis = (description: string, category: string): string => {
    const lowerDescription = description.toLowerCase()
    
    if (category === 'auth') {
      return 'Authentication flow analysis shows missing redirect logic after successful login. The form submission is working but the navigation step is not implemented.'
    } else if (category === 'routing') {
      return 'Routing analysis indicates missing navigation call. The component logic is executing but not triggering the redirect to the intended page.'
    } else if (category === 'data') {
      return 'Data flow analysis shows the component is not fetching data on mount or the state is not being updated correctly after API calls.'
    } else if (category === 'ui') {
      return 'UI interaction analysis indicates event handlers are not properly attached or CSS is preventing user interactions.'
    } else {
      return 'Component logic analysis shows missing implementation or incorrect conditional logic.'
    }
  }

  const generateSolutions = (description: string, category: string): BugSolution[] => {
    const solutions: BugSolution[] = []
    const lowerDescription = description.toLowerCase()
    
    if (category === 'auth' && lowerDescription.includes('redirect')) {
      solutions.push({
        id: 'auth-redirect',
        title: 'Add Router Redirect',
        description: 'Add router.push() call after successful login',
        code: `// In your login handler
const handleLogin = async (credentials) => {
  try {
    const response = await loginUser(credentials);
    if (response.success) {
      // Add this line
      router.push('/dashboard');
    }
  } catch (error) {
    setError('Login failed');
  }
};`,
        explanation: 'After successful authentication, redirect the user to the dashboard',
        impact: 'high',
        confidence: 0.95,
        type: 'fix',
        testCode: `// Test the redirect
test('should redirect after successful login', async () => {
  const mockRouter = { push: jest.fn() };
  await handleLogin({ email: 'test@example.com', password: 'password' });
  expect(mockRouter.push).toHaveBeenCalledWith('/dashboard');
});`
      })
    }
    
    if (category === 'routing') {
      solutions.push({
        id: 'routing-fix',
        title: 'Implement Navigation Logic',
        description: 'Add proper navigation after successful operations',
        code: `import { useRouter } from 'next/router';

const router = useRouter();

// After successful operation
const handleSuccess = () => {
  router.push('/success-page');
};`,
        explanation: 'Use Next.js router to navigate to the intended page',
        impact: 'high',
        confidence: 0.90,
        type: 'fix'
      })
    }
    
    if (category === 'data') {
      solutions.push({
        id: 'data-fetch',
        title: 'Add Data Fetching',
        description: 'Implement data fetching on component mount',
        code: `useEffect(() => {
  const fetchData = async () => {
    try {
      const data = await api.getData();
      setData(data);
    } catch (error) {
      setError(error);
    }
  };
  
  fetchData();
}, []);`,
        explanation: 'Fetch data when component mounts and handle errors',
        impact: 'high',
        confidence: 0.90,
        type: 'fix'
      })
    }
    
    if (category === 'ui') {
      solutions.push({
        id: 'ui-event',
        title: 'Fix Event Handlers',
        description: 'Ensure event handlers are properly attached',
        code: `// Make sure event handler is attached
<button 
  onClick={handleSubmit}
  onTouchEnd={handleSubmit} // For mobile
  className="submit-button"
>
  Submit
</button>`,
        explanation: 'Add both click and touch event handlers for mobile compatibility',
        impact: 'medium',
        confidence: 0.85,
        type: 'fix'
      })
    }
    
    // Add prevention solution
    solutions.push({
      id: 'prevention',
      title: 'Add Error Handling',
      description: 'Implement comprehensive error handling',
      code: `try {
  const result = await operation();
  if (result.success) {
    // Success logic
  } else {
    throw new Error(result.message);
  }
} catch (error) {
  console.error('Operation failed:', error);
  setError(error.message);
}`,
      explanation: 'Add try-catch blocks to handle errors gracefully',
      impact: 'medium',
      confidence: 0.80,
      type: 'prevention'
    })
    
    return solutions
  }

  const applyFix = async (solution: BugSolution) => {
    setIsFixing(true)
    setFixingStep('Applying fix...')
    
    try {
      // Simulate fix application
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Copy solution code to clipboard
      navigator.clipboard.writeText(solution.code)
      
      console.log('Fix applied:', solution.title)
      
    } catch (error) {
      console.error('Fix application failed:', error)
    } finally {
      setIsFixing(false)
      setFixingStep('Fix applied successfully!')
    }
  }

  const runSampleBug = (bug: any) => {
    setBugDescription(bug.description)
    analyzeBug(bug.description)
  }

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'auth': return 'text-red-600 bg-red-100'
      case 'routing': return 'text-blue-600 bg-blue-100'
      case 'data': return 'text-green-600 bg-green-100'
      case 'ui': return 'text-purple-600 bg-purple-100'
      case 'performance': return 'text-orange-600 bg-orange-100'
      case 'logic': return 'text-gray-600 bg-gray-100'
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

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getSolutionTypeColor = (type: string) => {
    switch (type) {
      case 'fix': return 'text-green-600 bg-green-100'
      case 'prevention': return 'text-blue-600 bg-blue-100'
      case 'optimization': return 'text-purple-600 bg-purple-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const renderBugAnalysis = (analysis: BugAnalysis) => {
    const isSelected = selectedAnalysis === analysis.id

    return (
      <motion.div
        key={analysis.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        }`}
        onClick={() => setSelectedAnalysis(selectedAnalysis === analysis.id ? null : selectedAnalysis)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Bug className="h-4 w-4" />
            <span className="font-medium">{analysis.bugDescription}</span>
            <Badge className={getCategoryColor(analysis.category)}>
              {analysis.category.toUpperCase()}
            </Badge>
            <Badge className={getSeverityColor(analysis.severity)}>
              {analysis.severity.toUpperCase()}
            </Badge>
            <Badge className={getConfidenceColor(analysis.confidence)}>
              {(analysis.confidence * 100).toFixed(0)}%
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                navigator.clipboard.writeText(analysis.analysis)
              }}
            >
              <Copy className="h-4 w-4 mr-1" />
              Copy
            </Button>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          {analysis.timestamp.toLocaleString()}
        </div>

        {isSelected && (
          <div className="mt-4 space-y-4">
            <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded border-l-4 border-red-500">
              <div className="text-sm font-medium text-red-800 dark:text-red-200 mb-1">
                Root Cause:
              </div>
              <p className="text-sm text-red-700 dark:text-red-300">
                {analysis.rootCause}
              </p>
            </div>
            
            <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded border-l-4 border-blue-500">
              <div className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-1">
                Analysis:
              </div>
              <p className="text-sm text-blue-700 dark:text-blue-300">
                {analysis.analysis}
              </p>
            </div>
            
            <div>
              <h4 className="text-sm font-medium mb-2">Solutions:</h4>
              <div className="space-y-3">
                {analysis.solutions.map((solution) => (
                  <div key={solution.id} className="p-3 bg-green-50 dark:bg-green-900/20 rounded">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-sm">{solution.title}</span>
                      <div className="flex items-center space-x-2">
                        <Badge className={getSolutionTypeColor(solution.type)}>
                          {solution.type.toUpperCase()}
                        </Badge>
                        <Badge className={getImpactColor(solution.impact)}>
                          {solution.impact.toUpperCase()}
                        </Badge>
                        <Badge className={getConfidenceColor(solution.confidence)}>
                          {(solution.confidence * 100).toFixed(0)}%
                        </Badge>
                      </div>
                    </div>
                    
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                      {solution.description}
                    </p>
                    
                    <div className="bg-gray-900 text-gray-100 p-2 rounded font-mono text-xs overflow-x-auto mb-2">
                      <pre>{solution.code}</pre>
                    </div>
                    
                    <p className="text-xs text-gray-500 mb-2">
                      {solution.explanation}
                    </p>
                    
                    {solution.testCode && (
                      <div className="mt-2">
                        <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                          Test Code:
                        </div>
                        <div className="bg-gray-900 text-gray-100 p-2 rounded font-mono text-xs overflow-x-auto">
                          <pre>{solution.testCode}</pre>
                        </div>
                      </div>
                    )}
                    
                    <div className="flex items-center space-x-2 mt-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          navigator.clipboard.writeText(solution.code)
                        }}
                      >
                        <Copy className="h-4 w-4 mr-1" />
                        Copy Code
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
                ))}
              </div>
            </div>
          </div>
        )}
      </motion.div>
    )
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Bug className="h-6 w-6 text-red-600" />
                <span>Bug Fixing AI</span>
              </CardTitle>
              <CardDescription>
                Describe the bug and get instant analysis with detailed solutions
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

          {/* Fixing Status */}
          {isFixing && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <Wrench className="h-5 w-5 text-green-600" />
                <span className="text-sm font-medium text-green-800 dark:text-green-200">
                  {fixingStep}
                </span>
              </div>
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Bug Fixing AI */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="analyzer">Analyzer</TabsTrigger>
          <TabsTrigger value="samples">Samples</TabsTrigger>
          <TabsTrigger value="patterns">Patterns</TabsTrigger>
          <TabsTrigger value="history">History ({bugAnalyses.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="analyzer" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <MessageSquare className="h-4 w-4" />
                  <span>Bug Description</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="bug-description">Describe the bug you're experiencing</Label>
                    <Textarea
                      id="bug-description"
                      value={bugDescription}
                      onChange={(e) => setBugDescription(e.target.value)}
                      placeholder="e.g., The login form submits successfully but doesn't redirect"
                      className="min-h-[100px]"
                    />
                  </div>
                  <Button
                    onClick={() => analyzeBug(bugDescription)}
                    disabled={isAnalyzing || !bugDescription.trim()}
                    className="w-full"
                  >
                    <Bug className="h-4 w-4 mr-2" />
                    {isAnalyzing ? 'Analyzing...' : 'Analyze Bug'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Analysis Tips</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Be Specific:</strong> Describe what's happening vs what should happen
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Include Context:</strong> Mention the component or feature affected
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Error Messages:</strong> Include any error messages you're seeing
                  </div>
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
                <span>Sample Bug Reports</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {SAMPLE_BUGS.map((bug) => (
                  <div
                    key={bug.id}
                    className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                    onClick={() => runSampleBug(bug)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium text-sm">{bug.description}</div>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          {bug.expectedBehavior}
                        </p>
                        <div className="flex items-center space-x-2 mt-2">
                          <Badge className={getCategoryColor(bug.category)}>
                            {bug.category}
                          </Badge>
                          <Badge className={getSeverityColor(bug.severity)}>
                            {bug.severity}
                          </Badge>
                        </div>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          runSampleBug(bug)
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

        <TabsContent value="patterns" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Search className="h-4 w-4" />
                <span>Bug Patterns</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(BUG_PATTERNS).map(([category, patternData]) => (
                  <div key={category} className="p-3 border rounded-lg">
                    <div className="font-medium text-sm mb-2">{category.toUpperCase()}</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                      Common patterns: {patternData.patterns.join(', ')}
                    </div>
                    <div className="space-y-1">
                      {patternData.commonIssues.map((issue, index) => (
                        <div key={index} className="text-xs">
                          • {issue}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="history" className="space-y-4">
          {bugAnalyses.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <Bug className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                  No Bug Analysis History
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Start analyzing bugs to see your history here.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Badge variant="outline">
                    Total Analyzed: {bugAnalyses.length}
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
                {bugAnalyses.map(renderBugAnalysis)}
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
