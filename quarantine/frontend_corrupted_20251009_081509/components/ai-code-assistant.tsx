/**
 * AI Code Assistant Component
 * Integrates multiple AI components for enhanced code editing
 */

'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Brain, 
  Code, 
  Shield, 
  Zap, 
  Eye, 
  TestTube, 
  BookOpen, 
  Lightbulb,
  AlertTriangle,
  CheckCircle,
  Loader2,
  Sparkles
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { apiService } from '@/lib/api'

interface AIAnalysis {
  type: 'security' | 'performance' | 'quality' | 'suggestions' | 'documentation' | 'testing'
  title: string
  description: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  suggestions: string[]
  confidence: number
}

interface AIAssistantProps {
  code: string
  language: string
  onAnalysisComplete?: (analysis: AIAnalysis[]) => void
}

export function AIAssistant({ code, language, onAnalysisComplete }: AIAssistantProps) {
  const [analyses, setAnalyses] = useState<AIAnalysis[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')
  const [selectedAnalysis, setSelectedAnalysis] = useState<AIAnalysis | null>(null)

  useEffect(() => {
    if (code.trim()) {
      analyzeCode()
    }
  }, [code, language])

  const analyzeCode = async () => {
    setIsAnalyzing(true)
    setAnalyses([])

    try {
      // Parallel AI analysis using different components
      const [
        securityAnalysis,
        performanceAnalysis,
        qualityAnalysis,
        suggestionsAnalysis,
        documentationAnalysis,
        testingAnalysis
      ] = await Promise.all([
        analyzeSecurity(code, language),
        analyzePerformance(code, language),
        analyzeQuality(code, language),
        getSuggestions(code, language),
        analyzeDocumentation(code, language),
        generateTests(code, language)
      ])

      const allAnalyses = [
        ...securityAnalysis,
        ...performanceAnalysis,
        ...qualityAnalysis,
        ...suggestionsAnalysis,
        ...documentationAnalysis,
        ...testingAnalysis
      ]

      setAnalyses(allAnalyses)
      onAnalysisComplete?.(allAnalyses)
    } catch (error) {
      console.error('AI analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  // AI Component Integrations
  const analyzeSecurity = async (code: string, language: string): Promise<AIAnalysis[]> => {
    try {
      const response = await apiService.analyzeCodeSecurity(code, language)
      if (response.success && response.data) {
        return response.data.vulnerabilities.map((vuln: any) => ({
          type: 'security' as const,
          title: vuln.title,
          description: vuln.description,
          severity: vuln.severity,
          suggestions: vuln.fixes,
          confidence: vuln.confidence
        }))
      }
    } catch (error) {
      console.error('Security analysis failed:', error)
    }
    return []
  }

  const analyzePerformance = async (code: string, language: string): Promise<AIAnalysis[]> => {
    try {
      const response = await apiService.analyzeCodePerformance(code, language)
      if (response.success && response.data) {
        return response.data.issues.map((issue: any) => ({
          type: 'performance' as const,
          title: issue.title,
          description: issue.description,
          severity: issue.severity,
          suggestions: issue.optimizations,
          confidence: issue.confidence
        }))
      }
    } catch (error) {
      console.error('Performance analysis failed:', error)
    }
    return []
  }

  const analyzeQuality = async (code: string, language: string): Promise<AIAnalysis[]> => {
    try {
      const response = await apiService.analyzeCodeQuality(code, language)
      if (response.success && response.data) {
        return response.data.issues.map((issue: any) => ({
          type: 'quality' as const,
          title: issue.title,
          description: issue.description,
          severity: issue.severity,
          suggestions: issue.improvements,
          confidence: issue.confidence
        }))
      }
    } catch (error) {
      console.error('Quality analysis failed:', error)
    }
    return []
  }

  const getSuggestions = async (code: string, language: string): Promise<AIAnalysis[]> => {
    try {
      const response = await apiService.getCodeSuggestions(code, language)
      if (response.success && response.data) {
        return response.data.map((suggestion: any) => ({
          type: 'suggestions' as const,
          title: suggestion.title,
          description: suggestion.description,
          severity: 'low' as const,
          suggestions: [suggestion.improvement],
          confidence: suggestion.confidence
        }))
      }
    } catch (error) {
      console.error('Suggestions analysis failed:', error)
    }
    return []
  }

  const analyzeDocumentation = async (code: string, language: string): Promise<AIAnalysis[]> => {
    try {
      const response = await apiService.analyzeDocumentation(code, language)
      if (response.success && response.data) {
        return response.data.issues.map((issue: any) => ({
          type: 'documentation' as const,
          title: issue.title,
          description: issue.description,
          severity: issue.severity,
          suggestions: issue.improvements,
          confidence: issue.confidence
        }))
      }
    } catch (error) {
      console.error('Documentation analysis failed:', error)
    }
    return []
  }

  const generateTests = async (code: string, language: string): Promise<AIAnalysis[]> => {
    try {
      const response = await apiService.generateCodeTests(code, language)
      if (response.success && response.data) {
        return [{
          type: 'testing' as const,
          title: 'Test Coverage Analysis',
          description: response.data.description,
          severity: 'medium' as const,
          suggestions: response.data.testSuggestions,
          confidence: response.data.confidence
        }]
      }
    } catch (error) {
      console.error('Test generation failed:', error)
    }
    return []
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      case 'high': return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400'
      case 'medium': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
      case 'low': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'security': return <Shield className="h-4 w-4" />
      case 'performance': return <Zap className="h-4 w-4" />
      case 'quality': return <Code className="h-4 w-4" />
      case 'suggestions': return <Lightbulb className="h-4 w-4" />
      case 'documentation': return <BookOpen className="h-4 w-4" />
      case 'testing': return <TestTube className="h-4 w-4" />
      default: return <Brain className="h-4 w-4" />
    }
  }

  const criticalIssues = analyses.filter(a => a.severity === 'critical').length
  const highIssues = analyses.filter(a => a.severity === 'high').length
  const mediumIssues = analyses.filter(a => a.severity === 'medium').length
  const lowIssues = analyses.filter(a => a.severity === 'low').length

  return (
    <div className="space-y-4">
      {/* AI Analysis Header */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <Brain className="h-5 w-5 text-blue-600" />
              <span>AI Code Analysis</span>
              {isAnalyzing && <Loader2 className="h-4 w-4 animate-spin text-blue-600" />}
            </CardTitle>
            
            <div className="flex items-center space-x-2">
              <Badge variant="outline" className="text-xs">
                {analyses.length} insights
              </Badge>
              {criticalIssues > 0 && (
                <Badge className="bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400">
                  {criticalIssues} critical
                </Badge>
              )}
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          {/* Analysis Summary */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
              <div className="text-2xl font-bold text-red-600">{criticalIssues}</div>
              <div className="text-xs text-red-600">Critical</div>
            </div>
            <div className="text-center p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">{highIssues}</div>
              <div className="text-xs text-orange-600">High</div>
            </div>
            <div className="text-center p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">{mediumIssues}</div>
              <div className="text-xs text-yellow-600">Medium</div>
            </div>
            <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{lowIssues}</div>
              <div className="text-xs text-green-600">Low</div>
            </div>
          </div>

          {/* AI Analysis Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid w-full grid-cols-6">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="security">Security</TabsTrigger>
              <TabsTrigger value="performance">Performance</TabsTrigger>
              <TabsTrigger value="quality">Quality</TabsTrigger>
              <TabsTrigger value="suggestions">Suggestions</TabsTrigger>
              <TabsTrigger value="testing">Testing</TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {analyses.slice(0, 6).map((analysis, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Card 
                      className="cursor-pointer hover:shadow-md transition-shadow"
                      onClick={() => setSelectedAnalysis(analysis)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-start space-x-3">
                          <div className="flex-shrink-0">
                            {getTypeIcon(analysis.type)}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center space-x-2 mb-1">
                              <h4 className="text-sm font-medium truncate">{analysis.title}</h4>
                              <Badge className={getSeverityColor(analysis.severity)}>
                                {analysis.severity}
                              </Badge>
                            </div>
                            <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">
                              {analysis.description}
                            </p>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </TabsContent>

            {['security', 'performance', 'quality', 'suggestions', 'testing'].map(tab => (
              <TabsContent key={tab} value={tab} className="space-y-4">
                <div className="space-y-3">
                  {analyses
                    .filter(a => a.type === tab)
                    .map((analysis, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <Card>
                          <CardHeader className="pb-3">
                            <div className="flex items-center justify-between">
                              <CardTitle className="text-sm flex items-center space-x-2">
                                {getTypeIcon(analysis.type)}
                                <span>{analysis.title}</span>
                              </CardTitle>
                              <div className="flex items-center space-x-2">
                                <Badge className={getSeverityColor(analysis.severity)}>
                                  {analysis.severity}
                                </Badge>
                                <Badge variant="outline">
                                  {Math.round(analysis.confidence * 100)}% confidence
                                </Badge>
                              </div>
                            </div>
                          </CardHeader>
                          <CardContent>
                            <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                              {analysis.description}
                            </p>
                            {analysis.suggestions.length > 0 && (
                              <div>
                                <h5 className="text-sm font-medium mb-2">Suggestions:</h5>
                                <ul className="space-y-1">
                                  {analysis.suggestions.map((suggestion, idx) => (
                                    <li key={idx} className="text-sm text-gray-600 dark:text-gray-400 flex items-start space-x-2">
                                      <span className="text-blue-600 mt-1">•</span>
                                      <span>{suggestion}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      </motion.div>
                    ))}
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </CardContent>
      </Card>

      {/* Detailed Analysis Modal */}
      <AnimatePresence>
        {selectedAnalysis && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
            onClick={() => setSelectedAnalysis(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold flex items-center space-x-2">
                  {getTypeIcon(selectedAnalysis.type)}
                  <span>{selectedAnalysis.title}</span>
                </h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedAnalysis(null)}
                >
                  ×
                </Button>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <Badge className={getSeverityColor(selectedAnalysis.severity)}>
                    {selectedAnalysis.severity}
                  </Badge>
                  <Badge variant="outline">
                    {Math.round(selectedAnalysis.confidence * 100)}% confidence
                  </Badge>
                </div>
                
                <p className="text-gray-600 dark:text-gray-400">
                  {selectedAnalysis.description}
                </p>
                
                {selectedAnalysis.suggestions.length > 0 && (
                  <div>
                    <h4 className="font-medium mb-2">AI Suggestions:</h4>
                    <ul className="space-y-2">
                      {selectedAnalysis.suggestions.map((suggestion, idx) => (
                        <li key={idx} className="flex items-start space-x-2">
                          <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                          <span className="text-sm">{suggestion}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
