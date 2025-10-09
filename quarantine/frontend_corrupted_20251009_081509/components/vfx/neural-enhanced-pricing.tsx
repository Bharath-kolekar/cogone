'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Check, Star, Zap, Crown, Rocket } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { NeuralBackground, NeuralPulse, NeuralGrid } from './neural-ui'
import { HolographicEffect, MorphingShape, EnergyField } from './advanced-animations'
import { ParticleSystem } from './particle-system'

const plans = [
  {
    name: "Free",
    price: "₹0",
    period: "forever",
    description: "Perfect for trying out voice-to-app",
    features: [
      "3 apps per month",
      "Basic voice commands",
      "Hindi & English support",
      "Mobile optimized",
      "Community support"
    ],
    cta: "Get Started Free",
    popular: false,
    neuralIntensity: 0.3,
    color: "#6b7280",
    icon: Rocket
  },
  {
    name: "Pro",
    price: "₹299",
    period: "per month",
    description: "For serious app creators",
    features: [
      "Unlimited apps",
      "Advanced AI features",
      "10+ Indian languages",
      "Team collaboration",
      "Priority support",
      "Export & deploy",
      "Custom domains"
    ],
    cta: "Start Pro Trial",
    popular: true,
    neuralIntensity: 0.8,
    color: "#3b82f6",
    icon: Zap
  },
  {
    name: "Enterprise",
    price: "₹999",
    period: "per month",
    description: "For teams and organizations",
    features: [
      "Everything in Pro",
      "White-label solution",
      "API access",
      "Custom integrations",
      "Dedicated support",
      "Advanced analytics",
      "SSO integration"
    ],
    cta: "Contact Sales",
    popular: false,
    neuralIntensity: 0.9,
    color: "#8b5cf6",
    icon: Crown
  }
]

export function NeuralEnhancedPricing() {
  const [selectedPlan, setSelectedPlan] = useState('Pro')
  const [isAnnual, setIsAnnual] = useState(false)

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 relative overflow-hidden">
      {/* Neural Background */}
      <NeuralBackground nodeCount={30} connectionCount={50} className="opacity-20" />
      
      {/* Particle System */}
      <ParticleSystem 
        particleCount={25} 
        colors={['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981']}
        speed={0.4}
        className="opacity-30"
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
              Simple, Transparent Pricing
            </NeuralPulse>
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-8">
            Start free, scale as you grow. No hidden fees, no surprises.
          </p>

          {/* Billing Toggle */}
          <div className="flex items-center justify-center space-x-4 mb-8">
            <span className={`text-sm font-medium ${!isAnnual ? 'text-gray-900 dark:text-gray-100' : 'text-gray-500'}`}>
              Monthly
            </span>
            <button
              onClick={() => setIsAnnual(!isAnnual)}
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-gray-200 dark:bg-gray-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  isAnnual ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
            <span className={`text-sm font-medium ${isAnnual ? 'text-gray-900 dark:text-gray-100' : 'text-gray-500'}`}>
              Annual
              <Badge variant="secondary" className="ml-2">Save 20%</Badge>
            </span>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <motion.div
              key={plan.name}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className={`relative ${plan.popular ? 'md:-mt-8' : ''}`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-20">
                  <Badge className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-4 py-1">
                    <Star className="h-3 w-3 mr-1" />
                    Most Popular
                  </Badge>
                </div>
              )}

              <HolographicEffect intensity={plan.neuralIntensity}>
                <Card 
                  className={`h-full transition-all duration-300 hover:shadow-2xl ${
                    plan.popular 
                      ? 'border-2 border-blue-500 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-700' 
                      : 'border-0 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm'
                  } relative overflow-hidden`}
                >
                  {/* Neural Grid Background */}
                  <NeuralGrid 
                    rows={8} 
                    cols={6} 
                    className="absolute inset-0 opacity-10"
                  />
                  
                  {/* Morphing Shape Animation */}
                  <div className="absolute top-4 right-4 opacity-20">
                    <MorphingShape 
                      shapes={['circle', 'square', 'triangle']}
                      size={25}
                      color={plan.color}
                    />
                  </div>
                  
                  {/* Energy Field for Popular Plan */}
                  {plan.popular && (
                    <EnergyField 
                      intensity={0.6} 
                      color={plan.color} 
                      className="opacity-30"
                    >
                      <div />
                    </EnergyField>
                  )}

                  <CardHeader className="text-center pb-4 relative z-10">
                    <div className="mx-auto w-12 h-12 rounded-lg flex items-center justify-center mb-4 relative overflow-hidden"
                         style={{ backgroundColor: `${plan.color}20` }}>
                      <NeuralPulse 
                        intensity={plan.neuralIntensity} 
                        color={plan.color}
                        className="absolute inset-0"
                      >
                        <div />
                      </NeuralPulse>
                      <plan.icon className="h-6 w-6 relative z-10" style={{ color: plan.color }} />
                    </div>
                    
                    <CardTitle className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                      <NeuralPulse intensity={plan.neuralIntensity * 0.7} color={plan.color}>
                        {plan.name}
                      </NeuralPulse>
                    </CardTitle>
                    
                    <div className="mt-4">
                      <span className="text-4xl font-bold text-gray-900 dark:text-gray-100">
                        {isAnnual && plan.name !== 'Free' ? `₹${Math.floor(parseInt(plan.price.replace('₹', '')) * 0.8)}` : plan.price}
                      </span>
                      <span className="text-gray-600 dark:text-gray-400 ml-2">
                        {plan.period}
                      </span>
                    </div>
                    
                    <CardDescription className="text-gray-600 dark:text-gray-400 mt-2">
                      {plan.description}
                    </CardDescription>
                  </CardHeader>

                  <CardContent className="pt-0 relative z-10">
                    <ul className="space-y-3 mb-8">
                      {plan.features.map((feature, featureIndex) => (
                        <motion.li
                          key={feature}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: featureIndex * 0.1 }}
                          className="flex items-center space-x-3"
                        >
                          <div 
                            className="w-5 h-5 rounded-full flex items-center justify-center"
                            style={{ backgroundColor: `${plan.color}20` }}
                          >
                            <Check className="h-3 w-3" style={{ color: plan.color }} />
                          </div>
                          <span className="text-gray-700 dark:text-gray-300 text-sm">
                            {feature}
                          </span>
                        </motion.li>
                      ))}
                    </ul>

                    <Button 
                      className={`w-full ${
                        plan.popular 
                          ? 'bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600' 
                          : 'bg-gray-900 dark:bg-gray-100 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-gray-200'
                      }`}
                      onClick={() => setSelectedPlan(plan.name)}
                    >
                      <NeuralPulse intensity={0.5} color="#ffffff">
                        {plan.cta}
                      </NeuralPulse>
                    </Button>
                  </CardContent>
                </Card>
              </HolographicEffect>
            </motion.div>
          ))}
        </div>

        {/* Additional Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <HolographicEffect intensity={0.2}>
            <div className="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-2xl p-8 relative overflow-hidden">
              <NeuralBackground nodeCount={10} connectionCount={15} className="opacity-20" />
              
              <div className="relative z-10">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
                  <NeuralPulse intensity={0.4} color="#3b82f6">
                    All plans include:
                  </NeuralPulse>
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm text-gray-600 dark:text-gray-400">
                  <div className="flex items-center justify-center space-x-2">
                    <Check className="h-4 w-4 text-green-500" />
                    <span>30-second app generation</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2">
                    <Check className="h-4 w-4 text-green-500" />
                    <span>Mobile-optimized output</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2">
                    <Check className="h-4 w-4 text-green-500" />
                    <span>UPI payment support</span>
                  </div>
                </div>
                
                <p className="text-sm text-gray-500 mt-6">
                  Need a custom plan? <a href="#" className="text-blue-500 hover:text-blue-600">Contact us</a>
                </p>
              </div>
            </div>
          </HolographicEffect>
        </motion.div>
      </div>
    </section>
  )
}
