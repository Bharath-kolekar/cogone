/**
 * Navigation Component
 * Handles authentication state and navigation
 */

'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { User, LogOut, Settings, Menu, X } from 'lucide-react'
import { useAuthContext } from '@/contexts/AuthContext'
import { motion, AnimatePresence } from 'framer-motion'
// import { VoiceDictationToggle } from '@/components/voice-dictation-toggle' // Removed - file deleted (corrupted)
import { useVoiceDictation } from '@/hooks/useVoiceDictation'
import { initializeVoiceCommandMapper } from '@/services/voice-command-mapper'

export function Navigation() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [showVoiceToggle, setShowVoiceToggle] = useState(false)
  const { user, isAuthenticated, logout } = useAuthContext()

  // Initialize voice dictation
  const voiceDictation = useVoiceDictation()

  useEffect(() => {
    // Initialize voice command mapper
    if (voiceDictation.isSupported) {
      initializeVoiceCommandMapper(voiceDictation)
    }
  }, [voiceDictation.isSupported])

  const handleLogout = () => {
    logout()
    setIsMenuOpen(false)
  }

  const handleVoiceCommand = (command: string) => {
    console.log('Voice command received:', command)
    // Voice commands are handled by the voice command mapper
  }

  return (
    <nav className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">V</span>
            </div>
            <span className="text-xl font-bold text-gray-900 dark:text-white">
              Voice-to-App
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <Link 
              href="/features" 
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Features
            </Link>
            <Link 
              href="/pricing" 
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Pricing
            </Link>
            <Link 
              href="/editor" 
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Editor
            </Link>
            <Link 
              href="/docs" 
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Docs
            </Link>
            
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <Link href="/dashboard">
                  <Button variant="outline" size="sm">
                    Dashboard
                  </Button>
                </Link>
                
                <Link href="/editor">
                  <Button variant="outline" size="sm">
                    Editor
                  </Button>
                </Link>
                
                <Link href="/voice-ai">
                  <Button variant="outline" size="sm">
                    Voice AI
                  </Button>
                </Link>
                
                <Link href="/smart-coding-ai">
                  <Button variant="outline" size="sm">
                    Smart Coding AI
                  </Button>
                </Link>
                
                <Link href="/voice-conversation">
                  <Button variant="outline" size="sm">
                    Voice Chat
                  </Button>
                </Link>
                
                <Link href="/super-intelligence">
                  <Button variant="outline" size="sm" className="bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600">
                    Super Intelligence
                  </Button>
                </Link>
                
                {/* Voice Dictation Toggle */}
                {voiceDictation.isSupported && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowVoiceToggle(!showVoiceToggle)}
                    className={voiceDictation.isListening ? 'bg-green-100 dark:bg-green-900/20' : ''}
                  >
                    <div className="flex items-center space-x-2">
                      {voiceDictation.isListening ? (
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                      ) : (
                        <div className="w-2 h-2 bg-gray-400 rounded-full"></div>
                      )}
                      <span className="text-xs">Voice</span>
                    </div>
                  </Button>
                )}
                
                <div className="relative group">
                  <Button variant="ghost" size="sm" className="flex items-center space-x-2">
                    <User className="h-4 w-4" />
                    <span>{user?.name || user?.email}</span>
                  </Button>
                  
                  {/* Dropdown Menu */}
                  <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                    <div className="py-2">
                      <Link 
                        href="/profile" 
                        className="flex items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        <Settings className="h-4 w-4 mr-2" />
                        Profile Settings
                      </Link>
                      <button
                        onClick={handleLogout}
                        className="flex items-center w-full px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        <LogOut className="h-4 w-4 mr-2" />
                        Logout
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link href="/auth">
                  <Button variant="ghost" size="sm">
                    Sign In
                  </Button>
                </Link>
                <Link href="/auth">
                  <Button size="sm">
                    Get Started
                  </Button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden border-t border-gray-200 dark:border-gray-700"
            >
              <div className="py-4 space-y-4">
                <Link 
                  href="/features" 
                  className="block text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Features
                </Link>
                <Link 
                  href="/pricing" 
                  className="block text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Pricing
                </Link>
                    <Link
                      href="/editor"
                      className="block text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Editor
                    </Link>
                    
                    <Link
                      href="/voice-ai"
                      className="block text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Voice AI
                    </Link>
                    
                    <Link
                      href="/super-intelligence"
                      className="block text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Super Intelligence
                    </Link>
                <Link 
                  href="/docs" 
                  className="block text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Docs
                </Link>
                
                {isAuthenticated ? (
                  <div className="space-y-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <Link href="/dashboard" onClick={() => setIsMenuOpen(false)}>
                      <Button variant="outline" className="w-full">
                        Dashboard
                      </Button>
                    </Link>
                    <Link href="/profile" onClick={() => setIsMenuOpen(false)}>
                      <Button variant="ghost" className="w-full justify-start">
                        <Settings className="h-4 w-4 mr-2" />
                        Profile Settings
                      </Button>
                    </Link>
                    <Button
                      variant="ghost"
                      className="w-full justify-start text-red-600 dark:text-red-400"
                      onClick={handleLogout}
                    >
                      <LogOut className="h-4 w-4 mr-2" />
                      Logout
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <Link href="/auth" onClick={() => setIsMenuOpen(false)}>
                      <Button variant="ghost" className="w-full">
                        Sign In
                      </Button>
                    </Link>
                    <Link href="/auth" onClick={() => setIsMenuOpen(false)}>
                      <Button className="w-full">
                        Get Started
                      </Button>
                    </Link>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Voice Dictation Panel */}
      <AnimatePresence>
        {showVoiceToggle && voiceDictation.isSupported && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800"
          >
            <div className="container mx-auto px-4 py-4">
              <div className="text-center text-sm text-muted-foreground">
                Voice Dictation Toggle temporarily disabled (component removed)
              </div>
              {/* <VoiceDictationToggle /> - Component deleted (corrupted) */}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}
