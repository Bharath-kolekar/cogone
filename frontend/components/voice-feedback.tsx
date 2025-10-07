/**
 * Voice Feedback Component
 * Provides audio feedback for voice commands and actions
 */

'use client'

import { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { Slider } from '@/components/ui/slider'
import { 
  Volume2, 
  VolumeX, 
  Play, 
  Pause, 
  RotateCcw,
  Settings,
  CheckCircle,
  AlertCircle,
  Info
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

interface VoiceFeedbackProps {
  enabled?: boolean
  onToggle?: (enabled: boolean) => void
  onSettingsChange?: (settings: VoiceFeedbackSettings) => void
}

interface VoiceFeedbackSettings {
  enabled: boolean
  volume: number
  rate: number
  pitch: number
  voice: string
  confirmCommands: boolean
  confirmErrors: boolean
  confirmSuccess: boolean
}

const defaultSettings: VoiceFeedbackSettings = {
  enabled: true,
  volume: 0.8,
  rate: 0.9,
  pitch: 1.0,
  voice: 'default',
  confirmCommands: true,
  confirmErrors: true,
  confirmSuccess: true
}

export function VoiceFeedback({ 
  enabled = true, 
  onToggle,
  onSettingsChange 
}: VoiceFeedbackProps) {
  const [settings, setSettings] = useState<VoiceFeedbackSettings>(defaultSettings)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [availableVoices, setAvailableVoices] = useState<SpeechSynthesisVoice[]>([])
  const [lastCommand, setLastCommand] = useState<string | null>(null)
  const [feedbackHistory, setFeedbackHistory] = useState<Array<{
    id: string
    type: 'command' | 'success' | 'error' | 'info'
    message: string
    timestamp: Date
  }>>([])

  const speechSynthesisRef = useRef<SpeechSynthesisUtterance | null>(null)

  useEffect(() => {
    // Load available voices
    const loadVoices = () => {
      const voices = speechSynthesis.getVoices()
      setAvailableVoices(voices)
    }

    loadVoices()
    speechSynthesis.addEventListener('voiceschanged', loadVoices)

    // Listen for voice command events
    const handleVoiceCommand = (event: CustomEvent) => {
      const { action, params } = event.detail
      speakCommandConfirmation(action, params)
    }

    window.addEventListener('voice-command', handleVoiceCommand as EventListener)

    return () => {
      speechSynthesis.removeEventListener('voiceschanged', loadVoices)
      window.removeEventListener('voice-command', handleVoiceCommand as EventListener)
    }
  }, [])

  const speak = (text: string, options?: Partial<VoiceFeedbackSettings>) => {
    if (!settings.enabled || !text.trim()) return

    // Cancel any ongoing speech
    speechSynthesis.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.volume = options?.volume ?? settings.volume
    utterance.rate = options?.rate ?? settings.rate
    utterance.pitch = options?.pitch ?? settings.pitch

    if (options?.voice || settings.voice !== 'default') {
      const voice = availableVoices.find(v => v.name === (options?.voice || settings.voice))
      if (voice) {
        utterance.voice = voice
      }
    }

    utterance.onstart = () => setIsSpeaking(true)
    utterance.onend = () => setIsSpeaking(false)
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event.error)
      setIsSpeaking(false)
    }

    speechSynthesisRef.current = utterance
    speechSynthesis.speak(utterance)
  }

  const speakCommandConfirmation = (command: string, params?: string) => {
    if (!settings.confirmCommands) return

    const message = params ? `Executed ${command}: ${params}` : `Executed ${command}`
    speak(message)
    
    setLastCommand(command)
    addToHistory('command', message)
  }

  const speakSuccess = (message: string) => {
    if (!settings.confirmSuccess) return

    speak(`Success: ${message}`)
    addToHistory('success', message)
  }

  const speakError = (message: string) => {
    if (!settings.confirmErrors) return

    speak(`Error: ${message}`)
    addToHistory('error', message)
  }

  const speakInfo = (message: string) => {
    speak(message)
    addToHistory('info', message)
  }

  const addToHistory = (type: 'command' | 'success' | 'error' | 'info', message: string) => {
    const entry = {
      id: Date.now().toString(),
      type,
      message,
      timestamp: new Date()
    }
    
    setFeedbackHistory(prev => [entry, ...prev.slice(0, 9)]) // Keep last 10 entries
  }

  const stopSpeaking = () => {
    speechSynthesis.cancel()
    setIsSpeaking(false)
  }

  const testVoice = () => {
    speak("This is a test of the voice feedback system. How does it sound?")
  }

  const handleSettingsChange = (newSettings: Partial<VoiceFeedbackSettings>) => {
    const updatedSettings = { ...settings, ...newSettings }
    setSettings(updatedSettings)
    onSettingsChange?.(updatedSettings)
  }

  const getFeedbackIcon = (type: string) => {
    switch (type) {
      case 'command': return <Play className="h-4 w-4 text-blue-600" />
      case 'success': return <CheckCircle className="h-4 w-4 text-green-600" />
      case 'error': return <AlertCircle className="h-4 w-4 text-red-600" />
      case 'info': return <Info className="h-4 w-4 text-gray-600" />
      default: return <Volume2 className="h-4 w-4" />
    }
  }

  const getFeedbackColor = (type: string) => {
    switch (type) {
      case 'command': return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800'
      case 'success': return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
      case 'error': return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
      case 'info': return 'bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800'
      default: return 'bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800'
    }
  }

  return (
    <div className="space-y-4">
      {/* Voice Feedback Controls */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <Volume2 className="h-5 w-5" />
              <span>Voice Feedback</span>
            </CardTitle>
            
            <div className="flex items-center space-x-2">
              <Switch
                checked={settings.enabled}
                onCheckedChange={(enabled) => handleSettingsChange({ enabled })}
              />
              {isSpeaking && (
                <Badge variant="outline" className="animate-pulse">
                  Speaking
                </Badge>
              )}
            </div>
          </div>
          <CardDescription>
            Audio feedback for voice commands and actions
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-4">
          {/* Quick Controls */}
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={testVoice}
              disabled={!settings.enabled}
            >
              <Play className="h-4 w-4 mr-2" />
              Test Voice
            </Button>
            
            <Button
              variant="outline"
              size="sm"
              onClick={stopSpeaking}
              disabled={!isSpeaking}
            >
              <Pause className="h-4 w-4 mr-2" />
              Stop
            </Button>
            
            <Button
              variant="outline"
              size="sm"
              onClick={() => speakInfo("Voice feedback system is working correctly")}
            >
              <Info className="h-4 w-4 mr-2" />
              Info
            </Button>
          </div>

          {/* Voice Settings */}
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Volume</label>
              <Slider
                value={[settings.volume]}
                onValueChange={([value]) => handleSettingsChange({ volume: value })}
                max={1}
                min={0}
                step={0.1}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>0%</span>
                <span>{Math.round(settings.volume * 100)}%</span>
                <span>100%</span>
              </div>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Speech Rate</label>
              <Slider
                value={[settings.rate]}
                onValueChange={([value]) => handleSettingsChange({ rate: value })}
                max={2}
                min={0.1}
                step={0.1}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Slow</span>
                <span>{settings.rate}x</span>
                <span>Fast</span>
              </div>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Voice</label>
              <select
                value={settings.voice}
                onChange={(e) => handleSettingsChange({ voice: e.target.value })}
                className="w-full text-sm border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-800"
              >
                <option value="default">Default</option>
                {availableVoices.map((voice, index) => (
                  <option key={index} value={voice.name}>
                    {voice.name} ({voice.lang})
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Feedback Options */}
          <div className="space-y-3">
            <h4 className="text-sm font-medium">Feedback Options</h4>
            
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm">Confirm Commands</label>
                <p className="text-xs text-gray-500">Speak when commands are executed</p>
              </div>
              <Switch
                checked={settings.confirmCommands}
                onCheckedChange={(enabled) => handleSettingsChange({ confirmCommands: enabled })}
              />
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm">Confirm Success</label>
                <p className="text-xs text-gray-500">Speak when actions succeed</p>
              </div>
              <Switch
                checked={settings.confirmSuccess}
                onCheckedChange={(enabled) => handleSettingsChange({ confirmSuccess: enabled })}
              />
            </div>
            
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm">Confirm Errors</label>
                <p className="text-xs text-gray-500">Speak when errors occur</p>
              </div>
              <Switch
                checked={settings.confirmErrors}
                onCheckedChange={(enabled) => handleSettingsChange({ confirmErrors: enabled })}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Feedback History */}
      {feedbackHistory.length > 0 && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm">Recent Feedback</CardTitle>
            <CardDescription>
              Last voice feedback messages
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {feedbackHistory.map((entry) => (
                <motion.div
                  key={entry.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`p-2 rounded border ${getFeedbackColor(entry.type)}`}
                >
                  <div className="flex items-center space-x-2">
                    {getFeedbackIcon(entry.type)}
                    <span className="text-sm flex-1">{entry.message}</span>
                    <span className="text-xs text-gray-500">
                      {entry.timestamp.toLocaleTimeString()}
                    </span>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
