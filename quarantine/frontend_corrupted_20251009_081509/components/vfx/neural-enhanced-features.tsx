'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Mic, Zap, Globe, Shield, Smartphone, Users, Gift, Code } from 'lucide-react'
import { motion } from 'framer-motion'
import { SeamlessEditDemo } from '@/components/seamless-edit-demo'
import { NeuralBackground, NeuralPulse, NeuralGrid } from './neural-ui'
import { HolographicEffect, MorphingShape, LiquidBlob, GlitchEffect } from './advanced-animations'
import { ParticleSystem } from './particle-system'

const features = [
  {
    icon: Mic,
    title: "Voice Commands",
    description: "Speak naturally in Hindi, English, Tamil, Telugu, and 6+ Indian languages. Our AI understands your intent perfectly.",
    highlight: "30-second generation",
    neuralIntensity: 0.8,
    color: "#3b82f6"
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "From voice to working app in under 30 seconds. No coding knowledge required, just speak your idea.",
    highlight: "Instant results",
    neuralIntensity: 0.9,
    color: "#8b5cf6"
  },
  {
    icon: Globe,
    title: "Multi-Language Support",
    description: "Built for India with support for 10+ regional languages. Voice commands work seamlessly in your preferred language.",
    highlight: "10+ languages",
    neuralIntensity: 0.7,
    color: "#06b6d4"
  },
  {
    icon: Shield,
    title: "Privacy First",
    description: "Your voice data stays local when possible. Choose between local processing or secure cloud fallback.",
    highlight: "Local processing",
    neuralIntensity: 0.6,
    color: "#10b981"
  },
  {
    icon: Smartphone,
    title: "Mobile Optimized",
    description: "Perfect for Indian mobile users. Responsive design works flawlessly on all screen sizes and devices.",
    highlight: "Mobile-first",
    neuralIntensity: 0.8,
    color: "#f59e0b"
  },
  {
    icon: Users,
    title: "Collaborative",
    description: "Invite team members to collaborate on your apps. Share, edit, and deploy together seamlessly.",
    highlight: "Team features",
    neuralIntensity: 0.7,
    color: "#ef4444"
  },
  {
    icon: Gift,
    title: "Gamification",
    description: "Earn points, unlock achievements, climb leaderboards. Make app creation fun and rewarding.",
    highlight: "Earn rewards",
    neuralIntensity: 0.9,
    color: "#ec4899"
  },
  {
    icon: Code,
    title: "Export & Deploy",
    description: "Download your app code or deploy directly to Vercel, Netlify, or your preferred platform.",
    highlight: "One-click deploy",
    neuralIntensity: 0.8,
    color: "#6366f1"
  },
  {
    icon: Code,
    title: "Seamless Edit & Fix",
    description: "Select code + Ctrl+L to describe changes. AI will optimize, fix, and improve your code instantly.",
    highlight: "Ctrl+L magic",
    neuralIntensity: 0.9,
    color: "#14b8a6"
  }
]

export function NeuralEnhancedFeatures() {
  return (
    <section className="py-20 bg-white dark:bg-gray-900 relative overflow-hidden">
      {/* Neural Background */}
      <NeuralBackground nodeCount={25} connectionCount={40} className="opacity-30" />
      
      {/* Particle System */}
      <ParticleSystem 
        particleCount={20} 
        colors={['#3b82f6', '#8b5cf6', '#06b6d4']}
        speed={0.3}
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
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-gray-100 mb-6">
            <GlitchEffect intensity={0.2}>
              Built for India, Made for Everyone
            </GlitchEffect>
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Experience the future of app development with voice commands, 
            multi-language support, and AI-powered generation.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="relative"
            >
              <HolographicEffect intensity={feature.neuralIntensity}>
                <Card className="h-full hover:shadow-lg transition-all duration-300 border-0 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 relative overflow-hidden group">
                  {/* Neural Grid Background */}
                  <NeuralGrid 
                    rows={6} 
                    cols={8} 
                    className="absolute inset-0 opacity-10"
                  />
                  
                  {/* Morphing Shape Animation */}
                  <div className="absolute top-4 right-4 opacity-20">
                    <MorphingShape 
                      shapes={['circle', 'square', 'triangle']}
                      size={30}
                      color={feature.color}
                    />
                  </div>
                  
                  {/* Liquid Blob Animation */}
                  <div className="absolute bottom-4 left-4 opacity-20">
                    <LiquidBlob 
                      size={40}
                      color={feature.color}
                    />
                  </div>

                  <CardHeader className="text-center pb-4 relative z-10">
                    <div className="mx-auto w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4 relative overflow-hidden">
                      {/* Neural Pulse Effect */}
                      <NeuralPulse 
                        intensity={feature.neuralIntensity} 
                        color={feature.color}
                        className="absolute inset-0"
                      >
                        <div />
                      </NeuralPulse>
                      
                      <feature.icon className="h-6 w-6 text-blue-600 dark:text-blue-400 relative z-10" />
                    </div>
                    
                    <CardTitle className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                      <NeuralPulse intensity={feature.neuralIntensity * 0.5} color={feature.color}>
                        {feature.title}
                      </NeuralPulse>
                    </CardTitle>
                    
                    <div 
                      className="inline-block text-xs font-medium px-2 py-1 rounded-full"
                      style={{ 
                        backgroundColor: `${feature.color}20`,
                        color: feature.color
                      }}
                    >
                      {feature.highlight}
                    </div>
                  </CardHeader>
                  
                  <CardContent className="pt-0 relative z-10">
                    <CardDescription className="text-gray-600 dark:text-gray-400 text-center">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                  
                  {/* Hover Effect */}
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                    initial={{ x: '-100%' }}
                    whileHover={{ x: '100%' }}
                    transition={{ duration: 0.6 }}
                  />
                </Card>
              </HolographicEffect>
            </motion.div>
          ))}
        </div>

        {/* Enhanced Additional Info Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          viewport={{ once: true }}
          className="mt-20 text-center"
        >
          <HolographicEffect intensity={0.3}>
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl p-8 relative overflow-hidden">
              {/* Neural Background */}
              <NeuralBackground nodeCount={15} connectionCount={25} className="opacity-20" />
              
              <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4 relative z-10">
                <NeuralPulse intensity={0.6} color="#3b82f6">
                  Why Choose Voice-to-App?
                </NeuralPulse>
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left relative z-10">
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="p-4 rounded-lg bg-white/50 dark:bg-gray-700/50 backdrop-blur-sm"
                >
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                    🇮🇳 India-First
                  </h4>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    Built specifically for Indian users with UPI payments, regional language support, and mobile-first design.
                  </p>
                </motion.div>
                
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="p-4 rounded-lg bg-white/50 dark:bg-gray-700/50 backdrop-blur-sm"
                >
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                    🚀 Free to Start
                  </h4>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    Create your first 3 apps completely free. No credit card required, no hidden fees.
                  </p>
                </motion.div>
                
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="p-4 rounded-lg bg-white/50 dark:bg-gray-700/50 backdrop-blur-sm"
                >
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                    🔒 Privacy Protected
                  </h4>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    Your voice data stays private with local processing options and secure cloud fallbacks.
                  </p>
                </motion.div>
              </div>
            </div>
          </HolographicEffect>
        </motion.div>
      </div>

      {/* Seamless Edit Demo */}
      <div className="mt-20">
        <SeamlessEditDemo />
      </div>
    </section>
  )
}
