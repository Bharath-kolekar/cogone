/**
 * Voice Dictation Hook
 * Provides voice control for UI components
 */

import { useState, useEffect, useCallback, useRef } from 'react'

interface VoiceDictationState {
  isListening: boolean
  isSupported: boolean
  transcript: string
  isProcessing: boolean
  error: string | null
  confidence: number
}

interface VoiceDictationActions {
  startListening: () => void
  stopListening: () => void
  toggleListening: () => void
  clearTranscript: () => void
  processCommand: (command: string) => void
}

interface VoiceCommand {
  pattern: RegExp
  action: (params: string[]) => void
  description: string
}

export function useVoiceDictation(): VoiceDictationState & VoiceDictationActions {
  const [state, setState] = useState<VoiceDictationState>({
    isListening: false,
    isSupported: false,
    transcript: '',
    isProcessing: false,
    error: null,
    confidence: 0,
  })

  const recognitionRef = useRef<SpeechRecognition | null>(null)
  const commandsRef = useRef<VoiceCommand[]>([])

  // Check for browser support
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (SpeechRecognition) {
      setState(prev => ({ ...prev, isSupported: true }))
      initializeRecognition()
    } else {
      setState(prev => ({ 
        ...prev, 
        isSupported: false, 
        error: 'Speech recognition not supported in this browser' 
      }))
    }
  }, [])

  const initializeRecognition = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()
    
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = 'en-US'
    recognition.maxAlternatives = 1

    recognition.onstart = () => {
      setState(prev => ({ ...prev, isListening: true, error: null }))
    }

    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('')

      const confidence = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.confidence)
        .reduce((acc, conf) => acc + conf, 0) / event.results.length

      setState(prev => ({ 
        ...prev, 
        transcript, 
        confidence,
        isProcessing: event.results[event.results.length - 1].isFinal
      }))

      // Process final results
      if (event.results[event.results.length - 1].isFinal) {
        processVoiceCommand(transcript)
      }
    }

    recognition.onerror = (event) => {
      setState(prev => ({ 
        ...prev, 
        isListening: false, 
        error: `Speech recognition error: ${event.error}` 
      }))
    }

    recognition.onend = () => {
      setState(prev => ({ ...prev, isListening: false }))
    }

    recognitionRef.current = recognition
  }

  const processVoiceCommand = (command: string) => {
    const normalizedCommand = command.toLowerCase().trim()
    
    for (const voiceCommand of commandsRef.current) {
      const match = normalizedCommand.match(voiceCommand.pattern)
      if (match) {
        try {
          voiceCommand.action(match.slice(1))
          setState(prev => ({ ...prev, isProcessing: false }))
          return
        } catch (error) {
          console.error('Error executing voice command:', error)
          setState(prev => ({ 
            ...prev, 
            error: 'Failed to execute voice command',
            isProcessing: false 
          }))
        }
      }
    }

    // No command matched
    setState(prev => ({ 
      ...prev, 
      error: `Command not recognized: "${command}"`,
      isProcessing: false 
    }))
  }

  const startListening = useCallback(() => {
    if (recognitionRef.current && !state.isListening) {
      try {
        recognitionRef.current.start()
      } catch (error) {
        setState(prev => ({ 
          ...prev, 
          error: 'Failed to start voice recognition' 
        }))
      }
    }
  }, [state.isListening])

  const stopListening = useCallback(() => {
    if (recognitionRef.current && state.isListening) {
      recognitionRef.current.stop()
    }
  }, [state.isListening])

  const toggleListening = useCallback(() => {
    if (state.isListening) {
      stopListening()
    } else {
      startListening()
    }
  }, [state.isListening, startListening, stopListening])

  const clearTranscript = useCallback(() => {
    setState(prev => ({ ...prev, transcript: '', error: null }))
  }, [])

  const processCommand = useCallback((command: string) => {
    processVoiceCommand(command)
  }, [])

  // Register voice commands
  const registerCommand = useCallback((command: VoiceCommand) => {
    commandsRef.current.push(command)
  }, [])

  const unregisterCommand = useCallback((pattern: RegExp) => {
    commandsRef.current = commandsRef.current.filter(cmd => cmd.pattern !== pattern)
  }, [])

  return {
    ...state,
    startListening,
    stopListening,
    toggleListening,
    clearTranscript,
    processCommand,
    // Expose command registration for external use
    registerCommand,
    unregisterCommand,
  }
}
