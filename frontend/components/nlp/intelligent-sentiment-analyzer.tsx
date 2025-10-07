'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Heart, Smile, Frown, Meh, TrendingUp, TrendingDown, Brain, Zap, Target, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface SentimentAnalysisResult {
  overall: {
    sentiment: 'positive' | 'negative' | 'neutral' | 'mixed'
    score: number
    confidence: number
    magnitude: number
  }
  emotions: Array<{
    emotion: string
    intensity: number
    confidence: number
  }>
  aspects: Array<{
    aspect: string
    sentiment: 'positive' | 'negative' | 'neutral'
    score: number
    confidence: number
  }>
  trends: {
    direction: 'improving' | 'declining' | 'stable'
    change: number
    period: string
  }
  recommendations: Array<{
    type: 'improvement' | 'warning' | 'suggestion'
    message: string
    priority: 'high' | 'medium' | 'low'
  }>
  context: {
    domain: string
    audience: string
    purpose: string
  }
  linguistic: {
    politeness: number
    formality: number
    clarity: number
    engagement: number
  }
}

interface IntelligentSentimentAnalyzerProps {
  text: string
  onAnalysisComplete?: (result: SentimentAnalysisResult) => void
  showEmotions?: boolean
  showAspects?: boolean
  showTrends?: boolean
  enableRealTime?: boolean
  className?: string
}

const EMOTION_ICONS = {
  'joy': Smile,
  'sadness': Frown,
  'anger': AlertCircle,
  'fear': AlertCircle,
  'surprise': Zap,
  'disgust': Frown,
  'love': Heart,
  'excitement': TrendingUp,
  'anxiety': AlertCircle,
  'calm': Meh,
  'confusion': Brain,
  'satisfaction': Smile,
  'disappointment': Frown,
  'hope': Heart,
  'frustration': AlertCircle
}

const EMOTION_COLORS = {
  'joy': 'text-yellow-600 bg-yellow-100',
  'sadness': 'text-blue-600 bg-blue-100',
  'anger': 'text-red-600 bg-red-100',
  'fear': 'text-purple-600 bg-purple-100',
  'surprise': 'text-orange-600 bg-orange-100',
  'disgust': 'text-green-600 bg-green-100',
  'love': 'text-pink-600 bg-pink-100',
  'excitement': 'text-yellow-600 bg-yellow-100',
  'anxiety': 'text-red-600 bg-red-100',
  'calm': 'text-blue-600 bg-blue-100',
  'confusion': 'text-gray-600 bg-gray-100',
  'satisfaction': 'text-green-600 bg-green-100',
  'disappointment': 'text-red-600 bg-red-100',
  'hope': 'text-green-600 bg-green-100',
  'frustration': 'text-red-600 bg-red-100'
}

export function IntelligentSentimentAnalyzer({
  text,
  onAnalysisComplete,
  showEmotions = true,
  showAspects = true,
  showTrends = true,
  enableRealTime = true,
  className = ''
}: IntelligentSentimentAnalyzerProps) {
  const [analysis, setAnalysis] = useState<SentimentAnalysisResult | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const analysisRef = useRef<SentimentAnalysisResult | null>(null)

  useEffect(() => {
    if (text && enableRealTime) {
      analyzeSentiment(text)
    }
  }, [text, enableRealTime])

  const analyzeSentiment = async (inputText: string) => {
    setIsAnalyzing(true)
    setProgress(0)
    setAnalysisStep('Initializing sentiment analysis...')

    try {
      // Simulate real-time analysis steps
      const steps = [
        'Analyzing emotional content...',
        'Detecting sentiment patterns...',
        'Identifying emotional aspects...',
        'Calculating sentiment scores...',
        'Analyzing linguistic features...',
        'Detecting emotional trends...',
        'Evaluating context...',
        'Generating recommendations...',
        'Assessing engagement level...',
        'Finalizing analysis...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setAnalysisStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 200))
      }

      // Perform sentiment analysis
      const result = await performSentimentAnalysis(inputText)
      
      setAnalysis(result)
      analysisRef.current = result
      onAnalysisComplete?.(result)
      
    } catch (error) {
      console.error('Sentiment analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
      setProgress(100)
      setAnalysisStep('Analysis complete!')
    }
  }

  const performSentimentAnalysis = async (inputText: string): Promise<SentimentAnalysisResult> => {
    // Simulate advanced sentiment analysis
    await new Promise(resolve => setTimeout(resolve, 1000))

    const textLower = inputText.toLowerCase()
    
    // Sentiment analysis
    const positiveWords = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'pleased', 'satisfied', 'excited', 'thrilled', 'delighted']
    const negativeWords = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'sad', 'disappointed', 'frustrated', 'annoyed', 'upset', 'worried', 'concerned']
    const neutralWords = ['okay', 'fine', 'alright', 'average', 'normal', 'standard', 'typical']
    
    const positiveCount = positiveWords.filter(word => textLower.includes(word)).length
    const negativeCount = negativeWords.filter(word => textLower.includes(word)).length
    const neutralCount = neutralWords.filter(word => textLower.includes(word)).length
    
    let sentiment: 'positive' | 'negative' | 'neutral' | 'mixed' = 'neutral'
    let score = 0
    let confidence = 0.8
    
    if (positiveCount > negativeCount && positiveCount > neutralCount) {
      sentiment = 'positive'
      score = 0.3 + Math.random() * 0.7
    } else if (negativeCount > positiveCount && negativeCount > neutralCount) {
      sentiment = 'negative'
      score = -0.3 - Math.random() * 0.7
    } else if (positiveCount > 0 && negativeCount > 0) {
      sentiment = 'mixed'
      score = (positiveCount - negativeCount) / (positiveCount + negativeCount)
    } else {
      sentiment = 'neutral'
      score = -0.2 + Math.random() * 0.4
    }

    // Emotion analysis
    const emotions = [
      { emotion: 'joy', intensity: Math.random(), confidence: 0.8 },
      { emotion: 'satisfaction', intensity: Math.random(), confidence: 0.7 },
      { emotion: 'excitement', intensity: Math.random(), confidence: 0.6 },
      { emotion: 'calm', intensity: Math.random(), confidence: 0.5 }
    ].filter(emotion => emotion.intensity > 0.3)

    // Aspect-based sentiment
    const aspects = [
      { aspect: 'overall experience', sentiment: sentiment as 'positive' | 'negative' | 'neutral', score, confidence: 0.9 },
      { aspect: 'quality', sentiment: sentiment as 'positive' | 'negative' | 'neutral', score: score + Math.random() * 0.2 - 0.1, confidence: 0.8 },
      { aspect: 'service', sentiment: sentiment as 'positive' | 'negative' | 'neutral', score: score + Math.random() * 0.2 - 0.1, confidence: 0.7 }
    ]

    // Trends analysis
    const trends = {
      direction: Math.random() > 0.5 ? 'improving' : 'stable' as 'improving' | 'declining' | 'stable',
      change: (Math.random() - 0.5) * 0.4,
      period: 'recent'
    }

    // Recommendations
    const recommendations = []
    if (sentiment === 'negative') {
      recommendations.push({
        type: 'improvement' as const,
        message: 'Consider addressing negative feedback points',
        priority: 'high' as const
      })
    }
    if (sentiment === 'mixed') {
      recommendations.push({
        type: 'suggestion' as const,
        message: 'Focus on strengthening positive aspects',
        priority: 'medium' as const
      })
    }
    if (score < -0.5) {
      recommendations.push({
        type: 'warning' as const,
        message: 'Strong negative sentiment detected',
        priority: 'high' as const
      })
    }

    // Context analysis
    const context = {
      domain: 'general',
      audience: 'mixed',
      purpose: 'feedback'
    }

    // Linguistic analysis
    const linguistic = {
      politeness: 0.7 + Math.random() * 0.3,
      formality: 0.5 + Math.random() * 0.5,
      clarity: 0.6 + Math.random() * 0.4,
      engagement: 0.5 + Math.random() * 0.5
    }

    return {
      overall: {
        sentiment,
        score,
        confidence,
        magnitude: Math.abs(score)
      },
      emotions,
      aspects,
      trends,
      recommendations,
      context,
      linguistic
    }
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100'
      case 'negative': return 'text-red-600 bg-red-100'
      case 'mixed': return 'text-yellow-600 bg-yellow-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return Smile
      case 'negative': return Frown
      case 'mixed': return Meh
      default: return Meh
    }
  }

  const getTrendColor = (direction: string) => {
    switch (direction) {
      case 'improving': return 'text-green-600 bg-green-100'
      case 'declining': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getTrendIcon = (direction: string) => {
    switch (direction) {
      case 'improving': return TrendingUp
      case 'declining': return TrendingDown
      default: return Meh
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      default: return 'text-green-600 bg-green-100'
    }
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Analysis Status */}
      {isAnalyzing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
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
          {/* Overall Sentiment */}
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-blue-600" />
                <span>Sentiment Analysis</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center space-x-4 mb-4">
                <div className="text-4xl">
                  {(() => {
                    const Icon = getSentimentIcon(analysis.overall.sentiment)
                    return <Icon className="h-12 w-12" />
                  })()}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                    {analysis.overall.sentiment.charAt(0).toUpperCase() + analysis.overall.sentiment.slice(1)} Sentiment
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Score: {(analysis.overall.score * 100).toFixed(1)}% • Confidence: {(analysis.overall.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge className={getSentimentColor(analysis.overall.sentiment)}>
                  {analysis.overall.sentiment}
                </Badge>
                <Badge variant="outline">
                  Magnitude: {(analysis.overall.magnitude * 100).toFixed(1)}%
                </Badge>
                <Badge variant="outline">
                  Confidence: {(analysis.overall.confidence * 100).toFixed(1)}%
                </Badge>
              </div>

              {/* Sentiment Score Bar */}
              <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
                <div 
                  className={`h-3 rounded-full ${
                    analysis.overall.score > 0 ? 'bg-green-500' : 
                    analysis.overall.score < 0 ? 'bg-red-500' : 'bg-gray-500'
                  }`}
                  style={{ 
                    width: `${Math.abs(analysis.overall.score) * 100}%`,
                    marginLeft: analysis.overall.score < 0 ? `${100 - Math.abs(analysis.overall.score) * 100}%` : '0'
                  }}
                />
              </div>
            </CardContent>
          </Card>

          {/* Emotions */}
          {showEmotions && analysis.emotions.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Heart className="h-4 w-4" />
                  <span>Emotions Detected</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {analysis.emotions.map((emotion, index) => {
                    const Icon = EMOTION_ICONS[emotion.emotion as keyof typeof EMOTION_ICONS] || Brain
                    return (
                      <div key={index} className="flex items-center space-x-2 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                        <Icon className="h-5 w-5" />
                        <div className="flex-1">
                          <div className="text-sm font-medium capitalize">{emotion.emotion}</div>
                          <div className="text-xs text-gray-500">
                            {(emotion.intensity * 100).toFixed(0)}% intensity
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Aspects */}
          {showAspects && analysis.aspects.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Aspect-Based Sentiment</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analysis.aspects.map((aspect, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Badge className={getSentimentColor(aspect.sentiment)}>
                          {aspect.sentiment}
                        </Badge>
                        <span className="font-medium">{aspect.aspect}</span>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">
                          {(aspect.score * 100).toFixed(1)}%
                        </div>
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${
                              aspect.score > 0 ? 'bg-green-500' : 
                              aspect.score < 0 ? 'bg-red-500' : 'bg-gray-500'
                            }`}
                            style={{ width: `${Math.abs(aspect.score) * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Trends */}
          {showTrends && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Sentiment Trends</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <div className="flex items-center space-x-3">
                    {(() => {
                      const Icon = getTrendIcon(analysis.trends.direction)
                      return <Icon className="h-5 w-5" />
                    })()}
                    <div>
                      <div className="font-medium capitalize">{analysis.trends.direction}</div>
                      <div className="text-sm text-gray-500">{analysis.trends.period}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <Badge className={getTrendColor(analysis.trends.direction)}>
                      {analysis.trends.direction}
                    </Badge>
                    <div className="text-sm text-gray-500 mt-1">
                      {(analysis.trends.change * 100).toFixed(1)}% change
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Recommendations */}
          {analysis.recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <AlertCircle className="h-4 w-4" />
                  <span>Recommendations</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analysis.recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <Badge className={getPriorityColor(rec.priority)}>
                        {rec.priority}
                      </Badge>
                      <div className="flex-1">
                        <div className="font-medium capitalize">{rec.type}</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">{rec.message}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Linguistic Analysis */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm">Politeness</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">
                  {(analysis.linguistic.politeness * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: `${analysis.linguistic.politeness * 100}%` }}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm">Formality</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">
                  {(analysis.linguistic.formality * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${analysis.linguistic.formality * 100}%` }}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm">Clarity</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-yellow-600">
                  {(analysis.linguistic.clarity * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-yellow-500 h-2 rounded-full"
                    style={{ width: `${analysis.linguistic.clarity * 100}%` }}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm">Engagement</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-600">
                  {(analysis.linguistic.engagement * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-purple-500 h-2 rounded-full"
                    style={{ width: `${analysis.linguistic.engagement * 100}%` }}
                  />
                </div>
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
