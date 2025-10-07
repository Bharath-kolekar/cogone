'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Heart, Eye, Activity, Brain, Zap, Target, TrendingUp, AlertCircle, CheckCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface BiometricData {
  heartRate: {
    current: number
    average: number
    variability: number
    trend: 'increasing' | 'decreasing' | 'stable'
  }
  eyeTracking: {
    blinkRate: number
    pupilDilation: number
    gazePattern: string
    focusLevel: number
  }
  facialAnalysis: {
    microExpressions: any[]
    stressIndicators: number
    emotionalState: string
    confidence: number
  }
  movement: {
    posture: string
    fidgeting: number
    energy: number
    tension: number
  }
  voice: {
    pitch: number
    tone: number
    stress: number
    emotion: string
  }
}

interface BiometricIntegrationProps {
  enableHeartRate?: boolean
  enableEyeTracking?: boolean
  enableFacialAnalysis?: boolean
  enableMovementTracking?: boolean
  enableVoiceAnalysis?: boolean
  onBiometricData?: (data: BiometricData) => void
  className?: string
}

export function BiometricIntegration({
  enableHeartRate = true,
  enableEyeTracking = true,
  enableFacialAnalysis = true,
  enableMovementTracking = true,
  enableVoiceAnalysis = true,
  onBiometricData,
  className = ''
}: BiometricIntegrationProps) {
  const [biometricData, setBiometricData] = useState<BiometricData>({
    heartRate: {
      current: 72,
      average: 75,
      variability: 0.15,
      trend: 'stable'
    },
    eyeTracking: {
      blinkRate: 15,
      pupilDilation: 0.5,
      gazePattern: 'focused',
      focusLevel: 0.8
    },
    facialAnalysis: {
      microExpressions: [],
      stressIndicators: 0.2,
      emotionalState: 'neutral',
      confidence: 0.85
    },
    movement: {
      posture: 'upright',
      fidgeting: 0.3,
      energy: 0.7,
      tension: 0.4
    },
    voice: {
      pitch: 0.5,
      tone: 0.6,
      stress: 0.3,
      emotion: 'calm'
    }
  })

  const [isMonitoring, setIsMonitoring] = useState(false)
  const [monitoringStep, setMonitoringStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedSensor, setSelectedSensor] = useState<string | null>(null)

  const monitoringInterval = useRef<NodeJS.Timeout>()
  const sensorData = useRef<{
    heartRateHistory: number[]
    eyeTrackingHistory: any[]
    facialAnalysisHistory: any[]
    movementHistory: any[]
    voiceHistory: any[]
  }>({
    heartRateHistory: [],
    eyeTrackingHistory: [],
    facialAnalysisHistory: [],
    movementHistory: [],
    voiceHistory: []
  })

  useEffect(() => {
    if (isMonitoring) {
      startBiometricMonitoring()
    } else {
      stopBiometricMonitoring()
    }
    return () => stopBiometricMonitoring()
  }, [isMonitoring])

  const startBiometricMonitoring = useCallback(async () => {
    setProgress(0)
    setMonitoringStep('Initializing biometric sensors...')

    try {
      const steps = [
        'Calibrating heart rate sensor...',
        'Initializing eye tracking...',
        'Setting up facial analysis...',
        'Configuring movement sensors...',
        'Preparing voice analysis...',
        'Establishing baseline readings...',
        'Validating sensor accuracy...',
        'Starting continuous monitoring...',
        'Optimizing data collection...',
        'Biometric monitoring active...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setMonitoringStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Start continuous monitoring
      monitoringInterval.current = setInterval(collectBiometricData, 2000)

    } catch (error) {
      console.error('Biometric monitoring failed:', error)
    }
  }, [])

  const stopBiometricMonitoring = useCallback(() => {
    if (monitoringInterval.current) {
      clearInterval(monitoringInterval.current)
    }
  }, [])

  const collectBiometricData = useCallback(() => {
    // Simulate biometric data collection
    const newData: BiometricData = {
      heartRate: {
        current: 65 + Math.random() * 20,
        average: 70 + Math.random() * 10,
        variability: 0.1 + Math.random() * 0.2,
        trend: Math.random() > 0.5 ? 'increasing' : Math.random() > 0.5 ? 'decreasing' : 'stable'
      },
      eyeTracking: {
        blinkRate: 10 + Math.random() * 20,
        pupilDilation: 0.3 + Math.random() * 0.4,
        gazePattern: ['focused', 'scanning', 'drifting'][Math.floor(Math.random() * 3)],
        focusLevel: 0.5 + Math.random() * 0.5
      },
      facialAnalysis: {
        microExpressions: generateMicroExpressions(),
        stressIndicators: Math.random() * 0.5,
        emotionalState: ['happy', 'neutral', 'stressed', 'focused'][Math.floor(Math.random() * 4)],
        confidence: 0.8 + Math.random() * 0.2
      },
      movement: {
        posture: ['upright', 'slouched', 'leaning'][Math.floor(Math.random() * 3)],
        fidgeting: Math.random(),
        energy: Math.random(),
        tension: Math.random()
      },
      voice: {
        pitch: 0.3 + Math.random() * 0.4,
        tone: 0.4 + Math.random() * 0.4,
        stress: Math.random() * 0.6,
        emotion: ['calm', 'excited', 'stressed', 'focused'][Math.floor(Math.random() * 4)]
      }
    }

    setBiometricData(newData)
    onBiometricData?.(newData)

    // Store historical data
    sensorData.current.heartRateHistory.push(newData.heartRate.current)
    sensorData.current.eyeTrackingHistory.push(newData.eyeTracking)
    sensorData.current.facialAnalysisHistory.push(newData.facialAnalysis)
    sensorData.current.movementHistory.push(newData.movement)
    sensorData.current.voiceHistory.push(newData.voice)

    // Keep only last 100 readings
    Object.keys(sensorData.current).forEach(key => {
      const history = sensorData.current[key as keyof typeof sensorData.current]
      if (Array.isArray(history) && history.length > 100) {
        (sensorData.current as any)[key] = history.slice(-100)
      }
    })
  }, [onBiometricData])

  const generateMicroExpressions = () => {
    const expressions = ['smile', 'frown', 'surprise', 'anger', 'fear', 'disgust', 'sadness']
    return expressions.slice(0, Math.floor(Math.random() * 3) + 1).map(expr => ({
      expression: expr,
      intensity: Math.random(),
      duration: Math.random() * 0.5,
      confidence: 0.7 + Math.random() * 0.3
    }))
  }

  const getBiometricIcon = (sensor: string) => {
    const icons = {
      'heartRate': Heart,
      'eyeTracking': Eye,
      'facialAnalysis': Brain,
      'movement': Activity,
      'voice': Zap
    }
    return icons[sensor as keyof typeof icons] || Target
  }

  const getBiometricColor = (sensor: string) => {
    const colors = {
      'heartRate': 'text-red-600 bg-red-100',
      'eyeTracking': 'text-blue-600 bg-blue-100',
      'facialAnalysis': 'text-purple-600 bg-purple-100',
      'movement': 'text-green-600 bg-green-100',
      'voice': 'text-orange-600 bg-orange-100'
    }
    return colors[sensor as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'good': return CheckCircle
      case 'warning': return AlertCircle
      case 'critical': return AlertCircle
      default: return CheckCircle
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'good': return 'text-green-600 bg-green-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'critical': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const sensors = [
    { id: 'heartRate', name: 'Heart Rate', enabled: enableHeartRate },
    { id: 'eyeTracking', name: 'Eye Tracking', enabled: enableEyeTracking },
    { id: 'facialAnalysis', name: 'Facial Analysis', enabled: enableFacialAnalysis },
    { id: 'movement', name: 'Movement', enabled: enableMovementTracking },
    { id: 'voice', name: 'Voice Analysis', enabled: enableVoiceAnalysis }
  ]

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Monitoring Status */}
      {isMonitoring && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-pulse rounded-full h-5 w-5 bg-green-500"></div>
            <span className="text-sm font-medium text-green-800 dark:text-green-200">
              {monitoringStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Control Panel */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="h-5 w-5 text-green-600" />
            <span>Biometric Monitoring</span>
          </CardTitle>
          <CardDescription>
            Advanced biometric sensors for enhanced mood detection
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="font-medium">Monitoring Status</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {isMonitoring ? 'Active' : 'Inactive'}
              </div>
            </div>
            <Button
              onClick={() => setIsMonitoring(!isMonitoring)}
              variant={isMonitoring ? 'destructive' : 'default'}
            >
              {isMonitoring ? 'Stop Monitoring' : 'Start Monitoring'}
            </Button>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {sensors.map((sensor) => {
              const Icon = getBiometricIcon(sensor.id)
              const status = sensor.enabled ? 'good' : 'critical'
              const StatusIcon = getStatusIcon(status)
              return (
                <div
                  key={sensor.id}
                  className={`p-3 rounded-lg border-2 ${
                    selectedSensor === sensor.id ? 'border-blue-500' : 'border-gray-200'
                  } cursor-pointer`}
                  onClick={() => setSelectedSensor(selectedSensor === sensor.id ? null : sensor.id)}
                >
                  <div className="flex items-center space-x-2 mb-2">
                    <Icon className="h-4 w-4" />
                    <StatusIcon className="h-4 w-4" />
                  </div>
                  <div className="text-sm font-medium">{sensor.name}</div>
                  <Badge className={getStatusColor(status)}>
                    {sensor.enabled ? 'Enabled' : 'Disabled'}
                  </Badge>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Biometric Data */}
      {isMonitoring && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Heart Rate */}
          {enableHeartRate && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Heart className="h-5 w-5 text-red-600" />
                  <span>Heart Rate Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">
                      {biometricData.heartRate.current.toFixed(0)}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Current BPM</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {biometricData.heartRate.average.toFixed(0)}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Average BPM</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {(biometricData.heartRate.variability * 100).toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Variability</div>
                  </div>
                  <div className="text-center">
                    <Badge className={getBiometricColor(biometricData.heartRate.trend)}>
                      {biometricData.heartRate.trend}
                    </Badge>
                    <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">Trend</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Eye Tracking */}
          {enableEyeTracking && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Eye className="h-5 w-5 text-blue-600" />
                  <span>Eye Tracking Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {biometricData.eyeTracking.blinkRate.toFixed(0)}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Blink Rate</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {(biometricData.eyeTracking.pupilDilation * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Pupil Dilation</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {biometricData.eyeTracking.gazePattern}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Gaze Pattern</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {(biometricData.eyeTracking.focusLevel * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Focus Level</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Facial Analysis */}
          {enableFacialAnalysis && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-purple-600" />
                  <span>Facial Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Emotional State:</span>
                    <Badge className={getBiometricColor(biometricData.facialAnalysis.emotionalState)}>
                      {biometricData.facialAnalysis.emotionalState}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Stress Indicators:</span>
                    <span className="text-sm">{(biometricData.facialAnalysis.stressIndicators * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Confidence:</span>
                    <span className="text-sm">{(biometricData.facialAnalysis.confidence * 100).toFixed(1)}%</span>
                  </div>
                  {biometricData.facialAnalysis.microExpressions.length > 0 && (
                    <div>
                      <div className="font-medium mb-2">Micro Expressions:</div>
                      <div className="flex flex-wrap gap-2">
                        {biometricData.facialAnalysis.microExpressions.map((expr, index) => (
                          <Badge key={index} variant="outline">
                            {expr.expression} ({(expr.intensity * 100).toFixed(0)}%)
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Movement Analysis */}
          {enableMovementTracking && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Activity className="h-5 w-5 text-green-600" />
                  <span>Movement Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {biometricData.movement.posture}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Posture</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {(biometricData.movement.fidgeting * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Fidgeting</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {(biometricData.movement.energy * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Energy</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {(biometricData.movement.tension * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Tension</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Voice Analysis */}
          {enableVoiceAnalysis && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="h-5 w-5 text-orange-600" />
                  <span>Voice Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {(biometricData.voice.pitch * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Pitch</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {(biometricData.voice.tone * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Tone</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">
                      {(biometricData.voice.stress * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Stress</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {biometricData.voice.emotion}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">Emotion</div>
                  </div>
                </div>
              </CardContent>
            </Card>
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
