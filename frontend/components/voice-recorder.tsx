'use client'

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Mic, MicOff, Square, Play, Pause } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useVoiceProcessing } from '@/hooks/useVoiceProcessing'

interface VoiceRecorderProps {
  onTranscript: (transcript: string) => void
  isRecording: boolean
  onRecordingChange: (recording: boolean) => void
  disabled?: boolean
}

export function VoiceRecorder({ 
  onTranscript, 
  isRecording, 
  onRecordingChange, 
  disabled = false 
}: VoiceRecorderProps) {
  const [isPaused, setIsPaused] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  // Use the voice processing hook
  const {
    isRecording: hookIsRecording,
    isProcessing,
    isGenerating,
    transcript,
    intent,
    appId,
    appStatus,
    error,
    audioBlob,
    audioUrl,
    startRecording: hookStartRecording,
    stopRecording: hookStopRecording,
    processAudio,
    extractIntent,
    generateApp,
    clearError,
  } = useVoiceProcessing()

  // Check for browser support
  const [browserSupport, setBrowserSupport] = useState({
    mediaRecorder: false,
    webSpeech: false,
  })

  useEffect(() => {
    // Check MediaRecorder support
    setBrowserSupport(prev => ({
      ...prev,
      mediaRecorder: typeof MediaRecorder !== 'undefined'
    }))

    // Check Web Speech API support
    setBrowserSupport(prev => ({
      ...prev,
      webSpeech: 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
    }))
  }, [])

  // Sync with parent component state
  useEffect(() => {
    onRecordingChange(hookIsRecording)
  }, [hookIsRecording, onRecordingChange])

  // Handle transcript updates
  useEffect(() => {
    if (transcript) {
      onTranscript(transcript)
    }
  }, [transcript, onTranscript])

  // Handle recording timer
  useEffect(() => {
    if (hookIsRecording) {
      setRecordingTime(0)
      intervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }
  }, [hookIsRecording])

  const startRecording = async () => {
    await hookStartRecording()
  }

  const stopRecording = () => {
    hookStopRecording()
  }

  const pauseRecording = () => {
    // Pause functionality can be added later if needed
    setIsPaused(true)
  }

  const resumeRecording = () => {
    // Resume functionality can be added later if needed
    setIsPaused(false)
  }

  const playRecording = () => {
    if (audioUrl && audioRef.current) {
      audioRef.current.play()
      setIsPlaying(true)
    }
  }

  const pausePlayback = () => {
    if (audioRef.current) {
      audioRef.current.pause()
      setIsPlaying(false)
    }
  }

  const handleProcessAudio = async () => {
    await processAudio()
  }

  const handleGenerateApp = async () => {
    if (transcript && intent) {
      await generateApp(transcript, intent)
    } else if (transcript) {
      // Extract intent first, then generate app
      await extractIntent(transcript)
      // The generateApp will be called automatically when intent is available
    }
  }

  // Auto-generate app when intent is available
  useEffect(() => {
    if (intent && transcript && !appId) {
      generateApp(transcript, intent)
    }
  }, [intent, transcript, appId, generateApp])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (!browserSupport.mediaRecorder) {
    return (
      <Card className="bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800">
        <CardContent className="p-6 text-center">
          <p className="text-red-600 dark:text-red-400">
            Your browser doesn't support audio recording. Please use Chrome, Firefox, or Safari.
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {/* Error Display */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4"
        >
          <div className="flex items-center justify-between">
            <p className="text-red-600 dark:text-red-400">{error}</p>
            <Button
              onClick={clearError}
              variant="ghost"
              size="sm"
              className="text-red-600 hover:text-red-700"
            >
              ×
            </Button>
          </div>
        </motion.div>
      )}

      {/* Recording Controls */}
      <div className="flex justify-center space-x-4">
        {!hookIsRecording ? (
          <Button
            onClick={startRecording}
            disabled={disabled || isProcessing || isGenerating}
            size="lg"
            className="bg-red-500 hover:bg-red-600 text-white px-8 py-4 rounded-full shadow-lg"
          >
            <Mic className="h-6 w-6 mr-2" />
            Start Recording
          </Button>
        ) : (
          <div className="flex space-x-2">
            {!isPaused ? (
              <Button
                onClick={pauseRecording}
                variant="outline"
                size="lg"
                className="px-6 py-4"
              >
                <Pause className="h-5 w-5 mr-2" />
                Pause
              </Button>
            ) : (
              <Button
                onClick={resumeRecording}
                variant="outline"
                size="lg"
                className="px-6 py-4"
              >
                <Play className="h-5 w-5 mr-2" />
                Resume
              </Button>
            )}
            
            <Button
              onClick={stopRecording}
              size="lg"
              className="bg-red-500 hover:bg-red-600 text-white px-6 py-4"
            >
              <Square className="h-5 w-5 mr-2" />
              Stop
            </Button>
          </div>
        )}
      </div>

      {/* Recording Status */}
      <AnimatePresence>
        {hookIsRecording && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="text-center"
          >
            <div className="flex items-center justify-center space-x-3 mb-2">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
              <span className="text-lg font-medium text-red-600 dark:text-red-400">
                Recording... {formatTime(recordingTime)}
              </span>
            </div>
            <p className="text-sm text-gray-500">
              Speak clearly and describe your app idea
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Processing Status */}
      <AnimatePresence>
        {isProcessing && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="text-center"
          >
            <div className="flex items-center justify-center space-x-3 mb-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
              <span className="text-lg font-medium text-blue-600 dark:text-blue-400">
                Processing audio...
              </span>
            </div>
            <p className="text-sm text-gray-500">
              Converting your voice to text
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Generation Status */}
      <AnimatePresence>
        {isGenerating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="text-center"
          >
            <div className="flex items-center justify-center space-x-3 mb-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-500"></div>
              <span className="text-lg font-medium text-green-600 dark:text-green-400">
                Generating app...
              </span>
            </div>
            <p className="text-sm text-gray-500">
              Creating your application
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Audio Playback */}
      <AnimatePresence>
        {audioUrl && !hookIsRecording && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="space-y-3"
          >
            <div className="flex justify-center space-x-2">
              <Button
                onClick={isPlaying ? pausePlayback : playRecording}
                variant="outline"
                size="sm"
              >
                {isPlaying ? (
                  <Pause className="h-4 w-4 mr-2" />
                ) : (
                  <Play className="h-4 w-4 mr-2" />
                )}
                {isPlaying ? 'Pause' : 'Play'} Recording
              </Button>
              
              <Button
                onClick={handleProcessAudio}
                disabled={isProcessing || isGenerating}
                size="sm"
                className="bg-blue-500 hover:bg-blue-600 text-white"
              >
                {isProcessing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <Mic className="h-4 w-4 mr-2" />
                    Process Audio
                  </>
                )}
              </Button>

              {transcript && (
                <Button
                  onClick={handleGenerateApp}
                  disabled={isGenerating}
                  size="sm"
                  className="bg-green-500 hover:bg-green-600 text-white"
                >
                  {isGenerating ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Generating...
                    </>
                  ) : (
                    <>
                      <Mic className="h-4 w-4 mr-2" />
                      Generate App
                    </>
                  )}
                </Button>
              )}
            </div>
            
            <audio
              ref={audioRef}
              src={audioUrl}
              onEnded={() => setIsPlaying(false)}
              className="hidden"
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Transcript Display */}
      <AnimatePresence>
        {transcript && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4"
          >
            <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">
              Voice Command:
            </h3>
            <p className="text-gray-600 dark:text-gray-400 italic">
              "{transcript}"
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Intent Display */}
      <AnimatePresence>
        {intent && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
          >
            <h3 className="font-semibold text-blue-800 dark:text-blue-200 mb-2">
              Detected Intent:
            </h3>
            <p className="text-blue-600 dark:text-blue-400">
              {intent}
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* App Status Display */}
      <AnimatePresence>
        {appStatus && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4"
          >
            <h3 className="font-semibold text-green-800 dark:text-green-200 mb-2">
              App Generation Status:
            </h3>
            <div className="space-y-2">
              <p className="text-green-600 dark:text-green-400">
                Status: {appStatus.status}
              </p>
              {appStatus.progress && (
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${appStatus.progress}%` }}
                  ></div>
                </div>
              )}
              {appStatus.current_step && (
                <p className="text-sm text-green-600 dark:text-green-400">
                  Current step: {appStatus.current_step}
                </p>
              )}
              {appStatus.preview_url && (
                <div className="mt-2">
                  <a
                    href={appStatus.preview_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    View App Preview
                  </a>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Browser Support Info */}
      <div className="text-center text-xs text-gray-400">
        {browserSupport.webSpeech ? (
          <span className="text-green-600">✓ Local speech recognition available</span>
        ) : (
          <span className="text-yellow-600">⚠ Using server-side processing</span>
        )}
      </div>
    </div>
  )
}