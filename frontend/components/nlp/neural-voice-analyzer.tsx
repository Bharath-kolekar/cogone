'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Waveform, Mic, Volume2, TrendingUp, Target, Zap, Eye, BarChart3, Activity } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface VoiceAnalysisResult {
  audio: {
    duration: number
    sampleRate: number
    channels: number
    bitRate: number
    format: string
  }
  speech: {
    speakingRate: number
    pauseFrequency: number
    averagePauseLength: number
    speechClarity: number
    volumeLevel: number
    pitchRange: number
  }
  linguistic: {
    wordCount: number
    sentenceCount: number
    averageWordsPerSentence: number
    vocabularyRichness: number
    repetitionRate: number
    fillerWords: number
  }
  emotional: {
    stressLevel: number
    confidence: number
    engagement: number
    energy: number
    calmness: number
  }
  cognitive: {
    complexity: number
    coherence: number
    fluency: number
    organization: number
    focus: number
  }
  patterns: {
    speakingStyle: string
    communicationType: string
    personalityTraits: string[]
    strengths: string[]
    improvements: string[]
  }
  insights: {
    summary: string
    recommendations: string[]
    keyFindings: string[]
  }
}

interface NeuralVoiceAnalyzerProps {
  audioData?: Blob
  transcript?: string
  onAnalysisComplete?: (result: VoiceAnalysisResult) => void
  showVisualizations?: boolean
  enableRealTime?: boolean
  className?: string
}

export function NeuralVoiceAnalyzer({
  audioData,
  transcript,
  onAnalysisComplete,
  showVisualizations = true,
  enableRealTime = true,
  className = ''
}: NeuralVoiceAnalyzerProps) {
  const [analysis, setAnalysis] = useState<VoiceAnalysisResult | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const analysisRef = useRef<VoiceAnalysisResult | null>(null)

  useEffect(() => {
    if (audioData || transcript) {
      analyzeVoice(audioData, transcript)
    }
  }, [audioData, transcript])

  const analyzeVoice = async (audio?: Blob, text?: string) => {
    setIsAnalyzing(true)
    setProgress(0)
    setAnalysisStep('Initializing neural voice analysis...')

    try {
      // Simulate real-time analysis steps
      const steps = [
        'Analyzing audio characteristics...',
        'Processing speech patterns...',
        'Detecting linguistic features...',
        'Analyzing emotional indicators...',
        'Evaluating cognitive patterns...',
        'Identifying communication style...',
        'Generating personality insights...',
        'Creating recommendations...',
        'Compiling comprehensive report...',
        'Finalizing analysis...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setAnalysisStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 400))
      }

      // Perform voice analysis
      const result = await performVoiceAnalysis(audio, text)
      
      setAnalysis(result)
      analysisRef.current = result
      onAnalysisComplete?.(result)
      
    } catch (error) {
      console.error('Voice analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
      setProgress(100)
      setAnalysisStep('Analysis complete!')
    }
  }

  const performVoiceAnalysis = async (audio?: Blob, text?: string): Promise<VoiceAnalysisResult> => {
    // Simulate advanced voice analysis
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Mock audio analysis
    const audioAnalysis = {
      duration: 45.2 + Math.random() * 20,
      sampleRate: 44100,
      channels: 1,
      bitRate: 128000,
      format: 'WebM'
    }

    // Mock speech analysis
    const speechAnalysis = {
      speakingRate: 120 + Math.random() * 40, // words per minute
      pauseFrequency: 0.3 + Math.random() * 0.4, // pauses per minute
      averagePauseLength: 0.5 + Math.random() * 1.0, // seconds
      speechClarity: 0.7 + Math.random() * 0.3,
      volumeLevel: 0.6 + Math.random() * 0.4,
      pitchRange: 0.4 + Math.random() * 0.3
    }

    // Mock linguistic analysis
    const wordCount = text ? text.split(/\s+/).length : 150 + Math.floor(Math.random() * 100)
    const sentenceCount = text ? text.split(/[.!?]+/).length : 8 + Math.floor(Math.random() * 12)
    
    const linguisticAnalysis = {
      wordCount,
      sentenceCount,
      averageWordsPerSentence: wordCount / sentenceCount,
      vocabularyRichness: 0.6 + Math.random() * 0.3,
      repetitionRate: 0.1 + Math.random() * 0.2,
      fillerWords: Math.floor(Math.random() * 10)
    }

    // Mock emotional analysis
    const emotionalAnalysis = {
      stressLevel: Math.random(),
      confidence: 0.5 + Math.random() * 0.5,
      engagement: 0.4 + Math.random() * 0.6,
      energy: 0.3 + Math.random() * 0.7,
      calmness: 0.2 + Math.random() * 0.8
    }

    // Mock cognitive analysis
    const cognitiveAnalysis = {
      complexity: 0.4 + Math.random() * 0.6,
      coherence: 0.5 + Math.random() * 0.5,
      fluency: 0.6 + Math.random() * 0.4,
      organization: 0.4 + Math.random() * 0.6,
      focus: 0.5 + Math.random() * 0.5
    }

    // Mock pattern analysis
    const speakingStyles = ['conversational', 'formal', 'persuasive', 'explanatory', 'narrative']
    const communicationTypes = ['direct', 'indirect', 'analytical', 'emotional', 'collaborative']
    const personalityTraits = ['confident', 'analytical', 'empathetic', 'assertive', 'creative']
    const strengths = ['clear communication', 'good pacing', 'engaging tone', 'logical structure']
    const improvements = ['reduce filler words', 'improve clarity', 'enhance engagement', 'better organization']

    const patternAnalysis = {
      speakingStyle: speakingStyles[Math.floor(Math.random() * speakingStyles.length)],
      communicationType: communicationTypes[Math.floor(Math.random() * communicationTypes.length)],
      personalityTraits: personalityTraits.slice(0, 2 + Math.floor(Math.random() * 3)),
      strengths: strengths.slice(0, 2 + Math.floor(Math.random() * 2)),
      improvements: improvements.slice(0, 2 + Math.floor(Math.random() * 2))
    }

    // Generate insights
    const insights = {
      summary: `This ${audioAnalysis.duration.toFixed(1)}-second recording shows ${patternAnalysis.speakingStyle} speaking style with ${linguisticAnalysis.wordCount} words spoken at ${speechAnalysis.speakingRate.toFixed(0)} words per minute. The speaker demonstrates ${emotionalAnalysis.confidence > 0.7 ? 'high' : 'moderate'} confidence and ${cognitiveAnalysis.coherence > 0.7 ? 'strong' : 'adequate'} coherence.`,
      recommendations: [
        'Practice speaking at a consistent pace',
        'Work on reducing filler words',
        'Enhance vocal variety and expression',
        'Improve pause timing for better clarity'
      ],
      keyFindings: [
        `Speaking rate of ${speechAnalysis.speakingRate.toFixed(0)} WPM is ${speechAnalysis.speakingRate > 150 ? 'fast' : speechAnalysis.speakingRate < 100 ? 'slow' : 'optimal'}`,
        `Speech clarity score of ${(speechAnalysis.speechClarity * 100).toFixed(0)}% indicates ${speechAnalysis.speechClarity > 0.8 ? 'excellent' : speechAnalysis.speechClarity > 0.6 ? 'good' : 'needs improvement'} clarity`,
        `Confidence level of ${(emotionalAnalysis.confidence * 100).toFixed(0)}% shows ${emotionalAnalysis.confidence > 0.7 ? 'strong' : 'moderate'} confidence`
      ]
    }

    return {
      audio: audioAnalysis,
      speech: speechAnalysis,
      linguistic: linguisticAnalysis,
      emotional: emotionalAnalysis,
      cognitive: cognitiveAnalysis,
      patterns: patternAnalysis,
      insights
    }
  }

  const getScoreColor = (score: number) => {
    if (score > 0.8) return 'text-green-600 bg-green-100'
    if (score > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getScoreIcon = (score: number) => {
    if (score > 0.8) return '🟢'
    if (score > 0.6) return '🟡'
    return '🔴'
  }

  const getCategoryIcon = (category: string) => {
    const icons = {
      'audio': Waveform,
      'speech': Mic,
      'linguistic': Brain,
      'emotional': Eye,
      'cognitive': Target,
      'patterns': BarChart3
    }
    return icons[category as keyof typeof icons] || Activity
  }

  const categories = [
    { id: 'audio', name: 'Audio Quality', icon: Waveform },
    { id: 'speech', name: 'Speech Patterns', icon: Mic },
    { id: 'linguistic', name: 'Linguistic Analysis', icon: Brain },
    { id: 'emotional', name: 'Emotional Indicators', icon: Eye },
    { id: 'cognitive', name: 'Cognitive Patterns', icon: Target },
    { id: 'patterns', name: 'Communication Patterns', icon: BarChart3 }
  ]

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Analysis Status */}
      {isAnalyzing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
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

      {/* Analysis Results */}
      {analysis && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Summary */}
          <Card className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-purple-600" />
                <span>Neural Voice Analysis Summary</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                {analysis.insights.summary}
              </p>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {analysis.linguistic.wordCount}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Words</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {analysis.speech.speakingRate.toFixed(0)}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">WPM</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {(analysis.speech.speechClarity * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Clarity</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {analysis.audio.duration.toFixed(1)}s
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Duration</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Category Navigation */}
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => {
              const Icon = category.icon
              return (
                <Button
                  key={category.id}
                  variant={selectedCategory === category.id ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedCategory(selectedCategory === category.id ? null : category.id)}
                  className="flex items-center space-x-2"
                >
                  <Icon className="h-4 w-4" />
                  <span>{category.name}</span>
                </Button>
              )
            })}
          </div>

          {/* Detailed Analysis */}
          {selectedCategory && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              {/* Audio Quality */}
              {selectedCategory === 'audio' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm flex items-center space-x-2">
                        <Waveform className="h-4 w-4" />
                        <span>Audio Specifications</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Duration</span>
                          <span className="font-medium">{analysis.audio.duration.toFixed(1)}s</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Sample Rate</span>
                          <span className="font-medium">{analysis.audio.sampleRate} Hz</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Channels</span>
                          <span className="font-medium">{analysis.audio.channels}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Bit Rate</span>
                          <span className="font-medium">{analysis.audio.bitRate} bps</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Format</span>
                          <span className="font-medium">{analysis.audio.format}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm flex items-center space-x-2">
                        <Volume2 className="h-4 w-4" />
                        <span>Audio Quality</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600 dark:text-gray-400">Volume Level</span>
                          <Badge className={getScoreColor(analysis.speech.volumeLevel)}>
                            {(analysis.speech.volumeLevel * 100).toFixed(0)}%
                          </Badge>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full"
                            style={{ width: `${analysis.speech.volumeLevel * 100}%` }}
                          />
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Speech Patterns */}
              {selectedCategory === 'speech' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm flex items-center space-x-2">
                        <Mic className="h-4 w-4" />
                        <span>Speaking Rate</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-3xl font-bold text-blue-600 mb-2">
                          {analysis.speech.speakingRate.toFixed(0)}
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Words per minute</div>
                        <div className="mt-2">
                          <Badge variant="outline">
                            {analysis.speech.speakingRate > 150 ? 'Fast' : 
                             analysis.speech.speakingRate < 100 ? 'Slow' : 'Optimal'}
                          </Badge>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm flex items-center space-x-2">
                        <Target className="h-4 w-4" />
                        <span>Speech Clarity</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-3xl font-bold text-green-600 mb-2">
                          {(analysis.speech.speechClarity * 100).toFixed(0)}%
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Clarity score</div>
                        <div className="mt-2">
                          <Badge className={getScoreColor(analysis.speech.speechClarity)}>
                            {analysis.speech.speechClarity > 0.8 ? 'Excellent' : 
                             analysis.speech.speechClarity > 0.6 ? 'Good' : 'Needs Improvement'}
                          </Badge>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Linguistic Analysis */}
              {selectedCategory === 'linguistic' && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Vocabulary Richness</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">
                          {(analysis.linguistic.vocabularyRichness * 100).toFixed(0)}%
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                          <div 
                            className="bg-purple-500 h-2 rounded-full"
                            style={{ width: `${analysis.linguistic.vocabularyRichness * 100}%` }}
                          />
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Repetition Rate</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-orange-600">
                          {(analysis.linguistic.repetitionRate * 100).toFixed(0)}%
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                          <div 
                            className="bg-orange-500 h-2 rounded-full"
                            style={{ width: `${analysis.linguistic.repetitionRate * 100}%` }}
                          />
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Filler Words</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-red-600">
                          {analysis.linguistic.fillerWords}
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">Count</div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Emotional Indicators */}
              {selectedCategory === 'emotional' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(analysis.emotional).map(([key, value]) => (
                    <Card key={key}>
                      <CardHeader>
                        <CardTitle className="text-sm capitalize">{key.replace(/([A-Z])/g, ' $1')}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-blue-600 mb-2">
                            {(value * 100).toFixed(0)}%
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${value * 100}%` }}
                            />
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}

              {/* Cognitive Patterns */}
              {selectedCategory === 'cognitive' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(analysis.cognitive).map(([key, value]) => (
                    <Card key={key}>
                      <CardHeader>
                        <CardTitle className="text-sm capitalize">{key.replace(/([A-Z])/g, ' $1')}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-600 mb-2">
                            {(value * 100).toFixed(0)}%
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-green-500 h-2 rounded-full"
                              style={{ width: `${value * 100}%` }}
                            />
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}

              {/* Communication Patterns */}
              {selectedCategory === 'patterns' && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-sm">Speaking Style</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <Badge variant="outline" className="text-lg">
                          {analysis.patterns.speakingStyle}
                        </Badge>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardHeader>
                        <CardTitle className="text-sm">Communication Type</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <Badge variant="outline" className="text-lg">
                          {analysis.patterns.communicationType}
                        </Badge>
                      </CardContent>
                    </Card>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card>
                      <CardHeader>
                        <CardTitle className="text-sm">Personality Traits</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="flex flex-wrap gap-2">
                          {analysis.patterns.personalityTraits.map((trait, index) => (
                            <Badge key={index} variant="secondary">
                              {trait}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>

                    <Card>
                      <CardHeader>
                        <CardTitle className="text-sm">Strengths</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="flex flex-wrap gap-2">
                          {analysis.patterns.strengths.map((strength, index) => (
                            <Badge key={index} className="text-green-600 bg-green-100">
                              {strength}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  <Card>
                    <CardHeader>
                      <CardTitle className="text-sm">Areas for Improvement</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap gap-2">
                        {analysis.patterns.improvements.map((improvement, index) => (
                          <Badge key={index} className="text-yellow-600 bg-yellow-100">
                            {improvement}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}
            </motion.div>
          )}

          {/* Key Findings and Recommendations */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Key Findings</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {analysis.insights.keyFindings.map((finding, index) => (
                    <li key={index} className="flex items-start space-x-2 text-sm">
                      <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                      <span>{finding}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Recommendations</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {analysis.insights.recommendations.map((recommendation, index) => (
                    <li key={index} className="flex items-start space-x-2 text-sm">
                      <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                      <span>{recommendation}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>

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
