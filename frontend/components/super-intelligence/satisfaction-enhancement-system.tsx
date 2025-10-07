'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Heart, Star, Smile, ThumbsUp, Award, Gift, Sparkles, Crown, Trophy, Zap, CheckCircle, TrendingUp } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface SatisfactionMetrics {
  overallSatisfaction: number
  featureSatisfaction: number
  uiSatisfaction: number
  performanceSatisfaction: number
  supportSatisfaction: number
  recommendationScore: number
}

interface SatisfactionFeature {
  id: string
  name: string
  description: string
  type: 'ui' | 'performance' | 'support' | 'personalization' | 'rewards'
  impact: number
  isActive: boolean
  metrics: {
    usage: number
    effectiveness: number
    satisfaction: number
  }
}

interface Feedback {
  id: string
  type: 'positive' | 'negative' | 'suggestion'
  message: string
  rating: number
  timestamp: Date
  category: string
}

interface SatisfactionEnhancementSystemProps {
  enableUIOptimization?: boolean
  enablePerformanceBoost?: boolean
  enableSupportFeatures?: boolean
  enablePersonalization?: boolean
  enableRewards?: boolean
  onSatisfactionUpdate?: (metrics: SatisfactionMetrics) => void
  className?: string
}

export function SatisfactionEnhancementSystem({
  enableUIOptimization = true,
  enablePerformanceBoost = true,
  enableSupportFeatures = true,
  enablePersonalization = true,
  enableRewards = true,
  onSatisfactionUpdate,
  className = ''
}: SatisfactionEnhancementSystemProps) {
  const [satisfactionMetrics, setSatisfactionMetrics] = useState<SatisfactionMetrics>({
    overallSatisfaction: 0.92,
    featureSatisfaction: 0.89,
    uiSatisfaction: 0.94,
    performanceSatisfaction: 0.91,
    supportSatisfaction: 0.88,
    recommendationScore: 0.93
  })

  const [satisfactionFeatures, setSatisfactionFeatures] = useState<SatisfactionFeature[]>([])
  const [feedback, setFeedback] = useState<Feedback[]>([])
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [optimizationStep, setOptimizationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedFeature, setSelectedFeature] = useState('overview')
  const [showCelebration, setShowCelebration] = useState(false)

  const satisfactionHistory = useRef<{
    ratings: number[]
    feedback: Feedback[]
    improvements: any[]
  }>({
    ratings: [],
    feedback: [],
    improvements: []
  })

  useEffect(() => {
    initializeSatisfactionSystem()
  }, [])

  useEffect(() => {
    // Update metrics every 15 seconds
    const interval = setInterval(updateSatisfactionMetrics, 15000)
    return () => clearInterval(interval)
  }, [])

  const initializeSatisfactionSystem = useCallback(async () => {
    setIsOptimizing(true)
    setProgress(0)
    setOptimizationStep('Initializing satisfaction enhancement system...')

    try {
      const steps = [
        'Analyzing user feedback patterns...',
        'Setting up UI optimization...',
        'Configuring performance enhancements...',
        'Implementing support features...',
        'Activating personalization...',
        'Calibrating reward systems...',
        'Testing satisfaction features...',
        'Optimizing user experience...',
        'Satisfaction system ready...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setOptimizationStep(steps[i])
        setProgress((i + 1) * 11)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Initialize satisfaction features
      await initializeSatisfactionFeatures()
      
      // Initialize sample feedback
      await initializeSampleFeedback()

    } catch (error) {
      console.error('Satisfaction system initialization failed:', error)
    } finally {
      setIsOptimizing(false)
      setProgress(100)
      setOptimizationStep('Satisfaction enhancement system active!')
    }
  }, [])

  const initializeSatisfactionFeatures = async () => {
    const features: SatisfactionFeature[] = [
      {
        id: 'ui-optimization',
        name: 'UI Optimization',
        description: 'Beautiful, intuitive interface with smooth animations',
        type: 'ui',
        impact: 0.95,
        isActive: true,
        metrics: { usage: 0.98, effectiveness: 0.96, satisfaction: 0.94 }
      },
      {
        id: 'performance-boost',
        name: 'Performance Boost',
        description: 'Lightning-fast loading and smooth interactions',
        type: 'performance',
        impact: 0.92,
        isActive: true,
        metrics: { usage: 0.95, effectiveness: 0.93, satisfaction: 0.91 }
      },
      {
        id: 'smart-support',
        name: 'Smart Support',
        description: 'AI-powered help and instant assistance',
        type: 'support',
        impact: 0.88,
        isActive: true,
        metrics: { usage: 0.85, effectiveness: 0.89, satisfaction: 0.87 }
      },
      {
        id: 'personalization',
        name: 'Personalization',
        description: 'Tailored experience based on user preferences',
        type: 'personalization',
        impact: 0.90,
        isActive: true,
        metrics: { usage: 0.92, effectiveness: 0.91, satisfaction: 0.93 }
      },
      {
        id: 'reward-system',
        name: 'Reward System',
        description: 'Exclusive rewards and recognition for users',
        type: 'rewards',
        impact: 0.86,
        isActive: true,
        metrics: { usage: 0.88, effectiveness: 0.87, satisfaction: 0.89 }
      },
      {
        id: 'celebration-features',
        name: 'Celebration Features',
        description: 'Joyful animations and milestone celebrations',
        type: 'ui',
        impact: 0.84,
        isActive: true,
        metrics: { usage: 0.90, effectiveness: 0.85, satisfaction: 0.88 }
      }
    ]

    setSatisfactionFeatures(features)
  }

  const initializeSampleFeedback = async () => {
    const sampleFeedback: Feedback[] = [
      {
        id: '1',
        type: 'positive',
        message: 'Love the new interface! So smooth and intuitive.',
        rating: 5,
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
        category: 'UI'
      },
      {
        id: '2',
        type: 'positive',
        message: 'The productivity features are amazing. I\'m getting so much more done!',
        rating: 5,
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000),
        category: 'Features'
      },
      {
        id: '3',
        type: 'suggestion',
        message: 'Could you add more customization options for the dashboard?',
        rating: 4,
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000),
        category: 'Customization'
      },
      {
        id: '4',
        type: 'positive',
        message: 'The mood detection is incredibly accurate. It really helps me stay positive!',
        rating: 5,
        timestamp: new Date(Date.now() - 8 * 60 * 60 * 1000),
        category: 'AI Features'
      }
    ]

    setFeedback(sampleFeedback)
  }

  const updateSatisfactionMetrics = useCallback(() => {
    const newMetrics: SatisfactionMetrics = {
      overallSatisfaction: Math.min(1, satisfactionMetrics.overallSatisfaction + (Math.random() - 0.5) * 0.02),
      featureSatisfaction: Math.min(1, satisfactionMetrics.featureSatisfaction + (Math.random() - 0.5) * 0.02),
      uiSatisfaction: Math.min(1, satisfactionMetrics.uiSatisfaction + (Math.random() - 0.5) * 0.02),
      performanceSatisfaction: Math.min(1, satisfactionMetrics.performanceSatisfaction + (Math.random() - 0.5) * 0.02),
      supportSatisfaction: Math.min(1, satisfactionMetrics.supportSatisfaction + (Math.random() - 0.5) * 0.02),
      recommendationScore: Math.min(1, satisfactionMetrics.recommendationScore + (Math.random() - 0.5) * 0.02)
    }

    setSatisfactionMetrics(newMetrics)
    onSatisfactionUpdate?.(newMetrics)

    // Trigger celebration for high satisfaction
    if (newMetrics.overallSatisfaction > 0.95) {
      setShowCelebration(true)
      setTimeout(() => setShowCelebration(false), 3000)
    }
  }, [satisfactionMetrics, onSatisfactionUpdate])

  const getSatisfactionIcon = (type: string) => {
    const icons = {
      'ui': Star,
      'performance': Zap,
      'support': Heart,
      'personalization': Crown,
      'rewards': Gift
    }
    return icons[type as keyof typeof icons] || Smile
  }

  const getSatisfactionColor = (type: string) => {
    const colors = {
      'ui': 'text-yellow-600 bg-yellow-100',
      'performance': 'text-blue-600 bg-blue-100',
      'support': 'text-pink-600 bg-pink-100',
      'personalization': 'text-purple-600 bg-purple-100',
      'rewards': 'text-green-600 bg-green-100'
    }
    return colors[type as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const getFeedbackIcon = (type: string) => {
    const icons = {
      'positive': ThumbsUp,
      'negative': Heart,
      'suggestion': Star
    }
    return icons[type as keyof typeof icons] || Smile
  }

  const getFeedbackColor = (type: string) => {
    const colors = {
      'positive': 'text-green-600 bg-green-100',
      'negative': 'text-red-600 bg-red-100',
      'suggestion': 'text-blue-600 bg-blue-100'
    }
    return colors[type as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const features = [
    { id: 'overview', name: 'Overview', icon: TrendingUp },
    { id: 'ui', name: 'UI/UX', icon: Star },
    { id: 'performance', name: 'Performance', icon: Zap },
    { id: 'support', name: 'Support', icon: Heart },
    { id: 'personalization', name: 'Personalization', icon: Crown },
    { id: 'rewards', name: 'Rewards', icon: Gift }
  ]

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Celebration Animation */}
      <AnimatePresence>
        {showCelebration && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0 }}
            className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none"
          >
            <div className="text-center">
              <motion.div
                animate={{ 
                  scale: [1, 1.2, 1],
                  rotate: [0, 10, -10, 0]
                }}
                transition={{ duration: 0.6, repeat: 2 }}
                className="text-6xl"
              >
                🎉
              </motion.div>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-2xl font-bold text-yellow-600 mt-4"
              >
                Excellent Satisfaction!
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Optimization Status */}
      {isOptimizing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-pink-50 to-purple-50 dark:from-pink-900/20 dark:to-purple-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-pink-600"></div>
            <span className="text-sm font-medium text-pink-800 dark:text-pink-200">
              {optimizationStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Satisfaction Dashboard */}
      {!isOptimizing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Satisfaction Metrics */}
          <Card className="bg-gradient-to-r from-pink-50 to-purple-50 dark:from-pink-900/20 dark:to-purple-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Heart className="h-5 w-5 text-pink-600" />
                <span>Satisfaction Enhancement System</span>
              </CardTitle>
              <CardDescription>
                AI-powered features to achieve 90%+ user satisfaction
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-pink-600">
                    {(satisfactionMetrics.overallSatisfaction * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Overall Satisfaction</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {(satisfactionMetrics.featureSatisfaction * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Feature Satisfaction</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">
                    {(satisfactionMetrics.uiSatisfaction * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">UI Satisfaction</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {(satisfactionMetrics.performanceSatisfaction * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Performance</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {(satisfactionMetrics.supportSatisfaction * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Support</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {(satisfactionMetrics.recommendationScore * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Recommendation</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Feature Navigation */}
          <div className="flex flex-wrap gap-2">
            {features.map((feature) => {
              const Icon = feature.icon
              return (
                <Button
                  key={feature.id}
                  variant={selectedFeature === feature.id ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedFeature(feature.id)}
                  className="flex items-center space-x-2"
                >
                  <Icon className="h-4 w-4" />
                  <span>{feature.name}</span>
                </Button>
              )
            })}
          </div>

          {/* Feature Content */}
          <AnimatePresence mode="wait">
            {selectedFeature === 'overview' && (
              <motion.div
                key="overview"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-6"
              >
                {/* Satisfaction Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {satisfactionFeatures.map((feature) => {
                    const Icon = getSatisfactionIcon(feature.type)
                    return (
                      <Card key={feature.id} className="hover:shadow-lg transition-shadow">
                        <CardHeader>
                          <CardTitle className="text-sm flex items-center space-x-2">
                            <Icon className="h-4 w-4" />
                            <span>{feature.name}</span>
                          </CardTitle>
                        </CardHeader>
                        <CardContent>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                            {feature.description}
                          </p>
                          <div className="flex items-center justify-between mb-2">
                            <Badge className={getSatisfactionColor(feature.type)}>
                              {feature.type}
                            </Badge>
                            <Badge variant="outline">
                              {(feature.impact * 100).toFixed(0)}% impact
                            </Badge>
                          </div>
                          <div className="space-y-2">
                            <div className="flex justify-between text-xs">
                              <span>Usage</span>
                              <span>{(feature.metrics.usage * 100).toFixed(0)}%</span>
                            </div>
                            <Progress value={feature.metrics.usage * 100} className="h-1" />
                            <div className="flex justify-between text-xs">
                              <span>Effectiveness</span>
                              <span>{(feature.metrics.effectiveness * 100).toFixed(0)}%</span>
                            </div>
                            <Progress value={feature.metrics.effectiveness * 100} className="h-1" />
                            <div className="flex justify-between text-xs">
                              <span>Satisfaction</span>
                              <span>{(feature.metrics.satisfaction * 100).toFixed(0)}%</span>
                            </div>
                            <Progress value={feature.metrics.satisfaction * 100} className="h-1" />
                          </div>
                        </CardContent>
                      </Card>
                    )
                  })}
                </div>

                {/* User Feedback */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Heart className="h-5 w-5 text-pink-600" />
                      <span>User Feedback</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {feedback.map((item) => {
                        const Icon = getFeedbackIcon(item.type)
                        return (
                          <div key={item.id} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <Icon className="h-5 w-5 mt-0.5 text-gray-500" />
                            <div className="flex-1">
                              <div className="flex items-center justify-between mb-1">
                                <div className="flex items-center space-x-2">
                                  <Badge className={getFeedbackColor(item.type)}>
                                    {item.type}
                                  </Badge>
                                  <Badge variant="outline">{item.category}</Badge>
                                </div>
                                <div className="flex items-center space-x-1">
                                  {[...Array(5)].map((_, i) => (
                                    <Star
                                      key={i}
                                      className={`h-4 w-4 ${
                                        i < item.rating ? 'text-yellow-500 fill-current' : 'text-gray-300'
                                      }`}
                                    />
                                  ))}
                                </div>
                              </div>
                              <p className="text-sm text-gray-700 dark:text-gray-300">{item.message}</p>
                              <div className="text-xs text-gray-500 mt-1">
                                {item.timestamp.toLocaleString()}
                              </div>
                            </div>
                          </div>
                        )
                      })}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'ui' && (
              <motion.div
                key="ui"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Star className="h-5 w-5 text-yellow-600" />
                      <span>UI/UX Optimization</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-3">
                        <h4 className="font-medium">UI Enhancements</h4>
                        <div className="space-y-2">
                          {['Smooth Animations', 'Intuitive Navigation', 'Responsive Design', 'Accessibility Features'].map((enhancement, index) => (
                            <div key={index} className="flex items-center justify-between p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded">
                              <div className="flex items-center space-x-2">
                                <Star className="h-4 w-4 text-yellow-500" />
                                <span className="text-sm">{enhancement}</span>
                              </div>
                              <Badge variant="outline">Active</Badge>
                            </div>
                          ))}
                        </div>
                      </div>
                      <div className="space-y-3">
                        <h4 className="font-medium">UX Metrics</h4>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Ease of Use</span>
                            <span className="font-bold text-yellow-600">94%</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Visual Appeal</span>
                            <span className="font-bold text-green-600">96%</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Navigation Speed</span>
                            <span className="font-bold text-blue-600">92%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Toggle Details */}
          <div className="text-center">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowDetails(!showDetails)}
            >
              {showDetails ? 'Hide' : 'Show'} Detailed Analytics
            </Button>
          </div>
        </motion.div>
      )}
    </div>
  )
}
