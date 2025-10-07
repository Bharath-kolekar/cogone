'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Globe, Languages, Brain, Zap, CheckCircle, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface LanguageDetectionResult {
  primary: {
    language: string
    code: string
    confidence: number
    name: string
  }
  alternatives: Array<{
    language: string
    code: string
    confidence: number
    name: string
  }>
  script: {
    detected: string
    confidence: number
  }
  region: {
    detected: string
    confidence: number
  }
  dialect: {
    detected: string
    confidence: number
  }
  complexity: {
    level: 'basic' | 'intermediate' | 'advanced' | 'native'
    score: number
  }
  characteristics: {
    formality: 'formal' | 'informal' | 'mixed'
    tone: 'professional' | 'casual' | 'academic' | 'creative'
    style: 'conversational' | 'technical' | 'literary' | 'business'
  }
}

interface SmartLanguageDetectorProps {
  text: string
  onLanguageDetected?: (result: LanguageDetectionResult) => void
  showAlternatives?: boolean
  enableRealTime?: boolean
  className?: string
}

const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
  { code: 'ta', name: 'Tamil', flag: '🇮🇳' },
  { code: 'te', name: 'Telugu', flag: '🇮🇳' },
  { code: 'bn', name: 'Bengali', flag: '🇮🇳' },
  { code: 'gu', name: 'Gujarati', flag: '🇮🇳' },
  { code: 'mr', name: 'Marathi', flag: '🇮🇳' },
  { code: 'kn', name: 'Kannada', flag: '🇮🇳' },
  { code: 'ml', name: 'Malayalam', flag: '🇮🇳' },
  { code: 'pa', name: 'Punjabi', flag: '🇮🇳' },
  { code: 'or', name: 'Odia', flag: '🇮🇳' },
  { code: 'as', name: 'Assamese', flag: '🇮🇳' },
  { code: 'zh', name: 'Chinese', flag: '🇨🇳' },
  { code: 'ja', name: 'Japanese', flag: '🇯🇵' },
  { code: 'ko', name: 'Korean', flag: '🇰🇷' },
  { code: 'ar', name: 'Arabic', flag: '🇸🇦' },
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'it', name: 'Italian', flag: '🇮🇹' },
  { code: 'pt', name: 'Portuguese', flag: '🇵🇹' },
  { code: 'ru', name: 'Russian', flag: '🇷🇺' },
  { code: 'th', name: 'Thai', flag: '🇹🇭' },
  { code: 'vi', name: 'Vietnamese', flag: '🇻🇳' }
]

export function SmartLanguageDetector({
  text,
  onLanguageDetected,
  showAlternatives = true,
  enableRealTime = true,
  className = ''
}: SmartLanguageDetectorProps) {
  const [detection, setDetection] = useState<LanguageDetectionResult | null>(null)
  const [isDetecting, setIsDetecting] = useState(false)
  const [detectionStep, setDetectionStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showDetails, setShowDetails] = useState(false)
  const detectionRef = useRef<LanguageDetectionResult | null>(null)

  useEffect(() => {
    if (text && enableRealTime) {
      detectLanguage(text)
    }
  }, [text, enableRealTime])

  const detectLanguage = async (inputText: string) => {
    setIsDetecting(true)
    setProgress(0)
    setDetectionStep('Initializing language detection...')

    try {
      // Simulate real-time detection steps
      const steps = [
        'Analyzing character patterns...',
        'Detecting script type...',
        'Identifying language patterns...',
        'Calculating confidence scores...',
        'Determining regional variants...',
        'Analyzing dialect features...',
        'Assessing complexity level...',
        'Evaluating characteristics...',
        'Generating alternatives...',
        'Finalizing detection...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setDetectionStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 150))
      }

      // Perform language detection
      const result = await performLanguageDetection(inputText)
      
      setDetection(result)
      detectionRef.current = result
      onLanguageDetected?.(result)
      
    } catch (error) {
      console.error('Language detection failed:', error)
    } finally {
      setIsDetecting(false)
      setProgress(100)
      setDetectionStep('Detection complete!')
    }
  }

  const performLanguageDetection = async (inputText: string): Promise<LanguageDetectionResult> => {
    // Simulate advanced language detection
    await new Promise(resolve => setTimeout(resolve, 800))

    // Simple heuristic-based detection (in real implementation, use proper NLP libraries)
    const textLower = inputText.toLowerCase()
    
    // Check for Hindi/Indian languages
    const hindiPatterns = /[\u0900-\u097F]/
    const tamilPatterns = /[\u0B80-\u0BFF]/
    const teluguPatterns = /[\u0C00-\u0C7F]/
    const bengaliPatterns = /[\u0980-\u09FF]/
    
    let detectedLanguage = 'en'
    let confidence = 0.95
    let script = 'latin'
    let region = 'US'
    let dialect = 'standard'

    if (hindiPatterns.test(inputText)) {
      detectedLanguage = 'hi'
      script = 'devanagari'
      region = 'IN'
      dialect = 'standard'
    } else if (tamilPatterns.test(inputText)) {
      detectedLanguage = 'ta'
      script = 'tamil'
      region = 'IN'
      dialect = 'standard'
    } else if (teluguPatterns.test(inputText)) {
      detectedLanguage = 'te'
      script = 'telugu'
      region = 'IN'
      dialect = 'standard'
    } else if (bengaliPatterns.test(inputText)) {
      detectedLanguage = 'bn'
      script = 'bengali'
      region = 'IN'
      dialect = 'standard'
    } else {
      // English detection with some heuristics
      const englishWords = ['the', 'and', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would', 'could', 'should']
      const englishCount = englishWords.filter(word => textLower.includes(word)).length
      confidence = Math.min(0.95, 0.7 + (englishCount * 0.05))
    }

    const languageInfo = SUPPORTED_LANGUAGES.find(lang => lang.code === detectedLanguage) || SUPPORTED_LANGUAGES[0]

    // Generate alternatives
    const alternatives = SUPPORTED_LANGUAGES
      .filter(lang => lang.code !== detectedLanguage)
      .slice(0, 3)
      .map(lang => ({
        language: lang.name,
        code: lang.code,
        confidence: Math.random() * 0.3,
        name: lang.name
      }))
      .sort((a, b) => b.confidence - a.confidence)

    // Determine complexity
    const wordCount = inputText.split(/\s+/).length
    const avgWordLength = inputText.split(/\s+/).reduce((sum, word) => sum + word.length, 0) / wordCount
    const complexityScore = (wordCount * 0.3) + (avgWordLength * 0.7)
    
    let complexityLevel: 'basic' | 'intermediate' | 'advanced' | 'native' = 'basic'
    if (complexityScore > 8) complexityLevel = 'native'
    else if (complexityScore > 6) complexityLevel = 'advanced'
    else if (complexityScore > 4) complexityLevel = 'intermediate'

    // Determine characteristics
    const formality = textLower.includes('please') || textLower.includes('thank you') ? 'formal' : 'informal'
    const tone = textLower.includes('analysis') || textLower.includes('research') ? 'academic' : 
                 textLower.includes('business') || textLower.includes('professional') ? 'professional' : 'casual'
    const style = textLower.includes('?') ? 'conversational' : 
                  textLower.includes('technical') ? 'technical' : 'business'

    return {
      primary: {
        language: languageInfo.name,
        code: detectedLanguage,
        confidence,
        name: languageInfo.name
      },
      alternatives,
      script: {
        detected: script,
        confidence: 0.9
      },
      region: {
        detected: region,
        confidence: 0.8
      },
      dialect: {
        detected: dialect,
        confidence: 0.7
      },
      complexity: {
        level: complexityLevel,
        score: complexityScore
      },
      characteristics: {
        formality: formality as 'formal' | 'informal' | 'mixed',
        tone: tone as 'professional' | 'casual' | 'academic' | 'creative',
        style: style as 'conversational' | 'technical' | 'literary' | 'business'
      }
    }
  }

  const getLanguageFlag = (code: string) => {
    const lang = SUPPORTED_LANGUAGES.find(l => l.code === code)
    return lang?.flag || '🌍'
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getComplexityColor = (level: string) => {
    switch (level) {
      case 'native': return 'text-purple-600 bg-purple-100'
      case 'advanced': return 'text-blue-600 bg-blue-100'
      case 'intermediate': return 'text-yellow-600 bg-yellow-100'
      default: return 'text-green-600 bg-green-100'
    }
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Detection Status */}
      {isDetecting && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
              {detectionStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Detection Results */}
      {detection && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Primary Detection */}
          <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Globe className="h-5 w-5 text-green-600" />
                <span>Detected Language</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center space-x-4 mb-4">
                <div className="text-4xl">
                  {getLanguageFlag(detection.primary.code)}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                    {detection.primary.language}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {detection.primary.code.toUpperCase()} • {detection.script.detected} script
                  </p>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2 mb-4">
                <Badge className={getConfidenceColor(detection.primary.confidence)}>
                  {(detection.primary.confidence * 100).toFixed(1)}% confidence
                </Badge>
                <Badge variant="outline">
                  {detection.region.detected} region
                </Badge>
                <Badge variant="outline">
                  {detection.dialect.detected} dialect
                </Badge>
              </div>

              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Complexity</div>
                  <Badge className={getComplexityColor(detection.complexity.level)}>
                    {detection.complexity.level}
                  </Badge>
                </div>
                <div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Formality</div>
                  <Badge variant="outline">
                    {detection.characteristics.formality}
                  </Badge>
                </div>
                <div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Tone</div>
                  <Badge variant="outline">
                    {detection.characteristics.tone}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Alternative Languages */}
          {showAlternatives && detection.alternatives.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Languages className="h-4 w-4" />
                  <span>Alternative Languages</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {detection.alternatives.map((alt, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">
                          {getLanguageFlag(alt.code)}
                        </span>
                        <div>
                          <div className="font-medium">{alt.language}</div>
                          <div className="text-sm text-gray-500">{alt.code.toUpperCase()}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">
                          {(alt.confidence * 100).toFixed(1)}%
                        </div>
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full"
                            style={{ width: `${alt.confidence * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Detailed Analysis */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Script Analysis */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Brain className="h-4 w-4" />
                  <span>Script Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Script</span>
                    <Badge variant="outline">
                      {detection.script.detected}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Confidence</span>
                    <span className="text-sm font-medium">
                      {(detection.script.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Complexity Analysis */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Zap className="h-4 w-4" />
                  <span>Complexity Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Level</span>
                    <Badge className={getComplexityColor(detection.complexity.level)}>
                      {detection.complexity.level}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Score</span>
                    <span className="text-sm font-medium">
                      {detection.complexity.score.toFixed(1)}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Characteristics */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <CheckCircle className="h-4 w-4" />
                  <span>Characteristics</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Formality</span>
                    <Badge variant="outline">
                      {detection.characteristics.formality}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Tone</span>
                    <Badge variant="outline">
                      {detection.characteristics.tone}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Style</span>
                    <Badge variant="outline">
                      {detection.characteristics.style}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Regional Analysis */}
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Globe className="h-4 w-4" />
                  <span>Regional Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Region</span>
                    <Badge variant="outline">
                      {detection.region.detected}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Dialect</span>
                    <Badge variant="outline">
                      {detection.dialect.detected}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Confidence</span>
                    <span className="text-sm font-medium">
                      {(detection.region.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
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
