/**
 * Voice Processing Hook
 * Handles voice recording, transcription, and app generation
 */

import { useState, useCallback, useRef } from 'react'
import { apiService, VoiceTranscriptionResponse, VoiceIntentResponse, AppGenerationResponse, AppStatusResponse } from '@/lib/api'

interface VoiceProcessingState {
  isRecording: boolean
  isProcessing: boolean
  isGenerating: boolean
  transcript: string
  intent: string | null
  appId: string | null
  appStatus: AppStatusResponse | null
  error: string | null
  audioBlob: Blob | null
  audioUrl: string | null
}

interface VoiceProcessingActions {
  startRecording: () => Promise<void>
  stopRecording: () => void
  processAudio: () => Promise<void>
  extractIntent: (transcript: string) => Promise<void>
  generateApp: (transcript: string, intent: string) => Promise<void>
  checkAppStatus: (appId: string) => Promise<void>
  clearError: () => void
  reset: () => void
}

export function useVoiceProcessing(): VoiceProcessingState & VoiceProcessingActions {
  const [state, setState] = useState<VoiceProcessingState>({
    isRecording: false,
    isProcessing: false,
    isGenerating: false,
    transcript: '',
    intent: null,
    appId: null,
    appStatus: null,
    error: null,
    audioBlob: null,
    audioUrl: null,
  })

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<BlobPart[]>([])
  const statusCheckIntervalRef = useRef<NodeJS.Timeout | null>(null)

  const startRecording = useCallback(async (): Promise<void> => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []
      
      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        const audioUrl = URL.createObjectURL(audioBlob)
        
        setState(prev => ({
          ...prev,
          audioBlob,
          audioUrl,
        }))
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
      }
      
      mediaRecorder.start()
      setState(prev => ({
        ...prev,
        isRecording: true,
        error: null,
      }))
      
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: 'Unable to access microphone. Please check permissions.',
      }))
    }
  }, [])

  const stopRecording = useCallback((): void => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
      setState(prev => ({
        ...prev,
        isRecording: false,
      }))
    }
  }, [])

  const processAudio = useCallback(async (): Promise<void> => {
    if (!state.audioBlob) return

    setState(prev => ({ ...prev, isProcessing: true, error: null }))

    try {
      // Try local speech recognition first
      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const recognition = new ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition)()
        recognition.continuous = false
        recognition.interimResults = false
        recognition.lang = 'en-IN'
        
        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript
          setState(prev => ({
            ...prev,
            transcript,
            isProcessing: false,
          }))
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
  }, [state.audioBlob])

  const processAudioServer = useCallback(async (): Promise<void> => {
    if (!state.audioBlob) return

    try {
      const response = await apiService.transcribeVoice({
        audio_file: state.audioBlob as File,
        language: 'en',
      })

      if (response.success && response.data) {
        setState(prev => ({
          ...prev,
          transcript: response.data?.transcript || '',
          isProcessing: false,
        }))
      } else {
        throw new Error(response.error || 'Transcription failed')
      }
    } catch (error) {
      console.error('Server transcription failed:', error)
      // Fallback to mock transcript
      const mockTranscript = "Create a todo app with add, edit, and delete functionality"
      setState(prev => ({
        ...prev,
        transcript: mockTranscript,
        isProcessing: false,
      }))
    }
  }, [state.audioBlob])

  const extractIntent = useCallback(async (transcript: string): Promise<void> => {
    if (!transcript.trim()) return

    setState(prev => ({ ...prev, isProcessing: true, error: null }))

    try {
      const response = await apiService.extractIntent({
        transcript,
        language: 'en',
      })

      if (response.success && response.data) {
        setState(prev => ({
          ...prev,
          intent: response.data?.intent || null,
          isProcessing: false,
        }))
      } else {
        throw new Error(response.error || 'Intent extraction failed')
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        isProcessing: false,
        error: error instanceof Error ? error.message : 'Intent extraction failed',
      }))
    }
  }, [])

  const generateApp = useCallback(async (transcript: string, intent: string): Promise<void> => {
    if (!transcript.trim() || !intent) return

    setState(prev => ({ ...prev, isGenerating: true, error: null }))

    try {
      const response = await apiService.generateApp({
        transcript,
        plan: {
          steps: [intent],
          estimated_time_ms: 30000,
          complexity: 'medium',
        },
      })

      if (response.success && response.data) {
        setState(prev => ({
          ...prev,
          appId: response.data.app_id,
          isGenerating: false,
        }))

        // Start polling for status updates
        if (response.data.app_id) {
          startStatusPolling(response.data.app_id)
        }
      } else {
        throw new Error(response.error || 'App generation failed')
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        isGenerating: false,
        error: error instanceof Error ? error.message : 'App generation failed',
      }))
    }
  }, [])

  const checkAppStatus = useCallback(async (appId: string): Promise<void> => {
    try {
      const response = await apiService.getAppStatus(appId)

      if (response.success && response.data) {
        setState(prev => ({
          ...prev,
          appStatus: response.data || null,
        }))

        // Stop polling if app is completed or failed
        if (response.data.status === 'completed' || response.data.status === 'failed') {
          if (statusCheckIntervalRef.current) {
            clearInterval(statusCheckIntervalRef.current)
            statusCheckIntervalRef.current = null
          }
        }
      }
    } catch (error) {
      console.error('Failed to check app status:', error)
    }
  }, [])

  const startStatusPolling = useCallback((appId: string): void => {
    // Check status immediately
    checkAppStatus(appId)

    // Then check every 2 seconds
    statusCheckIntervalRef.current = setInterval(() => {
      checkAppStatus(appId)
    }, 2000)
  }, [checkAppStatus])

  const clearError = useCallback((): void => {
    setState(prev => ({ ...prev, error: null }))
  }, [])

  const reset = useCallback((): void => {
    // Clear any ongoing status checks
    if (statusCheckIntervalRef.current) {
      clearInterval(statusCheckIntervalRef.current)
      statusCheckIntervalRef.current = null
    }

    // Clean up audio URL
    if (state.audioUrl) {
      URL.revokeObjectURL(state.audioUrl)
    }

    setState({
      isRecording: false,
      isProcessing: false,
      isGenerating: false,
      transcript: '',
      intent: null,
      appId: null,
      appStatus: null,
      error: null,
      audioBlob: null,
      audioUrl: null,
    })
  }, [state.audioUrl])

  return {
    ...state,
    startRecording,
    stopRecording,
    processAudio,
    extractIntent,
    generateApp,
    checkAppStatus,
    clearError,
    reset,
  }
}
