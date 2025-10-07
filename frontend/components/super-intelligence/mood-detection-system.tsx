'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Heart, Smile, Frown, Meh, TrendingUp, TrendingDown, Eye, Activity, Zap, Target, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface MoodState {
  primary: 'happy' | 'sad' | 'neutral' | 'excited' | 'stressed' | 'focused' | 'confused' | 'motivated'
  intensity: number // 0-1
  confidence: number // 0-1
  timestamp: number
  duration: number // seconds
}

interface EmotionalIndicators {
  facialExpressions: {
    smile: number
    frown: number
    neutral: number
    surprise: number
    anger: number
  }
  voiceTone: {
    pitch: number
    volume: number
    speed: number
    stress: number
  }
  behavioralPatterns: {
    clickSpeed: number
    scrollPattern: number
    pauseFrequency: number
    taskCompletion: number
    errorRate: number
  }
  contextualFactors: {
    timeOfDay: number
    dayOfWeek: number
    sessionDuration: number
    previousMood: string
    taskComplexity: number
  }
}

interface MoodAnalysis {
  currentMood: MoodState
  moodHistory: MoodState[]
  emotionalIndicators: EmotionalIndicators
  trends: {
    direction: 'improving' | 'declining' | 'stable'
    change: number
    period: string
  }
  predictions: {
    nextMood: string
    confidence: number
    triggers: string[]
  }
  recommendations: {
    uiAdaptations: string[]
    productivityBoosters: string[]
    positivityEnhancers: string[]
    engagementStrategies: string[]
  }
}

interface SuperIntelligenceMoodDetectionProps {
  onMoodChange?: (mood: MoodState) => void
  onAnalysisComplete?: (analysis: MoodAnalysis) => void
  enableRealTime?: boolean
  enablePredictions?: boolean
  enableAdaptations?: boolean
  className?: string
}

const MOOD_ICONS = {
  'happy': Smile,
  'sad': Frown,
  'neutral': Meh,
  'excited': TrendingUp,
  'stressed': AlertCircle,
  'focused': Target,
  'confused': Brain,
  'motivated': Zap
}

const MOOD_COLORS = {
  'happy': 'text-yellow-600 bg-yellow-100',
  'sad': 'text-blue-600 bg-blue-100',
  'neutral': 'text-gray-600 bg-gray-100',
  'excited': 'text-orange-600 bg-orange-100',
  'stressed': 'text-red-600 bg-red-100',
  'focused': 'text-green-600 bg-green-100',
  'confused': 'text-purple-600 bg-purple-100',
  'motivated': 'text-pink-600 bg-pink-100'
}

export function SuperIntelligenceMoodDetection({
  onMoodChange,
  onAnalysisComplete,
  enableRealTime = true,
  enablePredictions = true,
  enableAdaptations = true,
  className = ''
}: SuperIntelligenceMoodDetectionProps) {
  const [moodAnalysis, setMoodAnalysis] = useState<MoodAnalysis | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedTimeframe, setSelectedTimeframe] = useState('recent')
  
  const interactionData = useRef<{
    clicks: number
    scrolls: number
    pauses: number
    errors: number
    tasksCompleted: number
    sessionStart: number
  }>({
    clicks: 0,
    scrolls: 0,
    pauses: 0,
    errors: 0,
    tasksCompleted: 0,
    sessionStart: Date.now()
  })

  const moodHistory = useRef<MoodState[]>([])

  useEffect(() => {
    if (enableRealTime) {
      startRealTimeMoodDetection()
    }
  }, [enableRealTime])

  const startRealTimeMoodDetection = useCallback(() => {
    const detectMood = async () => {
      setIsAnalyzing(true)
      setProgress(0)
      setAnalysisStep('Initializing super intelligence mood detection...')

      try {
        const steps = [
          'Analyzing facial expressions...',
          'Processing voice tone patterns...',
          'Detecting behavioral indicators...',
          'Evaluating contextual factors...',
          'Calculating emotional intensity...',
          'Identifying mood patterns...',
          'Generating predictions...',
          'Creating adaptation strategies...',
          'Optimizing user experience...',
          'Finalizing mood analysis...'
        ]

        for (let i = 0; i < steps.length; i++) {
          setAnalysisStep(steps[i])
          setProgress((i + 1) * 10)
          await new Promise(resolve => setTimeout(resolve, 300))
        }

        const analysis = await performMoodAnalysis()
        setMoodAnalysis(analysis)
        onAnalysisComplete?.(analysis)
        onMoodChange?.(analysis.currentMood)
        
        moodHistory.current.push(analysis.currentMood)
        if (moodHistory.current.length > 50) {
          moodHistory.current = moodHistory.current.slice(-50)
        }

      } catch (error) {
        console.error('Mood detection failed:', error)
      } finally {
        setIsAnalyzing(false)
        setProgress(100)
        setAnalysisStep('Mood analysis complete!')
      }
    }

    // Initial analysis
    detectMood()

    // Set up continuous monitoring
    const interval = setInterval(detectMood, 30000) // Every 30 seconds

    return () => clearInterval(interval)
  }, [onMoodChange, onAnalysisComplete])

  const performMoodAnalysis = async (): Promise<MoodAnalysis> => {
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Simulate advanced mood detection
    const currentTime = Date.now()
    const sessionDuration = (currentTime - interactionData.current.sessionStart) / 1000 / 60 // minutes

    // Analyze behavioral patterns
    const behavioralPatterns = {
      clickSpeed: Math.min(interactionData.current.clicks / sessionDuration, 10),
      scrollPattern: interactionData.current.scrolls / sessionDuration,
      pauseFrequency: interactionData.current.pauses / sessionDuration,
      taskCompletion: interactionData.current.tasksCompleted / Math.max(sessionDuration, 1),
      errorRate: interactionData.current.errors / Math.max(interactionData.current.clicks, 1)
    }

    // Simulate facial expression analysis
    const facialExpressions = {
      smile: 0.3 + Math.random() * 0.7,
      frown: Math.random() * 0.3,
      neutral: 0.2 + Math.random() * 0.6,
      surprise: Math.random() * 0.4,
      anger: Math.random() * 0.2
    }

    // Simulate voice tone analysis
    const voiceTone = {
      pitch: 0.4 + Math.random() * 0.6,
      volume: 0.5 + Math.random() * 0.5,
      speed: 0.3 + Math.random() * 0.7,
      stress: Math.random() * 0.8
    }

    // Determine primary mood based on indicators
    let primaryMood: MoodState['primary'] = 'neutral'
    let intensity = 0.5
    let confidence = 0.8

    if (facialExpressions.smile > 0.7 && behavioralPatterns.taskCompletion > 0.5) {
      primaryMood = 'happy'
      intensity = 0.6 + Math.random() * 0.4
    } else if (facialExpressions.frown > 0.5 || behavioralPatterns.errorRate > 0.3) {
      primaryMood = 'stressed'
      intensity = 0.5 + Math.random() * 0.5
    } else if (behavioralPatterns.clickSpeed > 5 && behavioralPatterns.taskCompletion > 0.7) {
      primaryMood = 'focused'
      intensity = 0.7 + Math.random() * 0.3
    } else if (voiceTone.speed > 0.7 && behavioralPatterns.taskCompletion > 0.6) {
      primaryMood = 'excited'
      intensity = 0.6 + Math.random() * 0.4
    } else if (behavioralPatterns.errorRate > 0.5) {
      primaryMood = 'confused'
      intensity = 0.4 + Math.random() * 0.6
    } else if (behavioralPatterns.taskCompletion > 0.8) {
      primaryMood = 'motivated'
      intensity = 0.7 + Math.random() * 0.3
    }

    const currentMood: MoodState = {
      primary: primaryMood,
      intensity,
      confidence,
      timestamp: currentTime,
      duration: sessionDuration * 60
    }

    // Generate trends
    const trends = {
      direction: Math.random() > 0.5 ? 'improving' : 'stable' as 'improving' | 'declining' | 'stable',
      change: (Math.random() - 0.5) * 0.4,
      period: 'recent'
    }

    // Generate predictions
    const predictions = {
      nextMood: ['happy', 'focused', 'motivated'][Math.floor(Math.random() * 3)],
      confidence: 0.6 + Math.random() * 0.3,
      triggers: ['task completion', 'positive feedback', 'progress milestone']
    }

    // Generate recommendations
    const recommendations = {
      uiAdaptations: generateUIAdaptations(primaryMood, intensity),
      productivityBoosters: generateProductivityBoosters(primaryMood, behavioralPatterns),
      positivityEnhancers: generatePositivityEnhancers(primaryMood, intensity),
      engagementStrategies: generateEngagementStrategies(primaryMood, behavioralPatterns)
    }

    return {
      currentMood,
      moodHistory: moodHistory.current,
      emotionalIndicators: {
        facialExpressions,
        voiceTone,
        behavioralPatterns,
        contextualFactors: {
          timeOfDay: new Date().getHours(),
          dayOfWeek: new Date().getDay(),
          sessionDuration,
          previousMood: moodHistory.current[moodHistory.current.length - 1]?.primary || 'neutral',
          taskComplexity: behavioralPatterns.errorRate
        }
      },
      trends,
      predictions,
      recommendations
    }
  }

  const generateUIAdaptations = (mood: string, intensity: number): string[] => {
    const adaptations = []
    
    if (mood === 'stressed') {
      adaptations.push('Reduce visual clutter', 'Increase white space', 'Use calming colors', 'Simplify navigation')
    } else if (mood === 'happy') {
      adaptations.push('Add celebratory animations', 'Use vibrant colors', 'Show progress achievements', 'Enable social sharing')
    } else if (mood === 'focused') {
      adaptations.push('Minimize distractions', 'Highlight important elements', 'Use focus mode', 'Enable deep work features')
    } else if (mood === 'confused') {
      adaptations.push('Add helpful tooltips', 'Show guided tutorials', 'Simplify interface', 'Provide contextual help')
    } else if (mood === 'motivated') {
      adaptations.push('Show progress bars', 'Add gamification elements', 'Enable achievement badges', 'Display motivational quotes')
    }
    
    return adaptations
  }

  const generateProductivityBoosters = (mood: string, patterns: any): string[] => {
    const boosters = []
    
    if (patterns.taskCompletion > 0.7) {
      boosters.push('Enable advanced shortcuts', 'Show productivity insights', 'Suggest workflow optimizations')
    }
    
    if (mood === 'focused') {
      boosters.push('Enable distraction blocking', 'Show time tracking', 'Provide focus sessions')
    }
    
    if (mood === 'motivated') {
      boosters.push('Set achievement goals', 'Enable progress tracking', 'Show performance metrics')
    }
    
    return boosters
  }

  const generatePositivityEnhancers = (mood: string, intensity: number): string[] => {
    const enhancers = []
    
    if (mood === 'sad' || mood === 'stressed') {
      enhancers.push('Show encouraging messages', 'Display positive affirmations', 'Enable mood-lifting animations')
    }
    
    if (intensity < 0.5) {
      enhancers.push('Add motivational content', 'Show success stories', 'Enable positive feedback')
    }
    
    return enhancers
  }

  const generateEngagementStrategies = (mood: string, patterns: any): string[] => {
    const strategies = []
    
    if (patterns.clickSpeed < 2) {
      strategies.push('Add interactive elements', 'Enable hover effects', 'Show micro-animations')
    }
    
    if (mood === 'bored' || patterns.pauseFrequency > 0.5) {
      strategies.push('Introduce new features', 'Show personalized content', 'Enable discovery mode')
    }
    
    return strategies
  }

  const getMoodIcon = (mood: string) => {
    return MOOD_ICONS[mood as keyof typeof MOOD_ICONS] || Brain
  }

  const getMoodColor = (mood: string) => {
    return MOOD_COLORS[mood as keyof typeof MOOD_COLORS] || 'text-gray-600 bg-gray-100'
  }

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'improving': return TrendingUp
      case 'declining': return TrendingDown
      default: return Activity
    }
  }

  const getTrendColor = (direction: string) => {
    switch (direction) {
      case 'improving': return 'text-green-600 bg-green-100'
      case 'declining': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Analysis Status */}
      {isAnalyzing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg p-4"
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

      {/* Mood Analysis Results */}
      {moodAnalysis && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Current Mood */}
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-blue-600" />
                <span>Super Intelligence Mood Detection</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center space-x-4 mb-4">
                <div className="text-4xl">
                  {(() => {
                    const Icon = getMoodIcon(moodAnalysis.currentMood.primary)
                    return <Icon className="h-12 w-12" />
                  })()}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                    {moodAnalysis.currentMood.primary.charAt(0).toUpperCase() + moodAnalysis.currentMood.primary.slice(1)} Mood
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Intensity: {(moodAnalysis.currentMood.intensity * 100).toFixed(1)}% • Confidence: {(moodAnalysis.currentMood.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge className={getMoodColor(moodAnalysis.currentMood.primary)}>
                  {moodAnalysis.currentMood.primary}
                </Badge>
                <Badge variant="outline">
                  Intensity: {(moodAnalysis.currentMood.intensity * 100).toFixed(1)}%
                </Badge>
                <Badge variant="outline">
                  Confidence: {(moodAnalysis.currentMood.confidence * 100).toFixed(1)}%
                </Badge>
              </div>

              {/* Mood Intensity Bar */}
              <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
                <div 
                  className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full"
                  style={{ width: `${moodAnalysis.currentMood.intensity * 100}%` }}
                />
              </div>
            </CardContent>
          </Card>

          {/* Emotional Indicators */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Eye className="h-4 w-4" />
                  <span>Facial Expressions</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(moodAnalysis.emotionalIndicators.facialExpressions).map(([expression, value]) => (
                    <div key={expression} className="flex justify-between items-center">
                      <span className="text-sm capitalize">{expression}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full"
                            style={{ width: `${value * 100}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-500">{(value * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Activity className="h-4 w-4" />
                  <span>Behavioral Patterns</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {Object.entries(moodAnalysis.emotionalIndicators.behavioralPatterns).map(([pattern, value]) => (
                    <div key={pattern} className="flex justify-between items-center">
                      <span className="text-sm capitalize">{pattern.replace(/([A-Z])/g, ' $1')}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-500 h-2 rounded-full"
                            style={{ width: `${Math.min(value * 10, 100)}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-500">{value.toFixed(2)}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Trends and Predictions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  {(() => {
                    const Icon = getTrendIcon(moodAnalysis.trends.direction)
                    return <Icon className="h-4 w-4" />
                  })()}
                  <span>Mood Trends</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-medium capitalize">{moodAnalysis.trends.direction}</div>
                    <div className="text-sm text-gray-500">{moodAnalysis.trends.period}</div>
                  </div>
                  <Badge className={getTrendColor(moodAnalysis.trends.direction)}>
                    {moodAnalysis.trends.direction}
                  </Badge>
                </div>
                <div className="text-sm text-gray-500 mt-2">
                  Change: {(moodAnalysis.trends.change * 100).toFixed(1)}%
                </div>
              </CardContent>
            </Card>

            {enablePredictions && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm flex items-center space-x-2">
                    <Target className="h-4 w-4" />
                    <span>Predictions</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Next Mood</span>
                      <Badge variant="outline">{moodAnalysis.predictions.nextMood}</Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">Confidence</span>
                      <span className="text-sm">{(moodAnalysis.predictions.confidence * 100).toFixed(0)}%</span>
                    </div>
                    <div className="text-xs text-gray-500">
                      Triggers: {moodAnalysis.predictions.triggers.join(', ')}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Recommendations */}
          {enableAdaptations && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">AI-Powered Recommendations</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm">UI Adaptations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-1">
                      {moodAnalysis.recommendations.uiAdaptations.map((adaptation, index) => (
                        <li key={index} className="text-sm flex items-start space-x-2">
                          <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                          <span>{adaptation}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm">Productivity Boosters</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-1">
                      {moodAnalysis.recommendations.productivityBoosters.map((booster, index) => (
                        <li key={index} className="text-sm flex items-start space-x-2">
                          <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                          <span>{booster}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm">Positivity Enhancers</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-1">
                      {moodAnalysis.recommendations.positivityEnhancers.map((enhancer, index) => (
                        <li key={index} className="text-sm flex items-start space-x-2">
                          <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
                          <span>{enhancer}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm">Engagement Strategies</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-1">
                      {moodAnalysis.recommendations.engagementStrategies.map((strategy, index) => (
                        <li key={index} className="text-sm flex items-start space-x-2">
                          <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                          <span>{strategy}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {/* Toggle Details */}
          <div className="text-center">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowDetails(!showDetails)}
            >
              {showDetails ? 'Hide' : 'Show'} Detailed Analysis
            </Button>
          </div>
        </motion.div>
      )}
    </div>
  )
}
