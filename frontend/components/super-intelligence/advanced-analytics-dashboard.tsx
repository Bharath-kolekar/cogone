'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { BarChart3, TrendingUp, PieChart, Activity, Brain, Target, Zap, Eye, Heart, Clock, Award, Users } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface AnalyticsData {
  moodTrends: {
    daily: { date: string; mood: string; intensity: number }[]
    weekly: { week: string; averageMood: number; dominantMood: string }[]
    monthly: { month: string; moodDistribution: any }[]
  }
  productivityMetrics: {
    focusTime: number
    taskCompletion: number
    efficiency: number
    satisfaction: number
    trends: { date: string; value: number }[]
  }
  behavioralPatterns: {
    peakHours: { hour: number; activity: number }[]
    breakPatterns: { time: string; duration: number }[]
    interactionPatterns: { type: string; frequency: number }[]
  }
  emotionalInsights: {
    stressLevels: { date: string; level: number }[]
    happinessIndex: { date: string; index: number }[]
    emotionalStability: number
    moodVolatility: number
  }
  aiPerformance: {
    accuracy: { date: string; accuracy: number }[]
    adaptationSuccess: { date: string; success: number }[]
    learningProgress: { date: string; progress: number }[]
    optimization: { date: string; efficiency: number }[]
  }
}

interface AdvancedAnalyticsDashboardProps {
  timeRange?: 'day' | 'week' | 'month' | 'year'
  enableRealTimeUpdates?: boolean
  showDetailedMetrics?: boolean
  onAnalyticsUpdate?: (data: AnalyticsData) => void
  className?: string
}

export function AdvancedAnalyticsDashboard({
  timeRange = 'week',
  enableRealTimeUpdates = true,
  showDetailedMetrics = true,
  onAnalyticsUpdate,
  className = ''
}: AdvancedAnalyticsDashboardProps) {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData>({
    moodTrends: {
      daily: [],
      weekly: [],
      monthly: []
    },
    productivityMetrics: {
      focusTime: 0,
      taskCompletion: 0,
      efficiency: 0,
      satisfaction: 0,
      trends: []
    },
    behavioralPatterns: {
      peakHours: [],
      breakPatterns: [],
      interactionPatterns: []
    },
    emotionalInsights: {
      stressLevels: [],
      happinessIndex: [],
      emotionalStability: 0,
      moodVolatility: 0
    },
    aiPerformance: {
      accuracy: [],
      adaptationSuccess: [],
      learningProgress: [],
      optimization: []
    }
  })

  const [isLoading, setIsLoading] = useState(false)
  const [selectedMetric, setSelectedMetric] = useState('overview')
  const [showInsights, setShowInsights] = useState(false)
  const [refreshInterval, setRefreshInterval] = useState(30000) // 30 seconds

  const analyticsHistory = useRef<AnalyticsData[]>([])
  const updateInterval = useRef<NodeJS.Timeout>()

  useEffect(() => {
    loadAnalyticsData()
  }, [timeRange])

  useEffect(() => {
    if (enableRealTimeUpdates) {
      startRealTimeUpdates()
    }
    return () => {
      if (updateInterval.current) {
        clearInterval(updateInterval.current)
      }
    }
  }, [enableRealTimeUpdates, refreshInterval])

  const loadAnalyticsData = useCallback(async () => {
    setIsLoading(true)
    
    try {
      // Simulate loading analytics data
      await new Promise(resolve => setTimeout(resolve, 1500))

      // Generate mock data based on time range
      const data = generateMockAnalyticsData(timeRange)
      setAnalyticsData(data)
      onAnalyticsUpdate?.(data)

      // Store in history
      analyticsHistory.current.push(data)
      if (analyticsHistory.current.length > 100) {
        analyticsHistory.current = analyticsHistory.current.slice(-100)
      }

    } catch (error) {
      console.error('Failed to load analytics data:', error)
    } finally {
      setIsLoading(false)
    }
  }, [timeRange, onAnalyticsUpdate])

  const startRealTimeUpdates = useCallback(() => {
    updateInterval.current = setInterval(() => {
      // Simulate real-time data updates
      setAnalyticsData(prev => ({
        ...prev,
        productivityMetrics: {
          ...prev.productivityMetrics,
          focusTime: Math.min(8, prev.productivityMetrics.focusTime + (Math.random() - 0.5) * 0.1),
          taskCompletion: Math.min(1, prev.productivityMetrics.taskCompletion + (Math.random() - 0.5) * 0.05),
          efficiency: Math.min(1, prev.productivityMetrics.efficiency + (Math.random() - 0.5) * 0.03),
          satisfaction: Math.min(1, prev.productivityMetrics.satisfaction + (Math.random() - 0.5) * 0.02)
        }
      }))
    }, refreshInterval)
  }, [refreshInterval])

  const generateMockAnalyticsData = (range: string): AnalyticsData => {
    const now = new Date()
    const data: AnalyticsData = {
      moodTrends: {
        daily: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(now.getTime() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          mood: ['happy', 'focused', 'stressed', 'excited', 'calm'][Math.floor(Math.random() * 5)],
          intensity: 0.5 + Math.random() * 0.5
        })),
        weekly: Array.from({ length: 4 }, (_, i) => ({
          week: `Week ${i + 1}`,
          averageMood: 0.6 + Math.random() * 0.4,
          dominantMood: ['happy', 'focused', 'stressed', 'excited'][Math.floor(Math.random() * 4)]
        })),
        monthly: Array.from({ length: 12 }, (_, i) => ({
          month: new Date(2024, i).toLocaleString('default', { month: 'short' }),
          moodDistribution: {
            happy: Math.random(),
            focused: Math.random(),
            stressed: Math.random(),
            excited: Math.random(),
            calm: Math.random()
          }
        }))
      },
      productivityMetrics: {
        focusTime: 4.5 + Math.random() * 2,
        taskCompletion: 0.7 + Math.random() * 0.3,
        efficiency: 0.8 + Math.random() * 0.2,
        satisfaction: 0.75 + Math.random() * 0.25,
        trends: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(now.getTime() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          value: 0.6 + Math.random() * 0.4
        }))
      },
      behavioralPatterns: {
        peakHours: Array.from({ length: 24 }, (_, i) => ({
          hour: i,
          activity: Math.random() * 100
        })),
        breakPatterns: [
          { time: '10:00', duration: 15 },
          { time: '12:00', duration: 30 },
          { time: '15:00', duration: 10 },
          { time: '17:00', duration: 20 }
        ],
        interactionPatterns: [
          { type: 'clicks', frequency: 150 + Math.random() * 100 },
          { type: 'scrolls', frequency: 50 + Math.random() * 50 },
          { type: 'pauses', frequency: 20 + Math.random() * 30 },
          { type: 'focus_sessions', frequency: 5 + Math.random() * 10 }
        ]
      },
      emotionalInsights: {
        stressLevels: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(now.getTime() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          level: Math.random()
        })),
        happinessIndex: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(now.getTime() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          index: 0.6 + Math.random() * 0.4
        })),
        emotionalStability: 0.7 + Math.random() * 0.3,
        moodVolatility: 0.2 + Math.random() * 0.3
      },
      aiPerformance: {
        accuracy: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(now.getTime() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          accuracy: 0.8 + Math.random() * 0.2
        })),
        adaptationSuccess: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(now.getTime() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          success: 0.7 + Math.random() * 0.3
        })),
        learningProgress: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(now.getTime() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          progress: Math.min(1, 0.5 + i * 0.1 + Math.random() * 0.1)
        })),
        optimization: Array.from({ length: 7 }, (_, i) => ({
          date: new Date(now.getTime() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
          efficiency: 0.8 + Math.random() * 0.2
        }))
      }
    }

    return data
  }

  const getMetricIcon = (metric: string) => {
    const icons = {
      'overview': BarChart3,
      'mood': Heart,
      'productivity': Target,
      'behavior': Activity,
      'emotions': Brain,
      'ai': Zap
    }
    return icons[metric as keyof typeof icons] || BarChart3
  }

  const getMetricColor = (metric: string) => {
    const colors = {
      'overview': 'text-blue-600 bg-blue-100',
      'mood': 'text-pink-600 bg-pink-100',
      'productivity': 'text-green-600 bg-green-100',
      'behavior': 'text-purple-600 bg-purple-100',
      'emotions': 'text-orange-600 bg-orange-100',
      'ai': 'text-red-600 bg-red-100'
    }
    return colors[metric as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const metrics = [
    { id: 'overview', name: 'Overview', icon: BarChart3 },
    { id: 'mood', name: 'Mood Trends', icon: Heart },
    { id: 'productivity', name: 'Productivity', icon: Target },
    { id: 'behavior', name: 'Behavior', icon: Activity },
    { id: 'emotions', name: 'Emotions', icon: Brain },
    { id: 'ai', name: 'AI Performance', icon: Zap }
  ]

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Loading State */}
      {isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
              Loading advanced analytics...
            </span>
          </div>
          <Progress value={75} className="h-2" />
        </motion.div>
      )}

      {/* Analytics Dashboard */}
      {!isLoading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Header */}
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5 text-blue-600" />
                <span>Advanced Analytics Dashboard</span>
              </CardTitle>
              <CardDescription>
                Deep insights into mood patterns, productivity, and AI performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Badge variant="outline">
                    {timeRange.charAt(0).toUpperCase() + timeRange.slice(1)} View
                  </Badge>
                  <Badge variant="outline">
                    {enableRealTimeUpdates ? 'Live Updates' : 'Static Data'}
                  </Badge>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowInsights(!showInsights)}
                  >
                    {showInsights ? 'Hide' : 'Show'} Insights
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={loadAnalyticsData}
                  >
                    Refresh
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Metric Navigation */}
          <div className="flex flex-wrap gap-2">
            {metrics.map((metric) => {
              const Icon = metric.icon
              return (
                <Button
                  key={metric.id}
                  variant={selectedMetric === metric.id ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedMetric(metric.id)}
                  className="flex items-center space-x-2"
                >
                  <Icon className="h-4 w-4" />
                  <span>{metric.name}</span>
                </Button>
              )
            })}
          </div>

          {/* Metric Content */}
          <AnimatePresence mode="wait">
            {selectedMetric === 'overview' && (
              <motion.div
                key="overview"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-6"
              >
                {/* Key Metrics */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm flex items-center space-x-2">
                        <Heart className="h-4 w-4" />
                        <span>Avg Mood</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-pink-600">
                        {analyticsData.moodTrends.weekly[0]?.averageMood ? 
                          (analyticsData.moodTrends.weekly[0].averageMood * 100).toFixed(0) : '0'}%
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        This week
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm flex items-center space-x-2">
                        <Target className="h-4 w-4" />
                        <span>Productivity</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-green-600">
                        {(analyticsData.productivityMetrics.efficiency * 100).toFixed(0)}%
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Efficiency
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm flex items-center space-x-2">
                        <Clock className="h-4 w-4" />
                        <span>Focus Time</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-blue-600">
                        {analyticsData.productivityMetrics.focusTime.toFixed(1)}h
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Today
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm flex items-center space-x-2">
                        <Zap className="h-4 w-4" />
                        <span>AI Accuracy</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-purple-600">
                        {analyticsData.aiPerformance.accuracy[0] ? 
                          (analyticsData.aiPerformance.accuracy[0].accuracy * 100).toFixed(0) : '0'}%
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">
                        Current
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Trends Chart */}
                <Card>
                  <CardHeader>
                    <CardTitle>Productivity Trends</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="text-center">
                        <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                        <p className="text-gray-600 dark:text-gray-400">
                          Interactive chart would be rendered here
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedMetric === 'mood' && (
              <motion.div
                key="mood"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-6"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Heart className="h-5 w-5 text-pink-600" />
                      <span>Mood Trends</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <h4 className="font-medium mb-2">Daily Mood</h4>
                          <div className="space-y-2">
                            {analyticsData.moodTrends.daily.slice(0, 5).map((day, index) => (
                              <div key={index} className="flex items-center justify-between">
                                <span className="text-sm">{day.date}</span>
                                <div className="flex items-center space-x-2">
                                  <Badge variant="outline">{day.mood}</Badge>
                                  <span className="text-sm">{(day.intensity * 100).toFixed(0)}%</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">Weekly Average</h4>
                          <div className="space-y-2">
                            {analyticsData.moodTrends.weekly.map((week, index) => (
                              <div key={index} className="flex items-center justify-between">
                                <span className="text-sm">{week.week}</span>
                                <div className="flex items-center space-x-2">
                                  <Badge variant="outline">{week.dominantMood}</Badge>
                                  <span className="text-sm">{(week.averageMood * 100).toFixed(0)}%</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedMetric === 'productivity' && (
              <motion.div
                key="productivity"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-6"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Focus Time</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-blue-600 mb-2">
                        {analyticsData.productivityMetrics.focusTime.toFixed(1)}h
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${(analyticsData.productivityMetrics.focusTime / 8) * 100}%` }}
                        />
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Task Completion</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-green-600 mb-2">
                        {(analyticsData.productivityMetrics.taskCompletion * 100).toFixed(0)}%
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${analyticsData.productivityMetrics.taskCompletion * 100}%` }}
                        />
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </motion.div>
            )}

            {selectedMetric === 'ai' && (
              <motion.div
                key="ai"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-6"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">AI Accuracy</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-purple-600 mb-2">
                        {analyticsData.aiPerformance.accuracy[0] ? 
                          (analyticsData.aiPerformance.accuracy[0].accuracy * 100).toFixed(0) : '0'}%
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-purple-500 h-2 rounded-full"
                          style={{ width: `${analyticsData.aiPerformance.accuracy[0]?.accuracy * 100 || 0}%` }}
                        />
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Learning Progress</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-3xl font-bold text-orange-600 mb-2">
                        {analyticsData.aiPerformance.learningProgress[0] ? 
                          (analyticsData.aiPerformance.learningProgress[0].progress * 100).toFixed(0) : '0'}%
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-orange-500 h-2 rounded-full"
                          style={{ width: `${analyticsData.aiPerformance.learningProgress[0]?.progress * 100 || 0}%` }}
                        />
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Insights Panel */}
          {showInsights && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Brain className="h-5 w-5 text-orange-600" />
                    <span>AI Insights</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                      <div className="font-medium text-blue-800 dark:text-blue-200">
                        Peak Productivity Hours
                      </div>
                      <div className="text-sm text-blue-600 dark:text-blue-300">
                        Your most productive hours are 10:00 AM - 12:00 PM. Consider scheduling important tasks during this time.
                      </div>
                    </div>
                    <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                      <div className="font-medium text-green-800 dark:text-green-200">
                        Mood Stability
                      </div>
                      <div className="text-sm text-green-600 dark:text-green-300">
                        Your emotional stability is {(analyticsData.emotionalInsights.emotionalStability * 100).toFixed(0)}%. 
                        This indicates good emotional regulation.
                      </div>
                    </div>
                    <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                      <div className="font-medium text-purple-800 dark:text-purple-200">
                        AI Adaptation Success
                      </div>
                      <div className="text-sm text-purple-600 dark:text-purple-300">
                        The AI system has successfully adapted to your preferences {(analyticsData.aiPerformance.adaptationSuccess[0]?.success * 100 || 0).toFixed(0)}% of the time.
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </motion.div>
      )}
    </div>
  )
}
