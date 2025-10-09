'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Mic, MicOff, Play, Pause, Download } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { VoiceRecorder } from '@/components/voice-recorder'
import { LanguageToggle } from '@/components/language-toggle'
import { ParticleSystem, NeuralNetworkViz } from './particle-system'
import { NeuralBackground, NeuralPulse, NeuralLoading } from './neural-ui'
import { HolographicEffect, GlitchEffect, EnergyField } from './advanced-animations'
import { VoiceVisualizer, CircularVoiceVisualizer, VoicePulse } from './voice-visualizer'

export function NeuralEnhancedHero() {
  const [isRecording, setIsRecording] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedApp, setGeneratedApp] = useState<{
    id: string;
    title: string;
    preview_url: string;
    status: string;
  } | null>(null)
  const [audioLevel, setAudioLevel] = useState(0)

  const handleVoiceCommand = async (command: string) => {
    setTranscript(command)
    setIsGenerating(true)
    
    // Simulate audio level changes
    const simulateAudioLevel = () => {
      const interval = setInterval(() => {
        setAudioLevel(Math.random() * 0.8 + 0.2)
      }, 100)
      
      setTimeout(() => {
        clearInterval(interval)
        setAudioLevel(0)
      }, 3000)
    }
    
    simulateAudioLevel()
    
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
    <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 overflow-hidden">
      {/* Neural Background */}
      <NeuralBackground nodeCount={20} connectionCount={30} />
      
      {/* Particle System */}
      <ParticleSystem 
        particleCount={30} 
        colors={['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981']}
        speed={0.5}
      />
      
      {/* Neural Network Visualization */}
      <NeuralNetworkViz nodes={15} connections={25} />

      <div className="container mx-auto px-4 py-16 relative z-10">
        <div className="text-center mb-12">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-6"
          >
            <GlitchEffect intensity={0.3}>
              Voice to App
            </GlitchEffect>
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
          <HolographicEffect intensity={0.5}>
            <Card className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-2xl relative overflow-hidden">
              {/* Energy Field */}
              <EnergyField intensity={isRecording ? 1 : 0.3} color="#3b82f6" />
              
              <CardHeader className="text-center relative z-10">
                <CardTitle className="text-2xl font-bold text-gray-800 dark:text-gray-200">
                  <NeuralPulse intensity={isRecording ? 1 : 0.5} color="#3b82f6">
                    Try It Now - Free
                  </NeuralPulse>
                </CardTitle>
                <CardDescription className="text-lg text-gray-600 dark:text-gray-400">
                  Speak your app idea and watch it come to life
                </CardDescription>
              </CardHeader>
              
              <CardContent className="space-y-6 relative z-10">
                {/* Voice Recorder with Enhanced Visuals */}
                <div className="relative">
                  <VoiceRecorder
                    onTranscript={handleVoiceCommand}
                    isRecording={isRecording}
                    onRecordingChange={setIsRecording}
                    disabled={isGenerating}
                  />
                  
                  {/* Voice Visualizer */}
                  {isRecording && (
                    <div className="absolute -bottom-4 left-0 right-0 h-16">
                      <VoiceVisualizer 
                        isRecording={isRecording} 
                        audioLevel={audioLevel}
                        className="opacity-60"
                      />
                    </div>
                  )}
                  
                  {/* Voice Pulse Effect */}
                  <VoicePulse 
                    isRecording={isRecording} 
                    audioLevel={audioLevel}
                    className="absolute inset-0 pointer-events-none"
                  />
                </div>

                <AnimatePresence>
                  {transcript && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 relative overflow-hidden"
                    >
                      {/* Neural Grid Background */}
                      <div className="absolute inset-0 opacity-10">
                        <div className="grid grid-cols-8 grid-rows-4 h-full">
                          {Array.from({ length: 32 }, (_, i) => (
                            <motion.div
                              key={i}
                              className="border border-blue-500/20"
                              animate={{
                                backgroundColor: Math.random() > 0.8 ? '#3b82f6' : 'transparent'
                              }}
                              transition={{ duration: 0.5 }}
                            />
                          ))}
                        </div>
                      </div>
                      
                      <div className="relative z-10">
                        <h3 className="font-semibold text-gray-800 dark:text-gray-200 mb-2">
                          Your Command:
                        </h3>
                        <p className="text-gray-600 dark:text-gray-400 italic">
                          "{transcript}"
                        </p>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                <AnimatePresence>
                  {isGenerating && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      className="text-center py-8 relative"
                    >
                      {/* Circular Voice Visualizer */}
                      <div className="absolute inset-0 flex items-center justify-center">
                        <CircularVoiceVisualizer 
                          isRecording={isGenerating} 
                          audioLevel={audioLevel}
                          size={120}
                          className="opacity-30"
                        />
                      </div>
                      
                      <div className="relative z-10">
                        <NeuralLoading size={40} color="#3b82f6" />
                        <span className="text-lg font-medium text-gray-700 dark:text-gray-300 ml-3">
                          Generating your app...
                        </span>
                        <p className="text-sm text-gray-500 mt-2">
                          This usually takes 20-30 seconds
                        </p>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                <AnimatePresence>
                  {generatedApp && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6 relative overflow-hidden"
                    >
                      {/* Success Energy Field */}
                      <EnergyField intensity={1} color="#10b981" className="opacity-50" />
                      
                      <div className="flex items-center justify-between relative z-10">
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
          </HolographicEffect>
        </motion.div>

        {/* Enhanced Floating Elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-blue-200 dark:bg-blue-800 rounded-full opacity-20 animate-pulse">
          <EnergyField intensity={0.5} color="#3b82f6" />
        </div>
        <div className="absolute bottom-20 right-10 w-32 h-32 bg-purple-200 dark:bg-purple-800 rounded-full opacity-20 animate-pulse delay-1000">
          <EnergyField intensity={0.3} color="#8b5cf6" />
        </div>
        <div className="absolute top-1/2 left-5 w-16 h-16 bg-green-200 dark:bg-green-800 rounded-full opacity-20 animate-pulse delay-500">
          <EnergyField intensity={0.4} color="#10b981" />
        </div>
      </div>
    </section>
  )
}
