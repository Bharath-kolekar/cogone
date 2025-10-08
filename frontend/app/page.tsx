import { NeuralEnhancedHero } from '@/components/vfx/neural-enhanced-hero'
import { NeuralEnhancedFeatures } from '@/components/vfx/neural-enhanced-features'
import { NeuralEnhancedPricing } from '@/components/vfx/neural-enhanced-pricing'
import { NeuralEnhancedTestimonials } from '@/components/vfx/neural-enhanced-testimonials'
import { CTA } from '@/components/cta'
import { NeuralEnhancedNavigation } from '@/components/vfx/neural-enhanced-navigation'
import { LanguageToggle } from '@/components/language-toggle'
import { NeuralNLPDashboard } from '@/components/nlp/neural-nlp-dashboard'
import { SmartCodingDashboard } from '@/components/smart-coding/smart-coding-dashboard'
import { AdvancedSmartCodingDashboard } from '@/components/smart-coding/advanced-smart-coding-dashboard'
import { SmartCodingAILiveDemo } from '@/components/SmartCodingAILiveDemo'
import { UnifiedAdvancedDashboard } from '@/components/smart-coding/unified-advanced-dashboard'

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <NeuralEnhancedNavigation />
      <NeuralEnhancedHero />
      <NeuralEnhancedFeatures />
      <NeuralEnhancedPricing />
      <NeuralEnhancedTestimonials />
      <CTA />
      
      {/* Advanced NLP Demo Section */}
      <section className="py-16 bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 dark:from-purple-900/20 dark:via-blue-900/20 dark:to-indigo-900/20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Advanced NLP Intelligence
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Experience the power of neural language processing with real-time analysis, 
              sentiment detection, entity extraction, and intelligent text generation.
            </p>
          </div>
          
          <div className="max-w-6xl mx-auto">
            <NeuralNLPDashboard
              initialText="Hello! I'm excited to demonstrate our advanced NLP capabilities. This system can analyze text, detect emotions, extract entities, and generate intelligent responses in real-time."
              enableRealTime={true}
              showAllFeatures={true}
              onAnalysisComplete={(result) => {
                console.log('NLP Analysis Complete:', result)
              }}
            />
          </div>
        </div>
      </section>

      {/* Smart Coding AI Demo Section */}
      <section className="py-16 bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 dark:from-green-900/20 dark:via-blue-900/20 dark:to-purple-900/20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Smart Coding AI Assistant
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Experience the future of coding with AI that understands your codebase, 
              generates precise diffs, coordinates multi-file changes, and provides intelligent debugging.
            </p>
          </div>
          
          <div className="max-w-7xl mx-auto">
            <AdvancedSmartCodingDashboard
              showAllFeatures={true}
              enableRealTimeGeneration={true}
              onCodeGenerated={(result) => {
                console.log('Advanced Smart Coding AI Generated:', result)
              }}
            />
          </div>
        </div>
      </section>

      {/* Live Six Sigma Quality Pipeline Demo */}
      <section className="py-16 bg-gradient-to-br from-gray-950 via-gray-900 to-black text-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <div className="inline-block mb-4">
              <span className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full text-sm font-semibold">
                🎯 Six Sigma Quality • 99.99966%+ Accuracy
              </span>
            </div>
            <h2 className="text-3xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Watch Cognomega Work in Real-Time
            </h2>
            <p className="text-lg text-gray-300 max-w-3xl mx-auto mb-2">
              See every validation step, proactive correction, and quality gate as Cognomega generates 
              100% accurate code with zero drift from your intent.
            </p>
            <p className="text-sm text-gray-400 max-w-2xl mx-auto">
              ✨ Auto-starts on page load • 🔄 Live WebSocket streaming • 🛠️ Proactive error correction • 
              📊 Complete transparency
            </p>
          </div>
          
          <div className="max-w-7xl mx-auto">
            <SmartCodingAILiveDemo autoStart={true} autoTriggerDemo={true} />
          </div>

          {/* Feature Highlights */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-6 max-w-6xl mx-auto">
            <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/30 p-6 rounded-xl border border-blue-700/50 text-center">
              <div className="text-3xl mb-3">⚡</div>
              <h3 className="text-lg font-semibold mb-2">Real-time</h3>
              <p className="text-sm text-gray-400">
                Instant updates via WebSocket
              </p>
            </div>
            <div className="bg-gradient-to-br from-purple-900/30 to-purple-800/30 p-6 rounded-xl border border-purple-700/50 text-center">
              <div className="text-3xl mb-3">🎯</div>
              <h3 className="text-lg font-semibold mb-2">Six Sigma</h3>
              <p className="text-sm text-gray-400">
                99.99966%+ accuracy
              </p>
            </div>
            <div className="bg-gradient-to-br from-green-900/30 to-green-800/30 p-6 rounded-xl border border-green-700/50 text-center">
              <div className="text-3xl mb-3">🛠️</div>
              <h3 className="text-lg font-semibold mb-2">Proactive</h3>
              <p className="text-sm text-gray-400">
                Auto-fix before delivery
              </p>
            </div>
            <div className="bg-gradient-to-br from-pink-900/30 to-pink-800/30 p-6 rounded-xl border border-pink-700/50 text-center">
              <div className="text-3xl mb-3">🎨</div>
              <h3 className="text-lg font-semibold mb-2">Zero Drift</h3>
              <p className="text-sm text-gray-400">
                Perfect goal alignment
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Advanced AI Features Section - NEW */}
      <section className="py-16 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 dark:from-indigo-900/20 dark:via-purple-900/20 dark:to-pink-900/20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Advanced AI Features
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Multi-agent code review, gap detection & resolution, 11-validator system, 
              consciousness-level AI, and autonomous learning - all integrated for maximum code quality.
            </p>
          </div>
          
          <div className="max-w-7xl mx-auto">
            <UnifiedAdvancedDashboard />
          </div>
        </div>
      </section>
    </main>
  )
}