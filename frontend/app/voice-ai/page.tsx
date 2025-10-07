/**
 * Voice AI Dashboard Page
 * Comprehensive control over AI systems through voice commands
 */

'use client'

import { useState, useEffect } from 'react'
import { useAuthContext } from '@/contexts/AuthContext'
import { Navigation } from '@/components/navigation'
import { VoiceAIDashboard } from '@/components/voice-ai-dashboard'
import { useVoiceDictation } from '@/hooks/useVoiceDictation'
import { initializeVoiceCommandMapper } from '@/services/voice-command-mapper'
import { initializeVoiceAIIntegration } from '@/services/voice-ai-integration'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Brain, Activity, AlertCircle } from 'lucide-react'
import { motion } from 'framer-motion'

export default function VoiceAIPage() {
  const { isAuthenticated, isLoading } = useAuthContext()
  const [isInitialized, setIsInitialized] = useState(false)
  const [initializationError, setInitializationError] = useState<string | null>(null)

  const voiceDictation = useVoiceDictation()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      window.location.href = '/auth'
    }
  }, [isAuthenticated, isLoading])

  useEffect(() => {
    if (voiceDictation.isSupported && !isInitialized) {
      try {
        // Initialize voice command mapper
        const commandMapper = initializeVoiceCommandMapper(voiceDictation)
        
        // Initialize voice AI integration
        initializeVoiceAIIntegration(voiceDictation, commandMapper)
        
        setIsInitialized(true)
        setInitializationError(null)
      } catch (error) {
        console.error('Failed to initialize voice AI system:', error)
        setInitializationError('Failed to initialize voice AI system')
      }
    }
  }, [voiceDictation.isSupported, isInitialized])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex items-center space-x-3">
          <Activity className="h-6 w-6 animate-spin text-blue-600" />
          <p className="text-lg">Loading Voice AI Dashboard...</p>
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
                Please log in to access the Voice AI Dashboard.
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

  if (!voiceDictation.isSupported) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="p-6">
            <div className="text-center">
              <AlertCircle className="h-12 w-12 text-red-600 mx-auto mb-4" />
              <h2 className="text-xl font-semibold mb-2">Voice Recognition Not Supported</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Your browser doesn't support voice recognition. Please use Chrome, Firefox, or Safari.
              </p>
              <Button onClick={() => window.location.href = '/editor'}>
                Go to Code Editor
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
              <Button onClick={() => window.location.reload()}>
                Retry
              </Button>
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
              <Brain className="h-8 w-8 text-purple-600" />
              <div>
                <h1 className="text-3xl font-bold">Voice AI Dashboard</h1>
                <p className="text-gray-600 dark:text-gray-400">
                  Control intelligence, smarty, and core DNA features through voice commands
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${voiceDictation.isListening ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`}></div>
                <span>
                  {voiceDictation.isListening ? 'Listening...' : 'Voice Ready'}
                </span>
              </Badge>
              
              <Badge variant="outline">
                {isInitialized ? 'AI Systems Active' : 'Initializing...'}
              </Badge>
            </div>
          </div>

          {/* Voice AI Dashboard */}
          <VoiceAIDashboard />
        </motion.div>
      </main>
    </div>
  )
}
