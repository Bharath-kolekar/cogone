/**
 * Voice Conversation Page
 * 2-way NLP voice conversation with Smart Coding AI
 */

'use client'

import { useState, useEffect } from 'react'
import { useAuthContext } from '@/contexts/AuthContext'
import { Navigation } from '@/components/navigation'
import { VoiceConversationUI } from '@/components/voice-conversation-ui'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Brain, Mic, Volume2, AlertCircle, CheckCircle } from 'lucide-react'
import { motion } from 'framer-motion'

export default function VoiceConversationPage() {
  const { isAuthenticated, isLoading } = useAuthContext()
  const [isInitialized, setIsInitialized] = useState(false)
  const [initializationError, setInitializationError] = useState<string | null>(null)
  const [conversationStats, setConversationStats] = useState({
    totalMessages: 0,
    userMessages: 0,
    aiMessages: 0,
    averageConfidence: 0,
    activeComponents: 0
  })

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      window.location.href = '/auth'
    }
  }, [isAuthenticated, isLoading])

  useEffect(() => {
    // Initialize voice conversation system
    if (isAuthenticated && !isInitialized) {
      try {
        // Check for speech recognition and synthesis support
        if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
          setInitializationError('Speech recognition not supported in this browser')
          return
        }

        if (!('speechSynthesis' in window)) {
          setInitializationError('Speech synthesis not supported in this browser')
          return
        }

        setIsInitialized(true)
        setInitializationError(null)
      } catch (error) {
        console.error('Failed to initialize voice conversation system:', error)
        setInitializationError('Failed to initialize voice conversation system')
      }
    }
  }, [isAuthenticated, isInitialized])

  const handleConversationStart = () => {
    console.log('Voice conversation started')
    // Update stats when conversation starts
  }

  const handleConversationEnd = () => {
    console.log('Voice conversation ended')
    // Update stats when conversation ends
  }

  const handleSmartCodingAction = (action: string, data: any) => {
    console.log('Smart Coding Action triggered:', action, data)
    // Handle Smart Coding AI actions from voice conversation
    // This could trigger integrations, analysis, optimizations, etc.
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex items-center space-x-3">
          <Brain className="h-6 w-6 animate-pulse text-purple-600" />
          <p className="text-lg">Loading Voice Conversation...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="p-6">
            <div className="text-center">
              <AlertCircle className="h-12 w-12 text-red-600 mx-auto mb-4" />
              <h2 className="text-xl font-semibold mb-2">Authentication Required</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Please log in to access the Voice Conversation feature.
              </p>
              <Button onClick={() => window.location.href = '/auth'}>
                Go to Login
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (initializationError) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="p-6">
            <div className="text-center">
              <AlertCircle className="h-12 w-12 text-red-600 mx-auto mb-4" />
              <h2 className="text-xl font-semibold mb-2">Initialization Error</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {initializationError}
              </p>
              <div className="space-y-2">
                <p className="text-sm text-gray-500">
                  Voice conversation requires:
                </p>
                <ul className="text-sm text-gray-500 text-left">
                  <li>• Speech Recognition API support</li>
                  <li>• Speech Synthesis API support</li>
                  <li>• Microphone permissions</li>
                  <li>• HTTPS connection (for production)</li>
                </ul>
              </div>
              <Button onClick={() => window.location.reload()} className="mt-4">
                Retry
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!isInitialized) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="p-6">
            <div className="text-center">
              <div className="flex items-center justify-center mb-4">
                <Brain className="h-12 w-12 text-purple-600 animate-pulse" />
              </div>
              <h2 className="text-xl font-semibold mb-2">Initializing Voice Conversation</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Setting up 2-way NLP voice communication with Smart Coding AI...
              </p>
              <div className="flex items-center justify-center space-x-2">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-purple-600 border-t-transparent" />
                <span className="text-sm">Please wait...</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Navigation />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Page Header */}
          <div className="mb-8">
            <div className="flex items-center space-x-3 mb-4">
              <div className="flex items-center space-x-2">
                <Brain className="h-8 w-8 text-purple-600" />
                <Mic className="h-6 w-6 text-blue-600" />
                <Volume2 className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h1 className="text-3xl font-bold">Voice Conversation</h1>
                <p className="text-gray-600 dark:text-gray-400">
                  2-way NLP voice communication with Smart Coding AI
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Voice Ready</span>
              </Badge>
              
              <Badge variant="outline" className="flex items-center space-x-2">
                <Brain className="h-4 w-4 text-purple-500" />
                <span>NLP Enhanced</span>
              </Badge>
              
              <Badge variant="outline" className="flex items-center space-x-2">
                <Mic className="h-4 w-4 text-blue-500" />
                <span>2-Way Communication</span>
              </Badge>
            </div>
          </div>

          {/* Voice Conversation Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <Card className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border-purple-200 dark:border-purple-800">
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center space-x-2 text-purple-800 dark:text-purple-200">
                  <Brain className="h-5 w-5" />
                  <span>Voice Conversation Stats</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {conversationStats.totalMessages}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Total Messages
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {conversationStats.userMessages}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      User Messages
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {conversationStats.aiMessages}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      AI Responses
                    </p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">
                      {Math.round(conversationStats.averageConfidence * 100)}%
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Avg Confidence
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Voice Conversation Interface */}
          <VoiceConversationUI
            onConversationStart={handleConversationStart}
            onConversationEnd={handleConversationEnd}
            onSmartCodingAction={handleSmartCodingAction}
          />
        </motion.div>
      </main>
    </div>
  )
}
