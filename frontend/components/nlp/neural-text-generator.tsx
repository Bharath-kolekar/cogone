'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Zap, Sparkles, Target, Wand2, Lightbulb, Copy, Download, RefreshCw } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Textarea } from '@/components/ui/textarea'

interface TextGenerationResult {
  generated: string
  confidence: number
  creativity: number
  coherence: number
  relevance: number
  style: {
    tone: string
    formality: string
    complexity: string
  }
  suggestions: Array<{
    type: 'improvement' | 'alternative' | 'enhancement'
    text: string
    reason: string
  }>
  metadata: {
    wordCount: number
    readingTime: number
    language: string
    topics: string[]
  }
}

interface NeuralTextGeneratorProps {
  prompt: string
  onGenerationComplete?: (result: TextGenerationResult) => void
  showSuggestions?: boolean
  enableRealTime?: boolean
  maxLength?: number
  creativity?: number
  className?: string
}

const GENERATION_STYLES = [
  { name: 'Creative', description: 'Imaginative and original content', icon: Sparkles },
  { name: 'Professional', description: 'Formal and business-appropriate', icon: Target },
  { name: 'Casual', description: 'Conversational and friendly', icon: Lightbulb },
  { name: 'Academic', description: 'Scholarly and research-oriented', icon: Brain },
  { name: 'Technical', description: 'Precise and detailed', icon: Zap }
]

const GENERATION_TYPES = [
  { name: 'Continue', description: 'Continue the existing text' },
  { name: 'Summarize', description: 'Create a summary' },
  { name: 'Expand', description: 'Expand on the topic' },
  { name: 'Rewrite', description: 'Rewrite in different style' },
  { name: 'Translate', description: 'Translate to another language' },
  { name: 'Explain', description: 'Explain in simple terms' }
]

export function NeuralTextGenerator({
  prompt,
  onGenerationComplete,
  showSuggestions = true,
  enableRealTime = true,
  maxLength = 500,
  creativity = 0.7,
  className = ''
}: NeuralTextGeneratorProps) {
  const [result, setResult] = useState<TextGenerationResult | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStep, setGenerationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [selectedStyle, setSelectedStyle] = useState('Creative')
  const [selectedType, setSelectedType] = useState('Continue')
  const [customPrompt, setCustomPrompt] = useState(prompt)
  const [showDetails, setShowDetails] = useState(false)
  const generationRef = useRef<TextGenerationResult | null>(null)

  useEffect(() => {
    if (prompt && enableRealTime) {
      setCustomPrompt(prompt)
      generateText(prompt)
    }
  }, [prompt, enableRealTime])

  const generateText = async (inputPrompt: string) => {
    setIsGenerating(true)
    setProgress(0)
    setGenerationStep('Initializing neural text generation...')

    try {
      // Simulate real-time generation steps
      const steps = [
        'Analyzing input prompt...',
        'Processing context and style...',
        'Generating neural patterns...',
        'Creating coherent content...',
        'Optimizing for readability...',
        'Enhancing creativity...',
        'Validating coherence...',
        'Generating suggestions...',
        'Calculating metrics...',
        'Finalizing output...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setGenerationStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Perform text generation
      const generationResult = await performTextGeneration(inputPrompt)
      
      setResult(generationResult)
      generationRef.current = generationResult
      onGenerationComplete?.(generationResult)
      
    } catch (error) {
      console.error('Text generation failed:', error)
    } finally {
      setIsGenerating(false)
      setProgress(100)
      setGenerationStep('Generation complete!')
    }
  }

  const performTextGeneration = async (inputPrompt: string): Promise<TextGenerationResult> => {
    // Simulate advanced text generation
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Mock text generation based on prompt and style
    const style = selectedStyle.toLowerCase()
    const type = selectedType.toLowerCase()
    
    let generatedText = ''
    
    if (type === 'continue') {
      generatedText = generateContinuation(inputPrompt, style)
    } else if (type === 'summarize') {
      generatedText = generateSummary(inputPrompt, style)
    } else if (type === 'expand') {
      generatedText = generateExpansion(inputPrompt, style)
    } else if (type === 'rewrite') {
      generatedText = generateRewrite(inputPrompt, style)
    } else if (type === 'explain') {
      generatedText = generateExplanation(inputPrompt, style)
    } else {
      generatedText = generateDefault(inputPrompt, style)
    }

    // Calculate metrics
    const wordCount = generatedText.split(/\s+/).length
    const readingTime = Math.ceil(wordCount / 200) // Average reading speed
    
    // Generate suggestions
    const suggestions = [
      {
        type: 'improvement' as const,
        text: 'Add more specific examples to strengthen your point',
        reason: 'Examples make content more convincing'
      },
      {
        type: 'alternative' as const,
        text: 'Consider a more conversational tone',
        reason: 'Might improve engagement'
      },
      {
        type: 'enhancement' as const,
        text: 'Include relevant statistics or data',
        reason: 'Data supports your arguments'
      }
    ]

    // Extract topics (simple keyword extraction)
    const topics = inputPrompt.toLowerCase().split(/\s+/)
      .filter(word => word.length > 3)
      .slice(0, 5)

    return {
      generated: generatedText,
      confidence: 0.85 + Math.random() * 0.1,
      creativity: creativity + Math.random() * 0.2,
      coherence: 0.8 + Math.random() * 0.15,
      relevance: 0.75 + Math.random() * 0.2,
      style: {
        tone: style,
        formality: style === 'professional' ? 'formal' : 'informal',
        complexity: style === 'academic' ? 'high' : 'medium'
      },
      suggestions,
      metadata: {
        wordCount,
        readingTime,
        language: 'en',
        topics
      }
    }
  }

  const generateContinuation = (prompt: string, style: string): string => {
    const continuations = {
      creative: `Building upon this foundation, we can explore innovative approaches that push the boundaries of conventional thinking. The possibilities are endless when we combine creativity with strategic planning.`,
      professional: `Furthermore, this approach aligns with industry best practices and provides a solid framework for implementation. The systematic methodology ensures consistent results across all projects.`,
      casual: `And that's just the beginning! There's so much more we can explore together. Let's dive deeper and see what amazing things we can discover.`,
      academic: `This analysis reveals significant implications for future research directions. The theoretical framework provides a robust foundation for empirical investigation and hypothesis testing.`,
      technical: `The implementation details include specific algorithms and data structures that optimize performance. The technical specifications ensure scalability and maintainability.`
    }
    return continuations[style as keyof typeof continuations] || continuations.creative
  }

  const generateSummary = (prompt: string, style: string): string => {
    return `In summary, the key points discussed include the main concepts, their practical applications, and the potential impact on future developments. This comprehensive overview provides a clear understanding of the topic.`
  }

  const generateExpansion = (prompt: string, style: string): string => {
    return `Expanding on this topic, we can explore multiple dimensions including historical context, current trends, future implications, and practical applications. Each aspect offers unique insights and opportunities for deeper understanding.`
  }

  const generateRewrite = (prompt: string, style: string): string => {
    return `This content has been reimagined with a fresh perspective, maintaining the core message while presenting it in a more engaging and accessible format. The new approach enhances clarity and impact.`
  }

  const generateExplanation = (prompt: string, style: string): string => {
    return `Let me break this down in simple terms: the concept works by following a logical sequence of steps, each building upon the previous one. This approach makes complex ideas more accessible and easier to understand.`
  }

  const generateDefault = (prompt: string, style: string): string => {
    return `Based on your input, here's a comprehensive response that addresses the key points while maintaining the appropriate tone and style for your specific needs.`
  }

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      // You could add a toast notification here
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
  }

  const downloadText = (text: string) => {
    const blob = new Blob([text], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'generated-text.txt'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getStyleIcon = (styleName: string) => {
    const style = GENERATION_STYLES.find(s => s.name === styleName)
    return style?.icon || Brain
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Generation Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Wand2 className="h-5 w-5 text-purple-600" />
            <span>Text Generation Settings</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Custom Prompt */}
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
              Custom Prompt
            </label>
            <Textarea
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              placeholder="Enter your prompt here..."
              className="min-h-[100px]"
            />
          </div>

          {/* Style Selection */}
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
              Generation Style
            </label>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
              {GENERATION_STYLES.map((style) => {
                const Icon = style.icon
                return (
                  <Button
                    key={style.name}
                    variant={selectedStyle === style.name ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedStyle(style.name)}
                    className="flex flex-col items-center space-y-1 h-auto py-3"
                  >
                    <Icon className="h-4 w-4" />
                    <span className="text-xs">{style.name}</span>
                  </Button>
                )
              })}
            </div>
          </div>

          {/* Type Selection */}
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
              Generation Type
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {GENERATION_TYPES.map((type) => (
                <Button
                  key={type.name}
                  variant={selectedType === type.name ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedType(type.name)}
                  className="text-xs"
                >
                  {type.name}
                </Button>
              ))}
            </div>
          </div>

          {/* Generate Button */}
          <Button
            onClick={() => generateText(customPrompt)}
            disabled={isGenerating || !customPrompt.trim()}
            className="w-full"
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4 mr-2" />
                Generate Text
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Generation Status */}
      {isGenerating && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-600"></div>
            <span className="text-sm font-medium text-purple-800 dark:text-purple-200">
              {generationStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Generation Results */}
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Generated Text */}
          <Card className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-purple-600" />
                  <span>Generated Text</span>
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => copyToClipboard(result.generated)}
                  >
                    <Copy className="h-4 w-4 mr-1" />
                    Copy
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => downloadText(result.generated)}
                  >
                    <Download className="h-4 w-4 mr-1" />
                    Download
                  </Button>
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose dark:prose-invert max-w-none">
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                  {result.generated}
                </p>
              </div>
              
              <div className="flex flex-wrap gap-2 mt-4">
                <Badge className={getConfidenceColor(result.confidence)}>
                  {(result.confidence * 100).toFixed(1)}% confidence
                </Badge>
                <Badge variant="outline">
                  {result.metadata.wordCount} words
                </Badge>
                <Badge variant="outline">
                  {result.metadata.readingTime} min read
                </Badge>
                <Badge variant="outline">
                  {result.style.tone} tone
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Quality Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Sparkles className="h-4 w-4" />
                  <span>Creativity</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-purple-600">
                  {(result.creativity * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-purple-500 h-2 rounded-full"
                    style={{ width: `${result.creativity * 100}%` }}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Brain className="h-4 w-4" />
                  <span>Coherence</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-blue-600">
                  {(result.coherence * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full"
                    style={{ width: `${result.coherence * 100}%` }}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Relevance</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-green-600">
                  {(result.relevance * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full"
                    style={{ width: `${result.relevance * 100}%` }}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-3">
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Zap className="h-4 w-4" />
                  <span>Quality</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-yellow-600">
                  {((result.confidence + result.coherence + result.relevance) / 3 * 100).toFixed(0)}%
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-yellow-500 h-2 rounded-full"
                    style={{ width: `${((result.confidence + result.coherence + result.relevance) / 3 * 100)}%` }}
                  />
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Suggestions */}
          {showSuggestions && result.suggestions.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Improvement Suggestions</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {result.suggestions.map((suggestion, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <Badge variant="outline" className="capitalize">
                        {suggestion.type}
                      </Badge>
                      <div className="flex-1">
                        <div className="font-medium">{suggestion.text}</div>
                        <div className="text-sm text-gray-600 dark:text-gray-400">{suggestion.reason}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Regenerate Button */}
          <div className="text-center">
            <Button
              variant="outline"
              onClick={() => generateText(customPrompt)}
              disabled={isGenerating}
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Regenerate
            </Button>
          </div>
        </motion.div>
      )}
    </div>
  )
}
