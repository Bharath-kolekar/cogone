'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, MessageSquare, Lightbulb, Wand2, BookOpen, GitBranch } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface UserPattern {
  id: string
  pattern: string
  frequency: number
  lastUsed: Date
  confidence: number
  examples: string[]
  suggestions: string[]
  category: 'function' | 'component' | 'style' | 'logic' | 'api' | 'data'
}

interface PatternLearningAIProps {
  onPatternLearned?: (pattern: UserPattern) => void
  showRealTimeLearning?: boolean
  enablePatternAnalysis?: boolean
  className?: string
}

const SAMPLE_PATTERNS = [
  {
    id: 'async-fetch',
    pattern: 'const fetchData = async (url: string) => { try { const response = await fetch(url); return await response.json(); } catch (error) { console.error(\'Fetch error:\', error); throw error; } };',
    frequency: 15,
    lastUsed: new Date(),
    confidence: 0.95,
    examples: [
      'const fetchData = async (url: string) => { try { const response = await fetch(url); return await response.json(); } catch (error) { console.error(\'Fetch error:\', error); throw error; } };',
      'const getUserData = async (id: string) => { try { const response = await fetch(`/api/users/${id}`); return await response.json(); } catch (error) { console.error(\'User fetch error:\', error); throw error; } };'
    ],
    suggestions: [
      'Add loading states',
      'Implement error boundaries',
      'Add retry logic',
      'Cache responses'
    ],
    category: 'api'
  },
  {
    id: 'react-hooks',
    pattern: 'const [state, setState] = useState(initialValue);',
    frequency: 25,
    lastUsed: new Date(),
    confidence: 0.98,
    examples: [
      'const [loading, setLoading] = useState(false);',
      'const [data, setData] = useState(null);',
      'const [error, setError] = useState(null);'
    ],
    suggestions: [
      'Add TypeScript types',
      'Implement custom hooks',
      'Add validation',
      'Optimize re-renders'
    ],
    category: 'component'
  },
  {
    id: 'error-handling',
    pattern: 'try { /* code */ } catch (error) { console.error(\'Error:\', error); throw error; }',
    frequency: 20,
    lastUsed: new Date(),
    confidence: 0.92,
    examples: [
      'try { const result = await apiCall(); return result; } catch (error) { console.error(\'API Error:\', error); throw error; }',
      'try { const data = processData(input); return data; } catch (error) { console.error(\'Processing Error:\', error); throw error; }'
    ],
    suggestions: [
      'Add user-friendly error messages',
      'Implement error logging',
      'Add fallback values',
      'Create error boundaries'
    ],
    category: 'logic'
  }
]

const PATTERN_CATEGORIES = {
  'function': { icon: Code, color: 'text-blue-600 bg-blue-100', description: 'Function patterns' },
  'component': { icon: BookOpen, color: 'text-green-600 bg-green-100', description: 'Component patterns' },
  'style': { icon: Target, color: 'text-purple-600 bg-purple-100', description: 'Styling patterns' },
  'logic': { icon: Brain, color: 'text-orange-600 bg-orange-100', description: 'Logic patterns' },
  'api': { icon: GitBranch, color: 'text-indigo-600 bg-indigo-100', description: 'API patterns' },
  'data': { icon: TrendingUp, color: 'text-pink-600 bg-pink-100', description: 'Data patterns' }
}

export function PatternLearningAI({
  onPatternLearned,
  showRealTimeLearning = true,
  enablePatternAnalysis = true,
  className = ''
}: PatternLearningAIProps) {
  const [userPatterns, setUserPatterns] = useState<UserPattern[]>(SAMPLE_PATTERNS)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('patterns')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedPattern, setSelectedPattern] = useState<string | null>(null)
  const [newCode, setNewCode] = useState('')
  const [detectedPatterns, setDetectedPatterns] = useState<UserPattern[]>([])
  const [learningInsights, setLearningInsights] = useState<any>(null)
  const [isLearning, setIsLearning] = useState(false)

  const analyzeCode = async (code: string) => {
    if (!code.trim()) return

    setIsAnalyzing(true)
    setProgress(0)
    setAnalysisStep('Analyzing code patterns...')

    try {
      // Simulate pattern analysis steps
      const steps = [
        'Parsing code structure...',
        'Identifying common patterns...',
        'Comparing with learned patterns...',
        'Detecting new patterns...',
        'Analyzing pattern frequency...',
        'Generating suggestions...',
        'Updating pattern database...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setAnalysisStep(steps[i])
        setProgress((i + 1) * 14.3)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Simulate pattern detection
      const detected = detectPatterns(code)
      setDetectedPatterns(detected)
      
      // Update learning insights
      setLearningInsights({
        totalPatterns: userPatterns.length,
        newPatterns: detected.length,
        confidence: 0.85 + Math.random() * 0.15,
        suggestions: generateSuggestions(code)
      })

    } catch (error) {
      console.error('Pattern analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
      setProgress(100)
      setAnalysisStep('Pattern analysis complete!')
    }
  }

  const detectPatterns = (code: string): UserPattern[] => {
    const patterns: UserPattern[] = []
    
    // Simple pattern detection simulation
    if (code.includes('async') && code.includes('fetch')) {
      patterns.push({
        id: `pattern-${Date.now()}`,
        pattern: 'async-fetch',
        frequency: 1,
        lastUsed: new Date(),
        confidence: 0.9,
        examples: [code],
        suggestions: ['Add error handling', 'Implement loading states', 'Add retry logic'],
        category: 'api'
      })
    }
    
    if (code.includes('useState') || code.includes('useEffect')) {
      patterns.push({
        id: `pattern-${Date.now() + 1}`,
        pattern: 'react-hooks',
        frequency: 1,
        lastUsed: new Date(),
        confidence: 0.95,
        examples: [code],
        suggestions: ['Add TypeScript types', 'Implement custom hooks', 'Add validation'],
        category: 'component'
      })
    }
    
    if (code.includes('try') && code.includes('catch')) {
      patterns.push({
        id: `pattern-${Date.now() + 2}`,
        pattern: 'error-handling',
        frequency: 1,
        lastUsed: new Date(),
        confidence: 0.88,
        examples: [code],
        suggestions: ['Add user-friendly messages', 'Implement logging', 'Add fallbacks'],
        category: 'logic'
      })
    }
    
    return patterns
  }

  const generateSuggestions = (code: string): string[] => {
    const suggestions = []
    
    if (code.includes('async')) {
      suggestions.push('Consider adding loading states')
      suggestions.push('Implement error boundaries')
    }
    
    if (code.includes('useState')) {
      suggestions.push('Add TypeScript types for better type safety')
      suggestions.push('Consider using custom hooks for reusability')
    }
    
    if (code.includes('fetch')) {
      suggestions.push('Add request caching for better performance')
      suggestions.push('Implement retry logic for failed requests')
    }
    
    return suggestions
  }

  const learnPattern = (pattern: UserPattern) => {
    setIsLearning(true)
    
    // Simulate learning process
    setTimeout(() => {
      setUserPatterns(prev => {
        const existing = prev.find(p => p.pattern === pattern.pattern)
        if (existing) {
          return prev.map(p => 
            p.pattern === pattern.pattern 
              ? { ...p, frequency: p.frequency + 1, lastUsed: new Date() }
              : p
          )
        } else {
          return [...prev, { ...pattern, id: `learned-${Date.now()}` }]
        }
      })
      
      onPatternLearned?.(pattern)
      setIsLearning(false)
    }, 1000)
  }

  const generateCodeFromPattern = (pattern: UserPattern) => {
    // Simulate code generation based on learned patterns
    const baseCode = pattern.examples[0] || pattern.pattern
    return `// Generated code based on your pattern: ${pattern.pattern}
${baseCode}

// Additional suggestions:
${pattern.suggestions.map(s => `// - ${s}`).join('\n')}`
  }

  const getCategoryIcon = (category: string) => {
    return PATTERN_CATEGORIES[category as keyof typeof PATTERN_CATEGORIES]?.icon || Code
  }

  const getCategoryColor = (category: string) => {
    return PATTERN_CATEGORIES[category as keyof typeof PATTERN_CATEGORIES]?.color || 'text-gray-600 bg-gray-100'
  }

  const getFrequencyColor = (frequency: number) => {
    if (frequency > 20) return 'text-green-600 bg-green-100'
    if (frequency > 10) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const renderPattern = (pattern: UserPattern) => {
    const isSelected = selectedPattern === pattern.id
    const Icon = getCategoryIcon(pattern.category)

    return (
      <motion.div
        key={pattern.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        }`}
        onClick={() => setSelectedPattern(selectedPattern === pattern.id ? null : selectedPattern)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Icon className="h-4 w-4" />
            <span className="font-medium">{pattern.pattern}</span>
            <Badge className={getCategoryColor(pattern.category)}>
              {pattern.category.toUpperCase()}
            </Badge>
            <Badge className={getFrequencyColor(pattern.frequency)}>
              {pattern.frequency}x
            </Badge>
            <Badge className={getConfidenceColor(pattern.confidence)}>
              {(pattern.confidence * 100).toFixed(0)}%
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                navigator.clipboard.writeText(generateCodeFromPattern(pattern))
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
                learnPattern(pattern)
              }}
              disabled={isLearning}
            >
              <Brain className="h-4 w-4 mr-1" />
              Learn
            </Button>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          Last used: {pattern.lastUsed.toLocaleDateString()}
        </div>

        {isSelected && (
          <div className="mt-3 space-y-3">
            <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm overflow-x-auto">
              <pre>{pattern.examples[0]}</pre>
            </div>
            
            {pattern.suggestions.length > 0 && (
              <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded">
                <div className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">
                  Suggestions:
                </div>
                <ul className="text-xs text-blue-600 dark:text-blue-400 space-y-1">
                  {pattern.suggestions.map((suggestion, index) => (
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
      <Card className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-purple-600" />
                <span>Pattern Learning AI</span>
              </CardTitle>
              <CardDescription>
                Learn your coding patterns and generate similar code automatically
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
              className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-600"></div>
                <span className="text-sm font-medium text-purple-800 dark:text-purple-200">
                  {analysisStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Pattern Learning AI */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="patterns">Patterns</TabsTrigger>
          <TabsTrigger value="analyze">Analyze</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
          <TabsTrigger value="generate">Generate</TabsTrigger>
        </TabsList>

        <TabsContent value="patterns" className="space-y-4">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Badge variant="outline">
                  Total Patterns: {userPatterns.length}
                </Badge>
                <Badge variant="outline" className="text-green-600">
                  Learned: {userPatterns.filter(p => p.frequency > 1).length}
                </Badge>
              </div>
            </div>

            <div className="space-y-3">
              {userPatterns.map(renderPattern)}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="analyze" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Code className="h-4 w-4" />
                  <span>Analyze Code</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="new-code">Paste your code to analyze patterns</Label>
                    <Textarea
                      id="new-code"
                      value={newCode}
                      onChange={(e) => setNewCode(e.target.value)}
                      placeholder="Paste your code here to analyze patterns..."
                      className="min-h-[200px] font-mono text-sm"
                    />
                  </div>
                  <Button
                    onClick={() => analyzeCode(newCode)}
                    disabled={isAnalyzing || !newCode.trim()}
                    className="w-full"
                  >
                    <Brain className="h-4 w-4 mr-2" />
                    {isAnalyzing ? 'Analyzing...' : 'Analyze Patterns'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Detected Patterns</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {detectedPatterns.length > 0 ? (
                    detectedPatterns.map((pattern, index) => (
                      <div key={index} className="p-3 border rounded-lg">
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-sm">{pattern.pattern}</div>
                            <div className="text-xs text-gray-500">
                              {pattern.category} • {(pattern.confidence * 100).toFixed(0)}% confidence
                            </div>
                          </div>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => learnPattern(pattern)}
                            disabled={isLearning}
                          >
                            <Brain className="h-4 w-4 mr-1" />
                            Learn
                          </Button>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-4 text-gray-500">
                      No patterns detected yet. Paste code to analyze.
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="insights" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Learning Progress</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Total Patterns</span>
                    <span className="font-medium">{userPatterns.length}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Learned Patterns</span>
                    <span className="font-medium text-green-600">
                      {userPatterns.filter(p => p.frequency > 1).length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Confidence</span>
                    <span className="font-medium">
                      {learningInsights?.confidence ? (learningInsights.confidence * 100).toFixed(0) : 0}%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Brain className="h-4 w-4" />
                  <span>Pattern Categories</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(PATTERN_CATEGORIES).map(([category, info]) => {
                    const count = userPatterns.filter(p => p.category === category).length
                    return (
                      <div key={category} className="flex justify-between items-center">
                        <span className="text-sm">{info.description}</span>
                        <Badge className={info.color}>
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
                  <span>Learning Insights</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {learningInsights ? (
                    <>
                      <div className="text-sm">
                        <strong>New Patterns:</strong> {learningInsights.newPatterns}
                      </div>
                      <div className="text-sm">
                        <strong>Suggestions:</strong> {learningInsights.suggestions?.length || 0}
                      </div>
                      <div className="text-sm">
                        <strong>Confidence:</strong> {(learningInsights.confidence * 100).toFixed(0)}%
                      </div>
                    </>
                  ) : (
                    <div className="text-center py-4 text-gray-500">
                      Analyze code to see insights
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="generate" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Wand2 className="h-4 w-4" />
                <span>Generate Code from Patterns</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  Select a pattern to generate similar code:
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {userPatterns.map((pattern) => (
                    <div
                      key={pattern.id}
                      className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                      onClick={() => {
                        const generatedCode = generateCodeFromPattern(pattern)
                        navigator.clipboard.writeText(generatedCode)
                      }}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-sm">{pattern.pattern}</div>
                          <div className="text-xs text-gray-500">
                            {pattern.category} • {pattern.frequency}x used
                          </div>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation()
                            const generatedCode = generateCodeFromPattern(pattern)
                            navigator.clipboard.writeText(generatedCode)
                          }}
                        >
                          <Copy className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
