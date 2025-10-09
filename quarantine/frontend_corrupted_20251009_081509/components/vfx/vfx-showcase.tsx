'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Brain, 
  Zap, 
  Sparkles, 
  Waves, 
  Cpu, 
  Network,
  Play,
  Pause,
  Settings,
  Eye,
  EyeOff
} from 'lucide-react'

// Import all VFX components
import { ParticleSystem, NeuralNetworkViz } from './particle-system'
import { 
  NeuralBackground, 
  NeuralPulse, 
  NeuralGrid, 
  NeuralWave, 
  NeuralLoading 
} from './neural-ui'
import { 
  HolographicEffect, 
  MorphingShape, 
  LiquidBlob, 
  MatrixRain, 
  GlitchEffect,
  FloatingElements,
  EnergyField
} from './advanced-animations'
import { 
  VoiceVisualizer, 
  CircularVoiceVisualizer, 
  VoicePulse 
} from './voice-visualizer'
import { PerformanceOptimizer, usePerformanceAwareAnimation } from './performance-optimizer'

const vfxCategories = [
  {
    id: 'particles',
    name: 'Particle Systems',
    icon: Sparkles,
    description: 'Dynamic particle effects and animations',
    color: '#3b82f6'
  },
  {
    id: 'neural',
    name: 'Neural Networks',
    icon: Brain,
    description: 'AI-inspired visual patterns and connections',
    color: '#8b5cf6'
  },
  {
    id: 'voice',
    name: 'Voice Visualizers',
    icon: Waves,
    description: 'Audio-reactive visual components',
    color: '#06b6d4'
  },
  {
    id: 'advanced',
    name: 'Advanced Effects',
    icon: Zap,
    description: 'Holographic, morphing, and glitch effects',
    color: '#10b981'
  }
]

export function VFXShowcase() {
  const [activeCategory, setActiveCategory] = useState('particles')
  const [isPlaying, setIsPlaying] = useState(false)
  const [showControls, setShowControls] = useState(true)
  const [audioLevel, setAudioLevel] = useState(0.5)
  const { shouldAnimate, fps } = usePerformanceAwareAnimation()

  const togglePlayback = () => {
    setIsPlaying(!isPlaying)
    if (!isPlaying) {
      // Simulate audio level changes
      const interval = setInterval(() => {
        setAudioLevel(Math.random() * 0.8 + 0.2)
      }, 100)
      
      setTimeout(() => {
        clearInterval(interval)
        setAudioLevel(0)
      }, 5000)
    }
  }

  return (
    <section className="py-20 bg-gradient-to-br from-gray-900 to-blue-900 relative overflow-hidden">
      {/* Neural Background */}
      <NeuralBackground nodeCount={25} connectionCount={40} className="opacity-30" />
      
      {/* Particle System */}
      <ParticleSystem 
        particleCount={30} 
        colors={['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981']}
        speed={0.5}
        className="opacity-40"
      />

      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            <NeuralPulse intensity={0.8} color="#3b82f6">
              VFX & Neural UI Showcase
            </NeuralPulse>
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Experience the power of advanced visual effects and neural-inspired UI components
          </p>
          
          {/* Performance Info */}
          <div className="flex items-center justify-center space-x-4 text-sm text-gray-400">
            <div className="flex items-center space-x-2">
              <Cpu className="h-4 w-4" />
              <span>FPS: {fps}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Network className="h-4 w-4" />
              <span>Animations: {shouldAnimate ? 'Enabled' : 'Optimized'}</span>
            </div>
          </div>
        </motion.div>

        <Tabs value={activeCategory} onValueChange={setActiveCategory} className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-8">
            {vfxCategories.map((category) => (
              <TabsTrigger 
                key={category.id} 
                value={category.id}
                className="flex items-center space-x-2"
              >
                <category.icon className="h-4 w-4" />
                <span>{category.name}</span>
              </TabsTrigger>
            ))}
          </TabsList>

          {/* Controls */}
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center space-x-4">
              <Button
                onClick={togglePlayback}
                variant={isPlaying ? "destructive" : "default"}
                className="flex items-center space-x-2"
              >
                {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                <span>{isPlaying ? 'Stop' : 'Play'} Demo</span>
              </Button>
              
              <Button
                onClick={() => setShowControls(!showControls)}
                variant="outline"
                size="sm"
              >
                {showControls ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
            </div>

            <Badge variant="secondary" className="bg-blue-500/20 text-blue-300">
              Performance Optimized
            </Badge>
          </div>

          {/* Particle Systems Tab */}
          <TabsContent value="particles" className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Particle System</CardTitle>
                  <CardDescription className="text-gray-300">
                    Interactive particle effects with customizable properties
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <ParticleSystem 
                      particleCount={50} 
                      colors={['#3b82f6', '#8b5cf6', '#06b6d4']}
                      speed={isPlaying ? 1 : 0.5}
                      className="opacity-80"
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Floating Elements</CardTitle>
                  <CardDescription className="text-gray-300">
                    Animated floating particles with organic movement
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <FloatingElements count={20} />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Neural Networks Tab */}
          <TabsContent value="neural" className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Neural Network</CardTitle>
                  <CardDescription className="text-gray-300">
                    AI-inspired network visualization with dynamic connections
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <NeuralNetworkViz nodes={20} connections={30} />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Neural Grid</CardTitle>
                  <CardDescription className="text-gray-300">
                    Interactive grid pattern with neural activation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <NeuralGrid rows={8} cols={12} />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Neural Wave</CardTitle>
                  <CardDescription className="text-gray-300">
                    Animated wave patterns with neural characteristics
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <NeuralWave 
                      amplitude={15}
                      frequency={0.02}
                      speed={0.01}
                      color="#3b82f6"
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Neural Loading</CardTitle>
                  <CardDescription className="text-gray-300">
                    Advanced loading animation with neural patterns
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center">
                    <NeuralLoading size={60} color="#3b82f6" />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Voice Visualizers Tab */}
          <TabsContent value="voice" className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Voice Visualizer</CardTitle>
                  <CardDescription className="text-gray-300">
                    Audio-reactive bar visualization
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <VoiceVisualizer 
                      isRecording={isPlaying} 
                      audioLevel={audioLevel}
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Circular Visualizer</CardTitle>
                  <CardDescription className="text-gray-300">
                    Circular audio visualization with radial patterns
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center">
                    <CircularVoiceVisualizer 
                      isRecording={isPlaying} 
                      audioLevel={audioLevel}
                      size={200}
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Voice Pulse</CardTitle>
                  <CardDescription className="text-gray-300">
                    Pulsing effect synchronized with audio input
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center">
                    <VoicePulse 
                      isRecording={isPlaying} 
                      audioLevel={audioLevel}
                      className="w-32 h-32"
                    />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Advanced Effects Tab */}
          <TabsContent value="advanced" className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Holographic Effect</CardTitle>
                  <CardDescription className="text-gray-300">
                    Futuristic holographic shimmer effect
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <HolographicEffect intensity={0.8}>
                      <div className="w-full h-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center">
                        <span className="text-white text-2xl font-bold">Holographic</span>
                      </div>
                    </HolographicEffect>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Morphing Shape</CardTitle>
                  <CardDescription className="text-gray-300">
                    Dynamic shape transformation animation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center">
                    <MorphingShape 
                      shapes={['circle', 'square', 'triangle']}
                      size={100}
                      color="#3b82f6"
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Liquid Blob</CardTitle>
                  <CardDescription className="text-gray-300">
                    Organic liquid-like morphing animation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center">
                    <LiquidBlob 
                      size={120}
                      color="#8b5cf6"
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Matrix Rain</CardTitle>
                  <CardDescription className="text-gray-300">
                    Matrix-style falling code animation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <MatrixRain 
                      characters="01"
                      speed={50}
                    />
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Glitch Effect</CardTitle>
                  <CardDescription className="text-gray-300">
                    Digital glitch distortion effect
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 relative overflow-hidden rounded-lg">
                    <GlitchEffect intensity={0.5}>
                      <div className="w-full h-full bg-gradient-to-br from-red-500/20 to-pink-500/20 flex items-center justify-center">
                        <span className="text-white text-2xl font-bold">Glitch</span>
                      </div>
                    </GlitchEffect>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-white/10 backdrop-blur-sm border-white/20">
                <CardHeader>
                  <CardTitle className="text-white">Energy Field</CardTitle>
                  <CardDescription className="text-gray-300">
                    Pulsing energy field with glow effects
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center">
                    <EnergyField 
                      intensity={0.8}
                      color="#10b981"
                      className="w-32 h-32"
                    />
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>

        {/* Performance Optimizer Demo */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <Card className="bg-white/10 backdrop-blur-sm border-white/20">
            <CardHeader>
              <CardTitle className="text-white">Performance Optimizer</CardTitle>
              <CardDescription className="text-gray-300">
                Automatic performance optimization based on device capabilities and FPS
              </CardDescription>
            </CardHeader>
            <CardContent>
              <PerformanceOptimizer
                enableParticles={shouldAnimate}
                enableNeural={shouldAnimate}
                enableAnimations={shouldAnimate}
                maxFPS={60}
                quality={fps > 50 ? 'high' : fps > 30 ? 'medium' : 'low'}
              >
                <div className="p-8 text-center">
                  <h3 className="text-xl font-semibold text-white mb-4">
                    Adaptive Performance
                  </h3>
                  <p className="text-gray-300 mb-4">
                    The VFX system automatically adjusts quality based on your device performance
                  </p>
                  <div className="flex items-center justify-center space-x-4 text-sm text-gray-400">
                    <span>Current FPS: {fps}</span>
                    <span>Quality: {fps > 50 ? 'High' : fps > 30 ? 'Medium' : 'Low'}</span>
                    <span>Animations: {shouldAnimate ? 'Enabled' : 'Optimized'}</span>
                  </div>
                </div>
              </PerformanceOptimizer>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  )
}
