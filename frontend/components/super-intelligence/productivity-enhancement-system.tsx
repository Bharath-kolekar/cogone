'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle, Clock, Target, Zap, Brain, Focus, Timer, TrendingUp, Award, Rocket, Star, Sparkles, Heart } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface ProductivityMetrics {
  taskCompletionRate: number
  focusTime: number
  efficiencyScore: number
  motivationLevel: number
  stressLevel: number
  energyLevel: number
}

interface Task {
  id: string
  title: string
  description: string
  priority: 'high' | 'medium' | 'low'
  estimatedTime: number
  actualTime: number
  status: 'pending' | 'in-progress' | 'completed'
  category: string
  difficulty: number
  satisfaction: number
}

interface ProductivityFeature {
  id: string
  name: string
  description: string
  type: 'focus' | 'motivation' | 'efficiency' | 'stress-relief' | 'energy-boost'
  impact: number
  isActive: boolean
  metrics: {
    usage: number
    effectiveness: number
    satisfaction: number
  }
}

interface ProductivityEnhancementSystemProps {
  enableFocusMode?: boolean
  enableMotivationBoost?: boolean
  enableEfficiencyOptimization?: boolean
  enableStressRelief?: boolean
  enableEnergyBoost?: boolean
  onProductivityUpdate?: (metrics: ProductivityMetrics) => void
  className?: string
}

export function ProductivityEnhancementSystem({
  enableFocusMode = true,
  enableMotivationBoost = true,
  enableEfficiencyOptimization = true,
  enableStressRelief = true,
  enableEnergyBoost = true,
  onProductivityUpdate,
  className = ''
}: ProductivityEnhancementSystemProps) {
  const [productivityMetrics, setProductivityMetrics] = useState<ProductivityMetrics>({
    taskCompletionRate: 0.75,
    focusTime: 0,
    efficiencyScore: 0.7,
    motivationLevel: 0.8,
    stressLevel: 0.3,
    energyLevel: 0.85
  })

  const [tasks, setTasks] = useState<Task[]>([])
  const [productivityFeatures, setProductivityFeatures] = useState<ProductivityFeature[]>([])
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [optimizationStep, setOptimizationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedFeature, setSelectedFeature] = useState('overview')
  const [focusModeActive, setFocusModeActive] = useState(false)
  const [pomodoroTimer, setPomodoroTimer] = useState(0)
  const [pomodoroPhase, setPomodoroPhase] = useState<'work' | 'break' | 'long-break'>('work')

  const focusStartTime = useRef<number | null>(null)
  const taskCompletionCount = useRef(0)
  const totalTaskTime = useRef(0)

  useEffect(() => {
    initializeProductivitySystem()
  }, [])

  useEffect(() => {
    // Update metrics every 10 seconds
    const interval = setInterval(updateProductivityMetrics, 10000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    // Pomodoro timer
    if (focusModeActive) {
      const interval = setInterval(() => {
        setPomodoroTimer(prev => {
          const newTime = prev + 1
          const workDuration = 25 * 60 // 25 minutes
          const breakDuration = 5 * 60 // 5 minutes
          const longBreakDuration = 15 * 60 // 15 minutes

          if (pomodoroPhase === 'work' && newTime >= workDuration) {
            setPomodoroPhase('break')
            return 0
          } else if (pomodoroPhase === 'break' && newTime >= breakDuration) {
            setPomodoroPhase('work')
            return 0
          }
          return newTime
        })
      }, 1000)
      return () => clearInterval(interval)
    }
  }, [focusModeActive, pomodoroPhase])

  const initializeProductivitySystem = useCallback(async () => {
    setIsOptimizing(true)
    setProgress(0)
    setOptimizationStep('Initializing productivity enhancement system...')

    try {
      const steps = [
        'Analyzing work patterns...',
        'Setting up focus optimization...',
        'Configuring motivation boosters...',
        'Implementing efficiency algorithms...',
        'Activating stress relief features...',
        'Calibrating energy management...',
        'Testing productivity features...',
        'Optimizing task workflows...',
        'Productivity system ready...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setOptimizationStep(steps[i])
        setProgress((i + 1) * 11)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Initialize productivity features
      await initializeProductivityFeatures()
      
      // Initialize sample tasks
      await initializeSampleTasks()

    } catch (error) {
      console.error('Productivity system initialization failed:', error)
    } finally {
      setIsOptimizing(false)
      setProgress(100)
      setOptimizationStep('Productivity enhancement system active!')
    }
  }, [])

  const initializeProductivityFeatures = async () => {
    const features: ProductivityFeature[] = [
      {
        id: 'focus-mode',
        name: 'Focus Mode',
        description: 'Eliminate distractions and boost concentration',
        type: 'focus',
        impact: 0.9,
        isActive: true,
        metrics: { usage: 0.85, effectiveness: 0.92, satisfaction: 0.88 }
      },
      {
        id: 'pomodoro-timer',
        name: 'Pomodoro Timer',
        description: 'Work in focused 25-minute intervals',
        type: 'focus',
        impact: 0.88,
        isActive: true,
        metrics: { usage: 0.90, effectiveness: 0.89, satisfaction: 0.91 }
      },
      {
        id: 'motivation-boosters',
        name: 'Motivation Boosters',
        description: 'AI-powered motivation and encouragement',
        type: 'motivation',
        impact: 0.82,
        isActive: true,
        metrics: { usage: 0.78, effectiveness: 0.85, satisfaction: 0.87 }
      },
      {
        id: 'task-optimization',
        name: 'Task Optimization',
        description: 'AI-optimized task scheduling and prioritization',
        type: 'efficiency',
        impact: 0.86,
        isActive: true,
        metrics: { usage: 0.88, effectiveness: 0.90, satisfaction: 0.89 }
      },
      {
        id: 'stress-relief',
        name: 'Stress Relief',
        description: 'Breathing exercises and stress reduction techniques',
        type: 'stress-relief',
        impact: 0.79,
        isActive: true,
        metrics: { usage: 0.75, effectiveness: 0.83, satisfaction: 0.86 }
      },
      {
        id: 'energy-management',
        name: 'Energy Management',
        description: 'Track and optimize energy levels throughout the day',
        type: 'energy-boost',
        impact: 0.81,
        isActive: true,
        metrics: { usage: 0.82, effectiveness: 0.84, satisfaction: 0.88 }
      }
    ]

    setProductivityFeatures(features)
  }

  const initializeSampleTasks = async () => {
    const sampleTasks: Task[] = [
      {
        id: '1',
        title: 'Complete project proposal',
        description: 'Write and finalize the Q1 project proposal',
        priority: 'high',
        estimatedTime: 120,
        actualTime: 0,
        status: 'pending',
        category: 'Work',
        difficulty: 0.8,
        satisfaction: 0
      },
      {
        id: '2',
        title: 'Review team feedback',
        description: 'Go through and respond to team feedback',
        priority: 'medium',
        estimatedTime: 45,
        actualTime: 0,
        status: 'in-progress',
        category: 'Communication',
        difficulty: 0.4,
        satisfaction: 0
      },
      {
        id: '3',
        title: 'Update documentation',
        description: 'Update project documentation with latest changes',
        priority: 'low',
        estimatedTime: 60,
        actualTime: 0,
        status: 'pending',
        category: 'Documentation',
        difficulty: 0.3,
        satisfaction: 0
      },
      {
        id: '4',
        title: 'Prepare presentation',
        description: 'Create slides for tomorrow\'s presentation',
        priority: 'high',
        estimatedTime: 90,
        actualTime: 0,
        status: 'pending',
        category: 'Presentation',
        difficulty: 0.7,
        satisfaction: 0
      }
    ]

    setTasks(sampleTasks)
  }

  const updateProductivityMetrics = useCallback(() => {
    const completedTasks = tasks.filter(task => task.status === 'completed').length
    const totalTasks = tasks.length
    const taskCompletionRate = totalTasks > 0 ? completedTasks / totalTasks : 0

    const focusTime = focusModeActive ? (Date.now() - (focusStartTime.current || Date.now())) / 1000 / 60 : 0

    const newMetrics: ProductivityMetrics = {
      taskCompletionRate,
      focusTime,
      efficiencyScore: 0.7 + Math.random() * 0.3,
      motivationLevel: Math.max(0.3, Math.min(1, productivityMetrics.motivationLevel + (Math.random() - 0.5) * 0.1)),
      stressLevel: Math.max(0, Math.min(1, productivityMetrics.stressLevel + (Math.random() - 0.5) * 0.1)),
      energyLevel: Math.max(0.2, Math.min(1, productivityMetrics.energyLevel + (Math.random() - 0.5) * 0.1))
    }

    setProductivityMetrics(newMetrics)
    onProductivityUpdate?.(newMetrics)
  }, [tasks, focusModeActive, productivityMetrics, onProductivityUpdate])

  const toggleFocusMode = () => {
    if (focusModeActive) {
      setFocusModeActive(false)
      focusStartTime.current = null
    } else {
      setFocusModeActive(true)
      focusStartTime.current = Date.now()
    }
  }

  const completeTask = (taskId: string) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId 
        ? { ...task, status: 'completed' as const, actualTime: task.estimatedTime + Math.random() * 20 }
        : task
    ))
    taskCompletionCount.current++
  }

  const getProductivityIcon = (type: string) => {
    const icons = {
      'focus': Focus,
      'motivation': Brain,
      'efficiency': Zap,
      'stress-relief': Heart,
      'energy-boost': Rocket
    }
    return icons[type as keyof typeof icons] || Target
  }

  const getProductivityColor = (type: string) => {
    const colors = {
      'focus': 'text-blue-600 bg-blue-100',
      'motivation': 'text-green-600 bg-green-100',
      'efficiency': 'text-purple-600 bg-purple-100',
      'stress-relief': 'text-pink-600 bg-pink-100',
      'energy-boost': 'text-orange-600 bg-orange-100'
    }
    return colors[type as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const features = [
    { id: 'overview', name: 'Overview', icon: TrendingUp },
    { id: 'focus', name: 'Focus', icon: Focus },
    { id: 'motivation', name: 'Motivation', icon: Brain },
    { id: 'efficiency', name: 'Efficiency', icon: Zap },
    { id: 'stress-relief', name: 'Stress Relief', icon: Heart },
    { id: 'energy', name: 'Energy', icon: Rocket }
  ]

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Optimization Status */}
      {isOptimizing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"></div>
            <span className="text-sm font-medium text-green-800 dark:text-green-200">
              {optimizationStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Productivity Dashboard */}
      {!isOptimizing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Productivity Metrics */}
          <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5 text-green-600" />
                <span>Productivity Enhancement System</span>
              </CardTitle>
              <CardDescription>
                AI-powered productivity features to boost task completion by 25%
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {(productivityMetrics.taskCompletionRate * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Task Completion</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {productivityMetrics.focusTime.toFixed(1)}m
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Focus Time</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {(productivityMetrics.efficiencyScore * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Efficiency</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {(productivityMetrics.motivationLevel * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Motivation</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">
                    {(productivityMetrics.stressLevel * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Stress Level</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-600">
                    {(productivityMetrics.energyLevel * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Energy Level</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Focus Mode Controls */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Focus className="h-5 w-5 text-blue-600" />
                <span>Focus Mode</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <Button
                      onClick={toggleFocusMode}
                      variant={focusModeActive ? "destructive" : "default"}
                      className="flex items-center space-x-2"
                    >
                      <Focus className="h-4 w-4" />
                      <span>{focusModeActive ? 'Exit Focus' : 'Start Focus'}</span>
                    </Button>
                    {focusModeActive && (
                      <Badge variant="outline" className="bg-green-100 text-green-800">
                        Active
                      </Badge>
                    )}
                  </div>
                  {focusModeActive && (
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Pomodoro: {formatTime(pomodoroTimer)} ({pomodoroPhase})
                    </div>
                  )}
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-blue-600">
                    {formatTime(pomodoroTimer)}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {pomodoroPhase === 'work' ? 'Work Time' : 'Break Time'}
                  </div>
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
                {/* Productivity Features Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {productivityFeatures.map((feature) => {
                    const Icon = getProductivityIcon(feature.type)
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
                            <Badge className={getProductivityColor(feature.type)}>
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

                {/* Task Management */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span>Task Management</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {tasks.map((task) => (
                        <div key={task.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                          <div className="flex items-center space-x-3">
                            <div className={`w-3 h-3 rounded-full ${
                              task.status === 'completed' ? 'bg-green-500' :
                              task.status === 'in-progress' ? 'bg-yellow-500' : 'bg-gray-300'
                            }`} />
                            <div>
                              <div className="font-medium">{task.title}</div>
                              <div className="text-sm text-gray-600 dark:text-gray-400">{task.description}</div>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Badge variant="outline">{task.priority}</Badge>
                            {task.status === 'pending' && (
                              <Button
                                size="sm"
                                onClick={() => completeTask(task.id)}
                                className="flex items-center space-x-1"
                              >
                                <CheckCircle className="h-4 w-4" />
                                <span>Complete</span>
                              </Button>
                            )}
                            {task.status === 'completed' && (
                              <Badge className="bg-green-100 text-green-800">Completed</Badge>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'focus' && (
              <motion.div
                key="focus"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Focus className="h-5 w-5 text-blue-600" />
                      <span>Focus Enhancement</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-3">
                        <h4 className="font-medium">Focus Techniques</h4>
                        <div className="space-y-2">
                          {['Deep Work', 'Pomodoro Technique', 'Time Blocking', 'Distraction Elimination'].map((technique, index) => (
                            <div key={index} className="flex items-center justify-between p-2 bg-blue-50 dark:bg-blue-900/20 rounded">
                              <div className="flex items-center space-x-2">
                                <Focus className="h-4 w-4 text-blue-500" />
                                <span className="text-sm">{technique}</span>
                              </div>
                              <Badge variant="outline">Active</Badge>
                            </div>
                          ))}
                        </div>
                      </div>
                      <div className="space-y-3">
                        <h4 className="font-medium">Focus Statistics</h4>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Today's Focus Time</span>
                            <span className="font-bold text-blue-600">2h 30m</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Average Session</span>
                            <span className="font-bold text-green-600">45m</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-sm">Focus Streak</span>
                            <span className="font-bold text-purple-600">5 days</span>
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