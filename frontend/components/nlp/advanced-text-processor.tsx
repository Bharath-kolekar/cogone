'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Zap, Eye, Filter, Sparkles, Target, TrendingUp, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface TextAnalysisResult {
  sentiment: {
    score: number
    label: 'positive' | 'negative' | 'neutral'
    confidence: number
  }
  entities: Array<{
    text: string
    type: string
    confidence: number
    start: number
    end: number
  }>
  keywords: Array<{
    word: string
    importance: number
    frequency: number
  }>
  topics: Array<{
    topic: string
    relevance: number
    keywords: string[]
  }>
  intent: {
    primary: string
    secondary: string[]
    confidence: number
  }
  language: {
    detected: string
    confidence: number
  }
  readability: {
    score: number
    level: string
    suggestions: string[]
  }
  emotions: Array<{
    emotion: string
    intensity: number
  }>
  summary: string
  actionItems: string[]
}

interface AdvancedTextProcessorProps {
  text: string
  onAnalysisComplete?: (result: TextAnalysisResult) => void
  showVisualization?: boolean
  enableRealTime?: boolean
  className?: string
}

export function AdvancedTextProcessor({
  text,
  onAnalysisComplete,
  showVisualization = true,
  enableRealTime = true,
  className = ''
}: AdvancedTextProcessorProps) {
  const [analysis, setAnalysis] = useState<TextAnalysisResult | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [processingStep, setProcessingStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const analysisRef = useRef<TextAnalysisResult | null>(null)

  useEffect(() => {
    if (text && enableRealTime) {
      processText(text)
    }
  }, [text, enableRealTime])

  const processText = async (inputText: string) => {
    setIsProcessing(true)
    setProgress(0)
    setProcessingStep('Initializing analysis...')

    try {
      // Simulate real-time processing steps
      const steps = [
        'Analyzing sentiment...',
        'Extracting entities...',
        'Identifying keywords...',
        'Detecting topics...',
        'Determining intent...',
        'Detecting language...',
        'Calculating readability...',
        'Analyzing emotions...',
        'Generating summary...',
        'Extracting action items...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setProcessingStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 200))
      }

      // Simulate advanced NLP analysis
      const result = await performAdvancedAnalysis(inputText)
      
      setAnalysis(result)
      analysisRef.current = result
      onAnalysisComplete?.(result)
      
    } catch (error) {
      console.error('Text processing failed:', error)
    } finally {
      setIsProcessing(false)
      setProgress(100)
      setProcessingStep('Analysis complete!')
    }
  }

  const performAdvancedAnalysis = async (inputText: string): Promise<TextAnalysisResult> => {
    // Simulate advanced NLP processing
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Mock analysis results based on text content
    const words = inputText.toLowerCase().split(/\s+/)
    const positiveWords = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy']
    const negativeWords = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'sad', 'disappointed']
    
    const positiveCount = words.filter(word => positiveWords.includes(word)).length
    const negativeCount = words.filter(word => negativeWords.includes(word)).length
    
    let sentimentScore = 0
    let sentimentLabel: 'positive' | 'negative' | 'neutral' = 'neutral'
    
    if (positiveCount > negativeCount) {
      sentimentScore = 0.7 + Math.random() * 0.3
      sentimentLabel = 'positive'
    } else if (negativeCount > positiveCount) {
      sentimentScore = -0.7 - Math.random() * 0.3
      sentimentLabel = 'negative'
    } else {
      sentimentScore = -0.2 + Math.random() * 0.4
      sentimentLabel = 'neutral'
    }

    // Extract entities (mock)
    const entities = [
      { text: 'AI', type: 'TECHNOLOGY', confidence: 0.9, start: 0, end: 2 },
      { text: 'machine learning', type: 'CONCEPT', confidence: 0.8, start: 10, end: 25 }
    ].filter(entity => inputText.includes(entity.text))

    // Extract keywords
    const keywords = words
      .filter(word => word.length > 3)
      .reduce((acc, word) => {
        acc[word] = (acc[word] || 0) + 1
        return acc
      }, {} as Record<string, number>)

    const topKeywords = Object.entries(keywords)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([word, frequency]) => ({
        word,
        importance: Math.random(),
        frequency
      }))

    // Detect topics
    const topics = [
      { topic: 'Technology', relevance: 0.8, keywords: ['ai', 'tech', 'software', 'digital'] },
      { topic: 'Business', relevance: 0.6, keywords: ['business', 'company', 'market', 'profit'] },
      { topic: 'Education', relevance: 0.4, keywords: ['learn', 'study', 'education', 'knowledge'] }
    ].filter(topic => 
      topic.keywords.some(keyword => inputText.toLowerCase().includes(keyword))
    )

    // Determine intent
    const intent = {
      primary: 'information_request',
      secondary: ['question', 'inquiry'],
      confidence: 0.85
    }

    // Language detection
    const language = {
      detected: 'en',
      confidence: 0.95
    }

    // Readability analysis
    const readability = {
      score: Math.random() * 100,
      level: 'intermediate',
      suggestions: [
        'Consider using shorter sentences',
        'Add more transition words',
        'Simplify complex terms'
      ]
    }

    // Emotion analysis
    const emotions = [
      { emotion: 'curiosity', intensity: 0.7 },
      { emotion: 'excitement', intensity: 0.5 },
      { emotion: 'confidence', intensity: 0.6 }
    ]

    // Generate summary
    const summary = `This text discusses ${topics[0]?.topic || 'general topics'} with a ${sentimentLabel} sentiment. Key themes include ${topKeywords.slice(0, 3).map(k => k.word).join(', ')}.`

    // Extract action items
    const actionItems = [
      'Review the main points',
      'Consider the implications',
      'Take appropriate action'
    ]

    return {
      sentiment: {
        score: sentimentScore,
        label: sentimentLabel,
        confidence: 0.85
      },
      entities,
      keywords: topKeywords,
      topics,
      intent,
      language,
      readability,
      emotions,
      summary,
      actionItems
    }
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100'
      case 'negative': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getEmotionColor = (emotion: string) => {
    const colors = {
      'curiosity': 'text-blue-600 bg-blue-100',
      'excitement': 'text-yellow-600 bg-yellow-100',
      'confidence': 'text-green-600 bg-green-100',
      'anger': 'text-red-600 bg-red-100',
      'sadness': 'text-gray-600 bg-gray-100',
      'joy': 'text-pink-600 bg-pink-100'
    }
    return colors[emotion as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Processing Status */}
      {isProcessing && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
              {processingStep}
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
          {/* Summary Card */}
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5 text-blue-600" />
                <span>Text Analysis Summary</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                {analysis.summary}
              </p>
              <div className="flex flex-wrap gap-2">
                <Badge className={getSentimentColor(analysis.sentiment.label)}>
                  {analysis.sentiment.label} sentiment
                </Badge>
                <Badge variant="outline">
                  {analysis.language.detected.toUpperCase()} language
                </Badge>
                <Badge variant="outline">
                  {analysis.readability.level} readability
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Detailed Analysis */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Sentiment Analysis */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Sentiment</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Score</span>
                    <span className="font-medium">
                      {(analysis.sentiment.score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${
                        analysis.sentiment.score > 0 ? 'bg-green-500' : 
                        analysis.sentiment.score < 0 ? 'bg-red-500' : 'bg-gray-500'
                      }`}
                      style={{ width: `${Math.abs(analysis.sentiment.score) * 100}%` }}
                    />
                  </div>
                  <Badge className={getSentimentColor(analysis.sentiment.label)}>
                    {analysis.sentiment.label}
                  </Badge>
                </div>
              </CardContent>
            </Card>

            {/* Entities */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Entities</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {analysis.entities.slice(0, 3).map((entity, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-sm font-medium">{entity.text}</span>
                      <Badge variant="outline" className="text-xs">
                        {entity.type}
                      </Badge>
                    </div>
                  ))}
                  {analysis.entities.length > 3 && (
                    <p className="text-xs text-gray-500">
                      +{analysis.entities.length - 3} more
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Keywords */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Zap className="h-4 w-4" />
                  <span>Keywords</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-1">
                  {analysis.keywords.slice(0, 5).map((keyword, index) => (
                    <Badge 
                      key={index} 
                      variant="secondary" 
                      className="text-xs"
                    >
                      {keyword.word}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Topics */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Filter className="h-4 w-4" />
                  <span>Topics</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {analysis.topics.map((topic, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-sm font-medium">{topic.topic}</span>
                      <span className="text-xs text-gray-500">
                        {(topic.relevance * 100).toFixed(0)}%
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Emotions */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Eye className="h-4 w-4" />
                  <span>Emotions</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {analysis.emotions.map((emotion, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <Badge className={getEmotionColor(emotion.emotion)}>
                        {emotion.emotion}
                      </Badge>
                      <span className="text-xs text-gray-500">
                        {(emotion.intensity * 100).toFixed(0)}%
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Intent */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Sparkles className="h-4 w-4" />
                  <span>Intent</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Badge variant="outline" className="w-full justify-center">
                    {analysis.intent.primary}
                  </Badge>
                  <div className="text-xs text-gray-500 text-center">
                    {(analysis.intent.confidence * 100).toFixed(0)}% confidence
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Action Items */}
          {analysis.actionItems.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <AlertCircle className="h-4 w-4" />
                  <span>Action Items</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {analysis.actionItems.map((item, index) => (
                    <li key={index} className="flex items-center space-x-2 text-sm">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
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
