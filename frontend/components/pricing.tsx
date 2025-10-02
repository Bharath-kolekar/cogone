'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Check, Star, Zap } from 'lucide-react'
import { motion } from 'framer-motion'

const plans = [
  {
    name: "Free",
    price: "₹0",
    period: "forever",
    description: "Perfect for trying out voice-to-app generation",
    features: [
      "5 voice commands per day",
      "Basic app templates",
      "Community support",
      "Generated apps expire in 7 days",
      "Mobile-optimized interface",
      "Hindi & English support"
    ],
    limitations: [
      "Limited to 5 apps per month",
      "No custom domains",
      "Basic templates only"
    ],
    cta: "Start Free",
    popular: false,
    color: "border-gray-200"
  },
  {
    name: "Pro",
    price: "₹999",
    period: "per month",
    description: "For serious app creators and developers",
    features: [
      "Unlimited voice commands",
      "Premium app templates",
      "Priority support",
      "Generated apps never expire",
      "Custom domains",
      "Advanced analytics",
      "All 10+ Indian languages",
      "Export to any platform",
      "Collaborative editing",
      "API access"
    ],
    limitations: [],
    cta: "Go Pro",
    popular: true,
    color: "border-blue-500"
  },
  {
    name: "Enterprise",
    price: "₹4,999",
    period: "per month",
    description: "For teams and organizations",
    features: [
      "Everything in Pro",
      "Team collaboration (up to 50 members)",
      "White-label solution",
      "Dedicated support",
      "Custom integrations",
      "Advanced security",
      "On-premise deployment",
      "Custom AI models",
      "Priority feature requests",
      "SLA guarantee"
    ],
    limitations: [],
    cta: "Contact Sales",
    popular: false,
    color: "border-purple-500"
  }
]

const paymentMethods = [
  { name: "UPI", icon: "💳", description: "Instant payments" },
  { name: "Cards", icon: "💳", description: "Visa, Mastercard" },
  { name: "Net Banking", icon: "🏦", description: "All major banks" },
  { name: "PayPal", icon: "🌍", description: "International" },
  { name: "Google Pay", icon: "📱", description: "Quick & secure" }
]

export function Pricing() {
  return (
    <section className="py-20 bg-gray-50 dark:bg-gray-800">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-gray-100 mb-6">
            Simple, Transparent Pricing
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto mb-8">
            Start free, upgrade when you need more. No hidden fees, no surprises.
          </p>
          
          {/* Payment methods */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            {paymentMethods.map((method) => (
              <div key={method.name} className="flex items-center space-x-2 bg-white dark:bg-gray-700 px-3 py-2 rounded-lg shadow-sm">
                <span className="text-lg">{method.icon}</span>
                <div className="text-sm">
                  <div className="font-medium text-gray-900 dark:text-gray-100">{method.name}</div>
                  <div className="text-gray-500 dark:text-gray-400 text-xs">{method.description}</div>
                </div>
              </div>
            ))}
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
              className="relative"
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-10">
                  <div className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
                    <Star className="h-4 w-4" />
                    <span>Most Popular</span>
                  </div>
                </div>
              )}
              
              <Card className={`h-full ${plan.popular ? 'ring-2 ring-blue-500 shadow-xl scale-105' : 'shadow-lg'} ${plan.color} border-2`}>
                <CardHeader className="text-center pb-6">
                  <CardTitle className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                    {plan.name}
                  </CardTitle>
                  <div className="mt-4">
                    <span className="text-4xl font-bold text-gray-900 dark:text-gray-100">
                      {plan.price}
                    </span>
                    <span className="text-gray-600 dark:text-gray-400 ml-2">
                      {plan.period}
                    </span>
                  </div>
                  <CardDescription className="text-gray-600 dark:text-gray-400 mt-2">
                    {plan.description}
                  </CardDescription>
                </CardHeader>
                
                <CardContent className="space-y-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">
                      What's included:
                    </h4>
                    <ul className="space-y-2">
                      {plan.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-start space-x-3">
                          <Check className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-600 dark:text-gray-400 text-sm">
                            {feature}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {plan.limitations.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-3">
                        Limitations:
                      </h4>
                      <ul className="space-y-2">
                        {plan.limitations.map((limitation, limitationIndex) => (
                          <li key={limitationIndex} className="flex items-start space-x-3">
                            <span className="text-gray-400 text-sm">
                              • {limitation}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <Button 
                    className={`w-full py-3 text-base font-medium ${
                      plan.popular 
                        ? 'bg-blue-500 hover:bg-blue-600 text-white' 
                        : 'bg-gray-900 hover:bg-gray-800 text-white dark:bg-gray-100 dark:hover:bg-gray-200 dark:text-gray-900'
                    }`}
                    size="lg"
                  >
                    {plan.cta}
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Additional info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <div className="bg-white dark:bg-gray-700 rounded-2xl p-8 shadow-lg">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
              💰 Money-Back Guarantee
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Not satisfied? Get a full refund within 30 days, no questions asked.
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
              <div className="flex items-center space-x-3">
                <Zap className="h-6 w-6 text-yellow-500" />
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100">Instant Setup</h4>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">Start creating apps immediately</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Check className="h-6 w-6 text-green-500" />
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100">Cancel Anytime</h4>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">No long-term commitments</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Star className="h-6 w-6 text-blue-500" />
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-gray-100">Premium Support</h4>
                  <p className="text-gray-600 dark:text-gray-400 text-sm">24/7 help when you need it</p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}