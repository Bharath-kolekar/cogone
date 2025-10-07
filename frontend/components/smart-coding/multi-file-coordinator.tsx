'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Files, GitBranch, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, Play, Pause, RotateCcw, Settings, Zap, Target, TrendingUp, Database, Code, Globe, BookOpen } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'

interface FileChange {
  id: string
  filePath: string
  type: 'create' | 'modify' | 'delete'
  content: string
  description: string
  dependencies: string[]
  impact: 'low' | 'medium' | 'high'
  category: 'database' | 'api' | 'frontend' | 'documentation' | 'config' | 'test'
}

interface MultiFileCoordinatorProps {
  onChangesAccepted?: (changes: FileChange[]) => void
  onChangesRejected?: (changes: FileChange[]) => void
  showPreview?: boolean
  enableRealTimeCoordination?: boolean
  className?: string
}

const SAMPLE_FEATURES = [
  {
    id: 'user-auth',
    name: 'User Authentication System',
    description: 'Complete authentication system with login, register, and password reset',
    files: [
      {
        id: 'auth-model',
        filePath: 'models/User.ts',
        type: 'create' as const,
        content: `import { Model, DataTypes } from 'sequelize';
import { sequelize } from '../config/database';

export class User extends Model {
  public id!: number;
  public email!: string;
  public password!: string;
  public name!: string;
  public createdAt!: Date;
  public updatedAt!: Date;
}

User.init({
  id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true,
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
}, {
  sequelize,
  modelName: 'User',
  tableName: 'users',
});`,
        description: 'User model with authentication fields',
        dependencies: [],
        impact: 'high' as const,
        category: 'database' as const
      },
      {
        id: 'auth-api',
        filePath: 'routes/auth.ts',
        type: 'create' as const,
        content: `import express from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { User } from '../models/User';

const router = express.Router();

// Register endpoint
router.post('/register', async (req, res) => {
  try {
    const { email, password, name } = req.body;
    
    // Check if user exists
    const existingUser = await User.findOne({ where: { email } });
    if (existingUser) {
      return res.status(400).json({ error: 'User already exists' });
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Create user
    const user = await User.create({
      email,
      password: hashedPassword,
      name,
    });
    
    // Generate JWT token
    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET!);
    
    res.status(201).json({ user, token });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Login endpoint
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    // Find user
    const user = await User.findOne({ where: { email } });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Check password
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Generate JWT token
    const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET!);
    
    res.json({ user, token });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;`,
        description: 'Authentication API endpoints',
        dependencies: ['auth-model'],
        impact: 'high' as const,
        category: 'api' as const
      },
      {
        id: 'auth-component',
        filePath: 'components/AuthForm.tsx',
        type: 'create' as const,
        content: `import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface AuthFormProps {
  mode: 'login' | 'register';
  onSubmit: (data: { email: string; password: string; name?: string }) => void;
}

export function AuthForm({ mode, onSubmit }: AuthFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await onSubmit({ email, password, name: mode === 'register' ? name : undefined });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {mode === 'register' && (
        <div>
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
      )}
      
      <div>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      
      <div>
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      
      <Button type="submit" disabled={loading} className="w-full">
        {loading ? 'Processing...' : mode === 'login' ? 'Login' : 'Register'}
      </Button>
    </form>
  );
}`,
        description: 'Authentication form component',
        dependencies: ['auth-api'],
        impact: 'medium' as const,
        category: 'frontend' as const
      },
      {
        id: 'auth-docs',
        filePath: 'docs/authentication.md',
        type: 'create' as const,
        content: `# Authentication System

## Overview
This document describes the authentication system implementation.

## API Endpoints

### Register
- **POST** /api/auth/register
- **Body**: { email, password, name }
- **Response**: { user, token }

### Login
- **POST** /api/auth/login
- **Body**: { email, password }
- **Response**: { user, token }

## Frontend Components

### AuthForm
A reusable form component for both login and registration.

## Database Schema

### User Model
- id: number (primary key)
- email: string (unique)
- password: string (hashed)
- name: string
- createdAt: Date
- updatedAt: Date

## Security Features
- Password hashing with bcrypt
- JWT token authentication
- Input validation
- Error handling`,
        description: 'Authentication system documentation',
        dependencies: ['auth-model', 'auth-api', 'auth-component'],
        impact: 'low' as const,
        category: 'documentation' as const
      }
    ]
  },
  {
    id: 'ecommerce',
    name: 'E-commerce Product System',
    description: 'Complete product management system with CRUD operations',
    files: [
      {
        id: 'product-model',
        filePath: 'models/Product.ts',
        type: 'create' as const,
        content: `import { Model, DataTypes } from 'sequelize';
import { sequelize } from '../config/database';

export class Product extends Model {
  public id!: number;
  public name!: string;
  public description!: string;
  public price!: number;
  public category!: string;
  public stock!: number;
  public imageUrl!: string;
  public createdAt!: Date;
  public updatedAt!: Date;
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
  },
  description: {
    type: DataTypes.TEXT,
    allowNull: false,
  },
  price: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false,
  },
  category: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  stock: {
    type: DataTypes.INTEGER,
    allowNull: false,
    defaultValue: 0,
  },
  imageUrl: {
    type: DataTypes.STRING,
    allowNull: true,
  },
}, {
  sequelize,
  modelName: 'Product',
  tableName: 'products',
});`,
        description: 'Product model with e-commerce fields',
        dependencies: [],
        impact: 'high' as const,
        category: 'database' as const
      }
    ]
  }
]

export function MultiFileCoordinator({
  onChangesAccepted,
  onChangesRejected,
  showPreview = true,
  enableRealTimeCoordination = true,
  className = ''
}: MultiFileCoordinatorProps) {
  const [selectedFeature, setSelectedFeature] = useState<string | null>(null)
  const [fileChanges, setFileChanges] = useState<FileChange[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStep, setGenerationStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('features')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [acceptedChanges, setAcceptedChanges] = useState<Set<string>>(new Set())
  const [rejectedChanges, setRejectedChanges] = useState<Set<string>>(new Set())
  const [selectedFile, setSelectedFile] = useState<string | null>(null)
  const [customFeature, setCustomFeature] = useState('')

  const generateFeatureFiles = async (featureId: string) => {
    setIsGenerating(true)
    setProgress(0)
    setGenerationStep('Analyzing feature requirements...')

    try {
      const feature = SAMPLE_FEATURES.find(f => f.id === featureId)
      if (!feature) return

      // Simulate file generation steps
      const steps = [
        'Analyzing feature requirements...',
        'Generating database models...',
        'Creating API endpoints...',
        'Building frontend components...',
        'Writing documentation...',
        'Validating dependencies...',
        'Finalizing file structure...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setGenerationStep(steps[i])
        setProgress((i + 1) * 14.3)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      setFileChanges(feature.files)
      setSelectedFeature(featureId)

    } catch (error) {
      console.error('Feature generation failed:', error)
    } finally {
      setIsGenerating(false)
      setProgress(100)
      setGenerationStep('Feature generation complete!')
    }
  }

  const generateCustomFeature = async () => {
    if (!customFeature.trim()) return

    setIsGenerating(true)
    setProgress(0)
    setGenerationStep('Analyzing custom feature requirements...')

    try {
      // Simulate custom feature generation
      const steps = [
        'Analyzing custom feature requirements...',
        'Identifying required components...',
        'Generating database schema...',
        'Creating API structure...',
        'Building frontend components...',
        'Writing documentation...',
        'Validating implementation...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setGenerationStep(steps[i])
        setProgress((i + 1) * 14.3)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Generate mock files based on custom feature
      const mockFiles: FileChange[] = [
        {
          id: 'custom-1',
          filePath: 'models/CustomModel.ts',
          type: 'create',
          content: `// Generated model for: ${customFeature}`,
          description: `Model for ${customFeature}`,
          dependencies: [],
          impact: 'high',
          category: 'database'
        },
        {
          id: 'custom-2',
          filePath: 'routes/custom.ts',
          type: 'create',
          content: `// Generated API for: ${customFeature}`,
          description: `API endpoints for ${customFeature}`,
          dependencies: ['custom-1'],
          impact: 'high',
          category: 'api'
        },
        {
          id: 'custom-3',
          filePath: 'components/CustomComponent.tsx',
          type: 'create',
          content: `// Generated component for: ${customFeature}`,
          description: `Frontend component for ${customFeature}`,
          dependencies: ['custom-2'],
          impact: 'medium',
          category: 'frontend'
        }
      ]

      setFileChanges(mockFiles)
      setSelectedFeature('custom')

    } catch (error) {
      console.error('Custom feature generation failed:', error)
    } finally {
      setIsGenerating(false)
      setProgress(100)
      setGenerationStep('Custom feature generation complete!')
    }
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
    const allChangeIds = fileChanges.map(change => change.id)
    setAcceptedChanges(new Set(allChangeIds))
    setRejectedChanges(new Set())
    onChangesAccepted?.(fileChanges)
  }

  const rejectAllChanges = () => {
    const allChangeIds = fileChanges.map(change => change.id)
    setRejectedChanges(new Set(allChangeIds))
    setAcceptedChanges(new Set())
    onChangesRejected?.(fileChanges)
  }

  const getChangeTypeColor = (type: string) => {
    switch (type) {
      case 'create': return 'text-green-600 bg-green-100'
      case 'modify': return 'text-blue-600 bg-blue-100'
      case 'delete': return 'text-red-600 bg-red-100'
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

  const getCategoryIcon = (category: string) => {
    const icons = {
      'database': Database,
      'api': Globe,
      'frontend': Code,
      'documentation': BookOpen,
      'config': Settings,
      'test': Target
    }
    return icons[category as keyof typeof icons] || Files
  }

  const getCategoryColor = (category: string) => {
    const colors = {
      'database': 'text-blue-600 bg-blue-100',
      'api': 'text-green-600 bg-green-100',
      'frontend': 'text-purple-600 bg-purple-100',
      'documentation': 'text-orange-600 bg-orange-100',
      'config': 'text-gray-600 bg-gray-100',
      'test': 'text-pink-600 bg-pink-100'
    }
    return colors[category as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const renderFileChange = (change: FileChange) => {
    const isAccepted = acceptedChanges.has(change.id)
    const isRejected = rejectedChanges.has(change.id)
    const isSelected = selectedFile === change.id
    const Icon = getCategoryIcon(change.category)

    return (
      <motion.div
        key={change.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        } ${isAccepted ? 'bg-green-50 dark:bg-green-900/20' : ''} ${isRejected ? 'bg-red-50 dark:bg-red-900/20' : ''}`}
        onClick={() => setSelectedFile(selectedFile === change.id ? null : change.id)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Icon className="h-4 w-4" />
            <span className="font-medium">{change.filePath}</span>
            <Badge className={getChangeTypeColor(change.type)}>
              {change.type.toUpperCase()}
            </Badge>
            <Badge className={getCategoryColor(change.category)}>
              {change.category.toUpperCase()}
            </Badge>
            <Badge className={getImpactColor(change.impact)}>
              {change.impact.toUpperCase()}
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
          {change.description}
        </div>

        {change.dependencies.length > 0 && (
          <div className="text-xs text-gray-500 mb-2">
            Dependencies: {change.dependencies.join(', ')}
          </div>
        )}

        {isSelected && (
          <div className="mt-3 p-3 bg-gray-900 text-gray-100 rounded font-mono text-sm overflow-x-auto">
            <pre>{change.content}</pre>
          </div>
        )}
      </motion.div>
    )
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Header */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Files className="h-6 w-6 text-green-600" />
                <span>Multi-File Coordinator</span>
              </CardTitle>
              <CardDescription>
                Coordinate complex features across multiple files and components
              </CardDescription>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={acceptAllChanges}
                disabled={fileChanges.length === 0}
              >
                <CheckCircle className="h-4 w-4 mr-1" />
                Accept All
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={rejectAllChanges}
                disabled={fileChanges.length === 0}
              >
                <XCircle className="h-4 w-4 mr-1" />
                Reject All
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
              className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-green-600"></div>
                <span className="text-sm font-medium text-green-800 dark:text-green-200">
                  {generationStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Feature Selection and File Changes */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="features">Features</TabsTrigger>
          <TabsTrigger value="changes">File Changes ({fileChanges.length})</TabsTrigger>
          <TabsTrigger value="preview">Preview</TabsTrigger>
        </TabsList>

        <TabsContent value="features" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Target className="h-4 w-4" />
                  <span>Pre-built Features</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {SAMPLE_FEATURES.map((feature) => (
                    <div
                      key={feature.id}
                      className={`p-3 border rounded-lg cursor-pointer transition-all ${
                        selectedFeature === feature.id ? 'ring-2 ring-green-500 bg-green-50 dark:bg-green-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                      }`}
                      onClick={() => generateFeatureFiles(feature.id)}
                    >
                      <h3 className="font-medium">{feature.name}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {feature.description}
                      </p>
                      <div className="flex items-center space-x-2 mt-2">
                        <Badge variant="outline">
                          {feature.files.length} files
                        </Badge>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation()
                            generateFeatureFiles(feature.id)
                          }}
                          disabled={isGenerating}
                        >
                          <Zap className="h-4 w-4 mr-1" />
                          Generate
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
                  <Code className="h-4 w-4" />
                  <span>Custom Feature</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="custom-feature">Describe your feature</Label>
                    <Textarea
                      id="custom-feature"
                      value={customFeature}
                      onChange={(e) => setCustomFeature(e.target.value)}
                      placeholder="e.g., Add a new feature that requires: New database model, API endpoint, Frontend component, Documentation"
                      className="min-h-[100px]"
                    />
                  </div>
                  <Button
                    onClick={generateCustomFeature}
                    disabled={isGenerating || !customFeature.trim()}
                    className="w-full"
                  >
                    <Zap className="h-4 w-4 mr-2" />
                    Generate Custom Feature
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="changes" className="space-y-4">
          {fileChanges.length === 0 ? (
            <Card>
              <CardContent className="p-8 text-center">
                <Files className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
                  No File Changes Generated
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  Select a feature or describe a custom feature to generate file changes.
                </p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Badge variant="outline">
                    Total Files: {fileChanges.length}
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
                {fileChanges.map(renderFileChange)}
              </div>
            </div>
          )}
        </TabsContent>

        <TabsContent value="preview" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Eye className="h-4 w-4" />
                <span>Feature Preview</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  {selectedFeature ? `Previewing: ${selectedFeature}` : 'No feature selected'}
                </div>
                <div className="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono text-sm overflow-x-auto">
                  <pre>
                    {fileChanges.length > 0 
                      ? fileChanges.map(change => `// ${change.filePath}\n${change.content}\n`).join('\n')
                      : 'No files to preview'
                    }
                  </pre>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
