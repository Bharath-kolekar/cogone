'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, Database, Globe, BookOpen } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface CodeContext {
  framework: string
  language: string
  styling: string
  database: string
  deployment: string
  testing: string
  architecture: string
}

interface GeneratedCode {
  id: string
  type: 'component' | 'function' | 'class' | 'interface' | 'config' | 'test'
  content: string
  description: string
  dependencies: string[]
  imports: string[]
  exports: string[]
  context: CodeContext
  confidence: number
  suggestions: string[]
}

interface ContextualCodeGeneratorProps {
  onCodeGenerated?: (code: GeneratedCode) => void
  showRealTimeGeneration?: boolean
  enableContextualAnalysis?: boolean
  className?: string
}

const FRAMEWORK_PRESETS = {
  'nextjs': {
    framework: 'Next.js',
    language: 'TypeScript',
    styling: 'Tailwind CSS',
    database: 'Supabase',
    deployment: 'Vercel',
    testing: 'Jest',
    architecture: 'App Router'
  },
  'react': {
    framework: 'React',
    language: 'TypeScript',
    styling: 'Tailwind CSS',
    database: 'Firebase',
    deployment: 'Netlify',
    testing: 'Jest',
    architecture: 'Component-based'
  },
  'vue': {
    framework: 'Vue.js',
    language: 'TypeScript',
    styling: 'Tailwind CSS',
    database: 'MongoDB',
    deployment: 'Vercel',
    testing: 'Vitest',
    architecture: 'Composition API'
  },
  'angular': {
    framework: 'Angular',
    language: 'TypeScript',
    styling: 'Angular Material',
    database: 'PostgreSQL',
    deployment: 'AWS',
    testing: 'Jasmine',
    architecture: 'Modular'
  }
}

const SAMPLE_REQUESTS = [
  {
    id: 'loading-state',
    request: 'Add a state for loading and error handling',
    context: 'react',
    expectedOutput: 'React hooks for loading and error states'
  },
  {
    id: 'api-endpoint',
    request: 'Create an API endpoint for user authentication',
    context: 'nextjs',
    expectedOutput: 'Next.js API route with authentication'
  },
  {
    id: 'database-model',
    request: 'Create a database model for products',
    context: 'nextjs',
    expectedOutput: 'Database model with Prisma/Supabase'
  },
  {
    id: 'form-validation',
    request: 'Add form validation with error messages',
    context: 'react',
    expectedOutput: 'Form validation with React Hook Form'
  },
  {
    id: 'responsive-component',
    request: 'Create a responsive card component',
    context: 'nextjs',
    expectedOutput: 'Responsive component with Tailwind CSS'
  }
]

export function ContextualCodeGenerator({
  onCodeGenerated,
  showRealTimeGeneration = true,
  enableContextualAnalysis = true,
  className = ''
}: ContextualCodeGeneratorProps) {
  const [userRequest, setUserRequest] = useState('')
  const [generatedCode, setGeneratedCode] = useState<GeneratedCode[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStep, setGenerationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('generator')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedCode, setSelectedCode] = useState<string | null>(null)
  const [context, setContext] = useState<CodeContext>(FRAMEWORK_PRESETS.nextjs)
  const [selectedFramework, setSelectedFramework] = useState('nextjs')
  const [customContext, setCustomContext] = useState('')
  const [codeSuggestions, setCodeSuggestions] = useState<string[]>([])

  useEffect(() => {
    if (selectedFramework && FRAMEWORK_PRESETS[selectedFramework as keyof typeof FRAMEWORK_PRESETS]) {
      setContext(FRAMEWORK_PRESETS[selectedFramework as keyof typeof FRAMEWORK_PRESETS])
    }
  }, [selectedFramework])

  const generateCode = async (request: string) => {
    if (!request.trim()) return

    setIsGenerating(true)
    setProgress(0)
    setGenerationStep('Analyzing request...')

    try {
      // Simulate code generation steps
      const steps = [
        'Analyzing user request...',
        'Identifying code context...',
        'Generating base code structure...',
        'Adding framework-specific patterns...',
        'Implementing best practices...',
        'Adding error handling...',
        'Generating documentation...',
        'Validating code syntax...',
        'Finalizing generated code...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setGenerationStep(steps[i])
        setProgress((i + 1) * 11.1)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Generate mock code based on request and context
      const mockCode = generateMockCode(request, context)
      setGeneratedCode(prev => [...prev, mockCode])
      onCodeGenerated?.(mockCode)

    } catch (error) {
      console.error('Code generation failed:', error)
    } finally {
      setIsGenerating(false)
      setProgress(100)
      setGenerationStep('Code generation complete!')
    }
  }

  const generateMockCode = (request: string, context: CodeContext): GeneratedCode => {
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('loading') && lowerRequest.includes('error')) {
      return {
        id: `code-${Date.now()}`,
        type: 'component',
        content: `import React, { useState, useEffect } from 'react';

interface LoadingErrorStateProps {
  isLoading: boolean;
  error: string | null;
  children: React.ReactNode;
}

export function LoadingErrorState({ isLoading, error, children }: LoadingErrorStateProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2 text-gray-600">Loading...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center">
          <div className="text-red-600 mr-2">⚠️</div>
          <div>
            <h3 className="text-red-800 font-medium">Error</h3>
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}`,
        description: 'Loading and error state management component',
        dependencies: ['react'],
        imports: ['React', 'useState', 'useEffect'],
        exports: ['LoadingErrorState'],
        context,
        confidence: 0.95,
        suggestions: [
          'Add retry functionality',
          'Implement custom loading animations',
          'Add error boundary for better error handling'
        ]
      }
    } else if (lowerRequest.includes('api') && lowerRequest.includes('authentication')) {
      return {
        id: `code-${Date.now()}`,
        type: 'function',
        content: `import { NextApiRequest, NextApiResponse } from 'next';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Find user in database
    const user = await findUserByEmail(email);
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate JWT token
    const token = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET!,
      { expiresIn: '24h' }
    );

    res.status(200).json({
      success: true,
      token,
      user: {
        id: user.id,
        email: user.email,
        name: user.name
      }
    });
  } catch (error) {
    console.error('Authentication error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}`,
        description: 'User authentication API endpoint',
        dependencies: ['next', 'jsonwebtoken', 'bcryptjs'],
        imports: ['NextApiRequest', 'NextApiResponse', 'jwt', 'bcrypt'],
        exports: ['handler'],
        context,
        confidence: 0.9,
        suggestions: [
          'Add rate limiting',
          'Implement refresh tokens',
          'Add input validation middleware'
        ]
      }
    } else if (lowerRequest.includes('database') && lowerRequest.includes('model')) {
      return {
        id: `code-${Date.now()}`,
        type: 'interface',
        content: `import { Model, DataTypes } from 'sequelize';
import { sequelize } from '../config/database';

export interface ProductAttributes {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  stock: number;
  imageUrl?: string;
  createdAt: Date;
  updatedAt: Date;
}

export class Product extends Model<ProductAttributes> implements ProductAttributes {
  public id!: number;
  public name!: string;
  public description!: string;
  public price!: number;
  public category!: string;
  public stock!: number;
  public imageUrl?: string;
  public readonly createdAt!: Date;
  public readonly updatedAt!: Date;

  static associate(models: any) {
    // Define associations here
  }
}

Product.init({
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
    validate: {
      notEmpty: true,
      len: [1, 255]
    }
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: false,
  },
  price: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false,
    validate: {
      min: 0
    }
  },
  category: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  stock: {
    type: DataTypes.INTEGER,
    allowNull: false,
    defaultValue: 0,
    validate: {
      min: 0
    }
  },
  imageUrl: {
    type: DataTypes.STRING,
    allowNull: true,
    validate: {
      isUrl: true
    }
  }
}, {
  sequelize,
  modelName: 'Product',
  tableName: 'products',
  timestamps: true,
});`,
        description: 'Product database model with validation',
        dependencies: ['sequelize'],
        imports: ['Model', 'DataTypes', 'sequelize'],
        exports: ['Product', 'ProductAttributes'],
        context,
        confidence: 0.85,
        suggestions: [
          'Add database indexes',
          'Implement soft deletes',
          'Add audit trail functionality'
        ]
      }
    } else {
      return {
        id: `code-${Date.now()}`,
        type: 'component',
        content: `// Generated code for: ${request}
// Framework: ${context.framework}
// Language: ${context.language}

export function GeneratedComponent() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Generated Component</h1>
      <p className="text-gray-600">This component was generated based on your request.</p>
    </div>
  );
}`,
        description: `Generated code for: ${request}`,
        dependencies: [context.framework.toLowerCase()],
        imports: [],
        exports: ['GeneratedComponent'],
        context,
        confidence: 0.7,
        suggestions: [
          'Customize the component structure',
          'Add proper TypeScript types',
          'Implement responsive design'
        ]
      }
    }
  }

  const runSampleRequest = (request: string) => {
    setUserRequest(request)
    generateCode(request)
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'component': return 'text-blue-600 bg-blue-100'
      case 'function': return 'text-green-600 bg-green-100'
      case 'class': return 'text-purple-600 bg-purple-100'
      case 'interface': return 'text-orange-600 bg-orange-100'
      case 'config': return 'text-gray-600 bg-gray-100'
      case 'test': return 'text-pink-600 bg-pink-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getFrameworkIcon = (framework: string) => {
    const icons = {
      'Next.js': Globe,
      'React': Code,
      'Vue.js': Globe,
      'Angular': Code
    }
    return icons[framework as keyof typeof icons] || Code
  }

  const renderGeneratedCode = (code: GeneratedCode) => {
    const isSelected = selectedCode === code.id
    const Icon = getFrameworkIcon(code.context.framework)

    return (
      <motion.div
        key={code.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        }`}
        onClick={() => setSelectedCode(selectedCode === code.id ? null : selectedCode)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Icon className="h-4 w-4" />
            <span className="font-medium">{code.description}</span>
            <Badge className={getTypeColor(code.type)}>
              {code.type.toUpperCase()}
            </Badge>
            <Badge className={getConfidenceColor(code.confidence)}>
              {(code.confidence * 100).toFixed(0)}%
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                navigator.clipboard.writeText(code.content)
              }}
            >
              <Copy className="h-4 w-4 mr-1" />
              Copy
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                // Download code as file
                const blob = new Blob([code.content], { type: 'text/plain' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `${code.type}.${code.context.language.toLowerCase()}`
                a.click()
                URL.revokeObjectURL(url)
              }}
            >
              <Download className="h-4 w-4 mr-1" />
              Download
            </Button>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          Framework: {code.context.framework} | Language: {code.context.language} | Styling: {code.context.styling}
        </div>

        {code.dependencies.length > 0 && (
          <div className="text-xs text-gray-500 mb-2">
            Dependencies: {code.dependencies.join(', ')}
          </div>
        )}

        {isSelected && (
          <div className="mt-3 space-y-3">
            <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm overflow-x-auto">
              <pre>{code.content}</pre>
            </div>
            
            {code.suggestions.length > 0 && (
              <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded">
                <div className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">
                  Suggestions:
                </div>
                <ul className="text-xs text-blue-600 dark:text-blue-400 space-y-1">
                  {code.suggestions.map((suggestion, index) => (
                    <li key={index}>• {suggestion}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </motion.div>
    )
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-6 w-6 text-purple-600" />
                <span>Contextual Code Generator</span>
              </CardTitle>
              <CardDescription>
                Generate code that perfectly matches your tech stack and requirements
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
          {/* Generation Status */}
          {isGenerating && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-600"></div>
                <span className="text-sm font-medium text-purple-800 dark:text-purple-200">
                  {generationStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Code Generator */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="generator">Code Generator</TabsTrigger>
          <TabsTrigger value="context">Context</TabsTrigger>
          <TabsTrigger value="generated">Generated ({generatedCode.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="generator" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Code className="h-4 w-4" />
                  <span>Code Request</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="user-request">Describe what you want to generate</Label>
                    <Textarea
                      id="user-request"
                      value={userRequest}
                      onChange={(e) => setUserRequest(e.target.value)}
                      placeholder="e.g., Add a state for loading and error handling"
                      className="min-h-[100px]"
                    />
                  </div>
                  <Button
                    onClick={() => generateCode(userRequest)}
                    disabled={isGenerating || !userRequest.trim()}
                    className="w-full"
                  >
                    <Zap className="h-4 w-4 mr-2" />
                    {isGenerating ? 'Generating...' : 'Generate Code'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Sample Requests</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {SAMPLE_REQUESTS.map((sample) => (
                    <div
                      key={sample.id}
                      className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                      onClick={() => runSampleRequest(sample.request)}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <code className="text-sm font-mono">{sample.request}</code>
                          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                            {sample.expectedOutput}
                          </p>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation()
                            runSampleRequest(sample.request)
                          }}
                          disabled={isGenerating}
                        >
                          <Play className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="context" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Settings className="h-4 w-4" />
                  <span>Framework Presets</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {Object.entries(FRAMEWORK_PRESETS).map(([key, preset]) => (
                    <div
                      key={key}
                      className={`p-3 border rounded-lg cursor-pointer transition-all ${
                        selectedFramework === key ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                      }`}
                      onClick={() => setSelectedFramework(key)}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="font-medium">{preset.framework}</h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {preset.language} • {preset.styling} • {preset.database}
                          </p>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation()
                            setSelectedFramework(key)
                          }}
                        >
                          Select
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
                  <Brain className="h-4 w-4" />
                  <span>Current Context</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Framework</span>
                    <Badge variant="outline">{context.framework}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Language</span>
                    <Badge variant="outline">{context.language}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Styling</span>
                    <Badge variant="outline">{context.styling}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Database</span>
                    <Badge variant="outline">{context.database}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Deployment</span>
                    <Badge variant="outline">{context.deployment}</Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Testing</span>
                    <Badge variant="outline">{context.testing}</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="generated" className="space-y-4">
          {generatedCode.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <Code className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                  No Code Generated Yet
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Describe what you want to generate to see contextual code here.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Badge variant="outline">
                    Total Generated: {generatedCode.length}
                  </Badge>
                  <Badge variant="outline" className="text-green-600">
                    Success Rate: 95%
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
                {generatedCode.map(renderGeneratedCode)}
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
