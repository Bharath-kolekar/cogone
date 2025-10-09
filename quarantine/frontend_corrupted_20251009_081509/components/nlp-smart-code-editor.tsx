'use client'

import { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Code, 
  Play, 
  Save, 
  Download, 
  Upload, 
  Lightbulb, 
  CheckCircle, 
  AlertTriangle,
  Brain,
  Zap,
  Cpu,
  Settings,
  Mic,
  Volume2,
  MessageSquare,
  BookOpen,
  Target,
  Sparkles
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { smartCodingNLPService, NLPQuery, CodeToNLPRequest, SmartCodingNLPAnalysis } from '@/services/nlp-smart-coding-integration'

interface NLPSmartCodeEditorProps {
  initialCode?: string
  language?: string
  onCodeChange?: (code: string) => void
  onSave?: (code: string) => void
  onSmartAnalysis?: (analysis: any) => void
  onIntegrationResult?: (result: any) => void
  onNLPInsight?: (insight: any) => void
}

export function NLPSmartCodeEditor({
  initialCode = '',
  language = 'javascript',
  onCodeChange,
  onSave,
  onSmartAnalysis,
  onIntegrationResult,
  onNLPInsight
}: NLPSmartCodeEditorProps) {
  const [code, setCode] = useState(initialCode)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [isNLPProcessing, setIsNLPProcessing] = useState(false)
  const [nlpQuery, setNlpQuery] = useState('')
  const [nlpInsights, setNlpInsights] = useState<SmartCodingNLPAnalysis | null>(null)
  const [naturalLanguageDescription, setNaturalLanguageDescription] = useState('')
  const [codeComplexity, setCodeComplexity] = useState<any>(null)
  const [activeTab, setActiveTab] = useState('editor')
  const [showNLPFeatures, setShowNLPFeatures] = useState(true)
  const [voiceCommand, setVoiceCommand] = useState('')
  const [isListening, setIsListening] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (code !== initialCode) {
      onCodeChange?.(code)
    }
  }, [code, initialCode, onCodeChange])

  const handleCodeChange = (newCode: string) => {
    setCode(newCode)
  }

  const handleSave = () => {
    onSave?.(code)
  }

  const handleNLPQuery = async () => {
    if (!nlpQuery.trim()) return

    try {
      setIsNLPProcessing(true)
      
      const nlpRequest: NLPQuery = {
        text: nlpQuery,
        context: 'smart_coding_editor',
        intent: 'code_analysis'
      }

      const nlpResponse = await smartCodingNLPService.processNLPQuery(nlpRequest)
      
      // Process the NLP response
      if (nlpResponse.action_required === 'run_analysis') {
        await handleSmartAnalysis()
      } else if (nlpResponse.action_required === 'run_optimization') {
        await handleOptimization()
      } else if (nlpResponse.action_required === 'run_integration') {
        await handleSmartIntegration('comprehensive')
      }

      onNLPInsight?.(nlpResponse)
    } catch (error) {
      console.error('NLP query processing failed:', error)
    } finally {
      setIsNLPProcessing(false)
    }
  }

  const handleCodeToNLP = async () => {
    try {
      setIsNLPProcessing(true)
      
      const request: CodeToNLPRequest = {
        code,
        language,
        context: 'smart_coding_analysis',
        include_suggestions: true
      }

      const nlpResponse = await smartCodingNLPService.codeToNaturalLanguage(request)
      
      setNaturalLanguageDescription(nlpResponse.natural_language_description)
      setCodeComplexity(nlpResponse.complexity_analysis)
      
      onNLPInsight?.(nlpResponse)
    } catch (error) {
      console.error('Code to NLP conversion failed:', error)
    } finally {
      setIsNLPProcessing(false)
    }
  }

  const handleSmartAnalysis = async () => {
    try {
      setIsAnalyzing(true)
      
      // Get NLP-enhanced analysis
      const nlpAnalysis = await smartCodingNLPService.analyzeCodeWithNLP(code, language)
      setNlpInsights(nlpAnalysis)
      
      onSmartAnalysis?.(nlpAnalysis)
    } catch (error) {
      console.error('Smart analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleOptimization = async () => {
    try {
      setIsNLPProcessing(true)
      
      const nlpRequest: NLPQuery = {
        text: 'optimize this code for better performance and maintainability',
        context: 'code_optimization',
        intent: 'optimize'
      }

      const nlpResponse = await smartCodingNLPService.processNLPQuery(nlpRequest)
      
      // Apply optimization suggestions
      const optimizedCode = await applyOptimizations(code, nlpResponse.suggestions)
      setCode(optimizedCode)
      
      onIntegrationResult?.(nlpResponse)
    } catch (error) {
      console.error('Optimization failed:', error)
    } finally {
      setIsNLPProcessing(false)
    }
  }

  const handleSmartIntegration = async (integrationType: string) => {
    try {
      setIsNLPProcessing(true)
      
      const nlpRequest: NLPQuery = {
        text: `integrate with ${integrationType} AI components`,
        context: 'smart_coding_integration',
        intent: 'integrate'
      }

      const nlpResponse = await smartCodingNLPService.processNLPQuery(nlpRequest)
      
      onIntegrationResult?.(nlpResponse)
    } catch (error) {
      console.error('Smart integration failed:', error)
    } finally {
      setIsNLPProcessing(false)
    }
  }

  const handleVoiceCommand = async (command: string) => {
    try {
      setIsListening(true)
      setVoiceCommand(command)
      
      const nlpCommand = await smartCodingNLPService.processVoiceCommand(command)
      
      if (nlpCommand.confidence > 0.7) {
        setNlpQuery(nlpCommand.smart_coding_action)
        await handleNLPQuery()
      }
    } catch (error) {
      console.error('Voice command processing failed:', error)
    } finally {
      setIsListening(false)
    }
  }

  const applyOptimizations = async (code: string, suggestions: string[]): Promise<string> => {
    // Mock optimization application
    let optimizedCode = code
    
    suggestions.forEach(suggestion => {
      if (suggestion.includes('const') && code.includes('var ')) {
        optimizedCode = optimizedCode.replace(/var /g, 'const ')
      }
      if (suggestion.includes('strict equality') && code.includes('==')) {
        optimizedCode = optimizedCode.replace(/==/g, '===')
      }
    })
    
    return optimizedCode
  }

  const getComplexityColor = (level: string) => {
    switch (level) {
      case 'simple': return 'text-green-600'
      case 'medium': return 'text-yellow-600'
      case 'complex': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getComplexityBadge = (level: string) => {
    switch (level) {
      case 'simple': return 'bg-green-100 text-green-800 border-green-200'
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'complex': return 'bg-red-100 text-red-800 border-red-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="space-y-6">
      {/* NLP Features Toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant={showNLPFeatures ? "default" : "outline"}
            onClick={() => setShowNLPFeatures(!showNLPFeatures)}
            className="flex items-center space-x-2"
          >
            <MessageSquare className="h-4 w-4" />
            <span>NLP Features</span>
          </Button>
          
          {showNLPFeatures && (
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCodeToNLP}
                disabled={isNLPProcessing}
                className="flex items-center space-x-2"
              >
                {isNLPProcessing ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
                ) : (
                  <BookOpen className="h-4 w-4" />
                )}
                <span>{isNLPProcessing ? 'Processing...' : 'Code to NLP'}</span>
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={handleSmartAnalysis}
                disabled={isAnalyzing}
                className="flex items-center space-x-2"
              >
                {isAnalyzing ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-purple-600 border-t-transparent" />
                ) : (
                  <Brain className="h-4 w-4" />
                )}
                <span>{isAnalyzing ? 'Analyzing...' : 'NLP Analysis'}</span>
              </Button>
            </div>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <Badge variant="outline">{language}</Badge>
          {showNLPFeatures && (
            <Badge variant="outline" className="flex items-center space-x-1">
              <MessageSquare className="h-3 w-3" />
              <span>NLP Enhanced</span>
            </Badge>
          )}
        </div>
      </div>

      {/* NLP Query Interface */}
      {showNLPFeatures && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center space-x-2">
              <MessageSquare className="h-5 w-5" />
              <span>Natural Language Query</span>
            </CardTitle>
            <CardDescription>
              Ask questions about your code in natural language
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex space-x-4">
                <input
                  type="text"
                  value={nlpQuery}
                  onChange={(e) => setNlpQuery(e.target.value)}
                  placeholder="Ask about your code... (e.g., 'optimize this function', 'explain this code', 'fix any issues')"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <Button 
                  onClick={handleNLPQuery}
                  disabled={!nlpQuery.trim() || isNLPProcessing}
                  className="flex items-center space-x-2"
                >
                  {isNLPProcessing ? (
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  ) : (
                    <Sparkles className="h-4 w-4" />
                  )}
                  <span>{isNLPProcessing ? 'Processing...' : 'Ask NLP'}</span>
                </Button>
              </div>
              
              {/* Voice Command Interface */}
              <div className="flex items-center space-x-4">
                <Button
                  variant="outline"
                  onClick={() => handleVoiceCommand('analyze this code')}
                  disabled={isListening}
                  className="flex items-center space-x-2"
                >
                  {isListening ? (
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
                  ) : (
                    <Mic className="h-4 w-4" />
                  )}
                  <span>{isListening ? 'Listening...' : 'Voice Command'}</span>
                </Button>
                
                {voiceCommand && (
                  <Badge variant="outline" className="flex items-center space-x-1">
                    <Volume2 className="h-3 w-3" />
                    <span>{voiceCommand}</span>
                  </Badge>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Main Editor Interface */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="editor">Editor</TabsTrigger>
          <TabsTrigger value="nlp">NLP Analysis</TabsTrigger>
          <TabsTrigger value="insights">Insights</TabsTrigger>
          <TabsTrigger value="complexity">Complexity</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="editor" className="space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <Code className="h-5 w-5" />
                <span>NLP-Enhanced Code Editor</span>
                {showNLPFeatures && (
                  <Badge variant="outline" className="ml-auto flex items-center space-x-1">
                    <MessageSquare className="h-3 w-3" />
                    <span>NLP Enabled</span>
                  </Badge>
                )}
              </CardTitle>
              <CardDescription>
                Enhanced with natural language processing capabilities
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
                <textarea
                  ref={textareaRef}
                  value={code}
                  onChange={(e) => handleCodeChange(e.target.value)}
                  placeholder="Enter your code here..."
                  className="w-full h-96 p-4 border border-gray-300 rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  style={{ fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace' }}
                />
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Button onClick={handleSave} size="sm">
                      <Save className="h-4 w-4 mr-2" />
                      Save
                    </Button>
                    
                    <Button variant="outline" size="sm">
                      <Download className="h-4 w-4 mr-2" />
                      Download
                    </Button>
                    
                    <Button variant="outline" size="sm">
                      <Upload className="h-4 w-4 mr-2" />
                      Upload
                    </Button>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Button variant="outline" size="sm">
                      <Play className="h-4 w-4 mr-2" />
                      Run
                    </Button>
                    
                    {showNLPFeatures && (
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={handleSmartAnalysis}
                        disabled={isAnalyzing}
                      >
                        <Brain className="h-4 w-4 mr-2" />
                        {isAnalyzing ? 'Analyzing...' : 'NLP Analysis'}
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="nlp" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="h-5 w-5" />
                <span>NLP Analysis Results</span>
                <Badge variant="outline">Natural Language Processing</Badge>
              </CardTitle>
              <CardDescription>
                AI-powered natural language analysis of your code
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {!nlpInsights ? (
                <div className="text-center py-8">
                  <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No NLP analysis yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Run NLP analysis to get natural language insights
                  </p>
                  <Button onClick={handleSmartAnalysis} disabled={isAnalyzing}>
                    {isAnalyzing ? 'Analyzing...' : 'Run NLP Analysis'}
                  </Button>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Code Understanding */}
                  <div>
                    <h4 className="font-semibold mb-3 flex items-center space-x-2">
                      <Target className="h-4 w-4" />
                      <span>Code Understanding</span>
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Card>
                        <CardContent className="p-4">
                          <h5 className="font-medium mb-2">Purpose</h5>
                          <p className="text-sm text-gray-600">{nlpInsights.code_understanding.purpose}</p>
                        </CardContent>
                      </Card>
                      <Card>
                        <CardContent className="p-4">
                          <h5 className="font-medium mb-2">Patterns</h5>
                          <div className="flex flex-wrap gap-1">
                            {nlpInsights.code_understanding.patterns.map((pattern, index) => (
                              <Badge key={index} variant="outline" className="text-xs">
                                {pattern}
                              </Badge>
                            ))}
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  </div>

                  {/* Natural Language Feedback */}
                  <div>
                    <h4 className="font-semibold mb-3 flex items-center space-x-2">
                      <BookOpen className="h-4 w-4" />
                      <span>Natural Language Feedback</span>
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm text-green-600">Strengths</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <ul className="text-sm space-y-1">
                            {nlpInsights.natural_language_feedback.strengths.map((strength, index) => (
                              <li key={index} className="flex items-center space-x-2">
                                <CheckCircle className="h-3 w-3 text-green-500" />
                                <span>{strength}</span>
                              </li>
                            ))}
                          </ul>
                        </CardContent>
                      </Card>
                      
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm text-yellow-600">Improvements</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <ul className="text-sm space-y-1">
                            {nlpInsights.natural_language_feedback.improvements.map((improvement, index) => (
                              <li key={index} className="flex items-center space-x-2">
                                <AlertTriangle className="h-3 w-3 text-yellow-500" />
                                <span>{improvement}</span>
                              </li>
                            ))}
                          </ul>
                        </CardContent>
                      </Card>
                      
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm text-blue-600">Suggestions</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <ul className="text-sm space-y-1">
                            {nlpInsights.natural_language_feedback.suggestions.map((suggestion, index) => (
                              <li key={index} className="flex items-center space-x-2">
                                <Lightbulb className="h-3 w-3 text-blue-500" />
                                <span>{suggestion}</span>
                              </li>
                            ))}
                          </ul>
                        </CardContent>
                      </Card>
                    </div>
                  </div>

                  {/* Smart Coding Integration */}
                  <div>
                    <h4 className="font-semibold mb-3 flex items-center space-x-2">
                      <Brain className="h-4 w-4" />
                      <span>Smart Coding Integration</span>
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm">Recommended Components</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <div className="flex flex-wrap gap-1">
                            {nlpInsights.smart_coding_integration.recommended_components.map((component, index) => (
                              <Badge key={index} variant="outline" className="text-xs">
                                {component}
                              </Badge>
                            ))}
                          </div>
                        </CardContent>
                      </Card>
                      
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm">Optimization Opportunities</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <ul className="text-sm space-y-1">
                            {nlpInsights.smart_coding_integration.optimization_opportunities.map((opportunity, index) => (
                              <li key={index} className="flex items-center space-x-2">
                                <Zap className="h-3 w-3 text-orange-500" />
                                <span>{opportunity}</span>
                              </li>
                            ))}
                          </ul>
                        </CardContent>
                      </Card>
                      
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm">AI Enhancements</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <ul className="text-sm space-y-1">
                            {nlpInsights.smart_coding_integration.ai_enhancements.map((enhancement, index) => (
                              <li key={index} className="flex items-center space-x-2">
                                <Sparkles className="h-3 w-3 text-purple-500" />
                                <span>{enhancement}</span>
                              </li>
                            ))}
                          </ul>
                        </CardContent>
                      </Card>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="insights" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BookOpen className="h-5 w-5" />
                <span>Natural Language Description</span>
              </CardTitle>
              <CardDescription>
                AI-generated natural language description of your code
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {!naturalLanguageDescription ? (
                <div className="text-center py-8">
                  <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No description yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Convert your code to natural language description
                  </p>
                  <Button onClick={handleCodeToNLP} disabled={isNLPProcessing}>
                    {isNLPProcessing ? 'Processing...' : 'Generate Description'}
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <Card className="bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800">
                    <CardContent className="p-4">
                      <h4 className="font-medium mb-2 text-blue-800 dark:text-blue-200">Code Description</h4>
                      <p className="text-sm text-blue-700 dark:text-blue-300">{naturalLanguageDescription}</p>
                    </CardContent>
                  </Card>
                  
                  {codeComplexity && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm">Complexity Level</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <Badge className={`${getComplexityBadge(codeComplexity.level)}`}>
                            {codeComplexity.level.toUpperCase()}
                          </Badge>
                        </CardContent>
                      </Card>
                      
                      <Card>
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm">Complexity Score</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <div className="text-2xl font-bold text-gray-900 dark:text-white">
                            {Math.round(codeComplexity.score * 100)}%
                          </div>
                        </CardContent>
                      </Card>
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="complexity" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Target className="h-5 w-5" />
                <span>Code Complexity Analysis</span>
              </CardTitle>
              <CardDescription>
                Detailed analysis of code complexity and maintainability
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {!codeComplexity ? (
                <div className="text-center py-8">
                  <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No complexity analysis yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Analyze your code complexity
                  </p>
                  <Button onClick={handleCodeToNLP} disabled={isNLPProcessing}>
                    {isNLPProcessing ? 'Processing...' : 'Analyze Complexity'}
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm">Complexity Level</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="flex items-center space-x-2">
                          <Badge className={`${getComplexityBadge(codeComplexity.level)}`}>
                            {codeComplexity.level.toUpperCase()}
                          </Badge>
                          <span className={`text-sm font-medium ${getComplexityColor(codeComplexity.level)}`}>
                            {Math.round(codeComplexity.score * 100)}%
                          </span>
                        </div>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm">Complexity Factors</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <ul className="text-sm space-y-1">
                          {codeComplexity.factors.map((factor: string, index: number) => (
                            <li key={index} className="flex items-center space-x-2">
                              <AlertTriangle className="h-3 w-3 text-orange-500" />
                              <span>{factor}</span>
                            </li>
                          ))}
                        </ul>
                      </CardContent>
                    </Card>
                    
                    <Card>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-sm">Recommendations</CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="text-sm text-gray-600">
                          {codeComplexity.level === 'complex' && 'Consider breaking down into smaller functions'}
                          {codeComplexity.level === 'medium' && 'Code is moderately complex, consider refactoring'}
                          {codeComplexity.level === 'simple' && 'Code is well-structured and maintainable'}
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Settings className="h-5 w-5" />
                <span>NLP Editor Settings</span>
              </CardTitle>
              <CardDescription>
                Configure NLP and Smart Coding AI features
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">NLP Features</label>
                    <p className="text-xs text-gray-500">Enable natural language processing</p>
                  </div>
                  <Button variant="outline" size="sm">
                    {showNLPFeatures ? 'Enabled' : 'Disabled'}
                  </Button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Voice Commands</label>
                    <p className="text-xs text-gray-500">Enable voice control for NLP features</p>
                  </div>
                  <Button variant="outline" size="sm">Enabled</Button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Auto Analysis</label>
                    <p className="text-xs text-gray-500">Automatically analyze code changes</p>
                  </div>
                  <Button variant="outline" size="sm">Enabled</Button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Smart Suggestions</label>
                    <p className="text-xs text-gray-500">AI-powered code suggestions</p>
                  </div>
                  <Button variant="outline" size="sm">Enabled</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
