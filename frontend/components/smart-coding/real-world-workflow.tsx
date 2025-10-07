'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Workflow, Code, Zap, Target, TrendingUp, Settings, Play, Pause, RotateCcw, CheckCircle, XCircle, Eye, EyeOff, Copy, Download, MessageSquare, Lightbulb, Wand2, Database, Globe, BookOpen, FileText, Upload, Save } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'

interface FeaturePlan {
  id: string
  name: string
  description: string
  requirements: string[]
  components: FeatureComponent[]
  status: 'planning' | 'in-progress' | 'completed' | 'testing'
  progress: number
  estimatedTime: string
  complexity: 'simple' | 'medium' | 'complex'
  priority: 'low' | 'medium' | 'high'
}

interface FeatureComponent {
  id: string
  name: string
  type: 'component' | 'api' | 'database' | 'config' | 'test' | 'documentation'
  filePath: string
  content: string
  dependencies: string[]
  status: 'pending' | 'in-progress' | 'completed'
  description: string
}

interface RealWorldWorkflowProps {
  onFeaturePlanned?: (plan: FeaturePlan) => void
  onFeatureCompleted?: (plan: FeaturePlan) => void
  showRealTimePlanning?: boolean
  enableAutoGeneration?: boolean
  className?: string
}

const SAMPLE_FEATURES = [
  {
    id: 'user-profile',
    name: 'User Profile Page',
    description: 'Create a user profile page with avatar upload, bio editing, and social links',
    requirements: [
      'Avatar upload functionality',
      'Bio editing with rich text',
      'Social links management',
      'Save to database',
      'Responsive design'
    ],
    components: [
      {
        id: 'profile-component',
        name: 'Profile Component',
        type: 'component' as const,
        filePath: 'components/Profile.tsx',
        content: `import React, { useState } from 'react';
import { Upload, Save, Edit } from 'lucide-react';

interface ProfileData {
  name: string;
  bio: string;
  avatar: string;
  socialLinks: {
    twitter: string;
    linkedin: string;
    github: string;
  };
}

export function Profile() {
  const [profile, setProfile] = useState<ProfileData>({
    name: '',
    bio: '',
    avatar: '',
    socialLinks: {
      twitter: '',
      linkedin: '',
      github: ''
    }
  });
  const [isEditing, setIsEditing] = useState(false);

  const handleSave = async () => {
    // Save profile data
    console.log('Saving profile:', profile);
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">User Profile</h1>
          <Button onClick={() => setIsEditing(!isEditing)}>
            <Edit className="h-4 w-4 mr-2" />
            {isEditing ? 'Cancel' : 'Edit'}
          </Button>
        </div>
        
        <div className="space-y-6">
          <div className="flex items-center space-x-4">
            <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center">
              {profile.avatar ? (
                <img src={profile.avatar} alt="Avatar" className="w-20 h-20 rounded-full" />
              ) : (
                <Upload className="h-8 w-8 text-gray-400" />
              )}
            </div>
            <div>
              <h2 className="text-xl font-semibold">{profile.name || 'Your Name'}</h2>
              <p className="text-gray-600">{profile.bio || 'Your bio here'}</p>
            </div>
          </div>
          
          {isEditing && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Name
                </label>
                <input
                  type="text"
                  value={profile.name}
                  onChange={(e) => setProfile(prev => ({ ...prev, name: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bio
                </label>
                <textarea
                  value={profile.bio}
                  onChange={(e) => setProfile(prev => ({ ...prev, bio: e.target.value }))}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Social Links
                </label>
                <div className="space-y-2">
                  <input
                    type="text"
                    placeholder="Twitter URL"
                    value={profile.socialLinks.twitter}
                    onChange={(e) => setProfile(prev => ({
                      ...prev,
                      socialLinks: { ...prev.socialLinks, twitter: e.target.value }
                    }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    type="text"
                    placeholder="LinkedIn URL"
                    value={profile.socialLinks.linkedin}
                    onChange={(e) => setProfile(prev => ({
                      ...prev,
                      socialLinks: { ...prev.socialLinks, linkedin: e.target.value }
                    }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <input
                    type="text"
                    placeholder="GitHub URL"
                    value={profile.socialLinks.github}
                    onChange={(e) => setProfile(prev => ({
                      ...prev,
                      socialLinks: { ...prev.socialLinks, github: e.target.value }
                    }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <Button onClick={handleSave} className="w-full">
                <Save className="h-4 w-4 mr-2" />
                Save Profile
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}`,
        dependencies: [],
        status: 'pending' as const,
        description: 'Main profile component with editing capabilities'
      },
      {
        id: 'profile-api',
        name: 'Profile API',
        type: 'api' as const,
        filePath: 'pages/api/profile.ts',
        content: `import { NextApiRequest, NextApiResponse } from 'next';
import { getSession } from 'next-auth/react';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const session = await getSession({ req });
  
  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  switch (req.method) {
    case 'GET':
      try {
        // Get user profile
        const profile = await getUserProfile(session.user.id);
        res.status(200).json(profile);
      } catch (error) {
        res.status(500).json({ error: 'Failed to fetch profile' });
      }
      break;
      
    case 'PUT':
      try {
        // Update user profile
        const { name, bio, socialLinks } = req.body;
        const updatedProfile = await updateUserProfile(session.user.id, {
          name,
          bio,
          socialLinks
        });
        res.status(200).json(updatedProfile);
      } catch (error) {
        res.status(500).json({ error: 'Failed to update profile' });
      }
      break;
      
    default:
      res.setHeader('Allow', ['GET', 'PUT']);
      res.status(405).end(\`Method \${req.method} Not Allowed\`);
  }
}`,
        dependencies: ['profile-component'],
        status: 'pending' as const,
        description: 'API endpoints for profile management'
      },
      {
        id: 'profile-schema',
        name: 'Profile Database Schema',
        type: 'database' as const,
        filePath: 'schema/profile.sql',
        content: `-- Profile table schema
CREATE TABLE profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255),
  bio TEXT,
  avatar_url VARCHAR(500),
  social_links JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX idx_profiles_user_id ON profiles(user_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_profiles_updated_at 
  BEFORE UPDATE ON profiles 
  FOR EACH ROW 
  EXECUTE FUNCTION update_updated_at_column();`,
        dependencies: [],
        status: 'pending' as const,
        description: 'Database schema for profile storage'
      }
    ],
    status: 'planning' as const,
    progress: 0,
    estimatedTime: '2-3 hours',
    complexity: 'medium' as const,
    priority: 'high' as const
  }
]

export function RealWorldWorkflow({
  onFeaturePlanned,
  onFeatureCompleted,
  showRealTimePlanning = true,
  enableAutoGeneration = true,
  className = ''
}: RealWorldWorkflowProps) {
  const [featurePlans, setFeaturePlans] = useState<FeaturePlan[]>(SAMPLE_FEATURES)
  const [isPlanning, setIsPlanning] = useState(false)
  const [planningStep, setPlanningStep] = useState('')
  const [progress, setProgress] = useState(0)
  const [activeTab, setActiveTab] = useState('planner')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedPlan, setSelectedPlan] = useState<string | null>(null)
  const [customFeature, setCustomFeature] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStep, setGenerationStep] = useState('')

  const planFeature = async (description: string) => {
    if (!description.trim()) return

    setIsPlanning(true)
    setProgress(0)
    setPlanningStep('Analyzing feature requirements...')

    try {
      // Simulate feature planning steps
      const steps = [
        'Analyzing feature requirements...',
        'Identifying required components...',
        'Planning database schema...',
        'Designing API endpoints...',
        'Creating frontend components...',
        'Setting up file structure...',
        'Generating implementation plan...',
        'Finalizing feature plan...'
      ]

      for (let i = 0; i < steps.length; i++) {
        setPlanningStep(steps[i])
        setProgress((i + 1) * 12.5)
        await new Promise(resolve => setTimeout(resolve, 300))
      }

      // Generate mock feature plan
      const featurePlan = generateFeaturePlan(description)
      setFeaturePlans(prev => [...prev, featurePlan])
      onFeaturePlanned?.(featurePlan)

    } catch (error) {
      console.error('Feature planning failed:', error)
    } finally {
      setIsPlanning(false)
      setProgress(100)
      setPlanningStep('Feature planning complete!')
    }
  }

  const generateFeaturePlan = (description: string): FeaturePlan => {
    const lowerDescription = description.toLowerCase()
    
    // Determine complexity based on description
    let complexity: 'simple' | 'medium' | 'complex' = 'simple'
    if (lowerDescription.includes('upload') || lowerDescription.includes('database') || lowerDescription.includes('api')) {
      complexity = 'medium'
    }
    if (lowerDescription.includes('dashboard') || lowerDescription.includes('admin') || lowerDescription.includes('analytics')) {
      complexity = 'complex'
    }

    // Generate components based on description
    const components: FeatureComponent[] = []
    
    if (lowerDescription.includes('component') || lowerDescription.includes('page')) {
      components.push({
        id: 'main-component',
        name: 'Main Component',
        type: 'component',
        filePath: 'components/FeatureComponent.tsx',
        content: `// Generated component for: ${description}`,
        dependencies: [],
        status: 'pending',
        description: 'Main feature component'
      })
    }
    
    if (lowerDescription.includes('api') || lowerDescription.includes('endpoint')) {
      components.push({
        id: 'api-endpoint',
        name: 'API Endpoint',
        type: 'api',
        filePath: 'pages/api/feature.ts',
        content: `// Generated API for: ${description}`,
        dependencies: ['main-component'],
        status: 'pending',
        description: 'API endpoint for feature'
      })
    }
    
    if (lowerDescription.includes('database') || lowerDescription.includes('schema')) {
      components.push({
        id: 'database-schema',
        name: 'Database Schema',
        type: 'database',
        filePath: 'schema/feature.sql',
        content: `-- Generated schema for: ${description}`,
        dependencies: [],
        status: 'pending',
        description: 'Database schema for feature'
      })
    }

    return {
      id: `plan-${Date.now()}`,
      name: `Feature: ${description.substring(0, 50)}...`,
      description,
      requirements: [
        'Responsive design',
        'Error handling',
        'Loading states',
        'User authentication'
      ],
      components,
      status: 'planning',
      progress: 0,
      estimatedTime: complexity === 'simple' ? '1-2 hours' : complexity === 'medium' ? '2-4 hours' : '4-8 hours',
      complexity,
      priority: 'medium'
    }
  }

  const generateFeatureCode = async (plan: FeaturePlan) => {
    setIsGenerating(true)
    setGenerationStep('Generating feature code...')

    try {
      // Simulate code generation
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Update plan status
      setFeaturePlans(prev => 
        prev.map(p => 
          p.id === plan.id 
            ? { ...p, status: 'completed', progress: 100 }
            : p
        )
      )

      onFeatureCompleted?.(plan)

    } catch (error) {
      console.error('Code generation failed:', error)
    } finally {
      setIsGenerating(false)
      setGenerationStep('Code generation complete!')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'planning': return 'text-blue-600 bg-blue-100'
      case 'in-progress': return 'text-yellow-600 bg-yellow-100'
      case 'completed': return 'text-green-600 bg-green-100'
      case 'testing': return 'text-purple-600 bg-purple-100'
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

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getComponentIcon = (type: string) => {
    const icons = {
      'component': Code,
      'api': Globe,
      'database': Database,
      'config': Settings,
      'test': Target,
      'documentation': BookOpen
    }
    return icons[type as keyof typeof icons] || FileText
  }

  const getComponentColor = (type: string) => {
    const colors = {
      'component': 'text-blue-600 bg-blue-100',
      'api': 'text-green-600 bg-green-100',
      'database': 'text-purple-600 bg-purple-100',
      'config': 'text-gray-600 bg-gray-100',
      'test': 'text-pink-600 bg-pink-100',
      'documentation': 'text-orange-600 bg-orange-100'
    }
    return colors[type as keyof typeof colors] || 'text-gray-600 bg-gray-100'
  }

  const renderFeaturePlan = (plan: FeaturePlan) => {
    const isSelected = selectedPlan === plan.id

    return (
      <motion.div
        key={plan.id}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className={`p-4 border rounded-lg transition-all ${
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'hover:bg-gray-50 dark:hover:bg-gray-800'
        }`}
        onClick={() => setSelectedPlan(selectedPlan === plan.id ? null : selectedPlan)}
      >
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <Workflow className="h-4 w-4" />
            <span className="font-medium">{plan.name}</span>
            <Badge className={getStatusColor(plan.status)}>
              {plan.status.toUpperCase()}
            </Badge>
            <Badge className={getComplexityColor(plan.complexity)}>
              {plan.complexity.toUpperCase()}
            </Badge>
            <Badge className={getPriorityColor(plan.priority)}>
              {plan.priority.toUpperCase()}
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation()
                generateFeatureCode(plan)
              }}
              disabled={isGenerating}
            >
              <Wand2 className="h-4 w-4 mr-1" />
              {isGenerating ? 'Generating...' : 'Generate'}
            </Button>
          </div>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">
          {plan.description}
        </div>

        <div className="flex items-center space-x-4 text-xs text-gray-500">
          <span>Progress: {plan.progress}%</span>
          <span>Est. Time: {plan.estimatedTime}</span>
          <span>Components: {plan.components.length}</span>
        </div>

        {isSelected && (
          <div className="mt-4 space-y-3">
            <div>
              <h4 className="text-sm font-medium mb-2">Requirements:</h4>
              <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                {plan.requirements.map((req, index) => (
                  <li key={index}>• {req}</li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="text-sm font-medium mb-2">Components:</h4>
              <div className="space-y-2">
                {plan.components.map((component) => {
                  const Icon = getComponentIcon(component.type)
                  return (
                    <div key={component.id} className="flex items-center space-x-2 p-2 bg-gray-50 dark:bg-gray-800 rounded">
                      <Icon className="h-4 w-4" />
                      <span className="text-sm">{component.name}</span>
                      <Badge className={getComponentColor(component.type)}>
                        {component.type}
                      </Badge>
                      <span className="text-xs text-gray-500">{component.filePath}</span>
                    </div>
                  )
                })}
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
      <Card className="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center space-x-2">
                <Workflow className="h-6 w-6 text-indigo-600" />
                <span>Real-World Workflow</span>
              </CardTitle>
              <CardDescription>
                Plan and develop complete features with all necessary components
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
          {/* Planning Status */}
          {isPlanning && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-indigo-50 dark:bg-indigo-900/20 rounded-lg p-4"
            >
              <div className="flex items-center space-x-3 mb-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-indigo-600"></div>
                <span className="text-sm font-medium text-indigo-800 dark:text-indigo-200">
                  {planningStep}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </motion.div>
          )}

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
            </motion.div>
          )}
        </CardContent>
      </Card>

      {/* Real-World Workflow */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="planner">Planner</TabsTrigger>
          <TabsTrigger value="features">Features</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
          <TabsTrigger value="progress">Progress</TabsTrigger>
        </TabsList>

        <TabsContent value="planner" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <MessageSquare className="h-4 w-4" />
                  <span>Feature Planning</span>
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
                      placeholder="e.g., Create a user profile page with avatar upload, bio editing, and social links"
                      className="min-h-[100px]"
                    />
                  </div>
                  <Button
                    onClick={() => planFeature(customFeature)}
                    disabled={isPlanning || !customFeature.trim()}
                    className="w-full"
                  >
                    <Workflow className="h-4 w-4 mr-2" />
                    {isPlanning ? 'Planning...' : 'Plan Feature'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Planning Tips</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Be Specific:</strong> Include details about functionality, UI, and data requirements
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Mention Components:</strong> Specify if you need API endpoints, database changes, or frontend components
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <strong>Include Context:</strong> Mention the tech stack or framework you're using
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="features" className="space-y-4">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Badge variant="outline">
                  Total Features: {featurePlans.length}
                </Badge>
                <Badge variant="outline" className="text-green-600">
                  Completed: {featurePlans.filter(p => p.status === 'completed').length}
                </Badge>
                <Badge variant="outline" className="text-blue-600">
                  In Progress: {featurePlans.filter(p => p.status === 'in-progress').length}
                </Badge>
              </div>
            </div>

            <div className="space-y-3">
              {featurePlans.map(renderFeaturePlan)}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="templates" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm flex items-center space-x-2">
                <Target className="h-4 w-4" />
                <span>Feature Templates</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {SAMPLE_FEATURES.map((feature) => (
                  <div
                    key={feature.id}
                    className="p-3 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer transition-all"
                    onClick={() => planFeature(feature.description)}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium text-sm">{feature.name}</div>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          {feature.description}
                        </p>
                        <div className="flex items-center space-x-2 mt-2">
                          <Badge className={getComplexityColor(feature.complexity)}>
                            {feature.complexity}
                          </Badge>
                          <Badge className={getPriorityColor(feature.priority)}>
                            {feature.priority}
                          </Badge>
                          <span className="text-xs text-gray-500">{feature.estimatedTime}</span>
                        </div>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          planFeature(feature.description)
                        }}
                        disabled={isPlanning}
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

        <TabsContent value="progress" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <TrendingUp className="h-4 w-4" />
                  <span>Overall Progress</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Total Features</span>
                    <span className="font-medium">{featurePlans.length}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Completed</span>
                    <span className="font-medium text-green-600">
                      {featurePlans.filter(p => p.status === 'completed').length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">In Progress</span>
                    <span className="font-medium text-blue-600">
                      {featurePlans.filter(p => p.status === 'in-progress').length}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Success Rate</span>
                    <span className="font-medium text-green-600">95%</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Workflow className="h-4 w-4" />
                  <span>Feature Types</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {['simple', 'medium', 'complex'].map((complexity) => {
                    const count = featurePlans.filter(p => p.complexity === complexity).length
                    return (
                      <div key={complexity} className="flex justify-between items-center">
                        <span className="text-sm">{complexity}</span>
                        <Badge className={getComplexityColor(complexity)}>
                          {count}
                        </Badge>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-sm flex items-center space-x-2">
                  <Lightbulb className="h-4 w-4" />
                  <span>Insights</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="text-sm">
                    <strong>Avg. Time:</strong> 2.5 hours per feature
                  </div>
                  <div className="text-sm">
                    <strong>Components:</strong> 3.2 per feature
                  </div>
                  <div className="text-sm">
                    <strong>Success Rate:</strong> 95% completion rate
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
