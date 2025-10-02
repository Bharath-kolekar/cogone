'use client'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Mic, ArrowRight, Download, Share2 } from 'lucide-react'
import { motion } from 'framer-motion'

export function CTA() {
  return (
    <section className="py-20 bg-gradient-to-br from-blue-600 to-purple-700">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Ready to Build Your First App?
          </h2>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto mb-8">
            Join thousands of users who are already creating amazing apps with just their voice. 
            Start free, no credit card required.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          {/* Main CTA */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <Card className="bg-white/10 backdrop-blur-sm border-white/20 text-white">
              <CardHeader className="text-center">
                <div className="mx-auto w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mb-4">
                  <Mic className="h-8 w-8 text-white" />
                </div>
                <CardTitle className="text-2xl font-bold text-white">
                  Start Creating Now
                </CardTitle>
                <CardDescription className="text-blue-100">
                  Try the voice-to-app experience right here
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 text-white">
                    <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-xs font-bold">1</span>
                    </div>
                    <span>Click the microphone button</span>
                  </div>
                  <div className="flex items-center space-x-3 text-white">
                    <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-xs font-bold">2</span>
                    </div>
                    <span>Speak your app idea in any language</span>
                  </div>
                  <div className="flex items-center space-x-3 text-white">
                    <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-xs font-bold">3</span>
                    </div>
                    <span>Watch your app come to life in 30 seconds</span>
                  </div>
                </div>

                <Button 
                  size="lg" 
                  className="w-full bg-white text-blue-600 hover:bg-blue-50 font-semibold py-4 text-lg"
                >
                  <Mic className="h-5 w-5 mr-2" />
                  Try Voice-to-App Demo
                  <ArrowRight className="h-5 w-5 ml-2" />
                </Button>

                <p className="text-blue-100 text-sm text-center">
                  No signup required for the demo • Works in Hindi, English, Tamil & more
                </p>
              </CardContent>
            </Card>
          </motion.div>

          {/* Benefits */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            viewport={{ once: true }}
            className="space-y-6"
          >
            <Card className="bg-white/10 backdrop-blur-sm border-white/20">
              <CardContent className="p-6">
                <h3 className="text-xl font-bold text-white mb-4">
                  🚀 Why Start Today?
                </h3>
                <ul className="space-y-3 text-blue-100">
                  <li className="flex items-start space-x-3">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Create your first 3 apps completely free</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>No coding knowledge required</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Works in 10+ Indian languages</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Mobile-optimized for Indian users</span>
                  </li>
                  <li className="flex items-start space-x-3">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>Export code or deploy instantly</span>
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-white/10 backdrop-blur-sm border-white/20">
              <CardContent className="p-6">
                <h3 className="text-xl font-bold text-white mb-4">
                  📱 Perfect for Everyone
                </h3>
                <div className="grid grid-cols-2 gap-4 text-blue-100">
                  <div>
                    <h4 className="font-semibold text-white mb-2">👨‍💼 Business Owners</h4>
                    <p className="text-sm">Create apps for your business without hiring developers</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-2">👨‍💻 Developers</h4>
                    <p className="text-sm">Rapidly prototype ideas and save development time</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-2">👩‍🎓 Students</h4>
                    <p className="text-sm">Learn app development concepts through voice commands</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-2">👨‍🚀 Entrepreneurs</h4>
                    <p className="text-sm">Validate ideas quickly with working prototypes</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                variant="outline" 
                size="lg"
                className="flex-1 bg-transparent border-white text-white hover:bg-white hover:text-blue-600"
              >
                <Download className="h-5 w-5 mr-2" />
                Download App
              </Button>
              <Button 
                variant="outline" 
                size="lg"
                className="flex-1 bg-transparent border-white text-white hover:bg-white hover:text-blue-600"
              >
                <Share2 className="h-5 w-5 mr-2" />
                Share with Friends
              </Button>
            </div>
          </motion.div>
        </div>

        {/* Social proof */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <p className="text-blue-100 mb-8">
            Trusted by users across India
          </p>
          
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-80">
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-white font-semibold">Mumbai</div>
              <div className="text-blue-100 text-sm">2,500+ users</div>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-white font-semibold">Delhi</div>
              <div className="text-blue-100 text-sm">2,200+ users</div>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-white font-semibold">Bangalore</div>
              <div className="text-blue-100 text-sm">1,800+ users</div>
            </div>
            <div className="bg-white/20 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-white font-semibold">Chennai</div>
              <div className="text-blue-100 text-sm">1,500+ users</div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}