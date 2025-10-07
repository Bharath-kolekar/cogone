'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { RefreshCw, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, MessageSquare, Lightbulb, Wand2, FileText, GitBranch, Layers } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface RefactoringRequest {
  id: string
  originalCode: string
  refactoredCode: string
  improvements: RefactoringImprovement[]
  type: 'performance' | 'readability' | 'maintainability' | 'structure' | 'types'
  complexity: 'simple' | 'medium' | 'complex'
  confidence: number
  description: string
  timestamp: Date
}

interface RefactoringImprovement {
  id: string
  type: 'custom-hooks' | 'typescript' | 'performance' | 'structure' | 'readability'
  title: string
  description: string
  code: string
  explanation: string
  impact: 'low' | 'medium' | 'high'
  confidence: number
}

interface RefactoringAIProps {
  onCodeRefactored?: (result: RefactoringRequest) => void
  showRealTimeRefactoring?: boolean
  enableAutoOptimization?: boolean
  className?: string
}

const SAMPLE_REFACTORING_REQUESTS = [
  {
    id: 'custom-hooks',
    request: 'Refactor this to use custom hooks and improve performance',
    type: 'performance',
    complexity: 'medium',
    description: 'Extract logic to custom hooks and optimize performance'
  },
  {
    id: 'typescript',
    request: 'Add proper TypeScript types and interfaces',
    type: 'types',
    complexity: 'simple',
    description: 'Add TypeScript types for better type safety'
  },
  {
    id: 'structure',
    request: 'Improve code structure and organization',
    type: 'structure',
    complexity: 'medium',
    description: 'Reorganize code for better maintainability'
  },
  {
    id: 'readability',
    request: 'Make this code more readable and clean',
    type: 'readability',
    complexity: 'simple',
    description: 'Improve code readability and documentation'
  }
]

const REFACTORING_PATTERNS = {
  'custom-hooks': {
    pattern: /useState|useEffect|useCallback|useMemo/,
    improvements: [
      {
        type: 'custom-hooks',
        title: 'Extract Custom Hook',
        description: 'Extract component logic into reusable custom hook',
        impact: 'high'
      },
      {
        type: 'performance',
        title: 'Add useMemo/useCallback',
        description: 'Optimize re-renders with memoization',
        impact: 'medium'
      }
    ]
  },
  'typescript': {
    pattern: /any|unknown|object/,
    improvements: [
      {
        type: 'typescript',
        title: 'Add TypeScript Types',
        description: 'Replace any types with proper TypeScript interfaces',
        impact: 'high'
      },
      {
        type: 'typescript',
        title: 'Add Generic Types',
        description: 'Add generic types for better type safety',
        impact: 'medium'
      }
    ]
  },
  'performance': {
    pattern: /\.map\(|\.filter\(|\.reduce\(/,
    improvements: [
      {
        type: 'performance',
        title: 'Optimize Array Operations',
        description: 'Optimize array operations for better performance',
        impact: 'medium'
      },
      {
        type: 'performance',
        title: 'Add Memoization',
        description: 'Add useMemo/useCallback for expensive operations',
        impact: 'high'
      }
    ]
  }
}

export function RefactoringAI({
  onCodeRefactored,
  showRealTimeRefactoring = true,
  enableAutoOptimization = true,
  className = ''
}: RefactoringAIProps) {
  const [originalCode, setOriginalCode] = useState('')
  const [refactoringRequests, setRefactoringRequests] = useState<RefactoringRequest[]>([])
  const [isRefactoring, setIsRefactoring] = useState(false)
  const [refactoringStep, setRefactoringStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('refactor')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedRequest, setSelectedRequest] = useState<string | null>(null)
  const [refactoringType, setRefactoringType] = useState<string>('')
  const [detectedPatterns, setDetectedPatterns] = useState<string[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  useEffect(() => {
    if (originalCode && enableAutoOptimization) {
      analyzeCode(originalCode)
    }
  }, [originalCode, enableAutoOptimization])

  const analyzeCode = async (code: string) => {
    setIsAnalyzing(true)
    
    try {
      // Simulate code analysis
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const patterns = []
      for (const [patternType, patternData] of Object.entries(REFACTORING_PATTERNS)) {
        if (patternData.pattern.test(code)) {
          patterns.push(patternType)
        }
      }
      
      setDetectedPatterns(patterns)
      
    } catch (error) {
      console.error('Code analysis failed:', error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const refactorCode = async (code: string, request: string) => {
    if (!code.trim()) return

    setIsRefactoring(true)
    setProgress(0)
    setRefactoringStep('Analyzing code structure...')

    try {
      // Simulate refactoring steps
      const steps = [
        'Analyzing code structure...',
        'Identifying improvement opportunities...',
        'Detecting performance issues...',
        'Extracting custom hooks...',
        'Adding TypeScript types...',
        'Optimizing performance...',
        'Improving readability...',
        'Generating refactored code...',
        'Validating improvements...',
        'Finalizing refactored code...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setRefactoringStep(steps[i])
        setProgress((i + 1) * 10)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Generate mock refactored code
      const refactoredCode = generateRefactoredCode(code, request)
      const improvements = generateImprovements(code, request)
      
      const refactoringRequest: RefactoringRequest = {
        id: `refactor-${Date.now()}`,
        originalCode: code,
        refactoredCode,
        improvements,
        type: determineRefactoringType(request),
        complexity: determineComplexity(code),
        confidence: 0.85 + Math.random() * 0.15,
        description: request,
        timestamp: new Date()
      }

      setRefactoringRequests(prev => [...prev, refactoringRequest])
      onCodeRefactored?.(refactoringRequest)

    } catch (error) {
      console.error('Refactoring failed:', error)
    } finally {
      setIsRefactoring(false)
      setProgress(100)
      setRefactoringStep('Refactoring complete!')
    }
  }

  const generateRefactoredCode = (code: string, request: string): string => {
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('custom hooks') || lowerRequest.includes('performance')) {
      return `// Refactored with custom hooks and performance optimizations
import React, { useState, useEffect, useCallback, useMemo } from 'react';

// Custom hook for data fetching
function useDataFetching(url: string) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(url);
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// Custom hook for form handling
function useForm(initialValues: Record<string, any>) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});

  const handleChange = useCallback((name: string, value: any) => {
    setValues(prev => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  }, [errors]);

  const handleSubmit = useCallback((onSubmit: (values: any) => void) => {
    return (e: React.FormEvent) => {
      e.preventDefault();
      onSubmit(values);
    };
  }, []);

  return { values, errors, handleChange, handleSubmit };
}

// Main component with optimized performance
interface ComponentProps {
  userId: string;
  onUserUpdate: (user: any) => void;
}

export function OptimizedComponent({ userId, onUserUpdate }: ComponentProps) {
  const { data: user, loading, error, refetch } = useDataFetching(\`/api/users/\${userId}\`);
  const { values, handleChange, handleSubmit } = useForm({
    name: '',
    email: '',
    bio: ''
  });

  // Memoized expensive calculations
  const userStats = useMemo(() => {
    if (!user) return null;
    return {
      totalPosts: user.posts?.length || 0,
      joinDate: new Date(user.createdAt).toLocaleDateString(),
      isActive: user.lastLogin > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    };
  }, [user]);

  // Memoized event handlers
  const handleUserUpdate = useCallback((updatedUser: any) => {
    onUserUpdate(updatedUser);
    refetch();
  }, [onUserUpdate, refetch]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="user-profile">
      <h1>{user?.name}</h1>
      {userStats && (
        <div className="stats">
          <p>Posts: {userStats.totalPosts}</p>
          <p>Joined: {userStats.joinDate}</p>
          <p>Status: {userStats.isActive ? 'Active' : 'Inactive'}</p>
        </div>
      )}
      {/* Rest of component */}
    </div>
  );
}`
    } else if (lowerRequest.includes('typescript') || lowerRequest.includes('types')) {
      return `// Refactored with proper TypeScript types
import React, { useState, useEffect, useCallback } from 'react';

// Type definitions
interface User {
  id: string;
  name: string;
  email: string;
  bio?: string;
  createdAt: string;
  lastLogin: string;
  posts: Post[];
}

interface Post {
  id: string;
  title: string;
  content: string;
  publishedAt: string;
  authorId: string;
}

interface UserStats {
  totalPosts: number;
  joinDate: string;
  isActive: boolean;
}

interface ComponentProps {
  userId: string;
  onUserUpdate: (user: User) => void;
  className?: string;
}

interface FormValues {
  name: string;
  email: string;
  bio: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  bio?: string;
}

// Custom hook with proper types
function useUserData(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchUser = useCallback(async (): Promise<void> => {
    setLoading(true);
    try {
      const response = await fetch(\`/api/users/\${userId}\`);
      if (!response.ok) {
        throw new Error(\`Failed to fetch user: \${response.statusText}\`);
      }
      const userData: User = await response.json();
      setUser(userData);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  return { user, loading, error, refetch: fetchUser };
}

// Main component with full TypeScript support
export function TypedComponent({ userId, onUserUpdate, className }: ComponentProps) {
  const { user, loading, error, refetch } = useUserData(userId);
  const [formValues, setFormValues] = useState<FormValues>({
    name: '',
    email: '',
    bio: ''
  });
  const [errors, setErrors] = useState<FormErrors>({});

  const handleInputChange = useCallback((field: keyof FormValues, value: string): void => {
    setFormValues(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  }, [errors]);

  const handleSubmit = useCallback((e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    // Validation logic here
    onUserUpdate(user!);
  }, [onUserUpdate, user]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div className={className}>
      <h1>{user.name}</h1>
      <form onSubmit={handleSubmit}>
        <input
          value={formValues.name}
          onChange={(e) => handleInputChange('name', e.target.value)}
          placeholder="Name"
        />
        <input
          value={formValues.email}
          onChange={(e) => handleInputChange('email', e.target.value)}
          placeholder="Email"
          type="email"
        />
        <textarea
          value={formValues.bio}
          onChange={(e) => handleInputChange('bio', e.target.value)}
          placeholder="Bio"
        />
        <button type="submit">Update User</button>
      </form>
    </div>
  );
}`
    } else {
      return `// Refactored for better structure and readability
import React, { useState, useEffect, useCallback } from 'react';

/**
 * User profile component with improved structure
 * @param userId - The ID of the user to display
 * @param onUserUpdate - Callback when user is updated
 */
interface ComponentProps {
  userId: string;
  onUserUpdate: (user: any) => void;
}

/**
 * Custom hook for managing user data
 */
function useUserProfile(userId: string) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchUser = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(\`/api/users/\${userId}\`);
      const userData = await response.json();
      setUser(userData);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  return { user, loading, error, refetch: fetchUser };
}

/**
 * Main component with improved structure
 */
export function RefactoredComponent({ userId, onUserUpdate }: ComponentProps) {
  const { user, loading, error, refetch } = useUserProfile(userId);

  // Handle loading state
  if (loading) {
    return <div className="loading">Loading user data...</div>;
  }

  // Handle error state
  if (error) {
    return (
      <div className="error">
        <p>Failed to load user data</p>
        <button onClick={refetch}>Retry</button>
      </div>
    );
  }

  // Handle empty state
  if (!user) {
    return <div className="empty">No user data available</div>;
  }

  return (
    <div className="user-profile">
      <header className="profile-header">
        <h1>{user.name}</h1>
        <p className="email">{user.email}</p>
      </header>
      
      <main className="profile-content">
        <section className="user-info">
          <h2>User Information</h2>
          <p>{user.bio || 'No bio available'}</p>
        </section>
        
        <section className="user-actions">
          <button onClick={() => onUserUpdate(user)}>
            Update Profile
          </button>
        </section>
      </main>
    </div>
  );
}`
    }
  }

  const generateImprovements = (code: string, request: string): RefactoringImprovement[] => {
    const improvements: RefactoringImprovement[] = []
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('custom hooks') || lowerRequest.includes('performance')) {
      improvements.push({
        id: 'custom-hooks',
        type: 'custom-hooks',
        title: 'Extract Custom Hooks',
        description: 'Extract component logic into reusable custom hooks',
        code: '// Custom hook example\nfunction useDataFetching(url) {\n  // Hook logic here\n}',
        explanation: 'Custom hooks improve reusability and separate concerns',
        impact: 'high',
        confidence: 0.95
      })
      
      improvements.push({
        id: 'performance',
        type: 'performance',
        title: 'Add Performance Optimizations',
        description: 'Add useMemo and useCallback for better performance',
        code: 'const memoizedValue = useMemo(() => {\n  return expensiveCalculation(data);\n}, [data]);',
        explanation: 'Memoization prevents unnecessary re-calculations',
        impact: 'high',
        confidence: 0.90
      })
    }
    
    if (lowerRequest.includes('typescript') || lowerRequest.includes('types')) {
      improvements.push({
        id: 'typescript',
        type: 'typescript',
        title: 'Add TypeScript Types',
        description: 'Replace any types with proper TypeScript interfaces',
        code: 'interface User {\n  id: string;\n  name: string;\n  email: string;\n}',
        explanation: 'TypeScript types provide better type safety and IDE support',
        impact: 'high',
        confidence: 0.95
      })
    }
    
    improvements.push({
      id: 'readability',
      type: 'readability',
      title: 'Improve Code Readability',
      description: 'Add comments and improve code structure',
      code: '/**\n * Component description\n * @param props - Component props\n */',
      explanation: 'Better documentation and structure improve maintainability',
      impact: 'medium',
      confidence: 0.85
    })
    
    return improvements
  }

  const determineRefactoringType = (request: string): 'performance' | 'readability' | 'maintainability' | 'structure' | 'types' => {
    const lowerRequest = request.toLowerCase()
    
    if (lowerRequest.includes('performance') || lowerRequest.includes('optimize')) {
      return 'performance'
    } else if (lowerRequest.includes('typescript') || lowerRequest.includes('types')) {
      return 'types'
    } else if (lowerRequest.includes('structure') || lowerRequest.includes('organize')) {
      return 'structure'
    } else if (lowerRequest.includes('readable') || lowerRequest.includes('clean')) {
      return 'readability'
    } else {
      return 'maintainability'
    }
  }

  const determineComplexity = (code: string): 'simple' | 'medium' | 'complex' => {
    const lines = code.split('\n').length
    const functions = (code.match(/function|const.*=|=>/g) || []).length
    
    if (lines > 100 || functions > 10) return 'complex'
    if (lines > 50 || functions > 5) return 'medium'
    return 'simple'
  }

  const runSampleRequest = (request: string) => {
    setOriginalCode(`// Sample messy code
import React, { useState, useEffect } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    setLoading(true);
    fetch(\`/api/users/\${userId}\`)
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setFormData(data);
      })
      .catch(err => setError(err))
      .finally(() => setLoading(false));
  }, [userId]);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(\`/api/users/\${userId}\`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
    .then(res => res.json())
    .then(data => setUser(data));
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1>{user?.name}</h1>
      <form onSubmit={handleSubmit}>
        <input name="name" value={formData.name} onChange={handleChange} />
        <input name="email" value={formData.email} onChange={handleChange} />
        <button type="submit">Update</button>
      </form>
    </div>
  );
}`)
    refactorCode(originalCode, request)
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'performance': return 'text-green-600 bg-green-100'
      case 'readability': return 'text-blue-600 bg-blue-100'
      case 'maintainability': return 'text-purple-600 bg-purple-100'
      case 'structure': return 'text-orange-600 bg-orange-100'
      case 'types': return 'text-indigo-600 bg-indigo-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'simple': return 'text-green-600 bg-green-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'complex': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600 bg-green-100'
    if (confidence > 0.6) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const renderRefactoringRequest = (request: RefactoringRequest) => {
    const isSelected = selectedRequest === request.id

    return (
      <motion.div
        key={request.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        }`}
        onClick={() => setSelectedRequest(selectedRequest === request.id ? null : selectedRequest)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <RefreshCw className="h-4 w-4" />
            <span className="font-medium">{request.description}</span>
            <Badge className={getTypeColor(request.type)}>
              {request.type.toUpperCase()}
            </Badge>
            <Badge className={getComplexityColor(request.complexity)}>
              {request.complexity.toUpperCase()}
            </Badge>
            <Badge className={getConfidenceColor(request.confidence)}>
              {(request.confidence * 100).toFixed(0)}%
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                navigator.clipboard.writeText(request.refactoredCode)
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
                const blob = new Blob([request.refactoredCode], { type: 'text/plain' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = 'refactored-code.tsx'
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
          {request.timestamp.toLocaleString()}
        </div>

        {isSelected && (
          <div className="mt-4 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="text-sm font-medium mb-2">Original Code:</h4>
                <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm overflow-x-auto max-h-40">
                  <pre>{request.originalCode}</pre>
                </div>
              </div>
              
              <div>
                <h4 className="text-sm font-medium mb-2">Refactored Code:</h4>
                <div className="bg-gray-900 text-gray-100 p-3 rounded font-mono text-sm overflow-x-auto max-h-40">
                  <pre>{request.refactoredCode}</pre>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="text-sm font-medium mb-2">Improvements:</h4>
              <div className="space-y-2">
                {request.improvements.map((improvement) => (
                  <div key={improvement.id} className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded">
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-sm">{improvement.title}</span>
                      <Badge className={getImpactColor(improvement.impact)}>
                        {improvement.impact.toUpperCase()}
                      </Badge>
                    </div>
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                      {improvement.description}
                    </p>
                    <div className="bg-gray-900 text-gray-100 p-2 rounded font-mono text-xs overflow-x-auto">
                      <pre>{improvement.code}</pre>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {improvement.explanation}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </motion.div>
    )
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-orange-50 to-red-50 dark:from-orange-900/20 dark:to-red-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <RefreshCw className="h-6 w-6 text-orange-600" />
                <span>Refactoring AI</span>
              </CardTitle>
              <CardDescription>
                Select messy code + Ctrl+L to refactor and improve performance
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
          {/* Refactoring Status */}
          {isRefactoring && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-orange-600"></div>
                <span className="text-sm font-medium text-orange-800 dark:text-orange-200">
                  {refactoringStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}

          {/* Analysis Status */}
          {isAnalyzing && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <Code className="h-5 w-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-800 dark:text-blue-200">
                  Analyzing code patterns...
                </span>
              </div>
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Refactoring AI */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="refactor">Refactor</TabsTrigger>
          <TabsTrigger value="samples">Samples</TabsTrigger>
          <TabsTrigger value="patterns">Patterns</TabsTrigger>
          <TabsTrigger value="history">History ({refactoringRequests.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="refactor" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Code className="h-4 w-4" />
                  <span>Code Refactoring</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="original-code">Paste your code to refactor</Label>
                    <Textarea
                      id="original-code"
                      value={originalCode}
                      onChange={(e) => setOriginalCode(e.target.value)}
                      placeholder="Paste your code here..."
                      className="min-h-[200px] font-mono text-sm"
                    />
                  </div>
                  <div>
                    <Label htmlFor="refactor-request">Refactoring request</Label>
                    <Input
                      id="refactor-request"
                      value={refactoringType}
                      onChange={(e) => setRefactoringType(e.target.value)}
                      placeholder="e.g., Refactor this to use custom hooks and improve performance"
                    />
                  </div>
                  <Button
                    onClick={() => refactorCode(originalCode, refactoringType)}
                    disabled={isRefactoring || !originalCode.trim()}
                    className="w-full"
                  >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    {isRefactoring ? 'Refactoring...' : 'Refactor Code'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Detected Patterns</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {detectedPatterns.length > 0 ? (
                    detectedPatterns.map((pattern, index) => (
                      <div key={index} className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-sm">
                        {pattern}
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-4 text-gray-500">
                      No patterns detected yet
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="samples" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Target className="h-4 w-4" />
                <span>Sample Refactoring Requests</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {SAMPLE_REFACTORING_REQUESTS.map((sample) => (
                  <div
                    key={sample.id}
                    className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                    onClick={() => runSampleRequest(sample.request)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium text-sm">{sample.request}</div>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          {sample.description}
                        </p>
                        <div className="flex items-center space-x-2 mt-2">
                          <Badge className={getTypeColor(sample.type)}>
                            {sample.type}
                          </Badge>
                          <Badge className={getComplexityColor(sample.complexity)}>
                            {sample.complexity}
                          </Badge>
                        </div>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          runSampleRequest(sample.request)
                        }}
                        disabled={isRefactoring}
                      >
                        <Play className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="patterns" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Layers className="h-4 w-4" />
                <span>Refactoring Patterns</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(REFACTORING_PATTERNS).map(([patternType, patternData]) => (
                  <div key={patternType} className="p-3 border rounded-lg">
                    <div className="font-medium text-sm mb-2">{patternType}</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                      Pattern: {patternData.pattern.toString()}
                    </div>
                    <div className="space-y-1">
                      {patternData.improvements.map((improvement, index) => (
                        <div key={index} className="text-xs">
                          • {improvement.title}: {improvement.description}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="history" className="space-y-4">
          {refactoringRequests.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <RefreshCw className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                  No Refactoring History
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Start refactoring code to see your history here.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Badge variant="outline">
                    Total Refactored: {refactoringRequests.length}
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
                {refactoringRequests.map(renderRefactoringRequest)}
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
