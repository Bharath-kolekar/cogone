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
  Volume2
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { apiService } from '@/lib/api'

interface SmartCodeEditorProps {
  initialCode?: string
  language?: string
  onCodeChange?: (code: string) => void
  onSave?: (code: string) => void
  onSmartAnalysis?: (analysis: any) => void
  onIntegrationResult?: (result: any) => void
}

interface CodeAnalysis {
  id: string
  type: 'suggestion' | 'error' | 'optimization' | 'security'
  message: string
  line?: number
  confidence: number
  source: string
}

interface IntegrationResult {
  responseId: string
  primaryResponse: any
  supportingResponses: Record<string, any>
  confidence: number
  integrationMetadata: Record<string, any>
  timestamp: string
}

export function SmartCodeEditor({
  initialCode = '',
  language = 'javascript',
  onCodeChange,
  onSave,
  onSmartAnalysis,
  onIntegrationResult
}: SmartCodeEditorProps) {
  const [code, setCode] = useState(initialCode)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [isIntegrating, setIsIntegrating] = useState(false)
  const [analyses, setAnalyses] = useState<CodeAnalysis[]>([])
  const [integrationResults, setIntegrationResults] = useState<IntegrationResult[]>([])
  const [selectedText, setSelectedText] = useState('')
  const [showSmartFeatures, setShowSmartFeatures] = useState(false)
  const [activeTab, setActiveTab] = useState('editor')
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

  const handleSmartAnalysis = async () => {
    try {
      setIsAnalyzing(true)
      
      // Mock smart analysis - in real implementation, this would call the backend
      const mockAnalyses: CodeAnalysis[] = [
        {
          id: '1',
          type: 'suggestion',
          message: 'Consider using const instead of let for variables that won\'t be reassigned',
          line: 3,
          confidence: 0.85,
          source: 'Code Quality Analyzer'
        },
        {
          id: '2',
          type: 'optimization',
          message: 'This function could be optimized using async/await pattern',
          line: 7,
          confidence: 0.92,
          source: 'Performance Optimizer'
        },
        {
          id: '3',
          type: 'security',
          message: 'Consider adding input validation for user data',
          line: 12,
          confidence: 0.88,
          source: 'Security Validator'
        }
      ]

      setAnalyses(mockAnalyses)
      onSmartAnalysis?.(mockAnalyses)
    } catch (error) {
      console.error('Smart analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleSmartIntegration = async (integrationType: string) => {
    try {
      setIsIntegrating(true)
      
      // Mock integration - in real implementation, this would call the backend
      const mockResult: IntegrationResult = {
        responseId: `result-${Date.now()}`,
        primaryResponse: {
          message: `Smart Coding AI integration completed for ${integrationType}`,
          confidence: 0.94,
          enhanced_code: code + '\n// Enhanced by Smart Coding AI',
          suggestions: ['Added error handling', 'Optimized performance', 'Enhanced security']
        },
        supportingResponses: {
          integration_type: integrationType,
          components_used: ['ai-orchestrator', 'accuracy-validation', 'security-validator'],
          processing_time: '1.8s'
        },
        confidence: 0.94,
        integrationMetadata: {
          integration_type: integrationType,
          timestamp: new Date().toISOString(),
          success: true
        },
        timestamp: new Date().toISOString()
      }

      setIntegrationResults(prev => [mockResult, ...prev])
      onIntegrationResult?.(mockResult)
    } catch (error) {
      console.error('Smart integration failed:', error)
    } finally {
      setIsIntegrating(false)
    }
  }

  const handleTextSelection = () => {
    const textarea = textareaRef.current
    if (textarea) {
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const selected = code.substring(start, end)
      setSelectedText(selected)
    }
  }

  const handleCtrlL = (e: React.KeyboardEvent) => {
    if (e.ctrlKey && e.key === 'l') {
      e.preventDefault()
      if (selectedText.trim()) {
        handleSmartIntegration('selected_code_analysis')
      } else {
        handleSmartAnalysis()
      }
    }
  }

  const getAnalysisIcon = (type: string) => {
    switch (type) {
      case 'suggestion':
        return <Lightbulb className="h-4 w-4 text-yellow-500" />
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-red-500" />
      case 'optimization':
        return <Zap className="h-4 w-4 text-blue-500" />
      case 'security':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      default:
        return <Lightbulb className="h-4 w-4 text-gray-500" />
    }
  }

  const getAnalysisColor = (type: string) => {
    switch (type) {
      case 'suggestion':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800'
      case 'error':
        return 'bg-red-50 border-red-200 text-red-800'
      case 'optimization':
        return 'bg-blue-50 border-blue-200 text-blue-800'
      case 'security':
        return 'bg-green-50 border-green-200 text-green-800'
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800'
    }
  }

  return (
    <div className="space-y-6">
      {/* Smart Features Toggle */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button
            variant={showSmartFeatures ? "default" : "outline"}
            onClick={() => setShowSmartFeatures(!showSmartFeatures)}
            className="flex items-center space-x-2"
          >
            <Brain className="h-4 w-4" />
            <span>Smart Features</span>
          </Button>
          
          {showSmartFeatures && (
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleSmartAnalysis}
                disabled={isAnalyzing}
                className="flex items-center space-x-2"
              >
                {isAnalyzing ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
                ) : (
                  <Cpu className="h-4 w-4" />
                )}
                <span>{isAnalyzing ? 'Analyzing...' : 'Smart Analysis'}</span>
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => handleSmartIntegration('comprehensive')}
                disabled={isIntegrating}
                className="flex items-center space-x-2"
              >
                {isIntegrating ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-purple-600 border-t-transparent" />
                ) : (
                  <Brain className="h-4 w-4" />
                )}
                <span>{isIntegrating ? 'Integrating...' : 'Smart Integration'}</span>
              </Button>
            </div>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <Badge variant="outline">{language}</Badge>
          {showSmartFeatures && (
            <Badge variant="outline" className="flex items-center space-x-1">
              <Brain className="h-3 w-3" />
              <span>AI Enhanced</span>
            </Badge>
          )}
        </div>
      </div>

      {/* Main Editor Interface */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="editor">Editor</TabsTrigger>
          <TabsTrigger value="analysis">Analysis</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="editor" className="space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <Code className="h-5 w-5" />
                <span>Code Editor</span>
                {selectedText && (
                  <Badge variant="outline" className="ml-auto">
                    {selectedText.length} chars selected
                  </Badge>
                )}
              </CardTitle>
              <CardDescription>
                Press Ctrl+L for smart analysis or select text and press Ctrl+L for selected code analysis
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
                <textarea
                  ref={textareaRef}
                  value={code}
                  onChange={(e) => handleCodeChange(e.target.value)}
                  onSelect={handleTextSelection}
                  onKeyDown={handleCtrlL}
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
                    
                    {showSmartFeatures && (
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={handleSmartAnalysis}
                        disabled={isAnalyzing}
                      >
                        <Brain className="h-4 w-4 mr-2" />
                        {isAnalyzing ? 'Analyzing...' : 'Smart Analysis'}
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analysis" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Cpu className="h-5 w-5" />
                <span>Smart Analysis</span>
                <Badge variant="outline">{analyses.length} findings</Badge>
              </CardTitle>
              <CardDescription>
                AI-powered code analysis and suggestions
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {analyses.length === 0 ? (
                <div className="text-center py-8">
                  <Cpu className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No analysis yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Run smart analysis to get AI-powered insights
                  </p>
                  <Button onClick={handleSmartAnalysis} disabled={isAnalyzing}>
                    {isAnalyzing ? 'Analyzing...' : 'Run Analysis'}
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {analyses.map((analysis) => (
                    <motion.div
                      key={analysis.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 }}
                    >
                      <Card className={`border-l-4 ${getAnalysisColor(analysis.type)}`}>
                        <CardContent className="p-4">
                          <div className="flex items-start space-x-3">
                            {getAnalysisIcon(analysis.type)}
                            <div className="flex-1">
                              <div className="flex items-center justify-between mb-2">
                                <h4 className="font-medium capitalize">{analysis.type}</h4>
                                <Badge variant="outline">
                                  {Math.round(analysis.confidence * 100)}% confidence
                                </Badge>
                              </div>
                              <p className="text-sm mb-2">{analysis.message}</p>
                              <div className="flex items-center justify-between text-xs text-gray-500">
                                <span>Source: {analysis.source}</span>
                                {analysis.line && <span>Line {analysis.line}</span>}
                              </div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="integrations" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5" />
                <span>Smart Integration Results</span>
                <Badge variant="outline">{integrationResults.length} integrations</Badge>
              </CardTitle>
              <CardDescription>
                Results from Smart Coding AI integration across 44+ components
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {integrationResults.length === 0 ? (
                <div className="text-center py-8">
                  <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                    No integrations yet
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    Run smart integration to see results from all AI components
                  </p>
                  <Button onClick={() => handleSmartIntegration('comprehensive')} disabled={isIntegrating}>
                    {isIntegrating ? 'Integrating...' : 'Run Integration'}
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {integrationResults.map((result, index) => (
                    <motion.div
                      key={result.responseId}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <Card>
                        <CardHeader className="pb-3">
                          <div className="flex items-center justify-between">
                            <CardTitle className="text-sm">
                              Integration Result #{index + 1}
                            </CardTitle>
                            <Badge variant="outline">
                              {Math.round(result.confidence * 100)}% confidence
                            </Badge>
                          </div>
                          <CardDescription className="text-xs">
                            {new Date(result.timestamp).toLocaleString()}
                          </CardDescription>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-3">
                            <div className="text-sm">
                              <strong>Response:</strong> {result.primaryResponse.message}
                            </div>
                            
                            {result.primaryResponse.suggestions && (
                              <div className="text-sm">
                                <strong>Suggestions:</strong>
                                <ul className="list-disc list-inside ml-4 mt-1">
                                  {result.primaryResponse.suggestions.map((suggestion: string, i: number) => (
                                    <li key={i} className="text-xs">{suggestion}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            
                            <div className="grid grid-cols-2 gap-4 text-xs text-gray-500">
                              <div>
                                <strong>Components Used:</strong> {result.supportingResponses.components_used?.length || 0}
                              </div>
                              <div>
                                <strong>Processing Time:</strong> {result.supportingResponses.processing_time}
                              </div>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
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
                <span>Smart Editor Settings</span>
              </CardTitle>
              <CardDescription>
                Configure Smart Coding AI features and preferences
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Smart Analysis</label>
                    <p className="text-xs text-gray-500">Enable AI-powered code analysis</p>
                  </div>
                  <Button variant="outline" size="sm">
                    {showSmartFeatures ? 'Enabled' : 'Disabled'}
                  </Button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Auto-save</label>
                    <p className="text-xs text-gray-500">Automatically save changes</p>
                  </div>
                  <Button variant="outline" size="sm">Enabled</Button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Voice Commands</label>
                    <p className="text-xs text-gray-500">Enable voice control for Smart Coding AI</p>
                  </div>
                  <Button variant="outline" size="sm">Enabled</Button>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium">Integration Notifications</label>
                    <p className="text-xs text-gray-500">Show notifications for integration results</p>
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
