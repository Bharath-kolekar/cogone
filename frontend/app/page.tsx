import { Hero } from '@/components/hero'
import { Features } from '@/components/features'
import { Pricing } from '@/components/pricing'
import { Testimonials } from '@/components/testimonials'
import { CTA } from '@/components/cta'
import { LanguageToggle } from '@/components/language-toggle'

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Features />
      <Pricing />
      <Testimonials />
      <CTA />
    </main>
  )
}