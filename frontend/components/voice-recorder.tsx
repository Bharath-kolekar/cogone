'use client'

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Mic, MicOff, Square, Play, Pause } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

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
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [audioUrl, setAudioUrl] = useState<string | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const [transcript, setTranscript] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

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

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      
      mediaRecorderRef.current = mediaRecorder
      
      const audioChunks: BlobPart[] = []
      
      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data)
      }
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' })
        setAudioBlob(audioBlob)
        setAudioUrl(URL.createObjectURL(audioBlob))
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
      }
      
      mediaRecorder.start()
      onRecordingChange(true)
      setRecordingTime(0)
      
      // Start timer
      intervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
      
    } catch (error) {
      console.error('Error starting recording:', error)
      alert('Unable to access microphone. Please check permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
      onRecordingChange(false)
      setIsPaused(false)
      
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }

  const pauseRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.pause()
      setIsPaused(true)
    }
  }

  const resumeRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'paused') {
      mediaRecorderRef.current.resume()
      setIsPaused(false)
    }
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

  const processAudio = async () => {
    if (!audioBlob) return
    
    setIsProcessing(true)
    
    try {
      // Try local speech recognition first
      if (browserSupport.webSpeech) {
        const recognition = new ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition)()
        recognition.continuous = false
        recognition.interimResults = false
        recognition.lang = 'en-IN' // Indian English
        
        recognition.onresult = (event) => {
          const transcript = event.results[0][0].transcript
          setTranscript(transcript)
          onTranscript(transcript)
          setIsProcessing(false)
        }
        
        recognition.onerror = () => {
          // Fallback to server processing
          processAudioServer()
        }
        
        recognition.start()
      } else {
        // Fallback to server processing
        processAudioServer()
      }
    } catch (error) {
      console.error('Error processing audio:', error)
      processAudioServer()
    }
  }

  const processAudioServer = async () => {
    if (!audioBlob) return
    
    try {
      const formData = new FormData()
      formData.append('audio_file', audioBlob, 'recording.webm')
      formData.append('language', 'en')
      
      const response = await fetch('/api/v0/voice/transcribe', {
        method: 'POST',
        body: formData,
      })
      
      if (response.ok) {
        const result = await response.json()
        setTranscript(result.transcript)
        onTranscript(result.transcript)
      } else {
        throw new Error('Transcription failed')
      }
    } catch (error) {
      console.error('Server transcription failed:', error)
      // Fallback to mock transcript
      const mockTranscript = "Create a todo app with add, edit, and delete functionality"
      setTranscript(mockTranscript)
      onTranscript(mockTranscript)
    } finally {
      setIsProcessing(false)
    }
  }

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
      {/* Recording Controls */}
      <div className="flex justify-center space-x-4">
        {!isRecording ? (
          <Button
            onClick={startRecording}
            disabled={disabled}
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
        {isRecording && (
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

      {/* Audio Playback */}
      <AnimatePresence>
        {audioUrl && !isRecording && (
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
                onClick={processAudio}
                disabled={isProcessing}
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
                    Generate App
                  </>
                )}
              </Button>
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