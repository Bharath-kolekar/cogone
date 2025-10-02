'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Mic, MicOff, Play, Pause, Download } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { VoiceRecorder } from '@/components/voice-recorder'
import { LanguageToggle } from '@/components/language-toggle'

export function Hero() {
  const [isRecording, setIsRecording] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedApp, setGeneratedApp] = useState(null)

  const handleVoiceCommand = async (command: string) => {
    setTranscript(command)
    setIsGenerating(true)
    
    // Simulate app generation
    setTimeout(() => {
      setIsGenerating(false)
      setGeneratedApp({
        id: '1',
        title: 'Generated App',
        preview_url: 'https://example.com',
        status: 'completed'
      })
    }, 3000)
  }

  return (
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6"
          >
            Voice to App
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto"
          >
            Convert your voice commands into working apps in just 30 seconds. 
            Powered by AI, optimized for India.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8"
          >
            <LanguageToggle />
            <div className="text-sm text-gray-500">
              Available in Hindi, English, Tamil, Telugu & more
            </div>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="max-w-4xl mx-auto"
        >
          <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl font-bold text-gray-800 dark:text-gray-200">
                Try It Now - Free
              </CardTitle>
              <CardDescription className="text-lg text-gray-600 dark:text-gray-400">
                Speak your app idea and watch it come to life
              </CardDescription>
            </CardHeader>
            
            <CardContent className="space-y-6">
              <VoiceRecorder
                onTranscript={handleVoiceCommand}
                isRecording={isRecording}
                onRecordingChange={setIsRecording}
                disabled={isGenerating}
              />

              <AnimatePresence>
                {transcript && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4"
                  >
                    <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">
                      Your Command:
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 italic">
                      "{transcript}"
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>

              <AnimatePresence>
                {isGenerating && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    className="text-center py-8"
                  >
                    <div className="inline-flex items-center space-x-3">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                      <span className="text-lg font-medium text-gray-700 dark:text-gray-300">
                        Generating your app...
                      </span>
                    </div>
                    <p className="text-sm text-gray-500 mt-2">
                      This usually takes 20-30 seconds
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>

              <AnimatePresence>
                {generatedApp && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-lg font-semibold text-green-800 dark:text-green-200 mb-2">
                          🎉 Your app is ready!
                        </h3>
                        <p className="text-green-600 dark:text-green-400">
                          "{generatedApp.title}" has been generated successfully
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => window.open(generatedApp.preview_url, '_blank')}
                        >
                          <Play className="h-4 w-4 mr-2" />
                          Preview
                        </Button>
                        <Button size="sm">
                          <Download className="h-4 w-4 mr-2" />
                          Download
                        </Button>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              <div className="text-center pt-4">
                <p className="text-sm text-gray-500 mb-4">
                  No signup required for the first 3 apps
                </p>
                <div className="flex flex-wrap justify-center gap-2 text-xs text-gray-400">
                  <span className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">Free</span>
                  <span className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">No Credit Card</span>
                  <span className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">30s Generation</span>
                  <span className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">Mobile Optimized</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Floating elements for visual appeal */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-blue-200 dark:bg-blue-800 rounded-full opacity-20 animate-pulse"></div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-purple-200 dark:bg-purple-800 rounded-full opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-5 w-16 h-16 bg-green-200 dark:bg-green-800 rounded-full opacity-20 animate-pulse delay-500"></div>
      </div>
    </section>
  )
}