'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Star } from 'lucide-react'
import { motion } from 'framer-motion'

const testimonials = [
  {
    name: "Priya Sharma",
    role: "Small Business Owner",
    location: "Mumbai, Maharashtra",
    avatar: "👩‍💼",
    rating: 5,
    text: "I created my restaurant's ordering app in just 2 minutes! The Hindi voice commands work perfectly. My customers love the easy interface.",
    app: "Restaurant Ordering App"
  },
  {
    name: "Rajesh Kumar",
    role: "Freelance Developer",
    location: "Bangalore, Karnataka",
    avatar: "👨‍💻",
    rating: 5,
    text: "As a developer, I was skeptical about voice-to-app generation. But this platform is incredible! It saves me hours of coding for client prototypes.",
    app: "E-commerce Store"
  },
  {
    name: "Anita Patel",
    role: "Teacher",
    location: "Ahmedabad, Gujarat",
    avatar: "👩‍🏫",
    rating: 5,
    text: "I built a student attendance app for my school using Tamil voice commands. The kids are amazed that their teacher can 'code'!",
    app: "Student Management System"
  },
  {
    name: "Vikram Singh",
    role: "Startup Founder",
    location: "Delhi, NCR",
    avatar: "👨‍🚀",
    rating: 5,
    text: "This platform helped me validate my startup idea quickly. I created 5 different app prototypes in one day using voice commands.",
    app: "Fitness Tracking App"
  },
  {
    name: "Meera Reddy",
    role: "Content Creator",
    location: "Hyderabad, Telangana",
    avatar: "👩‍🎨",
    rating: 5,
    text: "I'm not technical at all, but I created a portfolio website for my art using Telugu voice commands. It's beautiful and works perfectly!",
    app: "Artist Portfolio"
  },
  {
    name: "Arjun Nair",
    role: "Student",
    location: "Kochi, Kerala",
    avatar: "👨‍🎓",
    rating: 5,
    text: "I built a study group app for my college friends using Malayalam voice commands. Everyone is impressed with how professional it looks!",
    app: "Study Group Platform"
  }
]

export function Testimonials() {
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
            Loved by Users Across India
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            See what real users are saying about their voice-to-app experience
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
            >
              <Card className="h-full hover:shadow-lg transition-shadow duration-300 border-0 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700">
                <CardContent className="p-6">
                  <div className="flex items-center space-x-4 mb-4">
                    <div className="text-3xl">{testimonial.avatar}</div>
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                        {testimonial.name}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {testimonial.role}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-500">
                        {testimonial.location}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-1 mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>

                  <blockquote className="text-gray-700 dark:text-gray-300 mb-4 italic">
                    "{testimonial.text}"
                  </blockquote>

                  <div className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs font-medium px-2 py-1 rounded-full inline-block">
                    Created: {testimonial.app}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Stats section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          viewport={{ once: true }}
          className="mt-20"
        >
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-8 text-white text-center">
            <h3 className="text-2xl font-bold mb-8">
              Join Thousands of Happy Users
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div>
                <div className="text-3xl font-bold mb-2">10,000+</div>
                <div className="text-blue-100">Apps Created</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-2">5,000+</div>
                <div className="text-blue-100">Active Users</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-2">15+</div>
                <div className="text-blue-100">Languages Supported</div>
              </div>
              <div>
                <div className="text-3xl font-bold mb-2">4.9/5</div>
                <div className="text-blue-100">User Rating</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Trust indicators */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-8">
            Trusted by users from
          </h3>
          
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">Mumbai</div>
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">Delhi</div>
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">Bangalore</div>
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">Chennai</div>
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">Hyderabad</div>
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">Pune</div>
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">Kolkata</div>
            <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">Ahmedabad</div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}