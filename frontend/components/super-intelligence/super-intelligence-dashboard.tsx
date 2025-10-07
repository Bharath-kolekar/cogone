'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Heart, Eye, Target, Activity, BarChart3, Settings, Zap, Award, TrendingUp, Users, Clock, Star } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { SuperIntelligenceOrchestrator } from './super-intelligence-orchestrator'

interface SuperIntelligenceDashboardProps {
  userId?: string
  enableAllFeatures?: boolean
  showAdvancedMetrics?: boolean
  enableRealTimeUpdates?: boolean
  className?: string
}

export function SuperIntelligenceDashboard({
  userId,
  enableAllFeatures = true,
  showAdvancedMetrics = true,
  enableRealTimeUpdates = true,
  className = ''
}: SuperIntelligenceDashboardProps) {
  const [isActive, setIsActive] = useState(false)
  const [systemStatus, setSystemStatus] = useState<'initializing' | 'active' | 'learning' | 'optimizing'>('initializing')
  const [userEngagement, setUserEngagement] = useState({
    sessionTime: 0,
    interactions: 0,
    adaptations: 0,
    productivity: 0.7,
    satisfaction: 0.8
  })
  const [showSettings, setShowSettings] = useState(false)
  const [selectedFeature, setSelectedFeature] = useState('overview')

  const sessionStart = useRef(Date.now())
  const updateInterval = useRef<NodeJS.Timeout>()

  useEffect(() => {
    if (enableRealTimeUpdates) {
      startRealTimeUpdates()
    }
    return () => {
      if (updateInterval.current) {
        clearInterval(updateInterval.current)
      }
    }
  }, [enableRealTimeUpdates])

  const startRealTimeUpdates = () => {
    updateInterval.current = setInterval(() => {
      setUserEngagement(prev => ({
        sessionTime: Math.floor((Date.now() - sessionStart.current) / 1000 / 60), // minutes
        interactions: prev.interactions + Math.floor(Math.random() * 3),
        adaptations: prev.adaptations + Math.floor(Math.random() * 2),
        productivity: Math.min(0.95, prev.productivity + (Math.random() - 0.5) * 0.1),
        satisfaction: Math.min(0.95, prev.satisfaction + (Math.random() - 0.5) * 0.05)
      }))
    }, 5000)
  }

  const features = [
    {
      id: 'overview',
      name: 'System Overview',
      icon: Brain,
      description: 'Complete system status and metrics',
      color: 'text-blue-600 bg-blue-100'
    },
    {
      id: 'mood',
      name: 'Mood Detection',
      icon: Heart,
      description: 'AI-powered emotional analysis',
      color: 'text-pink-600 bg-pink-100'
    },
    {
      id: 'adaptation',
      name: 'UI Adaptation',
      icon: Eye,
      description: 'Dynamic interface optimization',
      color: 'text-green-600 bg-green-100'
    },
    {
      id: 'productivity',
      name: 'Productivity Boost',
      icon: Target,
      description: 'Enhanced productivity features',
      color: 'text-purple-600 bg-purple-100'
    },
    {
      id: 'learning',
      name: 'Learning System',
      icon: Activity,
      description: 'Continuous AI learning',
      color: 'text-orange-600 bg-orange-100'
    },
    {
      id: 'analytics',
      name: 'Analytics',
      icon: BarChart3,
      description: 'Performance insights',
      color: 'text-red-600 bg-red-100'
    }
  ]

  const getFeatureIcon = (featureId: string) => {
    const feature = features.find(f => f.id === featureId)
    return feature?.icon || Brain
  }

  const getFeatureColor = (featureId: string) => {
    const feature = features.find(f => f.id === featureId)
    return feature?.color || 'text-gray-600 bg-gray-100'
  }

  return (
    <div className={`min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 ${className}`}>
      {/* Header */}
      <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Brain className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                    Super Intelligence Dashboard
                  </h1>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    AI-powered mood detection and productivity enhancement
                  </p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Badge 
                variant={systemStatus === 'active' ? 'default' : 'secondary'}
                className="flex items-center space-x-2"
              >
                <div className={`w-2 h-2 rounded-full ${
                  systemStatus === 'active' ? 'bg-green-500' : 
                  systemStatus === 'learning' ? 'bg-yellow-500' : 
                  'bg-gray-500'
                }`} />
                <span className="capitalize">{systemStatus}</span>
              </Badge>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowSettings(!showSettings)}
              >
                <Settings className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                    <Clock className="h-6 w-6 text-blue-600" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {userEngagement.sessionTime}m
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Session Time
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                    <Activity className="h-6 w-6 text-green-600" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {userEngagement.interactions}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Interactions
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                    <Target className="h-6 w-6 text-purple-600" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {(userEngagement.productivity * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Productivity
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-pink-100 dark:bg-pink-900/20 rounded-lg flex items-center justify-center">
                    <Star className="h-6 w-6 text-pink-600" />
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      {(userEngagement.satisfaction * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Satisfaction
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Feature Navigation */}
          <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Zap className="h-5 w-5 text-blue-600" />
                <span>Super Intelligence Features</span>
              </CardTitle>
              <CardDescription>
                Select a feature to explore AI-powered capabilities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                {features.map((feature) => {
                  const Icon = feature.icon
                  return (
                    <Button
                      key={feature.id}
                      variant={selectedFeature === feature.id ? 'default' : 'outline'}
                      className="h-auto p-4 flex flex-col items-center space-y-2"
                      onClick={() => setSelectedFeature(feature.id)}
                    >
                      <Icon className="h-6 w-6" />
                      <div className="text-center">
                        <div className="font-medium text-sm">{feature.name}</div>
                        <div className="text-xs text-gray-500 mt-1">
                          {feature.description}
                        </div>
                      </div>
                    </Button>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {/* Selected Feature Content */}
          <AnimatePresence mode="wait">
            {selectedFeature === 'overview' && (
              <motion.div
                key="overview"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
        <SuperIntelligenceOrchestrator
          enableMoodDetection={enableAllFeatures}
          enableUIAdaptation={enableAllFeatures}
          enableProductivityBoost={enableAllFeatures}
          enableLearning={enableAllFeatures}
          enablePredictions={enableAllFeatures}
          enableAdvancedAI={enableAllFeatures}
          enableBiometricIntegration={enableAllFeatures}
          enableSocialFeatures={enableAllFeatures}
          enableAdvancedAnalytics={enableAllFeatures}
          enableVoiceIntegration={enableAllFeatures}
          enableAdvancedEngagement={enableAllFeatures}
          enableProductivityEnhancement={enableAllFeatures}
          enableSatisfactionEnhancement={enableAllFeatures}
          enableRetentionEnhancement={enableAllFeatures}
        />
              </motion.div>
            )}

            {selectedFeature === 'mood' && (
              <motion.div
                key="mood"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Heart className="h-5 w-5 text-pink-600" />
                      <span>Mood Detection System</span>
                    </CardTitle>
                    <CardDescription>
                      Advanced AI-powered emotional analysis and mood tracking
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <SuperIntelligenceOrchestrator
                      enableMoodDetection={true}
                      enableUIAdaptation={false}
                      enableProductivityBoost={false}
                      enableLearning={false}
                      enablePredictions={false}
                    />
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'adaptation' && (
              <motion.div
                key="adaptation"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Eye className="h-5 w-5 text-green-600" />
                      <span>UI Adaptation System</span>
                    </CardTitle>
                    <CardDescription>
                      Dynamic interface optimization based on user mood and behavior
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <SuperIntelligenceOrchestrator
                      enableMoodDetection={false}
                      enableUIAdaptation={true}
                      enableProductivityBoost={false}
                      enableLearning={false}
                      enablePredictions={false}
                    />
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'productivity' && (
              <motion.div
                key="productivity"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Target className="h-5 w-5 text-purple-600" />
                      <span>Productivity Enhancement</span>
                    </CardTitle>
                    <CardDescription>
                      AI-powered productivity boosters and efficiency optimization
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <SuperIntelligenceOrchestrator
                      enableMoodDetection={false}
                      enableUIAdaptation={false}
                      enableProductivityBoost={true}
                      enableLearning={false}
                      enablePredictions={false}
                    />
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'learning' && (
              <motion.div
                key="learning"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Activity className="h-5 w-5 text-orange-600" />
                      <span>Learning System</span>
                    </CardTitle>
                    <CardDescription>
                      Continuous AI learning and adaptation based on user interactions
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <SuperIntelligenceOrchestrator
                      enableMoodDetection={false}
                      enableUIAdaptation={false}
                      enableProductivityBoost={false}
                      enableLearning={true}
                      enablePredictions={false}
                    />
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'analytics' && (
              <motion.div
                key="analytics"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <BarChart3 className="h-5 w-5 text-red-600" />
                      <span>Analytics & Insights</span>
                    </CardTitle>
                    <CardDescription>
                      Comprehensive performance metrics and user behavior analysis
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <SuperIntelligenceOrchestrator
                      enableMoodDetection={false}
                      enableUIAdaptation={false}
                      enableProductivityBoost={false}
                      enableLearning={false}
                      enablePredictions={true}
                    />
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Settings Panel */}
          {showSettings && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <Card className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Settings className="h-5 w-5 text-gray-600" />
                    <span>System Settings</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">Mood Detection</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          Enable AI-powered emotional analysis
                        </div>
                      </div>
                      <Button variant="outline" size="sm">
                        {enableAllFeatures ? 'Enabled' : 'Disabled'}
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">UI Adaptation</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          Dynamic interface optimization
                        </div>
                      </div>
                      <Button variant="outline" size="sm">
                        {enableAllFeatures ? 'Enabled' : 'Disabled'}
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">Productivity Boost</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          Enhanced productivity features
                        </div>
                      </div>
                      <Button variant="outline" size="sm">
                        {enableAllFeatures ? 'Enabled' : 'Disabled'}
                      </Button>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">Learning System</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          Continuous AI learning
                        </div>
                      </div>
                      <Button variant="outline" size="sm">
                        {enableAllFeatures ? 'Enabled' : 'Disabled'}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}
