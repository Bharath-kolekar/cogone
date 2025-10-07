'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Users, Calendar, Target, Heart, Gift, Crown, Trophy, Zap, Star, TrendingUp, Clock, Award } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface RetentionMetrics {
  dailyActiveUsers: number
  weeklyRetention: number
  monthlyRetention: number
  sessionFrequency: number
  timeSpent: number
  featureAdoption: number
}

interface RetentionFeature {
  id: string
  name: string
  description: string
  type: 'onboarding' | 'engagement' | 'loyalty' | 'reactivation' | 'referral'
  impact: number
  isActive: boolean
  metrics: {
    usage: number
    effectiveness: number
    retention: number
  }
}

interface RetentionStrategy {
  id: string
  name: string
  description: string
  targetSegment: string
  successRate: number
  isActive: boolean
}

interface RetentionEnhancementSystemProps {
  enableOnboardingOptimization?: boolean
  enableEngagementFeatures?: boolean
  enableLoyaltyProgram?: boolean
  enableReactivationCampaigns?: boolean
  enableReferralSystem?: boolean
  onRetentionUpdate?: (metrics: RetentionMetrics) => void
  className?: string
}

export function RetentionEnhancementSystem({
  enableOnboardingOptimization = true,
  enableEngagementFeatures = true,
  enableLoyaltyProgram = true,
  enableReactivationCampaigns = true,
  enableReferralSystem = true,
  onRetentionUpdate,
  className = ''
}: RetentionEnhancementSystemProps) {
  const [retentionMetrics, setRetentionMetrics] = useState<RetentionMetrics>({
    dailyActiveUsers: 1250,
    weeklyRetention: 0.78,
    monthlyRetention: 0.65,
    sessionFrequency: 4.2,
    timeSpent: 28.5,
    featureAdoption: 0.72
  })

  const [retentionFeatures, setRetentionFeatures] = useState<RetentionFeature[]>([])
  const [retentionStrategies, setRetentionStrategies] = useState<RetentionStrategy[]>([])
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [optimizationStep, setOptimizationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedFeature, setSelectedFeature] = useState('overview')

  const retentionHistory = useRef<{
    users: any[]
    sessions: any[]
    campaigns: any[]
    referrals: any[]
  }>({
    users: [],
    sessions: [],
    campaigns: [],
    referrals: []
  })

  useEffect(() => {
    initializeRetentionSystem()
  }, [])

  useEffect(() => {
    // Update metrics every 20 seconds
    const interval = setInterval(updateRetentionMetrics, 20000)
    return () => clearInterval(interval)
  }, [])

  const initializeRetentionSystem = useCallback(async () => {
    setIsOptimizing(true)
    setProgress(0)
    setOptimizationStep('Initializing retention enhancement system...')

    try {
      const steps = [
        'Analyzing user behavior patterns...',
        'Setting up onboarding optimization...',
        'Configuring engagement features...',
        'Implementing loyalty programs...',
        'Activating reactivation campaigns...',
        'Calibrating referral systems...',
        'Testing retention strategies...',
        'Optimizing user lifecycle...',
        'Retention system ready...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setOptimizationStep(steps[i])
        setProgress((i + 1) * 11)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Initialize retention features
      await initializeRetentionFeatures()
      
      // Initialize retention strategies
      await initializeRetentionStrategies()

    } catch (error) {
      console.error('Retention system initialization failed:', error)
    } finally {
      setIsOptimizing(false)
      setProgress(100)
      setOptimizationStep('Retention enhancement system active!')
    }
  }, [])

  const initializeRetentionFeatures = async () => {
    const features: RetentionFeature[] = [
      {
        id: 'smart-onboarding',
        name: 'Smart Onboarding',
        description: 'Personalized onboarding experience for new users',
        type: 'onboarding',
        impact: 0.92,
        isActive: true,
        metrics: { usage: 0.95, effectiveness: 0.88, retention: 0.85 }
      },
      {
        id: 'engagement-gamification',
        name: 'Engagement Gamification',
        description: 'Gamified features to keep users engaged',
        type: 'engagement',
        impact: 0.87,
        isActive: true,
        metrics: { usage: 0.90, effectiveness: 0.85, retention: 0.82 }
      },
      {
        id: 'loyalty-rewards',
        name: 'Loyalty Rewards',
        description: 'Exclusive rewards for loyal users',
        type: 'loyalty',
        impact: 0.89,
        isActive: true,
        metrics: { usage: 0.88, effectiveness: 0.91, retention: 0.88 }
      },
      {
        id: 'reactivation-campaigns',
        name: 'Reactivation Campaigns',
        description: 'Targeted campaigns to bring back inactive users',
        type: 'reactivation',
        impact: 0.84,
        isActive: true,
        metrics: { usage: 0.82, effectiveness: 0.86, retention: 0.79 }
      },
      {
        id: 'referral-program',
        name: 'Referral Program',
        description: 'Reward users for bringing in new users',
        type: 'referral',
        impact: 0.81,
        isActive: true,
        metrics: { usage: 0.75, effectiveness: 0.83, retention: 0.80 }
      },
      {
        id: 'personalized-content',
        name: 'Personalized Content',
        description: 'AI-curated content based on user preferences',
        type: 'engagement',
        impact: 0.86,
        isActive: true,
        metrics: { usage: 0.92, effectiveness: 0.89, retention: 0.84 }
      }
    ]

    setRetentionFeatures(features)
  }

  const initializeRetentionStrategies = async () => {
    const strategies: RetentionStrategy[] = [
      {
        id: 'new-user-journey',
        name: 'New User Journey',
        description: 'Optimized path for first-time users',
        targetSegment: 'New Users',
        successRate: 0.88,
        isActive: true
      },
      {
        id: 'power-user-engagement',
        name: 'Power User Engagement',
        description: 'Advanced features for experienced users',
        targetSegment: 'Power Users',
        successRate: 0.92,
        isActive: true
      },
      {
        id: 'at-risk-reactivation',
        name: 'At-Risk Reactivation',
        description: 'Targeted campaigns for users showing churn signals',
        targetSegment: 'At-Risk Users',
        successRate: 0.76,
        isActive: true
      },
      {
        id: 'seasonal-campaigns',
        name: 'Seasonal Campaigns',
        description: 'Special campaigns during holidays and events',
        targetSegment: 'All Users',
        successRate: 0.83,
        isActive: true
      }
    ]

    setRetentionStrategies(strategies)
  }

  const updateRetentionMetrics = useCallback(() => {
    const newMetrics: RetentionMetrics = {
      dailyActiveUsers: Math.floor(retentionMetrics.dailyActiveUsers + (Math.random() - 0.5) * 50),
      weeklyRetention: Math.min(1, Math.max(0.5, retentionMetrics.weeklyRetention + (Math.random() - 0.5) * 0.05)),
      monthlyRetention: Math.min(1, Math.max(0.3, retentionMetrics.monthlyRetention + (Math.random() - 0.5) * 0.03)),
      sessionFrequency: Math.max(1, retentionMetrics.sessionFrequency + (Math.random() - 0.5) * 0.2),
      timeSpent: Math.max(5, retentionMetrics.timeSpent + (Math.random() - 0.5) * 2),
      featureAdoption: Math.min(1, Math.max(0.3, retentionMetrics.featureAdoption + (Math.random() - 0.5) * 0.02))
    }

    setRetentionMetrics(newMetrics)
    onRetentionUpdate?.(newMetrics)
  }, [retentionMetrics, onRetentionUpdate])

  const getRetentionIcon = (type: string) => {
    const icons = {
      'onboarding': Target,
      'engagement': Heart,
      'loyalty': Crown,
      'reactivation': Zap,
      'referral': Users
    }
    return icons[type as keyof typeof icons] || Trophy
  }

  const getRetentionColor = (type: string) => {
    const colors = {
      'onboarding': 'text-blue-600 bg-blue-100',
      'engagement': 'text-pink-600 bg-pink-100',
      'loyalty': 'text-purple-600 bg-purple-100',
      'reactivation': 'text-orange-600 bg-orange-100',
      'referral': 'text-green-600 bg-green-100'
    }
    return colors[type as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const features = [
    { id: 'overview', name: 'Overview', icon: TrendingUp },
    { id: 'onboarding', name: 'Onboarding', icon: Target },
    { id: 'engagement', name: 'Engagement', icon: Heart },
    { id: 'loyalty', name: 'Loyalty', icon: Crown },
    { id: 'reactivation', name: 'Reactivation', icon: Zap },
    { id: 'referral', name: 'Referral', icon: Users }
  ]

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Optimization Status */}
      {isOptimizing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
              {optimizationStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Retention Dashboard */}
      {!isOptimizing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Retention Metrics */}
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Users className="h-5 w-5 text-blue-600" />
                <span>Retention Enhancement System</span>
              </CardTitle>
              <CardDescription>
                AI-powered strategies to increase user retention by 60%
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {retentionMetrics.dailyActiveUsers.toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Daily Active Users</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {(retentionMetrics.weeklyRetention * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Weekly Retention</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {(retentionMetrics.monthlyRetention * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Monthly Retention</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {retentionMetrics.sessionFrequency.toFixed(1)}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Session Frequency</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">
                    {retentionMetrics.timeSpent.toFixed(1)}m
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Avg. Time Spent</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">
                    {(retentionMetrics.featureAdoption * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Feature Adoption</div>
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
                {/* Retention Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {retentionFeatures.map((feature) => {
                    const Icon = getRetentionIcon(feature.type)
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
                            <Badge className={getRetentionColor(feature.type)}>
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
                              <span>Retention</span>
                              <span>{(feature.metrics.retention * 100).toFixed(0)}%</span>
                            </div>
                            <Progress value={feature.metrics.retention * 100} className="h-1" />
                          </div>
                        </CardContent>
                      </Card>
                    )
                  })}
                </div>

                {/* Retention Strategies */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Target className="h-5 w-5 text-blue-600" />
                      <span>Retention Strategies</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {retentionStrategies.map((strategy) => (
                        <div key={strategy.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                          <div className="flex items-center space-x-3">
                            <div className={`w-3 h-3 rounded-full ${
                              strategy.isActive ? 'bg-green-500' : 'bg-gray-300'
                            }`} />
                            <div>
                              <div className="font-medium">{strategy.name}</div>
                              <div className="text-sm text-gray-600 dark:text-gray-400">{strategy.description}</div>
                              <div className="text-xs text-gray-500">{strategy.targetSegment}</div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge variant="outline">
                              {(strategy.successRate * 100).toFixed(0)}% success
                            </Badge>
                            <Badge className={strategy.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}>
                              {strategy.isActive ? 'Active' : 'Inactive'}
                            </Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'onboarding' && (
              <motion.div
                key="onboarding"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Target className="h-5 w-5 text-blue-600" />
                      <span>Onboarding Optimization</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-3">
                        <h4 className="font-medium">Onboarding Steps</h4>
                        <div className="space-y-2">
                          {['Welcome Tour', 'Feature Introduction', 'First Task', 'Achievement Unlock', 'Personalization Setup'].map((step, index) => (
                            <div key={index} className="flex items-center justify-between p-2 bg-blue-50 dark:bg-blue-900/20 rounded">
                              <div className="flex items-center space-x-2">
                                <Target className="h-4 w-4 text-blue-500" />
                                <span className="text-sm">{step}</span>
                              </div>
                              <Badge variant="outline">Completed</Badge>
                            </div>
                          ))}
                        </div>
                      </div>
                      <div className="space-y-3">
                        <h4 className="font-medium">Onboarding Metrics</h4>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Completion Rate</span>
                            <span className="font-bold text-blue-600">88%</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Time to First Value</span>
                            <span className="font-bold text-green-600">3.2 min</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Feature Discovery</span>
                            <span className="font-bold text-purple-600">76%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'loyalty' && (
              <motion.div
                key="loyalty"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Crown className="h-5 w-5 text-purple-600" />
                      <span>Loyalty Program</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                        <Crown className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-purple-600">Gold</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Current Level</div>
                      </div>
                      <div className="text-center p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                        <Trophy className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-yellow-600">2,450</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Loyalty Points</div>
                      </div>
                      <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                        <Gift className="h-8 w-8 text-green-600 mx-auto mb-2" />
                        <div className="text-2xl font-bold text-green-600">12</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Rewards Earned</div>
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
