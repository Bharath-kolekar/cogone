'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Mic, Zap, Globe, Shield, Smartphone, Users, Gift, Code } from 'lucide-react'
import { motion } from 'framer-motion'

const features = [
  {
    icon: Mic,
    title: "Voice Commands",
    description: "Speak naturally in Hindi, English, Tamil, Telugu, and 6+ Indian languages. Our AI understands your intent perfectly.",
    highlight: "30-second generation"
  },
  {
    icon: Zap,
    title: "Lightning Fast",
    description: "From voice to working app in under 30 seconds. No coding knowledge required, just speak your idea.",
    highlight: "Instant results"
  },
  {
    icon: Globe,
    title: "Multi-Language Support",
    description: "Built for India with support for 10+ regional languages. Voice commands work seamlessly in your preferred language.",
    highlight: "10+ languages"
  },
  {
    icon: Shield,
    title: "Privacy First",
    description: "Your voice data stays local when possible. Choose between local processing or secure cloud fallback.",
    highlight: "Local processing"
  },
  {
    icon: Smartphone,
    title: "Mobile Optimized",
    description: "Perfect for Indian mobile users. Responsive design works flawlessly on all screen sizes and devices.",
    highlight: "Mobile-first"
  },
  {
    icon: Users,
    title: "Collaborative",
    description: "Invite team members to collaborate on your apps. Share, edit, and deploy together seamlessly.",
    highlight: "Team features"
  },
  {
    icon: Gift,
    title: "Gamification",
    description: "Earn points, unlock achievements, climb leaderboards. Make app creation fun and rewarding.",
    highlight: "Earn rewards"
  },
  {
    icon: Code,
    title: "Export & Deploy",
    description: "Download your app code or deploy directly to Vercel, Netlify, or your preferred platform.",
    highlight: "One-click deploy"
  }
]

export function Features() {
  return (
    <section className="py-20 bg-white dark:bg-gray-900">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-gray-100 mb-6">
            Built for India, Made for Everyone
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
            >
              <Card className="h-full hover:shadow-lg transition-shadow duration-300 border-0 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700">
                <CardHeader className="text-center pb-4">
                  <div className="mx-auto w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                  </div>
                  <CardTitle className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    {feature.title}
                  </CardTitle>
                  <div className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs font-medium px-2 py-1 rounded-full">
                    {feature.highlight}
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <CardDescription className="text-gray-600 dark:text-gray-400 text-center">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Additional info section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          viewport={{ once: true }}
          className="mt-20 text-center"
        >
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
              Why Choose Voice-to-App?
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                  🇮🇳 India-First
                </h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Built specifically for Indian users with UPI payments, regional language support, and mobile-first design.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                  🚀 Free to Start
                </h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Create your first 3 apps completely free. No credit card required, no hidden fees.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                  🔒 Privacy Protected
                </h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Your voice data stays private with local processing options and secure cloud fallbacks.
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}