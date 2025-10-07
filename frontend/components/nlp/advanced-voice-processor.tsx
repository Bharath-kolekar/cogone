'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, MicOff, Volume2, VolumeX, Play, Pause, RotateCcw, Download, Upload, Brain, Zap, Target, TrendingUp } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Textarea } from '@/components/ui/textarea'
import { Slider } from '@/components/ui/slider'
import { AdvancedTextProcessor } from './advanced-text-processor'
import { SmartLanguageDetector } from './smart-language-detector'
import { IntelligentSentimentAnalyzer } from './intelligent-sentiment-analyzer'

interface VoiceProcessingResult {
  transcript: string
  confidence: number
  language: string
  duration: number
  wordCount: number
  speakingRate: number
  clarity: number
  emotions: Array<{
    emotion: string
    intensity: number
  }>
  keywords: string[]
  summary: string
  actionItems: string[]
  sentiment: {
    score: number
    label: string
  }
}

interface AdvancedVoiceProcessorProps {
  onTranscript?: (transcript: string) => void
  onProcessingComplete?: (result: VoiceProcessingResult) => void
  enableRealTime?: boolean
  showAnalysis?: boolean
  autoStart?: boolean
  className?: string
}

export function AdvancedVoiceProcessor({
  onTranscript,
  onProcessingComplete,
  enableRealTime = true,
  showAnalysis = true,
  autoStart = false,
  className = ''
}: AdvancedVoiceProcessorProps) {
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [processingResult, setProcessingResult] = useState<VoiceProcessingResult | null>(null)
  const [recordingTime, setRecordingTime] = useState(0)
  const [audioLevel, setAudioLevel] = useState(0)
  const [processingStep, setProcessingStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [sensitivity, setSensitivity] = useState([0.5])
  const [language, setLanguage] = useState('en')
  const [showTranscript, setShowTranscript] = useState(true)
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const recordingIntervalRef = useRef<NodeJS.Timeout | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const analyserRef = useRef<AnalyserNode | null>(null)
  const animationFrameRef = useRef<number | null>(null)

  useEffect(() => {
    if (autoStart) {
      startRecording()
    }
    
    return () => {
      stopRecording()
      cleanup()
    }
  }, [autoStart])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 44100
        } 
      })
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }
      
      mediaRecorder.onstop = () => {
        processAudio()
      }
      
      // Setup audio analysis
      setupAudioAnalysis(stream)
      
      mediaRecorder.start(100) // Collect data every 100ms
      setIsRecording(true)
      
      // Start recording timer
      recordingIntervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 0.1)
      }, 100)
      
      // Start audio level monitoring
      monitorAudioLevel()
      
    } catch (error) {
      console.error('Error starting recording:', error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current)
        recordingIntervalRef.current = null
      }
      
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }

  const setupAudioAnalysis = (stream: MediaStream) => {
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
      const analyser = audioContext.createAnalyser()
      const source = audioContext.createMediaStreamSource(stream)
      
      analyser.fftSize = 256
      source.connect(analyser)
      
      audioContextRef.current = audioContext
      analyserRef.current = analyser
    } catch (error) {
      console.error('Error setting up audio analysis:', error)
    }
  }

  const monitorAudioLevel = () => {
    const updateLevel = () => {
      if (analyserRef.current) {
        const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount)
        analyserRef.current.getByteFrequencyData(dataArray)
        
        const average = dataArray.reduce((sum, value) => sum + value, 0) / dataArray.length
        setAudioLevel(average / 255)
        
        animationFrameRef.current = requestAnimationFrame(updateLevel)
      }
    }
    updateLevel()
  }

  const processAudio = async () => {
    setIsProcessing(true)
    setProgress(0)
    setProcessingStep('Processing audio...')

    try {
      // Simulate audio processing steps
      const steps = [
        'Converting audio to text...',
        'Analyzing speech patterns...',
        'Detecting language...',
        'Extracting emotions...',
        'Identifying keywords...',
        'Analyzing sentiment...',
        'Generating summary...',
        'Finalizing results...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setProcessingStep(steps[i])
        setProgress((i + 1) * 12.5)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Simulate transcription result
      const mockTranscript = generateMockTranscript()
      setTranscript(mockTranscript)
      onTranscript?.(mockTranscript)

      // Process the transcript
      const result = await processTranscript(mockTranscript)
      setProcessingResult(result)
      onProcessingComplete?.(result)

    } catch (error) {
      console.error('Audio processing failed:', error)
    } finally {
      setIsProcessing(false)
      setProgress(100)
      setProcessingStep('Processing complete!')
    }
  }

  const generateMockTranscript = (): string => {
    const transcripts = [
      "Hello, I'm excited to discuss our new AI-powered voice processing system. This technology will revolutionize how we interact with computers and enable more natural communication.",
      "The implementation includes advanced natural language processing capabilities, real-time sentiment analysis, and intelligent entity extraction. We're confident this will improve user experience significantly.",
      "Our team has been working on this project for several months, and we're ready to launch the beta version next week. The feedback from early users has been overwhelmingly positive.",
      "This voice-to-text system supports multiple languages including English, Hindi, Tamil, and Telugu. The accuracy rate is above 95% for clear speech in quiet environments.",
      "We're planning to integrate this with our existing AI orchestrator to provide even more intelligent responses and context-aware processing."
    ]
    return transcripts[Math.floor(Math.random() * transcripts.length)]
  }

  const processTranscript = async (text: string): Promise<VoiceProcessingResult> => {
    // Simulate advanced transcript processing
    await new Promise(resolve => setTimeout(resolve, 800))

    const words = text.split(/\s+/)
    const wordCount = words.length
    const duration = recordingTime
    const speakingRate = wordCount / (duration / 60) // words per minute

    // Simulate sentiment analysis
    const sentimentScore = Math.random() * 2 - 1 // -1 to 1
    const sentimentLabel = sentimentScore > 0.3 ? 'positive' : sentimentScore < -0.3 ? 'negative' : 'neutral'

    // Simulate emotion detection
    const emotions = [
      { emotion: 'excitement', intensity: Math.random() },
      { emotion: 'confidence', intensity: Math.random() },
      { emotion: 'satisfaction', intensity: Math.random() }
    ].filter(e => e.intensity > 0.3)

    // Extract keywords
    const keywords = words
      .filter(word => word.length > 4)
      .slice(0, 5)
      .map(word => word.toLowerCase())

    // Generate summary
    const summary = `This ${duration.toFixed(1)}-second recording contains ${wordCount} words spoken at ${speakingRate.toFixed(1)} words per minute. The content discusses ${keywords.slice(0, 3).join(', ')} with a ${sentimentLabel} sentiment.`

    // Generate action items
    const actionItems = [
      'Review the key points discussed',
      'Follow up on mentioned topics',
      'Schedule next meeting if needed'
    ]

    return {
      transcript: text,
      confidence: 0.85 + Math.random() * 0.1,
      language: language,
      duration,
      wordCount,
      speakingRate,
      clarity: 0.8 + Math.random() * 0.2,
      emotions,
      keywords,
      summary,
      actionItems,
      sentiment: {
        score: sentimentScore,
        label: sentimentLabel
      }
    }
  }

  const cleanup = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())
    }
    if (audioContextRef.current) {
      audioContextRef.current.close()
    }
    if (recordingIntervalRef.current) {
      clearInterval(recordingIntervalRef.current)
    }
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current)
    }
  }

  const resetRecording = () => {
    stopRecording()
    setTranscript('')
    setProcessingResult(null)
    setRecordingTime(0)
    setAudioLevel(0)
    setProgress(0)
    setProcessingStep('')
  }

  const downloadTranscript = () => {
    if (transcript) {
      const blob = new Blob([transcript], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `transcript-${Date.now()}.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
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
      'excitement': 'text-yellow-600 bg-yellow-100',
      'confidence': 'text-blue-600 bg-blue-100',
      'satisfaction': 'text-green-600 bg-green-100',
      'frustration': 'text-red-600 bg-red-100',
      'calm': 'text-purple-600 bg-purple-100'
    }
    return colors[emotion as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Recording Controls */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Mic className="h-6 w-6 text-blue-600" />
            <span>Advanced Voice Processor</span>
          </CardTitle>
          <CardDescription>
            High-quality voice recording with real-time analysis
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Recording Status */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isProcessing}
                className={`${isRecording ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'}`}
              >
                {isRecording ? <MicOff className="h-4 w-4 mr-2" /> : <Mic className="h-4 w-4 mr-2" />}
                {isRecording ? 'Stop Recording' : 'Start Recording'}
              </Button>
              
              {isRecording && (
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {recordingTime.toFixed(1)}s
                  </span>
                </div>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={resetRecording}
                disabled={isRecording || isProcessing}
              >
                <RotateCcw className="h-4 w-4 mr-1" />
                Reset
              </Button>
              {transcript && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={downloadTranscript}
                >
                  <Download className="h-4 w-4 mr-1" />
                  Download
                </Button>
              )}
            </div>
          </div>

          {/* Audio Level Indicator */}
          {isRecording && (
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Volume2 className="h-4 w-4 text-gray-500" />
                <span className="text-sm text-gray-600 dark:text-gray-400">Audio Level</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-green-500 h-2 rounded-full transition-all duration-100"
                  style={{ width: `${audioLevel * 100}%` }}
                />
              </div>
            </div>
          )}

          {/* Processing Status */}
          {isProcessing && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
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

          {/* Advanced Settings */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Sensitivity</span>
              <Slider
                value={sensitivity}
                onValueChange={setSensitivity}
                max={1}
                min={0}
                step={0.1}
                className="w-32"
              />
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">Language</span>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-3 py-1 border rounded-md text-sm"
              >
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="ta">Tamil</option>
                <option value="te">Telugu</option>
                <option value="bn">Bengali</option>
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Transcript Display */}
      {transcript && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Volume2 className="h-5 w-5 text-green-600" />
                  <span>Transcript</span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setShowTranscript(!showTranscript)}
                >
                  {showTranscript ? 'Hide' : 'Show'} Transcript
                </Button>
              </CardTitle>
            </CardHeader>
            {showTranscript && (
              <CardContent>
                <Textarea
                  value={transcript}
                  readOnly
                  className="min-h-[120px] font-mono text-sm"
                />
              </CardContent>
            )}
          </Card>
        </motion.div>
      )}

      {/* Processing Results */}
      {processingResult && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {processingResult.wordCount}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Words</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">
                    {processingResult.speakingRate.toFixed(1)}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">WPM</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">
                    {(processingResult.confidence * 100).toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Confidence</div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {processingResult.duration.toFixed(1)}s
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Duration</div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sentiment and Emotions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Sentiment Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center space-x-3">
                  <Badge className={getSentimentColor(processingResult.sentiment.label)}>
                    {processingResult.sentiment.label}
                  </Badge>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Score: {(processingResult.sentiment.score * 100).toFixed(1)}%
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Brain className="h-4 w-4" />
                  <span>Emotions Detected</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {processingResult.emotions.map((emotion, index) => (
                    <Badge key={index} className={getEmotionColor(emotion.emotion)}>
                      {emotion.emotion} ({(emotion.intensity * 100).toFixed(0)}%)
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Keywords and Summary */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Key Topics</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {processingResult.keywords.map((keyword, index) => (
                    <Badge key={index} variant="outline">
                      {keyword}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Zap className="h-4 w-4" />
                  <span>Summary</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  {processingResult.summary}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Action Items */}
          {processingResult.actionItems.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Action Items</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {processingResult.actionItems.map((item, index) => (
                    <li key={index} className="flex items-center space-x-2 text-sm">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </motion.div>
      )}

      {/* Advanced Analysis */}
      {showAnalysis && transcript && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="text-center">
            <Button
              variant="outline"
              onClick={() => setShowAdvanced(!showAdvanced)}
            >
              <Brain className="h-4 w-4 mr-2" />
              {showAdvanced ? 'Hide' : 'Show'} Advanced Analysis
            </Button>
          </div>

          {showAdvanced && (
            <div className="space-y-6">
              <AdvancedTextProcessor
                text={transcript}
                showVisualization={true}
                enableRealTime={false}
              />
              
              <SmartLanguageDetector
                text={transcript}
                showAlternatives={true}
                enableRealTime={false}
              />
              
              <IntelligentSentimentAnalyzer
                text={transcript}
                showEmotions={true}
                showAspects={true}
                showTrends={true}
                enableRealTime={false}
              />
            </div>
          )}
        </motion.div>
      )}
    </div>
  )
}
