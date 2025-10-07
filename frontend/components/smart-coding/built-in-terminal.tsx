'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Terminal, Play, Pause, RotateCcw, Settings, Zap, Target, TrendingUp, Code, Bug, CheckCircle, XCircle, AlertTriangle, Info, Copy, Download } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface TerminalCommand {
  id: string
  command: string
  output: string
  status: 'success' | 'error' | 'warning' | 'info'
  timestamp: Date
  duration?: number
}

interface DebugSession {
  id: string
  name: string
  status: 'running' | 'paused' | 'stopped' | 'error'
  breakpoints: string[]
  variables: { [key: string]: any }
  callStack: string[]
  currentLine: number
}

interface BuiltInTerminalProps {
  onCommandExecuted?: (command: TerminalCommand) => void
  onDebugSessionStarted?: (session: DebugSession) => void
  showRealTimeOutput?: boolean
  enableDebugging?: boolean
  className?: string
}

const SAMPLE_COMMANDS = [
  {
    id: 'npm-install',
    command: 'npm install',
    description: 'Install project dependencies',
    category: 'package-management'
  },
  {
    id: 'npm-test',
    command: 'npm test',
    description: 'Run test suite',
    category: 'testing'
  },
  {
    id: 'npm-run-dev',
    command: 'npm run dev',
    description: 'Start development server',
    category: 'development'
  },
  {
    id: 'git-status',
    command: 'git status',
    description: 'Check git repository status',
    category: 'version-control'
  },
  {
    id: 'git-add',
    command: 'git add .',
    description: 'Stage all changes',
    category: 'version-control'
  },
  {
    id: 'git-commit',
    command: 'git commit -m "Initial commit"',
    description: 'Commit changes with message',
    category: 'version-control'
  },
  {
    id: 'python-check',
    command: 'python --version',
    description: 'Check Python version',
    category: 'environment'
  },
  {
    id: 'node-check',
    command: 'node --version',
    description: 'Check Node.js version',
    category: 'environment'
  }
]

const ERROR_PATTERNS = [
  {
    pattern: /ModuleNotFoundError: No module named '(.+)'/,
    solution: 'Install the missing module: pip install $1',
    category: 'python-import'
  },
  {
    pattern: /ImportError: cannot import name '(.+)' from '(.+)'/,
    solution: 'Check if the import is correct or if the module is installed',
    category: 'python-import'
  },
  {
    pattern: /SyntaxError: invalid syntax/,
    solution: 'Check for syntax errors in your Python code',
    category: 'python-syntax'
  },
  {
    pattern: /TypeError: '(.+)' object is not callable/,
    solution: 'Check if you are calling a function correctly',
    category: 'python-type'
  },
  {
    pattern: /npm ERR! (.+)/,
    solution: 'Check npm configuration and try npm install --force',
    category: 'npm-error'
  },
  {
    pattern: /EADDRINUSE: address already in use/,
    solution: 'Port is already in use. Try a different port or kill the process',
    category: 'port-conflict'
  }
]

export function BuiltInTerminal({
  onCommandExecuted,
  onDebugSessionStarted,
  showRealTimeOutput = true,
  enableDebugging = true,
  className = ''
}: BuiltInTerminalProps) {
  const [commandHistory, setCommandHistory] = useState<TerminalCommand[]>([])
  const [currentCommand, setCurrentCommand] = useState('')
  const [isExecuting, setIsExecuting] = useState(false)
  const [executionStep, setExecutionStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('terminal')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [debugSession, setDebugSession] = useState<DebugSession | null>(null)
  const [terminalOutput, setTerminalOutput] = useState('')
  const [commandSuggestions, setCommandSuggestions] = useState<string[]>([])
  const [errorAnalysis, setErrorAnalysis] = useState<any>(null)
  const terminalRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight
    }
  }, [commandHistory, terminalOutput])

  const executeCommand = async (command: string) => {
    if (!command.trim()) return

    setIsExecuting(true)
    setProgress(0)
    setExecutionStep('Executing command...')

    try {
      // Simulate command execution
      const steps = [
        'Parsing command...',
        'Validating syntax...',
        'Executing command...',
        'Processing output...',
        'Analyzing results...',
        'Generating response...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setExecutionStep(steps[i])
        setProgress((i + 1) * 16.7)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Generate mock output based on command
      const mockOutput = generateMockOutput(command)
      const status = mockOutput.includes('error') || mockOutput.includes('Error') ? 'error' : 'success'
      
      const commandResult: TerminalCommand = {
        id: `cmd-${Date.now()}`,
        command,
        output: mockOutput,
        status: status as any,
        timestamp: new Date(),
        duration: Math.random() * 2000 + 500
      }

      setCommandHistory(prev => [...prev, commandResult])
      setTerminalOutput(prev => prev + `$ ${command}\n${mockOutput}\n\n`)
      onCommandExecuted?.(commandResult)

      // Analyze for errors and provide solutions
      analyzeErrors(mockOutput)

    } catch (error) {
      console.error('Command execution failed:', error)
    } finally {
      setIsExecuting(false)
      setProgress(100)
      setExecutionStep('Command execution complete!')
    }
  }

  const generateMockOutput = (command: string): string => {
    const lowerCommand = command.toLowerCase()
    
    if (lowerCommand.includes('npm install')) {
      return `npm install
added 1234 packages in 45s
found 0 vulnerabilities`
    } else if (lowerCommand.includes('npm test')) {
      return `npm test
> test@1.0.0 test
> jest

PASS src/components/Button.test.tsx
PASS src/components/Input.test.tsx
PASS src/utils/helpers.test.ts

Test Suites: 3 passed, 3 total
Tests: 15 passed, 15 total
Time: 2.345s`
    } else if (lowerCommand.includes('npm run dev')) {
      return `npm run dev
> test@1.0.0 dev
> next dev

ready - started server on 0.0.0.0:3000, url: http://localhost:3000
info - Loaded env from .env.local`
    } else if (lowerCommand.includes('git status')) {
      return `git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   src/components/Button.tsx
        modified:   src/components/Input.tsx

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/components/NewComponent.tsx`
    } else if (lowerCommand.includes('python --version')) {
      return `python --version
Python 3.9.7`
    } else if (lowerCommand.includes('node --version')) {
      return `node --version
v18.17.0`
    } else if (lowerCommand.includes('python') && lowerCommand.includes('import')) {
      return `python script.py
Traceback (most recent call last):
  File "script.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'`
    } else {
      return `$ ${command}
Command executed successfully`
    }
  }

  const analyzeErrors = (output: string) => {
    for (const errorPattern of ERROR_PATTERNS) {
      const match = output.match(errorPattern.pattern)
      if (match) {
        setErrorAnalysis({
          pattern: errorPattern.pattern,
          solution: errorPattern.solution,
          category: errorPattern.category,
          match: match[1] || match[0]
        })
        return
      }
    }
    setErrorAnalysis(null)
  }

  const startDebugSession = async () => {
    const session: DebugSession = {
      id: `debug-${Date.now()}`,
      name: 'Debug Session',
      status: 'running',
      breakpoints: [],
      variables: {},
      callStack: ['main()'],
      currentLine: 1
    }

    setDebugSession(session)
    onDebugSessionStarted?.(session)
  }

  const stopDebugSession = () => {
    setDebugSession(null)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'text-green-600 bg-green-100'
      case 'error': return 'text-red-600 bg-red-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'info': return 'text-blue-600 bg-blue-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return CheckCircle
      case 'error': return XCircle
      case 'warning': return AlertTriangle
      case 'info': return Info
      default: return Terminal
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      executeCommand(currentCommand)
      setCurrentCommand('')
    } else if (e.key === 'ArrowUp') {
      // Navigate command history
      const lastCommand = commandHistory[commandHistory.length - 1]
      if (lastCommand) {
        setCurrentCommand(lastCommand.command)
      }
    }
  }

  const runSampleCommand = (command: string) => {
    setCurrentCommand(command)
    executeCommand(command)
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-900/20 dark:to-blue-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Terminal className="h-6 w-6 text-gray-600" />
                <span>Built-in Terminal & Debugging</span>
              </CardTitle>
              <CardDescription>
                Execute commands, debug code, and analyze errors with intelligent assistance
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={startDebugSession}
                disabled={debugSession !== null}
              >
                <Bug className="h-4 w-4 mr-1" />
                Start Debug
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={stopDebugSession}
                disabled={debugSession === null}
              >
                <Pause className="h-4 w-4 mr-1" />
                Stop Debug
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Execution Status */}
          {isExecuting && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-gray-50 dark:bg-gray-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-600"></div>
                <span className="text-sm font-medium text-gray-800 dark:text-gray-200">
                  {executionStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Terminal and Debugging */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="terminal">Terminal</TabsTrigger>
          <TabsTrigger value="commands">Commands</TabsTrigger>
          <TabsTrigger value="debugging">Debugging</TabsTrigger>
          <TabsTrigger value="analysis">Analysis</TabsTrigger>
        </TabsList>

        <TabsContent value="terminal" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Terminal className="h-4 w-4" />
                <span>Terminal Output</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div 
                ref={terminalRef}
                className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm h-96 overflow-y-auto"
              >
                <pre className="whitespace-pre-wrap">{terminalOutput || 'Welcome to the built-in terminal!\nType a command and press Enter to execute it.\n\n'}</pre>
              </div>
              <div className="flex items-center space-x-2 mt-4">
                <Input
                  ref={inputRef}
                  value={currentCommand}
                  onChange={(e) => setCurrentCommand(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Enter command..."
                  className="flex-1"
                  disabled={isExecuting}
                />
                <Button
                  onClick={() => executeCommand(currentCommand)}
                  disabled={isExecuting || !currentCommand.trim()}
                >
                  <Play className="h-4 w-4 mr-1" />
                  Execute
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="commands" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Code className="h-4 w-4" />
                  <span>Sample Commands</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {SAMPLE_COMMANDS.map((cmd) => (
                    <div
                      key={cmd.id}
                      className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                      onClick={() => runSampleCommand(cmd.command)}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <code className="text-sm font-mono">{cmd.command}</code>
                          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                            {cmd.description}
                          </p>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation()
                            runSampleCommand(cmd.command)
                          }}
                          disabled={isExecuting}
                        >
                          <Play className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Command History</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {commandHistory.slice(-10).map((cmd) => {
                    const Icon = getStatusIcon(cmd.status)
                    return (
                      <div
                        key={cmd.id}
                        className="p-2 border rounded text-sm"
                      >
                        <div className="flex items-center space-x-2 mb-1">
                          <Icon className="h-4 w-4" />
                          <code className="font-mono">{cmd.command}</code>
                          <Badge className={getStatusColor(cmd.status)}>
                            {cmd.status}
                          </Badge>
                        </div>
                        <div className="text-xs text-gray-500">
                          {cmd.timestamp.toLocaleTimeString()}
                          {cmd.duration && ` (${cmd.duration.toFixed(0)}ms)`}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="debugging" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Bug className="h-4 w-4" />
                  <span>Debug Session</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {debugSession ? (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">Session: {debugSession.name}</span>
                      <Badge className={getStatusColor(debugSession.status)}>
                        {debugSession.status}
                      </Badge>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="text-sm">
                        <strong>Current Line:</strong> {debugSession.currentLine}
                      </div>
                      <div className="text-sm">
                        <strong>Call Stack:</strong>
                        <div className="ml-2 text-xs text-gray-600 dark:text-gray-400">
                          {debugSession.callStack.join(' → ')}
                        </div>
                      </div>
                      <div className="text-sm">
                        <strong>Breakpoints:</strong> {debugSession.breakpoints.length}
                      </div>
                    </div>

                    <div className="flex space-x-2">
                      <Button size="sm" variant="outline">
                        <Pause className="h-4 w-4 mr-1" />
                        Pause
                      </Button>
                      <Button size="sm" variant="outline">
                        <Play className="h-4 w-4 mr-1" />
                        Continue
                      </Button>
                      <Button size="sm" variant="outline">
                        <Target className="h-4 w-4 mr-1" />
                        Step
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Bug className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                      No Debug Session
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">
                      Start a debug session to begin debugging your code.
                    </p>
                    <Button onClick={startDebugSession}>
                      <Bug className="h-4 w-4 mr-2" />
                      Start Debug Session
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Settings className="h-4 w-4" />
                  <span>Debug Configuration</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="debug-file">Debug File</Label>
                    <Input
                      id="debug-file"
                      placeholder="Enter file path to debug"
                      className="mt-1"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="debug-args">Debug Arguments</Label>
                    <Input
                      id="debug-args"
                      placeholder="Enter debug arguments"
                      className="mt-1"
                    />
                  </div>

                  <div className="flex space-x-2">
                    <Button size="sm" className="flex-1">
                      <Play className="h-4 w-4 mr-1" />
                      Start Debug
                    </Button>
                    <Button size="sm" variant="outline" className="flex-1">
                      <Settings className="h-4 w-4 mr-1" />
                      Configure
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="analysis" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Error Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {errorAnalysis ? (
                  <div className="space-y-3">
                    <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                      <div className="text-sm font-medium text-red-800 dark:text-red-200">
                        Error Detected
                      </div>
                      <div className="text-xs text-red-600 dark:text-red-400 mt-1">
                        {errorAnalysis.match}
                      </div>
                    </div>
                    
                    <div className="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                      <div className="text-sm font-medium text-green-800 dark:text-green-200">
                        Suggested Solution
                      </div>
                      <div className="text-xs text-green-600 dark:text-green-400 mt-1">
                        {errorAnalysis.solution}
                      </div>
                    </div>

                    <Button size="sm" className="w-full">
                      <Zap className="h-4 w-4 mr-1" />
                      Apply Fix
                    </Button>
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                      No Errors Detected
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400">
                      Run commands to see error analysis and solutions.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Performance Analysis</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Average Execution Time</span>
                    <span className="font-medium">1.2s</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Success Rate</span>
                    <span className="font-medium text-green-600">95%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Error Rate</span>
                    <span className="font-medium text-red-600">5%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Total Commands</span>
                    <span className="font-medium">{commandHistory.length}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
