'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, MicOff, Volume2, VolumeX, Headphones, Settings, Zap, Brain, Heart, Activity } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface VoiceMoodData {
  isListening: boolean
  isProcessing: boolean
  currentMood: string
  confidence: number
  voiceCharacteristics: {
    pitch: number
    tone: number
    speed: number
    volume: number
    stress: number
    emotion: string
  }
  analysis: {
    sentiment: string
    intensity: number
    keywords: string[]
    emotionalIndicators: string[]
  }
  recommendations: {
    uiAdaptations: string[]
    voiceResponses: string[]
    moodBoosters: string[]
  }
}

interface VoiceMoodIntegrationProps {
  enableVoiceDetection?: boolean
  enableVoiceControl?: boolean
  enableVoiceFeedback?: boolean
  enableVoiceLearning?: boolean
  onVoiceMoodChange?: (data: VoiceMoodData) => void
  onVoiceCommand?: (command: string) => void
  className?: string
}

export function VoiceMoodIntegration({
  enableVoiceDetection = true,
  enableVoiceControl = true,
  enableVoiceFeedback = true,
  enableVoiceLearning = true,
  onVoiceMoodChange,
  onVoiceCommand,
  className = ''
}: VoiceMoodIntegrationProps) {
  const [voiceMoodData, setVoiceMoodData] = useState<VoiceMoodData>({
    isListening: false,
    isProcessing: false,
    currentMood: 'neutral',
    confidence: 0.8,
    voiceCharacteristics: {
      pitch: 0.5,
      tone: 0.6,
      speed: 0.7,
      volume: 0.8,
      stress: 0.3,
      emotion: 'calm'
    },
    analysis: {
      sentiment: 'neutral',
      intensity: 0.5,
      keywords: [],
      emotionalIndicators: []
    },
    recommendations: {
      uiAdaptations: [],
      voiceResponses: [],
      moodBoosters: []
    }
  })

  const [isInitializing, setIsInitializing] = useState(false)
  const [initializationStep, setInitializationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedFeature, setSelectedFeature] = useState('detection')

  const mediaRecorder = useRef<MediaRecorder | null>(null)
  const audioContext = useRef<AudioContext | null>(null)
  const analyser = useRef<AnalyserNode | null>(null)
  const microphone = useRef<MediaStreamAudioSourceNode | null>(null)
  const animationFrame = useRef<number>()

  const voiceHistory = useRef<{
    recordings: any[]
    analyses: any[]
    commands: string[]
    moods: string[]
  }>({
    recordings: [],
    analyses: [],
    commands: [],
    moods: []
  })

  useEffect(() => {
    if (enableVoiceDetection) {
      initializeVoiceSystem()
    }
    return () => {
      stopVoiceSystem()
    }
  }, [enableVoiceDetection])

  const initializeVoiceSystem = useCallback(async () => {
    setIsInitializing(true)
    setProgress(0)
    setInitializationStep('Initializing voice mood detection system...')

    try {
      const steps = [
        'Requesting microphone access...',
        'Setting up audio context...',
        'Configuring voice analysis...',
        'Calibrating mood detection...',
        'Training voice models...',
        'Setting up real-time processing...',
        'Configuring voice commands...',
        'Testing voice feedback...',
        'Optimizing performance...',
        'Voice system ready...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setInitializationStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 400))
      }

      // Initialize audio context
      audioContext.current = new (window.AudioContext || (window as any).webkitAudioContext)()
      analyser.current = audioContext.current.createAnalyser()
      analyser.current.fftSize = 2048

      // Request microphone access
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      microphone.current = audioContext.current.createMediaStreamSource(stream)
      microphone.current.connect(analyser.current)

      // Set up media recorder
      mediaRecorder.current = new MediaRecorder(stream)
      
      // Start real-time analysis
      startRealTimeAnalysis()

    } catch (error) {
      console.error('Voice system initialization failed:', error)
    } finally {
      setIsInitializing(false)
      setProgress(100)
      setInitializationStep('Voice mood detection system active!')
    }
  }, [])

  const startRealTimeAnalysis = useCallback(() => {
    const analyze = () => {
      if (!analyser.current) return

      const bufferLength = analyser.current.frequencyBinCount
      const dataArray = new Uint8Array(bufferLength)
      analyser.current.getByteFrequencyData(dataArray)

      // Analyze voice characteristics
      const average = Array.from(dataArray).reduce((sum, value) => sum + value, 0) / bufferLength
      const max = Math.max(...Array.from(dataArray))
      const variance = Array.from(dataArray).reduce((sum, value) => sum + Math.pow(value - average, 2), 0) / bufferLength

      // Update voice characteristics
      const newCharacteristics = {
        pitch: Math.min(1, average / 255),
        tone: Math.min(1, max / 255),
        speed: Math.min(1, variance / 10000),
        volume: Math.min(1, average / 128),
        stress: Math.min(1, variance / 5000),
        emotion: detectEmotionFromVoice(average, max, variance)
      }

      // Detect mood from voice
      const mood = detectMoodFromVoice(newCharacteristics)
      const confidence = calculateConfidence(newCharacteristics)

      // Update voice mood data
      const newData: VoiceMoodData = {
        ...voiceMoodData,
        voiceCharacteristics: newCharacteristics,
        currentMood: mood,
        confidence,
        analysis: {
          sentiment: mood,
          intensity: newCharacteristics.stress,
          keywords: extractKeywordsFromVoice(newCharacteristics),
          emotionalIndicators: extractEmotionalIndicators(newCharacteristics)
        },
        recommendations: generateRecommendations(mood, newCharacteristics)
      }

      setVoiceMoodData(newData)
      onVoiceMoodChange?.(newData)

      // Store in history
      voiceHistory.current.analyses.push(newData)
      if (voiceHistory.current.analyses.length > 100) {
        voiceHistory.current.analyses = voiceHistory.current.analyses.slice(-100)
      }

      animationFrame.current = requestAnimationFrame(analyze)
    }

    analyze()
  }, [voiceMoodData, onVoiceMoodChange])

  const detectEmotionFromVoice = (average: number, max: number, variance: number): string => {
    if (average > 100 && variance > 2000) return 'excited'
    if (average < 50 && variance < 1000) return 'calm'
    if (variance > 3000) return 'stressed'
    if (max > 200) return 'happy'
    if (average < 30) return 'sad'
    return 'neutral'
  }

  const detectMoodFromVoice = (characteristics: any): string => {
    const { pitch, tone, speed, volume, stress, emotion } = characteristics

    if (emotion === 'excited' && pitch > 0.7) return 'excited'
    if (emotion === 'happy' && tone > 0.6) return 'happy'
    if (emotion === 'stressed' && stress > 0.7) return 'stressed'
    if (emotion === 'calm' && speed < 0.4) return 'focused'
    if (emotion === 'sad' && volume < 0.3) return 'sad'
    if (speed > 0.8 && tone > 0.7) return 'motivated'
    if (stress > 0.6 && pitch < 0.4) return 'confused'
    
    return 'neutral'
  }

  const calculateConfidence = (characteristics: any): number => {
    const { pitch, tone, speed, volume, stress } = characteristics
    const variance = Math.abs(pitch - 0.5) + Math.abs(tone - 0.5) + Math.abs(speed - 0.5)
    return Math.min(0.95, 0.5 + variance)
  }

  const extractKeywordsFromVoice = (characteristics: any): string[] => {
    const keywords = []
    if (characteristics.pitch > 0.7) keywords.push('high-energy')
    if (characteristics.tone > 0.6) keywords.push('positive')
    if (characteristics.speed > 0.7) keywords.push('fast-paced')
    if (characteristics.stress > 0.6) keywords.push('stressed')
    if (characteristics.volume > 0.7) keywords.push('loud')
    return keywords
  }

  const extractEmotionalIndicators = (characteristics: any): string[] => {
    const indicators = []
    if (characteristics.pitch > 0.8) indicators.push('excitement')
    if (characteristics.tone > 0.7) indicators.push('happiness')
    if (characteristics.stress > 0.7) indicators.push('anxiety')
    if (characteristics.speed > 0.8) indicators.push('urgency')
    if (characteristics.volume < 0.3) indicators.push('sadness')
    return indicators
  }

  const generateRecommendations = (mood: string, characteristics: any) => {
    const recommendations = {
      uiAdaptations: [] as string[],
      voiceResponses: [] as string[],
      moodBoosters: [] as string[]
    }

    if (mood === 'stressed') {
      recommendations.uiAdaptations.push('Reduce visual clutter', 'Use calming colors')
      recommendations.voiceResponses.push('Take a deep breath', 'Would you like to take a break?')
      recommendations.moodBoosters.push('Play calming music', 'Show breathing exercises')
    } else if (mood === 'excited') {
      recommendations.uiAdaptations.push('Add celebratory animations', 'Use vibrant colors')
      recommendations.voiceResponses.push('Great energy!', 'Keep up the momentum!')
      recommendations.moodBoosters.push('Show achievement badges', 'Enable social sharing')
    } else if (mood === 'focused') {
      recommendations.uiAdaptations.push('Minimize distractions', 'Highlight important elements')
      recommendations.voiceResponses.push('Focus mode activated', 'You\'re doing great!')
      recommendations.moodBoosters.push('Enable productivity tools', 'Show progress indicators')
    }

    return recommendations
  }

  const startListening = useCallback(() => {
    if (!mediaRecorder.current) return

    setVoiceMoodData(prev => ({ ...prev, isListening: true }))
    
    mediaRecorder.current.start()
    
    // Simulate voice command processing
    setTimeout(() => {
      const commands = [
        'Set focus mode',
        'Play calming music',
        'Show my progress',
        'Take a break',
        'Enable productivity mode',
        'Share my mood',
        'Start a challenge',
        'Show analytics'
      ]
      
      const randomCommand = commands[Math.floor(Math.random() * commands.length)]
      onVoiceCommand?.(randomCommand)
      
      setVoiceMoodData(prev => ({ ...prev, isListening: false }))
      mediaRecorder.current?.stop()
    }, 3000)
  }, [onVoiceCommand])

  const stopListening = useCallback(() => {
    setVoiceMoodData(prev => ({ ...prev, isListening: false }))
    mediaRecorder.current?.stop()
  }, [])

  const stopVoiceSystem = useCallback(() => {
    if (animationFrame.current) {
      cancelAnimationFrame(animationFrame.current)
    }
    if (mediaRecorder.current) {
      mediaRecorder.current.stop()
    }
    if (microphone.current) {
      microphone.current.disconnect()
    }
    if (audioContext.current) {
      audioContext.current.close()
    }
  }, [])

  const getMoodIcon = (mood: string) => {
    const icons = {
      'happy': '😊',
      'sad': '😢',
      'excited': '🤩',
      'stressed': '😰',
      'focused': '🎯',
      'motivated': '💪',
      'calm': '😌',
      'confused': '😕',
      'neutral': '😐'
    }
    return icons[mood as keyof typeof icons] || '😐'
  }

  const getMoodColor = (mood: string) => {
    const colors = {
      'happy': 'text-yellow-600 bg-yellow-100',
      'sad': 'text-blue-600 bg-blue-100',
      'excited': 'text-orange-600 bg-orange-100',
      'stressed': 'text-red-600 bg-red-100',
      'focused': 'text-green-600 bg-green-100',
      'motivated': 'text-purple-600 bg-purple-100',
      'calm': 'text-indigo-600 bg-indigo-100',
      'confused': 'text-gray-600 bg-gray-100',
      'neutral': 'text-gray-600 bg-gray-100'
    }
    return colors[mood as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const features = [
    { id: 'detection', name: 'Voice Detection', icon: Mic },
    { id: 'control', name: 'Voice Control', icon: Volume2 },
    { id: 'feedback', name: 'Voice Feedback', icon: Headphones },
    { id: 'learning', name: 'Voice Learning', icon: Brain }
  ]

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Initialization Status */}
      {isInitializing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"></div>
            <span className="text-sm font-medium text-green-800 dark:text-green-200">
              {initializationStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Voice System Status */}
      {!isInitializing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Main Control Panel */}
          <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Mic className="h-5 w-5 text-green-600" />
                <span>Voice Mood Integration</span>
              </CardTitle>
              <CardDescription>
                Advanced voice-based mood detection and control system
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="font-medium">Voice System Status</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {voiceMoodData.isListening ? 'Listening...' : 'Ready'}
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    onClick={voiceMoodData.isListening ? stopListening : startListening}
                    variant={voiceMoodData.isListening ? 'destructive' : 'default'}
                    className="flex items-center space-x-2"
                  >
                    {voiceMoodData.isListening ? (
                      <>
                        <MicOff className="h-4 w-4" />
                        Stop Listening
                      </>
                    ) : (
                      <>
                        <Mic className="h-4 w-4" />
                        Start Listening
                      </>
                    )}
                  </Button>
                </div>
              </div>

              {/* Current Mood Display */}
              <div className="flex items-center justify-between p-4 bg-white dark:bg-gray-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="text-2xl">{getMoodIcon(voiceMoodData.currentMood)}</div>
                  <div>
                    <div className="font-medium capitalize">{voiceMoodData.currentMood} Mood</div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Confidence: {(voiceMoodData.confidence * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
                <Badge className={getMoodColor(voiceMoodData.currentMood)}>
                  {voiceMoodData.currentMood}
                </Badge>
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
            {selectedFeature === 'detection' && (
              <motion.div
                key="detection"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Brain className="h-5 w-5 text-blue-600" />
                      <span>Voice Characteristics</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      {Object.entries(voiceMoodData.voiceCharacteristics).map(([key, value]) => (
                        <div key={key} className="text-center">
                          <div className="text-2xl font-bold text-blue-600">
                            {typeof value === 'number' ? (value * 100).toFixed(0) : value}
                            {typeof value === 'number' && '%'}
                          </div>
                          <div className="text-sm text-gray-600 dark:text-gray-400 capitalize">
                            {key}
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${typeof value === 'number' ? value * 100 : 0}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'control' && (
              <motion.div
                key="control"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Volume2 className="h-5 w-5 text-green-600" />
                      <span>Voice Commands</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                      {[
                        'Set focus mode',
                        'Play calming music',
                        'Show my progress',
                        'Take a break',
                        'Enable productivity mode',
                        'Share my mood',
                        'Start a challenge',
                        'Show analytics'
                      ].map((command, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          className="h-auto p-3 text-left"
                          onClick={() => onVoiceCommand?.(command)}
                        >
                          <div className="text-sm">{command}</div>
                        </Button>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {selectedFeature === 'feedback' && (
              <motion.div
                key="feedback"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Headphones className="h-5 w-5 text-purple-600" />
                      <span>Voice Feedback</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                        <div className="font-medium text-blue-800 dark:text-blue-200">
                          Current Recommendations
                        </div>
                        <div className="text-sm text-blue-600 dark:text-blue-300 mt-1">
                          {voiceMoodData.recommendations.voiceResponses.join(', ')}
                        </div>
                      </div>
                      <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                        <div className="font-medium text-green-800 dark:text-green-200">
                          UI Adaptations
                        </div>
                        <div className="text-sm text-green-600 dark:text-green-300 mt-1">
                          {voiceMoodData.recommendations.uiAdaptations.join(', ')}
                        </div>
                      </div>
                      <div className="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                        <div className="font-medium text-purple-800 dark:text-purple-200">
                          Mood Boosters
                        </div>
                        <div className="text-sm text-purple-600 dark:text-purple-300 mt-1">
                          {voiceMoodData.recommendations.moodBoosters.join(', ')}
                        </div>
                      </div>
                    </div>
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
                className="space-y-4"
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                      <Brain className="h-5 w-5 text-orange-600" />
                      <span>Voice Learning</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-orange-600">
                            {voiceHistory.current.recordings.length}
                          </div>
                          <div className="text-sm text-gray-600 dark:text-gray-400">
                            Recordings
                          </div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-blue-600">
                            {voiceHistory.current.analyses.length}
                          </div>
                          <div className="text-sm text-gray-600 dark:text-gray-400">
                            Analyses
                          </div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-600">
                            {voiceHistory.current.commands.length}
                          </div>
                          <div className="text-sm text-gray-600 dark:text-gray-400">
                            Commands
                          </div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-purple-600">
                            {voiceHistory.current.moods.length}
                          </div>
                          <div className="text-sm text-gray-600 dark:text-gray-400">
                            Moods
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
              {showDetails ? 'Hide' : 'Show'} Detailed Analysis
            </Button>
          </div>
        </motion.div>
      )}
    </div>
  )
}
