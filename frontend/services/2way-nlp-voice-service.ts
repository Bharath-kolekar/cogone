/**
 * 2-Way NLP Voice Service for Smart Coding AI
 * Enables natural conversation between user and Smart Coding AI through voice
 */

import { smartCodingNLPService, NLPQuery, NLPResponse } from './nlp-smart-coding-integration'

export interface VoiceMessage {
  id: string
  type: 'user' | 'ai'
  content: string
  timestamp: Date
  confidence?: number
  intent?: string
  entities?: Record<string, any>
  smartCodingAction?: string
  audioBlob?: Blob
}

export interface ConversationContext {
  sessionId: string
  messages: VoiceMessage[]
  currentIntent: string
  conversationState: 'idle' | 'listening' | 'processing' | 'speaking'
  userPreferences: {
    voice: string
    speed: number
    pitch: number
    language: string
  }
  smartCodingContext: {
    activeComponents: string[]
    lastAction: string
    currentTask: string
  }
}

export interface VoiceConversationConfig {
  enableAutoResponse: boolean
  enableInterruption: boolean
  enableContextAwareness: boolean
  maxConversationLength: number
  responseDelay: number
}

class TwoWayNLPVoiceService {
  private conversationContext: ConversationContext
  private config: VoiceConversationConfig
  private speechRecognition: any = null
  private speechSynthesis: SpeechSynthesis | null = null
  private isListening: boolean = false
  private isSpeaking: boolean = false
  private conversationCallbacks: {
    onMessage?: (message: VoiceMessage) => void
    onStateChange?: (state: string) => void
    onError?: (error: Error) => void
  } = {}

  constructor() {
    this.conversationContext = this.initializeContext()
    this.config = this.getDefaultConfig()
    this.initializeSpeechServices()
  }

  private initializeContext(): ConversationContext {
    return {
      sessionId: `session_${Date.now()}`,
      messages: [],
      currentIntent: 'greeting',
      conversationState: 'idle',
      userPreferences: {
        voice: 'default',
        speed: 1.0,
        pitch: 1.0,
        language: 'en-US'
      },
      smartCodingContext: {
        activeComponents: [],
        lastAction: '',
        currentTask: ''
      }
    }
  }

  private getDefaultConfig(): VoiceConversationConfig {
    return {
      enableAutoResponse: true,
      enableInterruption: true,
      enableContextAwareness: true,
      maxConversationLength: 50,
      responseDelay: 1000
    }
  }

  private initializeSpeechServices() {
    // Initialize Speech Recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
      this.speechRecognition = new SpeechRecognition()
      this.speechRecognition.continuous = true
      this.speechRecognition.interimResults = true
      this.speechRecognition.lang = this.conversationContext.userPreferences.language
      
      this.speechRecognition.onstart = () => {
        this.isListening = true
        this.conversationContext.conversationState = 'listening'
        this.conversationCallbacks.onStateChange?.('listening')
      }

      this.speechRecognition.onresult = (event: any) => {
        this.handleSpeechResult(event)
      }

      this.speechRecognition.onerror = (event: any) => {
        this.handleSpeechError(event)
      }

      this.speechRecognition.onend = () => {
        this.isListening = false
        this.conversationContext.conversationState = 'idle'
        this.conversationCallbacks.onStateChange?.('idle')
      }
    }

    // Initialize Speech Synthesis
    if ('speechSynthesis' in window) {
      this.speechSynthesis = window.speechSynthesis
    }
  }

  /**
   * Start voice conversation with Smart Coding AI
   */
  async startConversation(): Promise<void> {
    try {
      if (!this.speechRecognition) {
        throw new Error('Speech recognition not supported')
      }

      this.conversationContext.conversationState = 'listening'
      this.speechRecognition.start()
      
      // Send initial greeting
      await this.sendAIMessage("Hello! I'm your Smart Coding AI assistant. How can I help you with your coding today?")
    } catch (error) {
      this.conversationCallbacks.onError?.(error as Error)
    }
  }

  /**
   * Stop voice conversation
   */
  stopConversation(): void {
    if (this.speechRecognition && this.isListening) {
      this.speechRecognition.stop()
    }
    
    if (this.speechSynthesis && this.isSpeaking) {
      this.speechSynthesis.cancel()
    }
    
    this.conversationContext.conversationState = 'idle'
    this.conversationCallbacks.onStateChange?.('idle')
  }

  /**
   * Handle speech recognition results
   */
  private async handleSpeechResult(event: any): Promise<void> {
    const results = Array.from(event.results)
    const latestResult = results[results.length - 1] as any
    
    if (latestResult.isFinal) {
      const transcript = latestResult[0].transcript.trim()
      const confidence = latestResult[0].confidence
      
      if (transcript) {
        await this.processUserMessage(transcript, confidence)
      }
    }
  }

  /**
   * Process user voice message
   */
  private async processUserMessage(transcript: string, confidence: number): Promise<void> {
    try {
      this.conversationContext.conversationState = 'processing'
      this.conversationCallbacks.onStateChange?.('processing')

      // Create user message
      const userMessage: VoiceMessage = {
        id: `msg_${Date.now()}`,
        type: 'user',
        content: transcript,
        timestamp: new Date(),
        confidence
      }

      // Add to conversation context
      this.conversationContext.messages.push(userMessage)
      this.conversationCallbacks.onMessage?.(userMessage)

      // Process with NLP
      const nlpQuery: NLPQuery = {
        text: transcript,
        context: 'voice_conversation',
        intent: this.conversationContext.currentIntent
      }

      const nlpResponse = await smartCodingNLPService.processNLPQuery(nlpQuery)
      
      // Update conversation context
      this.conversationContext.currentIntent = nlpResponse.intent
      this.conversationContext.smartCodingContext.lastAction = nlpResponse.action_required

      // Generate AI response
      const aiResponse = await this.generateAIResponse(nlpResponse, transcript)
      
      // Send AI response
      await this.sendAIMessage(aiResponse, nlpResponse)

    } catch (error) {
      console.error('Error processing user message:', error)
      await this.sendAIMessage("I'm sorry, I didn't understand that. Could you please repeat your request?")
    }
  }

  /**
   * Generate AI response based on NLP analysis
   */
  private async generateAIResponse(nlpResponse: NLPResponse, userInput: string): Promise<string> {
    const intent = nlpResponse.intent
    const confidence = nlpResponse.confidence
    const action = nlpResponse.action_required

    // Generate contextual responses based on intent
    switch (intent) {
      case 'greeting':
        return this.generateGreetingResponse()
      
      case 'analyze':
        return this.generateAnalysisResponse(userInput, nlpResponse)
      
      case 'optimize':
        return this.generateOptimizationResponse(userInput, nlpResponse)
      
      case 'fix':
        return this.generateFixResponse(userInput, nlpResponse)
      
      case 'explain':
        return this.generateExplanationResponse(userInput, nlpResponse)
      
      case 'suggest':
        return this.generateSuggestionResponse(userInput, nlpResponse)
      
      case 'integrate':
        return this.generateIntegrationResponse(userInput, nlpResponse)
      
      case 'help':
        return this.generateHelpResponse()
      
      case 'goodbye':
        return this.generateGoodbyeResponse()
      
      default:
        return this.generateGeneralResponse(userInput, nlpResponse)
    }
  }

  /**
   * Send AI message with voice synthesis
   */
  private async sendAIMessage(content: string, nlpResponse?: NLPResponse): Promise<void> {
    try {
      // Create AI message
      const aiMessage: VoiceMessage = {
        id: `ai_msg_${Date.now()}`,
        type: 'ai',
        content,
        timestamp: new Date(),
        confidence: nlpResponse?.confidence,
        intent: nlpResponse?.intent,
        entities: nlpResponse?.entities,
        smartCodingAction: nlpResponse?.action_required
      }

      // Add to conversation context
      this.conversationContext.messages.push(aiMessage)
      this.conversationCallbacks.onMessage?.(aiMessage)

      // Speak the response
      await this.speakText(content)

    } catch (error) {
      console.error('Error sending AI message:', error)
    }
  }

  /**
   * Convert text to speech
   */
  private async speakText(text: string): Promise<void> {
    if (!this.speechSynthesis) {
      console.warn('Speech synthesis not supported')
      return
    }

    return new Promise((resolve, reject) => {
      try {
        this.isSpeaking = true
        this.conversationContext.conversationState = 'speaking'
        this.conversationCallbacks.onStateChange?.('speaking')

        const utterance = new SpeechSynthesisUtterance(text)
        const selectedVoice = this.getSelectedVoice()
        if (selectedVoice) {
          utterance.voice = selectedVoice
        }
        utterance.rate = this.conversationContext.userPreferences.speed
        utterance.pitch = this.conversationContext.userPreferences.pitch
        utterance.lang = this.conversationContext.userPreferences.language

        utterance.onend = () => {
          this.isSpeaking = false
          this.conversationContext.conversationState = 'idle'
          this.conversationCallbacks.onStateChange?.('idle')
          resolve()
        }

        utterance.onerror = (event) => {
          this.isSpeaking = false
          this.conversationContext.conversationState = 'idle'
          this.conversationCallbacks.onStateChange?.('idle')
          reject(new Error(`Speech synthesis error: ${event.error}`))
        }

        this.speechSynthesis.speak(utterance)

      } catch (error) {
        this.isSpeaking = false
        this.conversationContext.conversationState = 'idle'
        this.conversationCallbacks.onStateChange?.('idle')
        reject(error)
      }
    })
  }

  /**
   * Get selected voice for speech synthesis
   */
  private getSelectedVoice(): SpeechSynthesisVoice | null {
    if (!this.speechSynthesis) return null

    const voices = this.speechSynthesis.getVoices()
    const preferredVoice = voices.find(voice => 
      voice.name === this.conversationContext.userPreferences.voice
    )

    return preferredVoice || voices.find(voice => voice.lang.startsWith('en')) || voices[0] || null
  }

  /**
   * Handle speech recognition errors
   */
  private handleSpeechError(event: any): void {
    console.error('Speech recognition error:', event.error)
    this.conversationCallbacks.onError?.(new Error(`Speech recognition error: ${event.error}`))
  }

  // Response generation methods
  private generateGreetingResponse(): string {
    const greetings = [
      "Hello! I'm your Smart Coding AI assistant. I can help you analyze, optimize, and improve your code. What would you like to work on?",
      "Hi there! I'm here to help with your coding tasks. I can analyze code, suggest improvements, and integrate with 44+ AI components. What can I do for you?",
      "Welcome! I'm your Smart Coding AI companion. I can help you with code analysis, optimization, debugging, and much more. How can I assist you today?"
    ]
    return greetings[Math.floor(Math.random() * greetings.length)]
  }

  private generateAnalysisResponse(userInput: string, nlpResponse: NLPResponse): string {
    const components = nlpResponse.smart_coding_components.join(', ')
    return `I'll analyze your code using ${components}. This will help identify quality issues, security vulnerabilities, and performance bottlenecks. The analysis will provide detailed insights and recommendations for improvement.`
  }

  private generateOptimizationResponse(userInput: string, nlpResponse: NLPResponse): string {
    return `I'll optimize your code for better performance and efficiency. This includes algorithm optimization, memory usage improvements, and code structure enhancements. The optimization will be powered by our advanced AI components.`
  }

  private generateFixResponse(userInput: string, nlpResponse: NLPResponse): string {
    return `I'll help you fix any issues in your code. This includes debugging errors, resolving bugs, and implementing proper error handling. I'll use our comprehensive AI analysis to identify and resolve problems.`
  }

  private generateExplanationResponse(userInput: string, nlpResponse: NLPResponse): string {
    return `I'll provide a detailed explanation of your code. This includes describing the functionality, explaining the logic flow, and highlighting key concepts. I'll make it easy to understand how your code works.`
  }

  private generateSuggestionResponse(userInput: string, nlpResponse: NLPResponse): string {
    return `I'll suggest improvements for your code. This includes best practices, code quality enhancements, and architectural recommendations. I'll provide specific, actionable suggestions to make your code better.`
  }

  private generateIntegrationResponse(userInput: string, nlpResponse: NLPResponse): string {
    const components = nlpResponse.smart_coding_components.join(', ')
    return `I'll integrate your code with our Smart Coding AI components: ${components}. This will enhance your code with advanced AI capabilities and provide intelligent automation.`
  }

  private generateHelpResponse(): string {
    return `I can help you with many coding tasks! I can analyze code for quality and security, optimize performance, fix bugs, explain complex code, suggest improvements, and integrate with 44+ AI components. Just tell me what you'd like to do with your code.`
  }

  private generateGoodbyeResponse(): string {
    return `Goodbye! It was great helping you with your coding tasks. Feel free to come back anytime you need assistance with Smart Coding AI. Happy coding!`
  }

  private generateGeneralResponse(userInput: string, nlpResponse: NLPResponse): string {
    return `I understand you want to ${nlpResponse.action_required}. I'll use our Smart Coding AI components to help you with that. ${nlpResponse.natural_language_explanation}`
  }

  // Public API methods
  public setCallbacks(callbacks: {
    onMessage?: (message: VoiceMessage) => void
    onStateChange?: (state: string) => void
    onError?: (error: Error) => void
  }): void {
    this.conversationCallbacks = callbacks
  }

  public updateUserPreferences(preferences: Partial<ConversationContext['userPreferences']>): void {
    this.conversationContext.userPreferences = {
      ...this.conversationContext.userPreferences,
      ...preferences
    }
  }

  public updateConfig(config: Partial<VoiceConversationConfig>): void {
    this.config = {
      ...this.config,
      ...config
    }
  }

  public getConversationContext(): ConversationContext {
    return { ...this.conversationContext }
  }

  public getConversationHistory(): VoiceMessage[] {
    return [...this.conversationContext.messages]
  }

  public clearConversation(): void {
    this.conversationContext.messages = []
    this.conversationContext.currentIntent = 'greeting'
    this.conversationContext.smartCodingContext = {
      activeComponents: [],
      lastAction: '',
      currentTask: ''
    }
  }

  public isConversationActive(): boolean {
    return this.isListening || this.isSpeaking
  }

  public getAvailableVoices(): SpeechSynthesisVoice[] {
    if (!this.speechSynthesis) return []
    return this.speechSynthesis.getVoices()
  }

  public setVoice(voiceName: string): void {
    this.conversationContext.userPreferences.voice = voiceName
  }

  public setLanguage(language: string): void {
    this.conversationContext.userPreferences.language = language
    if (this.speechRecognition) {
      this.speechRecognition.lang = language
    }
  }

  public setSpeed(speed: number): void {
    this.conversationContext.userPreferences.speed = Math.max(0.1, Math.min(2.0, speed))
  }

  public setPitch(pitch: number): void {
    this.conversationContext.userPreferences.pitch = Math.max(0.1, Math.min(2.0, pitch))
  }
}

export const twoWayNLPVoiceService = new TwoWayNLPVoiceService()
