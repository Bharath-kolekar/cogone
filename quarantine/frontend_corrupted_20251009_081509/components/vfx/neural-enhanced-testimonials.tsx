'use client'

import { Card, CardContent } from '@/components/ui/card'
// import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Star, Quote } from 'lucide-react'
import { motion } from 'framer-motion'
import { NeuralBackground, NeuralPulse } from './neural-ui'
import { HolographicEffect, GlitchEffect } from './advanced-animations'
import { ParticleSystem } from './particle-system'

const testimonials = [
  {
    name: "Priya Sharma",
    role: "Startup Founder",
    company: "TechCorp India",
    avatar: "/avatars/priya.jpg",
    content: "Voice-to-App has revolutionized how we prototype ideas. What used to take weeks now takes minutes. The Hindi language support is incredible!",
    rating: 5,
    neuralIntensity: 0.7,
    color: "#3b82f6"
  },
  {
    name: "Rajesh Kumar",
    role: "Mobile Developer",
    company: "AppStudio",
    avatar: "/avatars/rajesh.jpg",
    content: "The AI understands my voice commands perfectly in Tamil. I've built 15 apps this month alone. The quality is production-ready!",
    rating: 5,
    neuralIntensity: 0.8,
    color: "#8b5cf6"
  },
  {
    name: "Anita Patel",
    role: "Product Manager",
    company: "InnovateLabs",
    avatar: "/avatars/anita.jpg",
    content: "Our team productivity has increased 300%. We can now test ideas instantly and iterate rapidly. The collaborative features are amazing.",
    rating: 5,
    neuralIntensity: 0.6,
    color: "#06b6d4"
  },
  {
    name: "Vikram Singh",
    role: "Freelance Developer",
    company: "Independent",
    avatar: "/avatars/vikram.jpg",
    content: "I've been using this for client projects. The Telugu language support helps me communicate better with local clients. Game changer!",
    rating: 5,
    neuralIntensity: 0.9,
    color: "#10b981"
  },
  {
    name: "Deepika Reddy",
    role: "UX Designer",
    company: "DesignHub",
    avatar: "/avatars/deepika.jpg",
    content: "The seamless edit feature with Ctrl+L is magical. I can describe changes in natural language and see them implemented instantly.",
    rating: 5,
    neuralIntensity: 0.8,
    color: "#f59e0b"
  },
  {
    name: "Arjun Mehta",
    role: "CTO",
    company: "ScaleUp",
    avatar: "/avatars/arjun.jpg",
    content: "We've reduced our development time by 80%. The AI-generated code is clean, well-structured, and follows best practices.",
    rating: 5,
    neuralIntensity: 0.7,
    color: "#ef4444"
  }
]

export function NeuralEnhancedTestimonials() {
  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 relative overflow-hidden">
      {/* Neural Background */}
      <NeuralBackground nodeCount={20} connectionCount={35} className="opacity-20" />
      
      {/* Particle System */}
      <ParticleSystem 
        particleCount={15} 
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
            <NeuralPulse intensity={0.6} color="#3b82f6">
              Loved by Developers Across India
            </NeuralPulse>
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            See what our users are saying about their experience with Voice-to-App
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="relative"
            >
              <HolographicEffect intensity={testimonial.neuralIntensity}>
                <Card className="h-full bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-300 relative overflow-hidden group">
                  {/* Neural Grid Background */}
                  <div className="absolute inset-0 opacity-10">
                    <div className="grid grid-cols-6 grid-rows-4 h-full">
                      {Array.from({ length: 24 }, (_, i) => (
                        <motion.div
                          key={i}
                          className="border border-blue-500/20"
                          animate={{
                            backgroundColor: Math.random() > 0.9 ? testimonial.color : 'transparent'
                          }}
                          transition={{ duration: 2, repeat: Infinity }}
                        />
                      ))}
                    </div>
                  </div>

                  <CardContent className="p-6 relative z-10">
                    {/* Quote Icon */}
                    <div className="flex justify-center mb-4">
                      <motion.div
                        className="w-12 h-12 rounded-full flex items-center justify-center"
                        style={{ backgroundColor: `${testimonial.color}20` }}
                        whileHover={{ scale: 1.1 }}
                      >
                        <NeuralPulse intensity={testimonial.neuralIntensity} color={testimonial.color}>
                          <Quote className="h-6 w-6" style={{ color: testimonial.color }} />
                        </NeuralPulse>
                      </motion.div>
                    </div>

                    {/* Rating */}
                    <div className="flex justify-center mb-4">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <motion.div
                          key={i}
                          initial={{ opacity: 0, scale: 0 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: i * 0.1 }}
                        >
                          <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                        </motion.div>
                      ))}
                    </div>

                    {/* Content */}
                    <blockquote className="text-gray-700 dark:text-gray-300 text-center mb-6 italic">
                      <GlitchEffect intensity={0.1}>
                        "{testimonial.content}"
                      </GlitchEffect>
                    </blockquote>

                    {/* Author */}
                    <div className="flex items-center justify-center space-x-3">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center text-white font-semibold">
                        {testimonial.name.split(' ').map(n => n[0]).join('')}
                      </div>
                      <div className="text-left">
                        <div className="font-semibold text-gray-900 dark:text-gray-100">
                          <NeuralPulse intensity={testimonial.neuralIntensity * 0.5} color={testimonial.color}>
                            {testimonial.name}
                          </NeuralPulse>
                        </div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          {testimonial.role} at {testimonial.company}
                        </div>
                      </div>
                    </div>
                  </CardContent>

                  {/* Hover Effect */}
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                    initial={{ x: '-100%' }}
                    whileHover={{ x: '100%' }}
                    transition={{ duration: 0.6 }}
                  />
                </Card>
              </HolographicEffect>
            </motion.div>
          ))}
        </div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-20 text-center"
        >
          <HolographicEffect intensity={0.3}>
            <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 relative overflow-hidden">
              <NeuralBackground nodeCount={12} connectionCount={20} className="opacity-20" />
              
              <div className="relative z-10">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-8">
                  <NeuralPulse intensity={0.5} color="#3b82f6">
                    Trusted by Thousands
                  </NeuralPulse>
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                      <NeuralPulse intensity={0.6} color="#3b82f6">
                        10K+
                      </NeuralPulse>
                    </div>
                    <div className="text-gray-600 dark:text-gray-400">Apps Generated</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-600 dark:text-purple-400 mb-2">
                      <NeuralPulse intensity={0.6} color="#8b5cf6">
                        5K+
                      </NeuralPulse>
                    </div>
                    <div className="text-gray-600 dark:text-gray-400">Happy Users</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-3xl font-bold text-cyan-600 dark:text-cyan-400 mb-2">
                      <NeuralPulse intensity={0.6} color="#06b6d4">
                        15+
                      </NeuralPulse>
                    </div>
                    <div className="text-gray-600 dark:text-gray-400">Languages</div>
                  </div>
                  
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600 dark:text-green-400 mb-2">
                      <NeuralPulse intensity={0.6} color="#10b981">
                        4.9★
                      </NeuralPulse>
                    </div>
                    <div className="text-gray-600 dark:text-gray-400">Average Rating</div>
                  </div>
                </div>
              </div>
            </div>
          </HolographicEffect>
        </motion.div>
      </div>
    </section>
  )
}
