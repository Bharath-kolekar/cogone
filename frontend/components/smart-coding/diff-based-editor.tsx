'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Code, GitBranch, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, Play, Pause, RotateCcw, Settings, Zap, Target, TrendingUp } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'

interface CodeChange {
  id: string
  filePath: string
  type: 'addition' | 'deletion' | 'modification'
  oldCode: string
  newCode: string
  lineNumber: number
  description: string
  impact: 'low' | 'medium' | 'high'
  confidence: number
}

interface DiffBasedEditorProps {
  initialCode?: string
  onChangesAccepted?: (changes: CodeChange[]) => void
  onChangesRejected?: (changes: CodeChange[]) => void
  showPreview?: boolean
  enableRealTimeDiff?: boolean
  className?: string
}

export function DiffBasedEditor({
  initialCode = '',
  onChangesAccepted,
  onChangesRejected,
  showPreview = true,
  enableRealTimeDiff = true,
  className = ''
}: DiffBasedEditorProps) {
  const [originalCode, setOriginalCode] = useState(initialCode)
  const [modifiedCode, setModifiedCode] = useState(initialCode)
  const [changes, setChanges] = useState<CodeChange[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisStep, setAnalysisStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('editor')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedChange, setSelectedChange] = useState<string | null>(null)
  const [acceptedChanges, setAcceptedChanges] = useState<Set<string>>(new Set())
  const [rejectedChanges, setRejectedChanges] = useState<Set<string>>(new Set())
  const [isGenerating, setIsGenerating] = useState(false)
  const editorRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    if (enableRealTimeDiff && modifiedCode !== originalCode) {
      analyzeChanges()
    }
  }, [modifiedCode, originalCode, enableRealTimeDiff])

  const analyzeChanges = async () => {
    setIsAnalyzing(true)
    setProgress(0)
    setAnalysisStep('Analyzing code changes...')

    try {
      // Simulate advanced diff analysis
      const steps = [
        'Parsing code structure...',
        'Identifying syntax changes...',
        'Analyzing semantic modifications...',
        'Detecting potential issues...',
        'Generating diff visualization...',
        'Calculating impact assessment...',
        'Finalizing change recommendations...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setAnalysisStep(steps[i])
        setProgress((i + 1) * 14.3)
        await new Promise(resolve => setTimeout(resolve, 200))
      }

      // Generate mock changes based on code differences
      const mockChanges = generateMockChanges(originalCode, modifiedCode)
      setChanges(mockChanges)

    } catch (error) {
      console.error('Change analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
      setProgress(100)
      setAnalysisStep('Analysis complete!')
    }
  }

  const generateMockChanges = (oldCode: string, newCode: string): CodeChange[] => {
    const changes: CodeChange[] = []
    const oldLines = oldCode.split('\n')
    const newLines = newCode.split('\n')

    // Simple diff algorithm simulation
    let oldIndex = 0
    let newIndex = 0
    let changeId = 0

    while (oldIndex < oldLines.length || newIndex < newLines.length) {
      if (oldIndex >= oldLines.length) {
        // Addition
        changes.push({
          id: `change-${changeId++}`,
          filePath: 'main.tsx',
          type: 'addition',
          oldCode: '',
          newCode: newLines[newIndex],
          lineNumber: newIndex + 1,
          description: `Added line ${newIndex + 1}`,
          impact: 'low',
          confidence: 0.9
        })
        newIndex++
      } else if (newIndex >= newLines.length) {
        // Deletion
        changes.push({
          id: `change-${changeId++}`,
          filePath: 'main.tsx',
          type: 'deletion',
          oldCode: oldLines[oldIndex],
          newCode: '',
          lineNumber: oldIndex + 1,
          description: `Removed line ${oldIndex + 1}`,
          impact: 'medium',
          confidence: 0.8
        })
        oldIndex++
      } else if (oldLines[oldIndex] === newLines[newIndex]) {
        // No change
        oldIndex++
        newIndex++
      } else {
        // Modification
        changes.push({
          id: `change-${changeId++}`,
          filePath: 'main.tsx',
          type: 'modification',
          oldCode: oldLines[oldIndex],
          newCode: newLines[newIndex],
          lineNumber: oldIndex + 1,
          description: `Modified line ${oldIndex + 1}`,
          impact: 'high',
          confidence: 0.85
        })
        oldIndex++
        newIndex++
      }
    }

    return changes
  }

  const acceptChange = (changeId: string) => {
    setAcceptedChanges(prev => new Set([...prev, changeId]))
    setRejectedChanges(prev => {
      const newSet = new Set(prev)
      newSet.delete(changeId)
      return newSet
    })
  }

  const rejectChange = (changeId: string) => {
    setRejectedChanges(prev => new Set([...prev, changeId]))
    setAcceptedChanges(prev => {
      const newSet = new Set(prev)
      newSet.delete(changeId)
      return newSet
    })
  }

  const acceptAllChanges = () => {
    const allChangeIds = changes.map(change => change.id)
    setAcceptedChanges(new Set(allChangeIds))
    setRejectedChanges(new Set())
    onChangesAccepted?.(changes)
  }

  const rejectAllChanges = () => {
    const allChangeIds = changes.map(change => change.id)
    setRejectedChanges(new Set(allChangeIds))
    setAcceptedChanges(new Set())
    onChangesRejected?.(changes)
  }

  const generateSmartChanges = async () => {
    setIsGenerating(true)
    setAnalysisStep('Generating smart code changes...')

    try {
      // Simulate AI-powered code generation
      await new Promise(resolve => setTimeout(resolve, 2000))

      const smartChanges: CodeChange[] = [
        {
          id: 'smart-1',
          filePath: 'components/UserProfile.tsx',
          type: 'addition',
          oldCode: '',
          newCode: 'const [loading, setLoading] = useState(false);',
          lineNumber: 5,
          description: 'Add loading state management',
          impact: 'medium',
          confidence: 0.95
        },
        {
          id: 'smart-2',
          filePath: 'components/UserProfile.tsx',
          type: 'addition',
          oldCode: '',
          newCode: 'const [error, setError] = useState(null);',
          lineNumber: 6,
          description: 'Add error state management',
          impact: 'medium',
          confidence: 0.95
        },
        {
          id: 'smart-3',
          filePath: 'components/UserProfile.tsx',
          type: 'modification',
          oldCode: 'const user = await getUser(id);',
          newCode: `try {
  const user = await getUser(id);
  if (!user) throw new Error('User not found');
} catch (error) {
  console.error('Failed to fetch user:', error);
}`,
          lineNumber: 15,
          description: 'Add error handling for user fetch',
          impact: 'high',
          confidence: 0.9
        }
      ]

      setChanges(prev => [...prev, ...smartChanges])

    } catch (error) {
      console.error('Smart generation failed:', error)
    } finally {
      setIsGenerating(false)
      setAnalysisStep('Smart generation complete!')
    }
  }

  const getChangeTypeColor = (type: string) => {
    switch (type) {
      case 'addition': return 'text-green-600 bg-green-100'
      case 'deletion': return 'text-red-600 bg-red-100'
      case 'modification': return 'text-blue-600 bg-blue-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const renderDiffLine = (change: CodeChange) => {
    const isAccepted = acceptedChanges.has(change.id)
    const isRejected = rejectedChanges.has(change.id)
    const isSelected = selectedChange === change.id

    return (
      <motion.div
        key={change.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        } ${isAccepted ? 'bg-green-50 dark:bg-green-900/20' : ''} ${isRejected ? 'bg-red-50 dark:bg-red-900/20' : ''}`}
        onClick={() => setSelectedChange(selectedChange === change.id ? null : change.id)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Badge className={getChangeTypeColor(change.type)}>
              {change.type.toUpperCase()}
            </Badge>
            <Badge className={getImpactColor(change.impact)}>
              {change.impact.toUpperCase()}
            </Badge>
            <Badge className={getConfidenceColor(change.confidence)}>
              {(change.confidence * 100).toFixed(0)}%
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                acceptChange(change.id)
              }}
              disabled={isAccepted}
            >
              <CheckCircle className="h-4 w-4 mr-1" />
              Accept
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                rejectChange(change.id)
              }}
              disabled={isRejected}
            >
              <XCircle className="h-4 w-4 mr-1" />
              Reject
            </Button>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          {change.description} (Line {change.lineNumber})
        </div>

        <div className="space-y-2">
          {change.oldCode && (
            <div className="bg-red-50 dark:bg-red-900/20 p-2 rounded border-l-4 border-red-500">
              <div className="text-xs text-red-600 dark:text-red-400 mb-1">- Old Code:</div>
              <code className="text-sm text-red-800 dark:text-red-200">{change.oldCode}</code>
            </div>
          )}
          {change.newCode && (
            <div className="bg-green-50 dark:bg-green-900/20 p-2 rounded border-l-4 border-green-500">
              <div className="text-xs text-green-600 dark:text-green-400 mb-1">+ New Code:</div>
              <code className="text-sm text-green-800 dark:text-green-200">{change.newCode}</code>
            </div>
          )}
        </div>
      </motion.div>
    )
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Code className="h-6 w-6 text-blue-600" />
                <span>Diff-Based Editor</span>
              </CardTitle>
              <CardDescription>
                Precise code changes with visual diff and impact analysis
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={generateSmartChanges}
                disabled={isGenerating}
              >
                <Zap className="h-4 w-4 mr-1" />
                {isGenerating ? 'Generating...' : 'Smart Generate'}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={acceptAllChanges}
                disabled={changes.length === 0}
              >
                <CheckCircle className="h-4 w-4 mr-1" />
                Accept All
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={rejectAllChanges}
                disabled={changes.length === 0}
              >
                <XCircle className="h-4 w-4 mr-1" />
                Reject All
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Analysis Status */}
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
                  {analysisStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Editor and Changes */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="editor">Code Editor</TabsTrigger>
          <TabsTrigger value="changes">Changes ({changes.length})</TabsTrigger>
          <TabsTrigger value="preview">Preview</TabsTrigger>
        </TabsList>

        <TabsContent value="editor" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Code className="h-4 w-4" />
                  <span>Original Code</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Textarea
                  ref={editorRef}
                  value={originalCode}
                  onChange={(e) => setOriginalCode(e.target.value)}
                  placeholder="Enter your original code here..."
                  className="min-h-[300px] font-mono text-sm"
                />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <GitBranch className="h-4 w-4" />
                  <span>Modified Code</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Textarea
                  value={modifiedCode}
                  onChange={(e) => setModifiedCode(e.target.value)}
                  placeholder="Enter your modified code here..."
                  className="min-h-[300px] font-mono text-sm"
                />
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="changes" className="space-y-4">
          {changes.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <Code className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                  No Changes Detected
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Modify the code in the editor to see changes here.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Badge variant="outline">
                    Total Changes: {changes.length}
                  </Badge>
                  <Badge variant="outline" className="text-green-600">
                    Accepted: {acceptedChanges.size}
                  </Badge>
                  <Badge variant="outline" className="text-red-600">
                    Rejected: {rejectedChanges.size}
                  </Badge>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setShowAdvanced(!showAdvanced)}
                  >
                    <Settings className="h-4 w-4 mr-1" />
                    {showAdvanced ? 'Hide' : 'Show'} Advanced
                  </Button>
                </div>
              </div>

              <div className="space-y-3">
                {changes.map(renderDiffLine)}
              </div>
            </div>
          )}
        </TabsContent>

        <TabsContent value="preview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Eye className="h-4 w-4" />
                <span>Code Preview</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                <pre>{modifiedCode || 'No code to preview'}</pre>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
