'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, Files, Terminal, GitBranch } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { DiffBasedEditor } from './diff-based-editor'
import { MultiFileCoordinator } from './multi-file-coordinator'
import { BuiltInTerminal } from './built-in-terminal'
import { ContextualCodeGenerator } from './contextual-code-generator'

interface SmartCodingDashboardProps {
  onCodeGenerated?: (result: any) => void
  showAllFeatures?: boolean
  enableRealTimeGeneration?: boolean
  className?: string
}

export function SmartCodingDashboard({
  onCodeGenerated,
  showAllFeatures = true,
  enableRealTimeGeneration = true,
  className = ''
}: SmartCodingDashboardProps) {
  const [activeTab, setActiveTab] = useState('overview')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStep, setGenerationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [generatedCode, setGeneratedCode] = useState<any[]>([])
  const [fileChanges, setFileChanges] = useState<any[]>([])
  const [terminalCommands, setTerminalCommands] = useState<any[]>([])
  const [debugSession, setDebugSession] = useState<any>(null)

  const handleCodeGenerated = (code: any) => {
    setGeneratedCode(prev => [...prev, code])
    onCodeGenerated?.(code)
  }

  const handleFileChanges = (changes: any[]) => {
    setFileChanges(prev => [...prev, ...changes])
  }

  const handleTerminalCommand = (command: any) => {
    setTerminalCommands(prev => [...prev, command])
  }

  const handleDebugSession = (session: any) => {
    setDebugSession(session)
  }

  const getOverallStats = () => {
    return {
      totalCodeGenerated: generatedCode.length,
      totalFileChanges: fileChanges.length,
      totalCommands: terminalCommands.length,
      debugSessions: debugSession ? 1 : 0,
      successRate: 95,
      averageGenerationTime: 2.3
    }
  }

  const stats = getOverallStats()

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 dark:from-blue-900/20 dark:via-purple-900/20 dark:to-pink-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-blue-600" />
                <span>Smart Coding AI Dashboard</span>
              </CardTitle>
              <CardDescription>
                Advanced AI-powered coding assistant with contextual understanding
              </CardDescription>
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
        </CardHeader>
        <CardContent>
          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{stats.totalCodeGenerated}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Code Generated</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{stats.totalFileChanges}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">File Changes</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{stats.totalCommands}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Commands</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">{stats.successRate}%</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Success Rate</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Dashboard */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="diff-editor">Diff Editor</TabsTrigger>
          <TabsTrigger value="multi-file">Multi-File</TabsTrigger>
          <TabsTrigger value="terminal">Terminal</TabsTrigger>
          <TabsTrigger value="generator">Generator</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Code className="h-4 w-4" />
                  <span>Recent Code Generation</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {generatedCode.slice(-3).map((code, index) => (
                    <div key={index} className="p-3 border rounded-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-sm">{code.description}</div>
                          <div className="text-xs text-gray-500">
                            {code.context?.framework} • {code.type}
                          </div>
                        </div>
                        <Badge variant="outline">
                          {(code.confidence * 100).toFixed(0)}%
                        </Badge>
                      </div>
                    </div>
                  ))}
                  {generatedCode.length === 0 && (
                    <div className="text-center py-4 text-gray-500">
                      No code generated yet
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Files className="h-4 w-4" />
                  <span>Recent File Changes</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {fileChanges.slice(-3).map((change, index) => (
                    <div key={index} className="p-3 border rounded-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-sm">{change.filePath}</div>
                          <div className="text-xs text-gray-500">
                            {change.type} • {change.impact}
                          </div>
                        </div>
                        <Badge variant="outline">
                          {change.type.toUpperCase()}
                        </Badge>
                      </div>
                    </div>
                  ))}
                  {fileChanges.length === 0 && (
                    <div className="text-center py-4 text-gray-500">
                      No file changes yet
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Terminal className="h-4 w-4" />
                  <span>Terminal Activity</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {terminalCommands.slice(-3).map((cmd, index) => (
                    <div key={index} className="p-3 border rounded-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <code className="text-sm font-mono">{cmd.command}</code>
                          <div className="text-xs text-gray-500">
                            {cmd.timestamp.toLocaleTimeString()} • {cmd.status}
                          </div>
                        </div>
                        <Badge variant="outline">
                          {cmd.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                  {terminalCommands.length === 0 && (
                    <div className="text-center py-4 text-gray-500">
                      No commands executed yet
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Debug Session</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {debugSession ? (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Session: {debugSession.name}</span>
                      <Badge variant="outline">
                        {debugSession.status}
                      </Badge>
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Current Line: {debugSession.currentLine}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      Breakpoints: {debugSession.breakpoints.length}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-4 text-gray-500">
                    No debug session active
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="diff-editor">
          <DiffBasedEditor
            onChangesAccepted={handleFileChanges}
            onChangesRejected={(changes) => console.log('Changes rejected:', changes)}
            showPreview={true}
            enableRealTimeDiff={enableRealTimeGeneration}
          />
        </TabsContent>

        <TabsContent value="multi-file">
          <MultiFileCoordinator
            onChangesAccepted={handleFileChanges}
            onChangesRejected={(changes) => console.log('Changes rejected:', changes)}
            showPreview={true}
            enableRealTimeCoordination={enableRealTimeGeneration}
          />
        </TabsContent>

        <TabsContent value="terminal">
          <BuiltInTerminal
            onCommandExecuted={handleTerminalCommand}
            onDebugSessionStarted={handleDebugSession}
            showRealTimeOutput={true}
            enableDebugging={true}
          />
        </TabsContent>

        <TabsContent value="generator">
          <ContextualCodeGenerator
            onCodeGenerated={handleCodeGenerated}
            showRealTimeGeneration={enableRealTimeGeneration}
            enableContextualAnalysis={true}
          />
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Performance Metrics</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Success Rate</span>
                    <span className="font-medium text-green-600">{stats.successRate}%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Avg Generation Time</span>
                    <span className="font-medium">{stats.averageGenerationTime}s</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Total Operations</span>
                    <span className="font-medium">
                      {stats.totalCodeGenerated + stats.totalFileChanges + stats.totalCommands}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Code className="h-4 w-4" />
                  <span>Code Quality</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Code Coverage</span>
                    <span className="font-medium text-blue-600">87%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Type Safety</span>
                    <span className="font-medium text-green-600">95%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Best Practices</span>
                    <span className="font-medium text-purple-600">92%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>AI Intelligence</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Context Understanding</span>
                    <span className="font-medium text-green-600">94%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Code Accuracy</span>
                    <span className="font-medium text-blue-600">91%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Suggestion Quality</span>
                    <span className="font-medium text-purple-600">88%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Brain className="h-4 w-4" />
                <span>AI Learning Progress</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <div className="text-sm font-medium mb-2">Framework Knowledge</div>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Next.js</span>
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div className="bg-blue-500 h-2 rounded-full" style={{ width: '95%' }}></div>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">React</span>
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div className="bg-green-500 h-2 rounded-full" style={{ width: '92%' }}></div>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Vue.js</span>
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div className="bg-purple-500 h-2 rounded-full" style={{ width: '88%' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div>
                    <div className="text-sm font-medium mb-2">Language Proficiency</div>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm">TypeScript</span>
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div className="bg-blue-500 h-2 rounded-full" style={{ width: '96%' }}></div>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">JavaScript</span>
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '94%' }}></div>
                        </div>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Python</span>
                        <div className="w-32 bg-gray-200 rounded-full h-2">
                          <div className="bg-green-500 h-2 rounded-full" style={{ width: '89%' }}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
