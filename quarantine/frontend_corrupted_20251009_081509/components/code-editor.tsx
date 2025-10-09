/**
 * Code Editor Component
 * Provides seamless edit & fix workflow with Ctrl+L integration
 */

'use client'

import { useState, useRef, useEffect, useCallback } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { 
  Code, 
  Wand2, 
  Check, 
  X, 
  Undo, 
  Redo, 
  Copy, 
  Download,
  Eye,
  EyeOff,
  Loader2,
  AlertCircle,
  CheckCircle
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { apiService } from '@/lib/api'

interface CodeChange {
  id: string
  originalCode: string
  modifiedCode: string
  description: string
  timestamp: Date
  status: 'pending' | 'applied' | 'rejected'
}

interface CodeEditorProps {
  initialCode?: string
  language?: string
  onCodeChange?: (newCode: string) => void
  onSave?: (code: string) => void
  readOnly?: boolean
}

export function CodeEditor({ 
  initialCode = '', 
  language = 'javascript',
  onCodeChange,
  onSave,
  readOnly = false 
}: CodeEditorProps) {
  const [code, setCode] = useState(initialCode)
  const [selectedText, setSelectedText] = useState('')
  const [selectionStart, setSelectionStart] = useState(0)
  const [selectionEnd, setSelectionEnd] = useState(0)
  const [isProcessing, setIsProcessing] = useState(false)
  const [changes, setChanges] = useState<CodeChange[]>([])
  const [showDiff, setShowDiff] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const historyRef = useRef<string[]>([])
  const historyIndexRef = useRef(-1)

  // Initialize history
  useEffect(() => {
    if (initialCode) {
      historyRef.current = [initialCode]
      historyIndexRef.current = 0
    }
  }, [initialCode])

  // Handle keyboard shortcuts
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.ctrlKey && e.key === 'l') {
      e.preventDefault()
      handleEditRequest()
    }
    if (e.ctrlKey && e.key === 'z') {
      e.preventDefault()
      handleUndo()
    }
    if (e.ctrlKey && e.key === 'y') {
      e.preventDefault()
      handleRedo()
    }
  }, [])

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [handleKeyDown])

  // Handle text selection
  const handleSelection = useCallback(() => {
    if (!textareaRef.current) return
    
    const start = textareaRef.current.selectionStart
    const end = textareaRef.current.selectionEnd
    const selected = code.substring(start, end)
    
    setSelectionStart(start)
    setSelectionEnd(end)
    setSelectedText(selected)
  }, [code])

  // Process edit request
  const handleEditRequest = async () => {
    if (!selectedText.trim()) {
      setError('Please select some code to edit')
      return
    }

    setIsProcessing(true)
    setError(null)
    setSuccess(null)

    try {
      const response = await apiService.processCodeChange({
        code: selectedText,
        language,
        context: code,
        description: 'User requested edit via Ctrl+L'
      })

      if (response.success && response.data) {
        const change: CodeChange = {
          id: Date.now().toString(),
          originalCode: selectedText,
          modifiedCode: response.data.modifiedCode,
          description: response.data.description,
          timestamp: new Date(),
          status: 'pending'
        }

        setChanges(prev => [change, ...prev])
        setShowDiff(true)
        setSuccess('Code modification ready! Review and apply if satisfied.')
      } else {
        throw new Error(response.error || 'Failed to process code change')
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to process code change')
    } finally {
      setIsProcessing(false)
    }
  }

  // Apply code change
  const applyChange = (changeId: string) => {
    const change = changes.find(c => c.id === changeId)
    if (!change) return

    const newCode = code.replace(change.originalCode, change.modifiedCode)
    
    // Add to history
    historyRef.current = historyRef.current.slice(0, historyIndexRef.current + 1)
    historyRef.current.push(newCode)
    historyIndexRef.current = historyRef.current.length - 1

    setCode(newCode)
    setChanges(prev => prev.map(c => 
      c.id === changeId ? { ...c, status: 'applied' } : c
    ))
    setShowDiff(false)
    setSuccess('Code change applied successfully!')
    onCodeChange?.(newCode)
  }

  // Reject code change
  const rejectChange = (changeId: string) => {
    setChanges(prev => prev.map(c => 
      c.id === changeId ? { ...c, status: 'rejected' } : c
    ))
    setShowDiff(false)
  }

  // Undo functionality
  const handleUndo = () => {
    if (historyIndexRef.current > 0) {
      historyIndexRef.current--
      const previousCode = historyRef.current[historyIndexRef.current]
      setCode(previousCode)
      onCodeChange?.(previousCode)
    }
  }

  // Redo functionality
  const handleRedo = () => {
    if (historyIndexRef.current < historyRef.current.length - 1) {
      historyIndexRef.current++
      const nextCode = historyRef.current[historyIndexRef.current]
      setCode(nextCode)
      onCodeChange?.(nextCode)
    }
  }

  // Copy code
  const handleCopy = () => {
    navigator.clipboard.writeText(code)
    setSuccess('Code copied to clipboard!')
  }

  // Download code
  const handleDownload = () => {
    const blob = new Blob([code], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `code.${language}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    setSuccess('Code downloaded!')
  }

  // Save code
  const handleSave = () => {
    onSave?.(code)
    setSuccess('Code saved!')
  }

  const canUndo = historyIndexRef.current > 0
  const canRedo = historyIndexRef.current < historyRef.current.length - 1
  const hasChanges = changes.some(c => c.status === 'pending')

  return (
    <div className="space-y-4">
      {/* Header */}
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center space-x-2">
              <Code className="h-5 w-5" />
              <span>Code Editor</span>
              <Badge variant="outline">{language}</Badge>
            </CardTitle>
            
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowDiff(!showDiff)}
                disabled={!hasChanges}
              >
                {showDiff ? <EyeOff className="h-4 w-4 mr-1" /> : <Eye className="h-4 w-4 mr-1" />}
                {showDiff ? 'Hide' : 'Show'} Diff
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          {/* Status Messages */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center space-x-2"
              >
                <AlertCircle className="h-4 w-4 text-red-600" />
                <span className="text-red-600 dark:text-red-400">{error}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setError(null)}
                  className="text-red-600 hover:text-red-700"
                >
                  <X className="h-4 w-4" />
                </Button>
              </motion.div>
            )}
            
            {success && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="mb-4 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg flex items-center space-x-2"
              >
                <CheckCircle className="h-4 w-4 text-green-600" />
                <span className="text-green-600 dark:text-green-400">{success}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSuccess(null)}
                  className="text-green-600 hover:text-green-700"
                >
                  <X className="h-4 w-4" />
                </Button>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Instructions */}
          <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <p className="text-sm text-blue-800 dark:text-blue-200">
              <strong>Quick Edit:</strong> Select any code and press <kbd className="px-2 py-1 bg-blue-100 dark:bg-blue-800 rounded text-xs">Ctrl+L</kbd> to describe changes
            </p>
          </div>

          {/* Code Editor */}
          <div className="relative">
            <Textarea
              ref={textareaRef}
              value={code}
              onChange={(e) => {
                setCode(e.target.value)
                onCodeChange?.(e.target.value)
              }}
              onSelect={handleSelection}
              placeholder="Enter your code here..."
              className="min-h-[400px] font-mono text-sm"
              readOnly={readOnly}
            />
            
            {/* Selection Info */}
            {selectedText && (
              <div className="absolute top-2 right-2 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded text-xs">
                {selectedText.length} characters selected
              </div>
            )}
          </div>

          {/* Toolbar */}
          <div className="flex items-center justify-between mt-4">
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleUndo}
                disabled={!canUndo}
              >
                <Undo className="h-4 w-4 mr-1" />
                Undo
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={handleRedo}
                disabled={!canRedo}
              >
                <Redo className="h-4 w-4 mr-1" />
                Redo
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={handleCopy}
              >
                <Copy className="h-4 w-4 mr-1" />
                Copy
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={handleDownload}
              >
                <Download className="h-4 w-4 mr-1" />
                Download
              </Button>
            </div>

            <div className="flex items-center space-x-2">
              {!readOnly && (
                <Button onClick={handleSave}>
                  Save Changes
                </Button>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Code Changes */}
      <AnimatePresence>
        {changes.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="space-y-4"
          >
            {changes.map((change) => (
              <Card key={change.id} className="border-l-4 border-l-blue-500">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-sm">{change.description}</CardTitle>
                      <p className="text-xs text-gray-500">
                        {change.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                    <Badge 
                      variant={change.status === 'applied' ? 'default' : 
                              change.status === 'rejected' ? 'destructive' : 'secondary'}
                    >
                      {change.status}
                    </Badge>
                  </div>
                </CardHeader>
                
                {showDiff && change.status === 'pending' && (
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="text-sm font-medium text-red-600 mb-2">Original</h4>
                        <pre className="bg-red-50 dark:bg-red-900/20 p-3 rounded text-xs overflow-x-auto">
                          {change.originalCode}
                        </pre>
                      </div>
                      <div>
                        <h4 className="text-sm font-medium text-green-600 mb-2">Modified</h4>
                        <pre className="bg-green-50 dark:bg-green-900/20 p-3 rounded text-xs overflow-x-auto">
                          {change.modifiedCode}
                        </pre>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 mt-4">
                      <Button
                        size="sm"
                        onClick={() => applyChange(change.id)}
                        className="bg-green-600 hover:bg-green-700"
                      >
                        <Check className="h-4 w-4 mr-1" />
                        Apply
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => rejectChange(change.id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <X className="h-4 w-4 mr-1" />
                        Reject
                      </Button>
                    </div>
                  </CardContent>
                )}
              </Card>
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Processing Indicator */}
      <AnimatePresence>
        {isProcessing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex items-center justify-center py-8"
          >
            <div className="flex items-center space-x-2">
              <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
              <span className="text-gray-600 dark:text-gray-400">
                Processing code change...
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
