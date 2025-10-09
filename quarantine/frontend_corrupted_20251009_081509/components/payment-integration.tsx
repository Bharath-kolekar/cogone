/**
 * Payment Integration Component
 * Handles subscription and payment management
 */

'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Check, X, CreditCard, Download, Star } from 'lucide-react'
import { motion } from 'framer-motion'
import { apiService, PaymentOrderRequest } from '@/lib/api'

interface SubscriptionPlan {
  id: string
  name: string
  price: number
  currency: string
  features: string[]
  popular?: boolean
}

interface PaymentIntegrationProps {
  onPaymentSuccess?: (orderId: string) => void
  onPaymentError?: (error: string) => void
}

export function PaymentIntegration({ 
  onPaymentSuccess, 
  onPaymentError 
}: PaymentIntegrationProps) {
  const [plans, setPlans] = useState<SubscriptionPlan[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  useEffect(() => {
    loadPlans()
  }, [])

  const loadPlans = async () => {
    try {
      setIsLoading(true)
      const response = await apiService.getSubscriptionPlans()
      if (response.success && response.data) {
        setPlans(response.data)
      } else {
        // Fallback to mock plans
        setPlans([
          {
            id: 'free',
            name: 'Free',
            price: 0,
            currency: 'USD',
            features: [
              '3 voice commands per month',
              'Basic app templates',
              'Community support',
              'Standard generation time'
            ]
          },
          {
            id: 'pro',
            name: 'Pro',
            price: 19,
            currency: 'USD',
            features: [
              'Unlimited voice commands',
              'All app templates',
              'Priority support',
              'Fast generation (30s)',
              'Export to multiple formats',
              'Custom branding'
            ],
            popular: true
          },
          {
            id: 'enterprise',
            name: 'Enterprise',
            price: 99,
            currency: 'USD',
            features: [
              'Everything in Pro',
              'Team collaboration',
              'Advanced analytics',
              'API access',
              'Custom integrations',
              'Dedicated support'
            ]
          }
        ])
      }
    } catch (error) {
      console.error('Failed to load plans:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubscribe = async (planId: string) => {
    if (planId === 'free') {
      // Free plan doesn't require payment
      onPaymentSuccess?.('free-plan')
      return
    }

    try {
      setIsProcessing(true)
      setSelectedPlan(planId)
      
      const plan = plans.find(p => p.id === planId)
      if (!plan) throw new Error('Plan not found')

      const response = await apiService.createPaymentOrder({
        amount: plan.price,
        currency: plan.currency,
        provider: 'razorpay', // Default to Razorpay for Indian market
        description: `${plan.name} subscription`
      })

      if (response.success && response.data) {
        // In a real implementation, you would redirect to payment gateway
        // For now, we'll simulate success
        setTimeout(() => {
          onPaymentSuccess?.(response.data.order_id)
          setIsProcessing(false)
          setSelectedPlan(null)
        }, 2000)
      } else {
        throw new Error(response.error || 'Payment initiation failed')
      }
    } catch (error) {
      console.error('Payment failed:', error)
      onPaymentError?.(error instanceof Error ? error.message : 'Payment failed')
      setIsProcessing(false)
      setSelectedPlan(null)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {plans.map((plan, index) => (
        <motion.div
          key={plan.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="relative"
        >
          {plan.popular && (
            <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
              <Badge className="bg-blue-600 text-white px-3 py-1">
                <Star className="h-3 w-3 mr-1" />
                Most Popular
              </Badge>
            </div>
          )}
          
          <Card className={`h-full ${plan.popular ? 'border-blue-500 shadow-lg' : ''}`}>
            <CardHeader className="text-center">
              <CardTitle className="text-xl">{plan.name}</CardTitle>
              <div className="mt-4">
                <span className="text-4xl font-bold">${plan.price}</span>
                {plan.price > 0 && (
                  <span className="text-gray-500">/month</span>
                )}
              </div>
              <CardDescription className="mt-2">
                {plan.price === 0 ? 'Perfect for getting started' : 
                 plan.price < 50 ? 'Great for individual developers' : 
                 'Perfect for teams and enterprises'}
              </CardDescription>
            </CardHeader>
            
            <CardContent className="space-y-4">
              <ul className="space-y-3">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start space-x-3">
                    <Check className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>
              
              <Button
                className={`w-full ${
                  plan.popular 
                    ? 'bg-blue-600 hover:bg-blue-700' 
                    : plan.price === 0 
                      ? 'bg-gray-600 hover:bg-gray-700' 
                      : 'bg-green-600 hover:bg-green-700'
                }`}
                onClick={() => handleSubscribe(plan.id)}
                disabled={isProcessing && selectedPlan === plan.id}
              >
                {isProcessing && selectedPlan === plan.id ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Processing...
                  </>
                ) : plan.price === 0 ? (
                  'Get Started Free'
                ) : (
                  <>
                    <CreditCard className="h-4 w-4 mr-2" />
                    Subscribe Now
                  </>
                )}
              </Button>
              
              {plan.price > 0 && (
                <p className="text-xs text-gray-500 text-center">
                  Cancel anytime. No hidden fees.
                </p>
              )}
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}
