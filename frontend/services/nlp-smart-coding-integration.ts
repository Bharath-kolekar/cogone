/**
 * NLP Smart Coding AI Integration Service
 * Provides natural language processing capabilities for Smart Coding AI
 */

import { apiService } from '@/lib/api'

export interface NLPQuery {
  text: string
  context?: string
  intent?: string
  entities?: Record<string, any>
  confidence?: number
}

export interface NLPResponse {
  intent: string
  entities: Record<string, any>
  confidence: number
  suggestions: string[]
  action_required: string
  smart_coding_components: string[]
  natural_language_explanation: string
}

export interface CodeToNLPRequest {
  code: string
  language: string
  context?: string
  include_suggestions?: boolean
}

export interface CodeToNLPResponse {
  natural_language_description: string
  complexity_analysis: {
    level: 'simple' | 'medium' | 'complex'
    factors: string[]
    score: number
  }
  functionality_breakdown: {
    main_purpose: string
    key_functions: string[]
    data_flow: string[]
  }
  improvement_suggestions: string[]
  smart_coding_recommendations: {
    components: string[]
    optimizations: string[]
    integrations: string[]
  }
}

export interface NLPVoiceCommand {
  command: string
  intent: string
  parameters: Record<string, any>
  smart_coding_action: string
  confidence: number
}

export interface SmartCodingNLPAnalysis {
  code_understanding: {
    purpose: string
    patterns: string[]
    complexity: number
    maintainability: number
  }
  natural_language_feedback: {
    strengths: string[]
    improvements: string[]
    suggestions: string[]
  }
  smart_coding_integration: {
    recommended_components: string[]
    optimization_opportunities: string[]
    ai_enhancements: string[]
  }
}

class SmartCodingNLPService {
  private nlpCache: Map<string, NLPResponse> = new Map()
  private codeAnalysisCache: Map<string, CodeToNLPResponse> = new Map()

  /**
   * Process natural language query for Smart Coding AI
   */
  async processNLPQuery(query: NLPQuery): Promise<NLPResponse> {
    try {
      // Check cache first
      const cacheKey = `${query.text}_${query.context || ''}`
      if (this.nlpCache.has(cacheKey)) {
        return this.nlpCache.get(cacheKey)!
      }

      // Process with backend NLP service
      const response = await apiService.request('/api/v0/nlp-smart-coding/process-query', {
        method: 'POST',
        body: JSON.stringify(query),
      })

      if (response.success && response.data) {
        const nlpResponse: NLPResponse = response.data
        this.nlpCache.set(cacheKey, nlpResponse)
        return nlpResponse
      }

      // Fallback to local processing
      return this.processNLPQueryLocally(query)
    } catch (error) {
      console.error('NLP query processing failed:', error)
      return this.processNLPQueryLocally(query)
    }
  }

  /**
   * Convert code to natural language description
   */
  async codeToNaturalLanguage(request: CodeToNLPRequest): Promise<CodeToNLPResponse> {
    try {
      // Check cache first
      const cacheKey = `${request.code}_${request.language}_${request.context || ''}`
      if (this.codeAnalysisCache.has(cacheKey)) {
        return this.codeAnalysisCache.get(cacheKey)!
      }

      // Process with backend NLP service
      const response = await apiService.request('/api/v0/nlp-smart-coding/code-to-nlp', {
        method: 'POST',
        body: JSON.stringify(request),
      })

      if (response.success && response.data) {
        const nlpResponse: CodeToNLPResponse = response.data
        this.codeAnalysisCache.set(cacheKey, nlpResponse)
        return nlpResponse
      }

      // Fallback to local processing
      return this.codeToNaturalLanguageLocally(request)
    } catch (error) {
      console.error('Code to NLP conversion failed:', error)
      return this.codeToNaturalLanguageLocally(request)
    }
  }

  /**
   * Process voice commands for Smart Coding AI
   */
  async processVoiceCommand(command: string): Promise<NLPVoiceCommand> {
    try {
      const nlpQuery: NLPQuery = {
        text: command,
        context: 'voice_command',
        intent: 'smart_coding_action'
      }

      const nlpResponse = await this.processNLPQuery(nlpQuery)
      
      return {
        command,
        intent: nlpResponse.intent,
        parameters: nlpResponse.entities,
        smart_coding_action: nlpResponse.action_required,
        confidence: nlpResponse.confidence
      }
    } catch (error) {
      console.error('Voice command processing failed:', error)
      return {
        command,
        intent: 'unknown',
        parameters: {},
        smart_coding_action: 'none',
        confidence: 0
      }
    }
  }

  /**
   * Get Smart Coding AI recommendations based on natural language
   */
  async getSmartCodingRecommendations(query: string): Promise<{
    recommended_components: string[]
    integration_suggestions: string[]
    optimization_opportunities: string[]
    natural_language_explanation: string
  }> {
    try {
      const nlpQuery: NLPQuery = {
        text: query,
        context: 'smart_coding_recommendation',
        intent: 'get_recommendations'
      }

      const nlpResponse = await this.processNLPQuery(nlpQuery)
      
      return {
        recommended_components: nlpResponse.smart_coding_components,
        integration_suggestions: nlpResponse.suggestions,
        optimization_opportunities: nlpResponse.suggestions.filter(s => 
          s.includes('optimize') || s.includes('improve') || s.includes('enhance')
        ),
        natural_language_explanation: nlpResponse.natural_language_explanation
      }
    } catch (error) {
      console.error('Smart coding recommendations failed:', error)
      return {
        recommended_components: [],
        integration_suggestions: [],
        optimization_opportunities: [],
        natural_language_explanation: 'Unable to process recommendations at this time.'
      }
    }
  }

  /**
   * Analyze code with NLP-enhanced Smart Coding AI
   */
  async analyzeCodeWithNLP(code: string, language: string): Promise<SmartCodingNLPAnalysis> {
    try {
      const codeToNLPRequest: CodeToNLPRequest = {
        code,
        language,
        context: 'smart_coding_analysis',
        include_suggestions: true
      }

      const codeAnalysis = await this.codeToNaturalLanguage(codeToNLPRequest)
      
      return {
        code_understanding: {
          purpose: codeAnalysis.functionality_breakdown.main_purpose,
          patterns: this.extractCodePatterns(code),
          complexity: codeAnalysis.complexity_analysis.score,
          maintainability: this.calculateMaintainability(code)
        },
        natural_language_feedback: {
          strengths: this.identifyStrengths(code),
          improvements: codeAnalysis.improvement_suggestions,
          suggestions: codeAnalysis.smart_coding_recommendations.optimizations
        },
        smart_coding_integration: {
          recommended_components: codeAnalysis.smart_coding_recommendations.components,
          optimization_opportunities: codeAnalysis.smart_coding_recommendations.optimizations,
          ai_enhancements: codeAnalysis.smart_coding_recommendations.integrations
        }
      }
    } catch (error) {
      console.error('NLP code analysis failed:', error)
      return {
        code_understanding: {
          purpose: 'Unknown',
          patterns: [],
          complexity: 0,
          maintainability: 0
        },
        natural_language_feedback: {
          strengths: [],
          improvements: [],
          suggestions: []
        },
        smart_coding_integration: {
          recommended_components: [],
          optimization_opportunities: [],
          ai_enhancements: []
        }
      }
    }
  }

  /**
   * Local fallback for NLP query processing
   */
  private processNLPQueryLocally(query: NLPQuery): NLPResponse {
    const intent = this.detectIntent(query.text)
    const entities = this.extractEntities(query.text)
    const confidence = this.calculateConfidence(query.text, intent)
    
    return {
      intent,
      entities,
      confidence,
      suggestions: this.generateSuggestions(intent, entities),
      action_required: this.determineAction(intent, entities),
      smart_coding_components: this.getSmartCodingComponents(intent, entities),
      natural_language_explanation: this.generateExplanation(intent, entities)
    }
  }

  /**
   * Local fallback for code to NLP conversion
   */
  private codeToNaturalLanguageLocally(request: CodeToNLPRequest): CodeToNLPResponse {
    const complexity = this.analyzeComplexity(request.code)
    const functionality = this.analyzeFunctionality(request.code)
    
    return {
      natural_language_description: this.generateCodeDescription(request.code, request.language),
      complexity_analysis: {
        level: complexity.level,
        factors: complexity.factors,
        score: complexity.score
      },
      functionality_breakdown: {
        main_purpose: functionality.purpose,
        key_functions: functionality.functions,
        data_flow: functionality.dataFlow
      },
      improvement_suggestions: this.generateImprovementSuggestions(request.code),
      smart_coding_recommendations: {
        components: this.getRecommendedComponents(request.code, request.language),
        optimizations: this.getOptimizationSuggestions(request.code),
        integrations: this.getIntegrationSuggestions(request.code)
      }
    }
  }

  // Helper methods for local processing
  private detectIntent(text: string): string {
    const lowerText = text.toLowerCase()
    
    if (lowerText.includes('analyze') || lowerText.includes('check')) return 'analyze'
    if (lowerText.includes('optimize') || lowerText.includes('improve')) return 'optimize'
    if (lowerText.includes('fix') || lowerText.includes('debug')) return 'fix'
    if (lowerText.includes('explain') || lowerText.includes('describe')) return 'explain'
    if (lowerText.includes('suggest') || lowerText.includes('recommend')) return 'suggest'
    if (lowerText.includes('integrate') || lowerText.includes('connect')) return 'integrate'
    
    return 'general'
  }

  private extractEntities(text: string): Record<string, any> {
    const entities: Record<string, any> = {}
    
    // Extract programming languages
    const languages = ['javascript', 'python', 'java', 'typescript', 'react', 'vue', 'angular']
    languages.forEach(lang => {
      if (text.toLowerCase().includes(lang)) {
        entities.language = lang
      }
    })
    
    // Extract code concepts
    const concepts = ['function', 'class', 'variable', 'loop', 'condition', 'api', 'database']
    concepts.forEach(concept => {
      if (text.toLowerCase().includes(concept)) {
        entities.concepts = entities.concepts || []
        entities.concepts.push(concept)
      }
    })
    
    return entities
  }

  private calculateConfidence(text: string, intent: string): number {
    let confidence = 0.5
    
    // Increase confidence based on specific keywords
    const intentKeywords: Record<string, string[]> = {
      analyze: ['analyze', 'check', 'review', 'examine'],
      optimize: ['optimize', 'improve', 'enhance', 'better'],
      fix: ['fix', 'debug', 'error', 'bug', 'issue'],
      explain: ['explain', 'describe', 'what', 'how'],
      suggest: ['suggest', 'recommend', 'advice', 'tip'],
      integrate: ['integrate', 'connect', 'link', 'combine']
    }
    
    const keywords = intentKeywords[intent] || []
    keywords.forEach(keyword => {
      if (text.toLowerCase().includes(keyword)) {
        confidence += 0.1
      }
    })
    
    return Math.min(confidence, 1.0)
  }

  private generateSuggestions(intent: string, entities: Record<string, any>): string[] {
    const suggestions: Record<string, string[]> = {
      analyze: [
        'Run code quality analysis',
        'Check for security vulnerabilities',
        'Analyze performance bottlenecks',
        'Review code structure and patterns'
      ],
      optimize: [
        'Optimize algorithm complexity',
        'Improve memory usage',
        'Enhance code readability',
        'Optimize database queries'
      ],
      fix: [
        'Fix syntax errors',
        'Resolve runtime issues',
        'Correct logic errors',
        'Handle edge cases'
      ],
      explain: [
        'Explain code functionality',
        'Describe algorithm flow',
        'Clarify complex logic',
        'Document code purpose'
      ],
      suggest: [
        'Suggest code improvements',
        'Recommend best practices',
        'Propose optimizations',
        'Advise on architecture'
      ],
      integrate: [
        'Integrate with AI components',
        'Connect to external services',
        'Link with database systems',
        'Combine with other modules'
      ]
    }
    
    return suggestions[intent] || ['Provide general assistance']
  }

  private determineAction(intent: string, entities: Record<string, any>): string {
    const actions: Record<string, string> = {
      analyze: 'run_analysis',
      optimize: 'run_optimization',
      fix: 'run_debugging',
      explain: 'generate_explanation',
      suggest: 'generate_suggestions',
      integrate: 'run_integration',
      general: 'provide_assistance'
    }
    
    return actions[intent] || 'provide_assistance'
  }

  private getSmartCodingComponents(intent: string, entities: Record<string, any>): string[] {
    const componentMap: Record<string, string[]> = {
      analyze: ['accuracy-validation', 'code-quality-analyzer', 'security-validator'],
      optimize: ['performance-optimizer', 'super-intelligent-optimizer', 'system-optimization'],
      fix: ['error-recovery-manager', 'consistency-enforcer', 'factual-accuracy-validator'],
      explain: ['nlp-enhancement-service', 'consciousness-core', 'proactive-intelligence'],
      suggest: ['ai-assistant-core', 'enhanced-ai-assistant', 'smart-coding-ai'],
      integrate: ['ai-orchestrator', 'unified-ai-component-orchestrator', 'tool-integration-manager'],
      general: ['ai-orchestrator', 'smart-coding-ai', 'ai-assistant-core']
    }
    
    return componentMap[intent] || ['ai-orchestrator']
  }

  private generateExplanation(intent: string, entities: Record<string, any>): string {
    const explanations: Record<string, string> = {
      analyze: 'I will analyze your code for quality, security, and performance issues.',
      optimize: 'I will help optimize your code for better performance and efficiency.',
      fix: 'I will help identify and fix issues in your code.',
      explain: 'I will provide a clear explanation of how your code works.',
      suggest: 'I will suggest improvements and best practices for your code.',
      integrate: 'I will help integrate your code with AI components and services.',
      general: 'I will assist you with your coding needs using Smart Coding AI.'
    }
    
    return explanations[intent] || 'I will help you with your coding task.'
  }

  private analyzeComplexity(code: string): { level: string; factors: string[]; score: number } {
    const lines = code.split('\n').length
    const functions = (code.match(/function\s+\w+/g) || []).length
    const loops = (code.match(/for\s*\(|while\s*\(|do\s*{/g) || []).length
    const conditions = (code.match(/if\s*\(|else\s*if\s*\(|switch\s*\(/g) || []).length
    
    let score = 0
    const factors: string[] = []
    
    if (lines > 100) {
      score += 0.3
      factors.push('Large codebase')
    }
    if (functions > 10) {
      score += 0.2
      factors.push('Many functions')
    }
    if (loops > 5) {
      score += 0.2
      factors.push('Complex loops')
    }
    if (conditions > 10) {
      score += 0.3
      factors.push('Complex conditions')
    }
    
    const level = score > 0.7 ? 'complex' : score > 0.4 ? 'medium' : 'simple'
    
    return { level, factors, score }
  }

  private analyzeFunctionality(code: string): { purpose: string; functions: string[]; dataFlow: string[] } {
    const functions = (code.match(/function\s+(\w+)/g) || []).map(f => f.replace('function ', ''))
    const variables = (code.match(/let\s+(\w+)|const\s+(\w+)|var\s+(\w+)/g) || []).map(v => v.split(' ')[1])
    
    return {
      purpose: 'Code functionality analysis',
      functions,
      dataFlow: variables
    }
  }

  private generateCodeDescription(code: string, language: string): string {
    const lines = code.split('\n').length
    const functions = (code.match(/function\s+\w+/g) || []).length
    
    return `This ${language} code contains ${lines} lines with ${functions} functions. It appears to be a ${this.detectCodeType(code)} implementation.`
  }

  private detectCodeType(code: string): string {
    if (code.includes('class ')) return 'object-oriented'
    if (code.includes('function ')) return 'functional'
    if (code.includes('async ')) return 'asynchronous'
    if (code.includes('import ') || code.includes('require(')) return 'modular'
    return 'procedural'
  }

  private generateImprovementSuggestions(code: string): string[] {
    const suggestions: string[] = []
    
    if (code.includes('var ')) {
      suggestions.push('Consider using let or const instead of var')
    }
    if (!code.includes('try') && code.includes('fetch(')) {
      suggestions.push('Add error handling for API calls')
    }
    if (code.includes('console.log')) {
      suggestions.push('Consider using proper logging instead of console.log')
    }
    
    return suggestions
  }

  private getRecommendedComponents(code: string, language: string): string[] {
    const components: string[] = []
    
    if (code.includes('function ') || code.includes('class ')) {
      components.push('code-quality-analyzer')
    }
    if (code.includes('fetch(') || code.includes('axios')) {
      components.push('security-validator')
    }
    if (code.includes('for ') || code.includes('while ')) {
      components.push('performance-optimizer')
    }
    
    return components
  }

  private getOptimizationSuggestions(code: string): string[] {
    const suggestions: string[] = []
    
    if (code.includes('for (let i = 0; i < array.length; i++)')) {
      suggestions.push('Use forEach or map for better readability')
    }
    if (code.includes('==') && !code.includes('===')) {
      suggestions.push('Use strict equality (===) instead of loose equality (==)')
    }
    
    return suggestions
  }

  private getIntegrationSuggestions(code: string): string[] {
    const suggestions: string[] = []
    
    if (code.includes('function ')) {
      suggestions.push('Integrate with AI Assistant for code suggestions')
    }
    if (code.includes('class ')) {
      suggestions.push('Use Smart Coding AI for object-oriented analysis')
    }
    
    return suggestions
  }

  private extractCodePatterns(code: string): string[] {
    const patterns: string[] = []
    
    if (code.includes('async ')) patterns.push('async/await')
    if (code.includes('Promise.')) patterns.push('Promise handling')
    if (code.includes('class ')) patterns.push('Object-oriented')
    if (code.includes('function ')) patterns.push('Functional programming')
    
    return patterns
  }

  private calculateMaintainability(code: string): number {
    let score = 1.0
    
    // Penalize long functions
    const functions = code.split('function ')
    functions.forEach(func => {
      const lines = func.split('\n').length
      if (lines > 50) score -= 0.1
    })
    
    // Penalize deep nesting
    const maxNesting = this.getMaxNesting(code)
    if (maxNesting > 4) score -= 0.2
    
    return Math.max(score, 0)
  }

  private getMaxNesting(code: string): number {
    let maxNesting = 0
    let currentNesting = 0
    
    for (const char of code) {
      if (char === '{') {
        currentNesting++
        maxNesting = Math.max(maxNesting, currentNesting)
      } else if (char === '}') {
        currentNesting--
      }
    }
    
    return maxNesting
  }

  private identifyStrengths(code: string): string[] {
    const strengths: string[] = []
    
    if (code.includes('const ') && !code.includes('var ')) {
      strengths.push('Good use of const declarations')
    }
    if (code.includes('try {') && code.includes('catch')) {
      strengths.push('Proper error handling')
    }
    if (code.includes('function ') && code.includes('return')) {
      strengths.push('Clear function structure')
    }
    
    return strengths
  }
}

export const smartCodingNLPService = new SmartCodingNLPService()
