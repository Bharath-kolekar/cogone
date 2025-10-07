/**
 * Voice Dictation Toggle Component
 * Provides UI control for voice dictation functionality
 */

'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Switch } from '@/components/ui/switch'
import { 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX, 
  Settings, 
  HelpCircle,
  CheckCircle,
  AlertCircle,
  Loader2
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useVoiceDictation } from '@/hooks/useVoiceDictation'

interface VoiceDictationToggleProps {
  onVoiceCommand?: (command: string) => void
  onToggle?: (enabled: boolean) => void
  showAdvanced?: boolean
  className?: string
}

export function VoiceDictationToggle({ 
  onVoiceCommand, 
  onToggle,
  showAdvanced = false,
  className = '' 
}: VoiceDictationToggleProps) {
  const [isEnabled, setIsEnabled] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  const [showHelp, setShowHelp] = useState(false)
  const [voiceFeedback, setVoiceFeedback] = useState(true)
  const [language, setLanguage] = useState('en-US')

  const {
    isListening,
    isSupported,
    transcript,
    isProcessing,
    error,
    confidence,
    startListening,
    stopListening,
    toggleListening,
    clearTranscript,
    processCommand
  } = useVoiceDictation()

  // Handle voice command processing
  useEffect(() => {
    if (transcript && isProcessing) {
      onVoiceCommand?.(transcript)
      processCommand(transcript)
    }
  }, [transcript, isProcessing, onVoiceCommand, processCommand])

  // Handle toggle changes
  useEffect(() => {
    onToggle?.(isEnabled)
  }, [isEnabled, onToggle])

  const handleToggle = () => {
    if (!isSupported) {
      return
    }

    setIsEnabled(!isEnabled)
    
    if (!isEnabled) {
      startListening()
    } else {
      stopListening()
    }
  }

  const handleClearTranscript = () => {
    clearTranscript()
  }

  const getStatusColor = () => {
    if (error) return 'text-red-600'
    if (isListening) return 'text-green-600'
    if (isProcessing) return 'text-blue-600'
    return 'text-gray-600'
  }

  const getStatusIcon = () => {
    if (error) return <AlertCircle className="h-4 w-4" />
    if (isListening) return <Mic className="h-4 w-4" />
    if (isProcessing) return <Loader2 className="h-4 w-4 animate-spin" />
    return <MicOff className="h-4 w-4" />
  }

  const getStatusText = () => {
    if (error) return 'Error'
    if (isListening) return 'Listening'
    if (isProcessing) return 'Processing'
    return 'Ready'
  }

  if (!isSupported) {
    return (
      <Card className={`border-red-200 dark:border-red-800 ${className}`}>
        <CardContent className="p-4">
          <div className="flex items-center space-x-3">
            <AlertCircle className="h-5 w-5 text-red-600" />
            <div>
              <p className="text-sm font-medium text-red-800 dark:text-red-200">
                Voice dictation not supported
              </p>
              <p className="text-xs text-red-600 dark:text-red-400">
                Please use Chrome, Firefox, or Safari
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Main Toggle */}
      <Card className="hover:shadow-md transition-shadow">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <Mic className="h-5 w-5" />
              <span>Voice Dictation</span>
            </CardTitle>
            
            <div className="flex items-center space-x-2">
              <Switch
                checked={isEnabled}
                onCheckedChange={handleToggle}
                disabled={!isSupported}
              />
              {showAdvanced && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowSettings(!showSettings)}
                >
                  <Settings className="h-4 w-4" />
                </Button>
              )}
            </div>
          </div>
          <CardDescription>
            Control the interface using voice commands
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          {/* Status Display */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className={`flex items-center space-x-2 ${getStatusColor()}`}>
                {getStatusIcon()}
              <span className="text-sm font-medium">
                {getStatusText()}
              </span>
            </div>
            
            {confidence > 0 && (
              <Badge variant="outline">
                {Math.round(confidence * 100)}% confidence
              </Badge>
            )}
          </div>

          {/* Transcript Display */}
          <AnimatePresence>
            {transcript && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-4"
              >
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      Voice Command:
                    </h4>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={handleClearTranscript}
                    >
                      Clear
                    </Button>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 italic">
                    "{transcript}"
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Error Display */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
              >
                <div className="flex items-center space-x-2">
                  <AlertCircle className="h-4 w-4 text-red-600" />
                  <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Quick Actions */}
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={toggleListening}
              disabled={!isSupported}
            >
              {isListening ? (
                <>
                  <MicOff className="h-4 w-4 mr-2" />
                  Stop
                </>
              ) : (
                <>
                  <Mic className="h-4 w-4 mr-2" />
                  Start
                </>
              )}
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowHelp(!showHelp)}
            >
              <HelpCircle className="h-4 w-4 mr-2" />
              Help
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Advanced Settings */}
      <AnimatePresence>
        {showSettings && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Voice Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Voice Feedback</label>
                    <p className="text-xs text-gray-500">Audio confirmation of commands</p>
                  </div>
                  <Switch
                    checked={voiceFeedback}
                    onCheckedChange={setVoiceFeedback}
                  />
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Language</label>
                    <p className="text-xs text-gray-500">Speech recognition language</p>
                  </div>
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="text-sm border border-gray-300 dark:border-gray-600 rounded px-2 py-1 bg-white dark:bg-gray-800"
                  >
                    <option value="en-US">English (US)</option>
                    <option value="en-GB">English (UK)</option>
                    <option value="es-ES">Spanish</option>
                    <option value="fr-FR">French</option>
                    <option value="de-DE">German</option>
                    <option value="it-IT">Italian</option>
                    <option value="pt-BR">Portuguese (Brazil)</option>
                    <option value="ru-RU">Russian</option>
                    <option value="ja-JP">Japanese</option>
                    <option value="ko-KR">Korean</option>
                    <option value="zh-CN">Chinese (Simplified)</option>
                    <option value="hi-IN">Hindi</option>
                  </select>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Help Panel */}
      <AnimatePresence>
        {showHelp && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="text-sm">Voice Commands</CardTitle>
                <CardDescription>
                  Common voice commands you can use
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="text-sm font-medium mb-2">Navigation</h4>
                    <ul className="space-y-1 text-xs text-gray-600 dark:text-gray-400">
                      <li>• "Go to dashboard"</li>
                      <li>• "Open editor"</li>
                      <li>• "Show settings"</li>
                      <li>• "Go back"</li>
                    </ul>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2">Code Editor</h4>
                    <ul className="space-y-1 text-xs text-gray-600 dark:text-gray-400">
                      <li>• "Save file"</li>
                      <li>• "New file"</li>
                      <li>• "Copy code"</li>
                      <li>• "Undo changes"</li>
                    </ul>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2">Voice Recording</h4>
                    <ul className="space-y-1 text-xs text-gray-600 dark:text-gray-400">
                      <li>• "Start recording"</li>
                      <li>• "Stop recording"</li>
                      <li>• "Generate app"</li>
                      <li>• "Process audio"</li>
                    </ul>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2">General</h4>
                    <ul className="space-y-1 text-xs text-gray-600 dark:text-gray-400">
                      <li>• "Help"</li>
                      <li>• "Clear"</li>
                      <li>• "Refresh"</li>
                      <li>• "Close"</li>
                    </ul>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
