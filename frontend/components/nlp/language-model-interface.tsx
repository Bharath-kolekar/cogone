'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Zap, Settings, Play, Pause, RotateCcw, Download, Upload, Target, TrendingUp, BarChart3, Activity } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Textarea } from '@/components/ui/textarea'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Slider } from '@/components/ui/slider'

interface LanguageModelConfig {
  model: string
  temperature: number
  maxTokens: number
  topP: number
  frequencyPenalty: number
  presencePenalty: number
  stopSequences: string[]
  systemPrompt: string
}

interface ModelResponse {
  text: string
  tokens: number
  finishReason: string
  confidence: number
  processingTime: number
  model: string
  timestamp: Date
}

interface LanguageModelInterfaceProps {
  onResponse?: (response: ModelResponse) => void
  showConfig?: boolean
  enableStreaming?: boolean
  className?: string
}

const AVAILABLE_MODELS = [
  { id: 'gpt-4', name: 'GPT-4', description: 'Most capable model', maxTokens: 8192, cost: 'high' },
  { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', description: 'Fast and efficient', maxTokens: 4096, cost: 'medium' },
  { id: 'claude-3', name: 'Claude 3', description: 'Anthropic\'s latest', maxTokens: 200000, cost: 'high' },
  { id: 'llama-2', name: 'Llama 2', description: 'Open source model', maxTokens: 4096, cost: 'low' },
  { id: 'mistral', name: 'Mistral', description: 'European model', maxTokens: 8192, cost: 'medium' },
  { id: 'local', name: 'Local Model', description: 'On-device processing', maxTokens: 2048, cost: 'free' }
]

const SYSTEM_PROMPTS = {
  'assistant': 'You are a helpful AI assistant. Provide clear, accurate, and helpful responses.',
  'creative': 'You are a creative writing assistant. Help with storytelling, poetry, and creative content.',
  'technical': 'You are a technical expert. Provide detailed technical explanations and solutions.',
  'business': 'You are a business consultant. Provide strategic advice and analysis.',
  'educational': 'You are an educational tutor. Explain concepts clearly and provide learning guidance.',
  'code': 'You are a programming assistant. Help with coding, debugging, and software development.'
}

export function LanguageModelInterface({
  onResponse,
  showConfig = true,
  enableStreaming = true,
  className = ''
}: LanguageModelInterfaceProps) {
  const [prompt, setPrompt] = useState('')
  const [response, setResponse] = useState<ModelResponse | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [streamingText, setStreamingText] = useState('')
  const [config, setConfig] = useState<LanguageModelConfig>({
    model: 'gpt-3.5-turbo',
    temperature: 0.7,
    maxTokens: 1000,
    topP: 0.9,
    frequencyPenalty: 0.0,
    presencePenalty: 0.0,
    stopSequences: [],
    systemPrompt: SYSTEM_PROMPTS.assistant
  })
  const [selectedModel, setSelectedModel] = useState(AVAILABLE_MODELS[1])
  const [promptType, setPromptType] = useState('assistant')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [generationStep, setGenerationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [conversationHistory, setConversationHistory] = useState<Array<{role: string, content: string}>>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const streamingRef = useRef<boolean>(false)

  const generateResponse = async () => {
    if (!prompt.trim()) return

    setIsGenerating(true)
    setProgress(0)
    setGenerationStep('Initializing language model...')
    setStreamingText('')

    try {
      // Add user message to conversation
      const newHistory = [...conversationHistory, { role: 'user', content: prompt }]
      setConversationHistory(newHistory)

      if (enableStreaming && config.model !== 'local') {
        await generateStreamingResponse(prompt, newHistory)
      } else {
        await generateStandardResponse(prompt, newHistory)
      }

    } catch (error) {
      console.error('Generation failed:', error)
    } finally {
      setIsGenerating(false)
      setProgress(100)
      setGenerationStep('Generation complete!')
    }
  }

  const generateStreamingResponse = async (userPrompt: string, history: Array<{role: string, content: string}>) => {
    setIsStreaming(true)
    streamingRef.current = true
    setStreamingText('')

    try {
      // Simulate streaming response
      const mockResponse = generateMockResponse(userPrompt)
      const words = mockResponse.split(' ')
      
      for (let i = 0; i < words.length && streamingRef.current; i++) {
        setStreamingText(prev => prev + (i > 0 ? ' ' : '') + words[i])
        setProgress((i / words.length) * 90)
        await new Promise(resolve => setTimeout(resolve, 50))
      }

      const finalResponse: ModelResponse = {
        text: streamingText,
        tokens: streamingText.split(' ').length,
        finishReason: 'stop',
        confidence: 0.85 + Math.random() * 0.1,
        processingTime: Date.now() - Date.now(),
        model: config.model,
        timestamp: new Date()
      }

      setResponse(finalResponse)
      onResponse?.(finalResponse)

      // Add assistant response to conversation
      setConversationHistory(prev => [...prev, { role: 'assistant', content: streamingText }])

    } finally {
      setIsStreaming(false)
      streamingRef.current = false
    }
  }

  const generateStandardResponse = async (userPrompt: string, history: Array<{role: string, content: string}>) => {
    // Simulate processing steps
    const steps = [
      'Processing prompt...',
      'Analyzing context...',
      'Generating response...',
      'Validating output...',
      'Finalizing response...'
    ]

    for (let i = 0; i < steps.length; i++) {
      setGenerationStep(steps[i])
      setProgress((i + 1) * 20)
      await new Promise(resolve => setTimeout(resolve, 300))
    }

    // Generate mock response
    const mockResponse = generateMockResponse(userPrompt)
    
    const finalResponse: ModelResponse = {
      text: mockResponse,
      tokens: mockResponse.split(' ').length,
      finishReason: 'stop',
      confidence: 0.85 + Math.random() * 0.1,
      processingTime: Date.now() - Date.now(),
      model: config.model,
      timestamp: new Date()
    }

    setResponse(finalResponse)
    onResponse?.(finalResponse)

    // Add assistant response to conversation
    setConversationHistory(prev => [...prev, { role: 'assistant', content: mockResponse }])
  }

  const generateMockResponse = (prompt: string): string => {
    const responses = {
      'creative': `Here's a creative response to your prompt: "${prompt}". Let me craft something imaginative and engaging that captures the essence of what you're looking for.`,
      'technical': `From a technical perspective, your query about "${prompt}" involves several key considerations. Let me break down the technical aspects and provide a comprehensive analysis.`,
      'business': `From a business standpoint, your question about "${prompt}" has strategic implications. Here's my analysis of the business considerations and recommendations.`,
      'educational': `Let me explain "${prompt}" in a clear, educational way. I'll break it down into digestible concepts and provide examples to help you understand.`,
      'code': `Here's how to approach "${prompt}" from a programming perspective. I'll provide code examples and explain the implementation details.`
    }
    
    return responses[promptType as keyof typeof responses] || 
           `I understand you're asking about "${prompt}". Let me provide a comprehensive response that addresses your question thoroughly.`
  }

  const stopGeneration = () => {
    streamingRef.current = false
    setIsStreaming(false)
    setIsGenerating(false)
  }

  const clearConversation = () => {
    setConversationHistory([])
    setResponse(null)
    setStreamingText('')
    setPrompt('')
  }

  const downloadResponse = () => {
    if (response) {
      const blob = new Blob([response.text], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `response-${Date.now()}.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }
  }

  const getModelCostColor = (cost: string) => {
    switch (cost) {
      case 'free': return 'text-green-600 bg-green-100'
      case 'low': return 'text-blue-600 bg-blue-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'high': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Model Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="h-6 w-6 text-blue-600" />
            <span>Language Model Interface</span>
          </CardTitle>
          <CardDescription>
            Advanced AI language model interaction with streaming support
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Model Selection */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {AVAILABLE_MODELS.map((model) => (
              <Card
                key={model.id}
                className={`cursor-pointer transition-all ${
                  selectedModel.id === model.id ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                }`}
                onClick={() => setSelectedModel(model)}
              >
                <CardContent className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium">{model.name}</h3>
                    <Badge className={getModelCostColor(model.cost)}>
                      {model.cost}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {model.description}
                  </p>
                  <div className="text-xs text-gray-500">
                    Max tokens: {model.maxTokens.toLocaleString()}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Prompt Type Selection */}
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
              Prompt Type
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {Object.entries(SYSTEM_PROMPTS).map(([type, prompt]) => (
                <Button
                  key={type}
                  variant={promptType === type ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => {
                    setPromptType(type)
                    setConfig(prev => ({ ...prev, systemPrompt: prompt }))
                  }}
                  className="text-xs"
                >
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </Button>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Configuration */}
      {showConfig && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm flex items-center space-x-2">
              <Settings className="h-4 w-4" />
              <span>Model Configuration</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                  Temperature: {config.temperature}
                </label>
                <Slider
                  value={[config.temperature]}
                  onValueChange={(value) => setConfig(prev => ({ ...prev, temperature: value[0] }))}
                  max={2}
                  min={0}
                  step={0.1}
                />
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                  Max Tokens: {config.maxTokens}
                </label>
                <Slider
                  value={[config.maxTokens]}
                  onValueChange={(value) => setConfig(prev => ({ ...prev, maxTokens: value[0] }))}
                  max={selectedModel.maxTokens}
                  min={100}
                  step={100}
                />
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                  Top P: {config.topP}
                </label>
                <Slider
                  value={[config.topP]}
                  onValueChange={(value) => setConfig(prev => ({ ...prev, topP: value[0] }))}
                  max={1}
                  min={0}
                  step={0.1}
                />
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                  Frequency Penalty: {config.frequencyPenalty}
                </label>
                <Slider
                  value={[config.frequencyPenalty]}
                  onValueChange={(value) => setConfig(prev => ({ ...prev, frequencyPenalty: value[0] }))}
                  max={2}
                  min={-2}
                  step={0.1}
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 block">
                System Prompt
              </label>
              <Textarea
                value={config.systemPrompt}
                onChange={(e) => setConfig(prev => ({ ...prev, systemPrompt: e.target.value }))}
                className="min-h-[80px]"
                placeholder="Enter system prompt..."
              />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Input and Generation */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm flex items-center space-x-2">
            <Target className="h-4 w-4" />
            <span>Prompt Input</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter your prompt here..."
            className="min-h-[120px]"
          />
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Button
                onClick={generateResponse}
                disabled={isGenerating || !prompt.trim()}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Generating...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Generate
                  </>
                )}
              </Button>
              
              {isGenerating && (
                <Button
                  variant="outline"
                  onClick={stopGeneration}
                >
                  <Pause className="h-4 w-4 mr-2" />
                  Stop
                </Button>
              )}
            </div>
            
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={clearConversation}
              >
                <RotateCcw className="h-4 w-4 mr-1" />
                Clear
              </Button>
              {response && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={downloadResponse}
                >
                  <Download className="h-4 w-4 mr-1" />
                  Download
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Generation Status */}
      {isGenerating && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
        >
          <div className="flex items-center space-x-3 mb-3">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
            <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
              {generationStep}
            </span>
          </div>
          <Progress value={progress} className="h-2" />
        </motion.div>
      )}

      {/* Response Display */}
      {(response || streamingText) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Brain className="h-5 w-5 text-green-600" />
                  <span>Model Response</span>
                </div>
                {response && (
                  <div className="flex items-center space-x-2">
                    <Badge className={getConfidenceColor(response.confidence)}>
                      {(response.confidence * 100).toFixed(1)}% confidence
                    </Badge>
                    <Badge variant="outline">
                      {response.tokens} tokens
                    </Badge>
                  </div>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="prose dark:prose-invert max-w-none">
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                  {streamingText || response?.text}
                </p>
              </div>
              
              {response && (
                <div className="flex flex-wrap gap-2 mt-4">
                  <Badge variant="outline">
                    {response.model}
                  </Badge>
                  <Badge variant="outline">
                    {response.processingTime}ms
                  </Badge>
                  <Badge variant="outline">
                    {response.timestamp.toLocaleTimeString()}
                  </Badge>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      )}

      {/* Conversation History */}
      {conversationHistory.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm flex items-center space-x-2">
              <Activity className="h-4 w-4" />
              <span>Conversation History</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {conversationHistory.map((message, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg ${
                    message.role === 'user' 
                      ? 'bg-blue-50 dark:bg-blue-900/20 ml-8' 
                      : 'bg-gray-50 dark:bg-gray-800 mr-8'
                  }`}
                >
                  <div className="flex items-center space-x-2 mb-2">
                    <Badge variant="outline" className="text-xs">
                      {message.role}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-700 dark:text-gray-300">
                    {message.content}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
