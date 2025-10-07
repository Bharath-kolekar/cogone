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
  Upload,
  Heart,
  Smile,
  Zap,
  Lightbulb,
  Target,
  BookOpen,
  TrendingUp,
  Users,
  Star
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { humanLikeVoiceNLPService, HumanLikeResponse, EmotionalState, Personality, Memory, LearningData } from '@/services/human-like-voice-nlp'

interface HumanLikeVoiceUIProps {
  onConversationStart?: () => void
  onConversationEnd?: () => void
  onSmartCodingAction?: (action: string, data: any) => void
  className?: string
}

export function HumanLikeVoiceUI({
  onConversationStart,
  onConversationEnd,
  onSmartCodingAction,
  className = ''
}: HumanLikeVoiceUIProps) {
  const [isConversationActive, setIsConversationActive] = useState(false)
  const [conversationState, setConversationState] = useState<string>('idle')
  const [messages, setMessages] = useState<Array<{
    id: string
    type: 'user' | 'ai'
    content: string
    timestamp: Date
    emotionalState?: EmotionalState
    personality?: Personality
    humanLikeFeatures?: any
  }>>([])
  const [aiPersonality, setAiPersonality] = useState<Personality | null>(null)
  const [aiEmotionalState, setAiEmotionalState] = useState<EmotionalState | null>(null)
  const [activeTab, setActiveTab] = useState('conversation')
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)
  const [availableVoices, setAvailableVoices] = useState<SpeechSynthesisVoice[]>([])
  const [selectedVoice, setSelectedVoice] = useState('default')
  const [speechSpeed, setSpeechSpeed] = useState(1.0)
  const [speechPitch, setSpeechPitch] = useState(1.0)
  const [language, setLanguage] = useState('en-US')
  const [showEmotionalAnalysis, setShowEmotionalAnalysis] = useState(true)
  const [showPersonalityTraits, setShowPersonalityTraits] = useState(true)
  const [showLearningInsights, setShowLearningInsights] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Initialize human-like voice service
    const initializeService = async () => {
      try {
        // Load AI personality and emotional state
        const personality = humanLikeVoiceNLPService.getPersonality()
        const emotionalState = humanLikeVoiceNLPService.getEmotionalState()
        
        setAiPersonality(personality)
        setAiEmotionalState(emotionalState)
        
        // Load available voices
        const loadVoices = () => {
          if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
            const voices = window.speechSynthesis.getVoices()
            setAvailableVoices(voices)
          }
        }

        loadVoices()
        
        if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
          window.speechSynthesis.addEventListener('voiceschanged', loadVoices)
        }

        return () => {
          if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
            window.speechSynthesis.removeEventListener('voiceschanged', loadVoices)
          }
        }
      } catch (error) {
        console.error('Failed to initialize human-like voice service:', error)
      }
    }

    initializeService()
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const startConversation = async () => {
    try {
      setIsConversationActive(true)
      onConversationStart?.()
      
      // Send initial greeting with human-like response
      const greetingResponse = await humanLikeVoiceNLPService.processHumanLikeInput("Hello")
      await handleAIResponse(greetingResponse)
    } catch (error) {
      console.error('Failed to start conversation:', error)
    }
  }

  const stopConversation = () => {
    setIsConversationActive(false)
    onConversationEnd?.()
  }

  const processUserInput = async (userInput: string, voiceData?: any) => {
    try {
      // Add user message
      const userMessage = {
        id: `user_${Date.now()}`,
        type: 'user' as const,
        content: userInput,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, userMessage])
      
      // Process with human-like NLP
      const humanLikeResponse = await humanLikeVoiceNLPService.processHumanLikeInput(userInput, voiceData)
      
      // Update AI state
      setAiEmotionalState(humanLikeResponse.emotionalTone)
      setAiPersonality(humanLikeResponse.personality)
      
      // Handle AI response
      await handleAIResponse(humanLikeResponse)
      
    } catch (error) {
      console.error('Error processing user input:', error)
    }
  }

  const handleAIResponse = async (response: HumanLikeResponse) => {
    // Add AI message
    const aiMessage = {
      id: `ai_${Date.now()}`,
      type: 'ai' as const,
      content: response.content,
      timestamp: new Date(),
      emotionalState: response.emotionalTone,
      personality: response.personality,
      humanLikeFeatures: response.naturalLanguageFeatures
    }
    setMessages(prev => [...prev, aiMessage])
    
    // Speak the response with human-like characteristics
    await speakWithHumanLikeCharacteristics(response)
  }

  const speakWithHumanLikeCharacteristics = async (response: HumanLikeResponse): Promise<void> => {
    if (!('speechSynthesis' in window)) return

    return new Promise((resolve, reject) => {
      try {
        const utterance = new SpeechSynthesisUtterance(response.content)
        
        // Apply human-like voice characteristics
        utterance.rate = response.voiceCharacteristics.speed
        utterance.pitch = response.voiceCharacteristics.pitch
        utterance.volume = response.voiceCharacteristics.volume
        
        // Add pauses for natural speech
        if (response.voiceCharacteristics.pauses.length > 0) {
          // This would require more complex implementation for actual pauses
          // For now, we'll adjust the rate to simulate pauses
          utterance.rate *= 0.9
        }
        
        utterance.onend = () => resolve()
        utterance.onerror = (event) => reject(new Error(`Speech synthesis error: ${event.error}`))
        
        window.speechSynthesis.speak(utterance)
      } catch (error) {
        reject(error)
      }
    })
  }

  const clearConversation = () => {
    setMessages([])
    humanLikeVoiceNLPService.clearMemory()
  }

  const exportConversation = () => {
    const conversationData = {
      timestamp: new Date().toISOString(),
      messages: messages,
      aiPersonality: aiPersonality,
      aiEmotionalState: aiEmotionalState,
      humanLikeFeatures: {
        memory: humanLikeVoiceNLPService.getMemory(),
        learning: humanLikeVoiceNLPService.getLearningData()
      }
    }
    
    const blob = new Blob([JSON.stringify(conversationData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `human-like-conversation-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const getEmotionalColor = (emotion: number) => {
    if (emotion > 0.7) return 'text-green-600'
    if (emotion > 0.4) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getEmotionalIcon = (emotion: string, value: number) => {
    if (value > 0.7) {
      switch (emotion) {
        case 'happiness': return <Smile className="h-4 w-4 text-green-500" />
        case 'excitement': return <Zap className="h-4 w-4 text-yellow-500" />
        case 'empathy': return <Heart className="h-4 w-4 text-pink-500" />
        case 'confidence': return <Target className="h-4 w-4 text-blue-500" />
        case 'curiosity': return <Lightbulb className="h-4 w-4 text-purple-500" />
        case 'stress': return <AlertTriangle className="h-4 w-4 text-red-500" />
      }
    }
    return <Activity className="h-4 w-4 text-gray-500" />
  }

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Human-Like Voice Header */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-purple-600" />
                <Heart className="h-5 w-5 text-pink-500" />
                <Smile className="h-5 w-5 text-yellow-500" />
              </div>
              <div>
                <CardTitle className="text-lg">Human-Like Voice Conversation</CardTitle>
                <CardDescription>
                  Natural conversation with emotional intelligence and personality
                </CardDescription>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* AI Emotional State */}
              {aiEmotionalState && (
                <div className="flex items-center space-x-2">
                  <Badge variant="outline" className="flex items-center space-x-1">
                    <Heart className="h-3 w-3" />
                    <span>Empathy: {Math.round(aiEmotionalState.empathy * 100)}%</span>
                  </Badge>
                  <Badge variant="outline" className="flex items-center space-x-1">
                    <Smile className="h-3 w-3" />
                    <span>Happiness: {Math.round(aiEmotionalState.happiness * 100)}%</span>
                  </Badge>
                </div>
              )}
              
              {/* Control Buttons */}
              <div className="flex items-center space-x-2">
                {!isConversationActive ? (
                  <Button 
                    onClick={startConversation}
                    className="flex items-center space-x-2"
                    disabled={conversationState === 'processing'}
                  >
                    <Mic className="h-4 w-4" />
                    <span>Start Human-Like Chat</span>
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
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">Voice</label>
                <select
                  value={selectedVoice}
                  onChange={(e) => setSelectedVoice(e.target.value)}
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
                  onChange={(e) => setSpeechSpeed(parseFloat(e.target.value))}
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
                  onChange={(e) => setSpeechPitch(parseFloat(e.target.value))}
                  className="w-full mt-1"
                />
              </div>
              
              <div className="flex items-center space-x-4">
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={showEmotionalAnalysis}
                    onChange={(e) => setShowEmotionalAnalysis(e.target.checked)}
                  />
                  <span className="text-sm">Show Emotional Analysis</span>
                </label>
                
                <label className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={showPersonalityTraits}
                    onChange={(e) => setShowPersonalityTraits(e.target.checked)}
                  />
                  <span className="text-sm">Show Personality Traits</span>
                </label>
              </div>
            </div>
          </CardContent>
        )}
      </Card>

      {/* Main Conversation Interface */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="conversation">Conversation</TabsTrigger>
          <TabsTrigger value="emotions">Emotions</TabsTrigger>
          <TabsTrigger value="personality">Personality</TabsTrigger>
          <TabsTrigger value="learning">Learning</TabsTrigger>
        </TabsList>

        <TabsContent value="conversation" className="space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="h-5 w-5" />
                <span>Human-Like Conversation</span>
                <Badge variant="outline">{messages.length} messages</Badge>
              </CardTitle>
              <CardDescription>
                Natural conversation with emotional intelligence and personality
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
              {messages.length === 0 ? (
                <div className="text-center py-8">
                  <div className="flex items-center justify-center space-x-2 mb-4">
                    <Brain className="h-12 w-12 text-purple-600" />
                    <Heart className="h-10 w-10 text-pink-500" />
                    <Smile className="h-8 w-8 text-yellow-500" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No conversation yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Start a human-like conversation with emotional intelligence and personality
                  </p>
                  <Button onClick={startConversation} disabled={isConversationActive}>
                    <Mic className="h-4 w-4 mr-2" />
                    Start Human-Like Chat
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
                            </div>
                            <p className="text-sm">{message.content}</p>
                            
                            {/* Human-like features for AI messages */}
                            {message.type === 'ai' && message.humanLikeFeatures && (
                              <div className="mt-2 space-y-1">
                                {message.humanLikeFeatures.emphasis.length > 0 && (
                                  <div className="flex flex-wrap gap-1">
                                    {message.humanLikeFeatures.emphasis.map((word: string, index: number) => (
                                      <Badge key={index} variant="outline" className="text-xs">
                                        {word}
                                      </Badge>
                                    ))}
                                  </div>
                                )}
                                
                                {message.humanLikeFeatures.questions.length > 0 && (
                                  <div className="text-xs text-gray-500">
                                    <Lightbulb className="h-3 w-3 inline mr-1" />
                                    {message.humanLikeFeatures.questions.length} question(s)
                                  </div>
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
                      <User className="h-3 w-3" />
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

        <TabsContent value="emotions" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Heart className="h-5 w-5" />
                <span>Emotional Intelligence</span>
              </CardTitle>
              <CardDescription>
                AI emotional state and user emotional analysis
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {!aiEmotionalState ? (
                <div className="text-center py-8">
                  <Heart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No emotional data yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Start a conversation to see emotional intelligence in action
                  </p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* AI Emotional State */}
                  <div>
                    <h4 className="font-semibold mb-3 flex items-center space-x-2">
                      <Bot className="h-4 w-4" />
                      <span>AI Emotional State</span>
                    </h4>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      {Object.entries(aiEmotionalState).map(([emotion, value]) => (
                        <Card key={emotion}>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center space-x-2">
                                {getEmotionalIcon(emotion, value)}
                                <span className="text-sm font-medium capitalize">{emotion}</span>
                              </div>
                              <span className={`text-sm font-bold ${getEmotionalColor(value)}`}>
                                {Math.round(value * 100)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${value * 100}%` }}
                              />
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="personality" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Star className="h-5 w-5" />
                <span>AI Personality</span>
              </CardTitle>
              <CardDescription>
                AI personality traits and communication style
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {!aiPersonality ? (
                <div className="text-center py-8">
                  <Star className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No personality data yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Start a conversation to see personality traits in action
                  </p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Personality Traits */}
                  <div>
                    <h4 className="font-semibold mb-3">Personality Traits</h4>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                      {Object.entries(aiPersonality.traits).map(([trait, value]) => (
                        <Card key={trait}>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-medium capitalize">{trait}</span>
                              <span className="text-sm font-bold text-blue-600">
                                {Math.round(value * 100)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-green-500 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${value * 100}%` }}
                              />
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                  
                  {/* Communication Style */}
                  <div>
                    <h4 className="font-semibold mb-3">Communication Style</h4>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      {Object.entries(aiPersonality.communicationStyle).map(([style, value]) => (
                        <Card key={style}>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-medium capitalize">{style}</span>
                              <span className="text-sm font-bold text-purple-600">
                                {Math.round(value * 100)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${value * 100}%` }}
                              />
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="learning" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="h-5 w-5" />
                <span>Learning & Memory</span>
              </CardTitle>
              <CardDescription>
                AI learning progress and memory insights
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-6">
                {/* Learning Statistics */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-blue-600">
                        {humanLikeVoiceNLPService.getMemory().length}
                      </div>
                      <p className="text-sm text-gray-600">Memories</p>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-green-600">
                        {humanLikeVoiceNLPService.getLearningData().successfulInteractions.length}
                      </div>
                      <p className="text-sm text-gray-600">Successful Interactions</p>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-orange-600">
                        {Object.keys(humanLikeVoiceNLPService.getLearningData().conversationPatterns).length}
                      </div>
                      <p className="text-sm text-gray-600">Patterns Learned</p>
                    </CardContent>
                  </Card>
                  
                  <Card>
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-purple-600">
                        {Object.keys(humanLikeVoiceNLPService.getLearningData().userPreferences).length}
                      </div>
                      <p className="text-sm text-gray-600">User Preferences</p>
                    </CardContent>
                  </Card>
                </div>
                
                {/* Recent Memories */}
                <div>
                  <h4 className="font-semibold mb-3">Recent Memories</h4>
                  <div className="space-y-2">
                    {humanLikeVoiceNLPService.getMemory().slice(0, 5).map((memory) => (
                      <Card key={memory.id}>
                        <CardContent className="p-3">
                          <div className="flex items-center justify-between">
                            <span className="text-sm">{memory.content}</span>
                            <Badge variant="outline" className="text-xs">
                              {Math.round(memory.importance * 100)}% important
                            </Badge>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
