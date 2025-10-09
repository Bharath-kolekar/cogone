'use client'

import { NeuralEnhancedHero } from '@/components/vfx/neural-enhanced-hero'
import { NeuralEnhancedFeatures } from '@/components/vfx/neural-enhanced-features'
import { NeuralEnhancedPricing } from '@/components/vfx/neural-enhanced-pricing'
import { NeuralEnhancedTestimonials } from '@/components/vfx/neural-enhanced-testimonials'
import { CTA } from '@/components/cta'
import { NeuralEnhancedNavigation } from '@/components/vfx/neural-enhanced-navigation'
import { LanguageToggle } from '@/components/language-toggle'
import { SmartCodingAILiveDemo } from '@/components/SmartCodingAILiveDemo'

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <NeuralEnhancedNavigation />
      <LanguageToggle />
      
      {/* Hero Section */}
      <section id="hero">
        <NeuralEnhancedHero />
      </section>

      {/* Features Section */}
      <section id="features" className="py-20">
        <NeuralEnhancedFeatures />
      </section>

      {/* Live Demo Section */}
      <section id="demo" className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">
            Try Our Smart Coding AI
          </h2>
          <SmartCodingAILiveDemo />
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20">
        <NeuralEnhancedPricing />
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 bg-gray-50 dark:bg-gray-900">
        <NeuralEnhancedTestimonials />
      </section>

      {/* CTA Section */}
      <section id="cta">
        <CTA />
      </section>

      {/* Note about removed components */}
      <div className="py-8 bg-blue-50 dark:bg-blue-900/20">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>Some advanced features temporarily disabled during cleanup</p>
          <p className="mt-1">Core functionality available - Advanced features coming soon!</p>
        </div>
      </div>
    </main>
  )
}
