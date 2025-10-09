'use client'

import { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX, 
  Settings, 
  MessageSquare, 
  Brain, 
  Activity,
  CheckCircle,
  AlertTriangle,
  User,
  Bot,
  Play,
  Pause,
  RotateCcw,
  Trash2,
  Download,
  Upload
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { twoWayNLPVoiceService, VoiceMessage, ConversationContext } from '@/services/2way-nlp-voice-service'

interface VoiceConversationUIProps {
  onConversationStart?: () => void
  onConversationEnd?: () => void
  onSmartCodingAction?: (action: string, data: any) => void
  className?: string
}

export function VoiceConversationUI({
  onConversationStart,
  onConversationEnd,
  onSmartCodingAction,
  className = ''
}: VoiceConversationUIProps) {
  const [isConversationActive, setIsConversationActive] = useState(false)
  const [conversationState, setConversationState] = useState<string>('idle')
  const [messages, setMessages] = useState<VoiceMessage[]>([])
  const [conversationContext, setConversationContext] = useState<ConversationContext | null>(null)
  const [activeTab, setActiveTab] = useState('conversation')
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)
  const [availableVoices, setAvailableVoices] = useState<SpeechSynthesisVoice[]>([])
  const [selectedVoice, setSelectedVoice] = useState('default')
  const [speechSpeed, setSpeechSpeed] = useState(1.0)
  const [speechPitch, setSpeechPitch] = useState(1.0)
  const [language, setLanguage] = useState('en-US')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Initialize voice service callbacks
    twoWayNLPVoiceService.setCallbacks({
      onMessage: (message: VoiceMessage) => {
        setMessages(prev => [...prev, message])
        scrollToBottom()
      },
      onStateChange: (state: string) => {
        setConversationState(state)
      },
      onError: (error: Error) => {
        console.error('Voice conversation error:', error)
      }
    })

    // Load available voices
    const loadVoices = () => {
      const voices = twoWayNLPVoiceService.getAvailableVoices()
      setAvailableVoices(voices)
    }

    loadVoices()
    
    // Load voices when they become available
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.addEventListener('voiceschanged', loadVoices)
    }

    return () => {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.removeEventListener('voiceschanged', loadVoices)
      }
    }
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const startConversation = async () => {
    try {
      await twoWayNLPVoiceService.startConversation()
      setIsConversationActive(true)
      onConversationStart?.()
    } catch (error) {
      console.error('Failed to start conversation:', error)
    }
  }

  const stopConversation = () => {
    twoWayNLPVoiceService.stopConversation()
    setIsConversationActive(false)
    onConversationEnd?.()
  }

  const clearConversation = () => {
    twoWayNLPVoiceService.clearConversation()
    setMessages([])
  }

  const exportConversation = () => {
    const conversationData = {
      timestamp: new Date().toISOString(),
      messages: messages,
      context: conversationContext
    }
    
    const blob = new Blob([JSON.stringify(conversationData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `voice-conversation-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const handleSmartCodingAction = (message: VoiceMessage) => {
    if (message.smartCodingAction && message.entities) {
      onSmartCodingAction?.(message.smartCodingAction, {
        intent: message.intent,
        entities: message.entities,
        confidence: message.confidence
      })
    }
  }

  const getStateColor = (state: string) => {
    switch (state) {
      case 'listening': return 'text-green-600'
      case 'processing': return 'text-blue-600'
      case 'speaking': return 'text-purple-600'
      case 'idle': return 'text-gray-600'
      default: return 'text-gray-600'
    }
  }

  const getStateIcon = (state: string) => {
    switch (state) {
      case 'listening': return <Mic className="h-4 w-4 animate-pulse" />
      case 'processing': return <Activity className="h-4 w-4 animate-spin" />
      case 'speaking': return <Volume2 className="h-4 w-4" />
      case 'idle': return <MicOff className="h-4 w-4" />
      default: return <MicOff className="h-4 w-4" />
    }
  }

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Voice Conversation Header */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-purple-600" />
                <div>
                  <CardTitle className="text-lg">2-Way NLP Voice Conversation</CardTitle>
                  <CardDescription>
                    Natural conversation with Smart Coding AI through voice
                  </CardDescription>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Conversation State */}
              <Badge 
                variant="outline" 
                className={`flex items-center space-x-2 ${getStateColor(conversationState)}`}
              >
                {getStateIcon(conversationState)}
                <span className="capitalize">{conversationState}</span>
              </Badge>
              
              {/* Control Buttons */}
              <div className="flex items-center space-x-2">
                {!isConversationActive ? (
                  <Button 
                    onClick={startConversation}
                    className="flex items-center space-x-2"
                    disabled={conversationState === 'processing'}
                  >
                    <Mic className="h-4 w-4" />
                    <span>Start Conversation</span>
                  </Button>
                ) : (
                  <Button 
                    onClick={stopConversation}
                    variant="destructive"
                    className="flex items-center space-x-2"
                  >
                    <MicOff className="h-4 w-4" />
                    <span>Stop Conversation</span>
                  </Button>
                )}
                
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsSettingsOpen(!isSettingsOpen)}
                >
                  <Settings className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </CardHeader>
        
        {/* Settings Panel */}
        {isSettingsOpen && (
          <CardContent className="pt-0">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-medium">Voice</label>
                <select
                  value={selectedVoice}
                  onChange={(e) => {
                    setSelectedVoice(e.target.value)
                    twoWayNLPVoiceService.setVoice(e.target.value)
                  }}
                  className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md text-sm"
                >
                  <option value="default">Default</option>
                  {availableVoices.map((voice, index) => (
                    <option key={index} value={voice.name}>
                      {voice.name} ({voice.lang})
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="text-sm font-medium">Speed: {speechSpeed.toFixed(1)}x</label>
                <input
                  type="range"
                  min="0.1"
                  max="2.0"
                  step="0.1"
                  value={speechSpeed}
                  onChange={(e) => {
                    const speed = parseFloat(e.target.value)
                    setSpeechSpeed(speed)
                    twoWayNLPVoiceService.setSpeed(speed)
                  }}
                  className="w-full mt-1"
                />
              </div>
              
              <div>
                <label className="text-sm font-medium">Pitch: {speechPitch.toFixed(1)}x</label>
                <input
                  type="range"
                  min="0.1"
                  max="2.0"
                  step="0.1"
                  value={speechPitch}
                  onChange={(e) => {
                    const pitch = parseFloat(e.target.value)
                    setSpeechPitch(pitch)
                    twoWayNLPVoiceService.setPitch(pitch)
                  }}
                  className="w-full mt-1"
                />
              </div>
            </div>
          </CardContent>
        )}
      </Card>

      {/* Main Conversation Interface */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="conversation">Conversation</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
          <TabsTrigger value="context">Context</TabsTrigger>
        </TabsList>

        <TabsContent value="conversation" className="space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="h-5 w-5" />
                <span>Voice Conversation</span>
                <Badge variant="outline">{messages.length} messages</Badge>
              </CardTitle>
              <CardDescription>
                Real-time conversation with Smart Coding AI
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
              {messages.length === 0 ? (
                <div className="text-center py-8">
                  <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No conversation yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Start a conversation to begin talking with Smart Coding AI
                  </p>
                  <Button onClick={startConversation} disabled={isConversationActive}>
                    <Mic className="h-4 w-4 mr-2" />
                    Start Conversation
                  </Button>
                </div>
              ) : (
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  <AnimatePresence>
                    {messages.map((message) => (
                      <motion.div
                        key={message.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ delay: 0.1 }}
                      >
                        <div className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                          <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                            message.type === 'user' 
                              ? 'bg-blue-500 text-white' 
                              : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
                          }`}>
                            <div className="flex items-center space-x-2 mb-1">
                              {message.type === 'user' ? (
                                <User className="h-4 w-4" />
                              ) : (
                                <Bot className="h-4 w-4" />
                              )}
                              <span className="text-xs opacity-75">
                                {formatTimestamp(message.timestamp)}
                              </span>
                              {message.confidence && (
                                <Badge variant="outline" className="text-xs">
                                  {Math.round(message.confidence * 100)}%
                                </Badge>
                              )}
                            </div>
                            <p className="text-sm">{message.content}</p>
                            {message.intent && (
                              <div className="mt-2 flex items-center space-x-2">
                                <Badge variant="outline" className="text-xs">
                                  {message.intent}
                                </Badge>
                                {message.smartCodingAction && (
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => handleSmartCodingAction(message)}
                                    className="text-xs"
                                  >
                                    Execute
                                  </Button>
                                )}
                              </div>
                            )}
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                  <div ref={messagesEndRef} />
                </div>
              )}
              
              {/* Conversation Controls */}
              {messages.length > 0 && (
                <div className="flex items-center justify-between pt-4 border-t">
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={clearConversation}
                      className="flex items-center space-x-2"
                    >
                      <Trash2 className="h-4 w-4" />
                      <span>Clear</span>
                    </Button>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={exportConversation}
                      className="flex items-center space-x-2"
                    >
                      <Download className="h-4 w-4" />
                      <span>Export</span>
                    </Button>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline" className="flex items-center space-x-1">
                      <Activity className="h-3 w-3" />
                      <span>{messages.filter(m => m.type === 'user').length} user</span>
                    </Badge>
                    <Badge variant="outline" className="flex items-center space-x-1">
                      <Bot className="h-3 w-3" />
                      <span>{messages.filter(m => m.type === 'ai').length} AI</span>
                    </Badge>
                  </div>
                </div>
              )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="history" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity className="h-5 w-5" />
                <span>Conversation History</span>
              </CardTitle>
              <CardDescription>
                Detailed conversation history and analytics
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
                {messages.length === 0 ? (
                  <div className="text-center py-8">
                    <Activity className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                      No conversation history
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400">
                      Start a conversation to see history here
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {messages.map((message, index) => (
                      <motion.div
                        key={message.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.05 }}
                      >
                        <Card className="hover:shadow-md transition-shadow">
                          <CardContent className="p-4">
                            <div className="flex items-start justify-between">
                              <div className="flex items-center space-x-3">
                                {message.type === 'user' ? (
                                  <User className="h-5 w-5 text-blue-500" />
                                ) : (
                                  <Bot className="h-5 w-5 text-purple-500" />
                                )}
                                <div>
                                  <p className="text-sm font-medium">
                                    {message.type === 'user' ? 'You' : 'Smart Coding AI'}
                                  </p>
                                  <p className="text-xs text-gray-500">
                                    {formatTimestamp(message.timestamp)}
                                  </p>
                                </div>
                              </div>
                              
                              <div className="flex items-center space-x-2">
                                {message.confidence && (
                                  <Badge variant="outline" className="text-xs">
                                    {Math.round(message.confidence * 100)}% confidence
                                  </Badge>
                                )}
                                {message.intent && (
                                  <Badge variant="outline" className="text-xs">
                                    {message.intent}
                                  </Badge>
                                )}
                              </div>
                            </div>
                            
                            <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
                              {message.content}
                            </p>
                            
                            {message.smartCodingAction && (
                              <div className="mt-2 flex items-center space-x-2">
                                <Badge variant="outline" className="text-xs">
                                  Action: {message.smartCodingAction}
                                </Badge>
                                <Button
                                  size="sm"
                                  variant="outline"
                                  onClick={() => handleSmartCodingAction(message)}
                                  className="text-xs"
                                >
                                  Execute Action
                                </Button>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      </motion.div>
                    ))}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="context" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5" />
                <span>Conversation Context</span>
              </CardTitle>
              <CardDescription>
                Current conversation context and Smart Coding AI state
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {!conversationContext ? (
                <div className="text-center py-8">
                  <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No active context
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Start a conversation to see context information
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm">Current Intent</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <Badge variant="outline" className="capitalize">
                          {conversationContext.currentIntent}
                        </Badge>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm">Conversation State</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <Badge variant="outline" className="capitalize">
                          {conversationContext.conversationState}
                        </Badge>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm">Active Components</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="flex flex-wrap gap-1">
                          {conversationContext.smartCodingContext.activeComponents.map((component, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {component}
                            </Badge>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm">Last Action</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {conversationContext.smartCodingContext.lastAction || 'None'}
                        </p>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
