'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Palette, Layout, Sparkles, Zap, Heart, Brain, Target, Settings, Eye, Activity } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface UIAdaptation {
  id: string
  type: 'color' | 'layout' | 'animation' | 'content' | 'interaction' | 'productivity'
  name: string
  description: string
  mood: string
  intensity: number
  effects: {
    visual: string[]
    behavioral: string[]
    cognitive: string[]
    emotional: string[]
  }
  implementation: {
    css: string
    animations: string[]
    components: string[]
    features: string[]
  }
  metrics: {
    engagement: number
    productivity: number
    satisfaction: number
    retention: number
  }
}

interface AdaptiveUIProps {
  currentMood: string
  moodIntensity: number
  userPreferences?: {
    colorScheme: string
    animationLevel: number
    productivityMode: boolean
    accessibility: boolean
  }
  onAdaptationChange?: (adaptation: UIAdaptation) => void
  className?: string
}

const MOOD_ADAPTATIONS = {
  'happy': {
    colors: {
      primary: '#10B981', // emerald-500
      secondary: '#F59E0B', // amber-500
      accent: '#EC4899', // pink-500
      background: '#F0FDF4', // green-50
      text: '#064E3B' // emerald-900
    },
    animations: ['bounce', 'pulse', 'wiggle'],
    layout: 'spacious',
    content: 'celebratory',
    interactions: 'playful'
  },
  'sad': {
    colors: {
      primary: '#3B82F6', // blue-500
      secondary: '#8B5CF6', // violet-500
      accent: '#06B6D4', // cyan-500
      background: '#EFF6FF', // blue-50
      text: '#1E3A8A' // blue-900
    },
    animations: ['gentle', 'fade'],
    layout: 'comfortable',
    content: 'supportive',
    interactions: 'gentle'
  },
  'stressed': {
    colors: {
      primary: '#059669', // emerald-600
      secondary: '#0D9488', // teal-600
      accent: '#10B981', // emerald-500
      background: '#F0FDFA', // teal-50
      text: '#064E3B' // emerald-900
    },
    animations: ['calm', 'breath'],
    layout: 'minimal',
    content: 'calming',
    interactions: 'smooth'
  },
  'focused': {
    colors: {
      primary: '#1F2937', // gray-800
      secondary: '#374151', // gray-700
      accent: '#3B82F6', // blue-500
      background: '#F9FAFB', // gray-50
      text: '#111827' // gray-900
    },
    animations: ['subtle', 'focus'],
    layout: 'concentrated',
    content: 'productive',
    interactions: 'efficient'
  },
  'excited': {
    colors: {
      primary: '#F59E0B', // amber-500
      secondary: '#EF4444', // red-500
      accent: '#EC4899', // pink-500
      background: '#FFFBEB', // amber-50
      text: '#92400E' // amber-900
    },
    animations: ['energetic', 'sparkle'],
    layout: 'dynamic',
    content: 'motivational',
    interactions: 'responsive'
  },
  'confused': {
    colors: {
      primary: '#8B5CF6', // violet-500
      secondary: '#3B82F6', // blue-500
      accent: '#06B6D4', // cyan-500
      background: '#F5F3FF', // violet-50
      text: '#4C1D95' // violet-900
    },
    animations: ['helpful', 'guide'],
    layout: 'guided',
    content: 'explanatory',
    interactions: 'assistive'
  },
  'motivated': {
    colors: {
      primary: '#DC2626', // red-600
      secondary: '#EA580C', // orange-600
      accent: '#F59E0B', // amber-500
      background: '#FEF2F2', // red-50
      text: '#991B1B' // red-900
    },
    animations: ['dynamic', 'progress'],
    layout: 'achievement',
    content: 'goal-oriented',
    interactions: 'rewarding'
  }
}

export function AdaptiveUISystem({
  currentMood,
  moodIntensity,
  userPreferences = {
    colorScheme: 'auto',
    animationLevel: 1,
    productivityMode: false,
    accessibility: false
  },
  onAdaptationChange,
  className = ''
}: AdaptiveUIProps) {
  const [activeAdaptations, setActiveAdaptations] = useState<UIAdaptation[]>([])
  const [isAdapting, setIsAdapting] = useState(false)
  const [adaptationStep, setAdaptationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [showAdaptations, setShowAdaptations] = useState(false)
  
  const adaptationHistory = useRef<UIAdaptation[]>([])
  const performanceMetrics = useRef<{
    engagement: number
    productivity: number
    satisfaction: number
    retention: number
  }>({
    engagement: 0.7,
    productivity: 0.6,
    satisfaction: 0.8,
    retention: 0.75
    })

  useEffect(() => {
    if (currentMood) {
      generateAdaptations()
    }
  }, [currentMood, moodIntensity, userPreferences])

  const generateAdaptations = useCallback(async () => {
    setIsAdapting(true)
    setProgress(0)
    setAdaptationStep('Analyzing mood and generating UI adaptations...')

    try {
      const steps = [
        'Analyzing current mood state...',
        'Evaluating user preferences...',
        'Generating color adaptations...',
        'Creating layout modifications...',
        'Designing animation sequences...',
        'Optimizing content presentation...',
        'Enhancing interaction patterns...',
        'Calculating productivity boosters...',
        'Implementing accessibility features...',
        'Finalizing adaptive UI...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setAdaptationStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 200))
      }

      const adaptations = await createUIAdaptations()
      setActiveAdaptations(adaptations)
      
      // Apply adaptations to the DOM
      applyAdaptations(adaptations)
      
      // Track adaptation history
      adaptationHistory.current.push(...adaptations)
      if (adaptationHistory.current.length > 100) {
        adaptationHistory.current = adaptationHistory.current.slice(-100)
      }

      // Notify parent component
      adaptations.forEach(adaptation => {
        onAdaptationChange?.(adaptation)
      })

    } catch (error) {
      console.error('UI adaptation failed:', error)
    } finally {
      setIsAdapting(false)
      setProgress(100)
      setAdaptationStep('UI adaptations complete!')
    }
  }, [currentMood, moodIntensity, userPreferences, onAdaptationChange])

  const createUIAdaptations = async (): Promise<UIAdaptation[]> => {
    await new Promise(resolve => setTimeout(resolve, 1000))

    const moodConfig = MOOD_ADAPTATIONS[currentMood as keyof typeof MOOD_ADAPTATIONS] || MOOD_ADAPTATIONS.focused
    const adaptations: UIAdaptation[] = []

    // Color Adaptation
    adaptations.push({
      id: 'color-adaptation',
      type: 'color',
      name: 'Mood-Based Color Scheme',
      description: `Adapting colors to enhance ${currentMood} mood`,
      mood: currentMood,
      intensity: moodIntensity,
      effects: {
        visual: ['Improved visual appeal', 'Enhanced mood alignment', 'Better color harmony'],
        behavioral: ['Increased engagement', 'Better focus', 'Reduced eye strain'],
        cognitive: ['Improved readability', 'Enhanced comprehension', 'Better information processing'],
        emotional: ['Mood enhancement', 'Emotional comfort', 'Positive associations']
      },
      implementation: {
        css: generateColorCSS(moodConfig.colors),
        animations: moodConfig.animations,
        components: ['buttons', 'cards', 'backgrounds', 'text'],
        features: ['dynamic-theming', 'mood-colors', 'adaptive-palette']
      },
      metrics: {
        engagement: 0.8,
        productivity: 0.6,
        satisfaction: 0.9,
        retention: 0.7
      }
    })

    // Layout Adaptation
    adaptations.push({
      id: 'layout-adaptation',
      type: 'layout',
      name: 'Adaptive Layout System',
      description: `Optimizing layout for ${currentMood} mood and productivity`,
      mood: currentMood,
      intensity: moodIntensity,
      effects: {
        visual: ['Better space utilization', 'Improved visual hierarchy', 'Enhanced readability'],
        behavioral: ['Faster task completion', 'Reduced cognitive load', 'Improved workflow'],
        cognitive: ['Better information organization', 'Enhanced focus', 'Reduced distractions'],
        emotional: ['Reduced stress', 'Increased comfort', 'Better user experience']
      },
      implementation: {
        css: generateLayoutCSS(moodConfig.layout, moodIntensity),
        animations: ['smooth-transitions', 'layout-shifts'],
        components: ['grid', 'flexbox', 'spacing', 'typography'],
        features: ['responsive-layout', 'adaptive-spacing', 'mood-layout']
      },
      metrics: {
        engagement: 0.7,
        productivity: 0.8,
        satisfaction: 0.8,
        retention: 0.75
      }
    })

    // Animation Adaptation
    adaptations.push({
      id: 'animation-adaptation',
      type: 'animation',
      name: 'Mood-Responsive Animations',
      description: `Adding animations that complement ${currentMood} mood`,
      mood: currentMood,
      intensity: moodIntensity,
      effects: {
        visual: ['Enhanced visual feedback', 'Smoother interactions', 'Better user guidance'],
        behavioral: ['Increased engagement', 'Improved task flow', 'Better user feedback'],
        cognitive: ['Reduced cognitive load', 'Enhanced understanding', 'Better visual cues'],
        emotional: ['Mood enhancement', 'Positive interactions', 'Emotional engagement']
      },
      implementation: {
        css: generateAnimationCSS(moodConfig.animations, moodIntensity),
        animations: moodConfig.animations,
        components: ['transitions', 'hover-effects', 'loading-states'],
        features: ['mood-animations', 'adaptive-timing', 'emotion-driven-motion']
      },
      metrics: {
        engagement: 0.9,
        productivity: 0.5,
        satisfaction: 0.85,
        retention: 0.8
      }
    })

    // Productivity Adaptation
    if (userPreferences.productivityMode || currentMood === 'focused') {
      adaptations.push({
        id: 'productivity-adaptation',
        type: 'productivity',
        name: 'Productivity Enhancement',
        description: 'Optimizing interface for maximum productivity',
        mood: currentMood,
        intensity: moodIntensity,
        effects: {
          visual: ['Reduced distractions', 'Enhanced focus areas', 'Clear task indicators'],
          behavioral: ['Faster task completion', 'Improved workflow', 'Better time management'],
          cognitive: ['Enhanced focus', 'Reduced cognitive load', 'Better task organization'],
          emotional: ['Increased motivation', 'Achievement satisfaction', 'Progress visibility']
        },
        implementation: {
          css: generateProductivityCSS(moodIntensity),
          animations: ['focus-indicators', 'progress-animations'],
          components: ['task-lists', 'progress-bars', 'focus-modes'],
          features: ['distraction-blocking', 'focus-mode', 'productivity-tracking']
        },
        metrics: {
          engagement: 0.6,
          productivity: 0.95,
          satisfaction: 0.8,
          retention: 0.85
        }
      })
    }

    return adaptations
  }

  const generateColorCSS = (colors: any): string => {
    return `
      :root {
        --mood-primary: ${colors.primary};
        --mood-secondary: ${colors.secondary};
        --mood-accent: ${colors.accent};
        --mood-background: ${colors.background};
        --mood-text: ${colors.text};
      }
      
      .mood-adaptive {
        background-color: var(--mood-background);
        color: var(--mood-text);
      }
      
      .mood-primary {
        background-color: var(--mood-primary);
        color: white;
      }
      
      .mood-secondary {
        background-color: var(--mood-secondary);
        color: white;
      }
      
      .mood-accent {
        background-color: var(--mood-accent);
        color: white;
      }
    `
  }

  const generateLayoutCSS = (layout: string, intensity: number): string => {
    const spacing = intensity > 0.7 ? '2rem' : intensity > 0.4 ? '1.5rem' : '1rem'
    const padding = intensity > 0.7 ? '3rem' : intensity > 0.4 ? '2rem' : '1rem'
    
    return `
      .adaptive-layout {
        padding: ${padding};
        gap: ${spacing};
        transition: all 0.3s ease;
      }
      
      .adaptive-spacing {
        margin: ${spacing};
        padding: ${spacing};
      }
      
      .adaptive-grid {
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: ${spacing};
      }
    `
  }

  const generateAnimationCSS = (animations: string[], intensity: number): string => {
    const duration = intensity > 0.7 ? '0.3s' : intensity > 0.4 ? '0.5s' : '0.7s'
    const easing = intensity > 0.7 ? 'cubic-bezier(0.4, 0, 0.2, 1)' : 'ease-in-out'
    
    return `
      .mood-animation {
        transition: all ${duration} ${easing};
      }
      
      .mood-hover:hover {
        transform: scale(1.05);
        transition: transform 0.2s ease;
      }
      
      .mood-focus:focus {
        box-shadow: 0 0 0 3px var(--mood-accent);
        transition: box-shadow 0.2s ease;
      }
    `
  }

  const generateProductivityCSS = (intensity: number): string => {
    return `
      .productivity-mode {
        filter: grayscale(0.1);
        background-color: #f8fafc;
      }
      
      .focus-area {
        border: 2px solid var(--mood-primary);
        border-radius: 8px;
        padding: 1rem;
        background-color: rgba(59, 130, 246, 0.05);
      }
      
      .distraction-reduced {
        opacity: 0.6;
        pointer-events: none;
      }
    `
  }

  const applyAdaptations = (adaptations: UIAdaptation[]) => {
    // Create or update style element
    let styleElement = document.getElementById('adaptive-ui-styles') as HTMLStyleElement
    if (!styleElement) {
      styleElement = document.createElement('style')
      styleElement.id = 'adaptive-ui-styles'
      document.head.appendChild(styleElement)
    }

    // Combine all CSS
    const combinedCSS = adaptations
      .map(adaptation => adaptation.implementation.css)
      .join('\n')

    styleElement.textContent = combinedCSS

    // Apply classes to body
    document.body.className = document.body.className
      .replace(/mood-\w+/g, '')
      .replace(/adaptive-\w+/g, '')
      .trim()

    document.body.classList.add('mood-adaptive', 'adaptive-layout', 'mood-animation')

    // Add mood-specific class
    document.body.classList.add(`mood-${currentMood}`)

    // Add productivity mode if enabled
    if (userPreferences.productivityMode || currentMood === 'focused') {
      document.body.classList.add('productivity-mode')
    }
  }

  const getAdaptationIcon = (type: string) => {
    const icons = {
      'color': Palette,
      'layout': Layout,
      'animation': Sparkles,
      'content': Brain,
      'interaction': Zap,
      'productivity': Target
    }
    return icons[type as keyof typeof icons] || Settings
  }

  const getAdaptationColor = (type: string) => {
    const colors = {
      'color': 'text-blue-600 bg-blue-100',
      'layout': 'text-green-600 bg-green-100',
      'animation': 'text-purple-600 bg-purple-100',
      'content': 'text-orange-600 bg-orange-100',
      'interaction': 'text-pink-600 bg-pink-100',
      'productivity': 'text-red-600 bg-red-100'
    }
    return colors[type as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Adaptation Status */}
      {isAdapting && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
              {adaptationStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Active Adaptations */}
      {activeAdaptations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">Active UI Adaptations</h3>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowAdaptations(!showAdaptations)}
            >
              {showAdaptations ? 'Hide' : 'Show'} Details
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {activeAdaptations.map((adaptation) => {
              const Icon = getAdaptationIcon(adaptation.type)
              return (
                <Card key={adaptation.id} className="mood-adaptive">
                  <CardHeader>
                    <CardTitle className="text-sm flex items-center space-x-2">
                      <Icon className="h-4 w-4" />
                      <span>{adaptation.name}</span>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      {adaptation.description}
                    </p>
                    
                    <div className="flex flex-wrap gap-2 mb-3">
                      <Badge className={getAdaptationColor(adaptation.type)}>
                        {adaptation.type}
                      </Badge>
                      <Badge variant="outline">
                        {adaptation.mood}
                      </Badge>
                      <Badge variant="outline">
                        {(adaptation.intensity * 100).toFixed(0)}% intensity
                      </Badge>
                    </div>

                    {showAdaptations && (
                      <div className="space-y-3">
                        <div>
                          <h4 className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Effects
                          </h4>
                          <div className="space-y-1">
                            {Object.entries(adaptation.effects).map(([category, effects]) => (
                              <div key={category}>
                                <div className="text-xs font-medium capitalize text-gray-600 dark:text-gray-400">
                                  {category}:
                                </div>
                                <ul className="text-xs text-gray-500 dark:text-gray-500 ml-2">
                                  {effects.slice(0, 2).map((effect, index) => (
                                    <li key={index}>• {effect}</li>
                                  ))}
                                </ul>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h4 className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                            Performance Metrics
                          </h4>
                          <div className="grid grid-cols-2 gap-2">
                            {Object.entries(adaptation.metrics).map(([metric, value]) => (
                              <div key={metric} className="text-center">
                                <div className="text-xs font-medium capitalize">{metric}</div>
                                <div className="text-sm font-bold text-blue-600">
                                  {(value * 100).toFixed(0)}%
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )
            })}
          </div>

          {/* Performance Overview */}
          <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20">
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Activity className="h-4 w-4" />
                <span>Adaptation Performance</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(performanceMetrics.current).map(([metric, value]) => (
                  <div key={metric} className="text-center">
                    <div className="text-2xl font-bold text-blue-600">
                      {(value * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400 capitalize">
                      {metric}
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div 
                        className="bg-blue-500 h-2 rounded-full"
                        style={{ width: `${value * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  )
}
